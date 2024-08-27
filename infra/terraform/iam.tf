resource "google_service_account" "account" {
  account_id   = "django-service-account"
  display_name = "Django Service Account"
}
resource "google_storage_bucket_iam_member" "bucket_roles" {
  for_each = toset(var.roles)

  bucket = google_storage_bucket.bucket.name
  role   = each.value
  member = "serviceAccount:${google_service_account.account.email}"
}

# Granting Storage Admin Role to a User or Service Account
resource "google_project_iam_member" "compute_storage_admin" {
  project = var.project_id
  role    = "roles/compute.storageAdmin"
  member  = "serviceAccount:${google_service_account.account.email}"
}
