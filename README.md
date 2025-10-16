# Project AI

Características:
- API con 5 endpoints descritos en `openapi.yaml`.
- `config.yml` y `models.yml` con la configuración y el modelo de IA usado.
- Código Flask (`app.py`) que muestra cómo el servicio usa S3 (boto3) y consulta una BBDD remota (simulada).
- Incluye endpoint `/openapi.yaml` que sirve la especificación en caliente (útil para que el orchestrator la lea por URL).
- Contiene `Dockerfile` y `Makefile` para levantar la demo rápidamente.

