output "environment" {
  description = "Environment this state manages."
  value       = var.environment
}

output "application_urls" {
  description = "Where the application is reachable on this machine."
  value       = module.app.urls
}

output "app_containers" {
  description = "Application container names."
  value       = module.app.container_names
}

output "database_container" {
  description = "Database container name."
  value       = docker_container.db.name
}

output "network" {
  description = "Docker network joining the containers."
  value       = docker_network.this.name
}
