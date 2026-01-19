import instaloader
import os
import json
import time

# --- Configuration et Récupération des secrets d'environnement ---
L_USERNAME = os.environ.get('INSTA_USERNAME')
L_SESSION_ID = os.environ.get('INSTA_SESSION_ID')

TARGET_PROFILE = L_USERNAME 
# CORRECTION du chemin : Le script est exécuté depuis la racine, le chemin doit être relatif au dossier du dépôt.
# Si vous exécutez dans 'fils/', l'OUTPUT_FILE devrait être 'followers_data.json'.
# Si vous exécutez à la racine (comme dans le workflow), il doit pointer vers le dossier 'fils/'.
OUTPUT_FILE = 'fils/followers_data.json' 

# --- Initialisation Instaloader ---
L = instaloader.Instaloader()

def fetch_followers():
    # Par défaut en cas d'échec
    data = {
        "timestamp": int(time.time()),
        "followers": 0,
        "status": "initial_failure"
    }

    try:
        if not L_USERNAME or not L_SESSION_ID:
            raise EnvironmentError("Erreur: Les secrets INSTA_USERNAME ou INSTA_SESSION_ID n'ont pas été chargés.")
        
        print(f"Tentative de connexion avec Session ID pour l'utilisateur: {L_USERNAME}")
        print(f"Session ID présent: {'Oui' if L_SESSION_ID else 'Non'}")
        print(f"Longueur du Session ID: {len(L_SESSION_ID) if L_SESSION_ID else 0} caractères")

        # CORRECTION: Injection multiple du cookie pour maximiser les chances de succès
        # Instaloader utilise requests en interne, on injecte le cookie dans toutes les variantes de domaine
        L.context._session.cookies.set('sessionid', L_SESSION_ID, domain='.instagram.com')
        L.context._session.cookies.set('sessionid', L_SESSION_ID, domain='instagram.com')
        L.context._session.cookies.set('sessionid', L_SESSION_ID, domain='www.instagram.com')

        # Ajouter d'autres cookies essentiels pour une session valide
        L.context._session.cookies.set('csrftoken', 'missing', domain='.instagram.com')

        print("Cookies injectés, tentative de chargement du profil...")

        # Charger le profil cible sans test_login() qui peut échouer
        profile = instaloader.Profile.from_username(L.context, TARGET_PROFILE)
        
        # Récupérer le nombre d'abonnés
        follower_count = profile.followers
        
        # --- Sauvegarde des données (Succès) ---
        data["followers"] = follower_count
        data["status"] = "success"

    except Exception as e:
        print(f"Échec critique de la récupération Instaloader : {e}")
        print(f"Type d'erreur: {e.__class__.__name__}")
        print(f"Message d'erreur complet: {str(e)}")

        # Gestion spécifique selon le type d'erreur
        error_type = e.__class__.__name__

        if "ProfileNotExistsException" in error_type:
            print("DIAGNOSTIC: Le profil Instagram n'a pas été trouvé")
            print("Causes possibles:")
            print("  1. Le Session ID est expiré ou invalide")
            print("  2. Le nom d'utilisateur est incorrect")
            print("  3. Instagram a détecté une activité suspecte")
        elif "LoginRequiredException" in error_type:
            print("DIAGNOSTIC: Instagram exige une authentification complète")
            print("  -> Le Session ID est probablement expiré")
        elif "ConnectionException" in error_type:
            print("DIAGNOSTIC: Problème de connexion réseau")

        # Tenter de charger les données précédentes en cas d'échec pour ne pas réinitialiser à 0
        try:
            with open(OUTPUT_FILE, 'r') as f:
                old_data = json.load(f)
                data["followers"] = old_data.get("followers", 0)
                data["status"] = f"failed_retaining_old_data: {e.__class__.__name__}"
        except FileNotFoundError:
             data["status"] = f"failed_no_old_data: {e.__class__.__name__}"
        except Exception:
             data["status"] = f"failed_read_error: {e.__class__.__name__}"

    finally:
        # --- Écriture du fichier JSON (CORRECTION DU CHEMIN IMPLICITE) ---
        try:
            # Assurez-vous que le répertoire 'fils' existe avant d'écrire
            os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
            with open(OUTPUT_FILE, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Données écrites dans {OUTPUT_FILE} avec statut: {data['status']}")
        except Exception as write_error:
            print(f"Erreur fatale lors de l'écriture du fichier JSON: {write_error}")


if __name__ == "__main__":
    fetch_followers()
