terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>5.37.0"
    }
  }

  backend "s3" {
    bucket         = "terraform-state-files-marko"
    key            = "py-ts-rust/terraform.tfstate"
    region         = "ap-southeast-2"
    encrypt        = true
    dynamodb_table = "terraform-state-lock-table"
  }

}

provider "aws" {
  region = "ap-southeast-2"
}
