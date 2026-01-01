# Marxian Economics 101 (GitHub Pages)

This repository contains:

- A PDF of the pamphlet (in `docs/assets/`)
- A web version (MkDocs Material) with chapter pages
- A downloadable LaTeX source bundle

## Local preview

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
mkdocs serve
```

Then open the local address printed in your terminal.

## GitHub Pages deployment

1. Push this repo to GitHub on the `main` branch.
2. In GitHub: **Settings → Pages**.
3. Under **Build and deployment**, set **Source** to **GitHub Actions**.
4. The workflow in `.github/workflows/deploy-pages.yml` will publish the site.

If you prefer “Deploy from a branch” instead of Actions, run `mkdocs build`, commit the `site/` output to a `gh-pages` branch, and point Pages at that branch.
