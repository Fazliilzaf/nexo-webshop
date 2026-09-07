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
             ingredient-teaser, nexo-footer, pdp-object,
             ingredients-library, brand-story
snippets/    ritual-step, cart-drawer
locales/     sv.default.json + en.json — zero hardcoded strings in Liquid/JS
templates/   index.json, product.json, page.ingredients.json, page.brand.json
config/      settings_schema.json, settings_data.json
```

The three signature moments: **homepage = FEEL** (ritual scroll),
**PDP = BUY** (flat object, instant commerce), **Ingredients = TRUST**
(the lens). **Brand = UNDERSTAND NEXO** — the quiet counterweight:
no glass, no JS, only type, space and principles.

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

- `pdp-mist-1.dev.jpg` / `pdp-mist-2.dev.jpg` — DEV-ONLY: the spray renders
  contain the "ECRAZY" typo. Replace with re-rendered images (same filenames
  minus `.dev`) before launch. Never use "ECRAZY" in copy or alt text.
- +3 cream imagery uses the JAR only. The pump bottle in combo material is an
  unconfirmed variant — do not use (blocker in OPEN-QUESTIONS.md).

Resolved 2026-08-31: product prices live in the store (329/269/249/729 kr,
brush 299 kr), footer company details filled (Hair TP Clinic Gbg AB,
559034-2688, SE559034268801, Vasaplasten 2, 411 34 Göteborg,
contact@hairtpclinic.com), legal pages published with real content.

## Pages to create in Shopify admin

- Page handle `ingredienser` → theme template `page.ingredients`
- Page handle `om-nexo` → theme template `page.brand`
- Legal pages (default template `page`, content from `production/legal/`):
  `integritetspolicy` · `kopvillkor` · `frakt-och-leverans` ·
  `returer-och-angerratt` — published 2026-08-31; legal review still
  recommended before launch
- Blog handle `journal` (templates `blog` + `article` apply automatically)
- Products with handles above + `borste` (brush — renders via the accessory
  branch of the PDP template: no step nav, no ritual strip, no +n) and
  metafields (namespace `nexo`): `tagline`, `volume`, `usage`,
  `key_ingredients` (JSON), `inci` (JSON)
- Shop metafield `nexo.ingredient_functions` (JSON) ←
  `content/ingredient-functions.json`
- Articles: commerce appears only when
  `article.metafields.nexo.product` (product reference) is set

## Not built yet (next phases)

Search · account/order history · subscriptions (selling plans) ·
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
