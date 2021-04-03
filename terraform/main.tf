terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 3.30.0"
    }
  }
}

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

# Configure the AWS Provider
provider "aws" {
  region = var.region
}

# Modules
module "db" {
  source = "./db"
  db_creds_secret_name = var.db_creds_secret_name
  region = var.region
  prefix = var.prefix
}

module "gateway" {
  source="./gateway"
  prefix = var.prefix
}