import requests
import os
from dotenv import load_dotenv

load_dotenv()

# local
# url = 'http://0.0.0.0:8080/run-genotools/'
# url = 'https://genotools-api-776926281950.europe-west4.run.app/run-genotools/'

# genotools \
#   --pfile /path/to/genotypes/for/qc \
#   --out /path/to/qc/output \
#   --ancestry \
#   --ref_panel /path/to/reference/panel \
#   --ref_labels /path/to/reference/ancestry/labels \
#   --all_sample \
#   --all_variant
#   --model /path/to/nba_v1/model

# payload = {
#     "pfile": "gs://syed_testing/GP2_merge_AAPDGC",
#     "out": "gs://syed_testing/res/dan_test",
#     "ancestry": True,
#     "ref_panel": "gs://syed_testing/ref/ref_panel/1kg_30x_hgdp_ashk_ref_panel",
#     "ref_labels": "gs://syed_testing/ref/ref_panel/1kg_30x_hgdp_ashk_ref_panel_labels.txt",
#     "model": "gs://syed_testing/ref/models/nba_v1/nba_v1.pkl",
#     "all_sample": True,
#     "all_variant": True,
#     "storage_type": "gcs"
# }

# payload = {
#     "pfile": "gs://syed_testing/GP2_merge_AAPDGC",
#     "out": "gs://syed_testing/res/dan_cloud_run_test",
#     "callrate": 0.5,
#     "sex": True,
#     "storage_type": "gcs"
# }

# API_KEY = os.getenv("API_KEY")
# API_KEY_NAME = os.getenv("API_KEY_NAME")

# headers = {
#     API_KEY_NAME: API_KEY,
#     "Content-Type": "application/json"
# }

# response = requests.post(url, json=payload, headers=headers)

# print(response.status_code)
# print(response.json())


url = 'https://genotools-api-776926281950.europe-west4.run.app/run-genotools/'

payload = {
    "pfile": "gs://syed_testing/GP2_merge_AAPDGC",
    "out": "gs://syed_testing/res/dan_cloud_run_test",
    "callrate": 0.5,
    "sex": True,
    "storage_type": "gcs"
}

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = os.getenv("API_KEY_NAME")

headers = {
    API_KEY_NAME: API_KEY,
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.status_code)
print(response.text)