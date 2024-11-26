from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security.api_key import APIKeyHeader, APIKey
from typing import List
import logging
import os
from google.cloud import secretmanager
from dotenv import load_dotenv
from genotools_api.models.models import GenoToolsParams
from genotools_api.utils.utils import download_from_gcs, construct_command, execute_genotools, upload_to_gcs

load_dotenv()


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def access_secret_version():
    client = secretmanager.SecretManagerServiceClient()
    secret_name = f"projects/776926281950/secrets/genotools-api-key/versions/latest"
    response = client.access_secret_version(name=secret_name)
    return response.payload.data.decode("UTF-8")

API_KEY = access_secret_version()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    return api_key

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
        if params.storage_type == 'gcs':
            in_base = os.path.basename(params.pfile)
            for ext in ['pgen', 'psam', 'pvar']:
                gcs_path = f'{params.pfile}.{ext}'
                local_path = f'/app/genotools_api/data/{in_base}.{ext}'
                download_from_gcs(gcs_path, local_path)
                
            params.pfile = f'/app/genotools_api/data/{in_base}'
            
            if params.ref_panel:
                ref_panel_name = os.path.basename(params.ref_panel)
                local_ref_panel_path = f'/app/genotools_api/data/{ref_panel_name}'
                
                for ext in ['bed','bim','fam']:
                    download_from_gcs(f'{params.ref_panel}.{ext}', f'{local_ref_panel_path}.{ext}')
                    
                params.ref_panel = local_ref_panel_path

            if params.ref_labels:
                ref_labels_name = os.path.basename(params.ref_labels)
                local_ref_labels_path = f'/app/genotools_api/data/{ref_labels_name}'
                download_from_gcs(params.ref_labels, local_ref_labels_path)
                params.ref_labels = local_ref_labels_path

            if params.model:
                common_snps = params.model.replace('.pkl','.common_snps')
                model_name = os.path.basename(params.model)
                common_snps_name = os.path.basename(common_snps)
                local_model_path = f'/app/genotools_api/data/{model_name}'
                local_common_snps_path = f'/app/genotools_api/data/{common_snps_name}'
                download_from_gcs(params.model, local_model_path)
                download_from_gcs(common_snps, local_common_snps_path)
                params.model = local_model_path

            gcs_out_path = params.out
            if gcs_out_path:
                out_base = os.path.basename(params.out)
                os.makedirs("/app/genotools_api/output", exist_ok=True)
                params.out = f'/app/genotools_api/output/{out_base}'
            else:
                raise ValueError("No output file provided")

        command = construct_command(params)
        print(command)
        result = execute_genotools(command, run_locally=True)

        if params.storage_type == 'gcs' and gcs_out_path:
            output_extensions = ['pgen', 'psam', 'pvar', 'json', 'outliers']
            for ext in output_extensions:
                local_file = f'{params.out}.{ext}'
                gcs_file = f'{gcs_out_path}.{ext}'
                if os.path.exists(local_file):
                    upload_to_gcs(local_file, gcs_file)

            log_files = [
                f'{params.out}_all_logs.log',
                f'{params.out}_cleaned_logs.log'
            ]
            for log_file in log_files:
                if os.path.exists(log_file):
                    gcs_log_file = os.path.join(os.path.dirname(gcs_out_path), os.path.basename(log_file))
                    upload_to_gcs(log_file, gcs_log_file)

    except ValueError as e:
        logger.error(f"ValueError: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("Unexpected error occurred")
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "message": "Job submitted",
        "command": command,
        "result": result
    }