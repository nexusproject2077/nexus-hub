"""
Version simplifiée qui utilise l'API Web Instagram directement
Au lieu d'Instaloader qui est problématique
"""
import requests
import os
import json
import time

# Configuration
USERNAME = os.environ.get('INSTA_USERNAME', 'merickkn')
SESSION_ID = os.environ.get('INSTA_SESSION_ID', '')
OUTPUT_FILE = 'fils/followers_data.json'

def fetch_followers():
    """Récupère le nombre d'abonnés Instagram"""

    # Données par défaut
    data = {
        "timestamp": int(time.time()),
        "followers": 0,
        "status": "initial_failure"
    }

    try:
        if not SESSION_ID:
            raise ValueError("INSTA_SESSION_ID n'est pas configuré")

        print(f"🔍 Récupération des abonnés pour @{USERNAME}")
        print(f"📝 Session ID: {len(SESSION_ID)} caractères")

        # Headers pour simuler un navigateur
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'X-IG-App-ID': '936619743392459',
            'X-Requested-With': 'XMLHttpRequest',
        }

        cookies = {
            'sessionid': SESSION_ID
        }

        # Méthode 1: API Web Instagram (la plus fiable)
        print("\n📡 Méthode 1: API Web Instagram...")
        url = f'https://www.instagram.com/api/v1/users/web_profile_info/?username={USERNAME}'

        response = requests.get(
            url,
            headers=headers,
            cookies=cookies,
            timeout=15
        )

        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            json_data = response.json()

            if 'data' in json_data and 'user' in json_data['data']:
                user = json_data['data']['user']
                followers = user.get('edge_followed_by', {}).get('count', 0)

                print(f"   ✅ Succès! Abonnés: {followers}")

                data['followers'] = followers
                data['status'] = 'success'
                return data

        # Méthode 2: Scraping de la page publique (fallback)
        print("\n📡 Méthode 2: Scraping page publique...")
        url = f'https://www.instagram.com/{USERNAME}/'

        response = requests.get(
            url,
            headers=headers,
            cookies=cookies,
            timeout=15
        )

        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            import re

            # Chercher le JSON embarqué dans le HTML
            match = re.search(r'"edge_followed_by":\{"count":(\d+)\}', response.text)

            if match:
                followers = int(match.group(1))
                print(f"   ✅ Succès! Abonnés: {followers}")

                data['followers'] = followers
                data['status'] = 'success_scraping'
                return data

        # Si toutes les méthodes échouent
        print("\n❌ Toutes les méthodes ont échoué")

        # Garder les anciennes données si disponibles
        try:
            with open(OUTPUT_FILE, 'r') as f:
                old_data = json.load(f)
                data['followers'] = old_data.get('followers', 0)
                data['status'] = f'failed_retaining_old_data (HTTP {response.status_code})'
                print(f"   📦 Conservation des anciennes données: {data['followers']} abonnés")
        except:
            data['status'] = f'failed_all_methods (HTTP {response.status_code})'

    except requests.exceptions.Timeout:
        print("❌ Timeout - Instagram ne répond pas")
        data['status'] = 'failed_timeout'

    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur réseau: {e}")
        data['status'] = f'failed_network: {type(e).__name__}'

    except Exception as e:
        print(f"❌ Erreur: {e}")
        data['status'] = f'failed: {type(e).__name__}'

    finally:
        # Sauvegarder les données
        try:
            os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

            with open(OUTPUT_FILE, 'w') as f:
                json.dump(data, f, indent=4)

            print(f"\n💾 Données sauvegardées: {OUTPUT_FILE}")
            print(f"   Status: {data['status']}")
            print(f"   Abonnés: {data['followers']}")

        except Exception as write_error:
            print(f"❌ Erreur d'écriture: {write_error}")

    return data

if __name__ == "__main__":
    print("=" * 60)
    print("RÉCUPÉRATION DES ABONNÉS INSTAGRAM")
    print("=" * 60)

    result = fetch_followers()

    print("\n" + "=" * 60)
    if result['status'] == 'success' or result['status'] == 'success_scraping':
        print(f"✅ SUCCÈS! {result['followers']} abonnés")
    else:
        print(f"❌ ÉCHEC: {result['status']}")
    print("=" * 60)
