import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions, StandardOptions, WorkerOptions
import os

class RunGenotoolsCommand(beam.DoFn):
    def __init__(self, command_template):
        self.command_template = command_template
    
    def process(self, element):
        import subprocess
        input_file = element['input_file']
        output_prefix = element['output_prefix']
        extra_args = element['extra_args']
        
        # Construct the command
        command = self.command_template.format(input_file=input_file, output_prefix=output_prefix, extra_args=extra_args).split()
        
        # Execute the command
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise RuntimeError(f"Command failed: {result.stderr.decode('utf-8')}")
        
        # Return the output prefix or any other result if needed
        return [output_prefix]

def run():
    options = PipelineOptions()
    google_cloud_options = options.view_as(GoogleCloudOptions)
    google_cloud_options.project = os.getenv('GCP_PROJECT')
    google_cloud_options.job_name = os.getenv('JOB_NAME')
    google_cloud_options.staging_location = os.getenv('STAGING_LOCATION')
    google_cloud_options.temp_location = os.getenv('TEMP_LOCATION')
    options.view_as(StandardOptions).runner = 'DataflowRunner'
    
    # Specify the custom Docker image
    worker_options = options.view_as(WorkerOptions)
    worker_options.worker_harness_container_image = os.getenv('WORKER_HARNESS_CONTAINER_IMAGE')
    
    # Command template
    command_template = os.getenv("COMMAND_TEMPLATE")
    
    # Input parameters
    input_file = os.getenv('INPUT_FILE')
    output_prefix = os.getenv('OUTPUT_PREFIX')
    extra_args = os.getenv('EXTRA_ARGS')

    # Ensure that all necessary environment variables are set
    if not all([google_cloud_options.project, google_cloud_options.job_name, google_cloud_options.staging_location,
                google_cloud_options.temp_location, worker_options.worker_harness_container_image,
                command_template, input_file, output_prefix, extra_args]):
        raise ValueError("One or more required environment variables are not set.")
    
    with beam.Pipeline(options=options) as p:
        (p
         | 'ReadInputFiles' >> beam.Create([
             {'input_file': input_file, 'output_prefix': output_prefix, 'extra_args': extra_args}
         ])
         | 'RunGenotools' >> beam.ParDo(RunGenotoolsCommand(command_template))
         | 'WriteOutput' >> beam.Map(lambda x: f"Output file: {x}")
        )

if __name__ == '__main__':
    run()