# agent-government-dev
Repositorio principal del agente de gobierno cloud desarrollado para XpertGroup.
Cloud Governance Agent es un agente de gobierno cloud desarrollado en Python que simula la operación segura de un entorno Azure mediante lenguaje natural, siguiendo una arquitectura modular por capas inspirada en sistemas de IA agentica. El proyecto separa claramente la comprensión del lenguaje (intent_parser.py), la lógica de negocio (actions), las validaciones (validation) y la orquestación (cli.py), aplicando principios como Single Responsibility, Human-in-the-Loop y Zero Trust. A partir de un inventario cloud, históricos de costos y hallazgos de seguridad simulados, el agente puede consultar recursos, detectar anomalías de costo, generar archivos terraform.auto.tfvars compatibles con un arquetipo de Terraform y proponer remediaciones que requieren confirmación humana antes de considerarse ejecutadas.


# Cloud Governance Agent

Mini agente de gobierno cloud desarrollado como solución al reto técnico de XpertGroup.

## Objetivo

El agente permite operar un entorno Azure simulado mediante lenguaje natural, aplicando principios de Platform Engineering, Infrastructure as Code y Zero Trust.

## Arquitectura

El proyecto sigue una arquitectura por capas.

```text
Usuario
   │
app.py
   │
cli.py
   │
intent_parser.py
   │
Actions
   ├── inventory.py
   ├── cost_anomaly.py
   ├── terraform_generator.py
   └── remediation.py
   │
Validation
   ├── tfvars_validator.py
   └── remediation_validator.py
```

Cada capa tiene una única responsabilidad, reduciendo el acoplamiento y facilitando el mantenimiento.

## Capacidades

* Consultar inventario cloud.
* Detectar anomalías de costo.
* Generar `terraform.auto.tfvars`.
* Proponer remediaciones con aprobación humana.

## Instalación

Requisitos:

* Python 3.11+
* Entorno virtual recomendado.

### Crear entorno

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Ejecutar

```bash
python3 app.py
```

## Ejemplos de uso

### Inventario

```text
¿Qué recursos del grupo rg-ops-prod son críticos?
```

### Costos

```text
Detecta anomalías de costo.
```

### Terraform

```text
Genera una Storage Account para logs en dev.
```

### Seguridad

```text
Muéstrame F-001.
Remedia F-001.
Muéstrame los hallazgos de seguridad.
```

## Validaciones implementadas

### Terraform

* existencia del archivo generado;
* validación de variables;
* advertencias para producción.

### Seguridad

* validación del hallazgo;
* separación entre lectura y propuesta;
* confirmación humana obligatoria.

## Escalabilidad

En un entorno real esta arquitectura evolucionaría reemplazando:

| Simulación             | Azure                |
| ---------------------- | -------------------- |
| inventory.json         | Azure Resource Graph |
| costs.json             | Cost Management API  |
| security_findings.json | Defender API         |
| CLI                    | API REST             |
| Archivos               | Cosmos DB            |
| Logs                   | Application Insights |

