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

# Define an output variable to expose the public IP address of the EC2 instance
output "public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.example_instance.public_ip
}
