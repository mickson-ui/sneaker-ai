from pydantic import BaseModel
from typing import List

class PredictionResult(BaseModel):
    """
    Represents a single prediction result.
    """
    label: str
    confidence: float


class PredictionResponse(BaseModel):
    """
    Full API response containing multiple predictions.
    """
    predictions: List[PredictionResult]