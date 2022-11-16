# This action Submits Kubeflow Pipelines to Kubeflow cluster running on Google Cloud Platform. 

The purpose of this action is to allow for automated deployments of [Kubeflow Pipelines](https://github.com/kubeflow/pipelines) on Google Cloud Platform (GCP). The action will collect the pipeline from a python file and compile it before uploading it to Kubeflow. The Kubeflow deployment must be using [IAP](https://www.kubeflow.org/docs/gke/deploy/monitor-iap-setup/) on GCP to work.

# Usage

## Example Workflow that uses this action 


To compile a pipeline and upload it to kubeflow: 

```yaml
permissions:
  contents: "read"
  id-token: "write"
  
steps:
  # Check out step MUST come before auth step
  - name: Checkout
    uses: "actions/checkout@v3"

  - name: Authenticate to Google Cloud
    id: auth
    uses: "google-github-actions/auth@v1"
    with:
      workload_identity_provider: projects/<project_number>/locations/global/workloadIdentityPools/<pool>/providers/<pool_provider>
      service_account: "<service_account_name>@<project>.iam.gserviceaccount.com"
      token_format: "id_token"
      id_token_audience: ${{ secrets.IAP_CLIENT_ID }}
      id_token_include_email: true

  - name: Submit Kubeflow pipeline
    id: kubeflow
    uses: Unity-Technologies/kubeflow-github-action/submit-pipeline@master
    with:
      KUBEFLOW_URL: https://kubeflow-platform.iap.stg.mlp.unity3d.com/pipeline
      ID_TOKEN: ${{ steps.auth.outputs.id_token }}
      PIPELINE_CODE_PATH: "kubeflow-pipeline-demo/hello_world_pipeline.py"
      PIPELINE_FUNCTION: "sequential_pipeline"
      PIPELINE_NAME: "demo-pipeline"
      PIPELINE_VERSION_NAME: "demo-pipeline-${{ github.sha }}"
      PIPELINE_NAMESPACE: "kubeflow-demo"
      PIPELINE_SERVICE_ACCOUNT: "kubeflow-demo"
      EXPERIMENT_NAME: "demo"
      RUN_PIPELINE: true
```

## Inputs to auth

* workload_identity_provider: The workload identity pool provider. To set this up, consider following PRE's guide [here](https://github.com/Unity-Technologies/terraform-google-pre-workload-identity-federation).
* service_account: A service account with permissions to call the KFP API.
* id_token_audience: The IAP client id, which can be obtained from Vault. See docs [here](https://docs.dp.unity3d.com/Machine_Learning_Platform/vault/).

## Inputs to kubeflow

* KUBEFLOW_URL: The endpoint where the Kubeflow service is running.
* ID_TOKEN: The OIDC token. Output of the `auth` [Github Actions](https://github.com/google-github-actions/auth) step in the same workflow. See more about OIDC tokens [here](https://docs.dp.unity3d.com/Machine-Learning-Platform/secrets/#oidc-token).
* PIPELINE_CODE_PATH: The full path name including the filename of the python file that describes the pipeline you want to run on Kubeflow.  This should be relative to the root of the GitHub repository where the Action is triggered.
* PIPELINE_FUNCTION: The name of the function which defines the pipeline in the Python file
* PIPELINE_NAME: The name of the pipeline, this name will be the name of the pipeline in the Kubeflow UI. Defaults to `{PIPELINE_FUNCTION}_{GITHUB_SHA}`.
* PIPELINE_VERSION_NAME: The name of the pipeline version. Defaults to `{PIPELINE_FUNCTION}_{GITHUB_SHA}`.
* PIPELINE_PARAMETERS_PATH: Optional. Path to a parameters YAML file in your repo; the parameters will be passed to the pipeline.
* PIPELINE_PARAMETERS: Optional. YAML string containing parameter values; the parameters will be passed to the pipeline. If both this and PIPELINE_PARAMETERS_PATH are provided, the parameter lists will be merged, but values in this argument will override any matching keys in the file. Use the `|` operator to write inline YAML, like so:
```yaml
PIPELINE_PARAMETERS: |
  docker_image: docker/whalesay:latest
  message: "Hello world!"
```
* EXPERIMENT_NAME: The name of the experiment name within which the kubeflow pipeline should run
* PIPELINE_NAMESPACE: The namespace in which the pipeline should run - should be your team's Kubeflow namespace.
* RUN_PIPELINE: Should github action also trigger the pipeline: "true" or "false" (default false).
  RUN_NAME: Name of the pipeline run. Defaults to `{PIPELINE_NAME}_{DATETIME}`.
* V2_COMPATIBLE: If the pipeline should be compiled with KFP SDK v2 compatibility. "true" or "false" (default false).
* PIPELINE_SERVICE_ACCOUNT: Specifies which Kubernetes service account this run uses - should be your team's service account which is provided with your Kubeflow profile.

## Necessary Permissions

The service account you use to obtain the `ID_TOKEN` parameter needs to have the correct permissions to call the KFP API and create pipelines and runs. The account should have the `roles/iap.httpsResourceAccessor` role in order to access the authenticated [id token](https://google-auth.readthedocs.io/en/stable/reference/google.oauth2.id_token.html?highlight=id_token) successfully.
To add this role to the associated GCP service account, please make a [PR to ML Platform Terraform repo](https://github.com/Unity-Technologies/ml-platform-terraform). You can follow this [example](https://github.com/Unity-Technologies/ml-platform-terraform#adding-service-account-role).

You must also add the service account email as a contributor to your Kubeflow namespace, using the `Manage Contributors` tab in the Kubeflow UI.
