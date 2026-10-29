# alarifi.group

The website for Alarifi Group, published with GitHub Pages at https://alarifi.group.

| Path | Page |
|---|---|
| `/` | Home: a one-button handheld with the Red Dot cartridge in the slot (English, with an Arabic toggle) |
| `/reddot/` | Red Dot: Cat Laser Chase |
| `/reddot/support` | Red Dot support |
| `/reddot/privacy` | Red Dot privacy policy |
| `/ansure/` | Ansure (أنشر): app page, its cartridge sits next to the handheld on the home page |
| `/ansure/support` | Ansure support (Arabic first, English underneath) |
| `/ansure/privacy` | Ansure privacy policy (Arabic first, English underneath) |
| `/app-ads.txt` | AdMob authorized seller line |

Plain HTML, CSS and JavaScript. `tools/build.py` writes the pages: edit it, then run `python3 tools/build.py`. Each page holds both languages side by side (`data-when="en"` and `data-when="ar"`); `assets/site.js` switches between them and between the light and dark themes.

## Adding an app

1. Add an entry to `APPS` in `tools/build.py` (slug, App Store link or `None` until it is live, names, texts, facts).
2. Add its images: `assets/<slug>-art.jpg` (480 x 480, the cartridge label), `assets/<slug>-screen.jpg` (600 x 845, a real screen from the app) and `assets/<slug>-icon.jpg` (256 x 256).
3. Add its support and privacy pages, following `build_reddot_docs`.
4. Run `python3 tools/build.py`.

The first app in `APPS` sits in the handheld on the home page. Every other app waits beside it as a cartridge that links to its own page.

Fonts: Michroma and Readex Pro, self-hosted under the SIL Open Font License (`assets/OFL.txt`).

Leave `app-ads.txt` and `CNAME` as they are unless the AdMob account or the domain changes.
