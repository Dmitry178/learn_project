from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class UsersOrm(Base):

    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint('lower_email', name='uq_lower_email'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)  # можно использовать тип CITEXT
    hashed_password: Mapped[str] = mapped_column(String(200), nullable=False)

    @property
    def lower_email(self):
        return self.email.lower()