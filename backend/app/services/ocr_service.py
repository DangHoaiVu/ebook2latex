from pathlib import Path

from PIL import Image

OCR_MODEL = None
OCR_IMPORT_ERROR = None

try:
    from pix2tex.cli import LatexOCR
except Exception as exc:  # pragma: no cover - phu thuoc moi truong local
    LatexOCR = None
    OCR_IMPORT_ERROR = exc


def get_ocr_model():
    """Load model OCR mot lan duy nhat de tiet kiem RAM."""
    global OCR_MODEL

    if OCR_MODEL is None and LatexOCR is not None:
        OCR_MODEL = LatexOCR()

    return OCR_MODEL


def image_to_latex(image_path: str | Path, fallback_text: str | None = None) -> str:
    """OCR anh cong thuc sang LaTeX, co fallback neu model chua san sang."""
    image_path = Path(image_path)

    try:
        model = get_ocr_model()
        if model is not None:
            with Image.open(image_path) as image:
                return model(image)
    except Exception:
        pass

    if fallback_text:
        return fallback_text.strip()

    if OCR_IMPORT_ERROR is not None:
        return r"\text{OCR model chua san sang}"

    return r"\text{Khong nhan dien duoc cong thuc}"
