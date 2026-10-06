# LinkedIn-FeedX

A Chrome extension that hides the LinkedIn feed and LinkedIn News, so you can use LinkedIn (messages, jobs, profiles, search) without the scroll.

It's a rebuild of [darrentu/LinkedIn-Feed-Blocker](https://github.com/darrentu/LinkedIn-Feed-Blocker), which is no longer on the Chrome Web Store.

## Features

- **Hide feed:** hides the main feed column on `linkedin.com/feed`.
- **Hide LinkedIn News:** hides the LinkedIn News sidebar module.

Both are on by default and can be toggled from the toolbar popup.

### Changes from the original

- Toggles apply instantly; no page refresh needed.
- Elements are hidden with CSS instead of being removed, so turning a toggle off brings them back.
- Handles LinkedIn's in-app navigation: moving between the feed and other pages without a reload applies the right state.
- "Hide LinkedIn News" defaults to on (in the original it was shown checked but wasn't actually enabled until toggled).
- No Bulma dependency; the popup is plain HTML/CSS with dark mode support.

## Install (unpacked)

1. Clone this repository.
2. Open `chrome://extensions` and enable **Developer mode**.
3. Click **Load unpacked** and select the repository folder.

## Project layout

| File | Purpose |
| --- | --- |
| `manifest.json` | Manifest V3 definition |
| `settings.js` | Default settings, shared by the content script and popup |
| `content.js` | Runs on linkedin.com; toggles `feedx-*` classes on `<html>` based on settings and the current URL |
| `content.css` | The selectors that actually hide things |
| `popup.html` / `popup.js` / `popup.css` | Toolbar popup with the toggles |
| `scripts/make_icons.py` | Regenerates `icons/` (standard library only) |

## When it stops working

LinkedIn changes its markup regularly. If something stops being hidden, update the selectors in `content.css`.

## Privacy

No data leaves your browser. The only thing stored is your toggle settings, in `chrome.storage.local`.

Not affiliated with LinkedIn.

## License

MIT. See [LICENSE](LICENSE). Based on work © 2024 Darren Tu.
