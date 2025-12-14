from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

# Import routers safely
try:
    from app.api import predict, match
except ImportError as e:
    print(f"Router import failed: {e}")
    predict = match = None

# Import DB safely
try:
    from app import db
except ImportError as e:
    print(f"DB import failed: {e}")
    db = None

# Lifespan handler for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    if db:
        try:
            db.init_db()
            print("Database initialized")
        except Exception as e:
            print(f"DB initialization failed: {e}")
    yield
    # Shutdown code
    print("App is shutting down")

# Create FastAPI app with lifespan
app = FastAPI(title="E-Waste Exchange API", lifespan=lifespan)

# ------------------- CORS Setup -------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with frontend URL if needed, e.g., "http://localhost:5173"
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------------------------------------

# Include routers if available
if predict:
    app.include_router(predict.router, prefix="/predict")
if match:
    app.include_router(match.router, prefix="/match")

# Root endpoint
@app.get("/")
def root():
    return {"message": "E-Waste Exchange API is running. See /docs for API docs."}
