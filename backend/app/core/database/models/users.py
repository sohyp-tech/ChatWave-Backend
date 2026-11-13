from sqlalchemy import String, Integer, Foreignkey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, index = True)
    name: Mapped[str] = mapped_column(String(20))
    phone_number: Mapped[str] = mapped_column(String, unique=True)
    description: Mapped[str] = mapped_column(String(100), nullable=True)
    photo_url: Mapped[str] = mapped_column(String, nullable=False)
    token: Mapped[str] = mapped_column(String, nullable=False)

    posts: Mapped[list] = relationship("Post", back_populates="user")