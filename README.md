# NEXO — webshop project kit

Everything Kimi (or any other build agent) needs to build the NEXO storefront,
in one repository. Extracted from Google Drive › NEXO on 2026-08-30.

## Hur du använder det här

1. Ge Kimi hela repot (`git clone`, eller ladda upp mappen).
2. Klistra in innehållet i **`PROMPT-KIMI.md`** som första meddelande.
3. Kimi läser resten själv.

Prompten är skriven på engelska med flit — modeller följer briefer märkbart
bättre på engelska. Allt *innehåll* som hamnar på sajten (produkttexter,
UI-strängar) är svenskt och engelskt i `content/`.

Briefen låser varumärket och målen, men inte utseendet. Kimi ombeds komma
tillbaka med två–tre olika kreativa riktningar innan den skriver kod — du
väljer, sedan bygger den.

## Innehåll

```
PROMPT-KIMI.md            Byggbriefen. Detta är prompten.
OPEN-QUESTIONS.md         15 saker som saknas — priser, bilder, org.nr m.m.
brand/
  tokens/brand-facts.json De få saker som är låsta: färg, ordmärke, +1/+2/+3
  logo/svg/               Ordmärket i svart, vitt, griege och currentColor
  fonts/Buda-Light.*      Displaytypsnittet (woff2 + ttf)
  reference/              Tryckta etiketter + officiella färgprovet +
                          products/ (label- och serierenderingar per produkt)
content/
  products.json           Alla tre produkter: copy, nyckelingredienser, full INCI (SV + EN)
theme/                    Temat "NEXO — Liquid Ritual" (Shopify OS 2.0, från grunden)
preview/                  Dev-only statisk rendering för visuell QA utan Shopify
```

## Varumärket i korthet

| | |
|---|---|
| Låst | Ordmärket · `#A8A09D` · produktnamnen · +1/+2/+3 · produkttexterna |
| Fritt | Layout, palett runt griege, typografi, rörelse, bildspråk, struktur |
| Produkter | +1 Lather Me Up (schampo) · +2 Mist Me Crazy (spray) · +3 Whip Me Good (kräm) |
| Ursprung | Made in Sweden · Vegan |

## Teknisk grund

Shopify Online Store 2.0, eget tema från grunden (Liquid + vanilla JS + CSS).
Shopify sköter betalning (Klarna/Swish/kort), moms, frakt och lager — Kimi
bygger presentationen. Kvalitetskraven är hårda (WCAG 2.2 AA, Lighthouse ≥ 90
mobil) men de säger ingenting om hur sajten ska se ut.

## Nästa steg för dig, Fazli

1. Svara på det som är blockerande i `OPEN-QUESTIONS.md` (framför allt priser
   och produktbilder — utan dem kan sajten inte gå live).
2. Skapa Shopify-butiken och lägg upp de tre produkterna med handles
   `lather-me-up`, `mist-me-crazy`, `whip-me-good` + `the-ritual`.
3. Kör `shopify theme dev` mot butiken när Kimi levererat temat.
