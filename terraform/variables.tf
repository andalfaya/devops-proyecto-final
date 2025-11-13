variable "env" {
  description = "Entorno de despliegue (dev, stg, prod)"
  type        = string
}

variable "backend_image" {
  description = "Imagen del backend (ej: ghcr.io/org/backend:tag)"
  type        = string
}

variable "frontend_image" {
  description = "Imagen del frontend (ej: ghcr.io/org/frontend:tag)"
  type        = string
}

variable "ports" {
  description = "Mapa de puertos por entorno"
  type = map(object({
    backend_nodeport  = number
    frontend_nodeport = number
  }))
  default = {
    dev = {
      backend_nodeport  = 8001
      frontend_nodeport = 8081
    }
    stg = {
      backend_nodeport  = 8101
      frontend_nodeport = 8181
    }
    prod = {
      backend_nodeport  = 8201
      frontend_nodeport = 8281
    }
  }
}
