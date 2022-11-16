import os
import yaml
import kfp
import kfp.compiler as compiler
import importlib.util
import logging
import sys
from datetime import datetime


logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def load_function(pipeline_function_name: str, full_path_to_pipeline: str) -> object:
    """Function to load python function from filepath and filename

    Arguments:
        pipeline_function_name {str} -- The name of the pipeline function
        full_path_to_pipeline {str} -- The full path name including the filename of the python file that 
                                        describes the pipeline you want to run on Kubeflow

    Returns:
        object -- [description]
    """
    logging.info(
        f"Loading the pipeline function from: {full_path_to_pipeline}")
    logging.info(
        f"The name of the pipeline function is: {pipeline_function_name}")
    sys.path.append(os.path.split(full_path_to_pipeline)[0])
    spec = importlib.util.spec_from_file_location(
        pipeline_function_name, full_path_to_pipeline)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    pipeline_func = getattr(foo, pipeline_function_name)
    logging.info("Succesfully loaded the pipeline function.")
    return pipeline_func


def pipeline_compile(pipeline_function: object, v2_compatible: bool = False) -> str:
    """Function to compile pipeline. The pipeline is compiled to a zip file. 

    Arguments:
        pipeline_func {object} -- The kubeflow pipeline function
        v2_compatible {bool} --  Whether to compile in V2_COMPATIBLE mode

    Returns:
        str -- The name of the compiled kubeflow pipeline
    """
    pipeline_name_zip = pipeline_function.__name__ + ".zip"
    if v2_compatible:
        c = compiler.Compiler(mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE)
    else:
        c = compiler.Compiler()
    c.compile(pipeline_function, pipeline_name_zip)
    logging.info("The pipeline function is compiled.")
    return pipeline_name_zip

def upload_pipeline_by_token(pipeline_name_zip: str,
                    pipeline_name: str,
                    kubeflow_url: str,
                    existing_token: str,
                    pipeline_version_name: str = None):
    """Function to upload pipeline to kubeflow. 

    Arguments:
        pipeline_name_zip {str} -- The name of the compiled pipeline
        pipeline_name {str} -- The name of the pipeline. This will be the name in the kubeflow UI.
        kubeflow_url {str} -- URL of the Kubeflow server
        existing_token {str} -- ID token for auth to kfp
        pipeline_version_name {str} -- The name of the pipeline version. This will be the name of
            this version in the kubeflow UI.
    """
    client = kfp.Client(
        host=kubeflow_url,
        existing_token=existing_token,
    )
    if pipeline_version_name:
        try:
            pipeline_id = find_pipeline_id(pipeline_name, client)
        except ValueError:
            response = client.upload_pipeline(
                pipeline_package_path=pipeline_name_zip,
                pipeline_name=pipeline_name)
            pipeline_id = response.id
        client.upload_pipeline_version(
            pipeline_package_path=pipeline_name_zip,
            pipeline_version_name=pipeline_version_name,
            pipeline_id=pipeline_id)
    else:
        client.upload_pipeline(
            pipeline_package_path=pipeline_name_zip,
            pipeline_name=pipeline_name)
    return client

def upload_pipeline(pipeline_name_zip: str,
                    pipeline_name: str,
                    kubeflow_url: str,
                    client_id: str,
                    pipeline_version_name: str = None):
    """Function to upload pipeline to kubeflow. 

    Arguments:
        pipeline_name_zip {str} -- The name of the compiled pipeline
        pipeline_name {str} -- The name of the pipeline. This will be the name in the kubeflow UI.
        kubeflow_url {str} -- URL of the Kubeflow server
        client_id {str} -- IAP Client ID for auth
        pipeline_version_name {str} -- The name of the pipeline version. This will be the name of
            this version in the kubeflow UI.
    """
    client = kfp.Client(
        host=kubeflow_url,
        client_id=client_id,
    )
    if pipeline_version_name:
        try:
            pipeline_id = find_pipeline_id(pipeline_name, client)
        except ValueError:
            response = client.upload_pipeline(
                pipeline_package_path=pipeline_name_zip,
                pipeline_name=pipeline_name)
            pipeline_id = response.id
        client.upload_pipeline_version(
            pipeline_package_path=pipeline_name_zip,
            pipeline_version_name=pipeline_version_name,
            pipeline_id=pipeline_id)
    else:
        client.upload_pipeline(
            pipeline_package_path=pipeline_name_zip,
            pipeline_name=pipeline_name)
    return client


def find_pipeline_id(pipeline_name: str,
                     client: kfp.Client,
                     page_size: str = 100,
                     page_token: str = "") -> str:
    """Function to find the pipeline id of a pipeline. 

    Arguments:
        pipeline_name {str} -- The name of the pipeline of interest
        client {kfp.Client} -- The kfp client
        page_size {str} -- The number of pipelines to collect a each API request

    Keyword Arguments:
        page_token {str} -- The page token to use for the API request (default: {" "})

    Returns:
        [type] -- The pipeline id. If None no match
    """
    while True:
        pipelines = client.list_pipelines(
            page_size=page_size, page_token=page_token)
        logging.info(f"Searching for pipeline name {pipeline_name}")
        for pipeline in pipelines.pipelines:
            if pipeline.name == pipeline_name:
                logging.info(f"The pipeline id is: {pipeline.id}")
                return pipeline.id
        # Start need to know where to do next itteration from
        page_token = pipelines.next_page_token
        # If no next token break
        if not page_token:
            raise ValueError("Failed to find pipeline with the name: {}".format(
                pipeline_name))


def find_pipeline_version_id(pipeline_id: str,
                             version_name: str,
                             client: kfp.Client,
                             page_size: str = 100,
                             page_token: str = "") -> str:
    """Function to find the pipeline id of a pipeline.

    Arguments:
        pipeline_id {str} -- The ID of the pipeline of interest
        version_name -- The name of the version of interest
        client {kfp.Client} -- The kfp client
        page_size {str} -- The number of pipeline versions to collect a each API request

    Keyword Arguments:
        page_token {str} -- The page token to use for the API request (default: {" "})

    Returns:
        [type] -- The pipeline version id. If None no match
    """
    while True:
        logging.info(f"Retrieving versions for pipeline ID {pipeline_id}")
        versions = client.list_pipeline_versions(
            pipeline_id=pipeline_id, page_size=page_size, page_token=page_token)
        for version in versions.versions:
            if version.name == version_name:
                logging.info(f"The pipeline version id is: {version.id}")
                return version.id
        # Start need to know where to do next itteration from
        page_token = versions.next_page_token
        # If no next token break
        if not page_token:
            raise ValueError("Failed to find pipeline version with the name: {}".format(
                version_name))


def find_experiment_id(experiment_name: str,
                       namespace: str,
                       client: kfp.Client,
                       page_size: int = 100,
                       page_token: str = "") -> str:
    """Function to return the experiment id

    Arguments:
        experiment_name {str} -- The experiment name
        namespace {str} -- The namespace to search for the experiment
        client {kfp.Client} -- The kfp client
        page_size {str} -- The number of experiments to collect a each API request

    Keyword Arguments:
        page_token {str} -- The page token to use for the API request (default: {" "})

    Returns:
        str -- The experiment id
    """
    while True:
        experiments = client.list_experiments(
            page_size=page_size, page_token=page_token, namespace=namespace)
        for experiment in experiments.experiments:
            if experiment.name == experiment_name:
                logging.info("Succesfully collected the experiment id")
                return experiment.id
        # Start need to know where to do next itteration from
        page_token = experiments.next_page_token
        # If no next tooken break
        if not page_token:
            raise ValueError("Failed to find experiment with the name: {}".format(
                experiment_name))


def read_pipeline_params(pipeline_parameters_path: str) -> dict:
    """Function to read pipeline parameters from YAML

    Arguments:
        pipeline_parameters_path {str} -- Path to YAML file containing set parameters
    Returns:
        dict -- Dictionary containing the parameters
    """
    pipeline_params = {}
    with open(pipeline_parameters_path) as f:
        try:
            pipeline_params = yaml.safe_load(f)
            logging.info(f"The pipeline parameters is: {pipeline_params}")
        except yaml.YAMLError as exc:
            logging.info("The yaml parameters could not be loaded correctly.")
            raise ValueError(
                "The yaml parameters could not be loaded correctly.")
        logging.info(f"The parameters are: {pipeline_params}")
    return pipeline_params


def parse_raw_params(pipeline_params: str) -> dict:
    """Function to parse raw YAML string into parameters dict

    Arguments:
        pipeline_params {str} -- Raw YAML string containing set parameters
    Returns:
        dict -- Dictionary containing the parameters
    """
    logging.info(f"Raw params string: {pipeline_params}")
    result = yaml.safe_load(pipeline_params)
    logging.info(f"Parsing result: {result}")
    return result

def run_pipeline(client: kfp.Client,
                 pipeline_name: str,
                 pipeline_id: str,
                 experiment_name: str,
                 pipeline_parameters_path: str,
                 pipeline_parameters: str,
                 namespace: str,
                 service_account: str,
                 pipeline_version_name: str = None,
                 run_name: str = None):
    """Function to trigger a run of an existing pipeline

    Arguments:
        client {kfp.Client} -- The kfp client
        pipeline_name {str} -- The name of the pipeline to trigger
        pipeline_id {str} -- The ID of the pipeline to trigger, takes precedence over name if provided
        experiment_name {str} -- The name of the experiment to place the run in
        pipeline_parameters_path {str} -- Optional path to parameters YAML file
        namespace {str} -- The Kubeflow namespace of the pipeline
        service_account {str} -- Optional, name of the Kubernetes service account to run the pipeline with
        pipeline_version_name {str} -- Name of the pipeline version, if pipeline_name was provided
        run_name {str} -- Name of the pipeline run
    """
    experiment_id = find_experiment_id(
        experiment_name=experiment_name, client=client, namespace=namespace)
    logging.info(f"The expriment id is: {experiment_id}")
    job_name = f"{pipeline_name}_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}" if not run_name else run_name
    logging.info(f"The job name is: {job_name}")

    file_pipeline_params = {} if not pipeline_parameters_path else read_pipeline_params(pipeline_parameters_path)
    raw_pipeline_params = {} if not pipeline_parameters else parse_raw_params(pipeline_parameters)
    logging.info(f"Parameters from file: {file_pipeline_params}\nParameters passed directly: {raw_pipeline_params}")
    pipeline_params = file_pipeline_params.copy()
    pipeline_params.update(raw_pipeline_params)
    logging.info(f"Merged parameters: {pipeline_params}")

    if pipeline_id:
        resolved_pipeline_id = pipeline_id
        resolved_version_id = None
    else:
        resolved_pipeline_id = find_pipeline_id(pipeline_name, client)
        logging.info(f"Found ID for pipeline {pipeline_name}: {resolved_pipeline_id}")
        if pipeline_version_name:
            resolved_version_id = find_pipeline_version_id(resolved_pipeline_id, pipeline_version_name, client)
            logging.info(f"Found ID for pipeline version {pipeline_version_name}: {resolved_version_id}")
        else:
            resolved_version_id = None

    logging.info(
        f"experiment_id: {experiment_id}, job_name:{job_name}, pipeline_params:{pipeline_params}, pipeline_id:{pipeline_id}, version_id:{resolved_version_id}, namespace:{namespace}")
    client.run_pipeline(
        experiment_id=experiment_id,
        job_name=job_name,
        params=pipeline_params,
        pipeline_id=resolved_pipeline_id,
        version_id=resolved_version_id,
        service_account=service_account)
    logging.info(
        "Successfully started the pipeline, head over to kubeflow and check it out")

