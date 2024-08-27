# Bucket configuration
resource "google_storage_bucket" "bucket" {
  name          = var.bucket_name
  location      = var.location
  project       = var.project_id
  force_destroy = false
  storage_class = "NEARLINE"

  lifecycle {
    prevent_destroy = false
  }

  versioning {
    enabled = true
  }

  cors {
    origin          = ["*"]
    method          = ["GET"]
    max_age_seconds = 3600
  }
}

resource "google_compute_backend_bucket" "backend_bucket" {
  name        = "static-backend-bucket"
  bucket_name = google_storage_bucket.bucket.name
  enable_cdn  = true
}
