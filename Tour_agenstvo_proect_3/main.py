
from fastapi import FastAPI, HTTPException, Request, Depends
import time

from sqlalchemy.orm import Session

from datetime import date

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .database import engine, Base, SessionLocal, get_db
from .models import Tour, Booking
from .base import TourCreate, TourUpdate, TourRead, BookingCreate, BookingRead, BookingUpdate

app = FastAPI(title="Tours", version="2.0.0",)


@app.get("/health", status_code=200)
def health():
    return {"status": "ok"}


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000
    print(f"{request.method} {request.url.path} "
          f"{response.status_code} {elapsed_ms:.1f}ms")
    return response



def check_get_tour(db: Session, tour_id: int) -> Tour:
    tour = db.get(Tour, tour_id)
    if tour is None:
        raise HTTPException(status_code=404, detail="Tour not found")
    return tour



@app.post("/api/tours", status_code=201)
def create_tour(item: TourCreate, db: Session = Depends(get_db)):
    tour = Tour(**item.model_dump())
    db.add(tour)
    db.commit()
    db.refresh(tour)
    return tour


@app.get("/api/tours")
def tours_list(
    request: Request,
    country: str | None = None,
    date_in: date | None = None,
    date_out: date | None = None,
    places: int | None = None,
    price: float | None = None,
    db: Session = Depends(get_db),
):
    valid = {"country", "date_in", "date_out", "places", "price"}
    unknown = set(request.query_params) - valid
    if unknown:
        raise HTTPException(
            status_code=400,
            detail={"error": f"Unknown filter fields: {sorted(unknown)}",
                    "field": sorted(unknown)[0]},
        )

    query = db.query(Tour)

    if country is not None:
        query = query.filter(Tour.country == country)
    if date_in is not None:
        query = query.filter(Tour.date_in == date_in)
    if date_out is not None:
        query = query.filter(Tour.date_out == date_out)
    if places is not None:
        query = query.filter(Tour.places == places)
    if price is not None:
        query = query.filter(Tour.price == price)

    return  query.all()


@app.get("/api/tours/{id}")
def get_tour(id: int, db: Session = Depends(get_db)):
    return check_get_tour(db, id)

@app.put("/api/tours/{id}")
def tour_full_update(item: TourCreate, id: int, db: Session = Depends(get_db)):
    tour = check_get_tour(db, id)

    for field, value in item.model_dump().items():
        setattr(tour, field, value)
    
    db.commit()
    db.refresh(tour)
    return tour

@app.patch("/api/tours/{id}")
def tour_update(id: int, item: TourUpdate, db: Session = Depends(get_db)):
    tour = check_get_tour(db, id)
    
    for field, value in item.model_dump(exclude_unset=True).items():
        setattr(tour, field, value)

    if tour.date_in > tour.date_out:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail={"error": "date_in must be earlier than date_out", "field": "date_in"},
        )

    db.commit()
    db.refresh(tour)
    return tour


@app.delete("/api/tours/{id}", status_code=204)
def delete_tour(id: int, db: Session = Depends(get_db)) -> None:
    tour = check_get_tour(db, id)
    db.delete(tour)
    db.commit()


###=============Booking================###

@app.post("/api/tours/{id}/bookings", status_code=201, response_model=BookingRead)
def booking_create(id: int, item: BookingCreate, db: Session = Depends(get_db)):
    tour = check_get_tour(db, id)
    booked = sum(b.places for b in tour.bookings)
    if booked + item.places > tour.places:
        raise HTTPException(
            status_code=409,
            detail={"error": "Not enough places", "field": "places"},
        )

    booking = Booking(tour_id=id, **item.model_dump())
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@app.get("/api/tours/{id}/bookings", response_model=list[BookingRead])
def get_bookings_list(id: int, db: Session = Depends(get_db)):
    tour = check_get_tour(db, id)
    return (
        db.query(Booking)
        .filter(Booking.tour_id == id)
        .order_by(Booking.created_at.desc())
        .all()
    )


@app.delete("/api/tours/{id}/bookings/{b_id}", status_code=204)
def booking_delete(id: int, b_id: int, db: Session = Depends(get_db)) -> None:
    booking = db.get(Booking, b_id)
    if booking is None or booking.tour_id != id:
        raise HTTPException(404, "Booking not found")
    db.delete(booking)
    db.commit()



@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    errors = jsonable_encoder(exc.errors())
    first = errors[0] if errors else {}
    loc = first.get("loc", [])
    field = loc[-1] if len(loc) > 1 else "body"

    if first.get("type") == "json_invalid":
        field = "body"
        message = "Malformed JSON"
    else:
        message = first.get("msg", "Validation error")
    return JSONResponse(status_code=400, content={"error": message, "field": field})