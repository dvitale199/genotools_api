from fastapi.testclient import TestClient
from app.main import app  # Import the FastAPI instance

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the GenoTools API!"}


def test_run_genotools():
    # Define the payload for the POST request
    payload = {
        "callrate": 0.5,
        "sex": True,
        "het": False,
        "maf": 0.1
    }

    # Send POST request to the endpoint
    response = client.post("/run-genotools/", json=payload)
    
    # Check response status code
    assert response.status_code == 200
    
    # Check the response content
    assert response.json() == {
        "message": "Job submitted",
        "command": "genotools --callrate 0.5 --sex --maf 0.1"
    }


test_read_main()
test_run_genotools()

payload = {
        "callrate": 0.5,
        "sex": True,
        "het": False,
        "maf": 0.1
    }

# Send POST request to the endpoint
response = client.post("/run-genotools/", json=payload)