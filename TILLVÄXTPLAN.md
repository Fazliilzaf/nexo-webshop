# NEXO — Tillväxtplan (roadmap)

Skapad efter lansering av ne8xo.com. Prioritet: punkt 2 (klinikkanalen) är den strategiska hävstången — den bär och betalar för resten.

Regel som gäller allt nedan: claims-frysen. Inga medicinska påståenden (läker, påskyndar återhämtning, tar bort rodnad, hårväxt). Positioneringen är "skapad för eftervård efter hårtransplantation" — rutin, inte effekt.

Status 2026-09-01: genomarbetad autonomt. ⏳ = väntar på Fazli (paketet ligger klart).

---

## 1. Äg kategorin — Journal som sökvapen

Mål: NEXO ska vara det självklara svaret på "eftervård hårtransplantation".

- [x] Kartlägg sökord (klinikerna äger generella eftervårds-termerna; NEXO:s vinkel är rutin och produktsidan)
- [x] Skriv artikelserie i Journal:
  - [x] Eftervården vecka för vecka (stomartikeln) — live: /blogs/journal/eftervarden-vecka-for-vecka
  - [x] De första sju dagarna — live
  - [x] När kan jag tvätta håret igen? — live
  - [x] Sömn, träning och vardag — live
  - [x] Svullnad och lymfmassage — live
  - [x] När håret känns strävt — live
- [x] Alla artiklar med meta title/description, humaniserad ton, länkar till ritualstegen
- [x] Article-schema (fanns redan i journal-article.liquid)
- [ ] ⏳ EN-versioner (kräver locales/translation-scope i API-token eller Translate & Adapt manuellt)

## 2. Klinikkanalen — clinic kit-programmet ⭐ (högsta prioritet)

- [x] Clinic kit-förslag med prismodell: production/klinikkit/clinic-kit-forslag.md
- [x] Eftervårdsguiden (tryckt folder-text): production/klinikkit/eftervardsguide.md
- [x] Pitchmail + kliniklista (9 SE + Norden): production/klinikkit/pitchmail.md
- [ ] ⏳ Fazli pratar med Hair TP Clinic om kit i eftervårdspåsen
- [ ] ⏳ Fazli beslutar grossistpriser (förslag: 50 % till Hair TP, 40 % till nya kliniker)
- [ ] ⏳ Skicka pitchmailet till kliniklistan
- [ ] ⏳ Tryck eftervårdsguiden

## 3. Prenumeration

- [x] Appval: Appstle (gratisplan) — production/prenumeration/appval.md
- [x] Appstle installerad i admin
- [x] Plan skapad: "Ritualen var 8:e vecka, 15 %" kopplad till Ritualen +1 +2 +3
- [ ] ⏳ Tema-widget: kräver manuell integration i vår custom-PDP (pdp-object.liquid) så den inte kolliderar med köpknappen + designmatchning
- [ ] ⏳ Testprenumeration (efter widgeten är live)
- [ ] ⏳ Fazli bekräftar 15 % / 8 veckor / fraktvillkor

## 4. Patientberättelser — inte modeller

- [x] Samtyckesmall (GDPR, återkallbar): production/patientberattelser/samtycke.md
- [x] Intervjufrågor + redaktionella regler + publiceringsformat (samma fil)
- [ ] ⏳ Fazli frågar 3–5 klinikkunder om deltagande
- [ ] ⏳ Kundernas svar redigeras (Kimi) → godkänns av kunden → publiceras

## 5. Borsten som andra dörr

- [x] Borst-PDP med dubbla vinklar (eftervård + ansikte/vardag), live på /products/borste
- [x] Journalartikel: "Så använder du lymfmassageborsten." — live: /blogs/journal/sa-anvander-du-lymfmassageborsten
- [ ] ⏳ Socialt innehållsspår för borsten (morgonrutin, inte transplantat) — när sociala kanaler startar

## 6. Sajten som PR

- [x] Skärmdumpar av hela flödet: production/awards/screens/ (8 st)
- [x] Konceptbeskrivning EN + credits: production/awards/submission-texts.md
- [ ] ⏳ Awwwards — konto + avgift (~$95), Fazli betalar
- [ ] ⏳ CSSDA — konto + ev. avgift, e-postverifiering till info@fazli.se
- [ ] ⏳ FWA — gratis, men e-postverifiering krävs
- [ ] ⏳ Vid nominering: pressutskick + journalinlägg

---

## Bonus-fixar gjorda under arbetet

- pH "translation missing"-bugg på mist/whip-PDP:erna (case-känslig guard) — fixad och live
- Tankstreck städade ur brand-texter (SV+EN) enligt stilregeln

## Ordning och beroenden (oförändrad rekommendation)

1. Klinikkit (2) — Fazlis relation till kliniken är nyckeln
2. Journalserie (1) — publicerad, börjar ranka över tid
3. Designinskick (6) — allt förberett, bara konto/avgift kvar
4. Prenumeration (3) — app + plan klara, widget-integration kvar
5. Patientberättelser (4) — mallar klara, samtal kvar
6. Borstspår (5) — PDP + artikel klara
