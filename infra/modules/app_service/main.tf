# Application service module.
#
# Wraps "run N copies of this image on this network" so the root module does
# not have to care how it happens. This is the smallest useful example of the
# reuse that turns into internal platform capability at scale.

terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

resource "docker_image" "app" {
  name         = var.image
  keep_locally = true
}

resource "docker_container" "app" {
  count = var.instance_count

  name    = "${var.project}-${var.environment}-app-${count.index + 1}"
  image   = docker_image.app.image_id
  restart = "unless-stopped"
  memory  = var.memory_mb

  env = [
    "DATABASE_URL=${var.database_url}",
    "PORT=${var.container_port}",
    "ENVIRONMENT=${var.environment}",
  ]

  networks_advanced {
    name = var.network_name
  }

  ports {
    internal = var.container_port
    external = var.host_port + count.index
  }

  dynamic "labels" {
    for_each = var.labels
    content {
      label = labels.key
      value = labels.value
    }
  }
}
