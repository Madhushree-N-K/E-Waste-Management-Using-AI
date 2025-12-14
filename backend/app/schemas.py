# backend/app/schemas.py

from pydantic import BaseModel
from typing import Dict, List, Optional


# ----------------------------------------------------
# Recycler Information Schema
# ----------------------------------------------------
class RecyclerInfo(BaseModel):
    name: str
    location: Dict[str, Optional[float]]   # {"lat": 12.3, "lng": 77.5}
    contact: Optional[str]
    rating: Optional[float]
    pickup_available: bool
    eco_certified: bool


# ----------------------------------------------------
# Prediction Response Schema
# ----------------------------------------------------
class PredictionResponse(BaseModel):
    item_type: str                        # e.g., "Laptop"
    confidence: float                     # model prediction confidence
    probabilities: Dict[str, float]       # all class probabilities
    estimated_price: float                # automatically calculated
    price_confidence: float               # confidence for price
    recyclers: List[RecyclerInfo]         # matched recyclers list


# ----------------------------------------------------
# Price Estimation Request Schema
# ----------------------------------------------------
class PriceRequest(BaseModel):
    item_type: str                         # e.g., "Laptop"
    weight: float                          # in KG


# ----------------------------------------------------
# Price Estimation Response Schema
# ----------------------------------------------------
class PriceResponse(BaseModel):
    estimated_price: float
    price_confidence: float = 0.95         # optional default value


# ----------------------------------------------------
# File Upload Prediction Request (Optional)
# ----------------------------------------------------
class PredictFileResponse(BaseModel):
    message: str
    data: PredictionResponse
