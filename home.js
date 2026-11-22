(() => {
  const input = document.getElementById('searchInput');
  const main = document.querySelector('.hub-main');
  const services = [...main.querySelectorAll('[data-service]')];
  const groups = [...main.querySelectorAll('[data-service-group]')];
  const status = document.getElementById('search-status');
  const normalize = text => text.normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase().trim();
  const originals = services.map(service => service.textContent);

  function filter() {
    const query = normalize(input.value);
    const words = query.split(/\s+/).filter(Boolean);
    let count = 0;
    services.forEach((service, index) => {
      const searchable = normalize([originals[index], service.textContent, service.dataset.keywords].join(' '));
      service.hidden = !words.every(word => searchable.includes(word));
      if (!service.hidden) count++;
    });
    groups.forEach(group => {
      group.hidden = !group.querySelector('[data-service]:not([hidden])');
    });
    main.classList.toggle('is-searching', !!query);
    status.hidden = !query;
    const tr = document.documentElement.lang === 'tr';
    status.textContent = !query ? '' : count === 0
      ? (tr ? 'Hizmet bulunamadı.' : 'Aucun service trouvé. Essayez un autre mot.')
      : (tr ? count + ' hizmet bulundu' : count + (count === 1 ? ' service trouvé' : ' services trouvés'));
  }
  input.addEventListener('input', filter);
  window.addEventListener('nexus:locale', filter);
})();
