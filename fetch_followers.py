"""
Version améliorée qui parse le HTML Instagram avec plusieurs patterns
"""
import requests
import os
import json
import time
import re

# Configuration
USERNAME = os.environ.get('INSTA_USERNAME', 'merickkn')
SESSION_ID = os.environ.get('INSTA_SESSION_ID', '')
OUTPUT_FILE = 'fils/followers_data.json'

def extract_followers_from_html(html_content):
    """Essaie plusieurs patterns pour extraire le nombre d'abonnés"""

    patterns = [
        # Pattern 1: Format JSON classique
        r'"edge_followed_by":\{"count":(\d+)\}',

        # Pattern 2: Format alternatif
        r'"follower_count":(\d+)',

        # Pattern 3: Dans les métadonnées
        r'"followed_by":\{"count":(\d+)\}',

        # Pattern 4: Format récent Instagram
        r'content="(\d+)\s+Followers"',

        # Pattern 5: Meta tag
        r'<meta\s+property="og:description"\s+content="[^"]*?(\d+)\s+Followers',

        # Pattern 6: SharedData
        r'"userInteractionCount":"(\d+)"',

        # Pattern 7: Script JSON (données embarquées)
        r'"follower_count":(\d+)',

        # Pattern 8: Meta description avec format différent
        r'(\d+)\s+Followers,',

        # Pattern 9: JSON dans script tag
        r'window\._sharedData\s*=\s*({.+?});',

        # Pattern 10: Nouveau format Instagram 2024/2025
        r'"edge_follow":\{"count":(\d+)\}',

        # Pattern 11: Dans les props
        r'"props":\{[^}]*"follower_count":(\d+)',
    ]

    # Essayer les patterns simples d'abord
    for i, pattern in enumerate(patterns[:8], 1):
        match = re.search(pattern, html_content, re.IGNORECASE)
        if match:
            followers = int(match.group(1))
            print(f"   ✅ Pattern {i} a trouvé: {followers} abonnés")
            return followers

    # Pattern 9: SharedData (extraction JSON complète)
    match = re.search(patterns[8], html_content)
    if match:
        try:
            import json as json_lib
            shared_data = json_lib.loads(match.group(1))
            # Chercher dans le JSON
            if 'entry_data' in shared_data:
                for page_type, pages in shared_data['entry_data'].items():
                    for page in pages:
                        if 'graphql' in page and 'user' in page['graphql']:
                            user = page['graphql']['user']
                            if 'edge_followed_by' in user:
                                followers = user['edge_followed_by']['count']
                                print(f"   ✅ Pattern 9 (SharedData JSON) a trouvé: {followers} abonnés")
                                return followers
        except:
            pass

    # Patterns 10-11
    for i, pattern in enumerate(patterns[9:], 10):
        match = re.search(pattern, html_content, re.IGNORECASE)
        if match:
            followers = int(match.group(1))
            print(f"   ✅ Pattern {i} a trouvé: {followers} abonnés")
            return followers

    return None

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

        # Headers pour simuler un navigateur (SANS Accept-Encoding pour éviter compression)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        cookies = {
            'sessionid': SESSION_ID
        }

        # Méthode 1: Scraping de la page publique
        print("\n📡 Récupération de la page Instagram...")
        url = f'https://www.instagram.com/{USERNAME}/'

        response = requests.get(
            url,
            headers=headers,
            cookies=cookies,
            timeout=15,
            allow_redirects=True
        )

        print(f"   Status: {response.status_code}")
        print(f"   Encoding détecté: {response.encoding}")

        if response.status_code == 200:
            # S'assurer que le contenu est bien décodé en UTF-8
            response.encoding = response.apparent_encoding or 'utf-8'
            html_text = response.text

            print(f"   Taille HTML: {len(html_text)} caractères")
            print(f"   Échantillon (premiers 200 caractères): {html_text[:200]}")

            # Essayer d'extraire avec plusieurs patterns
            followers = extract_followers_from_html(html_text)

            if followers is not None:
                print(f"   ✅ SUCCÈS! Abonnés: {followers}")
                data['followers'] = followers
                data['status'] = 'success'
                return data
            else:
                print("   ⚠️ Aucun pattern n'a trouvé le nombre d'abonnés")

                # Sauvegarder le HTML complet pour analyse (mode debug)
                debug_file = 'debug_instagram.html'
                try:
                    with open(debug_file, 'w', encoding='utf-8') as f:
                        f.write(html_text)
                    print(f"   💾 HTML complet sauvegardé dans {debug_file} pour analyse")
                except:
                    pass

                # Afficher un échantillon du HTML
                print(f"   📄 Échantillon HTML (500 premiers caractères):")
                print(html_text[:500])

                # Chercher tous les nombres qui pourraient être des abonnés
                print("\n   🔍 Recherche de nombres suspects dans le HTML...")
                number_matches = re.findall(r'(\d{2,8})\s*[Ff]ollowers?', html_text)
                if number_matches:
                    print(f"   Nombres trouvés près de 'Followers': {number_matches[:5]}")
                    # Essayer le premier nombre trouvé
                    try:
                        followers = int(number_matches[0])
                        print(f"   ⚠️ Utilisation du premier nombre trouvé: {followers}")
                        data['followers'] = followers
                        data['status'] = 'success_fuzzy_match'
                        return data
                    except:
                        pass

        # Si échec
        print("\n❌ Impossible d'extraire le nombre d'abonnés")

        # Garder les anciennes données si disponibles
        try:
            with open(OUTPUT_FILE, 'r') as f:
                old_data = json.load(f)
                data['followers'] = old_data.get('followers', 0)
                data['status'] = f'failed_retaining_old_data (HTTP {response.status_code})'
                print(f"   📦 Conservation des anciennes données: {data['followers']} abonnés")
        except:
            data['status'] = f'failed_extraction (HTTP {response.status_code})'

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
    if result['status'] == 'success':
        print(f"✅ SUCCÈS! {result['followers']} abonnés")
    else:
        print(f"❌ ÉCHEC: {result['status']}")
    print("=" * 60)
