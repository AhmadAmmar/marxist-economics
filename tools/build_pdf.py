"""Build the pamphlet PDF from latex/ in a temporary folder, publish it to docs/, and record exactly which source made it.

    python tools/build_pdf.py
"""
import hashlib
import json
import pathlib
import shutil
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCES = ["main.tex", "preamble.tex", "content.tex", "notation.tex", "glossary.tex", "bibliography.tex"]
RECORD = ROOT / "docs/pdf-source.json"


def lf_hash(path):
    """Line endings are ignored, so Windows and Linux checkouts agree."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def source_hashes():
    return {f: lf_hash(ROOT / "latex" / f) for f in SOURCES}


def build():
    with tempfile.TemporaryDirectory() as t:
        work = pathlib.Path(t) / "latex"
        shutil.copytree(ROOT / "latex", work)
        run = lambda *c: subprocess.run(c, cwd=work, capture_output=True, text=True, errors="replace")
        run("pdflatex", "-interaction=nonstopmode", "main.tex")
        run("bibtex", "main")
        run("makeindex", "-s", "main.ist", "-o", "main.gls", "main.glo")
        for _ in range(2):
            run("pdflatex", "-interaction=nonstopmode", "main.tex")
        log = (work / "main.log").read_text(encoding="latin1", errors="replace")
        errors = [l for l in log.splitlines() if l.startswith("! ")]
        if errors or not (work / "main.pdf").exists():
            raise SystemExit("LaTeX failed: " + "; ".join(errors[:5]))
        shutil.copy2(work / "main.pdf", ROOT / "docs/Marxian-Political-Economy.pdf")
    RECORD.write_text(json.dumps({"pdf": lf_hash(ROOT / "docs/Marxian-Political-Economy.pdf"), "sources": source_hashes()}, indent=1) + "\n", encoding="utf8", newline="\n")
    print("built docs/Marxian-Political-Economy.pdf")


if __name__ == "__main__":
    build()
