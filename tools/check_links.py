"""Check every link, anchor, equation reference and table in the built site. Exit code 1 if any internal one is broken.

    python tools/check_links.py [--external]     needs a built site/ folder

--external also tests outside addresses, and only reports them, because other sites go down or refuse automated requests.
"""
import argparse
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
ALLOWED_ABSOLUTE = ("/index.html", "/research.html", "/teaching.html", "/projects.html", "/writing.html", "/cv.html")


def pages(site):
    return {p: p.read_text(encoding="utf8") for p in site.rglob("*.html")}


def internal_problems(site):
    html = pages(site)
    ids = {p: set(re.findall(r'\bid="([^"]+)"', t)) for p, t in html.items()}
    bad, checked = [], 0
    for p, t in html.items():
        if p.name == "404.html":  # uses addresses from the site root, so that it works at any depth
            continue
        for href in re.findall(r'\bhref="([^"]+)"', t):
            if re.match(r"[a-z]+:|//", href) or href in ALLOWED_ABSOLUTE:
                continue
            checked += 1
            path, _, frag = urllib.parse.unquote(href).partition("#")
            target = p if not path else (p.parent / path).resolve()
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                bad.append(f"{p.relative_to(site)}: missing page {href}")
            elif frag and target.suffix == ".html" and frag not in ids.get(target, set()):
                bad.append(f"{p.relative_to(site)}: missing anchor {href}")
    return bad, checked


def source_problems():
    """Every LaTeX reference has a label, and every numbered table and figure is mentioned or captioned."""
    t = "\n".join((ROOT / "latex" / f).read_text(encoding="utf8") for f in ("content.tex", "notation.tex", "glossary.tex"))
    t = re.sub(r"(?m)(?<!\\)%.*$", "", t)
    labels = set(re.findall(r"\\label\{([^}]+)\}", t))
    refs = set(re.findall(r"\\(?:ref|eqref|cref|Cref|autoref)\{([^}]+)\}", t))
    bad = [f"reference to undefined label {r}" for r in sorted(refs - labels)]
    for label in sorted(labels - refs):
        if label.startswith(("tab:", "fig:")):
            print("note: label never referred to:", label)
    return bad


def external(site):
    urls = sorted({u for t in pages(site).values() for u in re.findall(r'href="(https?://[^"#]+)', t) if "ahmadammar.github.io" not in u})
    failed = []
    for u in urls:
        try:
            req = urllib.request.Request(u, method="GET", headers={"User-Agent": "Mozilla/5.0 link check"})
            urllib.request.urlopen(req, timeout=20).close()
        except urllib.error.HTTPError as e:
            if e.code in (404, 410):
                failed.append(f"{e.code} {u}")
        except Exception as e:
            failed.append(f"{type(e).__name__} {u}")
    return urls, failed


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default=str(ROOT / "site"))
    ap.add_argument("--external", action="store_true")
    a = ap.parse_args()
    site = pathlib.Path(a.site)
    bad, n = internal_problems(site)
    bad += source_problems()
    print(f"{n} internal links checked")
    print("\n".join("FAIL " + b for b in bad[:60]) or "OK: internal links, anchors and LaTeX references")
    if a.external:
        urls, failed = external(site)
        print(f"{len(urls)} external addresses tested, {len(failed)} not reachable (report only):")
        print("\n".join("  " + f for f in failed))
    sys.exit(bool(bad))
