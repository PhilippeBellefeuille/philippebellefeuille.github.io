// Shared by every page: follow the OS light/dark setting and handle the FR/EN/RU toggle.
// Load at the end of <body>.
//
// Language, first match wins:
//   1. ?lang=fr, ?lang=en or ?lang=ru in the URL (works on every page, good for sharing links)
//   2. the last language picked with the language buttons on this device
//   3. the browser's language: French or Russian if it starts with "fr" / "ru", English otherwise
(function () {
  var dark = window.matchMedia('(prefers-color-scheme: dark)');
  function applyMode() { document.body.classList.toggle('dark', dark.matches); document.body.classList.toggle('light', !dark.matches); }
  applyMode();
  dark.addEventListener('change', applyMode);

  var LANGS = ['fr', 'en', 'ru'];
  function valid(l) { return LANGS.indexOf(l) !== -1 ? l : null; }

  function setLang(l, fromButton) {
    document.body.dataset.lang = l;
    document.documentElement.lang = l;
    document.querySelectorAll('[data-set-lang]').forEach(function (b) {
      var on = b.dataset.setLang === l;
      b.classList.toggle('active', on);
      b.setAttribute('aria-pressed', on);
    });
    try { localStorage.setItem('lang', l); } catch (e) {}
    if (fromButton) {
      // Keep the address bar in step so a copied link opens in the language on screen.
      var url = new URL(location.href);
      url.searchParams.set('lang', l);
      history.replaceState(history.state, '', url);
    }
  }
  document.querySelectorAll('[data-set-lang]').forEach(function (b) {
    b.addEventListener('click', function () { setLang(b.dataset.setLang, true); });
  });

  // Analytics: GoatCounter (cookieless, no consent banner needed). Ignores localhost.
  // Count by path only, so ?lang=fr / ?lang=en visits add up to one page in the stats.
  window.goatcounter = { path: function () { return location.pathname; } };
  var gc = document.createElement('script');
  gc.async = true;
  gc.src = 'https://gc.zgo.at/count.js';
  gc.dataset.goatcounter = 'https://philippebellefeuille.goatcounter.com/count';
  document.head.appendChild(gc);

  var fromUrl = valid(new URLSearchParams(location.search).get('lang'));
  var saved = null;
  try { saved = valid(localStorage.getItem('lang')); } catch (e) {}
  var nav = (navigator.language || '').toLowerCase().slice(0, 2);
  var browser = valid(nav) || 'en';
  setLang(fromUrl || saved || browser, false);
})();
