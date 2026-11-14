# marshall-art-site

Static site for Marshall Art Restorations (marshallartrestorations.com — Linda J Marshall, New Gloucester, Maine). A hand-built replacement for the GoDaddy Website Builder site. Hosts free on GitHub Pages.

## Hosting

- Repo: github.com/smellyborelli/marshall-art-site, Pages from `main` at root.
- Custom domain comes from the `CNAME` file (`marshallartrestorations.com`). `www` is a DNS CNAME to `smellyborelli.github.io`.
- Cutover commit `b720baf` (2026-11-14): noindex removed from the three pages, robots.txt allows crawlers, CNAME added.
- Email lives on Microsoft 365 (MX → `*.mail.protection.outlook.com`). Keep the MX and TXT records as they are.

## Remaining cutover step

GoDaddy DNS, at the domain's DNS panel:

1. Replace both `@` A records (15.197.148.33, 3.33.130.190) with the four GitHub Pages IPs.
2. Point `www` CNAME at `smellyborelli.github.io`.

Then GitHub issues the certificate. Turn on Enforce HTTPS once the certificate is ready.

## Structure

- index.html — homepage
- gallery/index.html — before & after, 8 project pairs
- gallery-1/index.html — portfolio wall
- assets/images/ — WebP images. originals/ holds the full-resolution captures from the old GoDaddy CDN and is not tracked in git.
- assets/css/style.css — the only stylesheet. No JavaScript.
- tools/verify.py — mechanical check of the built pages (metadata bounds, alt text, links, JSON-LD, NAP, noindex absent). Run it after any edit: `python3 tools/verify.py` (needs beautifulsoup4).
