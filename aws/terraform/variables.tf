# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

variable "region" {
  description = "AWS region"
  type        = string
  default     = "eu-central-1"
}

variable "access_key" {
  description = "AWS auth"
  sensitive = true
  type = string
}

variable "secret_key" {
  description = "AWS auth"
  type = string
  sensitive = true
}

variable "ubuntu_subnet" {
  type = string
}

variable "windows_subnet" {
  type = string
}