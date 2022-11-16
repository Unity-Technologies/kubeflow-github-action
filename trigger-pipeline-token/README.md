# This action triggers a run of a Kubeflow Pipeline which has already been uploaded to Kubeflow.

# Usage

## Example Workflow that uses this action 

To trigger a pipeline:

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

  - name: Trigger Kubeflow pipeline by name, default version
    id: kubeflow
    uses: Unity-Technologies/kubeflow-github-action/trigger-pipeline@master
    with:
      KUBEFLOW_URL: https://kubeflow-platform.iap.stg.mlp.unity3d.com/pipeline
      ID_TOKEN: ${{ steps.auth.outputs.id_token }}
      PIPELINE_NAMESPACE: "kubeflow-demo"
      PIPELINE_SERVICE_ACCOUNT: "kubeflow-demo"
      PIPELINE_NAME: ${{ github.event.inputs.pipeline_name }}
      EXPERIMENT_NAME: ${{ github.event.inputs.experiment_name }}
      RUN_NAME: ${{ github.event.inputs.run_name }}
      PIPELINE_PARAMETERS_PATH: my-parameters-file.yaml
```

## Inputs to auth

* workload_identity_provider: The workload identity pool provider. To set this up, consider following PRE's guide [here](https://github.com/Unity-Technologies/terraform-google-pre-workload-identity-federation).
* service_account: A service account with permissions to call the KFP API.
* id_token_audience: The IAP client id, which can be obtained from Vault. See docs [here](https://docs.dp.unity3d.com/Machine_Learning_Platform/vault/).

## Inputs

* KUBEFLOW_URL: The endpoint where the Kubeflow service is running.
* ID_TOKEN: The OIDC token. Output of the `auth` [Github Actions](https://github.com/google-github-actions/auth) step in the same workflow. See more about OIDC tokens [here](https://docs.dp.unity3d.com/Machine-Learning-Platform/secrets/#oidc-token).
* PIPELINE_PARAMETERS_PATH: Optional. Path to a parameters YAML file in your repo; the parameters will be passed to the pipeline.
* PIPELINE_PARAMETERS: Optional. YAML string containing parameter values; the parameters will be passed to the pipeline. If both this and PIPELINE_PARAMETERS_PATH are provided, the parameter lists will be merged, but values in this argument will override any matching keys in the file. Use the `|` operator to write inline YAML, like so:
```yaml
PIPELINE_PARAMETERS: |
  docker_image: docker/whalesay:latest
  message: "Hello world!"
```
* EXPERIMENT_NAME: The name of the experiment name within which the kubeflow pipeline should run
* PIPELINE_NAMESPACE: The namespace in which the pipeline should run - should be your team's Kubeflow namespace.
* PIPELINE_ID: The ID of the version of the pipeline to be triggered. If provided this will take priority over the pipeline name and version name.
* PIPELINE_NAME: The name of the pipeline to be triggered. If provided without the version name will trigger the default version.
* PIPELINE_VERSION_NAME: The name of the version of the pipeline to be triggered. PIPELINE_NAME must be provided. If PIPELINE_ID is provided it will override this.
* RUN_NAME: Name of the run. Defaults to `{PIPELINE_NAME}_{DATETIME}`.
* PIPELINE_SERVICE_ACCOUNT: Specifies which Kubernetes service account this run uses - should be your team's service account which is provided with your Kubeflow profile.

## Necessary Permissions

The service account you use to obtain the `ID_TOKEN` parameter needs to have the correct permissions to call the KFP API and create pipelines and runs. The account should have the `roles/iap.httpsResourceAccessor` role in order to access the authenticated [id token](https://google-auth.readthedocs.io/en/stable/reference/google.oauth2.id_token.html?highlight=id_token) successfully.
To add this role to the associated GCP service account, please make a [PR to ML Platform Terraform repo](https://github.com/Unity-Technologies/ml-platform-terraform). You can follow this [example](https://github.com/Unity-Technologies/ml-platform-terraform#adding-service-account-role).

You must also add the service account email as a contributor to your Kubeflow namespace, using the `Manage Contributors` tab in the Kubeflow UI.
