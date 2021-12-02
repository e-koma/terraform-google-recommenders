resource "google_service_account" "recommender_service_account" {
  project      = var.gcp_project
  account_id   = "recommender-checker"
  display_name = "Service Account For Recommender"
  depends_on = [
    google_project_service.recommender_service
  ]
}

resource "google_organization_iam_member" "recommender_iam_member_cloudasset" {
  org_id = var.organization_id
  role   = "roles/cloudasset.viewer"
  member = "serviceAccount:${google_service_account.recommender_service_account.email}"
}

# NOTE: Recommenderの種類が増やす場合、対応するrecommender roleを付与する
resource "google_organization_iam_member" "recommender_iam_member_suggestion" {
  org_id = var.organization_id
  role   = "roles/recommender.computeViewer"
  member = "serviceAccount:${google_service_account.recommender_service_account.email}"
}

resource "google_pubsub_topic" "recommender_checker_topic" {
  project = var.gcp_project
  name    = "recommender-checker"
  depends_on = [
    google_project_service.recommender_service
  ]
}

data "archive_file" "recommender_checker_archive" {
  type        = "zip"
  source_dir  = "./scripts/cloudfunctions/recommender-checker"
  output_path = "./scripts/cloudfunctions/recommender-checker.zip"
}

resource "google_storage_bucket_object" "recommender_checker_object" {
  name   = "terraform/cloudfunctions/recommender-checker-${data.archive_file.recommender_checker_archive.output_md5}.zip"
  bucket = var.bucket_name
  source = data.archive_file.recommender_checker_archive.output_path
}

resource "google_cloudfunctions_function" "recommender_checker_func" {
  project     = var.gcp_project
  region      = var.gcp_region
  name        = "recommender-checker"
  description = "check Recommender for all GCP projects"
  runtime     = "python39"

  available_memory_mb   = 128
  source_archive_bucket = var.bucket_name
  source_archive_object = google_storage_bucket_object.recommender_checker_object.name
  timeout               = 300
  entry_point           = "check_recommender"

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = google_pubsub_topic.recommender_checker_topic.name
    failure_policy {
      retry = false
    }
  }

  environment_variables = {
    ORGANIZATION_ID                  = var.organization_id
    SLACK_HOOK_URL                   = var.slack_webhook_url
    IDLE_VM_RECOMMENDER_ENABLED      = var.idle_vm_recommender_enabled
    IDLE_PROJECT_RECOMMENDER_ENABLED = var.idle_project_recommender_enabled
  }
  service_account_email = google_service_account.recommender_service_account.email
}

resource "google_cloud_scheduler_job" "recommender_checker_scheduler" {
  project     = var.gcp_project
  region      = var.gcp_region
  name        = "recommender_checker_scheduler"
  description = "check Recommender for all GCP projects"
  schedule    = var.job_schedule
  time_zone   = var.job_timezone

  pubsub_target {
    topic_name = google_pubsub_topic.recommender_checker_topic.id
    data       = base64encode("{}")
  }
}
