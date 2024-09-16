# Create Artifact Registry repository
# resource "google_artifact_registry_repository" "docker_repository" {
#   repository_id = "django-blog"
#   location      = var.gcp_region
#   format        = "DOCKER"
#   description   = "Docker repository for django app"
# }

# Create a Cloud Run service resource:
# resource "google_cloud_run_v2_service" "django_service" {
#   name                = "django-app"
#   location            = var.gcp_region
#   deletion_protection = var.delete_protection

#   template {
#     containers {
#       image = "${var.gcp_region}-docker.pkg.dev/${var.project_id}/${var.image_name}/${var.image_name}:latest"
#       ports {
#         container_port = 8000
#       }
#       resources {
#         limits = {
#           cpu    = "2"
#           memory = "1024Mi"
#         }
#       }
#     }

#     service_account = google_service_account.account.email
#   }

#   traffic {
#     percent = 100
#     type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
#   }
# }
