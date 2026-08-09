"""
Nexus-Hub — Backend API (Cloud Run)
====================================

Petit service Flask servi par Cloud Run et exposé au frontend
(Firebase Hosting) via une réécriture `/api/**` -> Cloud Run.

Endpoints :
  GET /api/health    -> état du service (liveness/readiness)
  GET /api/status    -> statut synthétique du "Core" (pour le ticker / footer)
  GET /api/followers -> nombre d'abonnés Instagram (avec cache + fallback)

Variables d'environnement :
  INSTA_USERNAME     -> nom d'utilisateur Instagram (def: merickkn)
  INSTA_SESSION_ID   -> cookie de session Instagram (secret, optionnel)
  FOLLOWERS_TTL      -> durée de cache en secondes (def: 1800 = 30 min)
  PORT               -> port d'écoute (fourni automatiquement par Cloud Run)
"""

import json
import os
import time

import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
# CORS ouvert : le frontend peut aussi appeler l'API directement en dev.
CORS(app)

USERNAME = os.environ.get("INSTA_USERNAME", "merickkn")
SESSION_ID = os.environ.get("INSTA_SESSION_ID", "")
CACHE_TTL = int(os.environ.get("FOLLOWERS_TTL", "1800"))

# Fallback embarqué : la dernière valeur connue est copiée dans l'image.
FALLBACK_FILE = os.path.join(os.path.dirname(__file__), "followers_data.json")

# Cache mémoire simple (le conteneur Cloud Run reste chaud entre les requêtes).
_cache = {"data": None, "fetched_at": 0}


def _read_fallback():
    """Retourne la dernière valeur connue embarquée dans l'image."""
    try:
        with open(FALLBACK_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            data["status"] = "fallback_static"
            return data
    except Exception:
        return {"followers": 0, "status": "fallback_missing", "timestamp": int(time.time())}


def _fetch_from_instagram():
    """Interroge l'API web d'Instagram. Nécessite INSTA_SESSION_ID."""
    if not SESSION_ID:
        raise ValueError("INSTA_SESSION_ID non configuré")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "X-IG-App-ID": "936619743392459",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": f"https://www.instagram.com/{USERNAME}/",
        "X-ASBD-ID": "129477",
        "X-IG-WWW-Claim": "0",
    }
    cookies = {"sessionid": SESSION_ID, "csrftoken": "missing"}

    url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={USERNAME}"
    resp = requests.get(url, headers=headers, cookies=cookies, timeout=15)
    resp.raise_for_status()

    user = resp.json().get("data", {}).get("user", {})
    followers = None
    if "edge_followed_by" in user:
        followers = user["edge_followed_by"].get("count")
    elif "follower_count" in user:
        followers = user["follower_count"]

    if followers is None:
        raise ValueError("Nombre d'abonnés introuvable dans la réponse")

    return {"followers": followers, "status": "success", "timestamp": int(time.time())}


def _get_followers():
    """Renvoie les abonnés depuis le cache, l'API, ou le fallback statique."""
    now = time.time()
    if _cache["data"] and (now - _cache["fetched_at"] < CACHE_TTL):
        cached = dict(_cache["data"])
        cached["cached"] = True
        return cached

    try:
        data = _fetch_from_instagram()
    except Exception as exc:  # réseau, session expirée, rate-limit…
        app.logger.warning("Fetch Instagram échoué: %s", exc)
        data = _read_fallback()

    _cache["data"] = data
    _cache["fetched_at"] = now
    data = dict(data)
    data["cached"] = False
    return data


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "nexus-hub-api", "time": int(time.time())})


@app.get("/api/status")
def status():
    """Statut synthétique consommable par le frontend (ticker / footer)."""
    return jsonify(
        {
            "core": "stable",
            "uptime": "99.9%",
            "version": "V4",
            "time": int(time.time()),
        }
    )


@app.get("/api/followers")
def followers():
    return jsonify(_get_followers())


@app.get("/")
def root():
    return jsonify({"service": "nexus-hub-api", "docs": "/api/health, /api/status, /api/followers"})


if __name__ == "__main__":
    # Exécution locale : `python backend/main.py`
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
