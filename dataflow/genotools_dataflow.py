import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions, StandardOptions

class CustomOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_value_provider_argument('--input_file', type=str, help='Input file path')
        parser.add_value_provider_argument('--output_prefix', type=str, help='Output prefix')
        parser.add_value_provider_argument('--extra_args', type=str, help='Extra arguments for genotools')
        parser.add_value_provider_argument('--script_to_run', type=str, help='Script to run')
        parser.add_value_provider_argument('--command_template', type=str, help='Command template')

class RunGenotoolsCommand(beam.DoFn):
    def __init__(self, command_template):
        self.command_template = command_template
    
    def process(self, element):
        import subprocess
        input_file = element['input_file']
        output_prefix = element['output_prefix']
        extra_args = element['extra_args']
        
        # Construct the command
        command = self.command_template.get().format(input_file=input_file, output_prefix=output_prefix, extra_args=extra_args).split()
        
        # Execute the command
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise RuntimeError(f"Command failed: {result.stderr.decode('utf-8')}")
        
        # Return the output prefix or any other result if needed
        return [output_prefix]

def run():
    options = PipelineOptions()
    custom_options = options.view_as(CustomOptions)
    google_cloud_options = options.view_as(GoogleCloudOptions)
    google_cloud_options.project = custom_options.project
    google_cloud_options.job_name = custom_options.job_name
    google_cloud_options.staging_location = custom_options.staging_location
    google_cloud_options.temp_location = custom_options.temp_location
    options.view_as(StandardOptions).runner = 'DataflowRunner'
    
    # Command template
    command_template = custom_options.command_template
    
    with beam.Pipeline(options=options) as p:
        (p
         | 'ReadInputFiles' >> beam.Create([
             {'input_file': custom_options.input_file, 'output_prefix': custom_options.output_prefix, 'extra_args': custom_options.extra_args}
         ])
         | 'RunGenotools' >> beam.ParDo(RunGenotoolsCommand(command_template))
         | 'WriteOutput' >> beam.Map(lambda x: f"Output file: {x}")
        )

if __name__ == '__main__':
    run()