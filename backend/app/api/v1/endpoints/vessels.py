from fastapi import APIRouter

router = APIRouter()

# Default mock fleet data for vessel queries
MOCK_FLEET = [
    {
        "vessel_id": "V-001",
        "name": "MV Ocean Power",
        "capacity_dwt": 82000,
        "max_draft_m": 14.5,
        "loa_m": 229,
        "daily_charter_rate_usd": 18500,
        "speed_knots": 14.0,
    },
    {
        "vessel_id": "V-002",
        "name": "MV Eastern Trader",
        "capacity_dwt": 58000,
        "max_draft_m": 12.8,
        "loa_m": 190,
        "daily_charter_rate_usd": 14200,
        "speed_knots": 13.5,
    },
    {
        "vessel_id": "V-003",
        "name": "MV Iron Giant",
        "capacity_dwt": 180000,
        "max_draft_m": 18.2,
        "loa_m": 292,
        "daily_charter_rate_usd": 28000,
        "speed_knots": 14.5,
    },
]


@router.get("/")
def get_vessels():
    return {"status": "success", "count": len(MOCK_FLEET), "data": MOCK_FLEET}