import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = 'http://0.0.0.0:8080/run-genotools/'
payload = {
    "pfile": "gs://genotools_api/data/genotools_test",
    "out": "gs://genotools_api/data/TEST",
    "callrate": 0.5,
    "sex": True,
    "storage_type": "gcs"
}

# headers = {
#     "Authorization": os.getenv("API_KEY"),
#     "Content-Type": "application/json"
# }
headers = {
    "Authorization": "test_key",
    "Content-Type": "application/json"
}
response = requests.post(url, json=payload, headers=headers)

print(response.status_code)
print(response.json())