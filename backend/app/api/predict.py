# backend/app/api/predict.py

from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import JSONResponse
from PIL import Image
import io, traceback, sys

from app.core.model_utils import classify_image_pil
from app.schemas import PredictionResponse
from app.api.match import estimate_price_rule_based, find_recyclers

router = APIRouter()

@router.post("/", response_model=PredictionResponse)
async def predict_image(
    image: UploadFile = File(...),
    brand: str = Form(None),
    age_months: int = Form(0),
    condition: str = Form("good")
):
    """
    Upload → classify → estimate price → match recyclers.
    """
    try:
        # 1️⃣ Load file bytes
        contents = await image.read()

        # 2️⃣ Convert to PIL image
        try:
            pil_img = Image.open(io.BytesIO(contents)).convert("RGB")
        except Exception:
            traceback.print_exc()
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid image file."}
            )

        # 3️⃣ Classify image
        raw_label, confidence, probabilities = classify_image_pil(pil_img)

        # Normalize label for matching (lowercase)
        label = raw_label.lower()

        # 4️⃣ Price estimation
        estimated_price = estimate_price_rule_based(label)

        # 5️⃣ Recycler matching
        recycler_list = find_recyclers(label) or []

        # 6️⃣ Return clean API response
        return PredictionResponse(
            item_type=raw_label,         # return clean original label
            confidence=confidence,
            probabilities=probabilities,
            estimated_price=estimated_price,
            price_confidence=0.8,
            recyclers=recycler_list
        )

    except Exception:
        print("Internal error in /predict:", file=sys.stderr)
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error. Check backend logs."}
        )
