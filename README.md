# agent-government-dev
Repositorio principal del agente de gobierno cloud desarrollado para XpertGroup.

Estructura del repositorio.
agent-government-dev/
│
├── app.py ---------------------------> Layer 1 - Entry Point
├── cli.py ---------------------------> Layer 2 - Orchestration
├── requirements.txt
│
├── agent/
│   ├── nlu/
│   │   └── intent_parser.py-----------> Layer 3 - Intent Parsing / NLU
│   ├── actions/
│   │   ├── inventory.py
│   │   ├── terraform_generator.py
│   │   └── remediation.py
│   └── validation/
│       ├── tfvars_validator.py
│       └── remediation_validator.py
│
├── dataset/
│   ├── inventory.json
│   ├── costs.json
│   └── security_findings.json
│
├── generated/
│   └── terraform.tfvars
│
└── arquetipo-storage-consumidor/


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

La arquitectura permanecería igual; únicamente cambiarían los adaptadores hacia servicios reales.
