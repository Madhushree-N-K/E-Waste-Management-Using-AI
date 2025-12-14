from app.db import add_recycler, init_db

# Ensure DB exists
init_db()

sample_recyclers = [
    {
        "name": "Green Earth Recyclers",
        "accepted_items": "mobile,laptop,keyboard",
        "base_multiplier": 1.2,
        "lat": 12.9716,
        "lon": 77.5946,
        "rating": 4.5,
        "capacity_score": 0.9,
        "pickup_available": 1,
        "eco_certified": 1,
        "contact": "9876543210"
    },
    {
        "name": "Eco Friendly Hub",
        "accepted_items": "tv,fridge",
        "base_multiplier": 1.1,
        "lat": 13.0827,
        "lon": 80.2707,
        "rating": 4.2,
        "capacity_score": 0.8,
        "pickup_available": 0,
        "eco_certified": 0,
        "contact": "9123456780"
    }
]

for r in sample_recyclers:
    add_recycler(r)

print("Seeder completed → sample recyclers added.")
