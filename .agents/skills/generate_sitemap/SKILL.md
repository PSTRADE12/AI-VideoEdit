# Skill: generate_sitemap
Trigger: after ANY code change, before ending the turn.
Commands: `python scripts/generate_sitemap.py`
Expected: `sitemap: N modules -> SITEMAP.md`, no traceback.
Done when: `git diff --stat -- SITEMAP.md` reflects the change (or clean when behavior-only edits).
