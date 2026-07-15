#!/usr/bin/env python3
"""
Targeted repair for Chapter 5 rendering problems and math overflow.

Run from repo root:
    python .\fix_chapter05_rendering_and_overflow.py

Then:
    python -m mkdocs build
    python -m mkdocs serve

What it does:
- Replaces the visibly broken coffee-shop example with clean Markdown/MathJax.
- Replaces the visibly broken Sialkot football example block with clean Markdown/MathJax.
- Escapes currency dollar signs that break Markdown math parsing.
- Removes MathJax line-spacing fragments like \[0.3em] where they are rendering visibly.
- Adds/updates CSS so long equations/tables scroll horizontally instead of overflowing.
- Backs up edited files under _markdown_fix_backups/.
"""

from __future__ import annotations

import re
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path.cwd()
DOCS = ROOT / "docs"
CH5 = DOCS / "chapters" / "05-labour-power-wages-surplus-labour-and-surplus-value.md"
CSS = DOCS / "stylesheets" / "extra.css"
BACKUP = ROOT / "_markdown_fix_backups" / datetime.now().strftime("%Y%m%d-%H%M%S-ch5-rendering")


COFFEE_BLOCK = r"""!!! example "Example: A coffee-shop worker"
    Suppose:

    - The shop sells drinks and snacks worth \$800 during an 8-hour shift.
    - Of this, \$300 covers the value of used-up constant capital (beans, milk, cups, energy, machine depreciation) — this is $c$.
    - The barista's wage bill for the shift is \$100 — this is $v$.

    We want to find:

    - the new value created by living labour during the shift ($v+s$),
    - the surplus value $s$,
    - the rate of exploitation $e$, and
    - how many hours of the 8-hour day are necessary labour time and how many are surplus labour time.

    ### Step 1: Separate the value created by labour from the value of used-up machinery and inputs

    The total value of the day's output is \$800. Of this, \$300 is just the value of used-up constant capital $c$ being transferred to the finished products. The remainder must therefore be new value created by living labour:

    $$
    \begin{aligned}
    \text{Total value of output} &= \text{\$}800,\\
    \text{Value of used-up constant capital }(c) &= \text{\$}300,\\
    \Rightarrow\quad
    \text{New value created by labour }(v+s)
      &= \text{Total value} - \text{Constant capital}\\
      &= \text{\$}800 - \text{\$}300\\
      &= \text{\$}500.
    \end{aligned}
    $$

    So the labour of the barista has added \$500 of new value during the shift:

    $$
    v+s=\text{\$}500.
    $$

    ### Step 2: Split this new value into wages and surplus-value

    Out of this \$500 of new value, the capitalist pays the barista \$100 as wages. This \$100 is the value of variable capital $v$:

    $$
    v=\text{\$}100.
    $$

    The rest of the new value is surplus-value $s$:

    $$
    \begin{aligned}
    s
      &= (v+s)-v\\
      &= \text{\$}500-\text{\$}100\\
      &= \text{\$}400.
    \end{aligned}
    $$

    So:

    $$
    s=\text{\$}400.
    $$

    ### Step 3: Compute the rate of exploitation

    The *rate of exploitation* (or *rate of surplus-value*) is defined as the ratio of surplus-value to variable capital:

    $$
    e=\frac{s}{v}.
    $$

    Plugging in our numbers:

    $$
    \begin{aligned}
    e
      &= \frac{s}{v}\\
      &= \frac{\text{\$}400}{\text{\$}100}\\
      &= 4.
    \end{aligned}
    $$

    As a percentage:

    $$
    e=4\times 100\%=400\%.
    $$

    This means that, measured in value terms, the barista produces four times as much surplus for the owner as they receive back in wages.

    ### Step 4: Translate the value relations into hours of the working day

    The barista works an 8-hour shift. We know that, in value terms,

    $$
    v:s=100:400=1:4.
    $$

    So, of the *new* value (\$500) created in the day, one-fifth belongs to necessary labour (reproducing the wage) and four-fifths is surplus labour.

    Necessary labour time is therefore one-fifth of the working day:

    $$
    \begin{aligned}
    \text{Necessary labour time}
      &= \frac{v}{v+s}\times 8\ \text{hours}\\
      &= \frac{100}{500}\times 8\\
      &= 0.2\times 8\\
      &= 1.6\ \text{hours}.
    \end{aligned}
    $$

    The remaining part of the working day is surplus labour time:

    $$
    \begin{aligned}
    \text{Surplus labour time}
      &= 8\ \text{hours}-1.6\ \text{hours}\\
      &= 6.4\ \text{hours}.
    \end{aligned}
    $$

    So in this simple coffee-shop example:

    - In the first $1.6$ hours of the shift, the barista produces value equivalent to their own wage (necessary labour time).
    - In the remaining $6.4$ hours, they produce surplus-value for the owner (surplus labour time).
    - Over the whole day, the rate of exploitation is $e=400\%$: for every \$1 paid in wages, \$4 of surplus-value is extracted.

    This does not mean that the branch manager personally pockets \$400. The surplus value is divided, through complex mechanisms, into different forms of revenue: profit of enterprise, interest on loans, rent to the landlord, franchise fees to the global brand, and taxes to the state. Marx's key point is that all of these streams ultimately originate in unpaid surplus labour time like that of this barista.

"""


SIALKOT_BLOCK = r"""## Example: Sialkot football stitching

!!! note "Data-year note"
    The Sialkot football examples combine figures from different sources and years: piece-rate and time-per-ball benchmarks from 2022 reporting, producer-cost figures from a baseline survey in Atkin et al.'s Sialkot study, and retail/export benchmarks converted into PKR using a stated exchange-rate convention. The aim is not to pretend these are one same-year firm account. The aim is to make the class relation legible: wage, labour-time, producer-stage cost, surplus, and downstream price-forms.

!!! example "Example: Sialkot football stitching: piece-wage, implied time-wage, and the retail-price gap"
    A piece-wage can be rewritten as a time-wage once we specify the time required to produce one unit.

    Using widely reported benchmark figures for Sialkot-style hand-stitching, let the piece rate be:

    $$
    w_{\text{piece}}=\text{PKR }160/\text{ball},
    $$

    and let the labour-time per ball be:

    $$
    t_{\text{ball}}\approx 3\ \text{hours/ball}.
    $$

    These figures are used here as an illustrative benchmark, not as a complete firm-level accounts sheet for a single year.[^sialkot-bloomberg]

    Then the implied hourly wage is:

    $$
    \begin{aligned}
    w_{\text{hour}}
      &= \frac{w_{\text{piece}}}{t_{\text{ball}}}\\
      &\approx \frac{\text{PKR }160}{3\ \text{hours}}\\
      &\approx \text{PKR }53.33/\text{hour}.
    \end{aligned}
    $$

    If the worker stitches roughly $q=3$ balls per day, then:

    $$
    \begin{aligned}
    w_{\text{day}}
      &= w_{\text{piece}}\times q\\
      &= \text{PKR }160\times 3\\
      &= \text{PKR }480,
    \end{aligned}
    $$

    and:

    $$
    \begin{aligned}
    T_{\text{day}}
      &= t_{\text{ball}}\times q\\
      &= 3\times 3\\
      &= 9\ \text{hours}.
    \end{aligned}
    $$

    If this pace is sustained for roughly $20$ paid workdays in a month, then monthly wage income is:

    $$
    \begin{aligned}
    w_{\text{month}}
      &\approx \text{PKR }480\times 20\\
      &= \text{PKR }9600.
    \end{aligned}
    $$

    Against a quoted 2022 living-wage benchmark of about $\text{PKR }20000$ per month, this is:

    $$
    \begin{aligned}
    \frac{w_{\text{month}}}{L_{\text{month}}}
      &\approx \frac{9600}{20000}\\
      &=0.48\\
      &\Rightarrow 48\%.
    \end{aligned}
    $$

    So even before we compare the wage to export or retail prices, the wage relation already appears as a social-reproduction problem: the missing income has to be made up through longer hours, debt, rationing, unpaid household labour, or some combination of these.

    Now compare this wage to a downstream retail benchmark. Suppose a branded match ball retails at $P_{\text{retail}}=\text{USD }165$.[^sialkot-retail]

    Using the pamphlet's exchange-rate convention:

    $$
    \begin{aligned}
    P_{\text{retail}}
      &\approx 165\times \text{PKR }279.897\\
      &\approx \text{PKR }46183.
    \end{aligned}
    $$

    The number of wage-hours required to earn the retail price of one ball is:

    $$
    \begin{aligned}
    H
      &=\frac{P_{\text{retail}}}{w_{\text{hour}}}\\
      &\approx\frac{\text{PKR }46183}{\text{PKR }53.33/\text{hour}}\\
      &\approx 866\ \text{hours}.
    \end{aligned}
    $$

    Converted into footballs stitched and 9-hour workdays:

    $$
    \begin{aligned}
    \text{balls required}
      &\approx \frac{H}{t_{\text{ball}}}\\
      &\approx \frac{866}{3}\\
      &\approx 289\ \text{balls},
    \end{aligned}
    $$

    and:

    $$
    \begin{aligned}
    \text{workdays required}
      &\approx \frac{H}{T_{\text{day}}}\\
      &\approx \frac{866}{9}\\
      &\approx 96.2\ \text{workdays}.
    \end{aligned}
    $$

    So, under these benchmark assumptions, the worker would have to stitch roughly $289$ footballs — nearly $96$ nine-hour workdays — to earn enough wages to buy one branded match ball at the retail benchmark.

    This calculation does *not* mean that the local employer pockets the full retail price. It shows something more specific: the same commodity confronts the stitcher as an alien object with a money-price set elsewhere in the chain. The wage-form is small relative to the price-forms the object later takes on in circulation, through export contracting, branding, logistics, retail markups, finance, and rent.

    We return to the same industry in the producer-stage cost table after introducing constant capital, variable capital, cost price, and producer-stage surplus.

### Piece-rates and technological change

The Sialkot case also shows why technology is never just a neutral matter of "efficiency". Atkin et al.'s study of Sialkot football producers examined a new cutting die that reduced waste of rexine, the main material input. From the owner's standpoint, this looked like a straightforward cost-saving innovation. But the relevant workers were commonly paid by piece-rate. If the new technique slowed them down while they learned it, and if the piece-rate was not adjusted, then part of the cost of adoption was shifted onto workers as a lower effective hourly wage.

A productive force does not enter society abstractly or in isolation, but through a labour process already organised by property, wages, supervision, and competition. Under capitalist control, even a technique that could reduce material waste can become a conflict over who bears the transition cost and who captures the gain. That same logic returns later in automation and AI: the question is not only what the tool can do, but who owns it, who controls its introduction, how it changes the pace of work, and whether the saving becomes free time for workers or surplus for capital.

[^sialkot-bloomberg]: Bloomberg Businessweek reported benchmark figures for Sialkot football workers in November 2022, including a piece-rate figure, time-per-ball estimate, daily output, an illustrative monthly wage figure, and a living-wage benchmark. See the corresponding reference entry in the references page.

[^sialkot-retail]: For the retail-price benchmark and exchange-rate convention, see the corresponding GOAL and NBP reference entries in the references page.

"""


CSS_APPEND = r"""
/* Keep long equations and tables readable instead of letting them overflow. */
.md-typeset .arithmatex {
  max-width: 100%;
  overflow-x: auto;
  overflow-y: hidden;
  padding-bottom: 0.25rem;
}

.md-typeset div.arithmatex {
  margin: 1em 0;
}

.md-typeset table:not([class]) {
  display: block;
  max-width: 100%;
  overflow-x: auto;
  white-space: nowrap;
}

.md-typeset .admonition,
.md-typeset details {
  overflow-x: auto;
}
"""


def backup_file(path: Path) -> None:
    backup = BACKUP / path.relative_to(ROOT)
    backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, backup)


def escape_currency_dollars(text: str) -> str:
    """
    Convert unescaped currency dollars followed by a digit into literal dollars.
    Then restore pure numeric math spans such as $1.6$ that the previous pass may touch.
    """
    text = re.sub(r"(?<!\\)\$(?=\d)", r"\\$", text)

    # Restore pure numeric inline math accidentally touched by the currency pass:
    # \$1.6$ -> $1.6$
    text = re.sub(r"\\\$([0-9]+(?:\.[0-9]+)?(?:,[0-9]{3})*)\$", r"$\1$", text)

    return text


def clean_general_math_residue(text: str) -> str:
    # Remove optional vertical spacing in aligned equations if it is rendering visibly.
    for sp in ["0.3em", "0.5em", ".3em", ".5em"]:
        text = text.replace(rf"\\[{sp}]", r"\\")
        text = text.replace(rf"\[{sp}]", r"\\")

    # Fix literal bad inline display markers that earlier passes may have left.
    text = text.replace("$$and$$", "and")
    text = text.replace("$$ because", "because")
    text = text.replace("$$because", "because")
    text = text.replace("$$If", "If")
    text = text.replace("$$Converted", "Converted")

    # Remove conversion warnings.
    text = re.sub(r"(?m)^\[WARNING\].*$\n?", "", text)

    return text


def replace_chapter5_blocks(text: str) -> str:
    # Replace coffee example block from admonition start to before Forms of wages.
    coffee_pat = re.compile(
        r'!!! example "Example: A coffee-shop worker".*?(?=\n## Forms of wages|\n## Is this "theft"\?|\n## Example: Sialkot football stitching)',
        re.S,
    )
    if coffee_pat.search(text):
        text = coffee_pat.sub(lambda _m: COFFEE_BLOCK, text)

    # Replace Sialkot section until smartphone section.
    sialkot_pat = re.compile(
        r"\n## Example: Sialkot football stitching.*?(?=\n## Example: smartphone assembly|\n# Constant and variable capital|\n## Smartphone assembly)",
        re.S,
    )
    if sialkot_pat.search(text):
        text = sialkot_pat.sub(lambda _m: "\n" + SIALKOT_BLOCK.rstrip() + "\n\n", text)

    return text


def fix_markdown_files() -> list[Path]:
    changed = []
    for path in sorted(DOCS.rglob("*.md")):
        old = path.read_text(encoding="utf-8")
        new = old
        new = escape_currency_dollars(new)
        new = clean_general_math_residue(new)

        if path == CH5:
            new = replace_chapter5_blocks(new)

        if new != old:
            backup_file(path)
            path.write_text(new, encoding="utf-8", newline="\n")
            changed.append(path)
    return changed


def patch_css() -> bool:
    CSS.parent.mkdir(parents=True, exist_ok=True)
    old = CSS.read_text(encoding="utf-8") if CSS.exists() else ""
    if "Keep long equations and tables readable" in old:
        return False
    if CSS.exists():
        backup_file(CSS)
    CSS.write_text(old.rstrip() + "\n\n" + CSS_APPEND.lstrip(), encoding="utf-8", newline="\n")
    return True


def report() -> None:
    patterns = {
        "possible unescaped currency dollars": r"(?<!\\)\$[0-9]",
        "literal paired $$ outside display blocks": r"\$\$[^\n]+?\$\$",
        "visible optional spacing fragments": r"\\?\[(?:0\.3em|0\.5em|\.3em|\.5em)\]",
        "bad concatenations": r"ofnewvalue|paidinwages|Ifthis|Convertedinto|Tday\s*=",
        "warnings": r"\[WARNING\]",
        "raw LaTeX table fragments": r"\\toprule|\\midrule|\\bottomrule|\{@\{",
    }

    print("\nRemaining suspicious matches:")
    any_hit = False
    for label, pat in patterns.items():
        rx = re.compile(pat)
        hits = []
        for p in sorted(DOCS.rglob("*.md")):
            if rx.search(p.read_text(encoding="utf-8")):
                hits.append(str(p.relative_to(ROOT)))
        if hits:
            any_hit = True
            print(f"  {label}:")
            for h in hits[:20]:
                print(f"    {h}")
            if len(hits) > 20:
                print(f"    ... and {len(hits)-20} more")
    if not any_hit:
        print("  none")


def main() -> None:
    if not DOCS.exists():
        raise SystemExit("No docs/ folder found. Run from repo root.")
    if not CH5.exists():
        raise SystemExit(f"Could not find {CH5}")

    changed = fix_markdown_files()
    css_changed = patch_css()

    print(f"Changed {len(changed)} Markdown files.")
    if css_changed:
        print(f"Changed CSS: {CSS.relative_to(ROOT)}")
    if changed or css_changed:
        print(f"Backups: {BACKUP}")
        for p in changed:
            print(f"  fixed {p.relative_to(ROOT)}")

    report()


if __name__ == "__main__":
    main()
