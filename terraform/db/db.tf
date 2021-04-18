# Variables
variable "region" {
  type = string
}

variable "env" {
  type = string
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