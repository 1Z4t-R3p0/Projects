resource "aws_security_group" "ec2" {
  name        = "smart-citizen-ec2-sg"
  description = "Allow SSH and HTTP"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_key_pair" "main" {
  key_name   = "smart-citizen-key"
  public_key = file("${path.module}/../deploy_key.pub")
}

resource "aws_instance" "main" {
  ami                         = "ami-0522ab6e1ddcc7055" # Ubuntu 24.04 in ap-south-1
  instance_type               = "t2.micro"
  subnet_id                   = aws_subnet.public_1.id
  vpc_security_group_ids      = [aws_security_group.ec2.id]
  key_name                    = aws_key_pair.main.key_name
  associate_public_ip_address = true
  iam_instance_profile        = aws_iam_instance_profile.ec2_profile.name

  user_data = templatefile("${path.module}/user_data.sh", {
    DATABASE_URL  = "postgresql://citizen_admin:password123@${aws_db_instance.main.endpoint}/citizenreporter"
    S3_BUCKET     = aws_s3_bucket.uploads.id
    SNS_TOPIC_ARN = aws_sns_topic.alerts.arn
    AWS_REGION    = "ap-south-1"
    SECRET_KEY    = "production_secret_key_change_me"
  })

  tags = {
    Name = "smart-citizen-server"
  }

  depends_on = [aws_db_instance.main]
}

# IAM Role for EC2 to access S3 and SNS
resource "aws_iam_role" "ec2_role" {
  name = "smart-citizen-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_role_policy" "ec2_policy" {
  name = "smart-citizen-ec2-policy"
  role = aws_iam_role.ec2_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:PutObjectAcl",
          "s3:GetObject",
          "s3:DeleteObject"
        ]
        Resource = "${aws_s3_bucket.uploads.arn}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "sns:Publish"
        ]
        Resource = aws_sns_topic.alerts.arn
      },
      {
        Effect = "Allow"
        Action = [
          "rekognition:DetectLabels"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "smart-citizen-ec2-profile"
  role = aws_iam_role.ec2_role.name
}
