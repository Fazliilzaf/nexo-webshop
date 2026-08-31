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
# Prices DECIDED 2026-08-30 (SEK incl. VAT, in öre):
# +1 329 kr · +2 269 kr · +3 249 kr · Ritual bundle 729 kr
# Brush 299 kr DECIDED 2026-08-31
PRICES = {
    "lather-me-up": "32900",
    "mist-me-crazy": "26900",
    "whip-me-good": "24900",
    "the-ritual": "72900",
    "borste": "29900",
}
# Shipping weights (grams) DECIDED by owner 2026-08-31: volume-as-grams.
# Bundle = 250+100+30. Brush intentionally left EMPTY (owner decision
# 2026-08-31): flat-rate shipping means weight is unused at checkout.
# Add a value if weight-based rates or carrier label apps are introduced.
GRAMS = {
    "lather-me-up": "250",
    "mist-me-crazy": "100",
    "whip-me-good": "30",
    "the-ritual": "380",
}
# Handles whose empty grams are an accepted decision, not a blocker.
GRAMS_EMPTY_OK = {"borste"}

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


def product_row(handle, title, body, ptype, sku, barcode, price, tagline, volume,
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
        "Variant Grams": GRAMS.get(handle, ""),   # decided 2026-08-31; empty = still blocked
        "Variant Inventory Tracker": "",          # untracked — sell without stock check (decided 2026-08-31)
        "Variant Inventory Qty": "",
        "Variant Inventory Policy": "continue",   # keep selling when out of stock
        "Variant Fulfillment Service": "manual",
        "Variant Price": price,                   # decided 2026-08-30; empty = still blocked
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
            p.get("sku", ""), BARCODES.get(h, ""), PRICES[h],
            sv["tagline"], VOLUMES[h], USAGES[h],
            sv["keyIngredients"], sv["inci"],
            f'{sv["name"]} {p["step"]} | NEXO',
            sv["description"],
        ))

    bundle = CATALOG["bundle"]
    ritual_rows.append(product_row(
        bundle["handle"], bundle["sv"]["name"], bundle["sv"]["description"],
        "Ritual", "", "", PRICES["the-ritual"], "", "", "", None, None,
        f'{bundle["sv"]["name"]} | NEXO', bundle["sv"]["description"],
    ))
    write_csv(os.path.join(OUT, "products.csv"), PRODUCT_COLUMNS, ritual_rows)

    accessory_rows = [product_row(
        "borste", "NEXO Borste", "", "Tillbehör", "", "", PRICES["borste"],
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
        ("lather-me-up", "material-lather-desktop.jpg", "homepage material (desktop)", "approved", "2.png pre-cropped: lockup + product name, bottom claim sentence removed ('stimulerar hårbotten')"),
        ("lather-me-up", "material-lather-mobile.jpg", "homepage material (mobile)", "approved", "clean text-free crop of 2.png"),
        ("mist-me-crazy", "pdp-mist-1.jpg", "primary PDP image", "approved-owner-decision", "label reads 'MIST ME E CRAZY' — accepted as-is by owner 2026-08-31; re-render welcome, not required"),
        ("mist-me-crazy", "pdp-mist-2.jpg", "secondary PDP image", "approved-owner-decision", "label reads 'MIST ME E CRAZY' — accepted as-is by owner 2026-08-31; re-render welcome, not required"),
        ("mist-me-crazy", "material-mist-desktop.jpg", "homepage material (desktop)", "approved", "5.png pre-cropped: lockup + product name, bottom line removed for consistency"),
        ("mist-me-crazy", "material-mist-mobile.jpg", "homepage material (mobile)", "approved", "clean text-free crop of 3.png"),
        ("whip-me-good", "pdp-whip-1.jpg", "primary PDP image", "approved", "JAR is canonical +3 representation"),
        ("whip-me-good", "material-whip-desktop.jpg", "homepage material (desktop)", "approved", "4.png pre-cropped: lockup + product name, bottom claim removed ('stödjer läkning')"),
        ("whip-me-good", "material-whip-mobile.jpg", "homepage material (mobile)", "approved", "clean text-free crop of 4.png"),
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
