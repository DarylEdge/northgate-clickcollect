# The environment.
#
# One network, one database with a persistent volume, and the application
# behind it. Everything is named from the project and environment, so two
# environments can run side by side on one machine without colliding.

locals {
  name_prefix = "${var.project}-${var.environment}"

  common_labels = {
    module      = "devops-l5"
    project     = var.project
    environment = var.environment
    managed_by  = "terraform"
  }
}

resource "docker_network" "this" {
  name = local.name_prefix

  labels {
    label = "environment"
    value = var.environment
  }
}

resource "docker_volume" "db_data" {
  name = "${local.name_prefix}-db-data"

  labels {
    label = "environment"
    value = var.environment
  }
}

resource "docker_image" "db" {
  name         = var.db_image
  keep_locally = true
}

resource "docker_container" "db" {
  name    = "${local.name_prefix}-db"
  image   = docker_image.db.image_id
  restart = "unless-stopped"
  memory  = var.db_memory_mb

  env = [
    "POSTGRES_DB=${var.db_name}",
    "POSTGRES_USER=${var.db_user}",
    "POSTGRES_PASSWORD=${var.db_password}",
  ]

  # The alias is how the application reaches the database. It does not need
  # an IP address, and it does not need a published port on the host.
  networks_advanced {
    name    = docker_network.this.name
    aliases = ["db"]
  }

  volumes {
    volume_name    = docker_volume.db_data.name
    container_path = "/var/lib/postgresql/data"
  }

  healthcheck {
    test     = ["CMD-SHELL", "pg_isready -U ${var.db_user} -d ${var.db_name}"]
    interval = "10s"
    timeout  = "5s"
    retries  = 5
  }

  dynamic "labels" {
    for_each = local.common_labels
    content {
      label = labels.key
      value = labels.value
    }
  }
}

module "app" {
  source = "./modules/app_service"

  project        = var.project
  environment    = var.environment
  image          = var.app_image
  instance_count = var.app_instance_count
  host_port      = var.app_host_port
  memory_mb      = var.app_memory_mb
  network_name   = docker_network.this.name
  labels         = local.common_labels

  database_url = "postgresql://${var.db_user}:${var.db_password}@db:5432/${var.db_name}"

  depends_on = [docker_container.db]
}
