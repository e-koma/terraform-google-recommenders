# Recommender Terraform Module
This Terraform deploys a CloudFunction to use Recommender across the organization

## Required Permission
Organization Admin permission (`roles/resourcemanager.organizationAdmin`) is required for terraform execution.

## Usage
```hcl

```

## Supported Recommender
- `google.compute.instance.IdleResourceRecommender`

## Input Variables
| Name                        | Description                                 | Type   | Default           | Required |
|:----------------------------|:--------------------------------------------|:-------|:------------------|:---------|
| organization_id             | GCP Organization ID                         | string | ""                | yes      |
| gcp_project                 | GCP Project ID to deploy the Cloud Function | string | ""                | yes      |
| gcp_region                  | GCP Region to deploy                        | string | "asia-northeast1" | no       |
| bucket_name                 | GCS bucket to manage Cloud Function codes   | string | ""                | yes      |
| slack_webhook_url           | Slack Webhook URL to notify results         | string | ""                | yes      |
| job_schedule                | Cron expression for periodic execution      | string | "00 00 1 * *"     | no       |
| job_timezone                | Timezone                                    | string | "Etc/GMT"         | no       |
| idle_vm_recommender_enabled | Option to enable Recommender                | string | "true"            | no       |
