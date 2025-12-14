# backend/init_db.py
from app import db

def seed():
    db.init_db()
    sample = [
        {"name":"GreenRecyle Hub","base_multiplier":0.85,"lat":12.9716,"lon":77.5946,"rating":4.6,"capacity_score":0.9,"pickup_available":1,"eco_certified":1,"contact":"+91-9000000001"},
        {"name":"FastBuy Recyclers","base_multiplier":0.9,"lat":12.9610,"lon":77.6010,"rating":4.2,"capacity_score":0.8,"pickup_available":1,"eco_certified":0,"contact":"+91-9000000002"},
        {"name":"PartsTrader","base_multiplier":0.6,"lat":12.9350,"lon":77.6240,"rating":3.8,"capacity_score":0.6,"pickup_available":0,"eco_certified":0,"contact":"+91-9000000003"},
    ]
    for r in sample:
        db.add_recycler(r)
    print("Seeded recyclers.db with sample data.")

if __name__ == "__main__":
    seed()
