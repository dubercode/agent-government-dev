terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

# NOTA PARA EL CANDIDATO: este archivo es el arquetipo aprobado. No requiere credenciales reales de
# Azure para esta prueba — no se espera que ejecuten `terraform apply` contra un tenant real.
# Con `terraform validate` / `terraform plan` en modo local (sin backend remoto) es suficiente para
# demostrar que el .tfvars generado por el agente es sintácticamente correcto y respeta las variables.

provider "azurerm" {
  features {}
  skip_provider_registration = true
}

resource "azurerm_storage_account" "this" {
  name                            = replace(var.resource_name, "-", "")
  resource_group_name             = var.resource_group_name
  location                        = var.region
  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  https_traffic_only_enabled      = var.enable_https_traffic_only
  public_network_access_enabled   = var.public_network_access_enabled

  tags = {
    environment = var.environment
    criticidad  = var.criticidad
    workload    = var.workload
    managed_by  = "agente-devsecops-ia"
  }
}
