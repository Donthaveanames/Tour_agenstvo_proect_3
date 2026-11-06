from datetime import date

from database import SessionLocal
from models import Tour, Booking


TOURS = [
    {
        "country": "Китай",
        "date_in": date(2027, 4, 12),
        "date_out": date(2027, 4, 20),
        "places": 5,
        "price": 150000,
    },
    {
        "country": "Германия",
        "date_in": date(2027, 5, 12),
        "date_out": date(2027, 5, 26),
        "places": 3,
        "price": 70000,
    },
    {
        "country": "Франция",
        "date_in": date(2027, 6, 1),
        "date_out": date(2027, 6, 10),
        "places": 2,
        "price": 200000,
    },
]


BOOKINGS = [
    (0, "Иван Иванов", "+79001234567", 2),
    (0, "Мария Петрова", "+79007654321", 1),
    (1, "Пётр Сидоров", "+79005553322", 2),
]


def seed() -> None:
    db = SessionLocal()
    try:
        if db.query(Tour).count() > 0:
            print("База не пуста — сиды пропущены.")
            return

        tours: list[Tour] = []
        for data in TOURS:
            tour = Tour(**data)
            db.add(tour)
            tours.append(tour)

        db.flush()

        for tour_idx, name, phone, places in BOOKINGS:
            db.add(
                Booking(
                    tour_id=tours[tour_idx].id,
                    customer_name=name,
                    customer_phone=phone,
                    places=places,
                )
            )

        db.commit()
        print(f"Загружено туров: {len(TOURS)}, броней: {len(BOOKINGS)}.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()

