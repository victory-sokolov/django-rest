# Generate self-signed TLS certificates
resource "tls_private_key" "vault-ca" {
  algorithm = "RSA"
  rsa_bits  = "2048"
}

resource "tls_self_signed_cert" "vault-ca" {
  private_key_pem = tls_private_key.vault-ca.private_key_pem

  subject {
    common_name  = "vault-ca.local"
    organization = "HashiCorp Vault"
  }

  validity_period_hours = 8760
  is_ca_certificate     = true

  allowed_uses = [
    "cert_signing",
    "digital_signature",
    "key_encipherment",
  ]
}

# Create local directory for TLS files
resource "null_resource" "create_tls_dir" {
  provisioner "local-exec" {
    command = "mkdir -p ./tls && chmod 700 ./tls"
  }
}

# Write CA certificate to file
resource "local_file" "ca_cert" {
  depends_on      = [null_resource.create_tls_dir]
  content         = tls_self_signed_cert.vault-ca.cert_pem
  filename        = "./tls/ca.pem"
  file_permission = "0600"
}

# Create the Vault server certificates
resource "tls_private_key" "vault" {
  algorithm = "RSA"
  rsa_bits  = "2048"
}

# Create the request to sign the cert with our CA
resource "tls_cert_request" "vault" {
  private_key_pem = tls_private_key.vault.private_key_pem

  dns_names = [
    "vault",
    "vault.local",
    "vault.default.svc.cluster.local",
  ]

  ip_addresses = [
    google_compute_address.vault.address,
  ]

  subject {
    common_name  = "vault.local"
    organization = "HashiCorp Vault"
  }
}

# Now sign the cert
resource "tls_locally_signed_cert" "vault" {
  cert_request_pem   = tls_cert_request.vault.cert_request_pem
  ca_private_key_pem = tls_private_key.vault-ca.private_key_pem
  ca_cert_pem        = tls_self_signed_cert.vault-ca.cert_pem

  validity_period_hours = 8760

  allowed_uses = [
    "cert_signing",
    "client_auth",
    "digital_signature",
    "key_encipherment",
    "server_auth",
  ]
}

# Write Vault certificate to file
resource "local_file" "vault_cert" {
  depends_on      = [null_resource.create_tls_dir]
  content         = "${tls_locally_signed_cert.vault.cert_pem}${tls_self_signed_cert.vault-ca.cert_pem}"
  filename        = "./tls/ca.pem"
  file_permission = "0600"
}
