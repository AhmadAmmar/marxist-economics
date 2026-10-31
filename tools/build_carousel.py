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
    """Slides with anything drawn outside the white frame, which is 64 pixels in from each edge at 1440 pixels."""
    from PIL import Image
    bad = []
    for path in images:
        im = Image.open(path).convert("L")
        w, h = im.size
        margin = round(50 * w / 1440)
        outer = [(0, 0, margin, h), (w - margin - 8, 0, w, h), (0, 0, w, margin), (0, h - margin - 8, w, h)]
        if any(im.crop(box).getextrema()[1] > 60 for box in outer[1:2] + outer[3:]):
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
