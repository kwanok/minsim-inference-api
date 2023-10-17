import logging

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from src.models import model

app = FastAPI()


@app.get("/")
async def ping():
    return {"ping": "pong"}


class PredictRequest(BaseModel):
    text: str


class PredictResponse(BaseModel):
    negative: float
    neutral: float
    positive: float


@app.post("/predict")
async def predict(
    q: PredictRequest,
    roberta: model.Roberta = Depends(model.get_roberta),
) -> PredictResponse:
    try:
        result = roberta.predict(q.text)
    except Exception as e:
        logging.error(f"Exception occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return PredictResponse.model_validate(result, from_attributes=True)
