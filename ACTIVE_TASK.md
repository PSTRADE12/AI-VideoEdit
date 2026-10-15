# ⚡ ACTIVE_TASK.md — Working Memory & Handover Baton

## 🎯 Current Epic / Goal
**Title:** Standalone clone-and-run release + first serious edit readiness
- **Current Status:** STANDALONE READY — `config.py` resolver, `setup_check.py` gate green (10 modules), full README (FilmCraft install + any-AI-tool use). Bridge down (app closed); next: live verify + user's first footage.
- **Active Lead Model:** Muse Spark (opencode) @ 2026-10-15
- **Timestamp:** 2026-10-15 (standalone release; sitemap 10 modules)

---

## 📋 Execution Checklist
- [x] Phase 0: Workspace Reconnaissance & FirstSpark Initialization (location picked, folders created)
- [x] Phase 1: Editing system scripts (fc/transcribe/import/silence/wordpop/new_reel + sitemap gen)
- [x] Phase 2: Living-memory suite (AGENTS/MEMORY/PROJECT_CONTEXT/ACTIVE_TASK/CHANGELOG) + skills
- [x] Phase 3: Verification (sitemap regen OK 7 modules; secret scan clean — the 2 hits are FIRSTSPARK.md's own hook example patterns, not credentials; bridge gap: FilmCraft app closed after test session, re-verify live next turn)
- [x] Phase 4: Standalone release (config.py, setup_check.py READY, .env.example, .gitignore, requirements, full README with FilmCraft install + vendor decision; sitemap 10 modules; verified 0.8.0, secret scan clean)
- [x] Phase 5: Git init + first push (main branch; pre-commit drift-guard hook installed + tested; author = GitHub noreply, no personal info in tree or metadata)
- [ ] Phase 6: First serious edit (user's next footage; pending user drop)

---

## 🧠 Key Decisions & Blockers
- **Decisions Recorded:** Portable workspace (any clone path; agent opens this folder); transcription via faster-whisper interpreter from `setup_check.py`; karaoke = per-word clips; masters immutable; FilmCraft binaries never committed (install per machine or `vendor/`).
- **Current Blockers:** None for setup. Next edit needs: footage path (or new recording), language, silence level, reel-vs-horizontal choice.

---

## 🏃 Immediate Next Action for Incoming Agent
> **INCOMING AGENT READ THIS:** You are picking up the baton. Do NOT ask the user what to do.
> Perform this exact next step immediately:
>
> **Action:** Read `README.md` §2 (5-min connection check), run `python scripts/fc.py inspect` to confirm the live bridge, then read `MEMORY.md` gotchas before touching any timeline. If the bridge refuses, ask the user to start `filmcraft.exe --control 9876` and open their project.
