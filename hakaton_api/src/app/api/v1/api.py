from fastapi import APIRouter
from src.app.api.v1.endpoints import csv_predict, sample_predict

v1_router = APIRouter()

v1_router.include_router(csv_predict.router, tags=[""])
v1_router.include_router(sample_predict.router, tags=[""])
