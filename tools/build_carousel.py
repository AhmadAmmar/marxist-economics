"""Build the Sialkot deck and Instagram images from the compiled slides, keeping every earlier version.

    python tools/build_carousel.py

Writes docs/downloads/sialkot_slides.pptx with speaker notes from examples/sialkot/notes.json, and square 1440-pixel PNG images in
examples/sialkot/instagram/<date>_<first 8 characters of the PDF's hash>/. A new folder appears only when the slides' content changes.
"""
import datetime
import hashlib
import json
import pathlib
import subprocess

from research_helpers.carousel import images_to_pptx, pdf_to_images

ROOT = pathlib.Path(__file__).resolve().parents[1]
EX = ROOT / "examples/sialkot"
PIXELS = 1440


def text_fingerprint(pdf):
    """Hash the slides' text, because PDF bytes change with each compile even when the content does not."""
    text = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True).stdout
    return hashlib.sha256(text).hexdigest()[:8]


def overflowing(images):
    """Slides with anything drawn beyond the white frame, whose right and bottom edges sit near 1412 and 1398 of 1440 pixels."""
    from PIL import Image
    bad = []
    for path in images:
        im = Image.open(path).convert("L")
        w, h = im.size
        beyond = [(round(1420 * w / 1440), 0, w, h), (0, round(1405 * h / 1440), w, h)]
        if any(im.crop(box).getextrema()[1] > 60 for box in beyond):
            bad.append(path.name)
    return bad


def build():
    pdf = EX / "slides.pdf"
    tag = text_fingerprint(pdf)
    versions = EX / "instagram"
    existing = list(versions.glob(f"*_{tag}"))
    folder = existing[0] if existing else versions / f"{datetime.date.today()}_{tag}"
    images = sorted(folder.glob("slide-*.png")) or pdf_to_images(pdf, folder, pixels=PIXELS)
    bad = overflowing(images)
    if bad:
        raise SystemExit(f"text runs outside the frame on: {bad}")
    notes = json.loads((EX / "notes.json").read_text(encoding="utf8"))
    downloads = ROOT / "docs/downloads"
    downloads.mkdir(exist_ok=True)
    images_to_pptx(images, downloads / "sialkot_slides.pptx", notes)
    print(f"{len(images)} images in {folder.relative_to(ROOT)}; deck with notes in docs/downloads")


if __name__ == "__main__":
    build()
