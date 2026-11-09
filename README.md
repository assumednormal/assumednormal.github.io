# assumednormal.com

Static site for Max Mitchell’s data science & AI advisory practice. No build step: GitHub Pages serves the files as-is.

## Structure

| Path | Purpose |
| --- | --- |
| `index.html` | Home: hero, AI on-ramp, services, selected work |
| `services.html` | Engagement model, AI on-ramp, capabilities, who it’s for |
| `about.html` | Bio, career timeline, approach |
| `contact.html` | Contact details and next steps |
| `404.html` | Not-found page (uses root-absolute links) |
| `css/theme.css` | **Brand theme**: colors, type, labels, lists, tables. Shared by site and documents |
| `css/style.css` | Website layout (imports `theme.css`) |
| `css/document.css` | Print/PDF layout for client documents (imports `theme.css`) |
| `templates/document.html` | Client document template: letterhead, title block, sections, fee table, signatures |
| `assets/` | Portrait and favicon / logo mark |

## Brand

- **Typeface:** IBM Plex Mono (Google Fonts), weights 400 / 500 / 600. Fallback: system monospace.
- **Palette:** monochrome only.
  - Ink `#0a0a0a` for text and solid fills
  - Secondary text `#3d3d3d`, muted `#6b6b6b`
  - Rules `#d9d9d9`, panels `#f4f4f4`, paper `#ffffff`
- **Mark:** a single bell-curve stroke (`assets/favicon.svg`; inline SVG in headers).
- **Patterns:** small uppercase tracked labels (`.label`), hairline rules instead of boxes or shadows, square bullets (`ul.dash`), numbered sections (`01`, `02`…), no rounded corners.

## Client documents

1. Copy `templates/document.html` (keep it next to `css/` so the stylesheet resolves).
2. Replace the content. Reuse the blocks: `.callout`, `ul.dash`, `table.data`, `.doc-steps`, `.doc-sign`.
3. Open it in a browser → **Print → Save as PDF** (Letter, background graphics on).

For Word or Google Docs: set the font to IBM Plex Mono, use black/gray text only, uppercase 7–8pt gray labels, and thin gray rules under headings.
