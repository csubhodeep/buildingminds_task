# Inference API

## Description

This repository contains a simple machine learning model that can be used to predict the media outlet (e.g. New York Times) of a news article based solely on its content. 
It is based on this [Kaggle dataset](https://www.kaggle.com/snapcrack/all-the-news) containing data from several U.S. media outlets from 2016 to 2017.

It takes arbitrary text as an input and computes how likely it is that the text belongs to a specific media outlet. It was trained using Python 3.9.13 and `scikit-learn==1.1.1`. 
The accuracy of the model is not very good, but that is not important for this task.

The objective is to implement a simple API for this model.

The requirements are:
- The API accepts text input and returns a json response, including both the predicted classes and their probabilities, sorted by probability scores.
- The API should allow for batch predictions (i.e. users have the option to classify multiple input texts in a single request).
- Users should be able to control the maximum number of predictions in the json response.
- The request and response schema should be clearly defined.
- The input text, class predictions and probabilities of each request should be stored (e.g. in a simple database).
- The API should be wrapped into a docker container.

## How to run?

The following are the pre-requisites and installed in your PC:
1. Docker - 20.10.19

First, build the Docker image by running the following from the terminal
```commandline
sh build.sh
```

Second, start a container instance of the image built in the previous step by running the following command
from the terminal
```commandline
sh run.sh
```

Access the API docs on `https://0.0.0.0:8000/docs`

## How to develop?

Prepare the local dev environment by ensuring that Python - 3.9.15 is installed in your PC.

Clone into the repo, checkout a new branch and activate a virtual environment.

Install the dev-dependencies:
1. `pip==22.0.4`
```commandline
python3 -m pip install --upgrade pip==22.0.4 --require-virtualenv
```
2. `pip-tools==6.8.0`
```commandline
pip3 install pip-tools==6.8.0 --require-virtualenv
```
3. Install the rest of the third-party packages:
```commandline
pip-sync requirements/requirement-dev.txt
```


