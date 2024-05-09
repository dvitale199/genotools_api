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
    related: bool = None
    related_cutoff: float = None
    duplicated_cutoff: float = None
    prune_related: bool = None
    prune_duplicated: bool = None
    het: Optional[bool] = None
    all_sample: bool = None
    maf: Optional[float] = None
    storage_type: str = 'local'


@router.post("/run-genotools/")
def run_genotools(params: GenoToolsParams):
    params.pfile = expand_path(params.pfile) if params.pfile else None
    params.out = expand_path(params.out) if params.out else None
    command = "genotools"
    if params.callrate is not None:
        command += f" --callrate {params.callrate}"
    if params.sex:
        command += " --sex"
    if params.het:
        command += " --het"
    if params.maf is not None:
        command += f" --maf {params.maf}"
    
    if params.pfile:
        geno_path = params.pfile
        file_argstring = f" --pfile {geno_path}"
        command += file_argstring
    elif params.bfile:
        geno_path = params.bfile
        file_argstring = f" --bfile {geno_path}"
        command += file_argstring
    elif params.vcf:
        geno_path = params.vcf
        file_argstring = f" --vcf {geno_path}"
        command += file_argstring
    else:
        return {"message": "No geno file provided"}

    if params.out:
        command += f" --out {params.out}"
    else:
        return {"message": "No output file provided"}

    # placeholder for handle calling kubernetes to run this command in a job
    execute_genotools(command, run_locally=True)
    print(command)
    return {
        "message": "Job submitted", 
        "command": command
        # "result:": result
        }


def execute_genotools(command: str, run_locally: bool = True):
    """
    Executes the genotools command.
    
    Args:
    - command (str): The command to execute.
    - run_locally (bool): If True, the command is executed locally using shell_do.
      If False, the command is prepared for execution in a GKE cluster (method to be implemented).
    
    Returns:
    - dict: A dictionary with either the output of the command or an error message.
    """
    if run_locally:
        return shell_do(command, log=True, return_log=True)
        # shell_do(command)
    else:
        # Placeholder for GKE cluster execution method
        return {"message": "GKE execution method to be implemented"}


def expand_path(path: str) -> str:
    """Expand the user path."""
    return os.path.expanduser(path)

# def create_payload(**kwargs):
#     # Create a dictionary only with the parameters provided
#     return {key: value for key, value in kwargs.items() if value is not None}