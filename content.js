'use strict';

// Hiding is done by toggling classes on <html>; content.css does the rest.
// Classes (unlike removing nodes) can be undone, so changes in the popup
// apply immediately without a page refresh.
const root = document.documentElement;
let settings = { ...FEEDX_DEFAULTS };

function isFeedPage() {
  return location.pathname === '/feed' || location.pathname.startsWith('/feed/');
}

function apply() {
  const onFeed = isFeedPage();
  root.classList.toggle('feedx-hide-feed', onFeed && settings.hideFeed);
  root.classList.toggle('feedx-hide-news', settings.hideNews);
}

chrome.storage.local.get(FEEDX_DEFAULTS, (res) => {
  settings = res;
  apply();
});

chrome.storage.onChanged.addListener((changes, area) => {
  if (area !== 'local') return;
  for (const [key, { newValue }] of Object.entries(changes)) {
    if (key in FEEDX_DEFAULTS) settings[key] = newValue;
  }
  apply();
});

// LinkedIn is a single-page app, so navigating to and from /feed doesn't
// reload the page. Re-check the URL whenever the DOM changes.
let lastPath = location.pathname;
new MutationObserver(() => {
  if (location.pathname !== lastPath) {
    lastPath = location.pathname;
    apply();
  }
}).observe(root, { childList: true, subtree: true });
