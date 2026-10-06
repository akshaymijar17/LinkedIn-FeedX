'use strict';

const keys = Object.keys(FEEDX_DEFAULTS);

chrome.storage.local.get(FEEDX_DEFAULTS, (res) => {
  for (const key of keys) {
    const checkbox = document.getElementById(key);
    checkbox.checked = res[key];
    checkbox.addEventListener('change', () => {
      chrome.storage.local.set({ [key]: checkbox.checked });
    });
  }
});
