terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 3.30.0"
    }
    github = {
      source  = "integrations/github"
      version = "~> 4.0"
    }
  }
  backend "s3" {
    bucket = "trustthevote-versaedm-tfstate"
    key = "backend/main.tfstate"
    region = "us-east-2"

    workspaces = {
      name = "dev"
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

variable "github_token" {
  type = string
}

variable "github_project" {
  type = string
}

variable "github_repo" {
  type = string
}

# Configure the AWS Provider
provider "aws" {
  region = var.region
}

# Configure the GitHub Provider
provider "github" {
  token = var.github_token
  owner = var.github_project
}

# Modules
module "pipeline" {
  source = "./modules/pipeline"
  vpc_id = module.network.vpc.id
  github_token = var.github_token
  repository_owner = var.github_project
  repository_name = var.github_repo
}

module "network" {
  source = "./modules/network"
}
module "db" {
  source = "./modules/db"
  region = var.region
  env = var.env
}

module "gateway" {
  source="./modules/gateway"
  env = var.env
}

module "github" {
  source="./modules/github"
  webhook_url = module.pipeline.webhook_url
  github_project = var.github_project
  github_repo_name = var.github_repo
  github_token = var.github_token
}