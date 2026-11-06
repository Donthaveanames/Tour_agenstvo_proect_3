from datetime import date, datetime
from sqlalchemy import String, Date, Integer, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Tour(Base):
    __tablename__ = "tours"

    id: Mapped[int] = mapped_column(primary_key=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    date_in: Mapped[date] = mapped_column(Date, nullable=False)
    date_out: Mapped[date] = mapped_column(Date, nullable=False)
    places: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    bookings: Mapped[list["Booking"]] = relationship(
        back_populates="tour", cascade="all, delete-orphan"
    )


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    tour_id: Mapped[int] = mapped_column(ForeignKey("tours.id"), nullable=False)
    customer_name: Mapped[str] = mapped_column(nullable=False)
    customer_phone: Mapped[str] = mapped_column(nullable=False)
    places: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    tour: Mapped["Tour"] = relationship(back_populates="bookings")