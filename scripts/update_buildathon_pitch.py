"""Refresh the editable roadmap copy on the existing seven-slide pitch PDF."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
import shutil

from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "LabelFitIndiaBuildathon2026.pdf"
TEMP = ROOT / "tmp" / "pdfs" / "LABEL_CHECK_Startup_Buildathon_2026_updated.pdf"
OUTPUTS = [
    ROOT / "output" / "pdf" / "LABEL_CHECK_Startup_Buildathon_2026.pdf",
]

FONT = Path(r"C:\Windows\Fonts\arial.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")
pdfmetrics.registerFont(TTFont("PitchArial", str(FONT)))
pdfmetrics.registerFont(TTFont("PitchArialBold", str(FONT_BOLD)))

INK = HexColor("#53626E")
BLUE = HexColor("#4285F4")


def draw_row(pdf: canvas.Canvas, label: str, text: str, y: float, page_width: float) -> None:
    pdf.setFillColor(BLUE)
    pdf.setFont("PitchArialBold", 8.6)
    pdf.drawString(40, y, label)
    pdf.setFillColor(INK)
    pdf.setFont("PitchArial", 8.6)
    lines = simpleSplit(text, "PitchArial", 8.6, page_width - 175)
    for offset, line in enumerate(lines):
        pdf.drawString(137, y - offset * 10.4, line)


def make_slide_overlay(width: float, height: float) -> PdfReader:
    packet = BytesIO()
    pdf = canvas.Canvas(packet, pagesize=(width, height), pageCompression=1)

    # Slide 3 has a white footer area; cover only its old two footer rows.
    pdf.setFillColor(white)
    pdf.setStrokeColor(white)
    pdf.rect(35, 39, width - 70, 80, fill=1, stroke=0)

    draw_row(
        pdf,
        "Team & stage:",
        "Two-member LABEL CHECK; working local prototype; live Gemini scans demonstrated.",
        107,
        width,
    )
    draw_row(
        pdf,
        "Pilot evidence:",
        "10 mixed-category packages / 60 fields; only one complementary-food package.",
        90,
        width,
    )
    draw_row(
        pdf,
        "Scope:",
        "Transcription only; no health, safety, allergy or feeding decisions.",
        73,
        width,
    )
    draw_row(
        pdf,
        "Next:",
        "Evaluate 6+ month labels, then caregiver usability and B2B export interest.",
        56,
        width,
    )

    pdf.save()
    packet.seek(0)
    return PdfReader(packet)


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Pitch PDF not found: {SOURCE}")

    reader = PdfReader(str(SOURCE))
    if len(reader.pages) != 7:
        raise ValueError(f"Expected a seven-slide PDF, found {len(reader.pages)} pages")

    page = reader.pages[2]
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)
    page.merge_page(make_slide_overlay(width, height).pages[0])

    writer = PdfWriter()
    for source_page in reader.pages:
        writer.add_page(source_page)
    writer.add_metadata(
        {
            "/Title": "LABEL CHECK — LabelFit India Buildathon 2026",
            "/Subject": "Evidence-aligned pitch for an early label-transcription prototype",
        }
    )

    TEMP.parent.mkdir(parents=True, exist_ok=True)
    with TEMP.open("wb") as stream:
        writer.write(stream)

    for output in OUTPUTS:
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(TEMP, output)
        print(f"Updated: {output}")


if __name__ == "__main__":
    main()
