variable "organization_id" {
  type        = string
  description = "REQUIRED: GCP organization ID"
}

variable "gcp_project" {
  type        = string
  description = "REQUIRED: GCP Project ID to deploy the Cloud Function"
}

variable "gcp_region" {
  type        = string
  default     = "asia-northeast1"
  description = "OPTIONAL"
}

variable "bucket_name" {
  type        = string
  description = "REQUIRED: GCS bucket to manage Cloud Function codes"
}

variable "slack_webhook_url" {
  type        = string
  description = "REQUIRED: slack webhook URL to notify results"
}

variable "job_schedule" {
  type        = string
  default     = "00 00 1 * *"
  description = "OPTIONAL: a cron expression for periodic execution"
}

variable "job_timezone" {
  type        = string
  default     = "Etc/GMT"
  description = "OPTIONAL: timezone"
}

variable "idle_vm_recommender_enabled" {
  type        = string
  default     = "true"
  description = "OPTIONAL: Option to enable Recommender"
}
