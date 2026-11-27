(() => {
  const search = document.querySelector('.nh-search input[name="q"]');
  if (!search) return;
  document.addEventListener('keydown', event => {
    const target = document.activeElement;
    const editing = target && (target.matches('input,textarea,select') || target.isContentEditable);
    if (event.key === '/' && !editing) {
      event.preventDefault();
      search.focus();
    }
    if (event.key === 'Escape' && target === search) {
      search.value = '';
      search.blur();
    }
  });
})();