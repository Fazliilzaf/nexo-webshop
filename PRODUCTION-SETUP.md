# NEXO — Production setup checklist

Deterministisk checklista för att sätta upp Shopify-butiken. Temat läser
ALLT produktinnehåll från dessa källor — preview-data i `preview/render.js`
är dev-only och får aldrig bli production source of truth.

Design freeze gäller från `cd30408`: inga nya visuella features före launch.

---

## 1. Metafields — exakt mapping

### Produkt-metafields (namespace `nexo`), per produkt

| Key | Typ | Källa | Läses av |
|---|---|---|---|
| `nexo.tagline` | single_line_text | `content/products.json` → `sv.tagline` (+ EN) | PDP, ritual |
| `nexo.volume` | single_line_text | `sv.volume` ("250 ml" / "100 ml" / "30 ml") | PDP, ritual |
| `nexo.usage` | multi_line_text | `pdp.usage.*` i locales (härstammar från tryckta etiketter) | PDP |
| `nexo.key_ingredients` | json | `sv.keyIngredients` (`[{name, benefit}]`) | PDP |
| `nexo.inci` | json | `sv.inci` (`[[name, explanation]]`) | PDP + Ingredients-sidan |

Volymerna är verifierade mot tryckta etiketter (+1 250 ml · +2 100 ml ·
+3 30 ml). INCI ändras ALDRIG för att passa claims — flagga konflikt istället.

### Shop-metafield

| Key | Typ | Källa |
|---|---|---|
| `nexo.ingredient_functions` | json | `content/ingredient-functions.json` (hela `functions`-objektet) |

### Article-metafield (valfri, per artikel)

| Key | Typ | Effekt |
|---|---|---|
| `nexo.product` | product reference | Visar den diskreta produkt-fotnoten i artikeln |

## 2. Produkter

| Handle | Roll | Notering |
|---|---|---|
| `lather-me-up` | +1 | SKU NEXO-SH-250, EAN 7 394359 290407 |
| `mist-me-crazy` | +2 | EAN 7 394359 290414 |
| `whip-me-good` | +3 | EAN 7 394359 290421. **Burk** som produktbild (pump = obekräftad) |
| `the-ritual` | bundle | Hero-erbjudandet |
| `borste` | accessory | INGEN +4. Renderas via PDP:ns accessory-branch |

Produktbilder laddas upp som riktiga product images (ersätter tema-fallbacks).
+2:s nuvarande renders (`pdp-mist-*.dev.jpg`) är **dev-only** ("ECRAZY").

## 3. Sidor, blogg, navigation

- Sida `ingredienser` → template `page.ingredients`
- Sida `om-nexo` → template `page.brand`
- Blogg `journal` (templates `blog`/`article` automatiskt)
- Menyer: Ritualen `/#ritual` · Ingredienser `/pages/ingredienser` ·
  Journal `/blogs/journal` · Om NEXO `/pages/om-nexo`
- Legala sidor (mall `page` räcker): integritetspolicy, köpvillkor,
  frakt & leverans, returer — länkas i footern

## 4. HARD BLOCKERS (ingen placeholder får passera)

**COMMERCIAL:** priser +1/+2/+3 · bundle-pris · shipping (carrier, rates,
tröskel) · returns-policy
**COMPANY:** org.nr · VAT · registrerad adress · support email/telefon
**BRAND/PRODUCT:** canonical domain (nexo.se vs ne8xo.com — ej gissad) ·
vegan vs lanolin/bivax (+3) · +3 burk vs pump · +2-renders utan "ECRAZY"
**SHOPIFY:** store access · produkter · metafields · pages · blogg · navigation
**LEGAL:** privacy · terms · returns · shipping · cookie consent

### Domain-sweep (körs när canonical är beslutad)

canonical URLs · sitemap/robots · Open Graph · JSON-LD (Organization/
Product) · footer-kontakt · mailto-länkar · etikett/sajt-konsekvens.

### Claims freeze

Inga claims om hårväxt, läkning, post-transplant eller vegan utan godkänt
underlag. Konflikter flaggas i `OPEN-QUESTIONS.md`, inte löses i copy.

## 5. Production QA (riktiga butiken, inte preview)

Hela kedjan på mobil + desktop:
Home → PDP +1/+2/+3 → Ingredients → Brand → Journal → Brush → Cart → Checkout.

Verifiera: Lighthouse (≥90 perf, 100 a11y), `/cart/*`-endpoints, structured
data (Product/Offer/Article/Organization), navigation, checkout (Klarna/
Swish/kort), hreflang SV/EN, cookie consent.

## 6. Definition of done

- 0 kritiska accessibility-issues
- 0 placeholder production-copy
- 0 dev-only-bilder i storefront
- 0 olösta representationskonflikter (burk/pump, ECRAZY)
- 0 claims utan underlag
- 0 döda navigeringslänkar
- 0 kända commerce-blockers
- Riktiga Shopify-flödet QA:at end-to-end
