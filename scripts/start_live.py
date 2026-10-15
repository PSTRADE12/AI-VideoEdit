#!/usr/bin/env python3
"""Start the FilmCraft GUI in live-control mode, wait for the port, verify.

Usage:
  python scripts/start_live.py [--port 9876] [--project "<path>.fcproj" | --demo]

Opens the GUI with --control <port> (visible window, non-headless),
polls 127.0.0.1:<port> until it listens (or 60s timeout), then runs
`fc.py inspect` as proof the agent sees the live timeline.
Idempotent: if the port already listens, it just verifies and exits.
Binary resolves via config.py (env FILMCRAFT_APP → vendor/ → install → PATH).
"""
import os
import socket
import subprocess
import sys
import time

try:
    from config import bridge as _default_bridge, find_app as _find_app
    APP = os.environ.get("FILMCRAFT_APP") or _find_app()
    _DEFAULT_PORT = (_default_bridge() or "127.0.0.1:9876").split(":")[-1]
except ImportError:
    APP = os.environ.get("FILMCRAFT_APP",
                         r"C:\Program Files\FilmCraft\filmcraft.exe")
    _DEFAULT_PORT = "9876"


def resolve_port(argv):
    if "--port" in argv:
        return argv[argv.index("--port") + 1]
    return _DEFAULT_PORT


def listening(port):
    s = socket.socket()
    s.settimeout(1)
    try:
        s.connect(("127.0.0.1", int(port)))
        return True
    except OSError:
        return False
    finally:
        s.close()


def main():
    port = resolve_port(sys.argv)
    if listening(port):
        print(f"already live on 127.0.0.1:{port}")
    else:
        cmd = [APP, "--control", port]
        if "--demo" in sys.argv:
            cmd.append("--demo")
        if "--project" in sys.argv:
            cmd.append(sys.argv[sys.argv.index("--project") + 1])
        print("starting:", " ".join(f'"{c}"' if " " in c else c for c in cmd))
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
        for _ in range(60):
            if listening(port):
                break
            time.sleep(1)
        if not listening(port):
            print(f"port {port} did not open in 60s", file=sys.stderr)
            sys.exit(1)
        print(f"live on 127.0.0.1:{port}")
    here = os.path.dirname(os.path.abspath(__file__))
    subprocess.run([sys.executable, os.path.join(here, "fc.py"), "inspect"],
                   check=False)


if __name__ == "__main__":
    main()
