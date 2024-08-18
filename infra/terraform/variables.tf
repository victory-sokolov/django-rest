variable "gcp_service_list" {
  description = "The list of apis necessary for the Google cloud project"
  type        = list(string)
  default = [
    "serviceusage.googleapis.com",
    "storage.googleapis.com",
    "iam.googleapis.com",
    "artifactregistry.googleapis.com",
    "run.googleapis.com",
    "cloudbuild.googleapis.com",
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

variable "gcp_zone" {
  type    = string
  default = "europe-west4-b"
}

variable "location" {
  type    = string
  default = "EU"
}

variable "destroy" {
  type    = bool
  default = false
}

variable "image_name" {
  type    = string
  default = "django-blog"
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
