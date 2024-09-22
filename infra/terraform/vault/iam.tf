# Grant service account access to the storage bucket
resource "google_storage_bucket_iam_member" "vault_member" {
  count  = length(var.storage_bucket_roles)
  bucket = google_storage_bucket.vault.name
  role   = element(var.storage_bucket_roles, count.index)
  member = "serviceAccount:${google_service_account.vault-server.email}"
}
