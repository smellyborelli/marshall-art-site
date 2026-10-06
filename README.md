# marshall-art-site

Static site for Marshall Art Restorations (marshallartrestorations.com — Linda J Marshall, New Gloucester, Maine). A hand-built replacement for the GoDaddy Website Builder site. Hosts free on GitHub Pages behind Cloudflare.

## Preview mode

This build is a preview. Every page carries `<meta name="robots" content="noindex">` and `robots.txt` disallows all crawlers, so it can sit next to the live GoDaddy site without competing in search.

## Cutover checklist (one commit)

1. Remove `<meta name="robots" content="noindex">` from index.html, gallery/index.html, and gallery-1/index.html.
2. Replace robots.txt with the allow version noted inside it.
3. Add a CNAME file that contains the line: marshallartrestorations.com
4. Push. Then point Cloudflare DNS at GitHub Pages (see the project migration plan).

## Structure

- index.html — homepage
- gallery/index.html — before & after, 8 project pairs
- gallery-1/index.html — portfolio wall
- assets/images/ — WebP images. originals/ holds the full-resolution captures from the old GoDaddy CDN and is not tracked in git.
- assets/css/style.css — the only stylesheet. No JavaScript.
- tools/verify.py — mechanical check of the built pages (metadata bounds, alt text, links, JSON-LD, NAP). Run it after any edit: `python3 tools/verify.py` (needs beautifulsoup4).
