
output "instance_id"{
  description = "The ID of the instance is" 
  value       = aws_instance.example.id
}

output "public_ip"{ 
  description = "The public_ip is" 
  value       = aws_instance.example.public_ip 
}

output "private_public"{
  description = "The private_ip is"
  value       = aws_instance.example.private_ip
}

output "availability_zone"{ 
  description = "The availability zone is"
  value       = aws_instance.example.availability_zone 
}

