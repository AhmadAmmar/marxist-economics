# Marxian Economics 101

This repository contains the Marxian economics pamphlet in two publication forms:

- **LaTeX source archive** in `latex/` (authoritative source)
- **GitHub Pages website** in `docs/` built with MkDocs Material

## Key paths

- Public PDF (stable URL): `docs/Marxian-Political-Economy.pdf`
- LaTeX source files: `latex/main.tex`, `latex/content.tex`, `latex/notation.tex`, `latex/glossary.tex`, `latex/bibliography.tex`
- LaTeX bundle: `latex/latex-source.zip`

## Local build

```bash
pip install -r requirements.txt
mkdocs serve
```

## Deploy (GitHub Pages)

The workflow under `.github/workflows/` builds and deploys automatically via GitHub Actions.

## Updating from new LaTeX revisions

1. Update files under `latex/`.
2. Copy the latest compiled PDF into `docs/Marxian-Political-Economy.pdf` (keep filename unchanged).
3. Regenerate or manually update Markdown chapter files under `docs/chapters/`, `docs/appendix-notation.md`, `docs/appendix-glossary.md`, and `docs/references.md`.
4. Run `mkdocs build --strict` before pushing.
