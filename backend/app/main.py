from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Freight Intelligence & Vessel Optimization API",
    description="Backend API for SIH Freight Forecasting, Delay Risk, and Vessel Chartering Optimization Engine.",
    version="1.0.0"
)

# Enable CORS for Frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "system": "Freight Intelligence & Vessel Optimization System",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}