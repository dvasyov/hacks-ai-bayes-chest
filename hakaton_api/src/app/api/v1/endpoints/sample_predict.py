import os
import random
from typing import Match

from fastapi import APIRouter, Request
from starlette.responses import UJSONResponse

from src.app.schemas.request import RequestSample
from src.app.schemas.response import ResponseCategory

host = os.environ.get("APP_HOST", "http://localhost:8090")

router = APIRouter()


@router.post(
    "/get_predict_sample", response_class=UJSONResponse, response_model=ResponseCategory,
)
async def get_predict_sample(request: RequestSample):
    """
    """

    production_description = request.production_description
    match = random.choice([True, False])
    if match:
        response = ResponseCategory(match = "Подошло")
    else:
        response = ResponseCategory(match = "Не сошлось")
    return response