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

variable "env" {
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
module "network" {
  source = "./network"
}
module "db" {
  source = "./db"
  db_creds_secret_name = var.db_creds_secret_name
  region = var.region
  env = var.env
  vpc_id = module.network.vpc.id
  ingress_cidr = module.network.vpc.cidr_block
}

module "gateway" {
  source="./gateway"
  env = var.env
}