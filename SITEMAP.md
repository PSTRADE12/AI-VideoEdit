# SITEMAP.md — Codebase Symbol & Dependency Index

*Generated — do not hand-edit. Regenerate with `python scripts/generate_sitemap.py`.*

## Hubs (most imported — edit with care)
- `config.py` (imported by 3 local modules)
- `fc.py` (imported by 1 local modules)

## `scripts\config.py` (L1–L84)
- Local imports: —
- def `_first_existing(*paths)` (L27–L31) → calls: isfile
- def `find_cli()` (L34–L44) → calls: get, join, which
- def `find_app()` (L47–L57) → calls: get, join, which
- def `find_transcribe_python()` (L60–L75) → calls: expandvars, get, isfile, which
- def `bridge()` (L78–L79) → calls: get
- def `extra_flags()` (L82–L84) → calls: get, split

## `scripts\fc.py` (L1–L59)
- Local imports: config
- def `run_cli(*args)` (L36–L48) → calls: decode, endswith, exit, run
- def `main()` (L51–L55) → calls: exit

## `scripts\generate_sitemap.py` (L1–L107)
- Local imports: —
- def `fmt_args(args_node)` (L14–L21) → calls: append, join
- def `calls_in(fn)` (L24–L26) → calls: walk
- def `parse_file(path)` (L29–L50) → calls: append, parse, read, split, walk
- def `py_files()` (L53–L61) → calls: endswith, join, walk
- def `main()` (L64–L103) → calls: append, basename, get, items, join, relpath

## `scripts\import_transcript.py` (L1–L37)
- Local imports: —
- def `main()` (L16–L33) → calls: dumps, exit, load, write

## `scripts\new_reel.py` (L1–L35)
- Local imports: fc
- def `main()` (L20–L31) → calls: exit, startswith

## `scripts\setup_check.py` (L1–L80)
- Local imports: config
- def `check(name, passed, hint)` (L22–L26)
- def `run(cmd, timeout)` (L29–L31) → calls: decode, run

## `scripts\silence_scan.py` (L1–L49)
- Local imports: —
- def `main()` (L17–L45) → calls: dump, exit, findall, finditer, group, run

## `scripts\start_live.py` (L1–L74)
- Local imports: config
- def `resolve_port(argv)` (L29–L32) → calls: index
- def `listening(port)` (L35–L44) → calls: close, connect, settimeout, socket
- def `main()` (L47–L70) → calls: Popen, abspath, append, dirname, exit, index

## `scripts\transcribe.py` (L1–L47)
- Local imports: —
- def `main()` (L16–L43) → calls: append, dump, exit, get, lstrip, split

## `scripts\wordpop.py` (L1–L102)
- Local imports: —
- def `color_of(text)` (L34–L36) → calls: lower, strip
- def `build_new(words, prefix, pos, size)` (L39–L56) → calls: append, dumps, write
- def `build_color(words, ids_path, prefix)` (L59–L75) → calls: dump, dumps, get, loads, read, splitlines
- def `main()` (L78–L98) → calls: exit, index, load, split, startswith
