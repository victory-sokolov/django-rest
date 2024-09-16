# Google Cloud Engine configuration
resource "google_compute_network" "main" {
  name                            = "main"
  routing_mode                    = "REGIONAL"
  auto_create_subnetworks         = false
  mtu                             = 1460
  delete_default_routes_on_create = false

  depends_on = [
    google_project_service.gcp_services["compute.googleapis.com"],
    google_project_service.gcp_services["container.googleapis.com"],
  ]
}

# Configure Control Plane
resource "google_container_cluster" "primary" {
  name                     = var.gke_cluster_name
  location                 = var.gcp_zone
  remove_default_node_pool = true
  deletion_protection      = var.delete_protection
  initial_node_count       = var.initial_node_count
  network                  = google_compute_network.main.self_link
  subnetwork               = google_compute_subnetwork.private.self_link
  logging_service          = "logging.googleapis.com/kubernetes"
  # monitoring_service       = "monitoring.googleapis.com/kubernetes"
  networking_mode = "VPC_NATIVE"

  node_config {
    preemptible     = true
    machine_type    = var.machine_types["standard2"]
    service_account = google_service_account.account.email
    oauth_scopes    = var.oauth_scopes

    metadata = {
      disable-legacy-endpoints = "true"
    }
  }

  addons_config {
    http_load_balancing {
      disabled = false
    }
    horizontal_pod_autoscaling {
      disabled = true
    }
  }

  release_channel {
    channel = "REGULAR"
  }

  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  ip_allocation_policy {
    cluster_secondary_range_name  = "k8s-pod-range"
    services_secondary_range_name = "k8s-service-range"
  }

  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = false
    master_ipv4_cidr_block  = "172.16.0.0/28"
  }
}
