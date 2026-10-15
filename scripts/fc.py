#!/usr/bin/env python3
"""FilmCraft bridge wrapper. Single entry for every edit op.

Usage:
  python scripts/fc.py inspect
  python scripts/fc.py exec <id> [key=value ...]
  python scripts/fc.py run <script.jsonl>
  python scripts/fc.py describe <id>
  python scripts/fc.py commands [filter]

Env:
  FILMCRAFT_CLI    path to filmcraft-cli.exe (default: C:\\Program Files\\FilmCraft\\filmcraft-cli.exe)
  FILMCRAFT_BRIDGE host:port of live app (default: 127.0.0.1:9876).
    Omit --bridge (empty string) for headless mode; add --project/--demo flags
    via FILMCRAFT_EXTRA, e.g. FILMCRAFT_EXTRA="--demo".
"""
import os
import subprocess
import sys

try:
    from config import bridge as _bridge, extra_flags as _extra, find_cli as _find_cli
    CLI = os.environ.get("FILMCRAFT_CLI") or _find_cli()
    BRIDGE = _bridge()
    EXTRA = _extra()
except ImportError:  # script run without package context
    CLI = os.environ.get(
        "FILMCRAFT_CLI", r"C:\Program Files\FilmCraft\filmcraft-cli.exe")
    BRIDGE = os.environ.get("FILMCRAFT_BRIDGE", "127.0.0.1:9876")
    EXTRA = os.environ.get("FILMCRAFT_EXTRA", "").split() if os.environ.get(
        "FILMCRAFT_EXTRA") else []

TICKS_PER_SEC = 254016000000


def run_cli(*args):
    cmd = [CLI]
    if BRIDGE:
        cmd += ["--bridge", BRIDGE]
    cmd += EXTRA + list(args)
    p = subprocess.run(cmd, capture_output=True, timeout=120)
    out = p.stdout.decode(errors="ignore")
    err = p.stderr.decode(errors="ignore")
    if out:
        print(out, end="" if out.endswith("\n") else "\n")
    if p.returncode != 0:
        print(err, file=sys.stderr)
        sys.exit(p.returncode)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    run_cli(*sys.argv[1:])


if __name__ == "__main__":
    main()
