terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

resource "docker_network" "app_net" {
  name = "geoint_app_net"
}

resource "docker_volume" "pgdata" {
  name = "geoint_pgdata"
}

resource "docker_image" "app" {
  name = var.app_image
  build {
    context    = "${path.module}/.."
    dockerfile = "${path.module}/../Dockerfile"
  }
}

resource "docker_container" "db" {
  name  = "geoint-db"
  image = "postgres:16"

  networks_advanced { name = docker_network.app_net.name }

  env = [
    "POSTGRES_DB=${var.postgres_db}",
    "POSTGRES_USER=${var.postgres_user}",
    "POSTGRES_PASSWORD=${var.postgres_password}",
  ]

  volumes {
    volume_name    = docker_volume.pgdata.name
    container_path = "/var/lib/postgresql/data"
  }
}

resource "docker_container" "app" {
  name  = "geoint-app"
  image = docker_image.app.name

  networks_advanced { name = docker_network.app_net.name }

  env = [
    "POSTGRES_DB=${var.postgres_db}",
    "POSTGRES_USER=${var.postgres_user}",
    "POSTGRES_PASSWORD=${var.postgres_password}",
    "POSTGRES_HOST=geoint-db",
    "POSTGRES_PORT=5432",
    "APP_HOST=0.0.0.0",
    "APP_PORT=5000",
  ]

  ports {
    internal = 5000
    external = 5000
  }

  depends_on = [docker_container.db]
}
