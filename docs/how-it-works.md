# How this project is built

This page explains how one set of source files becomes the website, PDFs, slides, images and calculator. It is written so that you can learn from it, or reuse it for your own project.

## The idea: one source, many outputs

Copying text and numbers between files lets them drift apart. So each thing lives in one place, and everything else is generated.

| You edit | Which holds | It becomes |
|:--|:--|:--|
| `latex/` | The pamphlet | The PDF and the web chapters, references and appendices |
| `data/sialkot.json` | Shared football figures, with sources | Macros used by the pamphlet and slides |
| `examples/sialkot/*.tex` | The report and slides | Their PDFs |
| `examples/sialkot/notes.json` | Words to read aloud | PowerPoint speaker notes |
| `marxian/` | Equations as Python functions | The shared figures and command line |
| `docs/mathematics.md`, `contribute.md`, this page | Pages written directly | Web pages |

Never edit `docs/chapters/`, `docs/references.md`, `docs/appendix-*.md`, `docs/downloads/` or `latex/generated/`. The next build replaces them.

## What happens when you change something

**If you push to GitHub:** the workflow in `.github/workflows/deploy-pages.yml` installs the tools, rebuilds everything, runs all the checks and publishes the site if they pass. If a check fails, the old site stays up, and GitHub shows you why under *Actions*.

**On your own computer**, nothing changes until you run the build:

```powershell
python tools/build_all.py --site
```

To preview the result, run `python -m mkdocs serve` and open the address it prints.

**Instagram images** are made locally and committed, so that every version stays in the project's history. After a slide change, run the build and commit the new folder in `examples/sialkot/instagram/`. Old folders are never replaced.

## A normal update, step by step

```powershell
# 1. Change latex/content.tex
# 2. Rebuild and check everything
python tools/build_all.py --site
# 3. Review the changes
git status
git diff
# 4. Save a version with a short description
git add -A
git commit -m "Clarify the example in section 5"
# 5. Publish
git push
```

## The tools

| Tool | What it does |
|:--|:--|
| `tools/build_all.py` | Runs every step below in order |
| `tools/sialkot.py` | Turns `data/sialkot.json` into LaTeX macros through `marxian/` |
| `tools/tex_to_web.py` | Converts LaTeX to web pages with Pandoc, numbering sections, equations and citations as LaTeX does |
| `tools/build_pdf.py` | Compiles the PDF in a clean folder and records which source made it |
| `tools/build_carousel.py` | Makes the Instagram images and PowerPoint deck |
| `tools/make_workbook.py` | Writes the Excel calculator with live formulas |
| `tools/export_refs.py` | Writes `data/references.ris` for reference managers |
| `tools/check_sync.py` | Confirms that PDF, LaTeX, web pages and figures agree |
| `tools/check_links.py` | Tests links, anchors and references |
| `tools/check_arithmetic.py` | Recalculates numeric steps in equations |

## Going back to an earlier version

Git keeps every committed version. A *tag* names an important one.

```powershell
git tag                                # list named versions
git checkout before-open-project-2026-11-01   # look at one
git checkout main                      # come back
git revert <commit>                    # undo a change while keeping the history
```

## Instagram images

The images are 1440 by 1440 pixel PNG files. PNG suits text on a plain background, because its edges stay sharp, and Instagram recompresses every upload anyway. Instagram doesn't accept TIFF, and JPEG adds blur around text before Instagram compresses it again. A carousel can hold up to 20 images.

## References

`data/references.ris` holds the pamphlet's reference list. To add it to Zotero, choose *File > Import* and select that file. To collect PDFs, select the items, right-click and choose *Find Full Text*. Some sources are paywalled, so Zotero can't fetch everything.

## What goes where

| Project | Scope |
|:--|:--|
| This repository | The pamphlet, its example, and tools that know about them |
| [research-helpers](https://github.com/GeospatialGeeks/research-helpers) | General tools for any project, such as converting LaTeX to Word and PDF slides to images and PowerPoint |
| [ulster-thesis-template](https://github.com/GeospatialGeeks/ulster-thesis-template) | The thesis template |

The rule: if a tool would help a stranger with a different project, it belongs in research-helpers. If it needs to know about this pamphlet, it stays here.

## What the checks cannot do

They confirm that the outputs agree and that the sums add up. They can't tell you that an argument is right, or that a source says what is claimed. That takes readers, which is why [your corrections](contribute.md) matter.
