# backend/app/api/match.py

from fastapi import APIRouter, Query
from app import db

router = APIRouter()

# ---------------------------------------------------------
# PRICE ESTIMATION (Rule-based)
# ---------------------------------------------------------

def estimate_price_rule_based(item_type: str) -> float:
    base_prices = {
        "mobile": 300,
        "laptop": 2500,
        "keyboard": 100,
        "mouse": 80,
        "television": 1500,
        "charger": 50,
        "earphone": 40,
        "speaker": 200
    }
    return base_prices.get(item_type.lower(), 100)


# ---------------------------------------------------------
# RECYCLER MATCHING
# ---------------------------------------------------------

def find_recyclers(item_type: str):
    """
    Returns list of recyclers who accept this category.
    """
    all_rows = db.get_all_recyclers()
    item_type = item_type.lower()

    matched = []
    for r in all_rows:
        accepted = r.get("accepted_items", "")
        categories = [c.strip().lower() for c in accepted.split(",")]
        if item_type in categories:
            matched.append({
                "id": r["id"],
                "name": r["name"],
                "accepted_items": categories,
                "base_multiplier": r["base_multiplier"],
                "lat": r["lat"],
                "lon": r["lon"],
                "rating": r["rating"],
                "capacity_score": r["capacity_score"],
                "pickup_available": bool(r["pickup_available"]),
                "eco_certified": bool(r["eco_certified"]),
                "contact": r["contact"]
            })
    return matched


# ---------------------------------------------------------
# DYNAMIC TEST ROUTE
# ---------------------------------------------------------

@router.get("/test")
def test_route(category: str = Query(..., description="E-waste category to match")):
    """
    Returns matched recyclers for a given category.
    Example: /match/test?category=mobile
    """
    try:
        recyclers = find_recyclers(category)
        return {"category": category.lower(), "matched_recyclers": recyclers}
    except Exception as e:
        return {"error": str(e)}
