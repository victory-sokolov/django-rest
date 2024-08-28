output "bucket" {
  value = google_storage_bucket.bucket.name
}

output "ip" {
  value = google_compute_instance.vm_instance.network_interface.0.network_ip
}

output "cdn_url" {
  value = "http://${google_compute_global_forwarding_rule.forwarding_rule.ip_address}"
}

# output "artifact_registry_name" {
#   value = google_artifact_registry_repository.docker_repository.name
# }

# output "cloud_run_url" {
#   value = google_cloud_run_v2_service.django_service.uri
# }
