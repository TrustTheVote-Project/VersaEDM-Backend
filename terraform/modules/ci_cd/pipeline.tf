data "template_file" "buildspec" {
  template = file("${path.module}/buildspec.yml")
  vars = {
  }
}

resource "aws_ecr_repository" "build_pipeline_repo" {
  name = "versaedm_build_pipeline_repo"
  image_tag_mutability = "IMMUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_iam_role" "codepipeline_role" {
  name = "test-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "codepipeline.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "codepipeline_policy" {
  name = "codepipeline_policy"
  role = aws_iam_role.codepipeline_role.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect":"Allow",
      "Action": [
        "s3:GetObject",
        "s3:GetObjectVersion",
        "s3:GetBucketVersioning",
        "s3:PutObjectAcl",
        "s3:PutObject"
      ],
      "Resource": [
        "${aws_s3_bucket.codepipeline_bucket.arn}",
        "${aws_s3_bucket.codepipeline_bucket.arn}/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "codebuild:BatchGetBuilds",
        "codebuild:StartBuild"
      ],
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_s3_bucket" "codepipeline_bucket" {
  bucket = "versaedm-backend-pipeline-artifacts"
  acl    = "private"
}

resource "aws_codepipeline" "build_pipeline" {
  name = "versa-job"
  role_arn = aws_iam_role.codepipeline_role.arn

  artifact_store {
    location = aws_s3_bucket.codepipeline_bucket.bucket
    type = "S3"
  }

  stage {
    name = "Source"
    action {
      category = "Source"
      name = "Source"
      owner = "AWS"
      provider = "CodeStarSourceConnection"
      input_artifacts = []
      output_artifacts = ["source_artifact"]
      run_order = 1
      version = "1"

      configuration = {
        ConnectionArn = aws_codestarconnections_connection.github.arn
        FullRepositoryId = "${var.github_project}/${var.github_repo_name}"
        BranchName = "main"
      }
    }
  }

  stage {
    name = "Build"
    action {
      category = "Build"
      name = "Build"
      owner = "AWS"
      provider = "CodeBuild"
      version = "1"
      input_artifacts = ["source_artifact"]
      output_artifacts = ["build_artifact"]
      configuration = {
        "ProjectName" = "versaedm-backend-source"
      }
    }
  }
}

data "aws_iam_policy_document" "codebuild_trust" {
  statement {
    effect = "Allow"
    principals {
      identifiers = ["codebuild.amazonaws.com"]
      type = "Service"
    }
    actions = ["sts:AssumeRole"]
  }
}

resource aws_iam_role "build_phase_role" {
  name = "versaedm-build-phase"
  description = "Role assumed by CodeBuild during build phase of pipeline"
  assume_role_policy = data.aws_iam_policy_document.codebuild_trust.json
}

resource aws_cloudwatch_log_group "pipeline_log_group" {
  name = "/versaedm-backend/build-pipelines"
  retention_in_days = 60
}

resource aws_codebuild_project "source_phase" {
  name = "versaedm-backend-source"
  description = "Source phase for build pipeline"
  badge_enabled = false
  build_timeout = 60
  queued_timeout = 480

  service_role = aws_iam_role.build_phase_role.arn

  artifacts {
    type = "CODEPIPELINE"
    packaging = "NONE"
    override_artifact_name = false
    name = "versaedm-backend-source"
    encryption_disabled = false
  }

  environment {
    compute_type = "BUILD_GENERAL1_SMALL"
    image = "Ubuntu standard:5.0"
    image_pull_credentials_type = "CODEBUILD"
    type = "LINUX_CONTAINER"
    privileged_mode = false
  }

  logs_config {
    cloudwatch_logs {
      group_name = aws_cloudwatch_log_group.pipeline_log_group.name
      stream_name = "source"
    }
  }

  source {
    buildspec = data.template_file.buildspec.rendered
    git_clone_depth = 0
    insecure_ssl = false
    report_build_status = false
    type = "CODEPIPELINE"
  }
}