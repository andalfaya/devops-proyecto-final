provider "kubernetes" {
  config_path = "~/.kube/config"
}

resource "kubernetes_namespace" "ns" {
  metadata {
    name = var.env
  }
}