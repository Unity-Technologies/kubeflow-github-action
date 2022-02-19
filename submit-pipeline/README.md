# This action Submits Kubeflow Pipelines to Kubeflow cluster running on Google Cloud Platform. 

The purpose of this action is to allow for automated deployments of [Kubeflow Pipelines](https://github.com/kubeflow/pipelines) on Google Cloud Platform (GCP). The action will collect the pipeline from a python file and compile it before uploading it to Kubeflow. The Kubeflow deployment must be using [IAP](https://www.kubeflow.org/docs/gke/deploy/monitor-iap-setup/) on GCP to work.

# Usage

## Example Workflow that uses this action 


To compile a pipeline and upload it to kubeflow: 

```yaml
name: Compile and Deploy Kubeflow pipeline
on: [push]
```

## Inputs

* KUBEFLOW_URL: The endpoint where your Kubeflow UI is running.
* CLIENT_ID: The IAP client id, which was specified when the kubeflow deployment where setup using IAP.
* PIPELINE_CODE_PATH: The full path name including the filename of the python file that describes the pipeline you want to run on Kubeflow.  This should be relative to the root of the GitHub repository where the Action is triggered.
* PIPELINE_FUNCTION: The name of the function which defines the pipeline in the Python file
* PIPELINE_NAME: The name of the pipeline, this name will be the name of the pipeline in the Kubeflow UI. Defaults to `{PIPELINE_FUNCTION}_{GITHUB_SHA}`.
* PIPELINE_VERSION_NAME: The name of the pipeline version. Defaults to `{PIPELINE_FUNCTION}_{GITHUB_SHA}`.
* PIPELINE_PARAMETERS_PATH: Optional. Path to a parameters YAML file in your repo; the parameters will be passed to the pipeline.
* PIPELINE_PARAMETERS: Optional. YAML string containing parameter values; the parameters will be passed to the pipeline. If both this and PIPELINE_PARAMETERS_PATH are provided, the parameter lists will be merged, but values in this argument will override any matching keys in the file.
* ENCODED_GOOGLE_APPLICATION_CREDENTIALS: JSON key for a service account with permissions to call the KFP API. Base 64 encoded, e.g.:
``` bash
cat path-to-key.json | base64
```
* EXPERIMENT_NAME: The name of the experiment name within which the kubeflow pipeline should run
* PIPELINE_NAMESPACE: The namespace in which the pipeline should run
* RUN_PIPELINE: Should github action also trigger the pipeline: "true" or "false" (default false).
  RUN_NAME: Name of the pipeline run. Defaults to `{PIPELINE_NAME}_{DATETIME}`.
* V2_COMPATIBLE:
* description: If the pipeline should be compiled with KFP SDK v2 compatibility. "true" or "false" (default false).
* PIPELINE_SERVICE_ACCOUNT: Specifies which Kubernetes service account this run uses.
