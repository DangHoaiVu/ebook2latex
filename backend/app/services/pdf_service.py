from pathlib import Path
from uuid import uuid4

import fitz
from PIL import Image

from app.core.config import FORMULA_IMAGE_DIR


def inspect_pdf(pdf_path: str | Path) -> dict:
    """Doc file PDF va tra ve thong tin tong quan."""
    pdf_file = Path(pdf_path)
    with fitz.open(pdf_file) as document:
        total_pages = document.page_count

    return {
        "file_path": str(pdf_file),
        "total_pages": total_pages,
    }


def extract_formula_images(pdf_path: str | Path) -> list[dict]:
    """Cat cac vung nghi la cong thuc toan hoc tu PDF va luu anh tam."""
    pdf_file = Path(pdf_path)
    results: list[dict] = []

    with fitz.open(pdf_file) as document:
        for page_index, page in enumerate(document, start=1):
            blocks = page.get_text("dict").get("blocks", [])
            formula_blocks: list[dict] = []

            for block in blocks:
                lines = block.get("lines", [])
                text_parts: list[str] = []
                for line in lines:
                    for span in line.get("spans", []):
                        text_parts.append(span.get("text", ""))

                block_text = " ".join(text_parts).strip()
                if not block_text:
                    continue

                if _looks_like_formula(block_text):
                    formula_blocks.append(
                        {
                            "bbox": fitz.Rect(block["bbox"]),
                            "text": block_text,
                            "page_number": page_index,
                        }
                    )

            if not formula_blocks:
                rect = page.rect
                fallback_rect = fitz.Rect(
                    rect.x0 + rect.width * 0.15,
                    rect.y0 + rect.height * 0.25,
                    rect.x1 - rect.width * 0.15,
                    rect.y1 - rect.height * 0.25,
                )
                formula_blocks.append(
                    {
                        "bbox": fallback_rect,
                        "text": "",
                        "page_number": page_index,
                    }
                )

            for block in formula_blocks:
                image_path = _save_clip_image(page, block["bbox"])
                results.append(
                    {
                        "page_number": block["page_number"],
                        "image_path": str(image_path),
                        "source_text": block["text"],
                    }
                )

    return results


def _save_clip_image(page: fitz.Page, clip_rect: fitz.Rect) -> Path:
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), clip=clip_rect, alpha=False)
    image_name = f"{uuid4()}.png"
    image_path = FORMULA_IMAGE_DIR / image_name
    pix.save(image_path)

    with Image.open(image_path) as image:
        image.convert("RGB").save(image_path)

    return image_path


def _looks_like_formula(text: str) -> bool:
    formula_markers = ["=", "+", "-", "\\", "^", "_", "(", ")", "[", "]", "{", "}", "/"]
    contains_math_symbol = any(marker in text for marker in formula_markers)
    digits_ratio = sum(char.isdigit() for char in text) / max(len(text), 1)

    return contains_math_symbol or digits_ratio > 0.2
