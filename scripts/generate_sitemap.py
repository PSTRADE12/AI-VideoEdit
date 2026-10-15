#!/usr/bin/env python3
"""Zero-dependency AST sitemap generator. Usage: python3 scripts/generate_sitemap.py"""
import ast
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "SITEMAP.md")
TARGET_DIRS = ["scripts"]          # editing workspace: map the automation layer
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv"}
SKIP_FILES = set()


def fmt_args(args_node):
    parts = [a.arg for a in args_node.args]
    if args_node.vararg:
        parts.append("*" + args_node.vararg.arg)
    parts += [a.arg + "=" for a in args_node.kwonlyargs]
    if args_node.kwarg:
        parts.append("**" + args_node.kwarg.arg)
    return ", ".join(parts)


def calls_in(fn):
    return sorted({n.func.attr for n in ast.walk(fn)
                   if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)})


def parse_file(path):
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read(), path)
    imports, classes, funcs = [], [], []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports += [a.name.split(".")[0] for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module.split(".")[0])
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            methods = [(b.name, b.lineno, getattr(b, "end_lineno", b.lineno),
                        fmt_args(b.args), calls_in(b)[:6])
                       for b in node.body
                       if isinstance(b, (ast.FunctionDef, ast.AsyncFunctionDef))]
            classes.append((node.name, node.lineno,
                            getattr(node, "end_lineno", node.lineno), methods))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funcs.append((node.name, node.lineno,
                          getattr(node, "end_lineno", node.lineno),
                          fmt_args(node.args), calls_in(node)[:6]))
    return sorted(set(imports)), classes, funcs


def py_files():
    out = []
    for base in TARGET_DIRS:
        root = os.path.join(ROOT, base)
        for dp, dn, fn in os.walk(root):
            dn[:] = [d for d in dn if d not in SKIP_DIRS]
            out += [os.path.join(dp, f) for f in sorted(fn)
                    if f.endswith(".py") and f not in SKIP_FILES]
    return out


def main():
    files = py_files()
    local = {os.path.splitext(os.path.basename(f))[0] for f in files}
    centrality, per = {}, {}
    for f in files:
        imports, classes, funcs = parse_file(f)
        per[f] = (imports, classes, funcs)
        for imp in imports:
            if imp in local and imp != os.path.splitext(os.path.basename(f))[0]:
                centrality[imp] = centrality.get(imp, 0) + 1
    L = ["# SITEMAP.md — Codebase Symbol & Dependency Index", "",
         "*Generated — do not hand-edit. Regenerate with `python scripts/generate_sitemap.py`.*",
         "", "## Hubs (most imported — edit with care)"]
    hubs = sorted(centrality.items(), key=lambda kv: -kv[1])[:5]
    L += [f"- `{m}.py` (imported by {n} local modules)" for m, n in hubs] or ["- (none)"]
    L.append("")
    for f in sorted(per):
        rel = os.path.relpath(f, ROOT)
        imports, classes, funcs = per[f]
        with open(f, encoding="utf-8") as fh:
            total = sum(1 for _ in fh)
        mod = os.path.splitext(os.path.basename(f))[0]
        loc = sorted({i for i in imports if i in local and i != mod})
        L.append(f"## `{rel}` (L1–L{total})")
        L.append(f"- Local imports: {', '.join(loc) or '—'}")
        for name, s, e, methods in classes:
            L.append(f"- class `{name}` (L{s}–L{e}):")
            for m, ms, me, args, calls in methods:
                tail = f" → calls: {', '.join(calls)}" if calls else ""
                L.append(f"  - `{m}({args})` (L{ms}){tail}")
        for name, s, e, args, calls in funcs:
            tail = f" → calls: {', '.join(calls)}" if calls else ""
            L.append(f"- def `{name}({args})` (L{s}–L{e}){tail}")
        L.append("")
    text = "\n".join(L)
    if len(text.splitlines()) > 400:
        text += "\n> NOTE: map exceeds 400 lines — split per top-level directory (SITEMAP_<dir>.md) and keep only hubs here.\n"
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"sitemap: {len(files)} modules -> {OUT}")


if __name__ == "__main__":
    sys.exit(main())
