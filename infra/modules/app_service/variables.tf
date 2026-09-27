variable "project" {
  description = "Short project name."
  type        = string
}

variable "environment" {
  description = "Environment name."
  type        = string
}

variable "image" {
  description = "Application image including tag."
  type        = string
}

variable "instance_count" {
  description = "Number of application containers."
  type        = number
  default     = 1
}

variable "host_port" {
  description = "First host port. Instance n takes host_port + n - 1."
  type        = number
}

variable "container_port" {
  description = "Port the application listens on inside the container."
  type        = number
  default     = 5000
}

variable "memory_mb" {
  description = "Memory limit per container, in megabytes."
  type        = number
  default     = 256
}

variable "network_name" {
  description = "Docker network to join."
  type        = string
}

variable "database_url" {
  description = "Connection string passed to the application."
  type        = string
  sensitive   = true
}

variable "labels" {
  description = "Labels applied to every container this module creates."
  type        = map(string)
  default     = {}
}
