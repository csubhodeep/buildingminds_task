from typing import List

from pydantic import BaseModel
from pydantic import Field


class SinglePredictionRequest(BaseModel):
    text: str = Field(..., example="This is an example text")
    n_preds: int = Field(..., example=2, gt=0)


class BatchPredictionRequest(BaseModel):
    texts: List[str] = Field(..., example=["This is an example text", "This is another example text"])
    n_preds: int = Field(..., example=2, gt=0)

class SinglePredictionResponse(BaseModel):
    labels: List[str] = Field(..., example=['Guardian', 'Atlantic', 'New_York_Times'])
    probabilities: List[float] = Field(..., example=[0.7, 0.2, 0.1])


class BatchPredictionResponse(BaseModel):
    predictions: List[SinglePredictionResponse]