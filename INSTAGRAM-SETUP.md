# 📸 Guide Rapide - Compteur Instagram

## ✅ Votre site est déployé sur Netlify!
**URL:** https://nexus-hubs.netlify.app/

Maintenant, configurons le compteur d'abonnés Instagram pour qu'il se mette à jour automatiquement toutes les 6 heures! 🚀

---

## 🔑 Étape 1: Obtenir votre Session ID Instagram

### Méthode Simple (Recommandée)

1. **Ouvrez Instagram dans votre navigateur** (Chrome, Firefox, Edge...)
   - Allez sur: https://www.instagram.com
   - **Connectez-vous** à votre compte (@merickn)

2. **Ouvrez les outils de développement**
   - **Windows/Linux:** Appuyez sur `F12`
   - **Mac:** Appuyez sur `Cmd + Option + I`

3. **Allez dans l'onglet Application/Storage**
   - **Chrome/Edge:** Cliquez sur l'onglet **"Application"** en haut
   - **Firefox:** Cliquez sur l'onglet **"Stockage"**

4. **Trouvez les Cookies Instagram**
   - Dans le menu de gauche, cliquez sur **"Cookies"**
   - Puis cliquez sur **"https://www.instagram.com"**

5. **Copiez le Session ID**
   - Cherchez le cookie nommé **`sessionid`** (attention à l'orthographe!)
   - **Double-cliquez** sur la valeur pour la sélectionner
   - **Copiez-la** (Ctrl+C ou Cmd+C)
   - ⚠️ Elle ressemble à ça: `12345678%3Aabcdefgh%3A...` (environ 50-70 caractères)

### 📸 Aide Visuelle

```
Outils Développeur (F12)
  ↓
Onglet "Application" (ou "Storage")
  ↓
Menu gauche → "Cookies" → "https://www.instagram.com"
  ↓
Cherchez: sessionid
  ↓
Copiez la VALEUR (longue chaîne de caractères)
```

---

## 🔐 Étape 2: Configurer les Secrets GitHub

### 2.1 Aller dans les Paramètres GitHub

1. Allez sur votre dépôt: https://github.com/nexusproject2077/nexus-hub
2. Cliquez sur **"Settings"** (⚙️ en haut à droite)
3. Dans le menu de gauche:
   - Cliquez sur **"Secrets and variables"**
   - Puis sur **"Actions"**

### 2.2 Ajouter le Premier Secret (Username)

1. Cliquez sur **"New repository secret"** (bouton vert)
2. Remplissez:
   - **Name:** `INSTA_USERNAME`
   - **Value:** `merickn`
3. Cliquez sur **"Add secret"**

### 2.3 Ajouter le Deuxième Secret (Session ID)

1. Cliquez encore sur **"New repository secret"**
2. Remplissez:
   - **Name:** `INSTA_SESSION_ID`
   - **Value:** (collez le sessionid que vous avez copié à l'étape 1)
   - ⚠️ **Attention:** Collez TOUTE la valeur, ne modifiez rien!
3. Cliquez sur **"Add secret"**

### ✅ Vérification

Vous devriez maintenant voir deux secrets:
- `INSTA_USERNAME`
- `INSTA_SESSION_ID`

---

## 🚀 Étape 3: Lancer le Compteur pour la Première Fois

### 3.1 Aller dans GitHub Actions

1. Sur votre dépôt, cliquez sur l'onglet **"Actions"** (en haut)
2. Dans la liste des workflows à gauche, cliquez sur:
   **"Update Instagram Followers Count"**

### 3.2 Lancer le Workflow Manuellement

1. Cliquez sur le bouton **"Run workflow"** (à droite)
2. Une petite fenêtre s'ouvre
3. Cliquez encore sur **"Run workflow"** (bouton vert)

### 3.3 Attendre l'Exécution

- Le workflow va s'exécuter (petit cercle orange qui tourne)
- Attendez **2-3 minutes**
- Quand c'est terminé, vous verrez une coche verte ✅

### 3.4 Vérifier que ça Fonctionne

1. Cliquez sur l'exécution qui vient de se terminer
2. Cliquez sur **"update"** (le job)
3. Regardez les logs:
   - Vous devriez voir: `"status": "success"`
   - Et votre vrai nombre d'abonnés!

---

## 🌐 Étape 4: Vérifier sur Netlify

### 4.1 Attendre le Redéploiement

Netlify détecte automatiquement les changements sur GitHub:
- Après que GitHub Actions ait mis à jour `followers_data.json`
- Netlify redéploie automatiquement (1-2 minutes)

### 4.2 Voir le Résultat

1. Allez sur votre site: https://nexus-hubs.netlify.app/
2. Regardez la section avec votre photo Instagram (@merickn)
3. **Le nombre d'abonnés devrait s'afficher!** 🎉

---

## 🔄 Fonctionnement Automatique

Une fois configuré, tout est automatique:

```
┌────────────────────────────────────────┐
│ TOUTES LES 6 HEURES (automatique):    │
│                                        │
│ 1. GitHub Actions se lance            │
│    ↓                                   │
│ 2. Récupère vos abonnés Instagram     │
│    ↓                                   │
│ 3. Met à jour followers_data.json     │
│    ↓                                   │
│ 4. Commit automatique sur GitHub      │
│    ↓                                   │
│ 5. Netlify détecte le changement      │
│    ↓                                   │
│ 6. Redéploie votre site               │
│    ↓                                   │
│ 7. ✅ Compteur mis à jour!             │
└────────────────────────────────────────┘
```

Vous n'avez **rien à faire**, tout se met à jour automatiquement! 🚀

---

## 🔧 Dépannage

### ❌ Le compteur affiche "Erreur" ou "0"

**Cause 1: Session ID incorrect ou expiré**
- ✅ Revérifiez que vous avez copié TOUT le sessionid
- ✅ Assurez-vous qu'il n'y a pas d'espaces avant/après
- ✅ Récupérez un nouveau Session ID (voir Étape 1)
- ✅ Mettez à jour le secret dans GitHub

**Cause 2: Les secrets ne sont pas configurés**
- ✅ Vérifiez que les deux secrets existent dans GitHub
- ✅ Vérifiez l'orthographe: `INSTA_USERNAME` et `INSTA_SESSION_ID`
- ✅ Relancez le workflow manuellement

**Cause 3: Instagram a bloqué temporairement**
- ✅ Attendez quelques heures
- ✅ Ne relancez pas le workflow trop souvent (max 1-2 fois par heure)

### ❌ Le workflow échoue dans GitHub Actions

1. Allez dans l'onglet "Actions"
2. Cliquez sur l'exécution qui a échoué (croix rouge ❌)
3. Lisez les logs pour voir l'erreur
4. Vérifiez que les secrets sont bien configurés

### ❌ Netlify ne redéploie pas automatiquement

1. Allez sur votre dashboard Netlify
2. Vérifiez que "Auto publishing" est activé
3. Vous pouvez forcer un redéploiement:
   - Site settings → Build & deploy → Trigger deploy → Deploy site

---

## ⏰ Changer la Fréquence de Mise à Jour

Par défaut: toutes les 6 heures.

Pour changer:
1. Ouvrez `.github/workflows/update_followers.yml`
2. Ligne avec `cron: '0 */6 * * *'`
3. Modifiez:
   - `*/3` = toutes les 3 heures
   - `*/12` = toutes les 12 heures
   - `0 9 * * *` = tous les jours à 9h

---

## 💡 Conseils

### 🔐 Sécurité du Session ID

- ⚠️ Ne partagez JAMAIS votre Session ID (c'est comme votre mot de passe!)
- ✅ Le Session ID est stocké de manière sécurisée dans les secrets GitHub
- ✅ Il n'est jamais visible dans les logs publics

### ⏳ Durée de Validité

- Un Session ID reste valide pendant plusieurs semaines/mois
- Si votre compteur arrête de fonctionner après un moment:
  - Récupérez un nouveau Session ID
  - Mettez à jour le secret dans GitHub
  - Relancez le workflow

### 🚀 Performance

- Le compteur se met à jour toutes les 6 heures
- Netlify redéploie en 1-2 minutes
- Votre site est toujours à jour!

---

## 📋 Checklist Rapide

- [ ] ✅ Récupérer le Session ID Instagram (F12 → Cookies → sessionid)
- [ ] ✅ Ajouter `INSTA_USERNAME` dans les secrets GitHub
- [ ] ✅ Ajouter `INSTA_SESSION_ID` dans les secrets GitHub
- [ ] ✅ Lancer le workflow manuellement (Actions → Run workflow)
- [ ] ✅ Vérifier que ça fonctionne (logs verts ✅)
- [ ] ✅ Voir le résultat sur https://nexus-hubs.netlify.app/
- [ ] 🎉 Profiter du compteur automatique!

---

## 🆘 Besoin d'Aide?

Si quelque chose ne fonctionne pas:
1. Relisez la section "Dépannage" ci-dessus
2. Vérifiez les logs dans GitHub Actions
3. Assurez-vous que les secrets sont bien configurés
4. Essayez de récupérer un nouveau Session ID

---

**Bon comptage! 📸🚀**
