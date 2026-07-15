#!/usr/bin/env python3
"""
Fix malformed inline display-math pairs in generated MkDocs Markdown.

Problem this targets:
    The remaining $$ T_{\mathrm{S}} = T - T_{\mathrm{N}}, $$ is ...
or, after line wrapping:
    The remaining $$ T_{\mathrm{S}} = T -
    T_{\mathrm{N}}, $$ is ...

MkDocs/MathJax expects inline math as $...$ and display math as:
    $$
    ...
    $$

Run from repo root:
    python .\fix_inline_math_pairs.py
"""

from __future__ import annotations

import re
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path.cwd()
DOCS = ROOT / "docs"
BACKUP_ROOT = ROOT / "_markdown_fix_backups" / datetime.now().strftime("%Y%m%d-%H%M%S-inline-math")


DISPLAY_BLOCK_RE = re.compile(
    r"(?ms)(^|\n)([ \t]*)\$\$[ \t]*\n(.*?)(?:\n)([ \t]*)\$\$([ \t]*(?=\n|$))"
)


def protect_display_blocks(text: str) -> tuple[str, dict[str, str]]:
    protected: dict[str, str] = {}

    def repl(match: re.Match[str]) -> str:
        key = f"@@DISPLAY_MATH_BLOCK_{len(protected)}@@"
        protected[key] = match.group(0)
        return key

    return DISPLAY_BLOCK_RE.sub(repl, text), protected


def restore_display_blocks(text: str, protected: dict[str, str]) -> str:
    for key, value in protected.items():
        text = text.replace(key, value)
    return text


def fix_full_line_single_line_display(text: str) -> str:
    # A line that consists only of "$$ formula $$" should become a real display block.
    def repl(m: re.Match[str]) -> str:
        indent = m.group(1) or ""
        inner = m.group(2).strip()
        return f"{indent}$$\n{indent}{inner}\n{indent}$$"

    return re.sub(r"(?m)^([ \t]*)\$\$\s*(.+?)\s*\$\$\s*$", repl, text)


def fix_remaining_inline_pairs(text: str) -> str:
    # Protect proper display blocks first.
    text, protected = protect_display_blocks(text)

    def repl(m: re.Match[str]) -> str:
        inner = m.group(1)
        # Collapse newlines/spaces inside inline math.
        inner = re.sub(r"\s+", " ", inner).strip()
        return f"${inner}$"

    # Any remaining paired $$...$$ is not a proper display block, so it should be inline math.
    text = re.sub(r"(?s)\$\$\s*(.+?)\s*\$\$", repl, text)

    text = restore_display_blocks(text, protected)
    return text


def fix_known_bad_chapter05_phrases(text: str) -> str:
    # Clean exact screenshot-type line wrapping after inline conversion.
    text = text.replace(
        "The remaining $T_{\\mathrm{S}} = T - T_{\\mathrm{N}},$ is surplus labour time",
        "The remaining $T_{\\mathrm{S}} = T - T_{\\mathrm{N}}$ is surplus labour time",
    )

    text = text.replace(
        "as $e = \\frac{s}{v} = \\frac{T_{\\mathrm{S}}}{T_{\\mathrm{N}}},$ because",
        "as $e = \\frac{s}{v} = \\frac{T_{\\mathrm{S}}}{T_{\\mathrm{N}}}$, because",
    )

    return text


def process(path: Path) -> bool:
    old = path.read_text(encoding="utf-8")
    new = old

    new = fix_full_line_single_line_display(new)
    new = fix_remaining_inline_pairs(new)

    if path.name == "05-labour-power-wages-surplus-labour-and-surplus-value.md":
        new = fix_known_bad_chapter05_phrases(new)

    if new != old:
        backup = BACKUP_ROOT / path.relative_to(ROOT)
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup)
        path.write_text(new, encoding="utf-8", newline="\n")
        return True
    return False


def main() -> None:
    if not DOCS.exists():
        raise SystemExit("Run this from the repo root; docs/ was not found.")

    changed = []
    for path in sorted(DOCS.rglob("*.md")):
        if process(path):
            changed.append(path)

    print(f"Changed {len(changed)} Markdown files.")
    if changed:
        print(f"Backups: {BACKUP_ROOT}")
        for p in changed:
            print(f"  fixed {p.relative_to(ROOT)}")

    # Report any remaining paired inline display math outside proper display blocks.
    print("\nRemaining malformed paired $$...$$ outside proper display blocks:")
    found = False
    for path in sorted(DOCS.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        protected_text, _ = protect_display_blocks(text)
        if re.search(r"(?s)\$\$\s*.+?\s*\$\$", protected_text):
            found = True
            print(f"  {path.relative_to(ROOT)}")
    if not found:
        print("  none")


if __name__ == "__main__":
    main()
