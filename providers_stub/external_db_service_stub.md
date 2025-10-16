# External DB service (stub)

Endpoint esperado por `app.py`:

GET /api/v1/query

Respuesta esperada JSON:
{
  "db": "demo-db",
  "last_updated": "2025-10-15T12:00:00Z",
  "stats": {
    "total_items": 1234,
    "recent_prs": 5
  }
}

Para la demo, el orchestrator puede asumir que `https://other-repo.example.com/api/v1/query`
devuelve la estructura anterior.
