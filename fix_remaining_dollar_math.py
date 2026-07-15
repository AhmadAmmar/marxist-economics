#!/usr/bin/env python3
"""
Targeted cleanup for remaining literal/escaped $$ inline-math fragments,
especially in Chapter 5.

Run from repo root:
    python .\fix_remaining_dollar_math.py
"""

from __future__ import annotations

import re
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path.cwd()
DOCS = ROOT / "docs"
BACKUP = ROOT / "_markdown_fix_backups" / datetime.now().strftime("%Y%m%d-%H%M%S-remaining-dollar-math")


def backup_and_write(path: Path, new: str, old: str) -> bool:
    if new == old:
        return False
    b = BACKUP / path.relative_to(ROOT)
    b.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, b)
    path.write_text(new, encoding="utf-8", newline="\n")
    return True


def normalize_escaped_dollars(text: str) -> str:
    # Some converters write \$\$ instead of $$; browsers then show literal $$.
    text = text.replace(r"\$\$", "$$")
    return text


def protect_display_blocks(text: str) -> tuple[str, dict[str, str]]:
    """
    Protect proper display blocks so we do not convert them into inline math.

    A proper display block is:
        $$
        ...
        $$
    with delimiters alone on their lines.
    """
    blocks: dict[str, str] = {}

    pattern = re.compile(r"(?ms)(^|\n)([ \t]*)\$\$[ \t]*\n.*?\n[ \t]*\$\$[ \t]*(?=\n|$)")

    def repl(m: re.Match[str]) -> str:
        key = f"@@DISPLAY_BLOCK_{len(blocks)}@@"
        blocks[key] = m.group(0)
        return key

    return pattern.sub(repl, text), blocks


def restore_display_blocks(text: str, blocks: dict[str, str]) -> str:
    for k, v in blocks.items():
        text = text.replace(k, v)
    return text


def convert_bad_inline_dollar_pairs(text: str) -> str:
    """
    Convert any remaining paired $$...$$ that is not a proper display block into inline math.
    Works across line breaks.
    """
    text, blocks = protect_display_blocks(text)

    def repl(m: re.Match[str]) -> str:
        inner = m.group(1)
        inner = re.sub(r"\s+", " ", inner).strip()
        # Move terminal comma outside the math if present.
        if inner.endswith(","):
            inner = inner[:-1].rstrip()
            return f"${inner}$,"
        return f"${inner}$"

    text = re.sub(r"(?s)\$\$\s*(.+?)\s*\$\$", repl, text)
    return restore_display_blocks(text, blocks)


def targeted_chapter05(text: str) -> str:
    # Fix exact remaining screenshot fragment if the generic pass leaves it.
    text = re.sub(
        r"as\s+\$+\s*e\s*=\s*\\frac\{s\}\{v\}\s*=\s*\\frac\{T_\{\\mathrm\{S\}\}\}\{T_\{\\mathrm\{N\}\}\},?\s*\$+\s+because",
        r"as $e = \frac{s}{v} = \frac{T_{\mathrm{S}}}{T_{\mathrm{N}}}$, because",
        text,
        flags=re.S,
    )

    # Also handle if the delimiters are still escaped in the file.
    text = re.sub(
        r"as\s+\\\$\\\$\s*e\s*=\s*\\frac\{s\}\{v\}\s*=\s*\\frac\{T_\{\\mathrm\{S\}\}\}\{T_\{\\mathrm\{N\}\}\},?\s*\\\$\\\$\s+because",
        r"as $e = \frac{s}{v} = \frac{T_{\mathrm{S}}}{T_{\mathrm{N}}}$, because",
        text,
        flags=re.S,
    )

    return text


def process(path: Path) -> bool:
    old = path.read_text(encoding="utf-8")
    new = old

    new = normalize_escaped_dollars(new)
    new = convert_bad_inline_dollar_pairs(new)

    if path.name == "05-labour-power-wages-surplus-labour-and-surplus-value.md":
        new = targeted_chapter05(new)

    return backup_and_write(path, new, old)


def main() -> None:
    if not DOCS.exists():
        raise SystemExit("docs/ not found. Run this from the repo root.")

    changed = []
    for path in sorted(DOCS.rglob("*.md")):
        if process(path):
            changed.append(path)

    print(f"Changed {len(changed)} files.")
    if changed:
        print(f"Backups: {BACKUP}")
        for p in changed:
            print(f"  fixed {p.relative_to(ROOT)}")

    print("\nRemaining literal paired $$ outside proper display blocks:")
    any_hits = False
    for path in sorted(DOCS.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        protected, _ = protect_display_blocks(text)
        if re.search(r"(?s)\$\$\s*.+?\s*\$\$", protected):
            any_hits = True
            print(f"  {path.relative_to(ROOT)}")
    if not any_hits:
        print("  none")


if __name__ == "__main__":
    main()
