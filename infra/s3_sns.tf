resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "uploads" {
  bucket = "smart-citizen-uploads-${random_id.bucket_suffix.hex}"

  tags = {
    Name = "smart-citizen-uploads"
  }
}

resource "aws_s3_bucket_public_access_block" "uploads" {
  bucket = aws_s3_bucket.uploads.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_sns_topic" "alerts" {
  name = "smart-citizen-alerts"
}
