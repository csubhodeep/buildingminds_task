#!/bin/bash

if [ ! -d "data" ]; then
  mkdir "data"
fi

if [ ! -d "logs" ]; then
  mkdir "logs"
fi


docker rm inference_api_service -f

docker run -d \
--name inference_api_service \
-v ${PWD}/logs:/code/logs \
-v ${PWD}/data:/code/data \
-p 8000:80 -d \
inference_api

docker container prune -f
