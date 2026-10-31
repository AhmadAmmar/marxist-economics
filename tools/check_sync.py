"""Are the LaTeX source, the PDF, the web chapters and the Sialkot example telling the same story? Exit code 1 if not.

    python tools/check_sync.py

1. PDF: the published PDF was built from the current LaTeX, using the record written by build_pdf.py.
2. Web: the chapters hold the same words and numbers as latex/content.tex, in any order, because footnotes move to chapter ends.
3. Sialkot: arithmetic from data/sialkot.json holds, and stated figures appear in each document that uses them.
It compares text. It does not show that an argument or a source is right.
"""
import collections
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import build_pdf
import sialkot

ROOT = sialkot.ROOT
MAX_WORD_DIFF = 80  # headings and layout words legitimately differ between LaTeX and Markdown
LAYOUT_NUMBERS = {"1.5", "1.15", "0"}


def clean(t):
    t = t.replace("\\$", " ")
    t = re.sub(r"\$\$.*?\$\$|\\\[.*?\\\]|\\begin\{(equation\*?|align\*?|gather\*?|tabularx|tabular|table)\}.*?\\end\{\1\}", " ", t, flags=re.S)
    t = re.sub(r"\$[^$\n]*\$|\\\(.*?\\\)", " ", t)
    t = re.sub(r"<span class=\"citation\".*?</span>|<table.*?</table>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"\[\^[^\]]*\]:?|\{ *[#.][^}]*\}|\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"(?m)^\|.*\|$", " ", t)
    t = re.sub(r"\\(cite\w*|label|ref|eqref|autoref|index)\*?(\[[^\]]*\])*\{[^{}]*\}", " ", t)
    t = re.sub(r"(?<!\\)%.*", " ", t)
    t = re.sub(r"\\(begin|end)\{[^}]*\}", " ", t)
    t = re.sub(r"\\[a-zA-Z]+\*?", " ", t)
    return re.findall(r"[a-z]{3,}", t.lower())


def stated(t):
    return collections.Counter(n for n in re.findall(r"(?<![\w.])\d[\d,]*\.\d+|(?<![\w.,])\d{1,3}(?:,\d{3})+", t.replace("{,}", ",")) if n not in LAYOUT_NUMBERS)


def word_problems(tex, web):
    a, b = collections.Counter(clean(tex)), collections.Counter(clean(web))
    only_tex, only_web = sum((a - b).values()), sum((b - a).values())
    return [f"web and LaTeX differ by {only_tex} and {only_web} words: {(a - b).most_common(8)} {(b - a).most_common(8)}"] if max(only_tex, only_web) > MAX_WORD_DIFF else []


def number_problems(tex, web):
    a, b = stated(tex), stated(web)
    return [f"number {n} is in the LaTeX but not on the web" for n in a if n not in b]


def main():
    bad = []
    rec = ROOT / "docs/pdf-source.json"
    if not rec.exists():
        bad.append("no record of which source built the PDF: run tools/build_pdf.py")
    else:
        r = json.loads(rec.read_text(encoding="utf8"))
        if r["sources"] != build_pdf.source_hashes():
            bad.append("LaTeX changed after the PDF was built: run tools/build_pdf.py")
        if r["pdf"] != build_pdf.lf_hash(ROOT / "docs/Marxian-Political-Economy.pdf"):
            bad.append("the published PDF is not the one that was built")
    tex = (ROOT / "latex/content.tex").read_text(encoding="utf8")
    web = "\n".join(p.read_text(encoding="utf8") for p in sorted((ROOT / "docs/chapters").glob("*.md")))
    bad += word_problems(tex, web) + number_problems(tex, web)
    d = sialkot.derive(sialkot.inputs())
    for k, want in {"HourlyWage": 53.33, "MonthlyPayPKR": 9600, "CostSum": 210.81, "ProducerPrice": 227.91, "Surplus": 17.08, "NewValue": 73.37, "ExportAvgUSD": 4.44, "RetailPKR": 46183, "HoursToBuy": 866}.items():
        if d[k] != want:
            bad.append(f"Sialkot {k} is {d[k]}, the documents say {want}")
    for doc, figures in json.loads((ROOT / "data/sialkot.json").read_text(encoding="utf8"))["appear_in"].items():
        p = ROOT / doc
        if not p.exists():
            bad.append(f"{doc} is missing")
            continue
        t = p.read_text(encoding="utf8")
        bad += [f"{doc} does not state {f}" for f in figures if not re.search(r"(?<![\d.,])" + re.escape(f) + r"(?!\d)", t)]
    print("\n".join("FAIL " + b for b in bad) or "OK: PDF, LaTeX, web chapters and Sialkot figures agree")
    sys.exit(bool(bad))


if __name__ == "__main__":
    main()
