#!/usr/bin/env python3
"""Zero-dependency preview server for source-understanding HTML reports."""

from __future__ import annotations

import base64
import hashlib
import http.server
import os
import socket
import sys
import threading
import time
import webbrowser
from pathlib import Path


PORT = int(os.environ.get("HTML_REVIEW_PORT", "8043"))
WS_PORT = PORT + 1

INJECT = f"""<script>
(function(){{
  var ws = new WebSocket("ws://localhost:{WS_PORT}");
  ws.onmessage = function(e) {{
    if (e.data === "reload") {{
      sessionStorage.setItem("_html_review_scroll", String(window.scrollY));
      location.reload();
    }}
  }};
  ws.onclose = function() {{ setTimeout(function() {{ location.reload(); }}, 2000); }};
  window.addEventListener("load", function() {{
    var y = sessionStorage.getItem("_html_review_scroll");
    if (y) {{
      window.scrollTo(0, parseInt(y, 10));
      sessionStorage.removeItem("_html_review_scroll");
    }}
  }});
}})();
</script>"""

_html_path: Path | None = None


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        assert _html_path is not None
        if self.path in ("/", f"/{_html_path.name}"):
            content = _html_path.read_text(encoding="utf-8", errors="replace")
            if "</body>" in content:
                content = content.replace("</body>", INJECT + "</body>")
            data = content.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        super().do_GET()

    def log_message(self, fmt: str, *args: object) -> None:
        return


def _websocket_accept_key(key: str) -> str:
    digest = hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-5AB5DC11650A").encode("utf-8")).digest()
    return base64.b64encode(digest).decode("ascii")


def ws_server() -> None:
    assert _html_path is not None
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("localhost", WS_PORT))
    srv.listen(5)
    clients: list[socket.socket] = []

    def accept_loop() -> None:
        while True:
            conn, _ = srv.accept()
            data = conn.recv(4096).decode("utf-8", errors="replace")
            key = ""
            for line in data.split("\r\n"):
                if line.startswith("Sec-WebSocket-Key:"):
                    key = line.split(": ", 1)[1].strip()
                    break
            conn.send(
                (
                    "HTTP/1.1 101 Switching Protocols\r\n"
                    "Upgrade: websocket\r\n"
                    "Connection: Upgrade\r\n"
                    f"Sec-WebSocket-Accept: {_websocket_accept_key(key)}\r\n\r\n"
                ).encode("utf-8")
            )
            clients.append(conn)

    threading.Thread(target=accept_loop, daemon=True).start()
    last = hashlib.md5(_html_path.read_bytes()).hexdigest()
    while True:
        time.sleep(0.5)
        try:
            cur = hashlib.md5(_html_path.read_bytes()).hexdigest()
        except FileNotFoundError:
            continue
        if cur == last:
            continue
        last = cur
        frame = b"\x81" + bytes([len(b"reload")]) + b"reload"
        dead: list[socket.socket] = []
        for client in clients:
            try:
                client.send(frame)
            except Exception:
                dead.append(client)
        for client in dead:
            clients.remove(client)
        print(f"  reloaded ({time.strftime('%H:%M:%S')})")


def main() -> int:
    global _html_path
    if len(sys.argv) < 2:
        print("Usage: serve_html_review.py <source_understanding_review.html>")
        return 1

    _html_path = Path(sys.argv[1]).resolve()
    if not _html_path.exists():
        print(f"Not found: {_html_path}")
        return 1

    os.chdir(_html_path.parent)
    threading.Thread(target=ws_server, daemon=True).start()
    server = http.server.HTTPServer(("localhost", PORT), Handler)
    url = f"http://localhost:{PORT}/"
    print(f"Serving {_html_path.name} on {url}")
    print("Watching for changes. Press Ctrl+C to stop.")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
