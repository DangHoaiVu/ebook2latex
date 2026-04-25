from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    stored_path = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default="uploaded")
    page_count = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    formulas = relationship(
        "FormulaEntry",
        back_populates="document",
        cascade="all, delete-orphan",
    )


class FormulaEntry(Base):
    __tablename__ = "formula_entries"

    id = Column(String(36), primary_key=True, index=True)
    document_id = Column(String(36), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    page_number = Column(Integer, nullable=True)
    cropped_image_path = Column(Text, nullable=True)
    latex_result = Column(Text, nullable=True)
    source_text = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    document = relationship("Document", back_populates="formulas")
