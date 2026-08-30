# OPEN QUESTIONS — must be answered before launch

Nothing in the NEXO brand folder answers these. **Do not invent values.**
Use the placeholders below, mark them visibly in the UI, and list them in your
handover notes.

## Found on the final print labels (2026-08-30, from `brand/reference/products/`) — CONFIRM

These answers appear on the final label renders, so the questions below may
already be partially answered. Confirm before treating as final.

| Question | Found on labels |
|---|---|
| #3 Volumes | **+2 Spray = 100 ml / 3.38 fl.oz** · **+3 Cream = 30 ml / 1.01 fl.oz** (+1 = 250 ml, known) |
| #4 Company details | `ne8xo.com` · `contact@ne8xo.com` · **Vasaplatsen 2, 411 34 Göteborg** (legal name/org.nr/VAT still missing) |
| #7 Domain | Labels point to **ne8xo.com**, not `nexo.se` — which is canonical? |
| — Barcodes (EAN) | +1 `7 394359 290407` · +2 `7 394359 290414` · +3 `7 394359 290421` |
| — PAO | 6M on all three; VEGAN mark printed on all labels |

⚠️ **Compliance flags found while reading the labels — DECIDED 2026-08-30:**
- **+3 contains Lanolin and Cera Alba (beeswax)** — both animal-derived, yet the
  labels carry a VEGAN mark. **Decision (blocker, compliance):** until verified,
  the site shows NO vegan mark for +3 and NO series-wide vegan claim. Ingredient
  data stays unchanged. Prefer correct over marketable. → Still open: what is
  actually true for the formula/certification?
- Label copy mentions **"efter hårtransplantation"**. **Decision:** NOT used on
  the site. No medical/treatment language until claims are legally reviewed.
  Site copy stays on cosmetic benefits from `content/products.json`.
- `serie/9.png` (Vitavele Cosmetics, other brand) is **permanently excluded**
  from frontend and art direction.
- **Domain is still open** — neither `nexo.se` nor `ne8xo.com` is treated as
  canonical in metadata until confirmed.

**Asset decisions (2026-08-30):**
- Repo (`brand/reference/products/`) is source of truth for product assets.
- `pdp/spray-1.png` + `pdp/spray-2.png` contain a render typo ("MIST ME
  ECRAZY") — **temporary/dev-only**, must be re-rendered before launch. Never
  use "ECRAZY" in storefront copy or alt text.
- **+3 cream: the JAR is the primary packaging** until confirmed otherwise.
  The pump bottle in `pdp/combo.png` is NOT a confirmed SKU — do not use it as
  +3 product imagery. → Blocker: confirm jar vs pump.
- The brush is an accessory/tool — never part of +1/+2/+3 numbering. No +4.

## Blocking (cannot launch without)

| # | Question | Placeholder to use meanwhile |
|---|---|---|
| 1 | **Prices** for +1, +2, +3 and the Ritual bundle (incl. VAT, SEK) | `0,00 kr` + a `PRICE TBD` dev-only badge |
| 2 | **Product photography** — none exists in Drive | Flat renders of the label PDFs on black. Never a stock photo. |
| 3 | **Volume** of +2 Spray and +3 Cream (only +1 is known: 250 ml) | `— ml` |
| 4 | **Company details**: legal name, org.nr, VAT nr, registered address, support email/phone | `[ORG]` tokens in the footer |
| 5 | **Shipping**: carrier, rates, free-shipping threshold, delivery time, EU/international? | Free over 500 kr, 2–4 working days |
| 6 | **Returns policy** — the brief assumes 30 days open purchase (Swedish market norm) | 30 dagars öppet köp |
| 7 | **Domain** + Shopify plan | `nexo.se` assumed |

## Important (shapes the build)

| # | Question |
|---|---------|
| 8 | Subscription: which app/native selling plans, what discount, what interval? |
| 9 | Email platform — Klaviyo, Shopify Email, something else? Affects the capture form. |
| 10 | Do you want reviews (Judge.me / Okendo)? If so, reserve the PDP slot now. |
| 11 | Cookie consent vendor (required for EU) — Cookiebot, Shopify's own, other? |
| 12 | English market: which countries ship, which currencies, or is EN just for reading? |
| 13 | Social handles + whether Instagram feed appears in the footer. |
| 14 | Journal: do you have articles, or should the section be hidden at launch? |
| 15 | Is Buda Light licensed for web embedding, or should the site load it from Google Fonts? |

## Nice to have

- Founder story / "why NEXO" — is there a written version anywhere?
- Salon or retail partners to list?
- A press or stockist page?
