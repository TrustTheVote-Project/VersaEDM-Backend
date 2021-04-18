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
  region = var.region
  env = var.env
}

module "gateway" {
  source="./gateway"
  env = var.env
}