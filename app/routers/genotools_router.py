from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from genotools.utils import shell_do
from google.cloud import storage
import os

router = APIRouter()

class GenoToolsParams(BaseModel):
    bfile: Optional[str] = None
    pfile: Optional[str] = None
    vcf: Optional[str] = None
    out: Optional[str] = None
    full_output: Optional[bool] = None
    skip_fails: Optional[bool] = None
    warn: Optional[bool] = None
    callrate: Optional[float] = None
    sex: Optional[bool] = None
    related: Optional[bool] = None
    related_cutoff: Optional[float] = None
    duplicated_cutoff: Optional[float] = None
    prune_related: Optional[bool] = None
    prune_duplicated: Optional[bool] = None
    het: Optional[bool] = None
    all_sample: Optional[bool] = None
    all_variant: Optional[bool] = None
    maf: Optional[float] = None
    ancestry: Optional[bool] = None
    ref_panel: Optional[str] = None
    ancestry_labels: Optional[str] = None
    model: Optional[str] = None
    storage_type: str = 'local'


def download_from_gcs(gcs_path, local_path):
    storage_client = storage.Client()
    bucket_name, blob_name = gcs_path.replace("gs://", "").split("/", 1)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    blob.download_to_filename(local_path)
    return local_path


def upload_to_gcs(local_path, gcs_path):
    storage_client = storage.Client()
    bucket_name, blob_name = gcs_path.replace("gs://", "").split("/", 1)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(local_path)


def execute_genotools(command: str, run_locally: bool = True):

    if run_locally:
        return shell_do(command, log=True, return_log=True)
    else:
        return {"message": "GKE execution method to be implemented"}


def expand_path(path: str) -> str:
    """Expand the user path."""
    return os.path.expanduser(path)


def construct_command(params: GenoToolsParams) -> str:
    command = "genotools"
    
    # Mapping options to their respective values in params
    options_with_values = {
        "--callrate": params.callrate,
        "--related_cutoff": params.related_cutoff,
        "--duplicated_cutoff": params.duplicated_cutoff,
        "--maf": params.maf,
        "--ref_panel": params.ref_panel,
        "--ancestry_labels": params.ancestry_labels,
        "--model": params.model
    }

    flags = [
        ("--full_output", params.full_output),
        ("--skip_fails", params.skip_fails),
        ("--warn", params.warn),
        ("--sex", params.sex),
        ("--related", params.related),
        ("--prune_related", params.prune_related),
        ("--prune_duplicated", params.prune_duplicated),
        ("--het", params.het),
        ("--all_sample", params.all_sample),
        ("--all_variant", params.all_variant),
        ("--ancestry", params.ancestry)
    ]

    for option, value in options_with_values.items():
        if value is not None:
            command += f" {option} {value}"
    
    for flag, value in flags:
        if value:
            command += f" {flag}"

    if params.pfile:
        command += f" --pfile {expand_path(params.pfile)}"
    elif params.bfile:
        command += f" --bfile {expand_path(params.bfile)}"
    elif params.vcf:
        command += f" --vcf {expand_path(params.vcf)}"
    else:
        raise ValueError("No geno file provided")

    if params.out:
        command += f" --out {expand_path(params.out)}"
    else:
        raise ValueError("No output file provided")

    return command


@router.post("/run-genotools/")
def run_genotools(params: GenoToolsParams):
    try:
        gcs_out_path = None
        if params.storage_type == 'gcs':
            for ext in ['pgen', 'psam', 'pvar']:
                in_base = os.path.basename(params.pfile)
                gcs_path = f'{params.pfile}.{ext}'
                local_path = f'/app/genotools_api/data/{in_base}.{ext}'
                download_from_gcs(gcs_path, local_path)

            params.pfile = f'/app/genotools_api/data/{in_base}'
            
            gcs_out_path = params.out
            if gcs_out_path:
                out_base = os.path.basename(params.out)
                os.makedirs("/app/genotools_api/output", exist_ok=True)
                params.out = f'/app/genotools_api/output/{out_base}'
            else:
                raise ValueError("No output file provided")

        command = construct_command(params)
        result = execute_genotools(command, run_locally=True)

        if params.storage_type == 'gcs' and gcs_out_path:
            for ext in ['pgen', 'psam', 'pvar','json','outliers']:
                upload_to_gcs(f'{params.out}.{ext}', f'{gcs_out_path}.{ext}')

            upload_to_gcs(f'{params.out}_all_logs.log', f'{gcs_out_path}_all_logs.log')
            upload_to_gcs(f'{params.out}_cleaned_logs.log', f'{gcs_out_path}_cleaned_logs.log')

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "message": "Job submitted", 
        "command": command,
        "result": result
    }