# Prenumeration — appval och upplägg

## Rekommendation: Appstle Subscriptions (gratis nivå)

| App | Gratisplan | Betalt fr.o.m. | Passar NEXO? |
|---|---|---|---|
| **Appstle** | Ja, till 500 USD/mån i prenumerationsintäkt (2 % avgift) | 29 USD/mån | Ja. Snabb uppsättning (2–4 h), 5.0 i betyg, modern kundportal |
| Seal Subscriptions | Ja, begränsad | ~5 USD/mån | Bra budgetval, svagare portal |
| Recharge | Ja (1 % avgift) | 499 USD/mån | Nej. Byggd för enterprise, överdriven kostnad för vår fas |

Appstle väljs: gratis tills prenumerationerna passerar ca 5 000 kr/mån, lätt att växa i, svensktalande kunder klarar portalen (engelska/svenska stöds).

## Upplägg (beslut underlag för Fazli)

- **Vad:** Ritualen (+1+2+3) som prenumeration. Enskilda produkter kan läggas till senare.
- **Intervall:** var 8:e vecka som standard. Ritualen räcker ungefär så länge vid daglig användning. Kunden kan byta till 6 eller 12 veckor.
- **Rabatt:** 15 % mot engångspriset (729 kr → ca 620 kr). Fazli beslutar slutgiltigt.
- **Bindning:** ingen. Pausa, hoppa över eller avsluta när som helst i kundportalen.
- **Frakt:** samma som ordinarie (65 kr), alternativt fri frakt på prenumeration som extra morot.

## Texter (claims-säkra)

**Knapp:** Prenumerera och spara 15 %
**Under rubrik:** Ritualen, var 8:e vecka. Pausa eller avsluta när du vill.
**Brödtext:** Eftervård är en daglig rutin. Med prenumeration kommer ritualen hem till dig i rätt takt, utan att du behöver tänka på det. Byt intervall, hoppa över en leverans eller avsluta när som helst i din kundportal.

**Varför prenumerera (tre punkter):**
1. Ritualen hemma innan den tar slut
2. 15 % lägre pris, varje gång
3. Ingen bindningstid

## Teknisk implementering (efter installation)

1. Installera Appstle från Shopify App Store (gratis nivå)
2. Skapa prenumerationsplan: "Ritualen var 8:e vecka, 15 %"
3. Koppla planen till produkten Ritualen +1 +2 +3 (the-ritual)
4. Aktivera widget på produktsidan (Appstles tema-integration)
5. Testflöde: lägg testprenumeration i Shopifys testläge eller med riktigt kort som sedan avbryts
6. Verifiera: renewal-order skapas, kundportal fungerar, mail ser rätt ut

## Status (2026-09-01)

- [x] Appstle Subscriptions installerad i admin (gratisplan, kvot $0/$500 per månad)
- [x] Prenumerationsplan skapad: "Ritualen var 8:e vecka, 15%" kopplad till produkten Ritualen +1 +2 +3 (pay as you go, auto-renew, 15 % från första ordern)
- [ ] KVAR: tema-embed i live-temat. Skippad medvetet. Vår PDP är helt custom (pdp-object.liquid med egen add-to-cart), så Appstles widget måste placeras och designmatchas manuellt, annars riskerar den att kollidera med köpknappen. Kräver arbete i tema-editorn + test.
- [ ] KVAR: testprenumeration för att verifiera renewal-flödet (görs efter widgeten är live)

## Flagga

Appinstallation och eventuell betalplan kräver Fazlis godkännande i admin om Shopify ber om det.
