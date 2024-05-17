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

# fire up app
# python -m uvicorn app.main:app --host 0.0.0.0 --port 8080

#post
import requests

url = 'http://localhost:8080/run-genotools/'
payload = {
    "pfile": "/app/genotools_api/data/test_data/genotools_test",
    "out": "/app/genotools_api/data/test_data/CALLRATE_SEX_TEST",
    "callrate": 0.5,
    "sex": True
}

response = requests.post(url, json=payload)

print(response.status_code)
print(response.json()['message'])
print(response.json()['command'])
print(response.json()['result'])

# result = 'Your data has the following breakdown:\n- Genetic Sex:\n813 Females \n\n555 Males \n\n- Phenotypes:\n1166 Controls \n\n188 Cases \n\nOutput steps: sex\nRunning: callrate with input /app/genotools_api/data/test_data/genotools_test and output: /app/genotools_api/data/test_data/.vn30tpug_tmp/CALLRATE_SEX_TEST_callrate\nRunning: sex with input /app/genotools_api/data/test_data/.vn30tpug_tmp/CALLRATE_SEX_TEST_callrate and output: /app/genotools_api/data/test_data/CALLRATE_SEX_TEST\n'
# print(result)