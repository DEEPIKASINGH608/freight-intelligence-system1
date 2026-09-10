from fastapi import APIRouter, HTTPException
from app.schemas import DecisionEvaluationRequest, DecisionEngineResponse
from app.services.decision_engine import DecisionEngine

router = APIRouter()
engine = DecisionEngine()

@router.post("/evaluate", response_model=DecisionEngineResponse)
async def evaluate_decision(payload: DecisionEvaluationRequest):
    try:
        # Pass payload directly—do NOT call payload.dict() here
        return engine.synthesize_decision(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))