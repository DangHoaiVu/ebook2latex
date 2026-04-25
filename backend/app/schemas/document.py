from pydantic import BaseModel


class FormulaResult(BaseModel):
    id: str
    page_number: int | None = None
    image_path: str | None = None
    latex: str | None = None
    source_text: str | None = None


class PDFUploadResponse(BaseModel):
    message: str
    document_id: str
    file_name: str
    stored_path: str
    total_pages: int
    formulas: list[FormulaResult]


class SaveFormulaRequest(BaseModel):
    document_id: str
    formula_entry_id: str | None = None
    latex_result: str


class SaveFormulaResponse(BaseModel):
    message: str
    formula_entry_id: str
    latex_result: str
