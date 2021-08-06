resource "aws_iam_role" "cloudwatch_role" {
  name = "cloudwatch_role_pipeline_gateway"
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
  name              = "api_gateway_log_group_pipeline"
  retention_in_days = 180
}

resource "aws_api_gateway_account" "api_gateway_account" {
  cloudwatch_role_arn = aws_iam_role.cloudwatch_role.arn
}

resource "aws_apigatewayv2_api" "api_gateway" {
  name          = "gateway_pipeline"
  description   = "Accepts webhook requests"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "stage" {
  api_id        = aws_apigatewayv2_api.api_gateway.id
  name          = "build"
  auto_deploy   = false
  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gateway_log_group.arn
    format = <<-EOT
      { "requestId":"$context.requestId", "ip": "$context.identity.sourceIp", "requestTime":"$context.requestTime", "httpMethod":"$context.httpMethod","routeKey":"$context.routeKey", "status":"$context.status","protocol":"$context.protocol", "responseLength":"$context.responseLength" }
    EOT
  }
}

resource "aws_apigatewayv2_route" "webhook_endpoint" {
  api_id = aws_apigatewayv2_api.api_gateway.id
  route_key = "$default"
}

resource "aws_ecr_repository" "build_pipeline_repo" {
  name = "versaedm_build_pipeline_repo"
  image_tag_mutability = "IMMUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
}

output "gateway_url" {
  value = aws_apigatewayv2_api.api_gateway.api_endpoint
}