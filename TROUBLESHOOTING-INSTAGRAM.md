# 🔧 Dépannage du Compteur Instagram

## ❌ Erreur Actuelle: ProfileNotExistsException

Cette erreur signifie qu'Instagram **refuse l'accès** au profil. Cela arrive dans 3 cas:

### 1. Session ID Expiré ou Invalide ⚠️ (Cause la plus probable)

Les Session ID Instagram **expirent régulièrement**. Si vous avez copié le Session ID il y a plusieurs jours/semaines, il est probablement expiré.

**Solution:** Récupérez un NOUVEAU Session ID

---

## 🔑 Comment Récupérer un NOUVEAU Session ID

### Méthode Détaillée (Pas à Pas)

#### Étape 1: Déconnectez-vous d'Instagram

1. Allez sur https://www.instagram.com
2. **Déconnectez-vous** (Menu → Se déconnecter)
3. **Fermez complètement le navigateur** (toutes les fenêtres)

#### Étape 2: Ouvrez un Nouvel Onglet en Navigation Privée

**Pourquoi?** Pour avoir des cookies frais sans cache.

- **Chrome/Edge:** `Ctrl + Shift + N` (Windows) ou `Cmd + Shift + N` (Mac)
- **Firefox:** `Ctrl + Shift + P` (Windows) ou `Cmd + Shift + P` (Mac)

#### Étape 3: Connectez-vous à Instagram

1. Dans la fenêtre privée, allez sur https://www.instagram.com
2. **Connectez-vous avec votre compte** `@merickkn`
3. **NE PAS cocher "Enregistrer les informations"** si demandé
4. Attendez d'être complètement connecté

#### Étape 4: Ouvrez les Outils de Développement

Appuyez sur **F12** (ou clic droit → Inspecter)

#### Étape 5: Allez dans l'Onglet Application/Storage

- **Chrome/Edge:** Cliquez sur l'onglet **"Application"**
- **Firefox:** Cliquez sur l'onglet **"Stockage"**

#### Étape 6: Trouvez le Cookie sessionid

1. Dans le menu de gauche:
   - Cliquez sur **"Cookies"**
   - Puis sur **"https://www.instagram.com"**

2. Dans la liste des cookies, cherchez **`sessionid`**
   - ⚠️ PAS `ds_user_id`, PAS `csrftoken`, seulement **`sessionid`**

3. **Double-cliquez** sur la valeur pour la sélectionner
4. **Copiez-la** entièrement (Ctrl+C ou Cmd+C)

#### Étape 7: Vérifiez la Valeur Copiée

La valeur devrait ressembler à ça:
```
12345678%3A1AbCdEfGhIjKlMnOp%3A28%3AqRsTuVwXyZ...
```

**Caractéristiques:**
- Environ 50-100 caractères
- Contient des `%3A` (c'est normal!)
- Commence par des chiffres
- Contient des lettres et chiffres mélangés

⚠️ **Ne modifiez PAS la valeur!** Copiez-la exactement comme elle est.

---

## 🔐 Mettre à Jour le Secret dans GitHub

### Méthode 1: Mettre à Jour le Secret Existant

1. Allez sur: https://github.com/nexusproject2077/nexus-hub/settings/secrets/actions
2. Trouvez **`INSTA_SESSION_ID`**
3. Cliquez sur le **crayon** (Update) à droite
4. **Collez le NOUVEAU Session ID** (Ctrl+V)
5. Cliquez sur **"Update secret"**

### Méthode 2: Supprimer et Recréer

1. Allez sur: https://github.com/nexusproject2077/nexus-hub/settings/secrets/actions
2. Trouvez **`INSTA_SESSION_ID`**
3. Cliquez sur **"Remove"** (Supprimer)
4. Cliquez sur **"New repository secret"**
5. Name: `INSTA_SESSION_ID`
6. Value: (collez le nouveau Session ID)
7. Cliquez sur **"Add secret"**

---

## 🚀 Tester Après la Mise à Jour

1. Allez sur: https://github.com/nexusproject2077/nexus-hub/actions
2. Cliquez sur **"Update Instagram Followers Count"**
3. Cliquez sur **"Run workflow"** → **"Run workflow"**
4. Attendez 2-3 minutes
5. Cliquez sur le workflow qui vient de se terminer
6. Cliquez sur **"update"** (le job)
7. Regardez les logs:

**Logs de Succès:**
```
✅ Tentative de connexion avec Session ID pour l'utilisateur: merickkn
✅ Session ID présent: Oui
✅ Longueur du Session ID: 87 caractères
✅ Cookies injectés, tentative de chargement du profil...
✅ Nombre d'abonnés récupéré: 1234
✅ Données écrites dans fils/followers_data.json avec statut: success
```

**Logs d'Échec:**
```
❌ DIAGNOSTIC: Le profil Instagram n'a pas été trouvé
❌ Causes possibles:
   1. Le Session ID est expiré ou invalide
```

---

## 🔍 Diagnostics Courants

### Erreur: "Session ID présent: Non"

**Problème:** Le secret n'est pas configuré dans GitHub
**Solution:** Vérifiez que le secret `INSTA_SESSION_ID` existe dans Settings → Secrets

### Erreur: "Longueur du Session ID: 0 caractères"

**Problème:** Le secret est vide
**Solution:** Supprimez et recréez le secret avec une valeur valide

### Erreur: "ProfileNotExistsException"

**Problème:** Session ID invalide ou expiré
**Solution:** Récupérez un NOUVEAU Session ID (voir ci-dessus)

### Erreur: "LoginRequiredException"

**Problème:** Instagram exige une authentification complète
**Solution:** Le Session ID est expiré, récupérez-en un nouveau

### Succès mais compteur affiche "0"

**Problème:** Le fichier JSON n'a pas été copié à la racine
**Solution:** Vérifiez que le workflow contient bien l'étape "Copy data to root"

---

## 💡 Astuces pour Garder le Session ID Valide Plus Longtemps

1. **Restez connecté sur Instagram dans votre navigateur principal**
   - Si vous vous déconnectez partout, tous les Session ID expirent

2. **Ne copiez pas le Session ID trop souvent**
   - Instagram peut détecter une activité suspecte

3. **Utilisez le même navigateur**
   - Copiez toujours depuis le même navigateur où vous restez connecté

4. **Fréquence d'utilisation**
   - Le workflow toutes les 6 heures est OK
   - Ne lancez pas le workflow manuellement trop souvent (max 1-2 fois/heure)

---

## ⚠️ Limitations d'Instagram

Instagram peut bloquer l'accès si:
- Vous lancez le script trop souvent (+ de 1 fois par heure)
- Instagram détecte une activité "bot-like"
- Votre compte Instagram est récent (< 1 mois)
- Votre compte a déjà été signalé

**Solution:** Utilisez le workflow automatique (toutes les 6h) sans lancer manuellement trop souvent.

---

## 🆘 Si Rien ne Fonctionne

### Option 1: Attendre 24-48 heures

Instagram peut avoir temporairement bloqué votre compte. Attendez 24-48h et réessayez.

### Option 2: Alternative Sans Session ID

Si vous n'arrivez vraiment pas à faire fonctionner le Session ID, vous pouvez:

1. **Utiliser un compteur manuel** (modifier `followers_data.json` manuellement)
2. **Utiliser un service tiers** (comme l'API Instagram officielle - mais nécessite une entreprise)
3. **Afficher un compteur statique** (mettre un nombre fixe)

---

## 📊 Vérifier le Fichier JSON

Le fichier `followers_data.json` devrait ressembler à ça en cas de **succès**:

```json
{
    "timestamp": 1768837418,
    "followers": 1234,
    "status": "success"
}
```

En cas **d'échec**:

```json
{
    "timestamp": 1768837418,
    "followers": 0,
    "status": "failed_retaining_old_data: ProfileNotExistsException"
}
```

Vous pouvez voir ce fichier ici: https://github.com/nexusproject2077/nexus-hub/blob/main/followers_data.json

---

## ✅ Checklist de Dépannage

- [ ] J'ai récupéré un NOUVEAU Session ID (en navigation privée)
- [ ] J'ai vérifié que le Session ID est long (50-100 caractères)
- [ ] J'ai copié le Session ID ENTIER (avec les %3A)
- [ ] J'ai mis à jour le secret dans GitHub (crayon → Update)
- [ ] J'ai attendu que le secret soit sauvegardé (confirmation verte)
- [ ] J'ai lancé le workflow manuellement pour tester
- [ ] J'ai vérifié les logs du workflow (onglet "update")
- [ ] J'ai attendu 2-3 minutes pour le redéploiement Netlify
- [ ] J'ai vérifié mon site: https://nexus-hubs.netlify.app/

Si toutes les cases sont cochées et ça ne fonctionne toujours pas, attendez 24h (Instagram pourrait avoir bloqué temporairement).

---

**Bon courage! 🚀**
