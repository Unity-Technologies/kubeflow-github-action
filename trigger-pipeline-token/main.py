import os
from kfp_utils import *

def main():
    logging.info(
        "Started the process to compile and upload the pipeline to kubeflow.")
    logging.info(os.getenv("INPUT_RUN_PIPELINE"))
    logging.info(os.getenv("INPUT_EXPERIMENT_NAME"))

    logging.info("Started the process to run the pipeline on kubeflow.")
    pipeline_id = os.getenv("INPUT_PIPELINE_ID")
    run_name = os.getenv("INPUT_RUN_NAME")
    pipeline_name = os.getenv("INPUT_PIPELINE_NAME")
    pipeline_version_name = os.getenv("INPUT_PIPELINE_VERSION_NAME")
    client = kfp.Client(
        host=os.getenv("INPUT_KUBEFLOW_URL"),
        existing_token=os.getenv("INPUT_ID_TOKEN"),
    )

    if os.getenv("INPUT_PIPELINE_PARAMETERS_PATH") and not str.isspace(os.getenv("INPUT_PIPELINE_PARAMETERS_PATH")):
        pipeline_parameters_path = os.getenv("INPUT_PIPELINE_PARAMETERS_PATH")
    else:
        pipeline_parameters_path = None

    if os.getenv("INPUT_PIPELINE_PARAMETERS") and not str.isspace(os.getenv("INPUT_PIPELINE_PARAMETERS")):
        pipeline_parameters = os.getenv("INPUT_PIPELINE_PARAMETERS")
    else:
        pipeline_parameters = None

    run_pipeline(pipeline_name=pipeline_name,
                 pipeline_id=pipeline_id,
                 experiment_name=os.getenv("INPUT_EXPERIMENT_NAME"),
                 client=client,
                 pipeline_parameters_path=pipeline_parameters_path,
                 pipeline_parameters=pipeline_parameters,
                 namespace=os.getenv("INPUT_PIPELINE_NAMESPACE"),
                 service_account=os.getenv("INPUT_PIPELINE_SERVICE_ACCOUNT"),
                 run_name=run_name,
                 pipeline_version_name=pipeline_version_name)


if __name__ == "__main__":
    main()
