#!/usr/bin/env python3
"""Dependency check for ppt-deep-search.

This script is the stable host-facing dependency gate for the skill. Most
validators use only the Python standard library; Source Understanding screenshot
export also requires local Playwright with Chromium.
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
        root / ".gitmodules",
        root / "docs" / "architecture_design.md",
        root / "scripts" / "hitl_json_to_brief_skeleton.py",
        root / "scripts" / "validate_ppt_content_brief.py",
        root / "scripts" / "validate_markdown_size.py",
        root / "scripts" / "validate_source_understanding_html.py",
        root / "agents" / "openai.yaml",
        root / "references" / "evidence-principle.md",
        root / "references" / "source-understanding-html-ppt.md",
        root / "references" / "ppt-brief-hitl.md",
        root / "web-article-capture" / "SKILL.md",
        root / "web-article-capture" / "scripts" / "validate_capture_package.py",
        root / "web-article-capture" / "references" / "output-contract.md",
        root / "html-ppt-skill" / "SKILL.md",
        root / "web-article-capture" / "forward-tests" / "nvidia-pc" / "candidate" / "prompt.md",
        root / "web-article-capture" / "forward-tests" / "nvidia-pc" / "candidate" / "input" / "urls.txt",
        root / "web-article-capture" / "forward-tests" / "nvidia-pc" / "judge" / "rubric.md",
        root / "forward-tests" / "ppt-deep-search" / "README.md",
        root / "forward-tests" / "ppt-deep-search" / "main-agent-prompt.md",
    ]
    for case_dir in sorted((root / "forward-tests" / "ppt-deep-search").glob("*-hitl")):
        required.extend(
            [
                case_dir / "main-agent-prompt.md",
                case_dir / "candidate" / "prompt.md",
                case_dir / "judge" / "rubric.md",
                case_dir / "case-manifest.json",
            ]
        )
    missing = [str(path.relative_to(root)) for path in required if not path.exists()]
    if missing:
        print("[ERROR] Missing required files:")
        for item in missing:
            print(f"  - {item}")
        return 1

    if sys.version_info < (3, 9):
        print(f"[ERROR] Python 3.9+ is required; found {sys.version.split()[0]}")
        return 1

    markdown_size_self_test = subprocess.run(
        [sys.executable, str(root / "scripts" / "validate_markdown_size.py"), "--self-test"],
        cwd=root,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if markdown_size_self_test.returncode != 0:
        print("[ERROR] Markdown size validator self-test failed:")
        safe_print((markdown_size_self_test.stdout + markdown_size_self_test.stderr).strip())
        return 1
    safe_print(markdown_size_self_test.stdout.strip())

    markdown_size_check = subprocess.run(
        [sys.executable, str(root / "scripts" / "validate_markdown_size.py"), str(root)],
        cwd=root,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if markdown_size_check.returncode != 0:
        safe_print((markdown_size_check.stdout + markdown_size_check.stderr).strip())
        return 1
    safe_print(markdown_size_check.stdout.strip())

    ppt_content_brief_self_test = subprocess.run(
        [sys.executable, str(root / "scripts" / "validate_ppt_content_brief.py"), "--self-test"],
        cwd=root,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if ppt_content_brief_self_test.returncode != 0:
        print("[ERROR] PPT Content Brief validator self-test failed:")
        safe_print((ppt_content_brief_self_test.stdout + ppt_content_brief_self_test.stderr).strip())
        return 1
    safe_print(ppt_content_brief_self_test.stdout.strip())

    hitl_skeleton_self_test = subprocess.run(
        [sys.executable, str(root / "scripts" / "hitl_json_to_brief_skeleton.py"), "--self-test"],
        cwd=root,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if hitl_skeleton_self_test.returncode != 0:
        print("[ERROR] HITL JSON to brief skeleton self-test failed:")
        safe_print((hitl_skeleton_self_test.stdout + hitl_skeleton_self_test.stderr).strip())
        return 1
    safe_print(hitl_skeleton_self_test.stdout.strip())

    source_understanding_self_test = subprocess.run(
        [sys.executable, str(root / "scripts" / "validate_source_understanding_html.py"), "--self-test"],
        cwd=root,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if source_understanding_self_test.returncode != 0:
        print("[ERROR] Source Understanding HTML image exporter self-test failed:")
        safe_print((source_understanding_self_test.stdout + source_understanding_self_test.stderr).strip())
        return 1
    safe_print(source_understanding_self_test.stdout.strip())

    playwright_check = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "from playwright.sync_api import sync_playwright\n"
                "with sync_playwright() as p:\n"
                "    browser = p.chromium.launch()\n"
                "    browser.close()\n"
                "print('[OK] Python Playwright + Chromium available for Source Understanding image export.')\n"
            ),
        ],
        cwd=root,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if playwright_check.returncode != 0:
        print("[ERROR] Source Understanding image export requires local Python Playwright + Chromium:")
        print("  - Problem: Playwright import or Chromium launch failed.")
        print(
            "  - React: Install with `python -m pip install playwright` and "
            "`python -m playwright install chromium`, then rerun `python verify_dependencies.py`."
        )
        safe_print((playwright_check.stdout + playwright_check.stderr).strip())
        return 1
    safe_print(playwright_check.stdout.strip())

    print("[OK] Python standard library dependencies available for text validators.")
    print("[OK] No required external services or hardware dependencies.")
    print("[OK] Source Understanding HTML screenshot export is part of ppt-deep-search runtime.")
    if args.skip_services:
        print("[OK] --skip-services accepted; local dependency checks still ran.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
