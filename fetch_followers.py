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

        # CORRECTION DE LA MÉTHODE INSTALOADER : Utiliser l'injection directe de cookie via requests
        # Instaloader utilise requests en interne, on injecte le cookie directement
        L.context._session.cookies.set('sessionid', L_SESSION_ID, domain='.instagram.com')

        # Optionnel mais recommandé : charger le profil de l'utilisateur connecté pour valider la session
        L.test_login()

        # Charger le profil cible
        profile = instaloader.Profile.from_username(L.context, TARGET_PROFILE)
        
        # Récupérer le nombre d'abonnés
        follower_count = profile.followers
        
        # --- Sauvegarde des données (Succès) ---
        data["followers"] = follower_count
        data["status"] = "success"

    except Exception as e:
        print(f"Échec critique de la récupération Instaloader : {e}")
        # Tenter de charger les données précédentes en cas d'échec pour ne pas réinitialiser à 0
        try:
            with open(OUTPUT_FILE, 'r') as f:
                old_data = json.load(f)
                data["followers"] = old_data.get("followers", 0)
                data["status"] = f"failed_auth_retaining_old_data: {e.__class__.__name__}"
        except FileNotFoundError:
             data["status"] = f"failed_auth_no_old_data: {e.__class__.__name__}"
        except Exception:
             data["status"] = f"failed_auth_read_error: {e.__class__.__name__}"

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
