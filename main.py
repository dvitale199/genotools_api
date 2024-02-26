from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from genotools.utils import shell_do
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
async def read_root():
    return {"message": "Welcome to GenoTools"}

class GenoToolsArgs(BaseModel):
    bfile: str = None
    pfile: str = None
    vcf: str = None
    out: str = None
    full_output: bool = None
    skip_fails: bool = None
    warn: bool = None
    callrate: float = None
    sex: bool = None
    related: bool = None
    related_cutoff: float = None
    duplicated_cutoff: float = None
    prune_related: bool = None
    prune_duplicated: bool = None
    het: bool = None
    all_sample: bool = None

@app.post("/run-genotools")
async def run_genotools(args: GenoToolsArgs = Body(...)):
    command_builder = GenoToolsCommandBuilder()
    # Convert the Pydantic model to a dictionary, excluding undefined fields
    args_dict = args.model_dump(exclude_none=True)
    
    # Validate and execute the command
    response = command_builder.execute_command(**args_dict)
    
    if response["success"]:
        logger.info("Command executed successfully.")
        return {"success": True, "result": response["result"]}
    else:
        logger.error(f"Command execution failed: {response['message']}")
        raise HTTPException(status_code=400, detail=response["message"])
    

class GenoToolsCommandBuilder:

    allowed_args = [
        'bfile', 'pfile', 'vcf', 'out', 'full_output', 'skip_fails', 'warn',
        'callrate', 'sex', 'related', 'related_cutoff', 'duplicated_cutoff',
        'prune_related', 'prune_duplicated', 'het', 'all_sample'
    ]
        
    def __init__(self):
        self.base_command = "genotools"

    def build_command(self, **kwargs):
        """
        Builds a command line string for GenoTools from given keyword arguments.
        All arguments are optional, and only those provided will be included in the command.
        
        :param kwargs: Key-value pairs of command line arguments and their values.
                       Arguments are optional. For flags without explicit values, use a boolean True.
                       If an argument is not provided, it will not be included in the command.
        :return: A string representing the command line to execute.
        """
        args = []
        for key, value in kwargs.items():
            if key.startswith('_'):
                continue  # Skip internal or private arguments

            arg_name = f"--{key.replace('_', '-')}"  # Convert underscores to hyphens for CLI
            
            if isinstance(value, bool):
                if value:  # Only add flag if True
                    args.append(arg_name)
            else:
                args.append(f"{arg_name} {value}")
        return f"{self.base_command} {' '.join(args)}"
    
    def validate_input(self, **kwargs):
        """
        Validates the input arguments against the allowed list.
        Returns (True, "") if all arguments are valid, or (False, "error message") otherwise.
        """
        for key in kwargs.keys():
            if key not in self.allowed_args:
                return False, f"Invalid argument: {key}"
        return True, ""
    

    def execute_command(self, **kwargs):
        """
        Validates the input arguments, builds the command line string,
        and executes the command using the shell_do function from genotools.utils.

        :param kwargs: Key-value pairs of command line arguments and their values.
        :return: The output of the shell_do function, typically the execution status and command output.
        """
        # Validate input arguments first
        valid, message = self.validate_input(**kwargs)
        if not valid:
            return {"success": False, "message": message}

        # Build the command
        command = self.build_command(**kwargs)
        
        # Execute the command
        try:
            result = shell_do(command, log=True, return_log=True)
            return {"success": True, "result": result}

        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return {"success": False, "message": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
