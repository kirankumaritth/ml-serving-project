provider "kubernetes" {
  config_path = "~/.kube/config"
}

resource "kubernetes_namespace" "ml_ns" {
  metadata {
    name = "ml-serving"
  }
}
