import os
import io
import pandas as pd
import numpy as np

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse
from src.app.models.model import Model

host = os.environ.get("APP_HOST", "http://localhost:8090")

router = APIRouter()

model = Model()

@router.post("/get_predict_csv")
async def get_predict_csv(csv_file: UploadFile = File(...)):
   """
   """
   df = pd.read_csv(csv_file.file)

   probas = []
   for line in df.itertuples():
      proba = model.predict(line.name)
      if str(line.code) not in proba.keys():
         probas.append(0)
      else:
         max_proba = np.array(list(proba.values())).max()
         min_proba = np.array(list(proba.values())).min()
         cat_proba = float(proba[str(line.code)])
         response_proba = (cat_proba - min_proba) / (max_proba - min_proba)
         probas.append(round(float(response_proba) * 100))
      

   assurance = pd.DataFrame(probas, columns=["proba"])

   df_response = df.join(assurance)

   stream = io.StringIO()

   df_response.to_csv(stream, index = False)

   response = StreamingResponse(iter([stream.getvalue()]),
      media_type = "text/csv"
   )

   response.headers["Content-Disposition"] = "attachment; filename=response.csv"

   return response