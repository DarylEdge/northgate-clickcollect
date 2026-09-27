# Provider and version pinning.
#
# Everything here is pinned deliberately. An unpinned provider means the
# infrastructure you get depends on the day you ran it, which defeats the
# purpose of describing it in code.

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

# No host is configured, so the provider uses the local Docker socket.
# This is why the laboratory needs a working container runtime.
provider "docker" {}
