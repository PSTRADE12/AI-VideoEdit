# 📜 CHANGELOG

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Added
- Portable standalone release: `scripts/config.py` resolver, `scripts/setup_check.py` health gate, `.env.example`, `.gitignore` (vendor/exports/media/transcripts/keys out), `requirements.txt` + `requirements-transcribe.txt`, full clone-and-run `README.md` (FilmCraft install + any-AI-tool use). Binaries stay out of git (install per machine or git-ignored `vendor/`).
- Git repo initialized (`main`) with FirstSpark pre-commit drift-guard hook (sitemap freshness + secret tripwire, tested exit 0). Tree + authors carry no personal info (GitHub noreply author).
- Retired `FIRSTSPARK.md` (ignition protocol v1.1 fully implemented and verified; living suite is self-sustaining).
- Editing system: `scripts/fc.py`, `transcribe.py`, `import_transcript.py`, `silence_scan.py`, `wordpop.py`, `new_reel.py`, `generate_sitemap.py`.
- Agent skills: `generate_sitemap`, `test_and_verify`, `filmcraft_edit`.
- Living-memory suite per FirstSpark v1.1 (`AGENTS.md`, `MEMORY.md`, `PROJECT_CONTEXT.md`, `SITEMAP.md`, `ACTIVE_TASK.md`, `CHANGELOG.md`) + `README.md` operator guide.

## [Baseline] - 2026-10-11
### Added
- Workspace initialized via FirstSpark v1.1 ignition.
- Proven live session carried over: FilmCraft 0.5.0 bridge, 14-pause silence cut (20s), 181-word transcription, 180 karaoke pops, Reel 9x16 1080x1920, 4 centered titles, punch-in zooms (`opencode test.fcproj` rev history).
