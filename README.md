# 🎬 FilmcraftEdit — AI Video-Editing Workspace (clone & run)

**Open this folder in any AI coding tool (opencode, Cursor, Windsurf, Cline, Copilot, ChatGPT agent mode). Drop footage nearby. Tell the AI what you want in plain words. It drives FilmCraft for you.**

> **Requires FilmCraft to work.** This workspace is a driver + automation layer — it does NOT edit video by itself. You must install **FilmCraft** (free download: **https://getartcraft.com/apps/filmcraft**, Learning Machines LLC, Windows) on every machine that runs it, then open the FilmCraft app in `--control` mode (§2) so the AI can drive the live timeline. Without FilmCraft installed and open, only `setup_check.py` (no-bridge) works.

Battle-tested 2026-10-11 (100s clip → silence-cut, 180 karaoke pops, 1080x1920 reel, live in FilmCraft) and re-verified on FilmCraft 0.8.0. Everything the agent learned lives in `scripts/`, `.agents/skills/`, and `MEMORY.md`, so every session starts smart.

---

## 0. What you need (one-time, ~10 min)

| Need | What | Where |
|---|---|---|
| **FilmCraft** | Video editor: GUI (`filmcraft.exe`) + engine/CLI (`filmcraft-cli.exe`). Verified on **0.8.0**, publisher **Learning Machines LLC** | Official site: **https://getartcraft.com/apps/filmcraft** — install the Windows build (default `C:\Program Files\FilmCraft\`). No account needed for local editing |
| **ffmpeg 7+** | Silence scan, audio prep | https://ffmpeg.org/download.html or `winget install ffmpeg` — check with `ffmpeg -version` |
| **Python 3.10+** | Runs all scripts (stdlib only) | https://python.org — check with `python --version` |
| **Python 3.11 + faster-whisper** | Transcription only (FilmCraft 0.8.0 still has no built-in whisper — verified) | `py -3.11 -m pip install -r requirements-transcribe.txt`, or any Python with `import faster_whisper` working |
| **AI tool** | Any agent that can read files + run shell | opencode / Cursor / Windsurf / Cline / Copilot workspace — open **this folder** as the working directory |

> **Why FilmCraft stays in Program Files (not in this repo)?** The two binaries are ~146MB — committing them would bloat every `git clone` and break updates. This repo resolves them portable-style instead: env var → repo-local `vendor/` → default install → `PATH` (see `scripts/config.py`). If you truly want a USB-stick setup, copy both `.exe` files into `vendor/` (git-ignored) and everything keeps working with zero config. Never commit `vendor/` to git.

---

## 1. Clone & run (every machine)

```powershell
git clone <your-repo-url> FilmcraftEdit
cd FilmcraftEdit
python scripts/setup_check.py          # binaries, ffmpeg, python, folders
python scripts/setup_check.py --bridge # also checks the live app (needs §2)
```

Optional overrides (only if non-default install). Copy `.env.example` → `.env` or set env vars:

```powershell
$env:FILMCRAFT_CLI="D:\Portable\filmcraft-cli.exe"   # or vendor\filmcraft-cli.exe
$env:FILMCRAFT_APP="D:\Portable\filmcraft.exe"
$env:FILMCRAFT_BRIDGE="127.0.0.1:9876"               # empty = headless file ops
$env:TRANSCRIBE_PYTHON="C:\Python311\python.exe"     # auto-detected if unset
```

## 2. Start FilmCraft in control mode (every edit session)

The AI cannot edit until the app exposes the bridge. Leave this window open:

```powershell
& "C:\Program Files\FilmCraft\filmcraft.exe" --control 9876
# or: python scripts/start_live.py [--project "<path>.fcproj" | --demo]
```

Then open your project (`.fcproj`) or the demo. Verify the AI sees it:

```powershell
python scripts/fc.py inspect   # shows project/sequence JSON; refuses = redo step above
```

Headless (no GUI) also works for file ops: `$env:FILMCRAFT_BRIDGE=""; $env:FILMCRAFT_EXTRA="--demo"` — but timeline review needs the GUI.

## 3. Everyday use — copy-paste prompts (any AI tool)

> Formula: **footage + job + taste.** The agent inspects first, proves read-only, then edits live while you watch FilmCraft.

- **Cut silences + tighten (safe, on a copy):** `My footage is "<full-path>.mkv". Make a new 1080x1920 reel from it, remove pauses over 1.0s keeping 0.3s, save. Don't touch my original sequence.`
- **Karaoke word-pop subtitles (house style):** `Transcribe the active reel and build single-word karaoke pops: Bahnschrift Bold, centered lower-third, keywords yellow, rest white. Verify one quad is on-screen, then save.`
- **Titles that don't get cropped:** `Add a title "<TEXT>" at <N>s for 4s, centered top-safe on 1080x1920, Bahnschrift Bold with stroke. Verify its quad is inside the canvas.`
- **Punch-in motion:** `Add punch-in zooms (scale 177.8 → 210 and back) at <seconds> on the main clip.`
- **Export:** `Export the active sequence to exports\<name>_reel.mp4 as H.264 1080x1920 and confirm the file.`
- **Full job:** `Footage "<path>", English. New vertical reel, balanced silence cut, karaoke pops, 3 centered titles, export MP4 to exports\.`

Masters rule: originals are READ-ONLY. Destructive ops run on the NEW reel copy unless you explicitly approve cutting the original.

## 4. How a job flows (what the AI does)

1. `fc.py inspect` → sequence/clip ids (never guessed) → `describe <id>` before destructive steps.
2. Transcribe: `setup_check.py`-verified Python + `scripts/transcribe.py` → `transcripts/words.json`.
3. Import: `import_transcript.py` → `fc.py run import.jsonl` → `transcript.removePauses` / `createCaptions`.
4. Karaoke: `wordpop.py` → 3 batches (new → colors → align), verify `graphics.list` quad, `file.save`.
5. Titles/zooms → `file.save` → export to `exports/`.

## 5. Troubleshooting (every row earned)

| Symptom | Cause → Fix |
|---|---|
| `bridge: cannot connect to 127.0.0.1:9876` | App not in control mode → §2, keep window open |
| `speech-to-text is not available in this build` | Normal (verified 0.8.0) → external `transcribe.py` + `transcript.set` |
| `No module named 'faster_whisper'` | Wrong interpreter → `setup_check.py` shows the right one; install `requirements-transcribe.txt` there |
| `filmcraft-cli: No such file` | Non-default install → set `FILMCRAFT_CLI` or drop exes in `vendor/` |
| Captions half off-screen right | Box-position trap → agent rebuilds point-text centered; check `graphics.list` quad |
| All words one color | Static chunk highlight ≠ karaoke → one-clip-per-word rebuild |
| `sequence.lift: mark an In or Out point first` | Wrong delete op → `edit.clear {"clips":[...]}` for clip delete |
| `render is headless; use MCP render_frame` | CLI can't render over bridge → verify via `inspect`/`graphics.list`, eyeball the GUI |
| Garbled `��{` reading output | PowerShell `>` writes UTF-16 → agent reads `encoding="utf-16"` |

## 6. Folder map + git notes

```
FilmcraftEdit/
├── README.md, AGENTS.md, MEMORY.md, PROJECT_CONTEXT.md
├── ACTIVE_TASK.md, CHANGELOG.md, SITEMAP.md (generated — run generate_sitemap.py, don't hand-edit)
├── .env.example, .gitignore, requirements.txt, requirements-transcribe.txt
├── scripts/  fc.py, config.py, setup_check.py, start_live.py, transcribe.py,
│             import_transcript.py, silence_scan.py, wordpop.py, new_reel.py, generate_sitemap.py
├── .agents/skills/  filmcraft_edit, generate_sitemap, test_and_verify
├── transcripts/ (git-ignored contents), exports/ (ignored), media/ (ignored drop folder)
└── vendor/ (optional portable exes, always ignored — never commit)
```

Push checklist: `setup_check.py` green → `generate_sitemap.py` → commit (`.gitignore` keeps `vendor/`, `exports/`, `media/`, `*.fcproj`, transcripts out). Binaries install from the official site per machine — the repo stays lean.

House taste defaults: 1080x1920 @30fps, silence 1.0s/0.3s, Bahnschrift Bold karaoke (yellow `#FFD60A` keywords, white rest, `[540,1350]` centered), vertical-fill scale 177.8. Say the word to change any — the agent logs it to `MEMORY.md` and it sticks.
