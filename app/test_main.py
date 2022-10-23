from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_single_prediction():

    test_request = {
        "text": "This is an example text",
        "n_preds": 1
    }

    response = client.post("/inference_api/single_prediction", json=test_request)
    assert response.status_code == 200
    assert len(response.json()["labels"]) == 1
    assert response.json()["labels"][0] == "Guardian"
