from typing import List, Union
from urllib import response

import src.dependency.injection as dep
import src.repository.mysql as repository
import src.service.ml as service
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import Session
from src.schema.controller import ml as ctrlschema

router = APIRouter(prefix="/ml")


@router.get(
    "/predict",
    response_model=dict[str, List[ctrlschema.PredictionResponse]],
    status_code=status.HTTP_200_OK,
)
async def predict_next_value(
    *,
    db: Session = Depends(dep.mysqlrep.get_session),
    svc: service.Interface = Depends(dep.mlsvc),
    rep: repository.Interface = Depends(dep.mysqlrep),
    req: List[ctrlschema.InputData]
) -> Response:
    """Predict value next to series of input"""
    predicted_values, predicted_next_value = svc.train_and_predict(
        db, rep, [r.to_service for r in req]
    )
    return {
        "response": ctrlschema.PredictionResponse(
            predicted_data=[
                ctrlschema.PredictedData.from_service(pv) for pv in predicted_values
            ],
            predicted_next_value=ctrlschema.PredictedData.from_service(
                predicted_next_value
            ),
        ),
    }
