# Cookie consent + legal — beslut och implementation

## Cookie consent: rekommendation

**Val: Cookiebot (Usercentrics) eller Pandectes GDPR Compliance.**
- Cookiebot — mest etablerad i Sverige/EU, full **Google Consent Mode v2**,
  Shopify-app, automatisk cookie-scanning. Dyrast men säkrast.
- Pandectes — Shopify-native, billigare, Consent Mode v2, bra för en
  tre-SKU-butik.
- Shopifys inbyggda banner räcker **inte** för EU-kraven när ni ska köra
  Meta/Instagram-trafik (som planen säger).

Välj Cookiebot om budget tillåter, annars Pandectes. Båda kräver:
banner före scripts laddas, blockering av icke-nödvändiga cookies tills
samtycke, samtyckeslogg, möjlighet att ändra/dra tillbaka samtycke.

### Consent-kategorier att konfigurera

| Kategori | Innehåll | Default |
|---|---|---|
| Nödvändiga | Shopify-session, cart, valuta, språk, säkerhet | alltid på |
| Preferenser | tema-val (språk etc.) | av |
| Statistik | GA4/Shopify analytics om/när aktiverat | av |
| Marknadsföring | Meta Pixel/Conversions API, Klaviyo-spårning | av |

### Cookie-inventarie i nuläget (vår storefront)

Temat laddar **noll tredjeparts-trackers**. Alla scripts är förstaparts
(`nexo-*.js`) utan tracking, inga fonts/iframes från tredje part
(Buda Light self-hostas). Cookies som sätts är Shopifys egna nödvändiga:

| Cookie | Syfte | Kategori |
|---|---|---|
| `cart` / `cart_sig` / `cart_ts` | varukorg | nödvändig |
| `_secure_session_id` | session | nödvändig |
| `cart_currency` | valuta | nödvändig |
| `localization` | språk/marknad | nödvändig |
| `keep_alive` | session-hälsa | nödvändig |
| `_shopify_y` / `_shopify_s` | Shopify-intern analytics | statistik (kräver samtycke beroende på CMP-tolkning) |

Nyhetsbrevsformuläret är Shopify-native — inga extra cookies.

**Regel framåt:** inget nytt script (Meta Pixel, Klaviyo, Judge.me,
analys) läggs till utan att det (a) hamnar i rätt consent-kategori och
(b) laddas först efter samtycke. Temats `layout/theme.liquid` är den
enda punkten där detta kopplas in.

## Legal-texter

Fyra utkast i `production/legal/`, svenska (legal språk för svensk
e-handel). EN-versioner översätts i connect-fasen från samma struktur.
`[ORG]`-token kvar tills företagsdata finns — **sidorna publiceras inte
förrän alla token är ersatta.**

- `integritetspolicy.md` — GDPR: register, ändamål, lagringstider,
  mottagare (Shopify, betalnings-/fraktpartners), rättigheter, cookies.
- `kopvillkor.md` — avtal, priser inkl. 25 % moms, betalning
  (Klarna/Swish/kort), leverans, ångerrätt kopplad till retursidan.
- `frakt-och-leverans.md` — beslutad baseline: fri frakt ≥500 kr,
  2–4 arbetsdagar, kostnad under tröskeln anges i kassan.
- `returer-och-angerratt.md` — 30 dagars öppet köp + lagens 14 dagar;
  hygienundantaget för bruten försegling (2 kap. 11 § distansavtalslagen)
  — viktigt för kosmetika, skrivet in korrekt.

## Implementation i temat

- `templates/page.json` + `sections/main-page.liquid` — default-sidmall
  (editorial kolumn, samma typografi som Journal).
- Footer-länkar → `/pages/integritetspolicy` · `/pages/kopvillkor` ·
  `/pages/frakt-och-leverans` · `/pages/returer-och-angerratt`
  (döda tills sidorna skapats i admin — listat i README).
