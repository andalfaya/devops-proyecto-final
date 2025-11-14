variable "env" {
  description = "Entorno de despliegue (dev, stg, prod)"
  type        = string
  default     = ""
}

variable "backend_image" {
  description = "Imagen del backend (ej: ghcr.io/org/backend:tag)"
  type        = string
  default     = ""
}

variable "frontend_image" {
  description = "Imagen del frontend (ej: ghcr.io/org/frontend:tag)"
  type        = string
  default     = ""
}

variable "ports" {
  description = "Mapa de puertos por entorno"
  type = map(object({
    backend_nodeport  = number
    frontend_nodeport = number
    nodeexporter_nodeport = number
  }))
  default = {
    dev = {
      backend_nodeport  = 8101
      frontend_nodeport = 8181
      nodeexporter_nodeport = 8191
    }
    stg = {
      backend_nodeport  = 8201
      frontend_nodeport = 8281
      nodeexporter_nodeport = 8291
    }
    prod = {
      backend_nodeport  = 8301
      frontend_nodeport = 8381
      nodeexporter_nodeport = 8391
    }
  }
}

variable "replicas" {
  description = "replicas por entorno"
  type = map(object({
    backend_replicas       = number
    frontend_replicas      = number
    postgres_replicas      = number
    node_exporter_replicas = number
  }))
  default = {
    dev = {
      backend_replicas       = 1
      frontend_replicas      = 1
      postgres_replicas      = 1
      node_exporter_replicas = 1
    }
    stg = {
      backend_replicas       = 1
      frontend_replicas      = 1
      postgres_replicas      = 1
      node_exporter_replicas = 1
    }
    prod = {
      backend_replicas       = 1
      frontend_replicas      = 1
      postgres_replicas      = 1
      node_exporter_replicas = 1
    }
  }
}
