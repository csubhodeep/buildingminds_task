# We could use the tuned and more efficient official image from - tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim-2021-10-02
# However, it raises the following concerns:
# 1. it brings in Python-3.9.7 which may cause problems with the model file as it is trained on 3.9.13
# 2. it has older versions of packages in it - FastAPI (0.68.1) and uvicorn (0.15.0) while the newest are 0.85.1 and 0.18.3 respectively.
# 3. FastAPI, uvicorn and its sub-dependencies may cause conflict in version resolution with other third-party packages required by this project.

# so here we prefer compatibility and reproducibility and go with the official one which brings in Python-3.9.15

FROM python:3.9-slim

# following the directory structure recommended in the guidelines in the official docs - https://fastapi.tiangolo.com/deployment/docker/#create-the-fastapi-code
WORKDIR /code

COPY set_env.sh /code/set_env.sh

COPY requirements/requirements.txt /code/requirements.txt

COPY ./app /code/app

RUN mkdir "data"

RUN mkdir "logs"

RUN ["sh", "set_env.sh"]

# activate virtual environment
ENV PATH=/code/venv/bin:$PATH

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

