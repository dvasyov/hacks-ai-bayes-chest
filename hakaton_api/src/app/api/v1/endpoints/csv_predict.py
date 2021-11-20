import os
import io
import pandas as pd
import numpy as np
import random
import time

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse

host = os.environ.get("APP_HOST", "http://localhost:8090")

router = APIRouter()


@router.post("/get_predict_csv")
async def get_predict_csv(csv_file: UploadFile = File(...)):
    """
    """
    df = pd.read_csv(csv_file.file)

    assurance = pd.DataFrame([random.choice(np.arange(0, 1)) for i in range(df.shape[0])], columns=["proba"])

    df_response = df.join(assurance)

    stream = io.StringIO()

    df_response.to_csv(stream, index = False)

    response = StreamingResponse(iter([stream.getvalue()]),
       media_type = "text/csv"
    )

    response.headers["Content-Disposition"] = "attachment; filename=response.csv"
    
    return response