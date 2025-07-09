/*terraform {
  backend "s3" {
    bucket         = "bucketforterraformprojects"
    key            = "terraform/state/terraform.tfstate"
    region         = "eu-north-1"
    dynamodb_table = "Terraformtable"
    encrypt        = true
  }
}

 resource "aws_s3_bucket" "s3_bucket"{
      bucket = "Pranav's-s3-bucket"
   }

