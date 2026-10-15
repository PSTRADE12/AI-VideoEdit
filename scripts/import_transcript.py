#!/usr/bin/env python3
"""Words JSON -> FilmCraft transcript.set batch file (ticks).

Usage:
  python scripts/import_transcript.py <words.json> <item-id> [out.jsonl]

Then:  python scripts/fc.py run <out.jsonl>
Verify: python scripts/fc.py exec transcript.inspect
"""
import json
import sys

TICKS_PER_SEC = 254016000000


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    words = json.load(open(sys.argv[1]))
    item = int(sys.argv[2])
    out = sys.argv[3] if len(sys.argv) > 3 else "transcripts/import.jsonl"
    payload = {"id": "transcript.set", "params": {
        "item": item, "transcript": {
            "language": "en",
            "speakers": [{"name": "Speaker 1"}],
            "words": [{"text": w["text"],
                       "start": int(w["start"] * TICKS_PER_SEC),
                       "end": int(w["end"] * TICKS_PER_SEC)}
                      for w in words]}}}
    with open(out, "w") as f:
        f.write(json.dumps(payload) + "\n")
    print(f"prepared {len(words)} words for item {item} -> {out}")


if __name__ == "__main__":
    main()
