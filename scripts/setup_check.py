#!/usr/bin/env python3
"""Clone-and-run health check. Usage: python scripts/setup_check.py [--bridge]

Checks (no side effects, never edits a timeline):
  FilmCraft CLI+GUI binaries, ffmpeg, python + faster-whisper interpreter,
  scripts/ imports, and optionally the live bridge (only with --bridge).
Exit 0 = ready to edit, 1 = something to install/start (follow the hint).
"""
import os
import shutil
import socket
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from config import bridge, find_app, find_cli, find_transcribe_python

ok = True


def check(name, passed, hint=""):
    global ok
    print(("PASS " if passed else "FAIL ") + name + (f" — {hint}" if hint and not passed else ""))
    if not passed:
        ok = False


def run(cmd, timeout=30):
    p = subprocess.run(cmd, capture_output=True, timeout=timeout)
    return p.returncode, (p.stdout.decode(errors="ignore") + p.stderr.decode(errors="ignore"))


cli = find_cli()
app = find_app()
tpy = find_transcribe_python()
check("filmcraft-cli binary exists", os.path.isfile(cli), f"set FILMCRAFT_CLI or install FilmCraft (see README §1): {cli}")
if os.path.isfile(cli):
    try:
        rc, out = run([cli, "--version"])
        ver = next((l.strip() for l in out.splitlines() if l.strip()), "?")
        check("filmcraft-cli runs", rc == 0, ver)
        print(f"     version: {ver}")
    except Exception as e:
        check("filmcraft-cli runs", False, str(e))
check("filmcraft GUI binary exists", os.path.isfile(app), f"set FILMCRAFT_APP or install FilmCraft: {app}")
check("ffmpeg on PATH", shutil.which("ffmpeg") is not None, "install ffmpeg 7+ and add to PATH")
check("transcribe python exists", os.path.isfile(tpy) if os.path.isabs(tpy or "") else shutil.which(tpy or "") is not None, "set TRANSCRIBE_PYTHON to a python with faster-whisper")
try:
    rc, _ = run([tpy, "-c", "import faster_whisper"], timeout=60)
    check("faster-whisper import", rc == 0, f"run: {tpy} -m pip install -r requirements-transcribe.txt")
except Exception as e:
    check("faster-whisper import", False, str(e))
try:
    import config  # noqa
    check("scripts/config imports", True)
except Exception as e:
    check("scripts/config imports", False, str(e))

for d in ("transcripts", "exports", "media"):
    p = os.path.join(ROOT, d)
    check(f"folder {d}/", os.path.isdir(p), f"create {p}")

if "--bridge" in sys.argv:
    b = bridge() or "127.0.0.1:9876"
    host, port = b.rsplit(":", 1)
    s = socket.socket()
    s.settimeout(2)
    try:
        s.connect((host, int(port)))
        check(f"live bridge {b}", True)
    except OSError:
        check(f"live bridge {b}", False, f"start: \"{app}\" --control {port} (or python scripts/start_live.py)")
    finally:
        s.close()
else:
    print("SKIP live bridge (run with --bridge when FilmCraft GUI is open)")

print("\nREADY" if ok else "\nNOT READY — fix FAIL lines above (README §4 troubleshooting)")
sys.exit(0 if ok else 1)
