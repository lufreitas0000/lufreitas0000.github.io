(function () {
  'use strict';

  function initializeNavigation() {
    var nav = document.getElementById('floating-navigation');
    var toggle = document.getElementById('quick-menu-toggle');
    var panel = document.getElementById('quick-menu-panel');
    var topButton = document.getElementById('back-to-top');
    if (!nav || !toggle || !panel || !topButton) return;

    function closeMenu(restoreFocus) {
      panel.hidden = true;
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Open navigation menu');
      if (restoreFocus) toggle.focus();
    }
    function updateVisibility() {
      var mobile = window.matchMedia('(max-width: 720px)').matches;
      nav.hidden = !mobile && window.scrollY < 240;
      topButton.hidden = window.scrollY < 450;
      if (nav.hidden) closeMenu(false);
    }

    toggle.addEventListener('click', function () {
      var open = panel.hidden;
      panel.hidden = !open;
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close navigation menu' : 'Open navigation menu');
      if (open) {
        var firstLink = panel.querySelector('a');
        if (firstLink) firstLink.focus();
      }
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && !panel.hidden) closeMenu(true);
    });
    document.addEventListener('pointerdown', function (event) {
      if (!panel.hidden && !nav.contains(event.target)) closeMenu(false);
    });
    topButton.addEventListener('click', function () {
      var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      window.scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' });
    });
    window.addEventListener('scroll', updateVisibility, { passive: true });
    window.addEventListener('resize', updateVisibility);
    updateVisibility();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeNavigation);
  } else {
    initializeNavigation();
  }
})();
