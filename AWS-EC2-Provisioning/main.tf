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
 
 module "aws_instance"{
   source = "./modules/ec2"
   ami_id = "ami-0c2b8ca1dad447f8a"
   instance_type = "t2.micro"
}

/*resource "awsdynamodb_table"  "terraform_lock"{
  name          = "terraform-lock"
  billing_mode  = "PAY_PER_REQUEST"
  hash_key      = "LockID"


attribute (
  name = "LockID"
  type = "S"
}
}
