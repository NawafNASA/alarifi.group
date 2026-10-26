/* alarifi.group: language (English / Arabic) and theme (auto / light / dark) */
(function () {
  var root = document.documentElement;

  function save(key, value) {
    try { localStorage.setItem(key, value); } catch (e) {}
  }

  function setLang(lang) {
    root.lang = lang;
    root.dir = lang === 'ar' ? 'rtl' : 'ltr';
    var title = root.getAttribute(lang === 'ar' ? 'data-title-ar' : 'data-title-en');
    if (title) document.title = title;
    save('lang', lang);
    if (/[?&]lang=/.test(location.search) && window.history && history.replaceState) {
      var url = location.pathname + location.search.replace(/([?&])lang=(ar|en)/, '$1lang=' + lang) + location.hash;
      history.replaceState(null, '', url);
    }
  }

  function syncTheme() {
    var current = root.getAttribute('data-theme') || 'auto';
    var buttons = document.querySelectorAll('[data-set-theme]');
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].setAttribute('aria-pressed', buttons[i].getAttribute('data-set-theme') === current ? 'true' : 'false');
    }
  }

  function setTheme(theme) {
    if (theme === 'light' || theme === 'dark') root.setAttribute('data-theme', theme);
    else root.removeAttribute('data-theme');
    save('theme', theme);
    syncTheme();
  }

  document.addEventListener('click', function (event) {
    var langButton = event.target.closest('[data-toggle-lang]');
    if (langButton) { setLang(root.lang === 'ar' ? 'en' : 'ar'); return; }
    var themeButton = event.target.closest('[data-set-theme]');
    if (themeButton) setTheme(themeButton.getAttribute('data-set-theme'));
  });

  syncTheme();
})();
