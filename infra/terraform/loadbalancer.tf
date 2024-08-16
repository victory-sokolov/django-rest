# Google Cloud Load Balancer
resource "google_compute_url_map" "url_map" {
  name            = "static-url-map"
  default_service = google_compute_backend_bucket.backend_bucket.id
}

resource "google_compute_target_http_proxy" "http_proxy" {
  name    = "static-http-proxy"
  url_map = google_compute_url_map.url_map.id
}

resource "google_compute_global_forwarding_rule" "forwarding_rule" {
  name       = "static-forwarding-rule"
  target     = google_compute_target_http_proxy.http_proxy.id
  port_range = "80"
}
