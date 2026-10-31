"""Write the pamphlet's and the Sialkot example's references as RIS for Zotero and other reference managers.

    python tools/export_refs.py        writes data/references.ris

LaTeX \\bibitem entries are free text, so each becomes a record with the whole citation in its title and notes, plus its address where there is one.
Tidy individual records in the reference manager if needed.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXTRA = [("Atkin, D. et al. (2015) Organizational Barriers to Technology Adoption: Evidence from Soccer-Ball Producers in Pakistan. NBER Working Paper 21417.", "https://www.nber.org/papers/w21417"),
         ("Trade Development Authority of Pakistan. Annual Report: Pakistan Trade Perspective FY 2023-24.", "https://tdap.gov.pk/"),
         ("Dawn (Reuters) (9 December 2022) 'Made-in-Sialkot' ball puts Pakistan in FIFA World Cup.", "https://www.dawn.com/"),
         ("Global Living Wage Coalition. Living wage estimates for Pakistan.", "https://www.globallivingwage.org/countries/pakistan/")]


def clean(t):
    t = re.sub(r"(?<!\\)%.*", "", t)
    t = re.sub(r"\\(?:url|href)\{([^}]*)\}(?:\{[^}]*\})?", r"\1", t)
    t = re.sub(r"\\(?:emph|textit|textbf)\{([^{}]*)\}", r"\1", t)
    t = t.replace("--", "-").replace("~", " ").replace("\\&", "&").replace("\\%", "%").replace("``", '"').replace("''", '"')
    return " ".join(re.sub(r"\\[a-zA-Z]+\*?|[{}]", "", t).split())


def build():
    t = (ROOT / "latex/bibliography.tex").read_text(encoding="utf8").split("\\end{thebibliography}")[0]
    items = [clean(i) for i in re.split(r"\\bibitem(?:\[[^\]]*\])?\{[^}]+\}", t)[1:]]
    rows = [(i, (re.findall(r"https?://\S+", i) or [""])[0].rstrip(".,)")) for i in items] + EXTRA
    out = []
    for text, url in rows:
        year = re.search(r"\((\d{4})", text)
        out += ["TY  - GEN", f"TI  - {text}"] + ([f"PY  - {year.group(1)}"] if year else []) + ([f"UR  - {url}"] if url else []) + ["KW  - Marxian Economics 101", "ER  - ", ""]
    target = ROOT / "data/references.ris"
    target.write_text("\n".join(out), encoding="utf8", newline="\n")
    print(f"wrote {len(rows)} references to {target}")


if __name__ == "__main__":
    build()
