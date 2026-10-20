// Shared by every page: follow the OS light/dark setting and handle the FR/EN toggle.
// Load at the end of <body>.
(function () {
  var dark = window.matchMedia('(prefers-color-scheme: dark)');
  function applyMode() { document.body.classList.toggle('dark', dark.matches); document.body.classList.toggle('light', !dark.matches); }
  applyMode();
  dark.addEventListener('change', applyMode);

  function setLang(l) {
    document.body.dataset.lang = l;
    document.documentElement.lang = l;
    document.querySelectorAll('[data-set-lang]').forEach(function (b) {
      var on = b.dataset.setLang === l;
      b.classList.toggle('active', on);
      b.setAttribute('aria-pressed', on);
    });
    try { localStorage.setItem('lang', l); } catch (e) {}
  }
  document.querySelectorAll('[data-set-lang]').forEach(function (b) {
    b.addEventListener('click', function () { setLang(b.dataset.setLang); });
  });
  var saved = null;
  try { saved = localStorage.getItem('lang'); } catch (e) {}
  setLang(saved === 'en' ? 'en' : 'fr');
})();
