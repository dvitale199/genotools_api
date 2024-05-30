import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions, StandardOptions, WorkerOptions
import os

class RunGenotoolsCommand(beam.DoFn):
    def process(self, element):
        import subprocess
        input_file = element['input_file']
        output_prefix = input_file.replace(".pfile", "_processed")
        
        # Construct the genotools command
        command = [
            "genotools",
            "--pfile", input_file,
            "--callrate",
            "--sex",
            "--ancestry",
            "--out", output_prefix
        ]
        
        # Execute the command
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise RuntimeError(f"Genotools command failed: {result.stderr.decode('utf-8')}")
        
        # Return the output prefix or any other result if needed
        return [output_prefix]

def run():
    options = PipelineOptions()
    google_cloud_options = options.view_as(GoogleCloudOptions)
    google_cloud_options.project = 'your-gcp-project'
    google_cloud_options.job_name = 'genotools-processing-job'
    google_cloud_options.staging_location = 'gs://your-bucket/staging'
    google_cloud_options.temp_location = 'gs://your-bucket/temp'
    options.view_as(StandardOptions).runner = 'DataflowRunner'
    
    # Specify the custom Docker image
    worker_options = options.view_as(WorkerOptions)
    worker_options.worker_harness_container_image = 'gcr.io/your-gcp-project/genotools-dataflow:latest'
    worker_options.environment_config = {"SCRIPT_TO_RUN": os.getenv("SCRIPT_TO_RUN", "run_genotools_dataflow.py")}
    
    with beam.Pipeline(options=options) as p:
        (p
         | 'CreateInput' >> beam.Create([{'input_file': 'gs://your-bucket/input.pfile'}])
         | 'RunGenotools' >> beam.ParDo(RunGenotoolsCommand())
         | 'WriteOutput' >> beam.io.WriteToText('gs://your-bucket/output', file_name_suffix='.txt'))
         
if __name__ == '__main__':
    run()