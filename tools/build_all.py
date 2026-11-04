"""Rebuild everything from the sources, in order, then check it agrees.

    python tools/build_all.py            shared numbers, web pages, pamphlet PDF, Sialkot report and slides, sync check
    python tools/build_all.py --site     also build the website into site/

Change only latex/, data/ and examples/sialkot/*.tex. Everything else is generated.
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import build_carousel
import build_pdf
import export_refs
import make_workbook
import sialkot
import tex_to_web

ROOT = sialkot.ROOT


def examples():
    """Compile the example in a temporary copy, so that no LaTeX leftovers enter the repository."""
    with tempfile.TemporaryDirectory() as t:
        work = pathlib.Path(t)
        shutil.copytree(ROOT / "latex/generated", work / "latex/generated")
        shutil.copytree(ROOT / "examples/sialkot", work / "examples/sialkot", ignore=shutil.ignore_patterns("*.pdf", "*.aux", "*.log", "*.out"))
        d = work / "examples/sialkot"
        for name in ("report", "slides"):
            for _ in range(2):
                subprocess.run(["pdflatex", "-interaction=nonstopmode", f"{name}.tex"], cwd=d, capture_output=True, errors="replace")
            log = (d / f"{name}.log").read_text(encoding="latin1", errors="replace")
            errors = [l for l in log.splitlines() if l.startswith("! ")]
            if errors or not (d / f"{name}.pdf").exists():
                raise SystemExit(f"{name}.tex failed: {errors[:3]}")
            shutil.copy2(d / f"{name}.pdf", ROOT / "examples/sialkot" / f"{name}.pdf")
            print("built", f"examples/sialkot/{name}.pdf")


def cheatsheet():
    with tempfile.TemporaryDirectory() as t:
        shutil.copy2(ROOT / "cheatsheet/marxian_cheatsheet.tex", t)
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "marxian_cheatsheet.tex"], cwd=t, capture_output=True, errors="replace")
        (ROOT / "docs/downloads").mkdir(exist_ok=True)
        shutil.copy2(pathlib.Path(t) / "marxian_cheatsheet.pdf", ROOT / "docs/downloads/marxian_cheatsheet.pdf")


def publish_downloads():
    d = ROOT / "docs/downloads"
    d.mkdir(exist_ok=True)
    shutil.copy2(ROOT / "examples/sialkot/slides.pdf", d / "sialkot_slides.pdf")
    shutil.copy2(ROOT / "examples/sialkot/report.pdf", d / "sialkot_report.pdf")


if __name__ == "__main__":
    print("wrote", sialkot.write())
    tex_to_web.main(ROOT / "docs")
    build_pdf.build()
    examples()
    export_refs.build()
    make_workbook.build(ROOT / "docs/downloads/marxian_calculator.xlsx")
    cheatsheet()
    publish_downloads()
    if "--no-carousel" not in sys.argv:
        build_carousel.build()
    check = subprocess.run([sys.executable, str(ROOT / "tools/check_sync.py")])
    if check.returncode:
        sys.exit(1)
    if "--site" in sys.argv:
        subprocess.run([sys.executable, "-m", "mkdocs", "build", "--strict"], cwd=ROOT, check=True)
        if subprocess.run([sys.executable, str(ROOT / "tools/check_links.py")]).returncode:
            sys.exit(1)
