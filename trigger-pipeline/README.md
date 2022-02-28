# This action triggers a run of a Kubeflow Pipeline which has already been uploaded to Kubeflow.

# Usage

## Example Workflow that uses this action 

To trigger a pipeline:

```yaml
- name: Trigger Kubeflow pipeline by name, default version
  id: kubeflow
  uses: Unity-Technologies/kubeflow-github-action/trigger-pipeline@master
  with:
    KUBEFLOW_URL: https://kubeflow-platform.iap.stg.mlp.unity3d.com/pipeline
    ENCODED_GOOGLE_APPLICATION_CREDENTIALS: ${{ secrets.KUBEFLOW_DEMO_SA_KEY_ENCODED }}
    CLIENT_ID: ${{ secrets.IAP_CLIENT_ID }}
    PIPELINE_NAMESPACE: "kubeflow-demo"
    PIPELINE_SERVICE_ACCOUNT: "kubeflow-demo"
    PIPELINE_NAME: ${{ github.event.inputs.pipeline_name }}
    EXPERIMENT_NAME: ${{ github.event.inputs.experiment_name }}
    RUN_NAME: ${{ github.event.inputs.run_name }}
    PIPELINE_PARAMETERS_PATH: my-parameters-file.yaml
```

## Inputs

* KUBEFLOW_URL: The endpoint where the Kubeflow service is running.
* CLIENT_ID: The IAP client id, which can be obtained from Vault. See docs [here](https://docs.dp.unity3d.com/Machine_Learning_Platform/vault/).
* PIPELINE_PARAMETERS_PATH: Optional. Path to a parameters YAML file in your repo; the parameters will be passed to the pipeline.
* PIPELINE_PARAMETERS: Optional. YAML string containing parameter values; the parameters will be passed to the pipeline. If both this and PIPELINE_PARAMETERS_PATH are provided, the parameter lists will be merged, but values in this argument will override any matching keys in the file. Use the `|` operator to write inline YAML, like so:
```yaml
PIPELINE_PARAMETERS: |
  docker_image: docker/whalesay:latest
  message: "Hello world!"
```
* ENCODED_GOOGLE_APPLICATION_CREDENTIALS: JSON key for a service account with permissions to call the KFP API. Base 64 encoded, e.g.:
``` bash
cat path-to-key.json | base64
```
* EXPERIMENT_NAME: The name of the experiment name within which the kubeflow pipeline should run
* PIPELINE_NAMESPACE: The namespace in which the pipeline should run - should be your team's Kubeflow namespace.
* PIPELINE_ID: The ID of the version of the pipeline to be triggered. If provided this will take priority over the pipeline name and version name.
* PIPELINE_NAME: The name of the pipeline to be triggered. If provided without the version name will trigger the default version.
* PIPELINE_VERSION_NAME: The name of the version of the pipeline to be triggered. PIPELINE_NAME must be provided. If PIPELINE_ID is provided it will override this.
* RUN_NAME: Name of the run. Defaults to `{PIPELINE_NAME}_{DATETIME}`.
* PIPELINE_SERVICE_ACCOUNT: Specifies which Kubernetes service account this run uses - should be your team's service account which is provided with your Kubeflow profile.
