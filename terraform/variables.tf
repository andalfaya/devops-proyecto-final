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
      backend_nodeport  = 8001
      frontend_nodeport = 8081
      nodeexporter_nodeport = 8091
    }
    stg = {
      backend_nodeport  = 8101
      frontend_nodeport = 8181
      nodeexporter_nodeport = 8191
    }
    prod = {
      backend_nodeport  = 8201
      frontend_nodeport = 8281
      nodeexporter_nodeport = 8291
    }
  }
}
