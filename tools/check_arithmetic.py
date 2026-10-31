"""Scan the pamphlet's displayed equations for numeric chains such as 50 + 100 = 150 and recalculate each step.

    python tools/check_arithmetic.py        prints steps that do not hold

Only steps made wholly of numbers are tested. Approximate steps get a tolerance of 1% or the last digit shown, and results are for a person
to read, because a rounded or illustrative figure can be correct in context. It cannot judge an argument or a symbolic derivation.
"""
import math
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))


def macros():
    p = ROOT / "latex/generated/sialkot_numbers.tex"
    return dict(re.findall(r"\\newcommand\{\\([A-Za-z]+)\}\{([^}]*(?:\{,\}[^}]*)*)\}", p.read_text(encoding="utf8")))


def to_python(tex, table):
    s = tex
    for k, v in table.items():
        s = s.replace("\\" + k + "{}", v)
    s = re.sub(r"\\text\{[^{}]*\}|\\mathrm\{[^{}]*\}|\\qquad|\\quad|\\,|\\;|\\!|\\ |\\\$|\\left|\\right|~", " ", s)
    s = s.replace("{,}", "").replace("\\times", "*").replace("\\cdot", "*")
    s = s.replace("\\%", "/100")
    for _ in range(4):
        s = re.sub(r"\\d?frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", s)
    s = re.sub(r"(?<=\d)\s+(?=\d)", " ", s)
    if re.search(r"[A-Za-z\\{}_^]", s):
        return None
    s = s.strip(" .,;:&")
    return s if re.search(r"\d", s) else None


def steps(tex, table):
    tex = re.sub(r"\\tag\{[^}]*\}|\\label\{[^}]*\}|\\begin\{[^}]*\}|\\end\{[^}]*\}", " ", tex)
    for line in re.split(r"\\\\|,\\qquad|\\qquad", tex):
        parts = re.split(r"(=|\\approx)", line)
        vals = []
        for i in range(0, len(parts), 2):
            vals.append((to_python(parts[i], table), parts[i - 1] if i else ""))
        for (a, _), (b, op) in zip(vals, vals[1:]):
            if a and b:
                yield a.strip(), op, b.strip()


def main():
    table = macros()
    t = (ROOT / "latex/content.tex").read_text(encoding="utf8")
    blocks = re.findall(r"\\\[(.*?)\\\]|\\begin\{(?:equation|align)\*?\}(.*?)\\end\{(?:equation|align)\*?\}", t, re.S)
    tested, odd = 0, []
    for a, b in blocks:
        body = (a or b).replace("\n", " ")
        for left, op, right in steps(body, table):
            try:
                x, y = eval(left, {"__builtins__": {}}), eval(right, {"__builtins__": {}})
            except Exception:
                continue
            tested += 1
            tol = 1e-9 if op == "=" else max(0.01 * abs(y), 0.51)
            if op == "=":
                digits = right.split(".")[-1] if re.fullmatch(r"[\d.]+", right) and "." in right else ""
                tol = 0.51 * 10 ** (-len(digits)) if re.fullmatch(r"[\d.]+", right) else 1e-6
            if not math.isclose(x, y, abs_tol=tol):
                odd.append(f"{left} {op} {right}   (left is {x:.4f})")
    print(f"{tested} numeric steps tested, {len(odd)} to read:")
    print("\n".join("  " + o for o in odd))


if __name__ == "__main__":
    main()
