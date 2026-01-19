# Guide de Déploiement - NEXUS HUB sur GitHub Pages (100% GRATUIT)

GitHub Pages est **totalement gratuit** et illimité pour les projets publics! 🎉

---

## Étape 1: Configurer les Secrets Instagram (IMPORTANT)

### 1.1 Obtenir votre Session ID Instagram

1. Connectez-vous à Instagram sur votre navigateur
2. Appuyez sur **F12** pour ouvrir les outils de développement
3. Allez dans l'onglet **"Application"** (ou "Storage" sur Firefox)
4. Cliquez sur **"Cookies"** → **"https://www.instagram.com"**
5. Cherchez le cookie nommé **`sessionid`**
6. **Copiez sa valeur** (longue chaîne de caractères, genre: `12345678%3A...`)

### 1.2 Ajouter les secrets dans GitHub

1. Allez sur: https://github.com/nexusproject2077/nexus-hub
2. Cliquez sur **"Settings"** (Paramètres)
3. Menu de gauche → **"Secrets and variables"** → **"Actions"**
4. Cliquez sur **"New repository secret"**
5. Ajoutez **deux secrets**:

   **Secret 1:**
   - Name: `INSTA_USERNAME`
   - Value: `merickkn`

   **Secret 2:**
   - Name: `INSTA_SESSION_ID`
   - Value: (collez la valeur du sessionid copiée)

6. Cliquez sur **"Add secret"** pour chaque

---

## Étape 2: Activer GitHub Pages

### 2.1 Activer GitHub Pages dans les paramètres

1. Sur votre dépôt GitHub: https://github.com/nexusproject2077/nexus-hub
2. Cliquez sur **"Settings"**
3. Menu de gauche → **"Pages"**
4. Dans **"Build and deployment"**:
   - **Source**: Sélectionnez **"GitHub Actions"**

5. **C'est tout!** GitHub Pages est maintenant activé

### 2.2 Lancer le premier déploiement

**Option A: Automatique (Recommandé)**
- Faites un simple commit sur la branche `main`
- Le site se déploiera automatiquement

**Option B: Manuel**
1. Allez dans l'onglet **"Actions"**
2. Cliquez sur **"Deploy to GitHub Pages"** (workflow à gauche)
3. Cliquez sur **"Run workflow"** → **"Run workflow"**
4. Attendez 1-2 minutes

### 2.3 Obtenir l'URL de votre site

Votre site sera accessible à l'adresse:

```
https://nexusproject2077.github.io/nexus-hub/
```

🎉 Vous pouvez partager cette URL avec tout le monde!

---

## Étape 3: Tester le Compteur Instagram

### 3.1 Lancer le workflow de mise à jour

1. Allez dans l'onglet **"Actions"**
2. Cliquez sur **"Update Instagram Followers Count"**
3. Cliquez sur **"Run workflow"** → **"Run workflow"**
4. Attendez 2-3 minutes

### 3.2 Vérifier que ça fonctionne

1. Une fois le workflow terminé, vérifiez le fichier `followers_data.json`
2. Il devrait contenir vos vrais abonnés Instagram
3. Allez sur votre site: https://nexusproject2077.github.io/nexus-hub/
4. Le compteur devrait afficher votre nombre d'abonnés!

---

## Comment ça Fonctionne?

```
Toutes les 6 heures (automatique):
┌─────────────────────────────────────────┐
│ GitHub Actions                          │
│  ↓                                      │
│ Récupère abonnés Instagram             │
│  ↓                                      │
│ Met à jour followers_data.json          │
│  ↓                                      │
│ Commit automatique                      │
│  ↓                                      │
│ Redéploiement automatique sur Pages     │
│  ↓                                      │
│ ✅ Site mis à jour avec nouveau nombre  │
└─────────────────────────────────────────┘
```

---

## Avantages de GitHub Pages

✅ **100% GRATUIT** (pas besoin de carte bancaire)
✅ **Illimité** pour les projets publics
✅ **Rapide** (CDN mondial)
✅ **HTTPS inclus** (certificat SSL gratuit)
✅ **Déploiement automatique** à chaque commit
✅ **Aucune configuration complexe**

---

## Dépannage

### Le compteur affiche "Erreur" ou "0"

**Cause 1: Session ID invalide ou expiré**
1. Récupérez un nouveau Session ID (voir Étape 1.1)
2. Mettez à jour le secret `INSTA_SESSION_ID` dans GitHub
3. Relancez le workflow manuellement

**Cause 2: Les secrets ne sont pas configurés**
1. Vérifiez que vous avez bien ajouté `INSTA_USERNAME` et `INSTA_SESSION_ID`
2. Vérifiez qu'il n'y a pas d'espaces avant/après les valeurs
3. Relancez le workflow

**Cause 3: Le workflow n'a jamais été exécuté**
1. Allez dans l'onglet "Actions"
2. Lancez manuellement "Update Instagram Followers Count"

### Le site ne s'affiche pas

**Vérifiez que GitHub Pages est activé:**
1. Settings → Pages
2. Source doit être sur "GitHub Actions"
3. L'URL devrait apparaître en haut

**Vérifiez le déploiement:**
1. Allez dans l'onglet "Actions"
2. Vérifiez que "Deploy to GitHub Pages" est vert (succès)
3. Si rouge, cliquez dessus pour voir l'erreur

### Le compteur ne se met pas à jour automatiquement

1. Vérifiez que le workflow "Update Instagram Followers Count" s'exécute bien
2. Settings → Actions → General
3. Vérifiez que "Workflow permissions" est sur "Read and write permissions"

---

## Personnalisation

### Changer la fréquence de mise à jour

Par défaut, le compteur se met à jour toutes les 6 heures.

Pour changer:
1. Ouvrez `.github/workflows/update_followers.yml`
2. Ligne `- cron: '0 */6 * * *'`
3. Changez `*/6` pour une autre valeur:
   - `*/1` = toutes les heures
   - `*/12` = toutes les 12 heures
   - `0 8 * * *` = tous les jours à 8h

### Utiliser un domaine personnalisé

Si vous avez votre propre domaine:
1. Settings → Pages → Custom domain
2. Entrez votre domaine (ex: `nexus-hub.com`)
3. Configurez les DNS de votre domaine (instructions fournies)

---

## Maintenance

### Le Session ID expire régulièrement?

Les Session ID Instagram peuvent expirer après quelques semaines/mois. C'est normal.

**Solution rapide:**
1. Récupérez un nouveau Session ID
2. Mettez à jour le secret dans GitHub
3. Relancez le workflow

**Astuce:** Gardez une session Instagram active sur votre navigateur principal pour que le Session ID reste valide plus longtemps.

---

## Récapitulatif des URLs Importantes

- **Votre site**: https://nexusproject2077.github.io/nexus-hub/
- **Dépôt GitHub**: https://github.com/nexusproject2077/nexus-hub
- **Settings**: https://github.com/nexusproject2077/nexus-hub/settings
- **Actions**: https://github.com/nexusproject2077/nexus-hub/actions
- **Secrets**: https://github.com/nexusproject2077/nexus-hub/settings/secrets/actions

---

## Prochaines Étapes

1. ✅ Ajoutez les secrets Instagram (Étape 1)
2. ✅ Activez GitHub Pages (Étape 2)
3. ✅ Testez le compteur (Étape 3)
4. 🎉 Partagez votre site!

**Votre site sera accessible à:** https://nexusproject2077.github.io/nexus-hub/

C'est gratuit, automatique, et ça marche pour toujours! 🚀

---

## Besoin d'Aide?

Si vous rencontrez un problème:
1. Vérifiez les logs dans l'onglet "Actions"
2. Assurez-vous que les secrets sont bien configurés
3. Relisez la section "Dépannage" ci-dessus

Bon déploiement! 🎊
