# Creating VM instance
resource "google_compute_instance" "vm_instance" {
  name         = "terraform-instance"
  machine_type = var.machine_types["small"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    # A default network is created for all GCP projects
    network = "default"
    access_config {
    }
  }

  allow_stopping_for_update = true
}

resource "google_project_service" "gcp_services" {
  for_each           = toset(var.gcp_service_list)
  project            = var.project_id
  service            = each.key
  disable_on_destroy = false
}

# Reserve a static IP address
resource "google_compute_global_address" "app-ip" {
  name = "djangoapp-ip"
}

# Create Artifact Registry repository
resource "google_artifact_registry_repository" "docker_repository" {
  repository_id = "django-blog"
  location      = var.gcp_region
  format        = "DOCKER"
  description   = "Docker repository for django app"
}

# Create a Cloud Run service resource:
resource "google_cloud_run_v2_service" "django_service" {
  name     = "django-app"
  location = var.gcp_region

  template {
    containers {
      image = "${var.gcp_region}-docker.pkg.dev/${var.project_id}/${var.image_name}/${var.image_name}:latest"
      ports {
        container_port = 8000
      }
      resources {
        limits = {
          cpu    = "2"
          memory = "1024Mi"
        }
      }
    }

    service_account = google_service_account.run_service_account.email
  }

  traffic {
    percent = 100
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
  }

}

resource "google_service_account" "run_service_account" {
  account_id   = "cloud-run-sa"
  display_name = "Cloud Run Service Account"
}
