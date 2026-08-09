# Déploiement Nexus-Hub — Firebase Hosting + Cloud Run

Ce guide déploie le site en deux morceaux :

- **Frontend** (HTML / CSS / JS statiques) → **Firebase Hosting**
  → URL publique du type `https://nexus-hubs.web.app/`
- **Backend** (API Flask) → **Google Cloud Run**
  → appelé depuis le frontend via les chemins `/api/**`

Firebase Hosting réécrit toute requête `/api/**` vers le service Cloud Run
(`firebase.json` → `hosting.rewrites`), donc **le frontend et le backend
partagent le même domaine** : pas de problème de CORS en production.

```
Navigateur ──► https://nexus-hubs.web.app/            (Firebase Hosting, statique)
           └─► https://nexus-hubs.web.app/api/followers ──► Cloud Run (Flask)
```

---

## 0. Prérequis (une seule fois)

```bash
# Outils
npm install -g firebase-tools          # CLI Firebase
# gcloud : https://cloud.google.com/sdk/docs/install

# Connexions
firebase login
gcloud auth login
```

Le projet Firebase et le projet Google Cloud doivent être **le même projet GCP**.
L'identifiant utilisé partout ici est `nexus-hubs` (→ `nexus-hubs.web.app`).
Adaptez-le si votre identifiant de projet diffère (voir `.firebaserc`).

Créez le projet s'il n'existe pas encore :

```bash
firebase projects:create nexus-hubs        # ou via la console Firebase
gcloud config set project nexus-hubs
```

Activez les API nécessaires :

```bash
gcloud services enable run.googleapis.com \
                       cloudbuild.googleapis.com \
                       artifactregistry.googleapis.com
```

---

## 1. Déployer le backend sur Cloud Run

Depuis le dossier `backend/` :

```bash
cd backend

gcloud run deploy nexus-hub-api \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars INSTA_USERNAME=merickkn,FOLLOWERS_TTL=1800
```

> ⚠️ Le nom du service (`nexus-hub-api`) et la région (`europe-west1`)
> doivent correspondre au bloc `rewrites` de `firebase.json`.

### Session Instagram (optionnel, pour des abonnés en temps réel)

Sans `INSTA_SESSION_ID`, l'API renvoie la dernière valeur connue
(`backend/followers_data.json`). Pour activer la récupération live, stockez
le cookie de session comme **secret** plutôt qu'en clair :

```bash
echo -n "VOTRE_SESSION_ID" | gcloud secrets create insta-session --data-file=-

gcloud run services update nexus-hub-api \
  --region europe-west1 \
  --set-secrets INSTA_SESSION_ID=insta-session:latest
```

### Vérifier

```bash
curl https://nexus-hub-api-XXXX-ew.a.run.app/api/health
# {"service":"nexus-hub-api","status":"ok","time":...}
```

---

## 2. Déployer le frontend sur Firebase Hosting

Depuis la **racine du dépôt** :

```bash
firebase deploy --only hosting
```

Firebase publie le contenu statique (voir `firebase.json` → `hosting.public: "."`
et la liste `ignore` qui exclut le backend, les scripts Python, etc.) puis
câble les réécritures `/api/**` vers Cloud Run.

Résultat :

```
Hosting URL: https://nexus-hubs.web.app
```

---

## 3. Test de bout en bout

```bash
# Frontend
curl -I https://nexus-hubs.web.app/

# Backend via le domaine du frontend (réécriture)
curl https://nexus-hubs.web.app/api/followers
curl https://nexus-hubs.web.app/api/status
```

Le widget d'abonnés (`app.js`) appelle d'abord `/api/followers` et retombe
automatiquement sur `./followers_data.json` si le backend est indisponible.

---

## 4. Développement local

```bash
# Backend
cd backend
pip install -r requirements.txt
python main.py                 # http://localhost:8080/api/health

# Frontend (dans un autre terminal, à la racine)
python -m http.server 5000     # http://localhost:5000
```

En local, `app.js` tente `/api/followers` (404 sur le serveur statique) puis
utilise le JSON statique — le site reste fonctionnel.

---

## Récapitulatif des fichiers

| Fichier                        | Rôle                                                      |
| ------------------------------ | --------------------------------------------------------- |
| `firebase.json`                | Config Hosting + réécriture `/api/**` → Cloud Run         |
| `.firebaserc`                  | Projet Firebase par défaut (`nexus-hubs`)                 |
| `backend/main.py`              | API Flask (`/api/health`, `/api/status`, `/api/followers`)|
| `backend/Dockerfile`           | Image de conteneur Cloud Run                              |
| `backend/requirements.txt`     | Dépendances Python du backend                            |
| `backend/followers_data.json`  | Dernière valeur d'abonnés connue (fallback)              |
