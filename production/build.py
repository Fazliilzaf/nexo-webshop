#!/usr/bin/env python3
"""Build NEXO production import files from locked source data.

Reads:  content/products.json, content/ingredient-functions.json
Writes: production/import/products.csv          (Matrixify, ritual + bundle)
        production/import/products-accessory.csv (Matrixify, brush)
        production/import/shop-metafields.csv    (Matrixify, shop level)
        production/asset-manifest.csv

Rules: only verified source values are written. Anything unverified
(price, bundle price, inventory, weight) stays EMPTY. Stdlib only.
"""
import csv
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "production", "import")
os.makedirs(OUT, exist_ok=True)

with open(os.path.join(ROOT, "content", "products.json"), encoding="utf-8") as f:
    CATALOG = json.load(f)
with open(os.path.join(ROOT, "content", "ingredient-functions.json"), encoding="utf-8") as f:
    FUNCTIONS = json.load(f)["functions"]

VOLUMES = {"lather-me-up": "250 ml", "mist-me-crazy": "100 ml", "whip-me-good": "30 ml"}
USAGES = {
    "lather-me-up": "Massera försiktigt in i fuktigt hår och hårbotten tills det bildas ett mjukt lödder. Skölj noggrant. Upprepa vid behov.",
    "mist-me-crazy": "Spraya jämnt från cirka 10–15 cm avstånd. Låt torka eller massera försiktigt in. Använd i fuktigt eller torrt hår, när som helst på dagen.",
    "whip-me-good": "Använd dagligen vid behov. Arbeta in en liten mängd i hårbotten eller på torr hud.",
}
BARCODES = {
    "lather-me-up": "7394359290407",
    "mist-me-crazy": "7394359290414",
    "whip-me-good": "7394359290421",
}

PRODUCT_COLUMNS = [
    "Handle", "Title", "Body (HTML)", "Vendor", "Type", "Tags", "Published",
    "Option1 Name", "Option1 Value",
    "Variant SKU", "Variant Grams", "Variant Inventory Tracker",
    "Variant Inventory Qty", "Variant Inventory Policy",
    "Variant Fulfillment Service", "Variant Price", "Variant Barcode",
    "Variant Requires Shipping", "Variant Taxable",
    "SEO Title", "SEO Description", "Status",
    "Metafield: nexo.tagline [single_line_text_field]",
    "Metafield: nexo.volume [single_line_text_field]",
    "Metafield: nexo.usage [multi_line_text_field]",
    "Metafield: nexo.key_ingredients [json]",
    "Metafield: nexo.inci [json]",
]


def product_row(handle, title, body, ptype, sku, barcode, tagline, volume,
                usage, key_ingredients, inci, seo_title, seo_desc):
    return {
        "Handle": handle,
        "Title": title,
        "Body (HTML)": f"<p>{body}</p>" if body else "",
        "Vendor": "NEXO",
        "Type": ptype,
        "Tags": "",
        "Published": "FALSE",
        "Option1 Name": "Title",
        "Option1 Value": "Default Title",
        "Variant SKU": sku,
        "Variant Grams": "",                      # BLOCKED: unverified
        "Variant Inventory Tracker": "shopify",
        "Variant Inventory Qty": "",              # BLOCKED: unverified
        "Variant Inventory Policy": "deny",
        "Variant Fulfillment Service": "manual",
        "Variant Price": "",                      # BLOCKED: hard blocker
        "Variant Barcode": barcode,
        "Variant Requires Shipping": "TRUE",
        "Variant Taxable": "TRUE",                # verify with accountant
        "SEO Title": seo_title,
        "SEO Description": seo_desc[:320],
        "Status": "DRAFT",
        "Metafield: nexo.tagline [single_line_text_field]": tagline,
        "Metafield: nexo.volume [single_line_text_field]": volume,
        "Metafield: nexo.usage [multi_line_text_field]": usage,
        "Metafield: nexo.key_ingredients [json]": json.dumps(key_ingredients, ensure_ascii=False) if key_ingredients else "",
        "Metafield: nexo.inci [json]": json.dumps(inci, ensure_ascii=False) if inci else "",
    }


def write_csv(path, columns, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columns)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print("wrote", os.path.relpath(path, ROOT))


def main():
    ritual_rows = []
    for p in CATALOG["products"]:
        h = p["handle"]
        sv = p["sv"]
        ritual_rows.append(product_row(
            h, sv["name"], sv["description"], sv["category"],
            p.get("sku", ""), BARCODES.get(h, ""),
            sv["tagline"], VOLUMES[h], USAGES[h],
            sv["keyIngredients"], sv["inci"],
            f'{sv["name"]} {p["step"]} | NEXO',
            sv["description"],
        ))

    bundle = CATALOG["bundle"]
    ritual_rows.append(product_row(
        bundle["handle"], bundle["sv"]["name"], bundle["sv"]["description"],
        "Ritual", "", "", "", "", "", None, None,
        f'{bundle["sv"]["name"]} | NEXO', bundle["sv"]["description"],
    ))
    write_csv(os.path.join(OUT, "products.csv"), PRODUCT_COLUMNS, ritual_rows)

    accessory_rows = [product_row(
        "borste", "NEXO Borste", "", "Tillbehör", "", "",
        "", "", "", None, None, "NEXO Borste | NEXO", "",
    )]
    write_csv(os.path.join(OUT, "products-accessory.csv"), PRODUCT_COLUMNS, accessory_rows)

    shop_rows = [{
        "Name": "NEXO",
        "Metafield: nexo.ingredient_functions [json]": json.dumps(FUNCTIONS, ensure_ascii=False),
    }]
    write_csv(os.path.join(OUT, "shop-metafields.csv"),
              ["Name", "Metafield: nexo.ingredient_functions [json]"], shop_rows)

    manifest_rows = [
        # handle, asset, role, production_status, note
        ("lather-me-up", "pdp-lather-1.jpg", "primary PDP image", "approved", "bottle on stone, correct +1 lockup"),
        ("lather-me-up", "pdp-lather-2.jpg", "secondary PDP image", "approved", "lather texture on bottle"),
        ("lather-me-up", "material-lather.jpg", "homepage material", "approved", "cropped silk, no baked text"),
        ("mist-me-crazy", "pdp-mist-1.dev.jpg", "primary PDP image", "DEV-ONLY-REPLACE-BEFORE-LAUNCH", "render typo 'ECRAZY'"),
        ("mist-me-crazy", "pdp-mist-2.dev.jpg", "secondary PDP image", "DEV-ONLY-REPLACE-BEFORE-LAUNCH", "render typo 'ECRAZY'"),
        ("mist-me-crazy", "material-mist.jpg", "homepage material", "approved", "cropped silk, no baked text"),
        ("whip-me-good", "pdp-whip-1.jpg", "primary PDP image", "approved", "JAR is canonical +3 representation"),
        ("whip-me-good", "material-whip.jpg", "homepage material", "approved", "cropped silk, no baked text"),
        ("whip-me-good", "ritual-combo.jpg", "unused", "excluded-unconfirmed-pump", "contains unconfirmed cream pump bottle — never as +3 imagery"),
        ("the-ritual", "ritual-group.jpg", "bundle background", "approved", "pump shampoo + spray + jar, candle"),
        ("borste", "pdp-brush.jpg", "primary PDP image", "approved-accessory", "render on stone, plain wordmark"),
        ("borste", "pdp-brush-photo.jpg", "secondary PDP image", "approved-accessory", "real product photo IMG_3136"),
        ("brand", "nexo-logo-black.svg", "wordmark", "approved", "supplied variant"),
        ("brand", "nexo-logo-white.svg", "wordmark", "approved", "supplied variant"),
        ("brand", "nexo-logo-griege.svg", "wordmark", "approved", "supplied variant"),
        ("brand", "nexo-logo-current.svg", "wordmark", "approved", "supplied variant"),
        ("brand", "buda-light.woff2", "display font", "approved", "self-hosted"),
    ]
    manifest_path = os.path.join(ROOT, "production", "asset-manifest.csv")
    with open(manifest_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["handle", "asset", "role", "production_status", "note"])
        w.writerows(manifest_rows)
    print("wrote", os.path.relpath(manifest_path, ROOT))


if __name__ == "__main__":
    sys.exit(main())
