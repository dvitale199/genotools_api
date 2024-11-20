import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = 'http://0.0.0.0:8080/run-genotools/'
payload = {
    "pfile": "gs://syed_testing/GP2_merge_AAPDGC",
    "out": "gs://syed_testing/res/dan_test",
    "callrate": 0.5,
    "sex": True,
    "storage_type": "gcs"
}

headers = {
    "X-API-KEY": "test_key",  # Updated header name
    "Content-Type": "application/json"
}
# headers = {
#     "Authorization": "test_key",
#     "Content-Type": "application/json"
# }

response = requests.post(url, json=payload, headers=headers)

print(response.status_code)
print(response.json())
