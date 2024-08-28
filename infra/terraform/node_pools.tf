resource "google_container_node_pool" "general" {
  name       = "general"
  cluster    = google_container_cluster.primary.id
  node_count = 1
  location   = var.gcp_region

  management {
    auto_repair  = true
    auto_upgrade = true
  }


  node_config {
    preemptible     = false
    machine_type    = var.machine_types["standard2"]
    service_account = google_service_account.account.email
    oauth_scopes    = var.oauth_scopes
    workload_metadata_config {
      mode = "GKE_METADATA"
    }
    labels = {
      role = "general"
    }
  }

  autoscaling {
    min_node_count = var.min_node_count
    max_node_count = var.max_node_count
  }

}

resource "google_container_node_pool" "spot" {
  name     = "spot"
  cluster  = google_container_cluster.primary.id
  location = var.gcp_region

  management {
    auto_repair  = true
    auto_upgrade = true
  }

  autoscaling {
    min_node_count = var.min_node_count
    max_node_count = var.max_node_count
  }

  node_config {
    preemptible     = true
    machine_type    = var.machine_types["standard2"]
    service_account = google_service_account.account.email
    oauth_scopes    = var.oauth_scopes

    workload_metadata_config {
      mode = "GKE_METADATA"
    }

    labels = {
      team = "devops"
    }

    taint {
      key    = "instance_type"
      value  = "spot"
      effect = "NO_SCHEDULE"
    }

  }
}
