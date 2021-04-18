resource "aws_ecr_repository" "build_pipeline_repo" {
  name = "versaedm_build_pipeline_repo"
  image_tag_mutability = "IMMUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
}