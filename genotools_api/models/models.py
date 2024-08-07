from pydantic import BaseModel
from typing import Optional

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