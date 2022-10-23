#!/bin/bash

docker build -t inference_api .

docker system prune -f
