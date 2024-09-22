resource "google_storage_bucket" "vault" {
  location      = var.location
  name          = "django-vault-storage"
  project       = data.google_project.vault.project_id
  force_destroy = true
  storage_class = var.storage_class

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }

    condition {
      num_newer_versions = 1
    }
  }

}

# Grant service account access to the storage bucket
resource "google_storage_bucket_iam_member" "vault-server" {
  count  = length(var.storage_bucket_roles)
  bucket = google_storage_bucket.vault.name
  role   = element(var.storage_bucket_roles, count.index)
  member = "serviceAccount:${google_service_account.vault-server.email}"
}
