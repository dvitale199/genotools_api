#!/usr/bin/env python

import requests
import json
import pandas as pd
from requests.exceptions import HTTPError

# storage_type": {"gcs" or "local"}

d = {"email":"syed@datatecnica.com", "storage_type": "local", "pfile": "r10_v1/GP2_r10_v1_ready_genotools", "out": "r10_v1/GP2_r10_v1_post_genotools", "skip_fails":True, "ref_panel":"ref/new_panel/ref_panel_gp2_prune_rm_underperform_pos_update","ref_labels":"ref/new_panel/ref_panel_ancestry_updated.txt","model":"ref/models/python3_11/GP2_merge_release6_NOVEMBER_ready_genotools_qc_umap_linearsvc_ancestry_model.pkl", "ancestry":True, "all_sample":True, "all_variant":True, "amr_het":True, "skip_fails":True, "full_output":True}


# Headers with the API key
headers = {
    "X-API-KEY": "3hHAx2FG9U5WS0yjjHbq6MMlMHc9LIQnQfLHX0edwGvidA-wtV",
    "Content-Type": "application/json"
}
#k8s cluster link
link="http://34.36.210.198/run-genotools/"
print(f'json.dumps(d): {json.dumps(d)}')
try:    
    r = requests.post(f"{link}", data=json.dumps(d), headers=headers)
    # r = requests.post(f"{link}", data=json.dumps(d))
    print(f'r: {r}')
    r.raise_for_status()
    res=r.json()
    print(f"res: {res}")
except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}') 