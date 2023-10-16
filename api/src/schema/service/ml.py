"""schema for ml service"""
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class Prediction(BaseModel):
    """predicted data"""

    value: float = Field(..., description="predicted value")
    is_anomaly: bool = Field(..., description="anomaly or not")


class InputData(BaseModel):
    """predicted data"""

    value: float = Field(..., description="predicted value")
    time: datetime = Field(..., description="time")


class PredictedData(BaseModel):
    """predicted data"""

    value: float = Field(..., description="predicted value")
    time: datetime = Field(..., description="time")
    lower_bound: float = Field(..., description="lower bound of predicted value")
    upper_bound: float = Field(..., description="upper bound of predicted value")
