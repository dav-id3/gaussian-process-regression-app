"""schema for ml controller"""
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field
from src.schema.service import ml as svcschema


class InputData(BaseModel):
    y_value: float = Field(..., description="predicted value")
    x_value: float = Field(..., description="x value")

    def to_service(self) -> svcschema.InputData:
        return svcschema.InputData(
            y_value=self.y_value,
            x_value=self.x_value,
        )


class PredictedData(BaseModel):
    """predicted data"""

    y_value: float = Field(..., description="predicted value")
    x_value: float = Field(..., description="x value")
    lower_bound: float = Field(..., description="lower bound of predicted value")
    upper_bound: float = Field(..., description="upper bound of predicted value")

    @staticmethod
    def from_service(service_predicted_data: svcschema.PredictedData):
        return PredictedData(
            y_value=service_predicted_data.y_value,
            x_value=service_predicted_data.x_value,
            lower_bound=service_predicted_data.lower_bound,
            upper_bound=service_predicted_data.upper_bound,
        )


class PredictionResponse(BaseModel):
    """predicted data"""

    predicted_data: List[PredictedData] = Field(..., description="predicted data")
    predicted_next_data: PredictedData = Field(..., description="predicted next value")
