# 🔐 Guide: Obtenir l'API Meta Officielle pour Instagram

## 📋 Prérequis

- ✅ Un compte Instagram (le vôtre: @merickkn)
- ✅ Un compte Facebook (obligatoire, même si vous ne l'utilisez pas)
- ✅ Un email vérifié
- ✅ 15-30 minutes de temps

---

## 🎯 Quelle API Choisir?

Il existe 2 APIs Instagram officielles:

### 1. **Instagram Basic Display API** ⭐ (Recommandé pour vous)
- ✅ Pour les **comptes personnels**
- ✅ Accès à vos propres stats (abonnés, posts, etc.)
- ✅ Gratuit et simple
- ✅ Pas besoin d'approbation Meta complexe
- ❌ Fonctionne **uniquement pour votre propre compte**

### 2. **Instagram Graph API**
- Pour les **comptes Business/Créateurs**
- Accès aux insights marketing
- Nécessite approbation Meta stricte
- Plus complexe

**Pour votre cas:** Utilisez **Instagram Basic Display API** ✅

---

## 📝 Étape 1: Créer une App Meta Developers

### 1.1 Aller sur Meta for Developers

👉 https://developers.facebook.com/

### 1.2 Se connecter

Connectez-vous avec votre compte Facebook.

### 1.3 Créer une App

1. Cliquez sur **"Mes Apps"** (ou "My Apps") en haut à droite
2. Cliquez sur **"Créer une App"** (Create App)
3. **Sélectionnez le type:** "Consommateur" (Consumer) ou "Autre" (Other)
4. Cliquez sur **"Suivant"**

### 1.4 Configurer l'App

**Nom de l'app:** `nexus-hub-instagram` (ou ce que vous voulez)

**Email de contact:** Votre email

**Compte Meta Business (optionnel):** Laissez vide pour commencer

Cliquez sur **"Créer l'app"**

### 1.5 Vérification de sécurité

Complétez le CAPTCHA de sécurité.

---

## 📝 Étape 2: Configurer Instagram Basic Display API

### 2.1 Ajouter le Produit Instagram

1. Dans votre app, allez dans **"Ajouter des produits"** (Add Products)
2. Cherchez **"Instagram Basic Display"**
3. Cliquez sur **"Configurer"** (Set Up)

### 2.2 Créer une App Instagram

1. Scrollez jusqu'à **"Basic Display"**
2. Cliquez sur **"Créer une nouvelle app"** (Create New App)
3. Nom: `nexus-hub-instagram`
4. Cliquez sur **"Créer l'app"**

### 2.3 Configurer les Paramètres

Vous allez voir plusieurs champs à remplir:

**OAuth Redirect URIs:**
```
https://nexus-hubs.netlify.app/instagram-callback
https://localhost:8000/callback
```

**Deauthorize Callback URL:**
```
https://nexus-hubs.netlify.app/instagram-deauth
```

**Data Deletion Request URL:**
```
https://nexus-hubs.netlify.app/instagram-delete
```

Cliquez sur **"Enregistrer les modifications"** (Save Changes)

### 2.4 Noter les Credentials

Dans la même page, notez:

- **Instagram App ID:** (exemple: 123456789012345)
- **Instagram App Secret:** (cliquez sur "Afficher" pour voir)
- **Client OAuth Token:** On le générera plus tard

⚠️ **NE PARTAGEZ JAMAIS ces identifiants!**

---

## 📝 Étape 3: Ajouter un Utilisateur Test Instagram

### 3.1 Ajouter votre compte Instagram

1. Toujours dans **Instagram Basic Display**
2. Section **"Rôles"** → **"Utilisateurs Instagram testeurs"**
3. Cliquez sur **"Ajouter des utilisateurs Instagram testeurs"**
4. Entrez votre username Instagram: `merickkn`
5. Cliquez sur **"Soumettre"**

### 3.2 Accepter l'Invitation

1. Connectez-vous à Instagram (app mobile ou web)
2. Allez dans **Paramètres** → **Apps et sites web**
3. Vous verrez une invitation de **"Testeur"**
4. **Acceptez l'invitation**

⚠️ Cette étape est **CRITIQUE** - sans ça, l'API ne fonctionnera pas!

---

## 📝 Étape 4: Générer un Token d'Accès

### 4.1 Construire l'URL d'Autorisation

Remplacez `{app-id}` et `{redirect-uri}` dans cette URL:

```
https://api.instagram.com/oauth/authorize
  ?client_id={app-id}
  &redirect_uri={redirect-uri}
  &scope=user_profile,user_media
  &response_type=code
```

**Exemple réel:**
```
https://api.instagram.com/oauth/authorize?client_id=123456789012345&redirect_uri=https://nexus-hubs.netlify.app/instagram-callback&scope=user_profile,user_media&response_type=code
```

### 4.2 Ouvrir l'URL dans le Navigateur

1. Copiez l'URL complète dans votre navigateur
2. Cliquez sur **"Autoriser"** (Authorize)
3. Vous serez redirigé vers une page avec un code dans l'URL

**Exemple:**
```
https://nexus-hubs.netlify.app/instagram-callback?code=AQXXXXXXXXXXXXX
```

### 4.3 Copier le Code

Copiez la valeur après `code=` (commence par AQ généralement)

**Exemple:** `AQXXXXXXXXXXXXX#_`

⚠️ **Ce code expire en 60 secondes!** Passez vite à l'étape suivante.

---

## 📝 Étape 5: Échanger le Code contre un Token

### 5.1 Préparer la Requête

Vous avez besoin de:
- **app-id:** Votre Instagram App ID
- **app-secret:** Votre Instagram App Secret
- **code:** Le code que vous venez de copier
- **redirect-uri:** La même URL de redirect

### 5.2 Faire la Requête (avec curl ou Postman)

**Option A: Avec curl (Terminal/CMD):**

```bash
curl -X POST \
  https://api.instagram.com/oauth/access_token \
  -F client_id=VOTRE_APP_ID \
  -F client_secret=VOTRE_APP_SECRET \
  -F grant_type=authorization_code \
  -F redirect_uri=https://nexus-hubs.netlify.app/instagram-callback \
  -F code=LE_CODE_OBTENU
```

**Option B: Avec un script Python:**

```python
import requests

data = {
    'client_id': 'VOTRE_APP_ID',
    'client_secret': 'VOTRE_APP_SECRET',
    'grant_type': 'authorization_code',
    'redirect_uri': 'https://nexus-hubs.netlify.app/instagram-callback',
    'code': 'LE_CODE_OBTENU'
}

response = requests.post('https://api.instagram.com/oauth/access_token', data=data)
print(response.json())
```

### 5.3 Récupérer le Token

La réponse contiendra:

```json
{
  "access_token": "IGQVJ...",
  "user_id": 123456789
}
```

**Copiez le `access_token`!** C'est votre token d'accès!

---

## 📝 Étape 6: Obtenir un Token Longue Durée (60 jours)

Le token que vous venez d'obtenir expire en **1 heure**. Transformons-le en token de **60 jours**:

```bash
curl -X GET \
  "https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret=VOTRE_APP_SECRET&access_token=VOTRE_TOKEN_COURT"
```

Réponse:

```json
{
  "access_token": "IGQVJ...",
  "token_type": "bearer",
  "expires_in": 5184000  // 60 jours
}
```

**Sauvegardez ce nouveau token!** C'est celui que vous utiliserez.

---

## 📝 Étape 7: Tester l'API

### 7.1 Récupérer Vos Infos

```bash
curl -X GET \
  "https://graph.instagram.com/me?fields=id,username&access_token=VOTRE_TOKEN"
```

Réponse:

```json
{
  "id": "123456789",
  "username": "merickkn"
}
```

### 7.2 Récupérer Vos Stats (abonnés)

⚠️ **ATTENTION:** L'API Basic Display **ne donne PAS le nombre d'abonnés directement!**

Elle donne:
- ✅ Votre liste de posts
- ✅ Vos informations de profil
- ❌ **PAS** le nombre d'abonnés

**Pour avoir les abonnés, il faut:**
- Passer en **compte Business/Créateur** sur Instagram
- Utiliser l'**Instagram Graph API** (plus complexe)

---

## 🔄 Alternative: Instagram Graph API (Avec Abonnés)

### Prérequis Supplémentaires:

1. **Convertir votre compte Instagram en Business/Créateur:**
   - Instagram → Paramètres → Compte → Passer au compte professionnel
   - Choisir "Créateur" ou "Entreprise"

2. **Connecter votre Instagram à une Page Facebook:**
   - Créez une page Facebook (même vide)
   - Liez votre compte Instagram à cette page

3. **Utiliser l'API Graph avec votre Page:**
   - L'API Graph donne accès aux insights incluant les abonnés
   - Mais nécessite plus de configuration

### Récupérer les Abonnés avec Graph API:

```bash
curl -X GET \
  "https://graph.facebook.com/v18.0/{instagram-business-account-id}?fields=followers_count,username&access_token=VOTRE_TOKEN"
```

Réponse:

```json
{
  "followers_count": 1234,
  "username": "merickkn",
  "id": "123456789"
}
```

---

## 🔧 Étape 8: Intégrer dans Votre Projet

### 8.1 Créer un Script Python

Je vais créer un script qui utilise votre token Meta:

```python
import requests
import os
import json
import time

# Configuration
ACCESS_TOKEN = os.environ.get('META_ACCESS_TOKEN')  # Token longue durée
IG_USER_ID = os.environ.get('IG_USER_ID')  # Votre Instagram User ID
OUTPUT_FILE = 'fils/followers_data.json'

def fetch_followers():
    """Récupère via l'API Meta officielle"""

    data = {
        "timestamp": int(time.time()),
        "followers": 0,
        "status": "initial_failure"
    }

    try:
        # Récupérer les stats via Graph API
        url = f'https://graph.facebook.com/v18.0/{IG_USER_ID}'
        params = {
            'fields': 'followers_count,username',
            'access_token': ACCESS_TOKEN
        }

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            result = response.json()
            followers = result.get('followers_count', 0)

            data['followers'] = followers
            data['status'] = 'success_meta_api'
            print(f"✅ Abonnés récupérés via Meta API: {followers}")
        else:
            print(f"❌ Erreur API: {response.status_code}")
            data['status'] = f'failed_meta_api_{response.status_code}'

    except Exception as e:
        print(f"❌ Erreur: {e}")
        data['status'] = f'failed: {type(e).__name__}'

    finally:
        # Sauvegarder
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    return data

if __name__ == "__main__":
    fetch_followers()
```

### 8.2 Ajouter les Secrets GitHub

1. Allez dans vos secrets GitHub
2. Ajoutez:
   - `META_ACCESS_TOKEN`: Votre token longue durée
   - `IG_USER_ID`: Votre Instagram User ID (obtenu à l'étape 7.1)

---

## 🔄 Renouvellement du Token

Le token expire après **60 jours**. Pour le renouveler:

```bash
curl -X GET \
  "https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=VOTRE_TOKEN_ACTUEL"
```

**Automatisez ce renouvellement** en le faisant toutes les 50 jours dans votre workflow GitHub Actions.

---

## ✅ Avantages de l'API Meta Officielle

- ✅ **Gratuit** (pas de limite pour usage personnel)
- ✅ **Légal et officiel**
- ✅ **Fiable** (pas de blocage)
- ✅ **Données en temps réel**
- ✅ Token valable **60 jours** (renouvelable)

## ❌ Inconvénients

- ❌ **Configuration complexe** (30-60 min la première fois)
- ❌ Nécessite un **compte Business/Créateur** pour les abonnés
- ❌ Token à **renouveler tous les 60 jours**
- ❌ Fonctionne **uniquement pour votre propre compte**

---

## 🆘 Dépannage

### "Redirect URI Mismatch"
→ Vérifiez que l'URL de redirect est **exactement** la même partout

### "User Not Authorized"
→ Assurez-vous d'avoir **accepté l'invitation** comme testeur Instagram

### "Invalid Client ID"
→ Vérifiez que vous utilisez l'**Instagram App ID**, pas le Facebook App ID

### Pas de champ "followers_count"
→ Votre compte doit être en **mode Business/Créateur** sur Instagram

---

## 💡 Recommandation Finale

**Pour un compteur simple sur votre site:**

1. **Si vous avez 1-2 heures devant vous:** Suivez ce guide pour l'API Meta
2. **Si vous voulez quelque chose qui fonctionne en 5 min:** Restez avec la solution manuelle actuelle

L'API Meta est la solution **la plus professionnelle**, mais la solution manuelle que j'ai implémentée est **la plus pragmatique** pour un usage simple.

---

**Besoin d'aide pour une étape? Dites-moi où vous bloquez!** 🚀
