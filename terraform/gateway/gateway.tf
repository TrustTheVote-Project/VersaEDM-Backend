locals {
  api_schema            = data.local_file.openapi_spec.content
  schema_yml            = yamldecode(local.api_schema)
  schema_name           = local.schema_yml.info.title
  schema_description    = local.schema_yml.info.description
  schema_version        = local.schema_yml.info.version
}

variable "env" {
  type = string
}

data "local_file" "openapi_spec" {
  filename = "${path.module}/../../schema/edm-api.yml"
}

resource "aws_iam_role" "cloudwatch_role" {
  name = "cloudwatch_role_${var.env}"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "apigateway.amazonaws.com"
        }
      },
    ]
  })
  inline_policy {
    name = "cloudwatch_role_policy"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Effect = "Allow"
          Action = [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:DescribeLogGroups",
            "logs:DescribeLogStreams",
            "logs:PutLogEvents",
            "logs:GetLogEvents",
            "logs:FilterLogEvents"
          ]
          Resource = "*"
        }
      ]
    })
  }
}

resource "aws_cloudwatch_log_group" "api_gateway_log_group" {
  name              = "api_gateway_log_group_${var.env}"
  retention_in_days = 180
}

resource "aws_api_gateway_account" "api_gateway_account" {
  cloudwatch_role_arn = aws_iam_role.cloudwatch_role.arn
}

resource "aws_apigatewayv2_api" "api_gateway" {
  name          = "${local.schema_name}_${var.env}"
  description   = local.schema_description
  protocol_type = "HTTP"
  body          = local.api_schema
  version       = local.schema_version
}

resource "aws_apigatewayv2_stage" "stage" {
  api_id        = aws_apigatewayv2_api.api_gateway.id
  name          = var.env
  auto_deploy   = false
  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gateway_log_group.arn
    format = <<-EOT
      { "requestId":"$context.requestId", "ip": "$context.identity.sourceIp", "requestTime":"$context.requestTime", "httpMethod":"$context.httpMethod","routeKey":"$context.routeKey", "status":"$context.status","protocol":"$context.protocol", "responseLength":"$context.responseLength" }
    EOT
  }
}

output "schema_version" {
  value = local.schema_version
}
