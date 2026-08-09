# Guide de Déploiement - NEXUS HUB sur Render

## Prérequis

1. Un compte GitHub (vous l'avez déjà)
2. Un compte Render gratuit (à créer sur https://render.com)
3. Vos identifiants Instagram pour le compteur

---

## Étape 1: Configurer les Secrets GitHub (pour le compteur Instagram)

Le compteur d'abonnés Instagram fonctionne via GitHub Actions qui met à jour le nombre toutes les 6 heures.

### 1.1 Obtenir votre Session ID Instagram

1. Connectez-vous à Instagram sur votre navigateur
2. Ouvrez les outils de développement (F12)
3. Allez dans l'onglet "Application" ou "Stockage"
4. Cliquez sur "Cookies" → "https://www.instagram.com"
5. Cherchez le cookie nommé `sessionid`
6. Copiez sa valeur (une longue chaîne de caractères)

### 1.2 Ajouter les secrets dans GitHub

1. Allez sur votre dépôt GitHub: https://github.com/nexusproject2077/nexus-hub
2. Cliquez sur "Settings" (Paramètres)
3. Dans le menu de gauche, cliquez sur "Secrets and variables" → "Actions"
4. Cliquez sur "New repository secret"
5. Ajoutez deux secrets:

   **Secret 1:**
   - Name: `INSTA_USERNAME`
   - Value: `merickn` (votre nom d'utilisateur Instagram)

   **Secret 2:**
   - Name: `INSTA_SESSION_ID`
   - Value: (collez la valeur du sessionid que vous avez copiée)

---

## Étape 2: Tester le Workflow GitHub Actions

1. Allez dans l'onglet "Actions" de votre dépôt GitHub
2. Cliquez sur le workflow "Update Instagram Followers Count"
3. Cliquez sur "Run workflow" → "Run workflow"
4. Attendez quelques minutes que le workflow se termine
5. Vérifiez que le fichier `followers_data.json` a été mis à jour avec vos vrais abonnés

---

## Étape 3: Déployer sur Render

### 3.1 Créer un compte Render

1. Allez sur https://render.com
2. Cliquez sur "Get Started" ou "Sign Up"
3. Inscrivez-vous avec votre compte GitHub (recommandé)

### 3.2 Créer un nouveau site statique

1. Une fois connecté, cliquez sur "New +" en haut à droite
2. Sélectionnez "Static Site"
3. Connectez votre compte GitHub si ce n'est pas déjà fait
4. Cherchez et sélectionnez le dépôt `nexus-hub`
5. Configurez les paramètres:

   **Configuration:**
   - **Name**: `nexus-hub` (ou un nom de votre choix)
   - **Branch**: `main` (ou la branche que vous souhaitez déployer)
   - **Build Command**: (laissez vide ou mettez `echo "Site statique"`)
   - **Publish Directory**: `.` (point pour la racine)

6. Cliquez sur "Create Static Site"

### 3.3 Attendre le déploiement

- Render va automatiquement déployer votre site
- Le premier déploiement prend environ 1-2 minutes
- Une fois terminé, vous verrez "Live" en vert

### 3.4 Obtenir l'URL de votre site

- Render vous donnera une URL gratuite du type: `https://nexus-hub.onrender.com`
- Vous pouvez cliquer dessus pour voir votre site en ligne!

---

## Étape 4: Configurer le Déploiement Automatique

**Bonne nouvelle:** C'est déjà fait automatiquement!

Render détecte les changements sur votre branche GitHub et redéploie automatiquement:
- Quand vous faites un commit
- Quand le workflow GitHub Actions met à jour `followers_data.json`

---

## Étape 5: Vérifier que le Compteur Instagram Fonctionne

1. Allez sur votre site Render
2. Regardez la section avec votre photo Instagram (@merickn)
3. Le nombre d'abonnés devrait s'afficher (formaté en K si > 1000)
4. Si vous voyez "...", "0" ou "Erreur", attendez quelques minutes ou vérifiez:
   - Que les secrets GitHub sont bien configurés
   - Que le workflow GitHub Actions a été exécuté avec succès
   - Que le fichier `followers_data.json` existe à la racine du projet

---

## Comment ça Fonctionne?

### Architecture du Compteur Instagram

```
GitHub Actions (toutes les 6h)
         ↓
   Script Python (fetch_followers.py)
         ↓
   Récupère les abonnés via Instaloader
         ↓
   Sauvegarde dans fils/followers_data.json
         ↓
   Copie vers followers_data.json (racine)
         ↓
   Commit automatique sur GitHub
         ↓
   Render détecte le changement
         ↓
   Redéploiement automatique
         ↓
   Votre site affiche le nouveau nombre
```

### Fichiers Importants

- **`fetch_followers.py`**: Script qui récupère les abonnés Instagram
- **`.github/workflows/update_followers.yml`**: Configuration du workflow automatique
- **`followers_data.json`**: Fichier avec le nombre d'abonnés (mis à jour toutes les 6h)
- **`app.js`**: Script qui charge et affiche le nombre sur votre site
- **`render.yaml`**: Configuration pour Render (optionnel mais inclus)

---

## Dépannage

### Le compteur affiche "Erreur" ou "0"

1. Vérifiez que les secrets GitHub sont bien configurés
2. Vérifiez que votre Session ID Instagram est toujours valide (il expire parfois)
3. Relancez manuellement le workflow dans l'onglet Actions de GitHub
4. Vérifiez les logs du workflow pour voir les erreurs

### Le compteur ne se met pas à jour

1. Vérifiez que le workflow GitHub Actions s'exécute bien toutes les 6 heures
2. Vérifiez que Render redéploie automatiquement après les commits
3. Vous pouvez forcer un redéploiement manuel dans Render (bouton "Manual Deploy")

### Le site ne se déploie pas sur Render

1. Vérifiez que la branche est bien `main` (ou celle que vous avez configurée)
2. Vérifiez les logs de build dans Render pour voir les erreurs
3. Assurez-vous que le dépôt GitHub est public ou que Render a accès

---

## Maintenance

### Mettre à jour le Session ID Instagram

Si votre compteur arrête de fonctionner, c'est probablement que votre Session ID a expiré:

1. Récupérez un nouveau Session ID (voir Étape 1.1)
2. Allez dans les secrets GitHub
3. Modifiez le secret `INSTA_SESSION_ID` avec la nouvelle valeur
4. Relancez le workflow manuellement

### Personnaliser l'URL

Render offre des domaines personnalisés dans le plan gratuit:
1. Allez dans les paramètres de votre site sur Render
2. Section "Custom Domains"
3. Ajoutez votre propre domaine (si vous en avez un)

---

## Prochaines Étapes

Une fois votre site déployé:
- Partagez l'URL avec vos amis!
- Le compteur Instagram se mettra à jour automatiquement toutes les 6 heures
- Vous pouvez modifier le code et il se redéploiera automatiquement
- Consultez les statistiques de visite dans le dashboard Render

---

## Support

Si vous rencontrez des problèmes:
1. Vérifiez les logs dans l'onglet "Actions" de GitHub
2. Vérifiez les logs de déploiement dans Render
3. Assurez-vous que tous les fichiers sont bien présents dans votre dépôt

Bon déploiement! 🚀
