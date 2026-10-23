from fastapi import FastAPI, HTTPException
#from base import TourCreate

from datetime import date

from pydantic import BaseModel, Field

class TourCreate(BaseModel):
    country: str
    date_in: date
    date_out: date
    places: int = Field(gt=0)
    price: float = Field(gt=0)

app = FastAPI()


@app.get("/health", status_code=200)
def health():
    return {"status": "ok"}


db = {}
counter = 0

@app.post("/api/tours", status_code=201)
def create_tour(item: TourCreate):
    global counter
    counter = counter + 1
    db[counter] = {"id": counter, **item.model_dump()}
    return db[counter]


@app.get("/api/tours")
def tours_list():
    return list(db.values())


@app.get("/api/tours/{id}")
def get_tour(id: int):
    if id not in db:
        raise HTTPException(status_code=404, detail="Tour not found")
    return db[id]