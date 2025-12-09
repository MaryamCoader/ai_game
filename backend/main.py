from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import analysis

app = FastAPI()

# -----------------------------
# Add CORS middleware BEFORE including routers
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router AFTER middleware
app.include_router(analysis.router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok"}
