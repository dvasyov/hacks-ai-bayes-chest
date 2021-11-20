import os
import pandas as pd

from fastapi import APIRouter, Request, File, UploadFile
from starlette.responses import UJSONResponse

host = os.environ.get("APP_HOST", "http://localhost:8090")

router = APIRouter()


@router.post("/get_predict_csv")
async def get_predict_csv(csv_file: UploadFile = File(...)):
    """
    """
    df = pd.read_csv(csv_file.file)
    pass
