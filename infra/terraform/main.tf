# Creating VM instance
resource "google_compute_instance" "vm_instance" {
  name                = "terraform-instance"
  machine_type        = var.machine_types["small"]
  deletion_protection = var.delete_protection

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
  for_each                   = toset(var.gcp_service_list)
  project                    = var.project_id
  service                    = each.key
  disable_on_destroy         = false
  disable_dependent_services = false
}
