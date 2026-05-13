#!/usr/bin/env python3
"""Dependency check for ppt-deep-search.

The skill uses only Python standard library code. This script exists so the
host AgentWorkspace can verify the skill through a stable entry point.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify ppt-deep-search dependencies.")
    parser.add_argument("--skip-services", action="store_true", help="Accepted for protocol compatibility; no services are used.")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    required = [
        root / "SKILL.md",
        root / "scripts" / "validate_ppt_content_brief.py",
        root / "agents" / "openai.yaml",
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

    print("[OK] Python standard library dependencies available.")
    print("[OK] No external services, packages, browsers, or hardware dependencies required.")
    if args.skip_services:
        print("[OK] --skip-services accepted; no service checks were needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
