# Marxian Economics 101

This repository contains a LaTeX pamphlet and a MkDocs Material website version.

## Structure

- `latex/` — authoritative LaTeX source files.
- `docs/Marxian-Political-Economy.pdf` — public PDF used by the website.
- `docs/chapters/` — generated web-reading chapters.
- `docs/references.md` — references converted from `bibliography.tex`.
- `docs/appendix-notation.md` and `docs/appendix-glossary.md` — appendices.

## One source

`latex/` holds the text and `data/sialkot.json` the figures shared with the Sialkot example. Change those, then run:

```powershell
python tools/build_all.py --site
```

This generates the shared macros, the web pages, the pamphlet PDF and the Sialkot report and slides, then checks that they agree. GitHub regenerates the web pages and repeats the check before publishing, and refuses if the LaTeX changed without a new PDF.

`marxian/` holds the pamphlet's equations as Python functions, tested against its worked examples. Code is under the MIT licence in `LICENSE-CODE`.

## Local build on Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m mkdocs serve
python -m mkdocs build
```
