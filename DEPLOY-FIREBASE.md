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

## 🚀 Déploiement SANS terminal (Cloud Shell désactivé)

Si le terminal / Cloud Shell est désactivé, tout se fait depuis l'interface.

### A. Backend → Cloud Run (console Google Cloud)

1. Console Cloud Run → **« Connecter un dépôt »** (ou **Déployer le conteneur → Déployer en continu depuis un dépôt**).
2. **Configurer avec Cloud Build** → fournisseur **GitHub** → autoriser puis choisir le dépôt `nexusproject2077/nexus-hub`.
3. **Branche** : `^main$` (déploiement continu à chaque push sur `main`).
4. **Type de build** : `Dockerfile`.
   - **Emplacement du Dockerfile** : `backend/Dockerfile`
     ⚠️ bien indiquer le **fichier** `backend/Dockerfile`, **pas** le dossier `/backend`
     (sinon : *« read .../backend: is a directory »*).
   - Le contexte de build est la **racine du dépôt** ; le `Dockerfile` en tient
     compte (il fait `COPY backend/...`), aucune autre configuration n'est requise.
5. **Nom du service** : `nexus-hub-api` — **Région** : `europe-west1`
   (⚠️ doivent correspondre au bloc `rewrites` de `firebase.json`).
6. **Authentification** : *Autoriser les appels non authentifiés*.
7. (Optionnel) **Variables et secrets** :
   - `INSTA_USERNAME = merickn`, `FOLLOWERS_TTL = 1800`
   - Pour les abonnés en temps réel : créer un secret `insta-session` (valeur = cookie
     `sessionid` Instagram) puis le référencer sur `INSTA_SESSION_ID`.
8. **Créer / Déployer**. Cloud Build construit l'image et met le service en ligne
   (redéploiement automatique à chaque push ensuite).

### B. Frontend → Firebase Hosting (via GitHub Actions)

Le workflow `.github/workflows/deploy-firebase-hosting.yml` déploie automatiquement
à chaque push sur `main`. Il faut lui donner **un secret** (une seule fois) :

1. **Console Firebase** → ⚙️ *Paramètres du projet* → onglet **Comptes de service**
   → bouton **Générer une nouvelle clé privée** → un **fichier JSON** est téléchargé.
   ⚠️ Il faut bien **ce fichier JSON téléchargé**, PAS l'extrait de code affiché
   sur la page (celui qui commence par `var admin = require("firebase-admin")`).
   Le bon contenu commence par `{ "type": "service_account", "project_id": ... }`.
2. **GitHub** → dépôt `nexus-hub` → **Settings → Secrets and variables → Actions**
   → **New repository secret** :
   - **Name** : `FIREBASE_SERVICE_ACCOUNT`
   - **Secret** : coller **tout le contenu du fichier JSON** (les accolades incluses).
3. Le déploiement se lance au prochain push sur `main`, ou manuellement via
   l'onglet **Actions → Deploy Frontend to Firebase Hosting → Run workflow**.

> Le projet Firebase doit avoir l'ID `nexus-hubs` (→ `nexus-hubs.web.app`).
> Sinon, ajustez `projectId` dans le workflow, ainsi que `.firebaserc`.

Les sections ci-dessous décrivent l'équivalent **en ligne de commande** (si un jour
vous avez accès à un terminal).

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

Le `Dockerfile` attend le **contexte racine du dépôt**, donc on lance la
commande **depuis la racine** en pointant explicitement le Dockerfile :

```bash
# À la racine du dépôt (pas dans backend/)
gcloud run deploy nexus-hub-api \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars INSTA_USERNAME=merickn,FOLLOWERS_TTL=1800 \
  --set-build-env-vars GOOGLE_DOCKERFILE=backend/Dockerfile
```

> Si votre version de `gcloud` ne connaît pas `--set-build-env-vars`, utilisez
> plutôt la console (section « Déploiement sans terminal ») ou un build
> explicite : `gcloud builds submit --tag REGION-docker.pkg.dev/PROJET/REPO/nexus-hub-api -f backend/Dockerfile .`

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

## 🛠️ Dépannage

### `Failed to authenticate, have you run firebase login?` + `... is not valid JSON`
Le secret `FIREBASE_SERVICE_ACCOUNT` ne contient pas la clé JSON mais l'extrait
de code de la page « Comptes de service ». Recollez le **fichier JSON**
téléchargé (commence par `{ "type": "service_account", ... }`).

### `Failed to get Firebase project nexus-hubs` + HTTP 403 `PERMISSION_DENIED`
Le compte de service s'authentifie mais n'a pas les droits sur le projet.
Deux causes possibles, à vérifier dans l'ordre :

1. **Firebase n'est pas activé sur le projet.**
   - <https://console.firebase.google.com> → **Ajouter un projet** →
     *Ajouter Firebase à un projet Google Cloud existant* → sélectionner `nexus-hubs`.
   - Puis **Build → Hosting → Commencer** pour créer le site `nexus-hubs.web.app`.

2. **Le compte de service n'a pas les bons rôles IAM.**
   Console Google Cloud → **IAM et administration → IAM** (projet `nexus-hubs`)
   → repérer le compte de service de la clé (ex. `firebase-adminsdk-xxxxx@nexus-hubs.iam.gserviceaccount.com`)
   → **Modifier** → ajouter :
   - **Administrateur Firebase Hosting** (`roles/firebasehosting.admin`)
   - **Consommateur Service Usage** (`roles/serviceusage.serviceUsageConsumer`)
   - **Lecteur Firebase** (`roles/firebase.viewer`) — pour `firebase.projects.get`

   > Alternative rapide (moins fine) : un seul rôle **Administrateur Firebase**
   > (`roles/firebase.admin`). Comptez 1–2 min de propagation avant de relancer.

3. **Vérifier le bon projet** : le champ `project_id` **dans le fichier JSON**
   du secret doit être exactement `nexus-hubs`. Sinon, la clé vient d'un autre
   projet → régénérez-la depuis les paramètres du projet `nexus-hubs`.

Après correction : **Actions → Deploy Frontend to Firebase Hosting → Run workflow**.

### Déploiement Firebase : `Permission 'run.services.get' denied ... (or resource may not exist)`
La réécriture `/api/**` de `firebase.json` pointe vers le service Cloud Run
`nexus-hub-api`, que Firebase valide à la finalisation. Deux causes :

1. **Le service Cloud Run n'existe pas encore.** Un déclencheur Cloud Build de
   type *Dockerfile* ne fait que **construire** l'image, il ne déploie rien.
   Pour créer le service, utilisez le pipeline **build + deploy** fourni :
   - Cloud Build → **Déclencheurs** → votre déclencheur → **Type de
     configuration** = *Fichier de configuration Cloud Build* →
     emplacement `cloudbuild.yaml`.
   - (ou, plus simple, Cloud Run → *Déployer le conteneur → Déployer en continu
     depuis un dépôt*, qui construit **et** déploie automatiquement.)
   - Le compte de service du build (souvent `PROJET_NUMBER-compute@developer.gserviceaccount.com`)
     doit avoir : **Administrateur Cloud Run** (`roles/run.admin`) et
     **Utilisateur du compte de service** (`roles/iam.serviceAccountUser`).

2. **Le compte de service Firebase ne peut pas lire le service.** Ajoutez-lui
   le rôle **Lecteur Cloud Run** (`roles/run.viewer`) sur le projet `nexus-hubs`.

> ⚠️ Ordre : le service Cloud Run doit être **en ligne** avant de relancer le
> workflow Firebase, sinon la finalisation échoue à nouveau.

## Récapitulatif des fichiers

| Fichier                        | Rôle                                                      |
| ------------------------------ | --------------------------------------------------------- |
| `firebase.json`                | Config Hosting + réécriture `/api/**` → Cloud Run         |
| `.firebaserc`                  | Projet Firebase par défaut (`nexus-hubs`)                 |
| `backend/main.py`              | API Flask (`/api/health`, `/api/status`, `/api/followers`)|
| `backend/Dockerfile`           | Image de conteneur Cloud Run                              |
| `backend/requirements.txt`     | Dépendances Python du backend                            |
| `backend/followers_data.json`  | Dernière valeur d'abonnés connue (fallback)              |
