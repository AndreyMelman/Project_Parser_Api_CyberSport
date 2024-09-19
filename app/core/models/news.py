from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class News(Base):
    __tablename__ = "news"

    id_news: Mapped[int] = mapped_column(primary_key=True, unique=True)
    title: Mapped[str]
    created_at: Mapped[datetime]
    url: Mapped[str]
    img_url: Mapped[str]
    category: Mapped[str]
    sent_to_telegram: Mapped[bool] = mapped_column(default=False)
