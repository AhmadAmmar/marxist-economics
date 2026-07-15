#!/usr/bin/env python3
"""
Post-process MkDocs Markdown generated from LaTeX.

Run from the repository root:

    python tools/fix_mkdocs_markdown.py

or, if you place this file in the repo root:

    python fix_mkdocs_markdown.py

What it fixes:
- Literal Pandoc warning lines accidentally written into Markdown.
- Escaped Markdown links like \[2.4\](...) that render visibly instead of as links.
- Inline $$...$$ math inside paragraphs, which Material/MkDocs often leaves literal.
- Single-line display math blocks written as "$$ equation $$".
- A few common LaTeX-to-Markdown residues from this pamphlet conversion.
- The known Chapter 16 macro-drop sentence.
- Optional safety backups before editing.

It does not rewrite the pamphlet prose.
"""

from __future__ import annotations

import re
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()
DOCS = ROOT / "docs"
BACKUP_ROOT = ROOT / "_markdown_fix_backups" / datetime.now().strftime("%Y%m%d-%H%M%S")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def is_display_math_line(line: str) -> bool:
    s = line.strip()
    return s.startswith("$$") and s.endswith("$$") and len(s) > 4


def fix_single_line_dollars(text: str) -> str:
    """
    Fix two common bad forms:
    1. A paragraph contains inline $$...$$. Convert to $...$.
    2. A line is exactly "$$ formula $$". Convert to a proper display block.

    This avoids touching already-correct multi-line blocks:
        $$
        ...
        $$
    """
    fixed_lines: list[str] = []

    for line in text.splitlines():
        stripped = line.strip()

        # Case 2: whole line is a one-line display equation.
        # Example: "$$ r = \frac{s}{c+v}. $$"
        if is_display_math_line(line) and stripped.count("$$") == 2:
            inner = stripped[2:-2].strip()
            fixed_lines.append("$$")
            fixed_lines.append(inner)
            fixed_lines.append("$$")
            continue

        # Case 1: inline display math embedded in prose.
        # Example: "The remaining $$ T_S = T - T_N $$ is surplus time."
        # Convert each same-line $$...$$ to inline $...$.
        def repl_inline(m: re.Match[str]) -> str:
            inner = m.group(1).strip()
            return f"${inner}$"

        # Only matches same-line pairs, not multi-line blocks.
        line = re.sub(r"\$\$\s*([^\n$][^\n]*?[^\n$])\s*\$\$", repl_inline, line)
        fixed_lines.append(line)

    return "\n".join(fixed_lines) + ("\n" if text.endswith("\n") else "")


def fix_escaped_markdown_links(text: str) -> str:
    # Convert \[text\]\(url\) -> [text](url)
    text = re.sub(r"\\\[([^\]]+?)\\\]\\\(([^)]+?)\\\)", r"[\1](\2)", text)

    # Convert \[text\](url) -> [text](url)
    text = re.sub(r"\\\[([^\]]+?)\\\]\(([^)]+?)\)", r"[\1](\2)", text)

    # Convert [text]\(url\) -> [text](url)
    text = re.sub(r"\[([^\]]+?)\]\\\(([^)]+?)\\\)", r"[\1](\2)", text)
    text = re.sub(r"\[([^\]]+?)\]\\\(([^)]+?)\)", r"[\1](\2)", text)

    # If old links point from a chapter page to ../chapters/foo.md, MkDocs usually handles it,
    # but cleaner relative links inside docs/chapters/ are just foo.md.
    text = text.replace("(../chapters/", "(")

    return text


def fix_common_latex_residue(text: str) -> str:
    # Remove accidental Pandoc/conversion warnings.
    text = re.sub(r"(?m)^\[WARNING\].*$\n?", "", text)

    # Remove conflict markers if accidentally present as empty artifact lines.
    # Do NOT silently resolve real conflict bodies; leave obvious marker lines absent.
    # This only removes isolated markers with no content on the line.
    text = re.sub(r"(?m)^<<<<<<<\s*$\n?", "", text)
    text = re.sub(r"(?m)^=======\s*$\n?", "", text)
    text = re.sub(r"(?m)^>>>>>>>\s*$\n?", "", text)

    # Fix raw LaTeX textual formatting that sometimes survives conversion.
    text = re.sub(r"\\emph\{([^{}]+)\}", r"*\1*", text)
    text = re.sub(r"\\textbf\{([^{}]+)\}", r"**\1**", text)

    # Fix common macro residue outside math by replacing with readable symbols.
    replacements = {
        r"\constcap": "c",
        r"\varcap": "v",
        r"\surplus": "s",
        r"\profitrate": "r",
        r"\exploitrate": "e",
        r"\organiccomp": "OCC",
        r"\OCC": "OCC",
        r"\TRPF": "TRPF",
        r"\MELT": r"$\mu$",
        r"\Tn": r"$T_N$",
        r"\Ts": r"$T_S$",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    # Fix \num{...} -> number.
    text = re.sub(r"\\num\{([^{}]+)\}", r"\1", text)

    # Fix common LaTeX nonbreaking/crossref residue.
    text = text.replace("Eq.~", "Eq. ")
    text = text.replace("Section~", "Section ")
    text = text.replace("Example~", "Example ")
    text = re.sub(r"\\eqref\{[^{}]+\}", "", text)
    text = re.sub(r"\\ref\{[^{}]+\}", "", text)
    text = re.sub(r"\\label\{[^{}]+\}", "", text)

    # Remove empty HTML anchors that sometimes get inserted into math blocks.
    text = re.sub(r"<a\s+id=[\"'][^\"']+[\"']\s*></a>", "", text)

    # Fix broken bold conversion examples like **rate of profit}
    text = text.replace("**rate of profit}", "**rate of profit**")
    text = text.replace("**rate of surplus value}", "**rate of surplus value**")

    # Clean a few visible escaped punctuation artifacts.
    text = text.replace(r"\quad", r"\;")
    text = text.replace(r"\Rightarrow", r"\Rightarrow")

    # Remove stray ::: fences sometimes left by failed admonition conversion.
    text = re.sub(r"(?m)^:::\s*$\n?", "", text)

    return text


def fix_known_chapter16_phrase(path: Path, text: str) -> str:
    if path.name != "16-from-critique-to-transition-why-this-matters-for-you.md":
        return text

    bad = "The categories of value, surplus value, constant and variable capital, the , the , and the are not abstract curiosities."
    good = "The categories of value, surplus value, constant and variable capital, the profit rate ($r$), the organic composition of capital (OCC), and the tendency of the rate of profit to fall (TRPF) are not abstract curiosities."
    text = text.replace(bad, good)

    # More flexible repair if punctuation/spacing differs.
    text = re.sub(
        r"The categories of value, surplus value, constant and variable capital, the\s*,\s*the\s*,\s*and the\s*are not abstract curiosities\.",
        good,
        text,
    )
    return text


def fix_chapter05_targeted(path: Path, text: str) -> str:
    if path.name != "05-labour-power-wages-surplus-labour-and-surplus-value.md":
        return text

    # Clean known broken internal links in terminology map if they remain as literal Markdown.
    text = text.replace(
        "(see Section [2.4](02-method-dialectical-and-historical-materialism.md#sec:sociallabour-surplus-control)).",
        "(see [Section 2.4](02-method-dialectical-and-historical-materialism.md#social-labour-surplus-and-the-historical-problem-of-control)).",
    )
    text = text.replace(
        "(see Section [6.2](06-constant-and-variable-capital-circuits-of-capital.md#subsec:circuits)).",
        "(see [Section 6.2](06-constant-and-variable-capital-circuits-of-capital.md#circuits-of-capital)).",
    )
    text = text.replace(
        "(see Section [7.2](07-rate-of-profit-and-organic-composition-of-capital.md#sec:prices-production)",
        "(see [Section 7.2](07-rate-of-profit-and-organic-composition-of-capital.md#competition-average-profit-and-prices-of-production)",
    )

    # If any remaining link is printed as "Section [x](...)", convert to linked section phrase.
    text = re.sub(r"Section \[([0-9.]+)\]\(([^)]+)\)", r"[Section \1](\2)", text)

    return text


def process_file(path: Path) -> bool:
    original = read_text(path)
    text = original

    text = fix_common_latex_residue(text)
    text = fix_escaped_markdown_links(text)
    text = fix_single_line_dollars(text)
    text = fix_known_chapter16_phrase(path, text)
    text = fix_chapter05_targeted(path, text)

    if text != original:
        backup_path = BACKUP_ROOT / path.relative_to(ROOT)
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup_path)
        write_text(path, text)
        return True
    return False


def main() -> None:
    if not DOCS.exists():
        raise SystemExit("No docs/ folder found. Run this from the repository root.")

    md_files = sorted(DOCS.rglob("*.md"))
    changed = []

    for path in md_files:
        if process_file(path):
            changed.append(path)

    print(f"Processed {len(md_files)} Markdown files.")
    print(f"Changed {len(changed)} files.")
    if changed:
        print(f"Backups written to: {BACKUP_ROOT}")
        for p in changed:
            print(f"  fixed: {p.relative_to(ROOT)}")

    # Quick report of remaining suspicious strings.
    suspicious = [
        r"\[WARNING\]",
        r"\\\[",
        r"\$\$[^\\n]+?\$\$",  # single-line dollars likely inline/display error
        r"\\constcap",
        r"\\varcap",
        r"\\surplus",
        r"\\profitrate",
        r"\\exploitrate",
        r"\\num\{",
        r"\\eqref\{",
        r"\\ref\{",
        r"\{@\{",
        r"\\toprule",
        r"\\midrule",
        r"\\bottomrule",
        r"<<<<<<<|=======|>>>>>>>",
    ]

    print("\nRemaining suspicious matches:")
    any_hits = False
    for pat in suspicious:
        hits = []
        rx = re.compile(pat)
        for p in md_files:
            s = read_text(p)
            if rx.search(s):
                hits.append(str(p.relative_to(ROOT)))
        if hits:
            any_hits = True
            print(f"  {pat}:")
            for h in hits[:20]:
                print(f"    {h}")
            if len(hits) > 20:
                print(f"    ... and {len(hits)-20} more")
    if not any_hits:
        print("  none")


if __name__ == "__main__":
    main()
