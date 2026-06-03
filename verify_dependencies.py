#!/usr/bin/env python3
"""Dependency check for ppt-deep-search.

The skill uses only Python standard library code. This script exists so the
host AgentWorkspace can verify the skill through a stable entry point.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def safe_print(text: str) -> None:
    print(text.encode(sys.stdout.encoding or "utf-8", errors="replace").decode(sys.stdout.encoding or "utf-8", errors="replace"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify ppt-deep-search dependencies.")
    parser.add_argument("--skip-services", action="store_true", help="Accepted for protocol compatibility; no services are used.")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    required = [
        root / "SKILL.md",
        root / "docs" / "architecture_design.md",
        root / "scripts" / "validate_ppt_content_brief.py",
        root / "scripts" / "validate_html_review.py",
        root / "scripts" / "validate_html_review_data.py",
        root / "agents" / "openai.yaml",
        root / "references" / "html-review-surface.md",
        root / "references" / "html-review-data-model.md",
        root / "references" / "html-review-report-kit.md",
        root / "references" / "html-review-pattern-library.md",
        root / "scripts" / "serve_html_review.py",
    ]
    missing = [str(path.relative_to(root)) for path in required if not path.exists()]
    if missing:
        print("[ERROR] Missing required files:")
        for item in missing:
            print(f"  - {item}")
        return 1

    if sys.version_info < (3, 9):
        print(f"[ERROR] Python 3.9+ is required; found {sys.version.split()[0]}")
        return 1

    html_review_self_test = subprocess.run(
        [sys.executable, str(root / "scripts" / "validate_html_review.py"), "--self-test"],
        cwd=root,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if html_review_self_test.returncode != 0:
        print("[ERROR] HTML review validator self-test failed:")
        safe_print((html_review_self_test.stdout + html_review_self_test.stderr).strip())
        return 1
    safe_print(html_review_self_test.stdout.strip())

    html_review_data_self_test = subprocess.run(
        [sys.executable, str(root / "scripts" / "validate_html_review_data.py"), "--self-test"],
        cwd=root,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if html_review_data_self_test.returncode != 0:
        print("[ERROR] HTML review data validator self-test failed:")
        safe_print((html_review_data_self_test.stdout + html_review_data_self_test.stderr).strip())
        return 1
    safe_print(html_review_data_self_test.stdout.strip())

    print("[OK] Python standard library dependencies available.")
    print("[OK] No required external services, packages, browsers, or hardware dependencies.")
    print("[OK] HTML review generation may optionally use CDN assets and the local preview server.")
    if args.skip_services:
        print("[OK] --skip-services accepted; no service checks were needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
