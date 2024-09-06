
# Create a private DNS zone
resource "google_dns_managed_zone" "private_zone" {
  name        = "private-zone"
  dns_name    = "internal.local."
  visibility  = "private"
  description = "A private DNS zone for internal services."

  private_visibility_config {
    networks {
      network_url = google_compute_network.main.self_link
    }
  }
}

# Create a DNS record in the private zone
resource "google_dns_record_set" "internal_service" {
  name         = "djangoapp.internal.local."
  type         = "A"
  ttl          = 300
  managed_zone = google_dns_managed_zone.private_zone.name
  rrdatas      = [google_compute_instance.vm_instance.network_interface.0.access_config.0.nat_ip]
}
