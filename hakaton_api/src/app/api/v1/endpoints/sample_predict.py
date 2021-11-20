import os
import numpy as np
import pandas as pd
import torch

from fastapi import APIRouter
from starlette.responses import UJSONResponse

from src.app.schemas.request import RequestSample
from src.app.schemas.response import ResponseCategory
from src.app.models.model import Model

host = os.environ.get("APP_HOST", "http://localhost:8090")

router = APIRouter()

model = Model()

@router.post(
    "/get_predict_sample", response_class=UJSONResponse, response_model=ResponseCategory,
)
async def get_predict_sample(request: RequestSample):
    production_description = request.production_description
    production_code = request.production_code

    probas = model.predict(production_description)
    
    if production_code not in probas.keys():
        return ResponseCategory(match = 0)
    else:
        max_proba = np.array(list(probas.values())).max()
        min_proba = np.array(list(probas.values())).min()
        cat_proba = float(probas[production_code])
        response_proba = (cat_proba - min_proba) / (max_proba - min_proba)
        response = ResponseCategory(match = round(float(response_proba) * 100))
        return response
