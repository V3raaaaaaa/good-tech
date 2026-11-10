#!/usr/bin/env python3
"""good-tech database CLI. Stdlib only.

  python3 goodtech.py index                       rebuild INDEX.md
  python3 goodtech.py list [--cat C] [--tag T] [--min-score N]
  python3 goodtech.py search <keyword>            full-text, case-insensitive
  python3 goodtech.py new <category> <slug>       new entry from _template.md
  python3 goodtech.py lint                        refuse private links, local paths, secrets
"""
import argparse
import datetime
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
CATEGORIES = ["contracts", "backend", "frontend", "infra", "security", "data", "tokenomics"]
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    meta = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        val = val.strip()
        if val.startswith("[") and val.endswith("]"):
            val = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
        meta[key.strip()] = val
    return meta


def entries():
    out = []
    for cat in CATEGORIES:
        for f in sorted((ROOT / cat).glob("*.md")):
            text = f.read_text(encoding="utf-8")
            meta = parse_frontmatter(text)
            meta.setdefault("name", f.stem)
            meta["category"] = cat
            meta["path"] = f.relative_to(ROOT).as_posix()
            meta["_text"] = text
            tags = meta.get("tags") or []
            meta["tags"] = tags if isinstance(tags, list) else [tags]
            try:
                meta["score_n"] = int(meta.get("score") or 0)
            except ValueError:
                meta["score_n"] = 0
            out.append(meta)
    return out


def row(e):
    score = e.get("score") or "-"
    return f"{score:>2}  {e.get('status', '?'):<8}  {e['path']:<55}  {', '.join(e['tags'])}"


def cmd_index(_args):
    es = entries()
    lines = [
        "# good-tech index",
        "",
        "Digenerate oleh `python3 goodtech.py index`. Jangan edit manual.",
        "",
        f"Total: {len(es)} entry",
        "",
    ]
    for cat in CATEGORIES:
        group = sorted((e for e in es if e["category"] == cat), key=lambda e: -e["score_n"])
        if not group:
            continue
        lines += [f"## {cat}", "", "| Skor | Tech | Project | Status | Tags |", "|---|---|---|---|---|"]
        for e in group:
            lines.append(
                f"| {e.get('score') or '-'} | [{e['name']}]({e['path']}) | {e.get('project', '')} "
                f"| {e.get('status', '')} | {', '.join(e['tags'])} |"
            )
        lines.append("")
    (ROOT / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"INDEX.md rebuilt: {len(es)} entries")


def cmd_list(args):
    for e in entries():
        if args.cat and e["category"] != args.cat:
            continue
        if args.tag and args.tag not in e["tags"]:
            continue
        if e["score_n"] < args.min_score:
            continue
        print(row(e))


def cmd_search(args):
    kw = args.keyword.lower()
    for e in entries():
        hits = [ln.strip() for ln in e["_text"].splitlines() if kw in ln.lower()]
        if hits:
            print(row(e))
            for h in hits[:3]:
                print(f"      > {h[:110]}")


# Things that must never reach the shared repo: links into Claude's private memory, paths into
# local recon/bot folders, and anything shaped like a secret.
LINT_RULES = [
    ("memory link", re.compile(r"\[\[[a-z0-9-]+\]\]")),
    ("local recon path", re.compile(r"\b[a-z0-9]+-recon/")),
    ("local bot/tool path", re.compile(r"`(?:mintradar|unicred|[a-z0-9]+-mint|[a-z0-9]+-miner-share)/")),
    ("env file", re.compile(r"\b(?:alerts|\.env)\.env\b|\bwallets-all\.txt\b")),
    ("secret assignment", re.compile(r"(?i)\b(?:private[_ ]?key|api[_-]?key|secret|mnemonic|seed phrase)\s*[:=]\s*\S{8,}")),
    ("openai/anthropic key", re.compile(r"\bsk-(?:ant-)?[A-Za-z0-9_-]{20,}")),
    ("raw private key", re.compile(r"(?i)(?:privkey|private key)[^\n]{0,20}0x[0-9a-f]{64}")),
    # the repo is public: no hints about our own minting/farming ops or private relationships
    ("own ops / relationship", re.compile(r"(?i)\b(?:kode kita|bot kita|wallet kita|kita lakuin|live run|site temen|punya temen|we minted|our bot)\b")),
]


def cmd_lint(_args):
    bad = 0
    for f in sorted(ROOT.rglob("*.md")):
        rel = f.relative_to(ROOT).as_posix()
        if rel == "INDEX.md":
            continue
        for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            for label, rx in LINT_RULES:
                if rx.search(line):
                    bad += 1
                    print(f"{rel}:{n}: {label}: {line.strip()[:110]}")
    print("lint: clean" if not bad else f"lint: {bad} problem(s)")
    sys.exit(1 if bad else 0)


def cmd_new(args):
    if args.category not in CATEGORIES:
        sys.exit(f"category must be one of: {', '.join(CATEGORIES)}")
    if not SLUG_RE.match(args.slug):
        sys.exit("slug: lowercase, digits and dashes only")
    dest = ROOT / args.category / f"{args.slug}.md"
    if dest.exists():
        sys.exit(f"already exists: {dest.relative_to(ROOT)}")
    tpl = (ROOT / "_template.md").read_text(encoding="utf-8")
    tpl = (tpl.replace("{{NAME}}", args.slug.replace("-", " "))
              .replace("{{CATEGORY}}", args.category)
              .replace("{{DATE}}", datetime.date.today().isoformat()))
    dest.write_text(tpl, encoding="utf-8")
    print(f"created {dest.relative_to(ROOT)}")


def main():
    p = argparse.ArgumentParser(description="good-tech database")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("index").set_defaults(fn=cmd_index)
    sub.add_parser("lint").set_defaults(fn=cmd_lint)
    pl = sub.add_parser("list")
    pl.add_argument("--cat")
    pl.add_argument("--tag")
    pl.add_argument("--min-score", type=int, default=0)
    pl.set_defaults(fn=cmd_list)
    ps = sub.add_parser("search")
    ps.add_argument("keyword")
    ps.set_defaults(fn=cmd_search)
    pn = sub.add_parser("new")
    pn.add_argument("category")
    pn.add_argument("slug")
    pn.set_defaults(fn=cmd_new)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
