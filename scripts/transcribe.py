#!/usr/bin/env python3
"""Transcribe media with faster-whisper (word timestamps) -> words JSON.

Needs a Python with faster-whisper (see requirements-transcribe.txt):
  python scripts/setup_check.py            # shows which interpreter it found
  <transcribe-python> scripts/transcribe.py <media> [out.json] [--model base] [--lang en]

Output JSON: [{"text": str, "start": sec, "end": sec}, ...]
"""
import json
import sys

TICKS_PER_SEC = 254016000000


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opts = {a.split("=")[0]: a.split("=", 1)[1] for a in sys.argv[1:]
            if a.startswith("--")}
    if not args:
        print(__doc__)
        sys.exit(2)
    media = args[0]
    out = args[1] if len(args) > 1 else "transcripts/words.json"
    model_name = opts.get("--model", "base")
    lang = opts.get("--lang", "en").lstrip("=")

    from faster_whisper import WhisperModel
    print("loading faster-whisper/base ...", flush=True)
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    print("transcribing ...", flush=True)
    segments, info = model.transcribe(
        media, language=lang, word_timestamps=True, vad_filter=True)
    words = []
    for s in segments:
        for w in (s.words or []):
            words.append({"text": w.word.strip(),
                          "start": round(w.start, 3),
                          "end": round(w.end, 3)})
    print(f"LANG={info.language} WORDS={len(words)}")
    with open(out, "w") as f:
        json.dump(words, f, indent=1)
    print(f"saved {out}")


if __name__ == "__main__":
    main()
