"""
Récupération du nombre d'abonnés Instagram via instagrapi.
=========================================================

Fonctionne même pour un compte privé : c'est TON compte qui se connecte.

Authentification (par ordre de préférence) :
  1. INSTA_SESSION_ID       -> cl.login_by_sessionid(...)   (recommandé, réutilise
                               le cookie de session, aucun mot de passe en clair)
  2. INSTA_USERNAME + INSTA_PASSWORD  -> cl.login(...)      (peut déclencher un
                               challenge/2FA depuis une nouvelle IP comme la CI)

Un fichier de session (settings) est mis en cache pour limiter les reconnexions.

Sortie : fils/followers_data.json
  { "timestamp": <epoch>, "followers": <int>, "status": "<str>" }
"""

import json
import os
import time

USERNAME = os.environ.get("INSTA_USERNAME", "merickn")
SESSION_ID = os.environ.get("INSTA_SESSION_ID", "")
PASSWORD = os.environ.get("INSTA_PASSWORD", "")

OUTPUT_FILE = "fils/followers_data.json"
SETTINGS_FILE = "insta_settings.json"  # cache de session (device + tokens)


def _read_old_followers():
    """Dernière valeur connue, pour ne pas repartir de zéro en cas d'échec."""
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as fh:
            return int(json.load(fh).get("followers", 0))
    except Exception:
        return 0


def _save(data):
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=4)
    print(f"💾 Écrit {OUTPUT_FILE} : {data['followers']} abonnés (status={data['status']})")


def fetch_followers():
    data = {"timestamp": int(time.time()), "followers": _read_old_followers(), "status": "init"}

    try:
        from instagrapi import Client
    except ImportError:
        print("❌ instagrapi non installé (pip install instagrapi)")
        data["status"] = "failed_no_instagrapi"
        _save(data)
        return data

    cl = Client()
    cl.delay_range = [1, 3]  # petite temporisation anti-détection

    # Réutilise une session mise en cache si disponible
    if os.path.exists(SETTINGS_FILE):
        try:
            cl.load_settings(SETTINGS_FILE)
            print("♻️  Session chargée depuis le cache")
        except Exception as exc:
            print(f"⚠️  Cache de session illisible, on repart proprement : {exc}")

    # Authentification
    try:
        if SESSION_ID:
            print("🔐 Connexion via INSTA_SESSION_ID…")
            cl.login_by_sessionid(SESSION_ID)
        elif USERNAME and PASSWORD:
            print(f"🔐 Connexion via identifiants (@{USERNAME})…")
            cl.login(USERNAME, PASSWORD)
        else:
            raise ValueError("Aucune méthode d'auth : définir INSTA_SESSION_ID (ou INSTA_USERNAME + INSTA_PASSWORD)")
    except Exception as exc:
        print(f"❌ Échec de connexion : {exc}")
        data["status"] = f"failed_login: {type(exc).__name__}"
        _save(data)
        return data

    # Sauvegarde la session pour la prochaine exécution
    try:
        cl.dump_settings(SETTINGS_FILE)
    except Exception:
        pass

    # Récupération du nombre d'abonnés
    try:
        target = USERNAME or cl.account_info().username
        user_id = cl.user_id_from_username(target)
        info = cl.user_info(user_id)
        followers = int(info.follower_count)

        data["followers"] = followers
        data["timestamp"] = int(time.time())
        data["status"] = "success"
        print(f"✅ @{target} : {followers} abonnés")
    except Exception as exc:
        print(f"❌ Échec récupération abonnés : {exc}")
        data["status"] = f"failed_fetch: {type(exc).__name__}"

    _save(data)
    return data


if __name__ == "__main__":
    print("=" * 60)
    print("RÉCUPÉRATION DES ABONNÉS INSTAGRAM (instagrapi)")
    print("=" * 60)
    result = fetch_followers()
    print("=" * 60)
    # Sortie non bloquante : on ne casse pas le workflow si Instagram râle,
    # l'ancienne valeur est conservée.
