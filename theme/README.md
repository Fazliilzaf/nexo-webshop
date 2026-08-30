# NEXO — Liquid Ritual (Shopify theme)

Custom Online Store 2.0 theme built from scratch: Liquid, vanilla JS, CSS.
No Dawn fork, no framework, no build step.

## Structure

```
assets/      nexo-tokens.css   design tokens (griege #A8A09D is fixed)
             nexo-base.css     reset, type voices (Buda / grotesk / mono), buttons
             nexo-glass.css    the optical glass material (nav, docks, cart, rail ONLY)
             nexo-chrome.css   header + footer
             nexo-ritual.css   homepage: ritual stage, bundle, ingredient lens
             nexo-cart.css     cart drawer
             nexo.js           shared helpers (reduced motion, lerp, rAF)
             nexo-glass.js     pointer/tilt response for glass surfaces
             nexo-ritual.js    scroll engine: +1→+2→+3, bundle convergence, lens
             nexo-cart.js      AJAX cart + ritual completion logic
             buda-light.woff2  display face (self-hosted, font-display: swap)
             nexo-logo-*.svg   the four approved wordmark variants
             material-*.jpg    art-directed material worlds (lather/mist/whip),
                               cropped from the Produktserie renders — no baked text
layout/      theme.liquid
sections/    nexo-header, ritual-experience, ritual-bundle,
             ingredient-teaser, nexo-footer
snippets/    ritual-step, cart-drawer
locales/     sv.default.json + en.json — zero hardcoded strings in Liquid/JS
templates/   index.json
config/      settings_schema.json, settings_data.json
```

## Design law (keep these when extending)

1. **Glass is reserved** for things that float above the world: header bar,
   product docks, cart drawer, ritual rail, language switch, lens. Everything
   else stays raw and flat. Never glass pills on every button.
2. **Buda Light** for names/emotion (never below ~28px) · **system grotesk**
   for commerce/UI · **mono** for +1/+2/+3, INCI, spec, micro-labels.
3. The **+1 / +2 / +3 system is the UX backbone** — ritual rail, cart
   progress, bundle convergence all speak it.
4. Reduced motion is a designed static version (`.ritual--static`), not a
   broken one. Static mode is also the no-JS default; JS upgrades.
5. Transforms + opacity only in scroll-driven motion. No per-frame layout reads.

## Known placeholders (do not ship as-is)

- Prices render as `0,00 kr` + `PRICE TBD` badge until products exist in the
  store with real prices (handles: `lather-me-up`, `mist-me-crazy`,
  `whip-me-good`, `the-ritual`).
- ADD buttons are `disabled` until those products exist.
- Footer company details are `[ORG]` tokens (see OPEN-QUESTIONS.md).
- Ingredient teaser CTA points to `/pages/ingredienser` (page not built yet).
- Legal footer links are `#` placeholders.

## Not built yet (next phases)

PDP · ingredient library page (the full lens experience) · brand story ·
journal · search · account/order history · subscriptions (selling plans) ·
cart page · legal pages · cookie consent.

## Dev preview (no Shopify required)

`preview/` contains a liquidjs-based static renderer (dev-only, not part of
the theme):

```
cd preview && npm install && node render.js        # sv
node render.js en                                   # en
python3 -m http.server 8642                         # from repo root
open http://localhost:8642/preview/index.html
```

Against a real store: `shopify theme dev` from `theme/` once the four
products exist with the agreed handles.
