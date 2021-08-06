data "aws_iam_policy_document" "webhook_lambda_permissions" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      identifiers = ["lambda.amazonaws.com"]
      type = "Service"
    }
  }
}

resource "aws_iam_role" "webhook_role" {
  name = "versaedm-webhook"
  assume_role_policy = data.aws_iam_policy_document.webhook_lambda_permissions.json
}

resource "aws_iam_role_policy_attachment" "webhook_lambda_vpc_access" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
  role = aws_iam_role.webhook_role.id
}

resource "aws_iam_role_policy_attachment" "webhook_lambda_execution" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role = aws_iam_role.webhook_role.id
}