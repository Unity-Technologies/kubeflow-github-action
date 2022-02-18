# This action triggers a run of a Kubeflow Pipeline which has already been uploaded to Kubeflow.

# Usage

## Example Workflow that uses this action 

To trigger a pipeline:

```yaml
name: Compile and Deploy Kubeflow pipeline
on: [push]
```

## Inputs

* KUBEFLOW_URL: The endpoint where your Kubeflow UI is running.
* CLIENT_ID: The IAP client id, which was specified when the kubeflow deployment where setup using IAP.
* PIPELINE_PARAMETERS_PATH: Optional. Path to a parameters YAML file in your repo; the parameters will be passed to the pipeline.
* ENCODED_GOOGLE_APPLICATION_CREDENTIALS: JSON key for a service account with permissions to call the KFP API. Base 64 encoded, e.g.:
* ``` bash
* cat path-to-key.json | base64
* ```
* EXPERIMENT_NAME: The name of the experiment name within which the kubeflow pipeline should run
* PIPELINE_NAMESPACE: The namespace in which the pipeline should run
* PIPELINE_ID: The ID of the version of the pipeline to be triggered. If provided this will take priority over the pipeline name and version name.
* PIPELINE_NAME: The name of the pipeline to be triggered. If provided without the version name will trigger the default version.
* PIPELINE_VERSION_NAME: The name of the version of the pipeline to be triggered. PIPELINE_NAME must be provided. If PIPELINE_ID is provided it will override this.
* RUN_NAME: Name of the run. Defaults to `{PIPELINE_NAME}_{DATETIME}`.
* PIPELINE_SERVICE_ACCOUNT: Specifies which Kubernetes service account this run uses.
