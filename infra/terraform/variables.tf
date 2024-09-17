variable "gcp_service_list" {
  description = "The list of apis necessary for the Google cloud project"
  type        = list(string)
  default = [
    "serviceusage.googleapis.com",
    "cloudkms.googleapis.com",
    "storage.googleapis.com",
    "iam.googleapis.com",
    # "artifactregistry.googleapis.com",
    # "run.googleapis.com",
    # "cloudbuild.googleapis.com",
    "secretmanager.googleapis.com",
    "container.googleapis.com", # Enables GKE
    "compute.googleapis.com",
  ]
}

variable "project_id" {
  description = "Google cloud project id"
  type        = string
  default     = "django-app-431708"
}

variable "gcp_region" {
  type    = string
  default = "europe-west4"
}

variable "gke_cluster_name" {
  type    = string
  default = "primary"
}

variable "gcp_zone" {
  type    = string
  default = "europe-west4-b"
}

variable "location" {
  type    = string
  default = "EU"
}

variable "delete_protection" {
  type    = bool
  default = false # true to prevent deleting resources
}

variable "destroy" {
  type    = bool
  default = false
}

variable "image_name" {
  type    = string
  default = "django-blog"
}

variable "bucket_name" {
  type    = string
  default = "django-cdn"
}

variable "min_node_count" {
  type    = number
  default = 3
}

variable "max_node_count" {
  type    = number
  default = 5
}

variable "machine_types" {
  type = map(string)
  default = {
    small     = "e2-micro"
    medium    = "e2-medium"
    standard2 = "e2-standard-2"
    standard4 = "e2-standard-4"
  }
}

variable "vault_namespace" {
  type    = string
  default = "admin"
}

variable "initial_node_count" {
  type    = number
  default = 1
}

variable "roles" {
  type = list(string)
  default = [
    "roles/storage.objectViewer",
    "roles/storage.objectCreator",
    "roles/storage.objectAdmin",
  ]
}

variable "oauth_scopes" {
  type = list(string)
  default = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/devstorage.read_write",
    "https://www.googleapis.com/auth/servicecontrol",
  ]
}

variable "storage_class" {
  type    = string
  default = "NEARLINE"
}

#
# Vault options
# ------------------------------

# This is an option used by the kubernetes provider, but is part of the Vault
# security posture.
variable "vault_source_ranges" {
  type        = list(string)
  default     = ["0.0.0.0/0"]
  description = "List of addresses or CIDR blocks which are allowed to connect to the Vault IP address. The default behavior is to allow anyone (0.0.0.0/0) access. You should restrict access to external IPs that need to access the Vault cluster."
}

variable "num_vault_pods" {
  type        = number
  default     = 3
  description = "Number of Vault pods to run. Anti-affinity rules spread pods across available nodes. Please use an odd number for better availability."
}

variable "vault_container" {
  type        = string
  default     = "vault:1.2.1"
  description = "Name of the Vault container image to deploy. This can be specified like \"container:version\" or as a full container URL."
}

variable "vault_init_container" {
  type        = string
  default     = "sethvargo/vault-init:1.0.0"
  description = "Name of the Vault init container image to deploy. This can be specified like \"container:version\" or as a full container URL."
}

variable "vault_recovery_shares" {
  type        = string
  default     = "1"
  description = "Number of recovery keys to generate."
}

variable "vault_recovery_threshold" {
  type        = string
  default     = "1"
  description = "Number of recovery keys required for quorum. This must be less than or equal to \"vault_recovery_keys\"."
}
