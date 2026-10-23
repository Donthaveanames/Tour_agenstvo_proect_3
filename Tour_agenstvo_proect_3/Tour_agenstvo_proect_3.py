from fastapi import FastAPI
from base import TourCreate



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
    db[counter] = {"id": counter, **TourCreate.model_dump()}
    return db[counter]