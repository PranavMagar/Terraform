output "instance_id" {
  description = "The ID of the instance is"
  value       = aws_instance.example_instance.id
}

output "public_ip" {
  description = "The public IP is"
  value       = aws_instance.example_instance.public_ip
}

output "private_ip" {
  description = "The private IP is"
  value       = aws_instance.example_instance.private_ip
}

output "availability_zone" {
  description = "The availability zone is"
  value       = aws_instance.example_instance.availability_zone
}


