import json
from datetime import datetime
from pathlib import Path

from app.database.session import Base, SessionLocal, engine

from app.database.models import (
    Area,
    Place,
    Eatery,
    Dish,
)


BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"


def load_json(filename):

    file_path = DATA_DIR / filename

    print(f"Loading: {file_path}")

    with open(
        file_path,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


def create_tables():

    Base.metadata.create_all(
        bind=engine
    )

    print("Database tables created.")


def seed_areas(db):

    areas = load_json("areas.json")

    for item in areas:

        existing = (
            db.query(Area)
            .filter(
                Area.name == item["name"]
            )
            .first()
        )

        if existing:
            continue

        area = Area(
            name=item["name"],
            name_ta=item.get("name_ta"),
            lat=item.get("lat"),
            lng=item.get("lng"),
        )

        db.add(area)

    db.commit()

    print(f"Loaded {len(areas)} areas.")


def seed_places(db):

    places = load_json("places.json")

    for item in places:

        area = (
            db.query(Area)
            .filter(
                Area.name == item["area"]
            )
            .first()
        )

        if not area:

            print(
                f"Warning: area not found for "
                f"{item['name']}: {item['area']}"
            )

            continue

        existing = (
            db.query(Place)
            .filter(
                Place.name == item["name"]
            )
            .first()
        )

        if existing:
            continue

        place = Place(
            name=item["name"],
            name_ta=item.get("name_ta"),
            category=item["category"],
            area_id=area.id,
            lat=item.get("lat"),
            lng=item.get("lng"),
            description=item.get("description"),
            visit_duration_min=item.get(
                "visit_duration_min"
            ),
            entry_fee_inr=item.get(
                "entry_fee_inr"
            ),
            hours_note=item.get(
                "hours_note"
            ),
            indoor_outdoor=item.get(
                "indoor_outdoor"
            ),
            best_time=item.get(
                "best_time"
            ),
            source=item.get(
                "source"
            ),
            source_url=item.get(
                "source_url"
            ),
            last_verified_at=datetime.utcnow(),
        )

        db.add(place)

    db.commit()

    print(f"Loaded {len(places)} places.")


def seed_eateries(db):

    eateries = load_json("eateries.json")

    for item in eateries:

        area = (
            db.query(Area)
            .filter(
                Area.name == item["area"]
            )
            .first()
        )

        if not area:

            print(
                f"Warning: area not found for "
                f"{item['name']}: {item['area']}"
            )

            continue

        existing = (
            db.query(Eatery)
            .filter(
                Eatery.name == item["name"]
            )
            .first()
        )

        if existing:
            continue

        eatery = Eatery(
            name=item["name"],
            area_id=area.id,
            lat=item.get("lat"),
            lng=item.get("lng"),
            diet=item.get("diet"),
            cuisine=item.get("cuisine"),
            price_band=item.get("price_band"),
            notes=item.get("notes"),
            source=item.get("source"),
            last_verified_at=datetime.utcnow(),
        )

        db.add(eatery)

    db.commit()

    print(f"Loaded {len(eateries)} eateries.")


def seed_dishes(db):

    dishes = load_json("dishes.json")

    for item in dishes:

        existing = (
            db.query(Dish)
            .filter(
                Dish.name == item["name"]
            )
            .first()
        )

        if existing:
            continue

        dish = Dish(
            name=item["name"],
            name_ta=item.get("name_ta"),
            diet=item.get("diet"),
            description=item.get("description"),
        )

        db.add(dish)

    db.commit()

    print(f"Loaded {len(dishes)} dishes.")


def seed_database():

    print("Starting Chennai Explorer database seed...")

    create_tables()

    db = SessionLocal()

    try:

        seed_areas(db)

        seed_places(db)

        seed_eateries(db)

        seed_dishes(db)

        print(
            "\nChennai Explorer database "
            "seed completed successfully!"
        )

    except Exception as error:

        db.rollback()

        print("\nERROR:", error)

        raise

    finally:

        db.close()


if __name__ == "__main__":

    seed_database()