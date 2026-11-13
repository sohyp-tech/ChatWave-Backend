from sqlalchemy import String, Integer, DateTime, Foreignkey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database.database import Base
import datetime

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, index = True)
    poster_name: Mapped[str] = relationship("User", back_populates = "user")
    poster_id: Mapped[int] = mapped_column(Integer, Foreignkey("users.id"))
    post_content: Mapped[str] = mapped_column(String)
    post_date: Mapped[str] = mapped_column(DateTime, default = datetime.datetime.utcnow, nullable = False)
