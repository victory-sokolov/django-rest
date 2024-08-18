resource "google_compute_firewall" "firewall" {
  name    = "firewall"
  network = google_compute_network.main.name

  allow {
    protocol = "tcp"
    ports    = ["22", "8000", "8080", "31005"]
  }

  source_ranges = ["0.0.0.0/0"] # allow any ip to access port 22
}
