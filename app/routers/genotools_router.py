from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from genotools.utils import shell_do
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


def execute_genotools(command: str, run_locally: bool = True):

    if run_locally:
        return shell_do(command, log=True, return_log=True)
        # shell_do(command)
    else:
        # Placeholder for GKE cluster execution method
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
        command = construct_command(params)
    except ValueError as e:
        return {"message": str(e)}

    if params.storage_type == 'gcs':
        pass
        # placeholder for handle calling kubernetes to run this command in a job
    
    if params.storage_type == 'local':
        result = execute_genotools(command, run_locally=True)
        # return command
    
    # formatted_result = format_result(result)
    # return result
    return {
        "message": "Job submitted", 
        "command": command,
        "result": result
    }

