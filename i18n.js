/*
 * Localization is deliberately client-side: the page can paint immediately in
 * French, then switch only when the visitor's public IP resolves to Turkey.
 * Country detection is presentation-only; it must never be used for access
 * control or other security decisions.
 */
(function () {
  'use strict';

  const TURKISH = {
    'abonnés': 'takipçi', 'Core Stable': 'Çekirdek kararlı',
    'Neural Assistant': 'Yapay zeka asistanı', 'Precision V4': 'Hassasiyet V4',
    'Accéder': 'Eriş', 'Assistant Neural': 'Yapay zeka asistanı',
    'Calculateur': 'Hesap makinesi', 'Traduisez des textes complets en un instant.': 'Tüm metinleri anında çevirin.',
    'Envoi sécurisé et gratuit de gros fichiers': 'Büyük dosyaları güvenli ve ücretsiz gönderin',
    'Près de Chez Vous. Dès ce soir, Chattez & Rencontrez-vous.': 'Yakınınızda. Bu akşam sohbet edin ve tanışın.',
    'Boutique en ligne': 'Çevrim içi mağaza', 'Ressources': 'Kaynaklar',
    'Terminal d’accès': 'Erişim terminali', 'Sélectionnez un répertoire.': 'Bir dizin seçin.',
    'Répertoire 01': 'Dizin 01', 'Répertoire 02': 'Dizin 02', 'Répertoire 03': 'Dizin 03',
    'Projets': 'Projeler', 'Compétences': 'Beceriler', 'Missions & CV': 'Deneyimler ve özgeçmiş',
    'Analyse des modules et réalisations - code source, études de cas.': 'Modüllerin ve çalışmaların analizi - kaynak kod, vaka çalışmaları.',
    'Matrice des langages et protocoles maîtrisés - stacks, frameworks.': 'Hakim olunan diller ve protokoller matrisi - teknolojiler, çerçeveler.',
    'Journal de bord des expériences professionnelles et téléchargement du CV.': 'Mesleki deneyim günlüğü ve özgeçmiş indirme.',
    'Retour au hub': 'Hub’a dön', "Retour à l'archive": 'Arşive dön',
    'Pensées & Explorations': 'Düşünceler ve keşifler', 'Exploration': 'Keşif',
    'Article - 2025': 'Makale - 2025', 'Compétences techniques': 'Teknik beceriler',
    'Je maîtrise plusieurs technologies pour créer des projets complets de A à Z :': 'Uçtan uca projeler oluşturmak için birçok teknolojiye hakimim:',
    'Front-end :': 'Ön yüz:', 'Back-end :': 'Arka yüz:', 'Bases de données :': 'Veritabanları:', 'Gestion de projet :': 'Proje yönetimi:',
    'Plusieurs projets qui montrent l’étendue de mes compétences :': 'Becerilerimin kapsamını gösteren çeşitli projeler:',
    'Architecture, sécurité, UX/UI, optimisation et déploiement.': 'Mimari, güvenlik, UX/UI, optimizasyon ve dağıtım.',
    'Mon approche': 'Yaklaşımım', 'je gère': 'yönetiyorum',
    'Mon objectif ? Continuer à progresser, apprendre de nouvelles technologies et créer des projets qui ont un impact réel.': 'Hedefim mi? Gelişmeye devam etmek, yeni teknolojiler öğrenmek ve gerçek etkisi olan projeler oluşturmak.',
    'Modules actifs et expérimentaux.': 'Etkin ve deneysel modüller.', 'Tout': 'Tümü', 'En dev': 'Geliştirmede',
    'Aucun projet trouvé': 'Proje bulunamadı', 'Matrice des langages et protocoles maîtrisés.': 'Hakim olunan diller ve protokoller matrisi.',
    'Réseau social complet - authentification, messagerie temps réel, commentaires, gamification. Optimisé mobile & desktop.': 'Eksiksiz sosyal ağ - kimlik doğrulama, gerçek zamanlı mesajlaşma, yorumlar ve oyunlaştırma. Mobil ve masaüstü için optimize edilmiştir.',
    "Assistant IA intégré à l'écosystème Nexus. Interface conversationnelle, réponses contextuelles et suggestions intelligentes.": 'Nexus ekosistemine entegre yapay zeka asistanı. Konuşma arayüzü, bağlamsal yanıtlar ve akıllı öneriler.',
    'Calculatrice & convertisseur de précision. Interface claire, historique des calculs, raccourcis clavier.': 'Hassas hesap makinesi ve dönüştürücü. Açık arayüz, hesap geçmişi ve klavye kısayolları.',
    'Ce portail - hub personnel centralisant tous les modules Nexus. Particles canvas, cursor custom, design minimal dark.': 'Tüm Nexus modüllerini merkezileştiren kişisel portal. Parçacık kanvası, özel imleç, minimal koyu tasarım.',
    'Application caméra web interactive avec filtres temps réel, capture photo et effets visuels. En cours de développement.': 'Gerçek zamanlı filtreler, fotoğraf çekimi ve görsel efektlerle etkileşimli web kamerası uygulaması. Geliştirme aşamasında.',
    'Avancé': 'İleri', 'Intermédiaire': 'Orta', 'Basique+': 'Temel+', 'Basique': 'Temel', 'Notions': 'Temel bilgi',
    'Compétences humaines': 'Kişisel beceriler', 'Résolution de problèmes': 'Problem çözme', 'Travail d’équipe': 'Ekip çalışması',
    'Apprentissage rapide': 'Hızlı öğrenme', 'Rigueur': 'Titizlik', 'Gestion de projet': 'Proje yönetimi',
    'Développeur Web Full-Stack · Chef de projet': 'Full-Stack web geliştiricisi · Proje yöneticisi',
    'Troyes, France': 'Troyes, Fransa', 'Télécharger CV': 'Özgeçmişi indir', 'Imprimer': 'Yazdır',
    'Formation': 'Eğitim', 'En cours': 'Devam ediyor', 'Obtenu': 'Alındı',
    'Autodidacte - Développement web': 'Kendi kendine öğrenen - Web geliştirme', '2020 - présent · 6 ans': '2020 - günümüz · 6 yıl',
    'Projets notables': 'Öne çıkan projeler', 'Voir tous les projets': 'Tüm projeleri gör',
    'Stack technique': 'Teknik teknoloji seti', 'Voir le détail des compétences': 'Becerilerin ayrıntılarını gör',
    'Live': 'Canlı', 'Archive': 'Arşiv', 'Expert': 'Uzman', 'Blog': 'Blog', 'Communication': 'İletişim',
    "BUT MMI - Métiers du Multimédia et de l'Internet": 'BUT MMI - Multimedya ve internet meslekleri',
    'Développement web, UX/UI, gestion de projet, audiovisuel. Chef de projet SAE 105-106 (équipe de 4 - diagrammes Gantt, gestion des risques).': 'Web geliştirme, UX/UI, proje yönetimi, görsel-işitsel çalışmalar. SAE 105-106 proje yöneticisi (4 kişilik ekip - Gantt şemaları, risk yönetimi).',
    'HTML, CSS, JS, PHP, MySQL, MongoDB, Python - apprentissage en continu sur projets personnels.': 'HTML, CSS, JS, PHP, MySQL, MongoDB, Python - kişisel projelerde sürekli öğrenme.',
    "Assistant IA intégré à l'écosystème Nexus. Interface conversationnelle et réponses contextuelles.": 'Nexus ekosistemine entegre yapay zeka asistanı. Konuşma arayüzü ve bağlamsal yanıtlar.',
    'Calculatrice & convertisseur de précision avec historique des calculs et raccourcis clavier.': 'Hesap geçmişi ve klavye kısayollarıyla hassas hesap makinesi ve dönüştürücü.'
  };

  const TITLES = {
    'NEXUS HUB | Archive': 'NEXUS HUB | Arşiv',
    'NEXUS HUB | Blog': 'NEXUS HUB | Blog',
    'NEXUS HUB | Projets': 'NEXUS HUB | Projeler',
    'NEXUS HUB | Compétences': 'NEXUS HUB | Beceriler',
    'NEXUS HUB | CV': 'NEXUS HUB | Özgeçmiş'
  };

  function normalized(value) { return value.replace(/\s+/g, ' ').trim(); }
  function translateNode(node) {
    const original = normalized(node.nodeValue);
    const translated = TURKISH[original];
    if (!translated) return;
    const leading = (node.nodeValue.match(/^\s*/) || [''])[0];
    const trailing = (node.nodeValue.match(/\s*$/) || [''])[0];
    node.nodeValue = leading + translated + trailing;
  }
  function translateDocument() {
    document.documentElement.lang = 'tr';
    document.documentElement.dataset.locale = 'tr';
    if (TITLES[document.title]) document.title = TITLES[document.title];
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(translateNode);
    document.querySelectorAll('[placeholder]').forEach(el => {
      if (el.placeholder === 'Rechercher un service. (ou /)') el.placeholder = 'Bir hizmet ara. (veya /)';
    });
  }

  function fetchWithTimeout(url) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 1500);
    return fetch(url, { signal: controller.signal, cache: 'no-store' })
      .then(response => response.ok ? response.json() : Promise.reject(new Error('Country lookup failed')))
      .finally(() => clearTimeout(timer));
  }
  function detectCountry() {
    // The providers see the visitor's public IP themselves; no IP is stored by this site.
    return fetchWithTimeout('https://ipwho.is/')
      .then(data => data.country_code)
      .catch(() => fetchWithTimeout('https://ipapi.co/json/').then(data => data.country_code));
  }
  function start() {
    // The observer also covers footer/ticker HTML injected after initial paint.
    const observer = new MutationObserver(records => {
      if (document.documentElement.lang !== 'tr') return;
      records.forEach(record => record.addedNodes.forEach(node => {
        if (node.nodeType === Node.TEXT_NODE) translateNode(node);
        else if (node.nodeType === Node.ELEMENT_NODE) translateDocument();
      }));
    });
    observer.observe(document.body, { childList: true, subtree: true });
    detectCountry().then(code => {
      if (String(code).toUpperCase() === 'TR') {
        translateDocument();
        window.dispatchEvent(new CustomEvent('nexus:locale', { detail: { locale: 'tr' } }));
      }
    }).catch(() => { /* French remains the safe, deterministic fallback. */ });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, { once: true });
  else start();
}());
