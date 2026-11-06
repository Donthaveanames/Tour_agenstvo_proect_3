from datetime import date, datetime

from pydantic import BaseModel, Field, model_validator, ConfigDict
from typing import Optional


class TourCreate(BaseModel):
    country: str
    date_in: date
    date_out: date
    places: int = Field(gt=0)
    price: float = Field(gt=0)

    @model_validator(mode='after')
    def check_data(self):
        if self.date_in > self.date_out:
            raise ValueError("The check‑in date must be earlier than the check‑out date.")
        return self

class TourUpdate(BaseModel):
    country: Optional[str] = Field(default=None, min_length=1)
    date_in: Optional[date] = None
    date_out: Optional[date] = None
    places: Optional[int] = Field(default=None, gt=0)
    price: Optional[float] = Field(default=None, gt=0)


class TourRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    country: str
    date_in: date
    date_out: date
    places: int
    price: float



class BookingCreate(BaseModel):
    customer_name: str = Field(min_length=1)
    customer_phone: str = Field(min_length=1)
    places: int = Field(gt=0)

class BookingUpdate(BaseModel):
    customer_name: Optional[str] =  Field(default=None, min_length=1)
    customer_phone: Optional[str] =  Field(default=None, min_length=1)
    places: Optional[int] =  Field(default=None, gt=1)

class BookingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    tour_id: int
    customer_name: str
    customer_phone: str
    places: int
    created_at: datetime