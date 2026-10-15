# 🤖 AGENTS.md — Universal Agent Operating Guidelines

*FirstSpark protocol v1.1 — FilmcraftEdit workspace.*

Welcome, Agent. You are operating in an asynchronous, self-evolving, multi-model collaborative workspace for AI-driven video editing with FilmCraft.

## 1. Ground Rules & Safety Constraints
- **Secrets Never Enter Memory:** Never write API keys, tokens, passwords, or connection strings to any memory file, log, or chat. Reference env var *names* only. (STEP 0 invariant — outranks all below.)
- **Preserve Documentation Integrity:** Do not delete or overwrite existing documentation without explicit direction.
- **Safety First:** Never execute irreversible, destructive, or financial order operations without user confirmation or a sandbox/paper verification step.
- **Video Safety (project rule):** Original camera files / masters are READ-ONLY (keep them outside this repo). Edits happen on sequences/copies; `edit.clear`/`rippleDelete`/`removePauses` run on a NEW reel copy unless the user explicitly approves cutting the original. Verify with `inspect` before and `file.save` after.
- **Bridge Discipline:** Live edits go through `scripts/fc.py` (bridge `127.0.0.1:9876`). If the bridge refuses connection, STOP and ask the user to start `filmcraft.exe --control 9876` — never fake success.
- **Zero Hallucination Verification:** Verify clip/command ids via `describe`/`inspect` (or SITEMAP.md for scripts) before editing. Fresh evidence beats memory.

## 2. Navigation Protocol (Read SITEMAP.md First)
- Before adding a new script, consult `SITEMAP.md` for the existing automation layer (`scripts/`).
- `SITEMAP.md` is generated — never hand-edit; run `python scripts/generate_sitemap.py`.

## 3. Project Commands Quick Reference
- **Health check (run first on any machine):** `python scripts/setup_check.py` (add `--bridge` when the app is open). Paths resolve via `scripts/config.py`: env → `vendor/` → default install → `PATH`. Never hardcode machine paths.
- **Start live app:** `python scripts/start_live.py [--port 9876] [--project "<path>\x.fcproj" | --demo]` (launches GUI in `--control` mode, waits for the port, verifies via inspect)
- **Bridge check:** `python scripts/fc.py inspect`
- **Describe before destroy:** `python scripts/fc.py describe <command-id>`
- **Transcribe:** use the interpreter from `setup_check.py`: `<that-python> scripts/transcribe.py <media> transcripts/words.json` (needs faster-whisper, see `requirements-transcribe.txt`)
- **Silence scan (no ML):** `python scripts/silence_scan.py <media>`
- **Karaoke pops:** `python scripts/wordpop.py transcripts/words.json transcripts/pop` (then fc.py run ×3: new/color+align)
- **New vertical reel:** `python scripts/new_reel.py <item-id>`
- **Generate / Update Sitemap:** `python scripts/generate_sitemap.py`

## 4. The Continuous Evolution & Memory Protocol (Mandatory on Every Turn)
1. **Read Memory First:** Consult `MEMORY.md` before any deep edit turn.
2. **Gotcha Capture:** Non-obvious FilmCraft/ffmpeg/whisper quirks go to `MEMORY.md` under `## 💡 Project Learnings & Gotchas` with date + failing command/output + permanent rule.
3. **User Preference Capture:** Style/risk/workflow prefs → `MEMORY.md` `## 👤 User Preferences & Decisions`.
4. **Task Handover:** Check off `ACTIVE_TASK.md`, mark in-progress `[/]`, write the exact Immediate Next Action.
5. **Change Logging + Reuse:** Script changes → `CHANGELOG.md` bullet + regenerate `SITEMAP.md`. If a task repeats (2nd time doing it by hand), save it as a new `scripts/*.py` + skill trigger instead of re-typing — scripts are the reusable memory.
6. **Freshness Ritual:** Re-verify gotchas when evidence contradicts; retire disproven ones, never silent-delete.
