# Input variables.
#
# Anything that differs between environments belongs here, not in main.tf.
# If you find yourself editing main.tf to deploy to a different environment,
# something has gone wrong.

variable "project" {
  description = "Short project name, used as a prefix for every resource."
  type        = string
  default     = "northgate"

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{1,20}$", var.project))
    error_message = "Project must be lowercase letters, digits and hyphens, starting with a letter."
  }
}

variable "environment" {
  description = "Environment name. Set per environment in envs/*.tfvars."
  type        = string

  validation {
    condition     = contains(["staging", "production"], var.environment)
    error_message = "Environment must be either staging or production."
  }
}

variable "app_image" {
  description = <<-EOT
    Container image for the application, including its tag.

    Use the image your Week 5 pipeline published to the registry. If you are
    working offline, build it locally with the same tag first.
  EOT
  type        = string
}

variable "app_instance_count" {
  description = "How many application containers to run behind sequential host ports."
  type        = number
  default     = 1

  validation {
    condition     = var.app_instance_count >= 1 && var.app_instance_count <= 4
    error_message = "Run between 1 and 4 instances. More than that will exhaust the port range."
  }
}

variable "app_host_port" {
  description = "First host port for the application. Further instances take the next ports up."
  type        = number
  default     = 8081
}

variable "app_memory_mb" {
  description = "Memory limit per application container, in megabytes."
  type        = number
  default     = 256
}

variable "db_image" {
  description = "Container image for the database."
  type        = string
  default     = "postgres:16-alpine"
}

variable "db_memory_mb" {
  description = "Memory limit for the database container, in megabytes."
  type        = number
  default     = 256
}

variable "db_name" {
  description = "Database name."
  type        = string
  default     = "clickcollect"
}

variable "db_user" {
  description = "Database user."
  type        = string
  default     = "clickcollect"
}

variable "db_password" {
  description = <<-EOT
    Database password.

    There is deliberately no default. Supply it from the environment:

        export TF_VAR_db_password="$(openssl rand -base64 24)"

    Do not put it in a .tfvars file and do not commit it. This is the same
    rule you applied to pipeline secrets in Week 6.
  EOT
  type        = string
  sensitive   = true
}
