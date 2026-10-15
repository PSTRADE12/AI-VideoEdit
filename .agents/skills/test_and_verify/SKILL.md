# Skill: test_and_verify
Trigger: before claiming any task complete; before every commit.
Commands: `python scripts/fc.py inspect` (bridge live check) — never skip; if FilmCraft is closed, record that gap in ACTIVE_TASK.md instead of claiming verification.
Expected: inspect JSON with the active sequence you just edited.
Done when: bridge output pasted or summarized in the turn log. No-submit-on-red: a failing bridge blocks handover claims.
