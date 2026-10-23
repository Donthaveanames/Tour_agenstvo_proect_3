from datetime import date

from pydantic import BaseModel, Field
from pydantic.functional_validators import ModelAfterValidator


class TourCreate(BaseModel):
    country: str
    date_in: date
    date_out: date
    places: int = Field(gt=0)
    price: float = Field(gt=0)

    @ModelAfterValidator
    def check_data(self):
        if self.date_in > self.date_out:
            return ValueError("The check‑in date must be earlier than the check‑out date.")
        return self




