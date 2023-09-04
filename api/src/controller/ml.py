from typing import Union
from urllib import response
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import Session
from typing import List
import src.dependency.injection as dep
import src.service.ml as service
import src.repository.mysql as repository
from src.schema.service import category as svcschema

router = APIRouter(prefix="/category")


@router.get("/get", response_model=dict[str, List[svcschema.subcategories]], status_code=status.HTTP_200_OK)
async def get_subcategories(
    *,
    db: Session = Depends(dep.mysqlrep.get_session),
    svc: service.Interface = Depends(dep.mlsvc),
    rep: repository.Interface = Depends(dep.mysqlrep),
) -> Union[Response, List[dict]]:
    """get all subcategories"""
    pass