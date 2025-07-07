variable "instance_type"{
  type     = string
  default  = "t2.micro"
}

variable "ami_id"{
  type     = string
}

provider "aws"{
  region   = "us-east-1"
}

resource "aws_instance" "example_instance" {
  ami           = var.ami_id
  instance_type = var.instance_type
}

