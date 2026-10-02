from sqlalchemy.orm import Session

from app.database.models import (
    Area,
    Place,
    Eatery,
    Dish,
)


def search_places(
    db: Session,
    area: str | None = None,
    category: str | None = None,
    query: str | None = None,
    limit: int = 10,
):
    """
    Search Chennai places using area, category,
    or place name.
    """

    results = (
        db.query(
            Place,
            Area.name.label("area_name"),
        )
        .join(
            Area,
            Place.area_id == Area.id,
        )
    )

    if area:
        results = results.filter(
            Area.name.ilike(f"%{area}%")
        )

    if category:
        results = results.filter(
            Place.category.ilike(
                f"%{category}%"
            )
        )

    if query:
        results = results.filter(
            Place.name.ilike(
                f"%{query}%"
            )
        )

    results = results.limit(limit).all()

    return [
        {
            "name": place.name,
            "name_ta": place.name_ta,
            "category": place.category,
            "area": area_name,
            "latitude": place.lat,
            "longitude": place.lng,
            "description": place.description,
            "visit_duration_min": place.visit_duration_min,
            "entry_fee_inr": place.entry_fee_inr,
            "hours_note": place.hours_note,
            "indoor_outdoor": place.indoor_outdoor,
            "best_time": place.best_time,
            "source": place.source,
            "source_url": place.source_url,
        }
        for place, area_name in results
    ]


def search_eateries(
    db: Session,
    area: str | None = None,
    cuisine: str | None = None,
    query: str | None = None,
    limit: int = 10,
):
    """
    Search Chennai eateries using area,
    cuisine, or restaurant name.
    """

    results = (
        db.query(
            Eatery,
            Area.name.label("area_name"),
        )
        .join(
            Area,
            Eatery.area_id == Area.id,
        )
    )

    if area:
        results = results.filter(
            Area.name.ilike(f"%{area}%")
        )

    if cuisine:
        results = results.filter(
            Eatery.cuisine.ilike(
                f"%{cuisine}%"
            )
        )

    if query:
        results = results.filter(
            Eatery.name.ilike(
                f"%{query}%"
            )
        )

    results = results.limit(limit).all()

    return [
        {
            "name": eatery.name,
            "area": area_name,
            "latitude": eatery.lat,
            "longitude": eatery.lng,
            "diet": eatery.diet,
            "cuisine": eatery.cuisine,
            "price_band": eatery.price_band,
            "notes": eatery.notes,
            "source": eatery.source,
        }
        for eatery, area_name in results
    ]


def search_dishes(
    db: Session,
    query: str | None = None,
    limit: int = 10,
):
    """
    Search Chennai dishes by name.
    """

    results = db.query(Dish)

    if query:
        results = results.filter(
            Dish.name.ilike(
                f"%{query}%"
            )
        )

    results = results.limit(limit).all()

    return [
        {
            "name": dish.name,
            "name_ta": dish.name_ta,
            "diet": dish.diet,
            "description": dish.description,
        }
        for dish in results
    ]