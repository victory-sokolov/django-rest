
# resource "google_storage_bucket_iam_member" "default" {
#   bucket = google_storage_bucket.default.name
#   role   = "roles/storage.objectViewer"
#   member = "allUsers"
# }

resource "google_service_account" "account" {
  account_id   = "django-service-account"
  display_name = "Django Service Account"
}

# Granting Storage Admin Role to a User or Service Account
resource "google_project_iam_member" "compute_storage_admin" {
  project = var.project_id
  role    = "roles/compute.storageAdmin"
  member  = "serviceAccount:${google_service_account.account.email}"
}
