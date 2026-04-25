from uuid import uuid4

from app.core.database import Base, SessionLocal, engine
from app.models import Document, FormulaEntry


def seed() -> None:
    """Tao du lieu mau de thu nghiem giao dien va database local."""
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        document = Document(
            id=str(uuid4()),
            file_name="sample_math.pdf",
            stored_path="uploads/sample_math.pdf",
            status="seeded",
            page_count=3,
        )
        db.add(document)

        formula = FormulaEntry(
            id=str(uuid4()),
            document_id=document.id,
            page_number=1,
            cropped_image_path="formula_images/sample_formula.png",
            latex_result=r"\int_0^1 x^2 \, dx",
            source_text="int_0^1 x^2 dx",
        )
        db.add(formula)
        db.commit()

    print("Seed data da duoc them vao database.")


if __name__ == "__main__":
    seed()
