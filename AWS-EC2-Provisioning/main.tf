terraform{
   required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

  provider "aws"{
  region = "us-east-1"
}
 
 resource "aws_instance" "example"{
   ami = "ami-0c2b8ca1dad447f8a"
   instance_type = "t2.micro"
}
