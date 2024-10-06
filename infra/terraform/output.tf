output "bucket" {
  value = google_storage_bucket.bucket.name
}

output "ip" {
  value = google_compute_instance.vm_instance.network_interface.0.network_ip
}

output "cdn_url" {
  value = "http://${google_compute_global_forwarding_rule.forwarding_rule.ip_address}"
}

output "workspace" {
  value = terraform.workspace
}

output "vm_internal_ip" {
  value = google_compute_instance.vm_instance.network_interface[0].network_ip
}

output "dns_zone_name" {
  value = google_dns_managed_zone.dns_zone.dns_name
}

# output "artifact_registry_name" {
#   value = google_artifact_registry_repository.docker_repository.name
# }

# output "cloud_run_url" {
#   value = google_cloud_run_v2_service.django_service.uri
# }
