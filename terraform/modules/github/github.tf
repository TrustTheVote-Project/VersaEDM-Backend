variable "webhook_url" {
  type = string
}

data "github_repository" "versaedm_backend_repo" {
  full_name = "TrustTheVote-Project/VersaEDM-Backend"
}

resource "github_repository_webhook" "push_webhook" {
  repository = data.github_repository.versaedm_backend_repo.name

  events = ["push"]

  configuration {
    url = var.webhook_url
  }
}