resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "uploads" {
  bucket = "smart-citizen-uploads-${random_id.bucket_suffix.hex}"

  tags = {
    Name = "smart-citizen-uploads"
  }
}

resource "aws_s3_bucket_ownership_controls" "uploads" {
  bucket = aws_s3_bucket.uploads.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "uploads" {
  depends_on = [aws_s3_bucket_ownership_controls.uploads, aws_s3_bucket_public_access_block.uploads]

  bucket = aws_s3_bucket.uploads.id
  acl    = "public-read"
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
