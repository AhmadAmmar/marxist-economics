# Marxian Economics 101

This repository contains a LaTeX pamphlet and a MkDocs Material website version.

An introduction to political economy for organisers, by Comrade Ammara.

**Read it:** [website](https://ahmadammar.github.io/marxist-economics/) · [PDF](https://ahmadammar.github.io/marxist-economics/Marxian-Political-Economy.pdf) · [the mathematics, step by step](https://ahmadammar.github.io/marxist-economics/mathematics/) · [worked example: Sialkot footballs](https://ahmadammar.github.io/marxist-economics/examples/sialkot/)

**Found a mistake or have an idea?** [Open an issue](https://github.com/AhmadAmmar/marxist-economics/issues/new/choose), [join a discussion](https://github.com/AhmadAmmar/marxist-economics/discussions), or read [how to take part](https://ahmadammar.github.io/marxist-economics/contribute/). You don't need to code.

## What is here

| Folder | Contents |
|---|---|
| `latex/` | The pamphlet's source: the one place to edit its text |
| `data/` | Figures shared across documents, with sources, and references for Zotero |
| `marxian/` | The equations as Python functions, with a command line |
| `examples/sialkot/` | The worked example: report, slides, speaker notes and Instagram images, with every version kept |
| `cheatsheet/` | Source of the printable equation sheet |
| `tools/` | Build and checking scripts |
| `tests/` | Tests against the pamphlet's worked examples |
| `docs/` | The website. Chapters, references, appendices and downloads are generated |

## Build it

```powershell
python -m pip install -r requirements.txt
python tools/build_all.py --site
```

This needs Pandoc 2.12, LaTeX and Poppler. Pushing to GitHub rebuilds and publishes the site if all checks pass. [How this project is built](https://ahmadammar.github.io/marxist-economics/how-it-works/) explains every step.

## Licence and citation

Text: CC BY 4.0. Code: MIT. See `LICENSE`, `LICENSE-CODE` and `CITATION.cff`.
