#!/usr/bin/env python3
"""ffmpeg silencedetect scan -> silence JSON (no ML model needed).

Usage:
  python scripts/silence_scan.py <media> [out.json] [--db -30] [--dur 1.0]

Proven 2026-10-11: 100s mic-test -> 16 pauses >1.0s (~33s total).
Use to plan cuts when transcript/removePauses is unavailable.
Pair with: fc.py exec timeline.razor time=<ticks> + edit.rippleDelete.
"""
import json
import re
import subprocess
import sys


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(2)
    media, out = args[0], args[1] if len(args) > 1 else "transcripts/silences.json"
    db = "-30dB"
    dur = "1.0"
    for a in sys.argv[1:]:
        if a.startswith("--db"):
            db = a.split("=", 1)[1]
        if a.startswith("--dur"):
            dur = a.split("=", 1)[1]
    p = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", media,
         "-af", f"silencedetect=noise={db}:d={dur}", "-f", "null", "-"],
        capture_output=True, text=True, timeout=300)
    log = p.stderr
    starts = [float(m) for m in re.findall(r"silence_start: ([\d.]+)", log)]
    ends = [(float(m.group(1)), float(m.group(2))) for m in
            re.finditer(r"silence_end: ([\d.]+) \| silence_duration: ([\d.]+)", log)]
    silences = [{"start": s, "end": e, "dur": round(d, 3)}
                for s, (e, d) in zip(starts, ends)]
    total = round(sum(s["dur"] for s in silences), 2)
    print(f"SILENCES={len(silences)} TOTAL_S={total}")
    for s in silences[:20]:
        print(f"  {s['start']:.2f}-{s['end']:.2f} ({s['dur']}s)")
    json.dump(silences, open(out, "w"), indent=1)
    print(f"saved {out}")


if __name__ == "__main__":
    main()
