resource "aws_default_vpc" "default" {}

output "vpc" {
  value = aws_default_vpc.default
}