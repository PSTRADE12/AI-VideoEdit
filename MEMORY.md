# 🧠 MEMORY.md — Project Knowledge & Evolution Ledger

*Persistent long-term memory for all AI agents editing video here. Read before any deep edit turn.*

---

## 👤 User Preferences & Decisions
- **Communication:** Short, factual, no superlatives. Test session 2026-10-11 was a trial; serious work follows.
- **Edit style:** Balanced silence removal (1.0s threshold, 0.3s keep); Hormozi-style karaoke single-word pops; Bahnschrift Bold until Google Fonts installed; reel-first 1080x1920.
- **Workflow:** Live bridge editing with user watching FilmCraft; read-only prove-outs before destructive steps; save after every batch.
- **Workspace:** this folder (any clone path; agent opens here); masters stay outside the repo (any footage path you pass in).
- **Portability (2026-10-15):** paths resolve via `scripts/config.py` (env → `vendor/` → default install → PATH); `setup_check.py` is the entry gate; FilmCraft binaries (~146MB) are NEVER committed — install per machine from https://getartcraft.com/apps/filmcraft or drop into git-ignored `vendor/`.

---

## 💡 Project Learnings & Gotchas (Hard-Won Knowledge)
- **[2026-10-11 | FilmCraft build has NO whisper — re-verified 2026-10-15 on 0.8.0]:** `exec sequence.transcribe` → `speech-to-text is not available in this build (built without the whisper feature); import a transcript with transcript.set instead`. `transcript.models` lists whisper-tiny/base/small, all uninstalled. Rule: ALWAYS transcribe externally (faster-whisper, interpreter shown by `setup_check.py`) then `transcript.set`. (Evidence: bridge + headless `--demo` exec outputs.)
- **[2026-10-11 | python vs pip mismatch — solved portable 2026-10-15]:** `python` = 3.13 (no faster-whisper), `pip` = 3.11 (has faster-whisper 1.2.1). Rule: NEVER hardcode the interpreter — run `python scripts/setup_check.py` and use the `find_transcribe_python()` / `TRANSCRIBE_PYTHON` interpreter it reports. Verify with `import faster_whisper`.
- **[2026-10-11 | Ticks]:** Time = 254016000000 ticks/sec. Most timeline commands also accept `seconds=`/`frame=`. (Evidence: `filmcraft-cli help` VALUES + reel_step transcripts.)
- **[2026-10-11 | graphics box position trap]:** With `box`, `position` = box TOP-LEFT, not center. `[540,1350]+box[920,260]` → quad to x=1460 on 1080 canvas (off-screen, verified via `graphics.list clip=137`). Rule: karaoke pops = point text (NO box) + `graphics.set align=center` AFTER creation + `[540,1350]`. Verify quad inside canvas.
- **[2026-10-11 | Static highlight ≠ karaoke]:** `graphics.setCharStyle` has no time param — one style per clip forever. 3-word chunks with one yellow word look stuck. Rule: TRUE karaoke = one clip PER WORD (180 clips for 100s), each word its own color.
- **[2026-10-11 | No rounded caption bg]:** `captions.setStyle` params = font/size/color/background/backgroundColor/align/anchor/margin/lineSpacing/outline only — no radius, no per-word. `graphics.set` bg = full-clip rect, no radius exposed. Rule: use yellow-keyword style, not pills; promise pills only with square-corner caveat.
- **[2026-10-11 | Delete semantics]:** `sequence.lift {}` needs In/Out (fails on clip selection: `mark an In or Out point first`). `sequence.extract` same. Rule: delete timeline clips with `edit.clear {"clips":[...]}` (Backspace, leaves gap). Reserve `edit.rippleDelete` for intentional gap-closing (it shifts everything).
- **[2026-10-11 | PowerShell > is UTF-16]:** `fc.py run ... > out.txt` writes UTF-16; Python must read clip ids with `encoding="utf-16"`. (Evidence: `��{` BOM broke json parse.)
- **[2026-10-11 | render via CLI bridge blocked]:** `render --seconds` → `render is headless; with --bridge use the MCP render_frame tool`. Rule: verify visually via `inspect`/`graphics.list`, not CLI renders.
- **[2026-10-11 | MCP binary is filmcraft-cli]:** Google AI's `filmcraft.exe mcp` config is wrong; MCP server = `filmcraft-cli.exe mcp` (verified handshake `serverInfo filmcraft 0.5.0`). Headless OR `--bridge 127.0.0.1:9876`.
- **[2026-10-11 | Vertical fill math]:** 1920x1080 source in 1080x1920 sequence → `motion scale 177.8` (1920/1080×100), position stays 540,960. Punch-in 210 at emphasis beats.

---

## 🛡️ Architectural Invariants (Do NOT Break)
- **Invariant 0 — No secrets in memory:** env names only, never values.
- **Invariant 1 — Masters immutable:** never write/trim/move original camera files; work on project sequences + `exports/`.
- **Invariant 2 — Ids from inspect:** clip/command/track ids always come from live `inspect`/`describe`, never memory or guesses.
- **Invariant 3 — Save the baton:** every edit turn ends with `file.save` + ACTIVE_TASK next action.

---

## 🗃️ Retired (Disproven or Obsolete — Never Silent-Delete)
- (none yet)

---

## 📈 Evolution Log (Cognitive Milestones)
- **2026-10-11:** Workspace initialized via FirstSpark v1.1; proven live session (silence cut 14 pauses/20s, 18 captions → 180 karaoke pops, Reel 9x16 1080x1920, 4 titles, punch-in zooms).
