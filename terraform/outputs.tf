output "frontend_url" {
  description = "Frontend accesible en localhost"
  value       = "http://localhost:${var.ports[var.env].frontend_nodeport}"
}

output "frontend_health_url" {
  description = "Endpoint de health del frontend en localhost"
  value       = "http://localhost:${var.ports[var.env].frontend_nodeport}/health"
}

output "backend_url" {
  description = "Backend accesible en localhost"
  value       = "http://localhost:${var.ports[var.env].backend_nodeport}"
}

output "backend_health_url" {
  description = "Endpoint de health del backend en localhost"
  value       = "http://localhost:${var.ports[var.env].backend_nodeport}/api/health"
}