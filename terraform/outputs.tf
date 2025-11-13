output "backend_url" {
  value = "http://localhost:${var.ports[var.env].backend_nodeport}/api/health"
}

output "frontend_url" {
  value = "http://localhost:${var.ports[var.env].frontend_nodeport}/health"
}

output "backend_port" {
  value = "${var.ports[var.env].backend_nodeport}"
}

output "frontend_port" {
  value = "${var.ports[var.env].frontend_nodeport}"
}