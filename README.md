# Marxian Economics 101

This repository contains a LaTeX pamphlet and a MkDocs Material website version.

## Structure

- `latex/` — authoritative LaTeX source files.
- `docs/Marxian-Political-Economy.pdf` — public PDF used by the website.
- `docs/chapters/` — generated web-reading chapters.
- `docs/references.md` — references converted from `bibliography.tex`.
- `docs/appendix-notation.md` and `docs/appendix-glossary.md` — appendices.

## Keeping everything in step

`latex/` is the source. After changing it, run `python tools/build_pdf.py`, update the web chapters, and run `python tools/check_sync.py`. GitHub runs the same check before publishing. Figures shared with the Sialkot example live in `data/sialkot.json`, and `tools/sialkot.py` writes them as LaTeX macros.

## Local build on Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m mkdocs serve
python -m mkdocs build
```
