resource "kubernetes_manifest" "backend_deployment" {
  manifest = yamldecode(templatefile("${path.module}/../k8s/backend-deployment.yaml", {
    backend_image = var.backend_image,
    env           = var.env
  }))
}

resource "kubernetes_manifest" "backend_service" {
  manifest = yamldecode(templatefile("${path.module}/../k8s/backend-service.yaml", {
    env              = var.env,
    backend_nodeport = var.ports[var.env].backend_nodeport
  }))
}

resource "kubernetes_manifest" "frontend_deployment" {
  manifest = yamldecode(templatefile("${path.module}/../k8s/frontend-deployment.yaml", {
    frontend_image = var.frontend_image,
    env            = var.env
  }))
}

resource "kubernetes_manifest" "frontend_service" {
  manifest = yamldecode(templatefile("${path.module}/../k8s/fontend-service.yaml", {
    env               = var.env,
    frontend_nodeport = var.ports[var.env].frontend_nodeport
  }))
}

resource "kubernetes_manifest" "postgres_statefulset" {
  manifest = yamldecode(file("${path.module}/../k8s/postgres-statefulset.yaml"))
}

resource "kubernetes_manifest" "postgres_service" {
  manifest = yamldecode(templatefile("${path.module}/../k8s/postgres-service.yaml", {
    env = var.env
  }))
}