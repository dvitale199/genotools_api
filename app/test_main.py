from fastapi.testclient import TestClient
from app.main import app  # Import the FastAPI instance
import requests
import os

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the GenoTools API!"}


def test_run_genotools():
    # Define the payload for the POST request
    payload = {
        "pfile": "pfile",
        "out": "out",
        "callrate": 0.5,
    }

    # Send POST request to the endpoint
    response = client.post("/run-genotools/", json=payload)
    
    # Check response status code
    assert response.status_code == 200
    
    # Check the response content
    assert response.json() == {
        "message": "Job submitted",
        "command": "genotools --pfile pfile --out out --callrate 0.5"
    }


# test_read_main()
# test_run_genotools()

# fire up app
# python -m uvicorn app.main:app --host 0.0.0.0 --port 8080

#post
url = 'http://localhost:8080/run-genotools/'
# payload = {
#     "pfile": "/app/genotools_api/data/test_data/genotools_test",
#     "out": "/app/genotools_api/data/test_data/CALLRATE_SEX_TEST",
#     "callrate": 0.5,
#     "sex": True
# }
payload = {
    "pfile": "gs://genotools_api/data/genotools_test",
    "out": "gs://genotools_api/data/CALLRATE_SEX_TEST",
    "callrate": 0.5,
    "sex": True,
    "storage_type": 'gcs'
}

response = requests.post(url, json=payload)
print(response.json())
# try:
#     response_json = response.json()
#     print(response_json['message'])
#     print(response_json['command'])
#     print(response_json['result'])
# except requests.exceptions.JSONDecodeError:
#     print("Response content is not valid JSON")
#     print(response.text)