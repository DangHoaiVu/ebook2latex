from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import UPLOAD_DIR
from app.core.database import get_db
from app.models import Document, FormulaEntry
from app.schemas.document import (
    FormulaResult,
    PDFUploadResponse,
    SaveFormulaRequest,
    SaveFormulaResponse,
)
from app.services.ocr_service import image_to_latex
from app.services.pdf_service import extract_formula_images, inspect_pdf

router = APIRouter()


@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Kiem tra server va database con hoat dong."""
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "message": "Server hoat dong binh thuong",
            "database": "connected",
        }
    except SQLAlchemyError as exc:
        return {
            "status": "degraded",
            "message": "Server hoat dong nhung ket noi database that bai",
            "database": "disconnected",
            "detail": str(exc),
        }


@router.post("/upload-pdf/", response_model=PDFUploadResponse)
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Nhan file PDF, cat cong thuc, OCR sang LaTeX va luu ket qua vao DB."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="Ten file khong hop le")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Chi chap nhan file PDF")

    document_id = str(uuid4())
    original_name = Path(file.filename).name
    file_name = f"{document_id}_{original_name}"
    saved_path = UPLOAD_DIR / file_name

    content = await file.read()
    saved_path.write_bytes(content)

    page_info = inspect_pdf(saved_path)
    extracted_images = extract_formula_images(saved_path)

    document = Document(
        id=document_id,
        file_name=original_name,
        stored_path=str(saved_path),
        status="uploaded",
        page_count=page_info["total_pages"],
    )
    db.add(document)

    formula_results: list[FormulaResult] = []
    for item in extracted_images:
        formula_id = str(uuid4())
        latex_result = image_to_latex(item["image_path"], fallback_text=item.get("source_text"))

        formula_entry = FormulaEntry(
            id=formula_id,
            document_id=document_id,
            page_number=item["page_number"],
            cropped_image_path=item["image_path"],
            latex_result=latex_result,
            source_text=item.get("source_text"),
        )
        db.add(formula_entry)
        formula_results.append(
            FormulaResult(
                id=formula_id,
                page_number=item["page_number"],
                image_path=item["image_path"],
                latex=latex_result,
                source_text=item.get("source_text"),
            )
        )

    db.commit()

    return PDFUploadResponse(
        message="Tai file PDF va trich xuat cong thuc thanh cong",
        document_id=document_id,
        file_name=original_name,
        stored_path=str(saved_path),
        total_pages=page_info["total_pages"],
        formulas=formula_results,
    )


@router.post("/save-formula/", response_model=SaveFormulaResponse)
def save_formula(payload: SaveFormulaRequest, db: Session = Depends(get_db)):
    """Luu chuoi LaTeX cuoi cung vao PostgreSQL."""
    document = db.get(Document, payload.document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Khong tim thay document")

    formula_entry = None
    if payload.formula_entry_id:
        formula_entry = db.get(FormulaEntry, payload.formula_entry_id)

    if formula_entry is None:
        formula_entry = FormulaEntry(
            id=str(uuid4()),
            document_id=payload.document_id,
            latex_result=payload.latex_result,
        )
        db.add(formula_entry)
    else:
        formula_entry.latex_result = payload.latex_result

    document.status = "saved"
    db.commit()
    db.refresh(formula_entry)

    return SaveFormulaResponse(
        message="Luu cong thuc thanh cong",
        formula_entry_id=formula_entry.id,
        latex_result=formula_entry.latex_result or "",
    )
