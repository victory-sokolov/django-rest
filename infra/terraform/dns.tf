
# Create a private DNS zone

resource "google_dns_managed_zone" "dns_zone" {
  name          = "private-zone"
  dns_name      = "django.app."
  visibility    = "private"
  description   = "A private DNS zone for internal services."
  force_destroy = true

  private_visibility_config {
    networks {
      network_url = google_compute_network.main.id
    }
  }
}

# Create a DNS record in the private zone
resource "google_dns_record_set" "internal_service" {
  name         = "django.app."
  type         = "A"
  ttl          = 300
  managed_zone = google_dns_managed_zone.dns_zone.name
  rrdatas = [
    google_compute_instance.vm_instance.network_interface[0].network_ip
  ]

  depends_on = [google_compute_instance.vm_instance]
}
