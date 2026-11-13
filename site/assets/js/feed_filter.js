(function () {
  var _activeCategories = new Set();
  var _activeTags = new Set();

  function _normalize(str) {
    return (str || '').trim().toLowerCase();
  }

  function applyFeedSearchAndFilters() {
    var inputEl = document.getElementById('feed-search-input');
    var query = _normalize(inputEl ? inputEl.value : '');
    var terms = query ? query.split(/\s+/) : [];
    var cards = document.querySelectorAll('.feed-card');
    var visibleCount = 0;

    cards.forEach(function (card) {
      var kind = card.getAttribute('data-kind') || '';
      var kindMatch = _activeCategories.size === 0 || _activeCategories.has(kind);

      var cardTags = (card.getAttribute('data-tags') || '')
        .split(',')
        .map(_normalize)
        .filter(Boolean);
      var tagMatch = true;
      _activeTags.forEach(function (reqTag) {
        if (cardTags.indexOf(reqTag) === -1) {
          tagMatch = false;
        }
      });

      var corpus = _normalize(card.getAttribute('data-search'));
      var textMatch = terms.every(function (term) {
        var clean = term.replace(/^#/, '');
        return corpus.indexOf(clean) !== -1 || cardTags.indexOf(clean) !== -1;
      });

      var show = kindMatch && tagMatch && textMatch;
      card.style.display = show ? 'block' : 'none';
      if (show) {
        visibleCount++;
      }
    });

    document.querySelectorAll('.feed-filter-btn').forEach(function (btn) {
      var f = btn.getAttribute('data-filter');
      if (f === 'all') {
        btn.classList.toggle('active', _activeCategories.size === 0);
      } else {
        btn.classList.toggle('active', _activeCategories.has(f));
      }
    });

    document.querySelectorAll('.feed-tag-btn').forEach(function (tb) {
      var t = _normalize(tb.getAttribute('data-tag'));
      tb.classList.toggle('active-tag', _activeTags.has(t));
    });

    var banner = document.getElementById('feed-active-tag-banner');
    var tagLabel = document.getElementById('feed-active-tag-label');
    if (banner && tagLabel) {
      if (_activeTags.size > 0) {
        banner.style.display = 'flex';
        tagLabel.textContent = Array.from(_activeTags)
          .map(function (t) { return '#' + t; })
          .join(', ');
      } else {
        banner.style.display = 'none';
      }
    }

    var statusEl = document.getElementById('feed-count-status');
    if (statusEl) {
      statusEl.textContent = 'Showing ' + visibleCount + ' of ' + cards.length + ' posts';
    }

    var emptyEl = document.getElementById('feed-empty-notice');
    if (emptyEl) {
      emptyEl.style.display = visibleCount === 0 ? 'block' : 'none';
    }
  }

  function setFeedCategory(kind) {
    if (kind === 'all') {
      _activeCategories.clear();
    } else if (_activeCategories.has(kind)) {
      _activeCategories.delete(kind);
    } else {
      _activeCategories.add(kind);
    }
    applyFeedSearchAndFilters();
  }

  function toggleFeedTag(tag) {
    var norm = _normalize(tag);
    if (_activeTags.has(norm)) {
      _activeTags.delete(norm);
    } else {
      _activeTags.add(norm);
    }
    applyFeedSearchAndFilters();
  }

  function clearFeedTags() {
    _activeTags.clear();
    applyFeedSearchAndFilters();
  }

  function resetFeedSearchAndFilters() {
    _activeCategories.clear();
    _activeTags.clear();
    var inputEl = document.getElementById('feed-search-input');
    if (inputEl) {
      inputEl.value = '';
    }
    applyFeedSearchAndFilters();
  }

  window.applyFeedSearchAndFilters = applyFeedSearchAndFilters;
  window.setFeedCategory = setFeedCategory;
  window.filterFeedNodes = setFeedCategory;
  window.toggleFeedTag = toggleFeedTag;
  window.clearFeedTags = clearFeedTags;
  window.resetFeedSearchAndFilters = resetFeedSearchAndFilters;
})();
