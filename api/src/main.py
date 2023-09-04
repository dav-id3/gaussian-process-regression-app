"""Application main entrypoint"""
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from src.configuration import const
from src.controller.base import router as base_router
from src.controller.account import router as account_router
from src.controller.category import router as category_router
from src.dependency.injection import env

# Application
app = FastAPI(title=const.PROJECT_NAME, version=const.PROJECT_VERSION)
app.include_router(base_router, tags=["test"])
app.include_router(account_router, tags=["account"])
app.include_router(category_router, tags=["category"])

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=env.ALLOW_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
