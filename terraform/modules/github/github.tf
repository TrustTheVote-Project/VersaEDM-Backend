variable "webhook_url" {
  type = string
}

variable "github_webhook_token" {
  type = string
}

variable "github_project" {
  type = string
}

variable "github_repo_name" {
  type = string
}

data "github_repository" "versaedm_backend_repo" {
  full_name = "${var.github_project}/${var.github_repo_name}"
}

resource "github_repository_webhook" "push_webhook" {
  repository = data.github_repository.versaedm_backend_repo.name

  events = ["push"]

  configuration {
    url = var.webhook_url
    insecure_ssl = "0"
    content_type = "json"
    secret = var.github_webhook_token
  }
}