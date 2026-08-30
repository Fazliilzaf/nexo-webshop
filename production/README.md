# NEXO — production import layer

Lokalt förberedd importstruktur. **Ingen Shopify-app eller access krävs ännu.**
Flödet när access finns: `configure → import → connect → production QA → launch`.

## Filer

```
production/
  metafield-definitions.json   exakta definitioner att skapa i Shopify först
  build.py                     genererar import-filerna från låsta källor
  validate.py                  pre-import validation (stdlib, exit 1 vid FAIL)
  asset-manifest.csv           handle → asset → role → production status
  import/
    products.csv               +1/+2/+3 + the-ritual (Matrixify-format, DRAFT)
    products-accessory.csv     borste (separat, accessory)
    shop-metafields.csv        nexo.ingredient_functions (JSON)
```

## Importordning (när store/access finns)

1. **Metafield definitions** — skapa exakt enligt `metafield-definitions.json`
   (produkt: tagline/volume/usage/key_ingredients/inci · shop:
   ingredient_functions · article: product). Rätt typer: `json` för
   key_ingredients/inci/functions, `product_reference` för article.
2. **Validera** — `python3 production/validate.py` måste ge PASS.
3. **Produkter** — importera `import/products.csv` (status DRAFT,
   Published FALSE). Sedan `import/products-accessory.csv`.
4. **Shop-metafield** — `import/shop-metafields.csv`
   (eller sätt via Admin API/manuellt — välj renaste vägen då).
5. **Sidor** — `ingredienser` (template `page.ingredients`),
   `om-nexo` (template `page.brand`). Blogg `journal`.
6. **Bilder** — ladda upp produktbilder enligt `asset-manifest.csv`.
   `DEV-ONLY-REPLACE-BEFORE-LAUNCH` får ALDRIG upp i storefront.
   +3 = burk. `ritual-combo.jpg` (pump) är exkluderad.
7. **Navigation** — Ritualen `/#ritual` · Ingredienser
   `/pages/ingredienser` · Journal `/blogs/journal` · Om NEXO `/pages/om-nexo`.
8. **Blockers** — fyll aldrig pris/inventory/vikt förrän hard blockers i
   `PRODUCTION-SETUP.md` är besvarade. Tomma fält är avsikten.
9. **Production QA** — hela kedjan på riktiga butiken (mobil + desktop),
   se PRODUCTION-SETUP.md §5–6.

## Regenerera

`python3 production/build.py && python3 production/validate.py`

Validatorn stoppar: saknade handles/volymer, fel INCI-format, dubbletter,
funktion utan INCI-match (och tvärtom), +4, dev-assets, ECRAZY, pump för +3,
förbjudna claims (vegan/hårväxt/läkning/transplant/healing/cruelty) i
importdata. Negativtestad (injicerad claim fångas med exakt fält).

## Noteringar

- `Variant Taxable: TRUE` är standardantagandet för fysiska varor i Sverige —
  verifiera med bokföring.
- Matrixify-kolumnformatet är förberett men ingen app är vald; samma CSV:er
  kan mappas mot Admin API om vi väljer det istället.
- `Image Src` lämnas tom med avsikt — bilder kopplas via asset-manifestet,
  inte via påhittade URL:er.
