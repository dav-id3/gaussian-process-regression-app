"""schema for mysql"""
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from src.schema.service.ml import PredictedData


class PredictionResponse(BaseModel):
    """predicted data"""

    predicted_data: List[PredictedData] = Field(..., description="predicted data")
    predicted_next_data: PredictedData = Field(..., description="predicted next value")
          
