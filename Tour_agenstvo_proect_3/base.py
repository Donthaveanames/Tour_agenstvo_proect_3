from datetime import date

from pydantic import BaseModel, Field
from typing import Optional
from pydantic.functional_validators import ModelAfterValidator


class TourCreate(BaseModel):
    country: str
    date_in: date
    date_out: date
    places: int = Field(gt=0)
    price: float = Field(gt=0)

#    @ModelAfterValidator
#    def check_data(self):
#        if self.date_in > self.date_out:
#            raise ValueError("The check‑in date must be earlier than the check‑out date.")
#        return self

class TourUpdate(BaseModel):
    country: Optional[str] = Field(default=None, min_length=1)
    date_in: Optional[date] = None
    date_out: Optional[date] = None
    places: Optional[int] = Field(default=None, gt=0)
    price: Optional[float] = Field(default=None, gt=0)


