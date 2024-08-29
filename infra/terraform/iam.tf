resource "google_project_iam_custom_role" "django_roles" {
  role_id     = "djangoApp"
  title       = "Django App"
  description = "Role created for Django application"
  permissions = [
    "orgpolicy.policy.get",
    "resourcemanager.projects.get",
    "storage.multipartUploads.abort",
    "storage.multipartUploads.create",
    "storage.multipartUploads.list",
    "storage.multipartUploads.listParts",
    "storage.objects.create",
    "storage.objects.delete",
    "storage.objects.get",
    "storage.objects.list",
    "storage.objects.update",
  ]
}

resource "google_service_account" "account" {
  account_id   = "django-service-account"
  display_name = "Django Service Account"
  description  = "Django Main Service Account"
}

resource "google_service_account" "kubernetes" {
  account_id = "kubernetes"
}

# resource "google_service_account" "run_service_account" {
#   account_id   = "cloud-run-sa"
#   display_name = "Cloud Run Service Account"
# }

resource "google_storage_bucket_iam_member" "bucket_roles" {
  bucket = google_storage_bucket.bucket.name
  role   = google_project_iam_custom_role.django_roles.id
  member = google_service_account.account.member
}

# Granting Storage Admin Role to a User or Service Account
resource "google_project_iam_member" "compute_storage_admin" {
  project = var.project_id
  role    = "roles/compute.storageAdmin"
  member  = google_service_account.account.member
}

resource "google_service_account_iam_member" "identity_user" {
  service_account_id = google_service_account.account.name
  role               = "roles/iam.workloadIdentityUser"
  member             = google_service_account.account.member
}
