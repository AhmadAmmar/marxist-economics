"""Generate the web edition from latex/, so that the LaTeX is the only source of the text.

    python tools/tex_to_web.py                write docs/chapters, references and appendices
    python tools/tex_to_web.py --out <dir>    write somewhere else

Numbers for sections, equations, examples and citations are worked out in one pass, as LaTeX does, so links and numbers match the PDF.
Needs pandoc.
"""
import argparse
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
L = ROOT / "latex"
MATH_ENVS = "equation|align"


def slugify(title):
    s = re.sub(r"\\[a-zA-Z]+\*?(\{([^{}]*)\})?", r"\2", title)
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s


def inputs(text, seen=("notation", "glossary", "bibliography")):
    """Strip comments, keeping escaped percent signs."""
    return re.sub(r"(?m)(?<!\\)%.*$", "", text)


def macros():
    """Single-line macros from the preamble, with print-only commands removed, for pandoc to expand."""
    keep = []
    for line in (L / "preamble.tex").read_text(encoding="utf8").splitlines():
        if re.match(r"\\newcommand\{\\[A-Za-z]+\}(\[\d\])?\{.*\}\s*(%.*)?$", line) and "money" not in line:
            keep.append(re.sub(r"\s*%.*$", "", line).replace("\\xspace", ""))
    generated = L / "generated/sialkot_numbers.tex"
    if generated.exists():
        keep += [l for l in generated.read_text(encoding="utf8").splitlines() if l.startswith("\\newcommand")]
    return "\n".join(keep) + "\n"


def bib_keys():
    return re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}", inputs((L / "bibliography.tex").read_text(encoding="utf8")))


def aligned_rows(inner):
    return [r for r in re.split(r"\\\\", inner) if r.strip()]


def split_sections(text):
    parts = re.split(r"(?m)^(?=\\section\{)", text)
    return parts[0], parts[1:]


def number(sections):
    """Walk the source in order and give every label its number, chapter and anchor."""
    labels, chapters = {}, []
    token = re.compile(r"\\(section|subsection)\{((?:[^{}]|\{[^{}]*\})*)\}|\\begin\{(equation|align|example|table)\}|\\label\{([^}]+)\}|(\\\\)")
    for s, body in enumerate(sections, 1):
        title = re.match(r"\\section\{((?:[^{}]|\{[^{}]*\})*)\}", body).group(1)
        name = f"{s:02d}-{slugify(title)}"
        chapters.append({"n": s, "title": title, "file": name + ".md"})
        sub = eq = ex = 0
        last = ("section", str(s))
        for m in token.finditer(body):
            if m.group(1) == "section":
                last = ("section", str(s))
            elif m.group(1) == "subsection":
                sub += 1
                last = ("subsection", f"{s}.{sub}")
            elif m.group(3) == "equation":
                eq += 1
                last = ("equation", f"{s}.{eq}")
            elif m.group(3) == "align":
                for rowno, row in enumerate(aligned_rows(body[m.end():body.index("\\end{align}", m.end())])):
                    eq += 1
                    lab = re.search(r"\\label\{([^}]+)\}", row)
                    if lab:
                        labels[lab.group(1)] = {"kind": "equation", "num": f"{s}.{eq}", "file": name + ".md", "id": re.sub(r"[^A-Za-z0-9_-]", "-", lab.group(1))}
                last = ("align", "")
            elif m.group(3) == "example":
                ex += 1
                last = ("example", f"{s}.{ex}")
            elif m.group(4) and last[0] != "align":
                labels[m.group(4)] = {"kind": last[0], "num": last[1], "file": name + ".md", "id": re.sub(r"[^A-Za-z0-9_-]", "-", m.group(4))}
    for source, page, word in (("notation.tex", "../appendix-notation.md", "Appendix A"), ("glossary.tex", "../appendix-glossary.md", "Appendix B")):
        for key in re.findall(r"\\label\{([^}]+)\}", inputs((L / source).read_text(encoding="utf8"))):
            labels[key] = {"kind": "appendix", "num": word, "file": page, "id": re.sub(r"[^A-Za-z0-9_-]", "-", key)}
    return labels, chapters


def link(lab, here, text):
    f = "" if lab["file"] == here else lab["file"]
    return f"\\href{{{f}#{lab['id']}}}{{{text}}}"


def preprocess(body, chapter, labels, cite_no):
    s = chapter["n"]
    here = chapter["file"]
    t = inputs(body)
    t = re.sub(r"\\money\{([^{}]*)\}", lambda m: "\\$" + m.group(1), t)

    def ref(m):
        cmd, key = m.group(1), m.group(2)
        lab = labels.get(key)
        if lab is None:
            raise SystemExit(f"undefined reference {key}")
        if cmd == "eqref":
            return link(lab, here, f"({lab['num']})")
        if cmd in ("cref", "Cref"):
            word = {"section": "Section", "subsection": "Section", "equation": "Eq.", "example": "Example", "appendix": ""}[lab["kind"]]
            return link(lab, here, f"{word} {lab['num']}".strip())
        return link(lab, here, lab["num"])

    t = re.sub(r"\\(eqref|ref|cref|Cref)\{([^}]+)\}", ref, t)

    def cite(m):
        keys = [k.strip() for k in m.group(1).split(",")]
        for k in keys:
            if k not in cite_no:
                raise SystemExit(f"undefined citation {k}")
        return " CITEMARK" + "QQ".join(str(cite_no[k]) for k in keys) + "END"

    t = re.sub(r"\s*\\cite\{([^}]+)\}", cite, t)
    eq = [0]

    def math(m):
        env, inner = m.group(1), m.group(2)
        if env == "align":
            rows, anchors = [], ""
            for row in aligned_rows(inner):
                eq[0] += 1
                lab = re.search(r"\\label\{([^}]+)\}", row)
                if lab:
                    anchors += "EQANCHOR" + re.sub(r"[^A-Za-z0-9]", "QZ", lab.group(1)) + "END "
                rows.append(re.sub(r"\\label\{[^}]+\}", "", row).strip() + f" \\tag{{{s}.{eq[0]}}}")
            return f"\n{anchors}\n\n\\[\n\\begin{{align}}\n" + " \\\\\n".join(rows) + "\n\\end{align}\n\\]"
        eq[0] += 1
        num = f"{s}.{eq[0]}"
        lab = re.search(r"\\label\{([^}]+)\}", inner)
        anchor = ""
        if lab:
            anchor = "\nEQANCHOR" + re.sub(r"[^A-Za-z0-9]", "QZ", lab.group(1)) + "END\n\n"
        inner = re.sub(r"\\label\{[^}]+\}", "", inner).strip()
        return f"{anchor}\\[\n{inner}\n\\tag{{{num}}}\n\\]"

    t = re.sub(r"\\begin\{(equation|align)\}(.*?)\\end\{\1\}", math, t, flags=re.S)
    t = re.sub(r"\\begin\{align\*\}(.*?)\\end\{align\*\}", lambda m: "\\[\n\\begin{aligned}" + re.sub(r"\\label\{[^}]+\}", "", m.group(1)) + "\\end{aligned}\n\\]", t, flags=re.S)
    ex = [0]

    def example(m):
        ex[0] += 1
        title = m.group(1) or ""
        anchor = "EQANCHOR" + re.sub(r"[^A-Za-z0-9]", "QZ", m.group(2)) + "END\n\n" if m.group(2) else ""
        return f"\n\nEXAMPLEOPEN{ex[0]}END\n\n{anchor}\\textbf{{Example {s}.{ex[0]}{': ' + title if title else ''}}}\n\n"

    t = re.sub(r"\\begin\{example\}(?:\[((?:[^\[\]]|\[[^\]]*\])*)\])?(?:\s*\\label\{([^}]+)\})?", example, t)
    t = t.replace("\\end{example}", "\n\nEXAMPLECLOSE\n\n")
    sub = [0]

    def subsection(m):
        sub[0] += 1
        return f"\\subsection{{{s}.{sub[0]} {m.group(1)}}}"

    t = re.sub(r"\\subsection\{((?:[^{}]|\{[^{}]*\})*)\}", subsection, t)
    t = re.sub(r"\\section\{((?:[^{}]|\{[^{}]*\})*)\}", lambda m: f"\\section{{{s}. {m.group(1)}}}", t, count=1)
    t = re.sub(r"\\caption\{", "\\\\caption{Table 1. ", t) if s == 2 else t
    t = re.sub(r"\\label\{([^}]+)\}", lambda m: "\\label{" + re.sub(r"[^A-Za-z0-9_-]", "-", m.group(1)) + "}", t)
    return t


def pandoc(tex):
    r = subprocess.run(["pandoc", "-f", "latex-raw_tex", "-t", "markdown+tex_math_dollars+footnotes+header_attributes-raw_tex-smart-bracketed_spans-native_spans-simple_tables-multiline_tables-grid_tables+pipe_tables", "--wrap=none", "--markdown-headings=atx"],
                       input=(macros() + tex).encode("utf8"), capture_output=True)
    if r.returncode:
        raise SystemExit(r.stderr.decode("utf8", "replace")[:800])
    return r.stdout.decode("utf8")


def postprocess(md, keys):
    def cites(m):
        nums = m.group(1).split("QQ")
        return '<span class="citation">[' + ", ".join(f'<a href="../references.md#ref-{keys[int(n) - 1].lower().replace(":", "-")}">{n}</a>' for n in nums) + "]</span>"

    md = re.sub(r" ?CITEMARK([0-9Q]+)END", cites, md)
    md = re.sub(r"EQANCHOR(\w+?)END", lambda m: '<span id="' + m.group(1).replace("QZ", "-") + '"></span>', md)
    md = re.sub(r"EXAMPLEOPEN\d+END", '<div class="example" markdown="1">', md)
    md = md.replace("EXAMPLECLOSE", "</div>")
    md = re.sub(r"(?m)^\*\*(Example \d+\.\d+[^\n]*?)\*\*$", r'<p class="example-title"><strong>\1</strong></p>', md)

    pieces = re.split(r"(\$\$.*?\$\$)", md, flags=re.S)
    out = []
    indent = ""
    for i, p in enumerate(pieces):
        if i % 2:
            # keep the math inside a list item, whose text is indented in fours; any other leading space would break the block
            line_start = out[-1].rsplit("\n", 1)[-1] if out else ""
            marker = re.match(r" *(?:[-*+]|\d+\.) +", line_start)
            spaces = len(marker.group(0)) if marker else len(line_start) - len(line_start.lstrip(" "))
            indent = " " * (spaces - spaces % 4)
            out[-1] = out[-1].rstrip(" ")
            body = re.sub(r"\\text\{\$([^$]+)\$ ?([^{}]*)\}", r"\1\\text{ \2}", p[2:-2].strip())
            out.append("\n\n" + indent + "$$\n" + "\n".join(indent + l.strip() for l in body.splitlines()) + "\n" + indent + "$$\n\n")
        else:
            if not i:
                out.append(p)
            elif p.startswith("\n"):
                # a new block keeps its own level; text continuing the same line stays inside the list item
                body = p.lstrip("\n")
                spaces = len(body) - len(body.lstrip(" "))
                out.append(" " * (spaces - spaces % 4) + body.lstrip(" "))
            else:
                out.append(indent + p.lstrip(" "))
    md = "".join(out)
    md = re.sub(r"\\ensuremath\{([^{}]*)\}", r"\1", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = re.sub(r"(?m)[ \t]+$", "", md)
    return md.strip() + "\n"


def bibliography(keys, out):
    t = inputs((L / "bibliography.tex").read_text(encoding="utf8"))
    items = re.split(r"\\bibitem(?:\[[^\]]*\])?\{[^}]+\}", t.split("\\end{thebibliography}")[0])[1:]
    lines = ["# References and further reading { #references }", "", "Citation numbers match the PDF edition.", ""]
    for n, (k, item) in enumerate(zip(keys, items), 1):
        text = pandoc(item.strip()).strip().replace("\n", " ")
        lines += [f'<div class="reference-entry" id="ref-{k.lower().replace(":", "-")}" markdown="1">', "", f"**[{n}]** {text}", "", "</div>", ""]
    (out / "references.md").write_text("\n".join(lines), encoding="utf8", newline="\n")


def notation(out, labels):
    t = inputs((L / "notation.tex").read_text(encoding="utf8"))
    title = re.search(r"\\section\{([^}]*)\}", t).group(1)
    intro = t[t.index("\\noindent"):t.index("\\begingroup")]
    caption = re.search(r"\\caption\{([^}]*)\}", t).group(1)
    head = re.findall(r"\\textbf\{([^}]*)\}", t[t.index("\\caption"):t.index("\\endfirsthead")])
    rows = t[t.index("\\endlastfoot") + len("\\endlastfoot"):t.index("\\end{longtable}")]
    table = [f"| **{head[0]}** | **{head[1]}** |", "|:--|:----|"]
    for row in re.split(r"\\\\\s*(?:\n|$)", rows):
        if "&" in row:
            a, b = row.split("&", 1)
            cell = lambda c: pandoc(c.strip()).strip().replace("\n", " ").replace("|", "\\|")
            table.append(f"| {cell(a)} | {cell(b)} |")
    md = [f"# Appendix A. {title} {{ #sec-notation }}", "", pandoc(intro).strip(), "", f'<p class="table-caption"><strong>Table 2.</strong> {caption}</p>', ""] + table
    after = t[t.index("\\end{longtable}") + len("\\end{longtable}"):]
    after = re.sub(r"\\endgroup|\\clearpage", " ", after).strip()
    if after:
        md += ["", pandoc(after).strip()]
    def anchor(m):
        lab = labels[m.group(1)]
        return f"(chapters/{lab['file']}#{lab['id']})"

    text = re.sub(r"\(#([A-Za-z]+:[^)]+)\)", anchor, "\n".join(md))
    (out / "appendix-notation.md").write_text(text + "\n", encoding="utf8", newline="\n")


def braces(text, start):
    depth = 0
    for i in range(start, len(text)):
        depth += {"{": 1, "}": -1}.get(text[i], 0)
        if depth == 0:
            return i
    raise SystemExit("unbalanced braces in glossary.tex")


def glossary(out):
    t = inputs((L / "glossary.tex").read_text(encoding="utf8"))
    acronyms = sorted(re.findall(r"\\newacronym\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}", t), key=lambda a: a[1].lower())
    terms = []
    for m in re.finditer(r"\\newglossaryentry\{([^}]*)\}\{", t):
        end = braces(t, m.end() - 1)
        body = t[m.end():end]
        field = lambda k: (lambda x: body[x.end():braces(body, x.end() - 1)] if x else "")(re.search(k + r"\s*=\s*\{", body))
        terms.append((m.group(1), field("name"), field("description"), field("sort") or field("name")))
    terms.sort(key=lambda x: x[3].lower())
    md = ["# Appendix B. Glossary and acronyms { #sec-glossary }", "", "## Acronyms", "", '<dl class="glossary-list">']
    for key, short, long_ in acronyms:
        md += [f'<dt id="acronym-{key}">{short}</dt>', f"<dd>{long_}</dd>"]
    md += ["</dl>", "", "## Glossary of terms", "", '<dl class="glossary-list">']
    for key, name, desc, _ in terms:
        text = pandoc(desc.strip()).strip()
        md += [f'<dt id="term-{key}">{pandoc(name).strip()}</dt>', f'<dd markdown="1">{text}</dd>']
    md += ["</dl>"]
    (out / "appendix-glossary.md").write_text("\n".join(md) + "\n", encoding="utf8", newline="\n")


def main(out):
    head, sections = split_sections(inputs((L / "content.tex").read_text(encoding="utf8")))
    keys = bib_keys()
    cite_no = {k: i for i, k in enumerate(keys, 1)}
    labels, chapters = number(sections)
    (out / "chapters").mkdir(parents=True, exist_ok=True)
    for chapter, body in zip(chapters, sections):
        body = re.split(r"(?m)^\\(?:clearpage|appendix|input\{)", body)[0]
        md = postprocess(pandoc(preprocess(body, chapter, labels, cite_no)), keys)
        (out / "chapters" / chapter["file"]).write_text(md, encoding="utf8", newline="\n")
    bibliography(keys, out)
    notation(out, labels)
    glossary(out)
    print(f"wrote {len(chapters)} chapters and {len(keys)} references to {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "docs"))
    main(pathlib.Path(ap.parse_args().out))
