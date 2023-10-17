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

    y_value: float = Field(..., description="predicted value")
    x_value: float = Field(..., description="x value")


class PredictedData(BaseModel):
    """predicted data"""

    y_value: float = Field(..., description="predicted value")
    x_value: float = Field(..., description="x value")
    lower_bound: float = Field(..., description="lower bound of predicted value")
    upper_bound: float = Field(..., description="upper bound of predicted value")
