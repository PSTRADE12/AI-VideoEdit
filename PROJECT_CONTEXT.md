# 🗺️ PROJECT_CONTEXT.md — Architectural Knowledge Base

## 1. System Overview & Core Purpose
- **Project Name:** FilmcraftEdit
- **Core Purpose:** Reusable AI video-editing workspace. An agent opened in this folder can transcribe footage, cut silences, build karaoke reel captions, add titles/motion callouts, reframe 16:9→9:16, and export — against a live FilmCraft app or headless — without relearning the toolchain each session.
- **Primary Tech Stack:** FilmCraft 0.8.0 (GUI + `filmcraft-cli.exe` engine/MCP; official site https://getartcraft.com/apps/filmcraft, Learning Machines LLC; install per machine, never committed), Python automation (`scripts/` with portable `config.py` resolver + `setup_check.py` gate; transcription needs faster-whisper per `requirements-transcribe.txt`), ffmpeg 8.1 (silence scan), any AI agent harness (opencode/Cursor/Windsurf/Cline — folder opened as workspace, `AGENTS.md` as constitution).

## 2. Directory & Module Map
| Directory / File | Core Responsibility | Key Entry Points |
| :--- | :--- | :--- |
| `scripts/fc.py` | Sole bridge wrapper (exec/run/describe/commands/inspect; paths via `config.py`) | `python scripts/fc.py inspect` |
| `scripts/config.py` | Portable resolver: env → `vendor/` → default install → PATH (CLI/APP/bridge/python) | imported by `fc.py`, `start_live.py`, `setup_check.py` |
| `scripts/setup_check.py` | Clone-and-run health gate (binaries, ffmpeg, faster-whisper, folders, `--bridge` live check) | `python scripts/setup_check.py [--bridge]` |
| `scripts/transcribe.py` | faster-whisper → word-timestamp JSON (interpreter from `setup_check.py`) | `transcribe.py <media> transcripts/words.json` |
| `scripts/import_transcript.py` | words JSON → `transcript.set` batch (ticks) | `import_transcript.py <json> <item-id>` |
| `scripts/silence_scan.py` | ffmpeg silencedetect → silence JSON (no ML) | `silence_scan.py <media>` |
| `scripts/wordpop.py` | words JSON → karaoke new/color/align batches | `wordpop.py <json> <prefix>` |
| `scripts/new_reel.py` | Prints proven 16:9→9:16 reel+fill steps | `new_reel.py <item-id>` |
| `scripts/generate_sitemap.py` | FirstSpark AST sitemap generator | `python scripts/generate_sitemap.py` |
| `.agents/skills/filmcraft_edit/` | Agent playbook: inspect-first, karaoke rules | `SKILL.md` |
| `transcripts/` | words/silence/batch JSONL artifacts | `words.json` |
| `exports/` | Finished MP4/WAV renders | — |
| `media/` | Optional local drop folder (or pass any footage path; originals stay read-only) | — |

## 3. Data Pipelines & Lifecycle Architecture
Typical reel turn (live bridge `127.0.0.1:9876`):
`<footage>.mkv` → `transcribe.py` (words.json, timeline-accurate: transcribe the EXPORTED reel wav after cuts, not the master) → `import_transcript.py` → `fc.py run import.jsonl` → `exec transcript.removePauses minSeconds=1.0 keepSeconds=0.3` → `new_reel.py` steps (1080x1920 + scale 177.8) → `wordpop.py` 3-batch karaoke (new → color → align, verify quad via `graphics.list`) → titles/callouts → `exec file.save` → `exec file.exportMedia` → `exports/`.
Silence-only path (no transcript): `silence_scan.py` → `timeline.razor` at boundaries → `edit.rippleDelete`/`edit.clear`.

## 4. Key Domain Terminology & Concepts
- **Ticks:** 254016000000/sec; commands also take `seconds=`/`frame=`/`timecode=`.
- **Bridge vs headless:** `--bridge 127.0.0.1:9876` drives the open GUI app (`filmcraft.exe --control 9876`); omit for headless file ops. MCP server binary is `filmcraft-cli.exe mcp`, never `filmcraft.exe mcp`.
- **Karaoke pop:** one `graphics.newText` per spoken word (point text, align-center-after, [540,1350]); static chunk highlights are NOT karaoke.
- **Item vs clip vs sequence:** item = media bin id; clip = timeline instance id; sequence = timeline container id. `transcript.set` takes item; `graphics.*`/`effects.*` take clip.
