from typing import Dict
from typing import List
from typing import Union
from datetime import datetime

from sklearn.pipeline import Pipeline
from sqlalchemy.orm import Session

from app.lib.db_models import Predictions, PredictionDetails


def get_predictions(input: List[str], model: Pipeline, n_preds: int) -> Dict[str, List[Dict[str, List[Union[str, float]]]]]:

    probs = model.predict_proba(input)

    result = []
    for ele in probs:
        labels_with_probs = [(lbl, prob) for lbl, prob in zip(model.classes_, ele)]
        result.append({
            "labels": [ele[0] for ele in sorted(labels_with_probs, key = lambda x: x[1], reverse=True)][:n_preds],
            "probabilities": sorted(ele, reverse=True)[:n_preds]
        })

    return {"predictions": result}


def write_predictions(db: Session, preds: List[Dict[str, List[Union[str, float]]]], texts: List[str]):
    ts = datetime.utcnow()
    for sample_id, (prediction, text) in enumerate(zip(preds, texts)):
        db_pred_row = Predictions(
            timestamp_utc = ts,
            sample_id=sample_id+1,
            text=text,
            label=prediction["labels"][0]
        )
        db.add(db_pred_row)
        for label, probability in zip(prediction["labels"], prediction["probabilities"]):
            db_pred_details_row = PredictionDetails(
                timestamp_utc = ts,
                sample_id = sample_id+1,
                label = label,
                probability = probability
            )
            db.add(db_pred_details_row)

    db.commit()