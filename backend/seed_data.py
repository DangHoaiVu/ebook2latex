from uuid import uuid4

from app.core.database import Base, SessionLocal, engine
from app.models import Document, FormulaEntry, User


def seed() -> None:
    """Tao du lieu mau de thu nghiem giao dien va database local."""
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        user = User(
            user_id=uuid4(),
            username_email="teo@dalat.edu.vn",
            password_hash="hashed_password_here",
            full_name="Le Van Teo",
            role="Admin",
        )
        db.add(user)

        document = Document(
            id=uuid4(),
            user_id=user.user_id,
            file_name="sample_math.pdf",
            file_path_url="uploads/sample_math.pdf",
            status="seeded",
        )
        db.add(document)

        formula = FormulaEntry(
            id=uuid4(),
            document_id=document.id,
            raw_image_path="formula_images/sample_formula.png",
            latex_content=r"\int_0^1 x^2 \, dx",
            order_index=1,
        )
        db.add(formula)
        db.commit()

    print("Seed data da duoc them vao database.")


if __name__ == "__main__":
    seed()
