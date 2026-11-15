"""Refresh the editable roadmap copy on the existing seven-slide pitch PDF."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
import shutil
from typing import TYPE_CHECKING, Any

class _Stub:
    """Type-safe fallback stub for optional PDF compilation dependencies."""
    def __getattr__(self, name: str) -> Any:
        return _Stub()

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return _Stub()


if TYPE_CHECKING:
    from pypdf import PdfReader, PdfWriter  # type: ignore
    from reportlab.lib.colors import HexColor, white  # type: ignore
    from reportlab.pdfbase import pdfmetrics  # type: ignore
    from reportlab.pdfbase.ttfonts import TTFont  # type: ignore
    from reportlab.pdfgen import canvas  # type: ignore
    from reportlab.lib.utils import simpleSplit  # type: ignore
    HAS_PDF_DEPS = True
else:
    try:
        from pypdf import PdfReader, PdfWriter
        from reportlab.lib.colors import HexColor, white
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.pdfgen import canvas
        from reportlab.lib.utils import simpleSplit
        HAS_PDF_DEPS = True
    except (ImportError, Exception):
        HAS_PDF_DEPS = False
        PdfReader = PdfWriter = _Stub()
        HexColor = white = pdfmetrics = TTFont = canvas = simpleSplit = _Stub()


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "LabelFitIndiaBuildathon2026.pdf"
TEMP = ROOT / "tmp" / "pdfs" / "LABEL_CHECK_Startup_Buildathon_2026_updated.pdf"
OUTPUTS = [
    ROOT / "output" / "pdf" / "LABEL_CHECK_Startup_Buildathon_2026.pdf",
]

FONT = Path(r"C:\Windows\Fonts\arial.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")

if not TYPE_CHECKING and HAS_PDF_DEPS:
    try:
        pdfmetrics.registerFont(TTFont("PitchArial", str(FONT)))
        pdfmetrics.registerFont(TTFont("PitchArialBold", str(FONT_BOLD)))
        INK = HexColor("#53626E")
        BLUE = HexColor("#4285F4")
    except Exception:
        INK = "#53626E"
        BLUE = "#4285F4"
else:
    INK = "#53626E"
    BLUE = "#4285F4"


def draw_row(pdf: Any, label: str, text: str, y: float, page_width: float) -> None:
    pdf.setFillColor(BLUE)
    pdf.setFont("PitchArialBold", 8.6)
    pdf.drawString(40, y, label)
    pdf.setFillColor(INK)
    pdf.setFont("PitchArial", 8.6)
    lines = simpleSplit(text, "PitchArial", 8.6, page_width - 175)
    for offset, line in enumerate(lines):
        pdf.drawString(137, y - offset * 10.4, line)


def make_slide_overlay(width: float, height: float) -> Any:
    packet = BytesIO()
    pdf = canvas.Canvas(packet, pagesize=(width, height), pageCompression=1)

    # Slide 3 has a white footer area; cover only its old evidence and roadmap rows.
    pdf.setFillColor(white)
    pdf.setStrokeColor(white)
    pdf.rect(35, 39, width - 70, 80, fill=1, stroke=0)

    draw_row(
        pdf,
        "Team & stage:",
        "Two-member LABEL CHECK; working local prototype; live Gemini scans demonstrated.",
        109,
        width,
    )
    draw_row(
        pdf,
        "Pilot evidence:",
        "10 target products have founder-entered text; Gemini comparison covers 6 fields across 2 SKUs.",
        94,
        width,
    )
    draw_row(
        pdf,
        "Usability:",
        "20 illustrative protocol rows only; no live caregiver sessions are documented.",
        79,
        width,
    )
    draw_row(
        pdf,
        "Scope:",
        "Transcription only; no health, safety, allergy or feeding decisions.",
        64,
        width,
    )
    draw_row(
        pdf,
        "Next:",
        "Pair scans with references; then run a consented caregiver study and expand toward 50 SKUs.",
        49,
        width,
    )

    pdf.save()
    packet.seek(0)
    return PdfReader(packet)


def make_ai_tools_overlay(width: float, height: float) -> Any:
    packet = BytesIO()
    pdf = canvas.Canvas(packet, pagesize=(width, height), pageCompression=1)
    pdf.setFillColor(white)
    pdf.setStrokeColor(white)
    pdf.rect(35, 62, width - 70, 196, fill=1, stroke=0)

    rows = [
        ("AI API:", "The local prototype sends a confirmed package photo to Gemini for candidate text.", 249),
        ("Model:", "Gemini 3.8 Flash is the server default; the model ID can be configured.", 218),
        ("AI Studio:", "Planned for prompt and schema iteration; not used in the live deployment.", 187),
        ("Deployment:", "GitHub Actions deploys this website to Cloud Run; Gemini analysis is disabled there.", 156),
        ("Next:", "Add gated analysis only after access, quotas, billing, and privacy controls are reviewed.", 125),
    ]
    for label, text, y in rows:
        draw_row(pdf, label, text, y, width)

    pdf.save()
    packet.seek(0)
    return PdfReader(packet)


def make_ai_model_overlay(width: float, height: float) -> Any:
    packet = BytesIO()
    pdf = canvas.Canvas(packet, pagesize=(width, height), pageCompression=1)
    pdf.setFillColor(white)
    pdf.setStrokeColor(white)
    pdf.rect(35, 61, width - 70, 209, fill=1, stroke=0)

    rows = [
        ("Model role:", "Gemini 3.8 Flash (default) returns six candidate fields as structured output.", 246),
        ("Server checks:", "Schema and evidence checks can downgrade unsupported candidates; status is uncalibrated.", 216),
        ("Expected screen:", "Each field shows candidate text, a photo snippet, and Readable / Check text / Not visible.", 186),
        ("User review:", "The caregiver compares the candidate wording with the package; no product verdict is given.", 156),
        ("Live status:", "Cloud Run page is live; Gemini analysis stays disabled there until controls are ready.", 126),
        ("Next target:", "Pair scans across 10 prepared references, expand toward 50 SKUs, then test with consented adults.", 96),
    ]
    for label, text, y in rows:
        draw_row(pdf, label, text, y, width)

    pdf.save()
    packet.seek(0)
    return PdfReader(packet)


def main() -> None:
    if not HAS_PDF_DEPS or isinstance(PdfReader, _Stub) or isinstance(PdfWriter, _Stub):
        print("Notice: 'pypdf' and 'reportlab' are required to compile pitch deck overlays.")
        print("Install optional PDF compilation dependencies with: pip install pypdf reportlab")
        return

    if not SOURCE.exists():
        raise FileNotFoundError(f"Pitch PDF not found: {SOURCE}")

    reader = PdfReader(str(SOURCE))
    if len(reader.pages) != 7:
        raise ValueError(f"Expected a seven-slide PDF, found {len(reader.pages)} pages")

    for page_index, overlay_factory in (
        (2, make_slide_overlay),
        (4, make_ai_tools_overlay),
        (5, make_ai_model_overlay),
    ):
        page = reader.pages[page_index]
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        page.merge_page(overlay_factory(width, height).pages[0])

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
