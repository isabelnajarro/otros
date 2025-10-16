# iask_me-demo

Repo demo que simula el servicio `iask_me` para integrarlo con el orchestrator.

Características:
- API con 5 endpoints descritos en `openapi.yaml`.
- `config.yml` y `models.yml` con la configuración y el modelo de IA usado.
- Código Flask (`app.py`) que muestra cómo el servicio usa S3 (boto3) y consulta una BBDD remota (simulada).
- Incluye endpoint `/openapi.yaml` que sirve la especificación en caliente (útil para que el orchestrator la lea por URL).
- Contiene `Dockerfile` y `Makefile` para levantar la demo rápidamente.

Nota: este repo es **solo demo**; puedes construir y ejecutar el contenedor localmente para que tu orchestrator lo consulte.
