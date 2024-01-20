from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import os
import shutil
from tempfile import TemporaryDirectory
# from google.cloud import batch_v1
from genotools.utils import shell_do
import json
import re
import logging

from pydantic import BaseModel, Field
from typing import Optional, Dict, List

# batch_client = batch_v1.BatchServiceClient()
app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
async def read_root():
    return {"message": "Welcome to GenoTools"}


class GenotoolsInput(BaseModel):
    geno_path: str
    out_path: str
    ref_path: str
    ref_labels_path: str
    model_file_path: str


@app.post("/run-genotools/") #, response_model=dict)
async def run_genotools(input_data: GenotoolsInput):
    geno_path = input_data.geno_path
    out_path = input_data.out_path
    ref_path = input_data.ref_path
    ref_labels_path = input_data.ref_labels_path
    model_path = input_data.model_file_path

    file_extensions = ['.pgen', '.pvar', '.psam']
    file_paths = {ext: f"{geno_path}{ext}" for ext in file_extensions}

    # Check if all files exist - add more checks later
    for ext, path in file_paths.items():
        if not os.path.isfile(path):
            raise HTTPException(status_code=404, detail=f"File not found: {path}")
        
    output = run_genotools_command(geno_path, out_path, ref_path, ref_labels_path, model_path)
    # parsed_output = parse_log(output)
    # response = ResponseData(**parsed_output)
    # print(response.model_dump_json(indent=4))

    return output

def run_genotools_command(filename_prefix, out_path, ref_path, ref_labels_path, model_path):
    command = (
        f"genotools --pfile {filename_prefix} "
        f"--out {out_path} "
        f"--ancestry "

        f"--ref_panel {ref_path} "
        f"--ref_labels {ref_labels_path} "
        f"--all_sample "
        f"--all_variant "
        f"--model {model_path}"
    )

    # process = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process = shell_do(command, log=True, return_log=True)
    # parsed_log = parse_log(process)
    # logger.info(json.dumps(parsed_log, indent=4))
    return process


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
