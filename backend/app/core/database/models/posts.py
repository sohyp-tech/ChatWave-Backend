from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database.database import Base
import datetime

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, index = True)
    poster: Mapped["User"] = relationship("User", back_populates = "posts")
    poster_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(String(50000))
    post_date: Mapped[datetime.datetime] = mapped_column(DateTime, default = datetime.datetime.utcnow, nullable = False)
