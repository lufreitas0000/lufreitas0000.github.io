(function () {
  'use strict';
  var activeCategories = new Set();

  function normalize(value) {
    return (value || '').trim().toLowerCase();
  }

  function applyFeedSearchAndFilters() {
    var input = document.getElementById('feed-search-input');
    var query = normalize(input ? input.value : '');
    var terms = query ? query.split(/\s+/).map(function (term) { return term.replace(/^#/, ''); }) : [];
    var cards = document.querySelectorAll('.feed-card');
    var visibleCount = 0;

    cards.forEach(function (card) {
      var kind = card.getAttribute('data-kind') || '';
      var corpus = normalize(card.getAttribute('data-search'));
      var matched = (activeCategories.size === 0 || activeCategories.has(kind)) &&
        terms.every(function (term) { return corpus.indexOf(term) !== -1; });
      card.hidden = !matched;
      if (matched) visibleCount += 1;
    });

    document.querySelectorAll('.feed-filter-btn').forEach(function (button) {
      var kind = button.getAttribute('data-filter');
      var selected = kind === 'all' ? activeCategories.size === 0 : activeCategories.has(kind);
      button.classList.toggle('active', selected);
      button.setAttribute('aria-pressed', String(selected));
    });

    var status = document.getElementById('feed-count-status');
    if (status) status.textContent = 'Showing ' + visibleCount + ' of ' + cards.length + ' notes';
    var emptyNotice = document.getElementById('feed-empty-notice');
    if (emptyNotice) emptyNotice.hidden = visibleCount !== 0;
  }

  function setFeedCategory(kind) {
    if (kind === 'all') activeCategories.clear();
    else if (activeCategories.has(kind)) activeCategories.delete(kind);
    else activeCategories.add(kind);
    applyFeedSearchAndFilters();
  }

  function resetFeedSearchAndFilters() {
    activeCategories.clear();
    var input = document.getElementById('feed-search-input');
    if (input) input.value = '';
    applyFeedSearchAndFilters();
  }

  function initializeSearch() {
    var toggle = document.getElementById('feed-search-toggle');
    var input = document.getElementById('feed-search-input');
    if (!toggle || !input) return;

    function setExpanded(expanded) {
      input.hidden = !expanded;
      toggle.setAttribute('aria-expanded', String(expanded));
      toggle.setAttribute('aria-label', expanded ? 'Close search' : 'Search notes');
      if (expanded) input.focus();
      else {
        input.value = '';
        applyFeedSearchAndFilters();
        toggle.focus();
      }
    }

    toggle.addEventListener('click', function () { setExpanded(input.hidden); });
    input.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') setExpanded(false);
    });
    document.addEventListener('pointerdown', function (event) {
      if (!input.hidden && !input.value && !event.target.closest('.feed-search-box')) {
        setExpanded(false);
      }
    });
    applyFeedSearchAndFilters();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeSearch);
  } else {
    initializeSearch();
  }

  window.applyFeedSearchAndFilters = applyFeedSearchAndFilters;
  window.setFeedCategory = setFeedCategory;
  window.resetFeedSearchAndFilters = resetFeedSearchAndFilters;
})();
