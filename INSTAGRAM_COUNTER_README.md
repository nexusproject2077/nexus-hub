# Compteur Instagram - Mode d'Emploi

## 🎯 Comment Ça Fonctionne

Le compteur d'abonnés Instagram utilise un **système hybride intelligent**:

### 1. Tentative Automatique (Toutes les 6h)
Le workflow GitHub Actions essaie automatiquement de récupérer vos abonnés via les APIs Instagram.

### 2. Fallback Manuel (Si les APIs échouent)
Si Instagram bloque les APIs (ce qui arrive souvent), le script utilise le fichier `manual_followers_count.txt`.

---

## 📝 Mise à Jour Manuelle (Simple!)

### Méthode 1: Éditer le Fichier Directement

1. Ouvrez le fichier `manual_followers_count.txt`
2. Remplacez le nombre par votre nombre actuel d'abonnés
3. Sauvegardez et commitez

**Exemple:**
```bash
echo "1567" > manual_followers_count.txt
git add manual_followers_count.txt
git commit -m "update: Mise à jour compteur Instagram"
git push
```

### Méthode 2: Via GitHub Web

1. Allez sur https://github.com/nexusproject2077/nexus-hub
2. Cliquez sur `manual_followers_count.txt`
3. Cliquez sur l'icône ✏️ (Edit)
4. Changez le nombre
5. Cliquez "Commit changes"

---

## 🔄 Fréquence de Mise à Jour

**Recommandation:** Mettez à jour une fois par semaine ou par mois, c'est largement suffisant!

Le nombre n'a pas besoin d'être exact à 100% - c'est juste pour montrer votre présence Instagram.

---

## ⚙️ Fonctionnement Technique

### Priorités du Script:

1. **Si `manual_followers_count.txt` existe** → Utilise ce nombre (priorité absolue)
2. **Sinon:** Essaie les APIs Instagram automatiquement
3. **Si les APIs échouent:** Garde l'ancien nombre en mémoire

### Fichiers Importants:

- `manual_followers_count.txt` - Votre nombre manuel (À ÉDITER)
- `fetch_followers.py` - Script de récupération
- `followers_data.json` - Données utilisées par le site web
- `.github/workflows/update_followers.yml` - Automatisation (toutes les 6h)

---

## 🚀 Déploiement Automatique

1. Vous modifiez `manual_followers_count.txt`
2. Vous commitez et pushez
3. Le workflow se lance automatiquement
4. Netlify redéploie votre site
5. Le nouveau nombre s'affiche! ✅

**Temps total:** 2-3 minutes

---

## ❓ FAQ

### Pourquoi le système automatique ne fonctionne pas toujours?

Instagram a renforcé la sécurité en 2024/2025 et bloque activement le scraping. Même avec un Session ID valide, les APIs sont souvent bloquées.

### Est-ce que je dois mettre le nombre exact?

Non! Un nombre approximatif suffit. C'est juste pour montrer que vous êtes actif sur Instagram.

### À quelle fréquence dois-je le mettre à jour?

Une fois par semaine/mois est largement suffisant. Ou même juste quand vous atteignez un jalon (1000, 2000, 5000, etc.).

### Puis-je désactiver les tentatives automatiques?

Oui, mais ce n'est pas nécessaire. Les tentatives automatiques ne coûtent rien et pourraient fonctionner un jour si Instagram change ses règles.

---

## 🎨 Personnalisation

### Changer la Fréquence des Tentatives Automatiques

Éditez `.github/workflows/update_followers.yml`, ligne 6:

```yaml
- cron: '0 */6 * * *'  # Toutes les 6 heures
```

Exemples:
- `*/12` = Toutes les 12 heures
- `0 9 * * *` = Tous les jours à 9h
- `0 9 * * 1` = Tous les lundis à 9h

---

## ✅ Checklist Rapide

- [ ] Le fichier `manual_followers_count.txt` existe
- [ ] Il contient un nombre valide (ex: 1234)
- [ ] Le workflow GitHub Actions s'exécute (vérifiez l'onglet Actions)
- [ ] Netlify redéploie automatiquement
- [ ] Le compteur s'affiche sur votre site

---

## 🆘 Besoin d'Aide?

Si le compteur ne s'affiche pas:

1. Vérifiez que `manual_followers_count.txt` contient un nombre
2. Vérifiez que `followers_data.json` a été mis à jour
3. Attendez 2-3 minutes que Netlify redéploie
4. Videz le cache de votre navigateur (Ctrl+F5)

---

**C'est tout! Le système est conçu pour être simple et fiable.** 🎉
