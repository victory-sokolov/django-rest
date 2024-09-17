# GCP Provider
provider "google" {
  credentials = file("gcp-creds.json")
  project     = var.project_id
  region      = var.gcp_region
  zone        = var.gcp_zone
}

provider "google-beta" {
  project = var.project_id
  region  = var.gcp_region
  zone    = var.gcp_zone
}
