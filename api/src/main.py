"""Application main entrypoint"""
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.configuration import const
from src.controller.ml import router as ml_router
from src.dependency.injection import env

# Application
app = FastAPI(title=const.PROJECT_NAME, version=const.PROJECT_VERSION)
app.include_router(ml_router, tags=["ml"])

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=env.ALLOW_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
