
# # Create a private DNS zone

# data "google_compute_instance" "vm_instance_data" {
#   name = google_compute_instance.vm_instance.name
#   zone = google_compute_instance.vm_instance.zone

#   depends_on = [google_compute_instance.vm_instance]
# }

# resource "google_dns_managed_zone" "private_zone" {
#   name        = "private-zone"
#   dns_name    = "internal.local."
#   visibility  = "private"
#   description = "A private DNS zone for internal services."

#   private_visibility_config {
#     networks {
#       network_url = google_compute_network.main.id
#     }
#   }
# }

# # Create a DNS record in the private zone
# resource "google_dns_record_set" "internal_service" {
#   name         = "djangoapp.internal.local."
#   type         = "A"
#   ttl          = 300
#   managed_zone = google_dns_managed_zone.private_zone.name
#   rrdatas      = [data.google_compute_instance.vm_instance_data.network_interface[0].access_config[0].nat_ip]

#   depends_on = [google_compute_instance.vm_instance]
# }
