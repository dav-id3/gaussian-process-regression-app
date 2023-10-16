"""schema for ml controller"""
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field
from src.schema.service import ml as svcschema


class InputData(BaseModel):
    value: float = Field(..., description="predicted value")
    time: datetime = Field(..., description="time")

    def to_service(self) -> svcschema.InputData:
        return svcschema.InputData(
            value=self.value,
            time=self.time,
        )


class PredictedData(BaseModel):
    """predicted data"""

    value: float = Field(..., description="predicted value")
    time: datetime = Field(..., description="time")
    lower_bound: float = Field(..., description="lower bound of predicted value")
    upper_bound: float = Field(..., description="upper bound of predicted value")

    @staticmethod
    def from_service(service_predicted_data: svcschema.PredictedData):
        return PredictedData(
            value=service_predicted_data.value,
            time=service_predicted_data.time,
            lower_bound=service_predicted_data.lower_bound,
            upper_bound=service_predicted_data.upper_bound,
        )


class PredictionResponse(BaseModel):
    """predicted data"""

    predicted_data: List[PredictedData] = Field(..., description="predicted data")
    predicted_next_data: PredictedData = Field(..., description="predicted next value")
