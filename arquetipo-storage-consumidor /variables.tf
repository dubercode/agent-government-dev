variable "resource_name" {
  description = "Nombre del recurso, debe seguir convención st-<workload>-<environment>-<uso>"
  type        = string
}

variable "resource_group_name" {
  description = "Resource group destino (debe existir previamente)"
  type        = string
}

variable "region" {
  description = "Región de Azure"
  type        = string
  default     = "eastus2"
}

variable "environment" {
  description = "prod | dev | qa"
  type        = string
}

variable "criticidad" {
  description = "alta | media | baja"
  type        = string
}

variable "workload" {
  description = "Nombre del workload/dueño lógico del recurso"
  type        = string
}

variable "enable_https_traffic_only" {
  description = "Debe ser true en todos los casos (control de seguridad obligatorio)"
  type        = bool
  default     = true
}

variable "public_network_access_enabled" {
  description = "Debe ser false para cualquier recurso con criticidad alta o media"
  type        = bool
  default     = false
}
