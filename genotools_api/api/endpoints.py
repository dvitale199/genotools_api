from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks
from fastapi.security.api_key import APIKeyHeader, APIKey
from typing import List
import logging
import os
from google.cloud import secretmanager
from dotenv import load_dotenv
from genotools_api.models.models import GenoToolsParams
from genotools_api.utils.utils import download_from_gcs, construct_command, execute_genotools, upload_to_gcs
from time import sleep

#This section sends email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from datetime import datetime

subject_submitted = "Job Submission Confirmstion"
subject_completed = "Job Completion Confirmstion"
body_submitted = 'You job has been submitted. You will receive an eamil upton job completion as well. \n You can now exit this terminal by pressing Ctrl+C.'
body_completed = 'You job has been completed, Please check logs for details.'
sender_email = "si11080772@gmail.com"
password = "qgetcdycqfkqpiaq"
# recipient = "islamuddinn@yahoo.com"

# import asyncio


load_dotenv()


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def send_email(subject, body, sender_email, password, recipient_email):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    text = msg.as_string()
    server.sendmail(sender_email, recipient_email, text)
    server.quit()


# def access_secret_version():
#     client = secretmanager.SecretManagerServiceClient()
#     secret_name = f"projects/776926281950/secrets/genotools-api-key/versions/latest"
#     response = client.access_secret_version(name=secret_name)
#     return response.payload.data.decode("UTF-8")

# API_KEY = access_secret_version()

#Using this method for now, will get from secret manager later.
# API_KEY = os.environ.get("API_TOKEN")

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    return api_key

router = APIRouter()


def background_task(command, recipient):
    """
    Simulates a long-running background task.
    """
    try:    
        logger.info(f"Starting background task")
        result = execute_genotools(command, run_locally=True)
        # sleep(60)
        send_email(subject_completed, body_completed+f"\n\nJob ID: {os.getpid()} - Completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"+"\n\nSubmission Command: "+command+"\n\nResults: "+result, sender_email, password, recipient)
        logger.info(f"Completed background task and Email Sent")
    except Exception as e:
        logger.error(f"Error Submitting background task: {e}")
        send_email(subject_completed, body_completed+f"\n\nJob ID: {os.getpid()} - Fsiled at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"+"\n\nSubmission Command: "+command+"\n\Error: "+{e}, sender_email, password, recipient)


@router.get("/")
async def root():
    return "Welcome to GenoTools"

# @router.post("/run-genotools/",dependencies=[Depends(get_api_key)])
@router.post("/run-genotools/")
# def run_genotools(params: GenoToolsParams, api_key: APIKey = Depends(get_api_key)):
async def run_genotools(params: GenoToolsParams, background_tasks: BackgroundTasks):#, api_key: APIKey = Depends(get_api_key)):    
    logger.debug(f"Received payload: {params}")
    recipient = params.email
    # logger.debug(f"Using API key: {api_key}")
    # if params.storage_type == 'gcs':    
    #     try:
    #         gcs_out_path = None
    #         if params.storage_type == 'gcs':
    #             in_base = os.path.basename(params.pfile)
    #             for ext in ['pgen', 'psam', 'pvar']:
    #                 gcs_path = f'{params.pfile}.{ext}'
    #                 local_path = f'/app/genotools_api/data/{in_base}.{ext}'
    #                 download_from_gcs(gcs_path, local_path)
                    
    #             params.pfile = f'/app/genotools_api/data/{in_base}'
                
    #             if params.ref_panel:
    #                 ref_panel_name = os.path.basename(params.ref_panel)
    #                 local_ref_panel_path = f'/app/genotools_api/data/{ref_panel_name}'
                    
    #                 for ext in ['bed','bim','fam']:
    #                     download_from_gcs(f'{params.ref_panel}.{ext}', f'{local_ref_panel_path}.{ext}')
                        
    #                 params.ref_panel = local_ref_panel_path

    #             if params.ref_labels:
    #                 ref_labels_name = os.path.basename(params.ref_labels)
    #                 local_ref_labels_path = f'/app/genotools_api/data/{ref_labels_name}'
    #                 download_from_gcs(params.ref_labels, local_ref_labels_path)
    #                 params.ref_labels = local_ref_labels_path

    #             if params.model:
    #                 common_snps = params.model.replace('.pkl','.common_snps')
    #                 model_name = os.path.basename(params.model)
    #                 common_snps_name = os.path.basename(common_snps)
    #                 local_model_path = f'/app/genotools_api/data/{model_name}'
    #                 local_common_snps_path = f'/app/genotools_api/data/{common_snps_name}'
    #                 download_from_gcs(params.model, local_model_path)
    #                 download_from_gcs(common_snps, local_common_snps_path)
    #                 params.model = local_model_path
    #             else:
    #                 params.model = None
    #                 print('TEST')

    #             gcs_out_path = params.out
    #             if gcs_out_path:
    #                 out_base = os.path.basename(params.out)
    #                 os.makedirs("/app/genotools_api/output", exist_ok=True)
    #                 params.out = f'/app/genotools_api/output/{out_base}'
    #             else:
    #                 raise ValueError("No output file provided")

    #         command = construct_command(params)
    #         print(command)
    #         result = execute_genotools(command, run_locally=True)

    #         if params.storage_type == 'gcs' and gcs_out_path:
    #             output_extensions = ['pgen', 'psam', 'pvar', 'json', 'outliers']
    #             for ext in output_extensions:
    #                 local_file = f'{params.out}.{ext}'
    #                 gcs_file = f'{gcs_out_path}.{ext}'
    #                 if os.path.exists(local_file):
    #                     upload_to_gcs(local_file, gcs_file)

    #             log_files = [
    #                 f'{params.out}_all_logs.log',
    #                 f'{params.out}_cleaned_logs.log'
    #             ]
    #             for log_file in log_files:
    #                 if os.path.exists(log_file):
    #                     gcs_log_file = os.path.join(os.path.dirname(gcs_out_path), os.path.basename(log_file))
    #                     upload_to_gcs(log_file, gcs_log_file)

    #     except ValueError as e:
    #         logger.error(f"ValueError: {e}")
    #         raise HTTPException(status_code=400, detail=str(e))
    #     except Exception as e:
    #         logger.exception("Unexpected error occurred")
    #         raise HTTPException(status_code=500, detail=str(e))
    #     return {
    #         "message": "Job submitted",
    #         "command": command,
    #         "result": result
    #     }        
    # else:
        # try:
            # print('working')
    params.pfile = f'/app/genotools_api/data/{params.pfile}'
    params.ref_panel = f'/app/genotools_api/data/{params.ref_panel}'
    params.ref_labels = f'/app/genotools_api/data/{params.ref_labels}'
    params.model = f'/app/genotools_api/data/{params.model}'
    #output paths
    # try:
    os.makedirs(f"/app/genotools_api/data/{'/'.join(params.out.split('/')[:-1])}/", exist_ok=True)
    params.out = f'/app/genotools_api/data/{params.out}'
    # except:
    #     print(f'Failed to create Folder: {'/'.join(params.out.split("/")[:-1])}')
    # params.out = f'/app/genotools_api/data/output_gke/{params.out}'
    

    command = construct_command(params)
    # print(f"Final command: {command}")
    # result = execute_genotools(command, run_locally=True)
    # print(f"result: {result}")
    # execute_genotools(command, run_locally=True)
    # asyncio.run(call_exectuion(command, run_locally=True))

    send_email(subject_submitted, body_submitted+f"\n\nJob ID: {os.getpid()} - Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"+"\n\nSubmission Command: "+command, sender_email, password, recipient)      
    # Add the background task to the queue
    background_tasks.add_task(background_task, command, recipient)
    # result = execute_genotools(command, run_locally=True)
    # send_email(subject_completed, body_completed+f"\n\nJob ID: {os.getpid()} - Completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"+"\n\nSubmission Command: "+command+"\n\nResults: "+result, sender_email, password, recipient)

        
    # except ValueError as e:
    #     logger.error(f"ValueError: {e}")
    #     raise HTTPException(status_code=400, detail=str(e))
    # except Exception as e:
    #     logger.exception("Unexpected error occurred")
    #     raise HTTPException(status_code=500, detail=str(e))  
    return {
        "message": "Job submitted",
        "command": command
        # "result": result
        }