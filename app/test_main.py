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

# post
# url = 'https://genotools.uc.r.appspot.com/run-genotools/'
# # payload = {
# #     "pfile": "/app/genotools_api/data/test_data/genotools_test",
# #     "out": "/app/genotools_api/data/test_data/CALLRATE_SEX_TEST",
# #     "callrate": 0.5,
# #     "sex": True
# # }
# payload = {
#     "pfile": "gs://genotools_api/data/genotools_test",
#     "out": "gs://genotools_api/data/TEST2",
#     "callrate": 0.5,
#     "sex": True,
#     "storage_type": 'gcs'
# }

# response = requests.post(url, json=payload)
# print(response)
# try:
#     response_json = response.json()
#     print(response_json['message'])
#     print(response_json['command'])
#     print(response_json['result'])
# except requests.exceptions.JSONDecodeError:
#     print("Response content is not valid JSON")
#     print(response.text)



import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account

# Path to your service account key file
SERVICE_ACCOUNT_FILE = '/app/genotools_api/.secrets/genotools-2f2e43058216.json'
IAP_CLIENT_ID = '143035444378-avffc25rdaenp4ajs3ujst0e482vq6nn.apps.googleusercontent.com'

# Obtain an OpenID Connect token from the service account credentials
credentials = service_account.IDTokenCredentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    target_audience=IAP_CLIENT_ID
)

# Refresh the token to get a valid ID token
credentials.refresh(Request())
token = credentials.token

# Define the endpoint URL and payload
url = 'https://genotools.uc.r.appspot.com/run-genotools/'
payload = {
    "pfile": "gs://genotools_api/data/genotools_test",
    "out": "gs://genotools_api/data/TEST2",
    "callrate": 0.5,
    "sex": True,
    "storage_type": 'gcs'
}

# Make the authenticated request
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
response = requests.post(url, json=payload, headers=headers)

# Print the response
try:
    print(response.json())
except requests.exceptions.JSONDecodeError:
    print("Error: Could not decode JSON response.")
    print(response.text)