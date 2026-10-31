# Sialkot football example

A worked example shared with section 5 of the pamphlet. Shared figures live in `data/sialkot.json`.

- `report.tex`: the full worked note.
- `slides.tex`: the current square slides. Its figures come from `latex/generated/sialkot_numbers.tex`.
- `slides_old.tex`: the earlier slides, kept for the record.

Build the slides with `pdflatex slides.tex`, run twice, in this folder. Run `python tools/sialkot.py` first if the data has changed.

`notes.json` holds the words to read aloud for each slide, in order. `instagram/` keeps each version of the images in its own dated folder, named with a fingerprint of the slides' text. The folder `2026-05-01_original` holds the first published version.

`python tools/build_all.py` from the project root rebuilds everything here. See the [guide](https://ahmadammar.github.io/marxist-economics/how-it-works/).
