#!/usr/bin/env python3
"""Portable path resolver — no hardcoded user/machine paths.

Search order for every binary:
  1. env var override
  2. repo-local vendor/ or tools/ (portable copy, git-ignored)
  3. standard install location
  4. PATH lookup

Env vars:
  FILMCRAFT_CLI     filmcraft-cli binary (bridge + headless engine)
  FILMCRAFT_APP     filmcraft GUI binary (live control mode)
  FILMCRAFT_BRIDGE  host:port, or empty for headless (default 127.0.0.1:9876)
  FILMCRAFT_EXTRA   extra flags, e.g. "--demo"
  TRANSCRIBE_PYTHON python with faster-whisper (auto-detected if unset)
"""
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_CLI = r"C:\Program Files\FilmCraft\filmcraft-cli.exe"
DEFAULT_APP = r"C:\Program Files\FilmCraft\filmcraft.exe"
DEFAULT_BRIDGE = "127.0.0.1:9876"


def _first_existing(*paths):
    for p in paths:
        if p and os.path.isfile(p):
            return p
    return None


def find_cli():
    return (
        os.environ.get("FILMCRAFT_CLI")
        or _first_existing(
            os.path.join(ROOT, "vendor", "filmcraft-cli.exe"),
            os.path.join(ROOT, "tools", "filmcraft-cli.exe"),
            DEFAULT_CLI,
        )
        or shutil.which("filmcraft-cli")
        or DEFAULT_CLI
    )


def find_app():
    return (
        os.environ.get("FILMCRAFT_APP")
        or _first_existing(
            os.path.join(ROOT, "vendor", "filmcraft.exe"),
            os.path.join(ROOT, "tools", "filmcraft.exe"),
            DEFAULT_APP,
        )
        or shutil.which("filmcraft")
        or DEFAULT_APP
    )


def find_transcribe_python():
    """Python interpreter that has faster-whisper. Order: env, common 3.11 spots, current."""
    env = os.environ.get("TRANSCRIBE_PYTHON")
    if env:
        return env
    candidates = [
        shutil.which("python3.11"),
        os.path.expandvars(r"%LocalAppData%\Programs\Python\Python311\python.exe"),
        os.path.expandvars(r"%ProgramFiles%\Python311\python.exe"),
        "/usr/bin/python3.11",
        "/usr/local/bin/python3.11",
    ]
    for c in candidates:
        if c and os.path.isfile(c):
            return c
    return shutil.which("python") or "python"


def bridge():
    return os.environ.get("FILMCRAFT_BRIDGE", DEFAULT_BRIDGE)


def extra_flags():
    raw = os.environ.get("FILMCRAFT_EXTRA", "")
    return raw.split() if raw else []
