terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-2"
}

locals {
  api_schema            = data.local_file.openapi_spec.content
  schema_yml            = yamldecode(local.api_schema)
  schema_name           = local.schema_yml.info.title
  schema_description    = local.schema_yml.info.description
  schema_version        = local.schema_yml.info.version
}

data "local_file" "openapi_spec" {
  filename = "${path.module}/../schema/edm-api.yml"
}

resource "aws_apigatewayv2_api" "versa_edm_api_gateway" {
  name          = local.schema_name
  description   = local.schema_description
  protocol_type = "HTTP"
  body          = local.api_schema
  version       = local.schema_version
}

resource "aws_apigatewayv2_stage" "dev" {
  api_id        = aws_apigatewayv2_api.versa_edm_api_gateway.id
  name          = "dev"
  auto_deploy   = false
}

# TODO: Add CloudWatch log resources

output "schema_version" {
  value = local.schema_version
}