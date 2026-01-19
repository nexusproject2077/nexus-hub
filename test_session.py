"""
Script de test pour vérifier si le Session ID Instagram fonctionne
"""
import requests
import os
import json

SESSION_ID = os.environ.get('INSTA_SESSION_ID', '')
USERNAME = os.environ.get('INSTA_USERNAME', 'merickkn')

def test_session_id():
    """Teste si le Session ID permet d'accéder à Instagram"""

    if not SESSION_ID:
        print("❌ ERREUR: INSTA_SESSION_ID n'est pas configuré")
        return False

    print(f"✅ Session ID présent: {len(SESSION_ID)} caractères")
    print(f"✅ Username: {USERNAME}")

    # Test 1: Vérifier avec l'API Web Instagram
    print("\n🔍 Test 1: API Web Instagram...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
    }

    cookies = {
        'sessionid': SESSION_ID
    }

    try:
        # Essayer de récupérer les infos du profil via l'API web
        url = f'https://www.instagram.com/api/v1/users/web_profile_info/?username={USERNAME}'
        response = requests.get(url, headers=headers, cookies=cookies, timeout=10)

        print(f"Status code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'user' in data['data']:
                user = data['data']['user']
                followers = user.get('edge_followed_by', {}).get('count', 0)
                print(f"\n✅ SUCCÈS! Abonnés récupérés: {followers}")
                return True, followers
            else:
                print("❌ Réponse invalide")
                print(json.dumps(data, indent=2)[:500])
        elif response.status_code == 401:
            print("❌ Session ID invalide ou expiré (401 Unauthorized)")
        elif response.status_code == 404:
            print("❌ Profil non trouvé (404)")
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(response.text[:200])

    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")

    # Test 2: Méthode alternative - scraping simple
    print("\n🔍 Test 2: Scraping page publique...")
    try:
        url = f'https://www.instagram.com/{USERNAME}/'
        response = requests.get(url, headers=headers, cookies=cookies, timeout=10)

        if response.status_code == 200:
            # Chercher le nombre d'abonnés dans le HTML
            import re
            match = re.search(r'"edge_followed_by":\{"count":(\d+)\}', response.text)
            if match:
                followers = int(match.group(1))
                print(f"✅ SUCCÈS! Abonnés trouvés: {followers}")
                return True, followers
            else:
                print("⚠️ Impossible de trouver le nombre d'abonnés dans le HTML")
        else:
            print(f"❌ Erreur: {response.status_code}")

    except Exception as e:
        print(f"❌ Erreur: {e}")

    return False, 0

if __name__ == "__main__":
    print("=" * 60)
    print("TEST DU SESSION ID INSTAGRAM")
    print("=" * 60)

    success, followers = test_session_id()

    print("\n" + "=" * 60)
    if success:
        print(f"✅ LE SESSION ID FONCTIONNE!")
        print(f"📊 Nombre d'abonnés: {followers}")
        print("\nVous pouvez utiliser ce Session ID dans GitHub Actions")
    else:
        print("❌ LE SESSION ID NE FONCTIONNE PAS")
        print("\nActions à faire:")
        print("1. Récupérez un nouveau Session ID (navigation privée)")
        print("2. Assurez-vous de copier la valeur COMPLÈTE")
        print("3. Vérifiez qu'il n'y a pas d'espaces avant/après")
    print("=" * 60)
