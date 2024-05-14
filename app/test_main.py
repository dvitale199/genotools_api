from fastapi.testclient import TestClient
from app.main import app  # Import the FastAPI instance
import requests

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

# payload = {
#     "pfile": "~/Desktop/Projects/genotools_api/data/test_data/genotools_test",
#     "out": "~/Desktop/Projects/genotools_api/data/test_data/CALLRATE_TEST",
#     "callrate": 0.5,
# }

# response = client.post("/run-genotools/", json=payload)

# test localhost docker client
import httpx

async def lh_submit():
    url = 'http://localhost:8080/run-genotools'
    payload = {
        "pfile": "~/Desktop/Projects/genotools_api/data/test_data/genotools_test",
        "out": "~/Desktop/Projects/genotools_api/data/test_data/CALLRATE_TEST",
        "callrate": 0.5,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        print(response.text)
        print(response.status_code)
        # Assertions can be added here as well

import asyncio
asyncio.run(lh_submit())


url = 'http://localhost:8080/run-genotools/'
payload = {
    "pfile": "/app/data/test_data/genotools_test",
    "out": "/app/data/test_data/CALLRATE_TEST",
    "callrate": 0.5,
}
import requests
response = requests.post(url, json=payload)
print(response)