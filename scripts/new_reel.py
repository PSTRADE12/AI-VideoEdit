#!/usr/bin/env python3
"""Create vertical reel sequence from a media item + 16:9->9:16 fill.

Usage:
  python scripts/new_reel.py <item-id> [name] [--w 1080 --h 1920 --fps 30]

Steps (mirrors proven 2026-10-11 session):
  1. file.newSequence fromItem=<id> w/h/fps  -> sequence id
  2. sequence.open -> make active
  3. motion scale 177.8 on the main clip (1920x1080 source fills 1080x1920,
     center-crop sides; position stays 540,960).
Run via fc.py or paste the printed commands.
"""
import subprocess
import sys

import fc  # noqa: F401  (keeps CLI constant docs together)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    item = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else "Reel 9x16"
    print("1) python scripts/fc.py exec file.newSequence "
          f'name="{name}" width=1080 height=1920 fps=30 fromItem={item}')
    print("2) python scripts/fc.py exec sequence.open item=<new-sequence-id>")
    print("3) python scripts/fc.py exec effects.setParam clip=<main-clip> "
          "effect=motion param=scale value=177.8")
    print("Find <main-clip>: python scripts/fc.py inspect  (Video 1 first clip)")


if __name__ == "__main__":
    main()
