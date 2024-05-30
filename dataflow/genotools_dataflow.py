import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions, StandardOptions, WorkerOptions
import subprocess
import os

class RunGenotoolsCommand(beam.DoFn):
    def __init__(self, command_template):
        self.command_template = command_template
    
    def process(self, element):
        import subprocess
        input_file = element['input_file']
        output_prefix = element['output_prefix']
        
        # Construct the command
        command = self.command_template.format(input_file=input_file, output_prefix=output_prefix).split()
        
        # Execute the command
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise RuntimeError(f"Command failed: {result.stderr.decode('utf-8')}")
        
        # Return the output prefix or any other result if needed
        return [output_prefix]

def run():
    options = PipelineOptions()
    google_cloud_options = options.view_as(GoogleCloudOptions)
    google_cloud_options.project = 'genotools'
    google_cloud_options.job_name = 'genotools-processing-job'
    google_cloud_options.staging_location = 'gs://genotools_api/staging'
    google_cloud_options.temp_location = 'gs://genotools_api/temp'
    options.view_as(StandardOptions).runner = 'DataflowRunner'
    
    # Specify the custom Docker image
    worker_options = options.view_as(WorkerOptions)
    worker_options.worker_harness_container_image = 'us-central1-docker.pkg.dev/genotools/genotools/genotools-dataflow:v0.0.1'
    
    # Retrieve the command template from environment variables or pipeline options
    command_template = os.getenv("COMMAND_TEMPLATE", "genotools --pfile {input_file} --out {output_prefix} {extra_args}")
    
    with beam.Pipeline(options=options) as p:
        (p
         | 'ReadInputFiles' >> beam.Create([
             {'input_file': 'gs://genotools_api/data/genotools_test', 'output_prefix': 'gs://genotools_api/data/CALLRATE_SEX', 'extra_args': '--callrate --sex'}
         ])
         | 'RunGenotools' >> beam.ParDo(RunGenotoolsCommand(command_template))
         | 'WriteOutput' >> beam.Map(lambda x: f"Output file: {x}")
        )

if __name__ == '__main__':
    run()