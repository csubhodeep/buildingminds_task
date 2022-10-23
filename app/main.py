import joblib
import logging
import os
import traceback
from logging import getLogger
from pathlib import Path
from threading import Thread

from fastapi import Depends
from fastapi import FastAPI
from fastapi import status
from fastapi.responses import JSONResponse
from sklearn.pipeline import Pipeline

from app.lib.db_models import Base
from app.lib.models import BatchPredictionRequest, BatchPredictionResponse
from app.lib.models import SinglePredictionRequest, SinglePredictionResponse
from app.lib.utils import get_predictions, write_predictions
from app.database import SessionLocal, engine

Base.metadata.create_all(bind=engine)


IS_DEBUG_MODE = os.getenv("ENVIRONMENT", "") == "test"


app = FastAPI(debug=IS_DEBUG_MODE, title="Inference API", version="1.0.0")

path_to_logs_folder = Path.cwd().joinpath("logs")
path_to_logs_folder.mkdir(exist_ok=True)


if IS_DEBUG_MODE:
    logging.basicConfig(
        filename=str(path_to_logs_folder.joinpath("api_logs.log")),
        level=logging.DEBUG,
        filemode="w",
    )
else:
    logging.basicConfig(
        filename=str(path_to_logs_folder.joinpath("api_logs.log")),
        level=logging.ERROR,
        filemode="w",
    )

app_logger = getLogger(name=__name__)


# Dependencies
def load_model():
    yield joblib.load("./app/model.joblib")

# Dependency
def get_db():

    global db
    try:
        db = SessionLocal()
    except:
        db = None

get_db()


@app.post(
    "/inference_api/single_prediction",
    status_code=status.HTTP_200_OK,
    response_model=SinglePredictionResponse,
)
async def single_prediction(
    request: SinglePredictionRequest,
    model: Pipeline = Depends(load_model)
):

    try:
        content = request.dict()

        result = get_predictions([content["text"]], model, content["n_preds"])["predictions"]
        if db:
            th = Thread(target=write_predictions, args=(db, result, [content["text"]]))
            th.start()
        if IS_DEBUG_MODE:
            app_logger.info(msg={**result, **content})
        # return just one result
        return result[0]
    except Exception as ex:
        error_message = {
            "request": content,
            "trace_of_error": traceback.format_tb(tb=ex.__traceback__)[0],
            "exception": str(ex),
        }
        app_logger.error(msg=error_message)
        return JSONResponse(
            content={"error": error_message},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@app.post(
    "/inference_api/batch_prediction",
    status_code=status.HTTP_200_OK,
    response_model=BatchPredictionResponse,
)
async def batch_prediction(request: BatchPredictionRequest, model: Pipeline = Depends(load_model)):

    try:
        content = request.dict()

        result = get_predictions(content["texts"], model, content["n_preds"])
        if db:
            th = Thread(target=write_predictions, args=(db, result["predictions"], content["texts"]))
            th.start()
        if IS_DEBUG_MODE:
            app_logger.info(msg={**result, **content})
        return result
    except Exception as ex:
        error_message = {
            "request": content,
            "trace_of_error": traceback.format_tb(tb=ex.__traceback__)[0],
            "exception": str(ex),
        }
        app_logger.error(msg=error_message)
        return JSONResponse(
            content={"error": error_message},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
