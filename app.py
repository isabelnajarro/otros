#!/usr/bin/env python3
# app.py - demo Flask app (serves openapi.yaml at /openapi.yaml)
from flask import Flask, request, jsonify, send_file, abort, Response
import yaml
import os
import requests
import boto3
from pathlib import Path

# cargar config
CFG_PATH = os.path.join(os.path.dirname(__file__), "config.yml")
with open(CFG_PATH, "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

S3_BUCKET = cfg.get("s3", {}).get("bucket")
EXTERNAL_DB_URL = cfg.get("external_db", {}).get("service_url")

# boto3 client (demo)
try:
    s3_client = boto3.client("s3")  # en demo asumimos credenciales por env
except Exception:
    s3_client = None

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status":"ok", "app": cfg.get("app", {})}), 200

@app.route("/openapi.yaml", methods=["GET"])
def serve_openapi():
    path = os.path.join(os.path.dirname(__file__), "openapi.yaml")
    if os.path.exists(path):
        return send_file(path, mimetype='application/x-yaml')
    return abort(404)

@app.route("/search", methods=["POST"])
def search():
    body = request.get_json() or {}
    q = body.get("query","")
    # Demo: retornamos un resultado ficticio
    return jsonify({"results":[{"id":"doc1","score":0.95,"snippet":"Resultado simulado para: "+q}]}), 200

@app.route("/items", methods=["GET"])
def list_items():
    page = int(request.args.get("page", 1))
    items = [{"id":"1", "name":"item-A"}, {"id":"2", "name":"item-B"}]
    return jsonify({"page":page,"items":items}), 200

@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json() or {}
    name = data.get("name","untitled")
    payload = data.get("payload","")
    # Demo: subir 'payload' a S3
    if S3_BUCKET and s3_client:
        key = f"demo/{name}.txt"
        try:
            s3_client.put_object(Bucket=S3_BUCKET, Key=key, Body=payload.encode("utf-8"))
            s3_url = f"s3://{S3_BUCKET}/{key}"
        except Exception as e:
            s3_url = f"ERROR: {e}"
    else:
        s3_url = "S3 not configured or boto3 missing"
    return jsonify({"id": "demo-1", "name": name, "s3_url": s3_url}), 201

@app.route("/models/info", methods=["GET"])
def model_info():
    # leer models.yml
    import yaml, os
    path = os.path.join(os.path.dirname(__file__), "models.yml")
    with open(path, "r", encoding="utf-8") as f:
        m = yaml.safe_load(f)
    return jsonify(m.get("model", {})), 200

@app.route("/admin/stats", methods=["GET"])
def admin_stats():
    try:
        resp = requests.get(EXTERNAL_DB_URL, timeout=6)
        resp.raise_for_status()
        return jsonify({"source":"external_db", "data": resp.json()}), 200
    except Exception as e:
        return jsonify({"error":"could not query external DB", "detail": str(e)}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
