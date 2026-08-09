// Enregistrement du Service Worker (PWA)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Chemin adapté pour votre sous-dossier /fils/
        navigator.serviceWorker.register('/fils/sw.js') 
            .then(reg => { console.log('Service Worker enregistré. Portée:', reg.scope); })
            .catch(err => { console.error('Échec de l\'enregistrement du Service Worker:', err); });
    });
}

// Fonction pour formater un nombre (H, M ou S) avec deux chiffres
function pad(number) { return number < 10 ? '0' + number : number; }

// Fonction pour mettre à jour l'heure
function updateTime() {
    const now = new Date();
    const hours = pad(now.getHours());
    const minutes = pad(now.getMinutes());
    const seconds = pad(now.getSeconds());
    document.getElementById('system-time').textContent = `${hours}:${minutes}:${seconds}`;
}

// Fonction utilitaire pour formater le nombre (ex: 12500 -> 12.5K)
function formatFollowers(num) {
    if (num >= 1000) {
        // La ligne toFixed(1).replace(/\.0$/, '') permet de ne pas afficher .0 (ex: 1.0K devient 1K)
        return (num / 1000).toFixed(1).replace(/\.0$/, '') + 'K';
    }
    return num.toLocaleString(); 
}

// Charge les abonnés depuis le backend Cloud Run (/api/followers).
// Si le backend est indisponible, on retombe sur le JSON statique embarqué,
// de sorte que le site reste fonctionnel même en hébergement purement statique.
async function fetchFollowersData() {
    // 1) Backend (Firebase Hosting réécrit /api/** vers Cloud Run)
    try {
        const apiResponse = await fetch('/api/followers', { cache: 'no-store' });
        if (apiResponse.ok) {
            return await apiResponse.json();
        }
    } catch (apiError) {
        console.warn('Backend indisponible, repli sur le JSON statique :', apiError);
    }

    // 2) Repli statique
    const response = await fetch('./followers_data.json');
    if (!response.ok) {
        throw new Error('Échec du chargement des données des abonnés.');
    }
    return await response.json();
}

async function loadFollowers() {
    const el = document.getElementById('follower-count');
    if (!el) return;
    try {
        const data = await fetchFollowersData();
        el.textContent = formatFollowers(data.followers);
    } catch (error) {
        console.error("Échec de la récupération des abonnés :", error);
        el.textContent = 'Erreur';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Logique de l'horloge
    updateTime();
    setInterval(updateTime, 1000);
    
    // Logique du widget d'abonnés
    loadFollowers(); 
    // Actualise l'affichage toutes les 30 minutes (0.000083333333 heures * 60 minutes * 1000 ms)
    // NOTE : Le calcul (0.000083333333 * 60 * 1000) est erroné. 30 minutes = 30 * 60 * 1000 ms.
    // L'ancienne valeur était équivalente à 0.005 secondes, ce qui n'a aucun sens. 
    // J'ai corrigé la valeur à 30 minutes (1,800,000 ms) ci-dessous.
    
    // Ancien calcul (erroné) : 0,000083333333 * 60 * 1000 = 0.005 ms (beaucoup trop rapide)
    // Nouveau calcul (30 minutes) : 30 * 60 * 1000 = 1,800,000 ms
    setInterval(loadFollowers, 1800000); 

    // Logique de recherche
    const searchInput = document.getElementById('searchInput');
    const projectCards = document.querySelectorAll('.project-card');

    searchInput.addEventListener('keyup', (e) => {
        const searchTerm = e.target.value.toLowerCase(); 

        projectCards.forEach(card => { 
            const projectTitle = card.getAttribute('data-title').toLowerCase(); 
            
            if (projectTitle.includes(searchTerm)) {
                card.classList.remove('hidden');
            } else {
                card.classList.add('hidden');
            }
        });
    });
});
