output "ec2_ip" {
  value = aws_instance.main.public_ip
}

output "rds_endpoint" {
  value = aws_db_instance.main.endpoint
}

output "s3_bucket" {
  value = aws_s3_bucket.uploads.id
}

output "sns_topic_arn" {
  value = aws_sns_topic.alerts.arn
}
