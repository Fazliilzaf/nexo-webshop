# Cookie consent + legal — beslut och implementation

## Cookie consent: beslutsmodell

**Baseline: Shopify Customer Privacy, korrekt konfigurerat från start.**
Shopify har egna customer-privacy-inställningar och cookie-banner för
EEA/UK som hanterar samtycke för Shopifys egna funktioner. Det är vår
utgångspunkt — inte en betald CMP.

**När externa trackers/apps införs** (t.ex. marketing- eller
analytics-integrationer): verifiera att varje integration respekterar
Shopifys consent-signal (Customer Privacy API). Om vår faktiska
production-stack kräver en separat CMP väljer vi då — kandidater:
Cookiebot (Usercentrics) eller Pandectes GDPR Compliance. Valet fattas
mot den stack vi faktiskt kör, inte i förväg.

**Google Consent Mode v2** är relevant först när vi faktiskt använder
Google-taggar (t.ex. Google Ads/GA4) som kräver det — inte automatiskt
för att trafiken kommer via Instagram.

**Oföränderlig arkitekturregel:** inget nytt marketing-/analytics-script
läggs till utan (a) klassificering i rätt consent-kategori och
(b) gate:ad laddning tills samtycke finns. `layout/theme.liquid` är den
enda inkopplingspunkten.

### Consent-kategorier att konfigurera

| Kategori | Innehåll | Default |
|---|---|---|
| Nödvändiga | Shopify-session, cart, valuta, språk, säkerhet | alltid på |
| Preferenser | tema-val (språk etc.) | av |
| Statistik | GA4/Shopify analytics om/när aktiverat | av |
| Marknadsföring | externa trackers om/när de införs | av |

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

## Legal-texter

**Status: DRAFT — LEGAL REVIEW REQUIRED** på samtliga fyra. Granskning
krävs särskilt kring: GDPR retention periods · hygienundantaget ·
30 dagars frivilligt öppet köp kontra lagstadgad ångerrätt ·
betalningsmetoder · shipping/returns · vilka personuppgiftsbiträden/
mottagare som faktiskt används. Production-versionen måste matcha den
verkliga Shopify/payment/shipping-stack vi slutligen väljer:
**configuration first → legal text reflects reality second.** Betal- och
fraktmetoder listas aldrig i publicerad text förrän de är aktiverade.

Fyra utkast i denna mapp, svenska (legal språk för svensk e-handel).
EN-versioner översätts i connect-fasen från samma struktur.
`[ORG]`-token kvar tills företagsdata finns — **sidorna publiceras inte
förrän alla token är ersatta.**

- `integritetspolicy.md` — GDPR: register, ändamål, lagringstider,
  mottagare (token-baserade tills stacken är låst), rättigheter, cookies.
- `kopvillkor.md` — avtal, priser inkl. 25 % moms, betalning
  ([BETALNINGSMETODER]-token tills aktiverat), leverans, tvist via ARN.
  (ODR-referensen borttagen — plattformen nedlagd 2025-07-20.)
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
