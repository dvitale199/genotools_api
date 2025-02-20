#!/usr/bin/env python

import requests
import json
import pandas as pd
from requests.exceptions import HTTPError

#storage_type": {"gcs" or "local"}

# d = {"storage_type": "local", "pfile": "syed-test/input/GP2_merge_AAPDGC", "out": "test1/GP2_merge_AAPDGC", "skip_fails":True, "ref_panel":"ref/ref_panel/1kg_30x_hgdp_ashk_ref_panel","ref_labels":"ref/ref_panel/1kg_30x_hgdp_ashk_ref_panel_labels.txt","model":"ref/models/python3_11/GP2_merge_release6_NOVEMBER_ready_genotools_qc_umap_linearsvc_ancestry_model.pkl", "ancestry":True, "sex":True, "het":True, "related":True}

d = {"email":"syed@datatecnica.com", "storage_type": "local", "pfile": "syed-test/input/GP2_merge_AAPDGC", "out": "syed-test/output/test4", "skip_fails":True, "ref_panel":"ref/ref_panel/1kg_30x_hgdp_ashk_ref_panel","ref_labels":"ref/ref_panel/1kg_30x_hgdp_ashk_ref_panel_labels.txt","model":"ref/models/python3_11/GP2_merge_release6_NOVEMBER_ready_genotools_qc_umap_linearsvc_ancestry_model.pkl", "callrate":.01}

# d = {"storage_type": "local", "pfile": "GP2_r9_pruned", "out": "test1/gp2_r9_all_3", "skip_fails":True, "ref_panel":"ref/ref_panel/1kg_30x_hgdp_ashk_ref_panel","ref_labels":"ref/ref_panel/1kg_30x_hgdp_ashk_ref_panel_labels.txt","model":"ref/models/python3_11/GP2_merge_release6_NOVEMBER_ready_genotools_qc_umap_linearsvc_ancestry_model.pkl", "all_sample":True, "all_variant":True, "ancestry":True}

# Headers with the API key
headers = {
    "X-API-KEY": "3hHAx2FG9U5WS0yjjHbq6MMlMHc9LIQnQfLHX0edwGvidA-wtV",
    "Content-Type": "application/json"
}
#k8s cluster link
# link="https://syed-genotools-test-email-776926281950.europe-west4.run.app/run-genotools/" 
link="http://34.36.122.207/run-genotools/" 
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

