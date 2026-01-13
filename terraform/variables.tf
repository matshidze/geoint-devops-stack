variable "postgres_db" { type = string  default = "appdb" }
variable "postgres_user" { type = string default = "geointuser" }
variable "postgres_password" { type = string default = "geointpass" }
variable "app_image" { type = string default = "geoint-demo-app:local" }
