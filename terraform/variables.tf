variable "db_host" {
  description = "Database host"
  type        = string
  default     = ""
}

variable "db_user" {
  description = "Database user"
  type        = string
  default     = ""
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
  default     = ""
}

variable "db_port" {
  description = "Database port"
  type        = string
  default     = "3306"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}
