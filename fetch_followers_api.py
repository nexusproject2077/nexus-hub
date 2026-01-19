"""
Version utilisant directement l'API GraphQL d'Instagram
BEAUCOUP plus fiable que le scraping HTML
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
    """Récupère le nombre d'abonnés via l'API GraphQL Instagram"""

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

        # Headers pour l'API GraphQL Instagram
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'X-IG-App-ID': '936619743392459',  # App ID Instagram Web
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': f'https://www.instagram.com/{USERNAME}/',
            'X-ASBD-ID': '129477',
            'X-IG-WWW-Claim': '0',
        }

        cookies = {
            'sessionid': SESSION_ID,
            'ds_user_id': '',  # Optionnel
            'csrftoken': 'missing',  # Peut être requis
        }

        # Méthode 1: API web_profile_info (la plus directe)
        print("\n📡 Méthode 1: API web_profile_info...")
        url = f'https://i.instagram.com/api/v1/users/web_profile_info/?username={USERNAME}'

        response = requests.get(
            url,
            headers=headers,
            cookies=cookies,
            timeout=15
        )

        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            try:
                json_data = response.json()
                print(f"   ✅ Réponse JSON reçue")

                # Extraire les données utilisateur
                if 'data' in json_data and 'user' in json_data['data']:
                    user = json_data['data']['user']

                    # Chercher le nombre d'abonnés
                    followers = None
                    if 'edge_followed_by' in user:
                        followers = user['edge_followed_by'].get('count', 0)
                    elif 'follower_count' in user:
                        followers = user['follower_count']

                    if followers is not None:
                        print(f"   ✅ SUCCÈS! Abonnés: {followers}")
                        data['followers'] = followers
                        data['status'] = 'success'
                        return data

            except json.JSONDecodeError as e:
                print(f"   ❌ Erreur JSON: {e}")
                print(f"   Réponse brute: {response.text[:200]}")

        # Méthode 2: GraphQL Query directe
        print("\n📡 Méthode 2: GraphQL Query...")

        graphql_url = 'https://www.instagram.com/graphql/query/'

        # Query hash pour récupérer les infos utilisateur
        # Ce hash peut changer, mais c'est un hash connu pour user info
        query_hash = '58b6785bea111c67129decbe6a448951'

        params = {
            'query_hash': query_hash,
            'variables': json.dumps({
                'username': USERNAME,
                'include_reel': False
            })
        }

        response = requests.get(
            graphql_url,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=15
        )

        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            try:
                json_data = response.json()

                # Chercher dans la structure GraphQL
                if 'data' in json_data and 'user' in json_data['data']:
                    user = json_data['data']['user']
                    if 'edge_followed_by' in user:
                        followers = user['edge_followed_by']['count']
                        print(f"   ✅ SUCCÈS! Abonnés: {followers}")
                        data['followers'] = followers
                        data['status'] = 'success_graphql'
                        return data

            except:
                pass

        # Méthode 3: Fallback - rechercher l'ID utilisateur puis les stats
        print("\n📡 Méthode 3: Recherche par ID utilisateur...")

        search_url = f'https://www.instagram.com/web/search/topsearch/?query={USERNAME}'

        response = requests.get(
            search_url,
            headers=headers,
            cookies=cookies,
            timeout=15
        )

        if response.status_code == 200:
            try:
                search_data = response.json()

                # Trouver l'utilisateur dans les résultats
                for user_result in search_data.get('users', []):
                    user = user_result.get('user', {})
                    if user.get('username', '').lower() == USERNAME.lower():
                        # Essayer d'extraire le nombre d'abonnés
                        followers = user.get('follower_count', 0)
                        if followers > 0:
                            print(f"   ✅ SUCCÈS! Abonnés: {followers}")
                            data['followers'] = followers
                            data['status'] = 'success_search'
                            return data

            except:
                pass

        # Si toutes les méthodes échouent
        print("\n❌ Toutes les méthodes API ont échoué")

        # Garder les anciennes données si disponibles
        try:
            with open(OUTPUT_FILE, 'r') as f:
                old_data = json.load(f)
                data['followers'] = old_data.get('followers', 0)
                data['status'] = 'failed_api_retaining_old_data'
                print(f"   📦 Conservation des anciennes données: {data['followers']} abonnés")
        except:
            data['status'] = 'failed_all_api_methods'

    except requests.exceptions.Timeout:
        print("❌ Timeout - Instagram ne répond pas")
        data['status'] = 'failed_timeout'

    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur réseau: {e}")
        data['status'] = f'failed_network: {type(e).__name__}'

    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
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
    print("RÉCUPÉRATION DES ABONNÉS INSTAGRAM VIA API")
    print("=" * 60)

    result = fetch_followers()

    print("\n" + "=" * 60)
    if 'success' in result['status']:
        print(f"✅ SUCCÈS! {result['followers']} abonnés")
    else:
        print(f"❌ ÉCHEC: {result['status']}")
    print("=" * 60)
