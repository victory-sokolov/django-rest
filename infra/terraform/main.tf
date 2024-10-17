# module "vault" {
#   source     = "./vault"
#   gcp_region = var.gcp_region
#   project_id = var.project_id
#   location   = var.location
# }

# Creating VM instance
resource "google_compute_instance" "vm_instance" {
  name                = "terraform-instance"
  machine_type        = var.machine_types["small"]
  deletion_protection = var.delete_protection

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
    }
  }

  network_interface {
    # A default network is created for all GCP projects
    network    = google_compute_network.main.self_link
    subnetwork = google_compute_subnetwork.private.self_link
    access_config {
    }
  }

  allow_stopping_for_update = true
}

resource "google_project_service" "gcp_services" {
  for_each                   = toset(var.gcp_service_list)
  project                    = var.project_id
  service                    = each.key
  disable_on_destroy         = false
  disable_dependent_services = false
}
