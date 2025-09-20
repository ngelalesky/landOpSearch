import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from stable_baselines3 import PPO
from env_service.land_opportunity_env import LandOpportunityEnv

app = FastAPI(title="Land Opportunity Search API")

# Load the trained model
try:
    model = PPO.load("best_model/best_model")
except Exception as e:
    print(f"Warning: Could not load model: {e}")
    model = None

class LandData(BaseModel):
    """Input data for land evaluation."""
    features: list[float]  # [x, y, soil_type, elevation, slope, water_access, zoning, market_value, development_potential]

class EvaluationResponse(BaseModel):
    """Response containing the model's evaluation."""
    score: float
    confidence: float
    recommended_action: int

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_land(data: LandData):
    """Evaluate a land parcel using the trained model."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Convert input features to numpy array
        features = np.array(data.features, dtype=np.float32)
        
        # Create a dummy environment for evaluation
        env = LandOpportunityEnv(land_data={})  # Empty dict since we're just evaluating
        
        # Get model's action and value prediction
        action, _states = model.predict(features, deterministic=True)
        
        # Get the model's value prediction (confidence)
        value = model.policy.get_value(features)[0]
        
        return EvaluationResponse(
            score=float(value),
            confidence=float(np.abs(value)),  # Use absolute value as confidence
            recommended_action=int(action)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 