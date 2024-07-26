from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security.api_key import APIKeyHeader, APIKey
from typing import List
import logging
import os
from dotenv import load_dotenv
from genotools_api.models.models import GenoToolsParams
from genotools_api.utils.utils import download_from_gcs, construct_command, execute_genotools, upload_to_gcs

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = os.getenv("API_KEY_NAME")
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def get_api_key(api_key_header: str = Security(api_key_header)):
    logger.debug(f"Expected API key: {API_KEY}")
    logger.debug(f"Received API key: {api_key_header}")
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
        )

router = APIRouter()

@router.get("/")
async def root():
    return "Welcome to GenoTools"


@router.post("/run-genotools/")
def run_genotools(params: GenoToolsParams, api_key: APIKey = Depends(get_api_key)):
    logger.debug(f"Received payload: {params}")
    logger.debug(f"Using API key: {api_key}")
    try:
        gcs_out_path = None
        local_files = []

        if params.storage_type == 'gcs':
            for ext in ['pgen', 'psam', 'pvar']:
                in_base = os.path.basename(params.pfile)
                gcs_path = f'{params.pfile}.{ext}'
                local_path = f'/app/data/{in_base}.{ext}'
                download_from_gcs(gcs_path, local_path)
                local_files.append(local_path)

            params.pfile = f'/app/data/{in_base}'
            
            gcs_out_path = params.out
            if gcs_out_path:
                out_base = os.path.basename(params.out)
                os.makedirs("/app/output", exist_ok=True)
                params.out = f'/app/output/{out_base}'
            else:
                raise ValueError("No output file provided")

        command = construct_command(params)
        result = execute_genotools(command, run_locally=True)

        if params.storage_type == 'gcs' and gcs_out_path:
            output_files = [f'{params.out}.{ext}' for ext in ['pgen', 'psam', 'pvar', 'json', 'outliers']]
            output_files.extend([f'{params.out}_all_logs.log', f'{params.out}_cleaned_logs.log'])

            # for file in output_files:
            for ext in ['.pgen', '.psam', '.pvar', '.json', '.outliers', '_all_logs.log', '_cleaned_logs.log']:
                local_file = f'{params.out}{ext}'
                upload_to_gcs(local_file, f'{gcs_out_path}{ext}')
                local_files.append(local_file)

        for file in local_files:
            if os.path.exists(file):
                os.remove(file)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "message": "Job submitted", 
        "command": command,
        "result": result
    }
    
