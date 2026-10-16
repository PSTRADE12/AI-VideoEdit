#!/usr/bin/env python3
"""Words JSON -> true karaoke single-word pop batch (centered, colored).

Proven recipe 2026-10-11 (fixes two real bugs — see MEMORY.md):
  - point text (NO box), align center applied AFTER creation,
    position [540,1350] lower-third on 1080x1920. Box mode puts position
    at top-LEFT, which pushed quads to x=1460 (off-screen).
  - one clip PER WORD (not 3-word chunks): static setCharStyle cannot
    animate within a clip, so per-word clips are the only true karaoke.

Usage:
  python scripts/wordpop.py <words.json> [out-prefix] [--pos=x,y --size=N]
  # defaults: pos 540,1350 + size 104 (1080x1920 house style).
  # 4K vertical 2160x3840: --pos=1080,2700 --size=208.
  # writes <prefix>.new.jsonl, prints clip-id capture + color + align steps
  python scripts/fc.py run <prefix>.new.jsonl > new_out.txt
  # then build color/align batches with --color/--align using captured ids:
  python scripts/wordpop.py <words.json> [out-prefix] --color single_ids.json
  python scripts/wordpop.py <words.json> [out-prefix] --align single_ids.json

Colors: keywords (len>=5 or mic/noise/quality/...) yellow #FFD60A else white.
Font: Bahnschrift Bold 104 (most modern geometric on stock Windows).
"""
import json
import sys

TICKS_PER_SEC = 254016000000
KEYWORDS = {"microphone", "mic", "noise", "reduction", "quality", "videos",
            "video", "terminal", "test", "hello", "received", "ready",
            "soon", "good", "another", "connecting", "recording",
            "visible", "coming", "together", "impact"}


def color_of(text):
    clean = text.strip(",.!?").lower()
    return "yellow" if (len(clean) >= 5 or clean in KEYWORDS) else "white"


def build_new(words, prefix, pos=(540, 1350), size=104):
    lines = []
    for i, w in enumerate(words):
        s, e = w["start"], w["end"]
        if i + 1 < len(words):
            e = min(e, words[i + 1]["start"] - 0.03)
        dur = max(0.25, round(e - s, 3))
        lines.append({"id": "graphics.newText", "params": {
            "text": w["text"], "size": size, "font": "Bahnschrift",
            "fontStyle": "Bold", "position": list(pos),
            "seconds": dur, "time": int(s * TICKS_PER_SEC)}})
    path = prefix + ".new.jsonl"
    with open(path, "w") as f:
        for l in lines:
            f.write(json.dumps(l) + "\n")
    print(f"new-text batch: {len(lines)} -> {path}")
    print("run: python scripts/fc.py run", path, "> new_out.txt")
    print("then: --ids new_out.txt (utf-16!) to extract clip ids")


def build_color(words, ids_path, prefix):
    raw = open(ids_path, encoding="utf-16").read().splitlines()
    ids = [json.loads(l)["result"]["clip"] for l in raw if l.strip()
           and json.loads(l).get("ok")]
    assert len(ids) == len(words), f"{len(ids)} ids vs {len(words)} words"
    with open(prefix + ".color.jsonl", "w") as f:
        for clip, w in zip(ids, words):
            c = "#FFD60A" if color_of(w["text"]) == "yellow" else "#FFFFFF"
            f.write(json.dumps({"id": "graphics.setCharStyle", "params": {
                "clip": clip, "start": 0, "end": len(w["text"]),
                "style": {"color": c, "bold": True}}}) + "\n")
    with open(prefix + ".align.jsonl", "w") as f:
        for clip in ids:
            f.write(json.dumps({"id": "graphics.set", "params": {
                "clip": clip, "props": {"align": "center"}}}) + "\n")
    json.dump(ids, open(prefix + ".ids.json", "w"))
    print(f"color+align batches for {len(ids)} clips")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(2)
    words = json.load(open(args[0]))
    prefix = args[1] if len(args) > 1 else "transcripts/pop"
    pos = (540, 1350)
    size = 104
    for a in sys.argv[1:]:
        if a.startswith("--pos="):
            x, y = a.split("=", 1)[1].split(",")
            pos = (int(x), int(y))
        elif a.startswith("--size="):
            size = int(a.split("=", 1)[1])
    if "--color" in sys.argv:
        build_color(words, sys.argv[sys.argv.index("--color") + 1], prefix)
    elif "--align" in sys.argv:
        build_color(words, sys.argv[sys.argv.index("--align") + 1], prefix)
    else:
        build_new(words, prefix, pos, size)


if __name__ == "__main__":
    main()
