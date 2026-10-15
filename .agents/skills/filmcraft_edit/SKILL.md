# Skill: filmcraft_edit
Trigger: any user request to cut, caption, title, reframe, or export video.
Workflow (live bridge, proven 2026-10-11):
1. `python scripts/fc.py inspect` — confirm active sequence + clip ids. Never guess ids.
2. Read-only first: `describe <id>` before any destructive `exec`.
3. Destructive ops (rippleDelete, edit.clear, removePauses) need user confirmation OR operate on a NEW reel copy, never the only original.
4. Time unit is ticks: 254016000000/sec. `seconds=` accepted by most timeline commands.
5. Captions: karaoke = one `graphics.newText` PER WORD (point text, no box, align center AFTER creation, [540,1350] on 1080x1920). Never 3-word chunks with static highlight. Never box-positioned text at x=540 (top-left bug → off-screen).
6. After ANY graphics batch: verify one clip with `graphics.list clip=<id>` (quad must sit inside canvas), then `exec file.save`.
7. Transcription MUST use faster-whisper (`scripts/transcribe.py`); FilmCraft builds to date (verified 0.8.0) have no built-in whisper.
Done when: `inspect` shows the edit + `file.save` bytes reported.
