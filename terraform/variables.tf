# ============================================================
# Variables - Things that change between environments
# ============================================================

variable "aws_region" {
  description = "AWS region to deploy in"
  default     = "ap-south-1"  # Mumbai
}

variable "app_name" {
  description = "Name of the application"
  default     = "ai-assistant"
}

variable "app_port" {
  description = "Port the app runs on"
  default     = 8000
}

variable "app_count" {
  description = "Number of containers to run"
  default     = 2  # Minimum 2 for high availability
}

variable "openai_api_key_arn" {
  description = "ARN of the OpenAI API key in AWS Secrets Manager"
  type        = string
}
