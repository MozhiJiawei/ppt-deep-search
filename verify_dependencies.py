#!/usr/bin/env python3
"""Verify external dependencies for ppt-deep-search.

This skill intentionally has a small dependency surface. Repository files,
validators, fixtures, and self-tests are internal health checks, not user
environment dependencies, so they are intentionally outside this dependency
check.
"""

from __future__ import annotations

import argparse
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify external dependencies for ppt-deep-search.")
    parser.add_argument("--skip-services", action="store_true", help="Accepted for protocol compatibility; no services are used.")
    args = parser.parse_args()

    if sys.version_info < (3, 9):
        print(f"[ERROR] Python 3.9+ is required; found {sys.version.split()[0]}")
        return 1

    print(f"[OK] Python {sys.version.split()[0]} is available.")
    print("[OK] No required external packages, services, browsers, or hardware dependencies.")
    print("[INFO] Network access is task-dependent only when supplemental web sources are requested.")
    if args.skip_services:
        print("[OK] --skip-services accepted; no service checks were needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
