data "github_repository" "versaedm_backend_repo" {
  full_name = "${var.github_project}/${var.github_repo_name}"
}