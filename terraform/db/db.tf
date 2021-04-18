# Variables
variable "region" {
  type = string
}

variable "env" {
  type = string
}

variable "db_creds_secret_name" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "ingress_cidr" {
  type = string
}

locals {
  db_creds = jsondecode(
  data.aws_secretsmanager_secret_version.db_creds.secret_string
  )
}

data "aws_secretsmanager_secret_version" "db_creds" {
  # Fill in the name you gave to your secret
  secret_id = aws_secretsmanager_secret.db_creds.id
}

# Resources
resource "aws_dynamodb_table" "dynamo_store" {
  name = "versaedm-dynamo-${var.env}"
  hash_key = "uid"
  billing_mode = "PAY_PER_REQUEST"

  attribute {
    name = "uid"
    type = "S"
  }
}
resource "aws_secretsmanager_secret" "db_creds" {
  description   = "Admin credentials for the Aurora instance on ${var.env}"
  name          = var.db_creds_secret_name
}
resource "aws_rds_cluster" "versa_pg_cluster" {
  apply_immediately = true
  availability_zones = ["${var.region}a", "${var.region}b", "${var.region}c"]
  cluster_identifier = "versaedm-pg-${var.env}"
  database_name = "versa_edm"
  enable_http_endpoint = true
  engine = "aurora-postgresql"
  engine_mode = "serverless"
  engine_version = "10.12"
  master_password = local.db_creds.db_master_password
  master_username = local.db_creds.db_master_username
  skip_final_snapshot = true
  vpc_security_group_ids = [aws_security_group.rds_vpc.id]
}
resource "aws_security_group" "rds_vpc" {
  name = "rds_vpc"
  description = "Allow connection to RDS instance"
  vpc_id = var.vpc_id

  ingress {
    description = "RDS Port"
    from_port = 5432
    to_port = 5432
    protocol = "tcp"
    cidr_blocks = [var.ingress_cidr]
  }
}