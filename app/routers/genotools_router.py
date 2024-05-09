from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

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
        file_argstring = f" --pgen {geno_path}"
        command += file_argstring
    elif params.bfile:
        geno_path = params.bfile
        file_argstring = f" --bgen {geno_path}"
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


    command += f" --pgen {params.pfile} --out {params.out}"



    # placeholder for handle calling kubernetes to run this command in a job
    
    return {"message": "Job submitted", "command": command}


def create_payload(**kwargs):
    # Create a dictionary only with the parameters provided
    return {key: value for key, value in kwargs.items() if value is not None}