# Contributing

You don't need to code to help. See the [plain guide](https://ahmadammar.github.io/marxist-economics/contribute/) for ways to report errors, suggest ideas or discuss the argument.

## Changing the source

- Text: `latex/`. Pages in `docs/chapters/` are generated from it, so don't edit them.
- Shared figures: `data/sialkot.json`, with a source for each.
- Equations: `marxian/`, with a test in `tests/` that checks a worked example.

Run `python tools/build_all.py --site` and open a pull request. It needs Python, Pandoc 2.12, LaTeX and Poppler. [How the project is built](https://ahmadammar.github.io/marxist-economics/how-it-works/) explains each step.

Please be specific, quote sources, and keep disagreement comradely.
