variable "vpc_id" {
  type = string
}

resource aws_security_group "pipeline_launcher" {
  name = "codepipeline-launcher"
  egress {
    from_port = 443
    to_port = 443
    cidr_blocks = ["0.0.0.0/0"]
    protocol = "tcp"
  }
  vpc_id = var.vpc_id
}

locals {
  lambda_name = "pipeline"
  lambda_dir = "${path.module}/../../lambdas/${local.lambda_name}"
}

resource "null_resource" "zip_lambda" {
  triggers = {
    manifest_sha1 = sha1(file("${local.lambda_dir}/main.py"))
  }
  provisioner "local-exec" {
    interpreter = ["/bin/bash", "-c"]
    command     = <<EOF
cd "${local.lambda_dir}"; zip "${local.lambda_name}.${null_resource.zip_lambda.id}.zip" main.py
EOF
  }
}

resource "aws_lambda_function" "pipeline_launcher" {
  function_name = "pipeline-launcher"
  handler = "main.lambda_handler"
  role = aws_iam_role.webhook_role.arn
  runtime = "python3.8"
  filename = "${local.lambda_dir}/${local.lambda_name}.${null_resource.zip_lambda.id}.zip"
}