# Bucket configuration
resource "google_storage_bucket" "bucket" {
  name          = "django-cdn"
  location      = var.location
  project       = var.project_id
  force_destroy = var.destroy
  storage_class = "NEARLINE"

  lifecycle {
    prevent_destroy = var.destroy
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
