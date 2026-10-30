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
- **Domain confirmed:** canonical = `ne8xo.com` (renewed 2026-08-30,
  verified live). See domain decision below.

**Asset decisions (2026-08-30):**
- Repo (`brand/reference/products/`) is source of truth for product assets.
- `pdp/spray-1.png` + `pdp/spray-2.png` contain a render typo ("MIST ME
  ECRAZY") — **temporary/dev-only**, re-render ordered with correct "MIST ME
  CRAZY". Never use "ECRAZY" in storefront copy or alt text.
- **+3 cream: JAR confirmed as canonical packaging** (2026-08-30). The pump
  bottle in `pdp/combo.png` is not a SKU — never use it as +3 imagery.
- The brush is an accessory/tool — never part of +1/+2/+3 numbering. No +4.

**Commercial decisions (2026-08-30):**
- **Prices DECIDED (SEK incl. VAT):** +1 = 329 kr · +2 = 269 kr · +3 = 249 kr
  · Ritual bundle = 729 kr. Wired into `production/build.py`.
- **Shipping/returns baseline approved:** Postnord/Instabox/Budbee · free
  shipping ≥500 kr · 2–4 working days · returfrist 14 dagar
  (see owner decision 2026-10-30 below).
- **Shopify:** no account yet — owner creates (Basic plan suffices) and adds
  collaborator access. Then: configure → import → connect → verify → QA.

**Vegan claim PAUSED (2026-08-30):** the VEGAN mark is removed from all
data surfaces until the factory's written current INCI spec + rationale
for +3 exists (INCI objectively contains Lanolin, Lanolin Alcohol, Cera
Alba — no test makes those vegan; the mark came from the factory's
testing). `claims` is now `["Cruelty free"]` (factory-stated) in
`content/products.json` and `brand/tokens/brand-facts.json`, annotated.
The site renders no claims regardless. Two outcomes when the document
arrives: (a) formula changed → update INCI from the factory spec;
(b) claim wrong → de-claim permanent (remove mark from future
prints/stickers).

**Domain (2026-08-30):** `ne8xo.com` RENEWED — verified live
(`status: ok`, Loopia NS). **Canonical domain confirmed: ne8xo.com**
(printed on all physical labels). nexo.se is held by a third party (for
sale) — optional later redirect. Domain sweep at connect-phase:
canonical URLs, sitemap/robots, OG, JSON-LD, footer
(contact@ne8xo.com now wired), mailto, label/site consistency.

**No subscriptions for now (2026-10-30, owner decision "det ska jag inte som det ser ut just nu"):**
NEXO does not sell subscriptions or other purchase options at this time. Verified
on the live store: all five products return zero `selling_plan_groups`, so no
customer can buy one. Consequence: Shopify's "Avbokningspolicy for kopalternativ",
which the admin labels Obligatorisk, is NOT required — that label comes from the
Appstle Subscription app being installed, not from Swedish law and not from any
active purchase option. It blocks nothing and the store can launch without it.
Appstle is on a free tier (no app charges on the billing invoices). Left installed;
uninstalling it removes the label, and that is the owner's call. If subscriptions
are introduced later, the interval, discount and cancellation terms are owner
decisions and the policy must be written from them, never invented.

**Return window = 14 days (2026-10-30, owner decision "14"):** the voluntary
30-day open-purchase promise is dropped. The return window is the statutory
14-day right of withdrawal under distansavtalslagen, which matches the 14-day
rule already configured in Shopify. The hygiene-seal exception
(2 kap. 11 § distansavtalslagen) is unchanged. Replaced in:
`production/legal/returer-och-angerratt.md`, `production/legal/kopvillkor.md`,
`production/legal/README.md`, `theme/locales/sv.default.json`,
`theme/locales/en.json`, and the footer badge of all 11 `preview/*.html`.
Also republished in Shopify: the pages Returer & ångerrätt and Köpvillkor,
and the Retur- och återbetalningspolicy.

**Contact routing (2026-10-30, owner decision):** all order notifications and
all customer inquiries are to be DELIVERED to `marknad@hairtpclinic.com`.
Neither setting lives in this repo:

1. Shopify admin → Settings → Notifications → recipient for new orders =
   `marknad@hairtpclinic.com`. Sender/reply-to stays on the `ne8xo.com` domain
   for deliverability — only the recipient changes.
2. Mail routing: `contact@hairtpclinic.com` forwards to
   `marknad@hairtpclinic.com` (Microsoft 365 admin).

**Published address CHANGED (2026-10-30, owner decision "byt allt"):** every
customer-facing contact address in this repo is now `marknad@hairtpclinic.com`.
Replaced in:
- `theme/locales/sv.default.json` + `theme/locales/en.json` (`footer.email`)
- `theme/README.md`
- all four legal documents under `production/legal/` (kopvillkor,
  integritetspolicy, returer-och-angerratt, frakt-och-leverans) and their README
- `production/patientberattelser/samtycke.md` (was `info@ne8xo.com`, an address
  used nowhere else)
- the eight footer mock-ups under `preview/` (were `contact@ne8xo.com`)

**Deliberately NOT changed — say so if this should change too:**
- `production/sources/hair-tp-eftervardsguide.md` — a source record of Hair TP
  Clinic's own aftercare guide. Its footer is the clinic's real contact line,
  not NEXO's. Rewriting a source document would corrupt the record.
- `info@fazli.se` in `production/awards/submission-texts.md` and
  `TILLVÄXTPLAN.md` — those are notes about which mailbox verifies award-site
  account registrations, not an order or inquiry address.
- The **printed labels** carry `contact@ne8xo.com`. Physical print cannot be
  changed retroactively, so `contact@ne8xo.com` must keep resolving — point it
  at `marknad@hairtpclinic.com` by forwarding, or mail sent from a bottle in a
  customer's hand goes nowhere.

**Legal note:** the four documents under `production/legal/` are published
pages. After merge they have to be re-published in Shopify for the new address
to take effect for customers — the repo change alone does not update a live page.

## Blocking (cannot launch without)

| # | Question | Placeholder to use meanwhile |
|---|---|---|
| 1 | **Prices** for +1, +2, +3 and the Ritual bundle (incl. VAT, SEK) | `0,00 kr` + a `PRICE TBD` dev-only badge |
| 2 | **Product photography** — none exists in Drive | Flat renders of the label PDFs on black. Never a stock photo. |
| 3 | **Volume** of +2 Spray and +3 Cream (only +1 is known: 250 ml) | `— ml` |
| 4 | **Company details**: legal name, org.nr, VAT nr, registered address, support email/phone | `[ORG]` tokens in the footer |
| 5 | **Shipping**: carrier, rates, free-shipping threshold, delivery time, EU/international? | Free over 500 kr, 2–4 working days |
| 6 | ~~**Returns policy**~~ — DECIDED 2026-10-30: 14 dagar | 14 dagars ångerrätt |
| 7 | **Domain** + Shopify plan | `nexo.se` assumed |

## Important (shapes the build)

| # | Question |
|---|---------|
| 8 | ~~Subscription~~ — DECIDED 2026-10-30: no subscriptions for now (see owner decision below) |
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
