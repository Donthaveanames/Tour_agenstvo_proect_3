from datetime import date
from sqlalchemy import String, Date, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Tour(Base):
    __tablename__ = "tours"

    id: Mapped[int] = mapped_column(primary_key=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    date_in: Mapped[date] = mapped_column(Date, nullable=False)
    date_out: Mapped[date] = mapped_column(Date, nullable=False)
    places: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)