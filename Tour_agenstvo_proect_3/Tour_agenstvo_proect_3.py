
from fastapi import FastAPI, HTTPException, Response, Request
import time
#from base import TourCreate, TourUpdate

from datetime import date

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


###======================================###
from pydantic import BaseModel, Field
from typing import Optional

class TourCreate(BaseModel):
    country: str = Field(min_length=1)
    date_in: date
    date_out: date
    places: int = Field(gt=0)
    price: float = Field(gt=0)


class TourUpdate(BaseModel):
    country: Optional[str] = Field(default=None, min_length=1)
    date_in: Optional[date] = None
    date_out: Optional[date] = None
    places: Optional[int] = Field(default=None, gt=0)
    price: Optional[float] = Field(default=None, gt=0)

###======================================###

app = FastAPI()


@app.get("/health", status_code=200)
def health():
    return {"status": "ok"}


db = {}
counter = 0

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000
    print(f"{request.method} {request.url.path} "
          f"{response.status_code} {elapsed_ms:.1f}ms")
    return response



def check(id) -> None:
    if id not in db:
        raise HTTPException(status_code=404, detail="Tour not found")



@app.post("/api/tours", status_code=201)
def create_tour(item: TourCreate):
    global counter
    counter = counter + 1
    db[counter] = {"id": counter, **item.model_dump()}
    return db[counter]


@app.get("/api/tours")
def tours_list(request: Request):

    params = dict(request.query_params)

    try:
        limit = int(params.pop("limit", 10))
        offset = int(params.pop("offset", 0))
    except ValueError:
        raise HTTPException(status_code=400,
                            detail={"error": "limit/offset must be integers",
                                    "field": "limit/offset"})
    if limit < 0 or offset < 0:
        raise HTTPException(status_code=400,
                            detail={"error": "limit/offset must be >= 0",
                                    "field": "limit/offset"})

    valid = set(TourCreate.model_fields) | {"id"}
    unknown = set(params) - valid
    if unknown:
        raise HTTPException(
            status_code=400,
            detail={"error": f"Unknown filter fields: {sorted(unknown)}",
                    "field": sorted(unknown)[0]},
        )

    result = [t for t in db.values()
              if all(str(t.get(k)) == v for k, v in params.items())]

    return result[offset: offset + limit]


@app.get("/api/tours/{id}")
def get_tour(id: int):
    check(id)
    return db[id]

@app.put("/api/tours/{id}")
def tour_full_update(item: TourCreate, id: int):
    check(id)
    db[id] = {"id": id, **item.model_dump()}
    return db[id]

@app.patch("/api/tours/{id}")
def tour_update(id: int, item: TourUpdate):
    check(id)
    db[id].update(item.model_dump(exclude_unset=True))
    return db[id]

@app.delete("/api/tours/{id}", status_code=204)
def delete_tour(id: int):
    check(id)
    del db[id]
    

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