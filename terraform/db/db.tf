# Variables
variable "region" {
  type = string
}

variable "prefix" {
  type = string
}

variable "db_creds_secret_name" {
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
resource "aws_secretsmanager_secret" "db_creds" {
  description   = "Admin credentials for the Aurora instance on ${var.prefix}"
  name          = var.db_creds_secret_name
}
resource "aws_rds_cluster" "pg_dev" {
  cluster_identifier = "versaedm-pg-${var.prefix}"
  engine = "aurora-postgresql"
  availability_zones = ["${var.region}a", "${var.region}b"]
  database_name = "versa_edm"
  master_username = local.db_creds.db_master_username
  master_password = local.db_creds.db_master_password
}