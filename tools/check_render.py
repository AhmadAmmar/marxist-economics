"""Open every built page in a real browser, in light and dark, on desktop and phone, and test what readers actually see.

    python tools/check_render.py [--site site] [--shots folder]      exit code 1 on any failure

Tests: no raw LaTeX or Markdown in the text; MathJax errors, undefined commands shown in red, and ordinary words swallowed into maths by paired dollar signs; clipped equations; each page's tables and displayed equations match the LaTeX source;
readable contrast for links and buttons (WCAG AA, 4.5:1); no sideways page overflow; no table clipped on desktop; a filled table of contents;
an opaque sidebar title; one main heading; images with alt text. Needs playwright and its Chromium, and network access for MathJax.
"""
import argparse
import functools
import http.server
import pathlib
import re
import shutil
import socket
import sys
import tempfile
import threading

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
BASE = "marxist-economics"
RAW = [(":::", r":::"), ("Markdown table", r"\|\s*:?-{3,}"), ("display maths", r"\$\$"), ("LaTeX environment", r"\\(begin|end)\{"), ("LaTeX command", r"\\(frac|dfrac|text|emph|textbf|cite|ref|eqref|label|caption|ensuremath)\b"),
       ("unresolved label", r"\[(eq|sec|subsec|tab|fig|ex):[^\]]*\]"), ("build marker", r"CITEMARK|EQANCHOR|EXAMPLEOPEN|EXAMPLECLOSE|QZ[a-z]"), ("TeX quotes", r"``|''")]
VIEWS = [("light", "desktop", 1440, 900), ("dark", "desktop", 1440, 900), ("light", "phone", 390, 800), ("dark", "phone", 390, 800)]

MEASURE = r"""() => {
  const lum = c => { const f = c.map(v => { v /= 255; return v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4) }); return .2126 * f[0] + .7152 * f[1] + .0722 * f[2] };
  const rgb = s => { const m = s.match(/[\d.]+/g).map(Number); return { c: m.slice(0, 3), a: m.length > 3 ? m[3] : 1 } };
  const bg = el => { for (let e = el; e; e = e.parentElement) { const b = rgb(getComputedStyle(e).backgroundColor); if (b.a > .5) return b.c } return [255, 255, 255] };
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + .05) / (Math.min(x, y) + .05) };
  const visible = e => { const r = e.getBoundingClientRect(), s = getComputedStyle(e); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' };
  const content = document.querySelector('.md-content');
  const low = [];
  for (const a of document.querySelectorAll('.md-content a, .md-nav a, .aa-header a, .aa-footer a, .md-button, .aa-crumb a')) {
    if (!visible(a) || a.classList.contains('headerlink')) continue;
    const r = ratio(rgb(getComputedStyle(a).color).c, bg(a));
    if (r < 4.5) low.push((a.innerText || a.href).trim().slice(0, 30) + ' ' + r.toFixed(1));
  }
  const clipped = [];
  for (const t of content.querySelectorAll('table')) {
    const box = t.closest('.md-typeset__table, .md-typeset__scrollwrap') || t.parentElement;
    if (t.getBoundingClientRect().width > content.getBoundingClientRect().width + 2 || box.scrollWidth > box.clientWidth + 2) clipped.push(t.innerText.slice(0, 30));
  }
  const toc = document.querySelector('.md-sidebar--secondary [data-md-component=toc]');
  const titles = [...document.querySelectorAll('.md-sidebar--primary .md-nav__title')].filter(visible);
  return {
    text: content.innerText,
    math: document.querySelectorAll('.md-content mjx-container').length,
    display: document.querySelectorAll('.md-content mjx-container[display=true]').length,
    errors: document.querySelectorAll('mjx-merror,[data-mjx-error]').length,
    badMath: (() => {
      const out = [];
      const items = window.MathJax && MathJax.startup && MathJax.startup.document ? [...MathJax.startup.document.math] : [];
      for (const item of items) {
        const tex = item.math;
        const html = item.typesetRoot ? item.typesetRoot.innerHTML : '';
        const stripped = tex.replace(/\\(begin|end)\s*\{[^{}]*\}/g, ' ').replace(/\\(text|mathrm|mathbf|operatorname|textbf|textit|tag)\s*\{[^{}]*\}/g, ' ').replace(/\\[a-zA-Z]+/g, ' ');
        if (/color:\s*red|mathcolor="red"|mjx-merror/.test(html)) out.push('undefined command: ' + tex.trim().replace(/\\s+/g, ' ').slice(0, 80));
        else if (/[A-Za-z]{5,}/.test(stripped) || /\b(and|the|for|but|has|of|to)\s+[A-Za-z]/.test(stripped)) out.push('words read as maths: ' + tex.trim().replace(/\\s+/g, ' ').slice(0, 80));
      }
      return out;
    })(),
    wideMath: [...content.querySelectorAll('mjx-container[display=true]')].filter(m => m.scrollWidth > m.clientWidth + 2).map(m => m.innerText.replace(/\s+/g, '').slice(0, 30)),
    tables: content.querySelectorAll('table').length,
    emptyHeads: [...content.querySelectorAll('table thead')].filter(h => !h.innerText.trim()).length,
    low, clipped,
    wide: document.documentElement.scrollWidth > innerWidth + 1,
    toc: toc ? toc.querySelectorAll('a').length : 0,
    h1: content.querySelectorAll('h1').length,
    noalt: [...content.querySelectorAll('img')].filter(i => !i.alt).length,
    seeThrough: titles.filter(t => rgb(getComputedStyle(t).backgroundColor).a < .5).length,
  };
}"""


def expected():
    """Tables and displayed equations in each chapter, counted from the LaTeX."""
    import tex_to_web as W
    _, sections = W.split_sections(W.inputs((ROOT / "latex/content.tex").read_text(encoding="utf8")))
    _, chapters = W.number(sections)
    out = {}
    for ch, body in zip(chapters, sections):
        body = re.split(r"(?m)^\\(?:clearpage|appendix|input\{)", body)[0]
        converted = len(W.ARRAY_TABLE.findall(body))
        tables = len(re.findall(r"\\begin\{(?:tabular|tabularx|longtable)\}", body)) + converted
        display = len(re.findall(r"(?<!\\)\\\[|\\begin\{(?:equation|align)\*?\}", body)) - converted
        out["chapters/" + ch["file"][:-3]] = (tables, display)
    return out


def serve(site):
    tmp = tempfile.TemporaryDirectory()
    shutil.copytree(site, pathlib.Path(tmp.name) / BASE)
    handler = functools.partial(type("Quiet", (http.server.SimpleHTTPRequestHandler,), {"log_message": lambda *a: None}), directory=tmp.name)
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return tmp, server, port


def problems_of(m, want, view):
    bad = []
    for name, pattern in RAW:
        hit = re.search(pattern, m["text"])
        if hit:
            bad.append(f"raw {name}: ...{m['text'][max(0, hit.start() - 25):hit.end() + 25]!r}")
    if m["errors"]:
        bad.append(f"{m['errors']} MathJax errors")
    bad += [f"bad maths: {x}" for x in m["badMath"][:12]]
    if view[1] == "desktop":
        bad += [f"equation clipped: {x}" for x in m["wideMath"][:6]]
    if m["emptyHeads"]:
        bad.append(f"{m['emptyHeads']} tables with an empty header row")
    if m["wide"]:
        bad.append("page scrolls sideways")
    bad += [f"low contrast: {x}" for x in m["low"][:8]]
    if view[1] == "desktop":
        bad += [f"table clipped: {x!r}" for x in m["clipped"][:4]]
        if m["toc"] == 0:
            bad.append("empty table of contents")
        if m["seeThrough"]:
            bad.append("sidebar title is see-through")
    if m["h1"] != 1:
        bad.append(f"{m['h1']} main headings")
    if m["noalt"]:
        bad.append(f"{m['noalt']} images without alt text")
    if want:
        if m["tables"] != want[0]:
            bad.append(f"{m['tables']} tables, the LaTeX has {want[0]}")
        if m["display"] != want[1]:
            bad.append(f"{m['display']} displayed equations, the LaTeX has {want[1]}")
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default=str(ROOT / "site"))
    ap.add_argument("--shots")
    a = ap.parse_args()
    site = pathlib.Path(a.site)
    pages = sorted(p.parent.relative_to(site).as_posix() for p in site.rglob("index.html"))
    want = expected()
    tmp, server, port = serve(site)
    failed = 0
    if a.shots:
        pathlib.Path(a.shots).mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for view in VIEWS:
            ctx = browser.new_context(viewport={"width": view[2], "height": view[3]}, color_scheme=view[0])
            page = ctx.new_page()
            for name in pages:
                url = f"http://127.0.0.1:{port}/{BASE}/" + ("" if name == "." else name + "/")
                page.goto(url, wait_until="networkidle")
                page.wait_for_function("() => !window.MathJax || !MathJax.startup || !MathJax.startup.promise || true")
                page.evaluate("() => window.MathJax && MathJax.startup && MathJax.startup.promise")
                page.wait_for_timeout(100)
                m = page.evaluate(MEASURE)
                bad = problems_of(m, want.get(name), view)
                for b in bad:
                    print(f"FAIL {view[0]} {view[1]} {name}: {b}"[:220])
                failed += len(bad)
                if a.shots:
                    page.screenshot(path=str(pathlib.Path(a.shots) / f"{name.replace('/', '_').replace('.', 'home')}_{view[0]}_{view[1]}.png"))
            ctx.close()
        browser.close()
    server.shutdown()
    tmp.cleanup()
    print(f"{len(pages)} pages in {len(VIEWS)} views: {failed} problems")
    sys.exit(bool(failed))


if __name__ == "__main__":
    main()
