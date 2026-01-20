"""
SOLUTION FINALE: Utilise instagrapi au lieu de requêtes HTTP brutes
instagrapi est une bibliothèque maintenue qui gère mieux l'authentification
"""
try:
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, UserNotFound
    INSTAGRAPI_AVAILABLE = True
except ImportError:
    INSTAGRAPI_AVAILABLE = False
    print("⚠️ instagrapi pas installé, utilisation méthode de fallback")

import os
import json
import time

# Configuration
USERNAME = os.environ.get('INSTA_USERNAME', 'merickkn')
SESSION_ID = os.environ.get('INSTA_SESSION_ID', '')
OUTPUT_FILE = 'fils/followers_data.json'

def fetch_with_instagrapi():
    """Méthode avec instagrapi (recommandé)"""
    if not INSTAGRAPI_AVAILABLE:
        return None

    try:
        print("📡 Utilisation d'instagrapi...")

        cl = Client()

        # Créer une session à partir du sessionid
        cl.set_cookie_file = None
        cl.set_session({
            'sessionid': SESSION_ID
        })

        # Tester la connexion
        try:
            cl.get_timeline_feed()
            print("   ✅ Session valide!")
        except LoginRequired:
            print("   ❌ Session invalide - réauthentification nécessaire")
            return None

        # Récupérer les infos utilisateur
        user_info = cl.user_info_by_username(USERNAME)
        followers = user_info.follower_count

        print(f"   ✅ SUCCÈS avec instagrapi! Abonnés: {followers}")
        return followers, 'success_instagrapi'

    except UserNotFound:
        print(f"   ❌ Utilisateur {USERNAME} non trouvé")
        return None
    except Exception as e:
        print(f"   ❌ Erreur instagrapi: {e}")
        return None

def fetch_with_simple_request():
    """Fallback: tentative simple sans authentification"""
    import requests

    print("📡 Tentative sans authentification (profil public)...")

    try:
        # Certains comptes publics exposent leurs stats sans auth
        url = f'https://www.instagram.com/{USERNAME}/?__a=1&__d=dis'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            try:
                data = response.json()
                # Chercher dans plusieurs endroits possibles
                if 'graphql' in data and 'user' in data['graphql']:
                    user = data['graphql']['user']
                    if 'edge_followed_by' in user:
                        followers = user['edge_followed_by']['count']
                        print(f"   ✅ SUCCÈS! Abonnés: {followers}")
                        return followers, 'success_public'
            except:
                pass

        print(f"   ❌ Impossible de récupérer (compte privé ou protégé)")
        return None

    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return None

def fetch_followers():
    """Récupère le nombre d'abonnés Instagram"""

    data = {
        "timestamp": int(time.time()),
        "followers": 0,
        "status": "initial_failure"
    }

    try:
        if not SESSION_ID:
            print("⚠️ SESSION_ID manquant, tentative en mode public...")
            result = fetch_with_simple_request()
            if result:
                data['followers'], data['status'] = result
                return data
        else:
            print(f"🔍 Récupération des abonnés pour @{USERNAME}")
            print(f"📝 Session ID: {len(SESSION_ID)} caractères")

            # Méthode 1: instagrapi (recommandé)
            result = fetch_with_instagrapi()
            if result:
                data['followers'], data['status'] = result
                return data

            # Méthode 2: Fallback public
            print("\n⚠️ instagrapi a échoué, tentative en mode public...")
            result = fetch_with_simple_request()
            if result:
                data['followers'], data['status'] = result
                return data

        # Si toutes les méthodes échouent
        print("\n❌ Toutes les méthodes ont échoué")

        # Conserver les anciennes données
        try:
            with open(OUTPUT_FILE, 'r') as f:
                old_data = json.load(f)
                data['followers'] = old_data.get('followers', 0)
                data['status'] = 'failed_retaining_old_data'
                print(f"   📦 Conservation: {data['followers']} abonnés")
        except:
            data['status'] = 'failed_all_methods'

    except Exception as e:
        print(f"❌ Erreur critique: {e}")
        import traceback
        traceback.print_exc()
        data['status'] = f'failed: {type(e).__name__}'

    finally:
        # Sauvegarder
        try:
            os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
            with open(OUTPUT_FILE, 'w') as f:
                json.dump(data, f, indent=4)

            print(f"\n💾 Données sauvegardées: {OUTPUT_FILE}")
            print(f"   Status: {data['status']}")
            print(f"   Abonnés: {data['followers']}")
        except Exception as e:
            print(f"❌ Erreur d'écriture: {e}")

    return data

if __name__ == "__main__":
    print("=" * 60)
    print("RÉCUPÉRATION DES ABONNÉS INSTAGRAM")
    print("=" * 60)

    result = fetch_followers()

    print("\n" + "=" * 60)
    if 'success' in result['status']:
        print(f"✅ SUCCÈS! {result['followers']} abonnés")
    else:
        print(f"❌ ÉCHEC: {result['status']}")
        print("\nRECOMMANDATIONS:")
        print("1. Vérifiez que le Session ID est récent (< 24h)")
        print("2. Assurez-vous que le compte Instagram n'est pas privé")
        print("3. Essayez de récupérer un nouveau Session ID")
        print("4. Si le problème persiste, Instagram bloque peut-être le scraping")
    print("=" * 60)
