output "container_names" {
  description = "Names of the application containers created."
  value       = docker_container.app[*].name
}

output "urls" {
  description = "Host URLs for each application instance."
  value       = [for i in range(var.instance_count) : "http://localhost:${var.host_port + i}"]
}
