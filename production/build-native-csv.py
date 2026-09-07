#!/usr/bin/env python3
"""Build a Shopify NATIVE product-import CSV (admin → Products → Import).

Native import has no metafield columns — this carries the product shells
(title, body, vendor, type, SKU, barcode, price, SEO). Metafields are set
separately (documented in production/README.md).

Same verified values as build.py. Empty stays empty. Stdlib only.
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

VOLUMES = {"lather-me-up": "250 ml", "mist-me-crazy": "100 ml", "whip-me-good": "30 ml"}
BARCODES = {"lather-me-up": "7394359290407", "mist-me-crazy": "7394359290414", "whip-me-good": "7394359290421"}
PRICES = {"lather-me-up": "329.00", "mist-me-crazy": "269.00", "whip-me-good": "249.00", "the-ritual": "729.00"}

COLUMNS = [
    "Handle", "Title", "Body (HTML)", "Vendor", "Type", "Tags", "Published",
    "Option1 Name", "Option1 Value",
    "Variant SKU", "Variant Grams", "Variant Inventory Tracker",
    "Variant Inventory Qty", "Variant Inventory Policy",
    "Variant Fulfillment Service", "Variant Price", "Variant Compare At Price",
    "Variant Requires Shipping", "Variant Taxable", "Variant Barcode",
    "Image Src", "Image Position", "Image Alt Text",
    "SEO Title", "SEO Description", "Status",
]


def row(handle, title, body, ptype, sku, barcode, price, seo_title, seo_desc):
    return {
        "Handle": handle, "Title": title,
        "Body (HTML)": f"<p>{body}</p>" if body else "",
        "Vendor": "NEXO", "Type": ptype, "Tags": "", "Published": "FALSE",
        "Option1 Name": "Title", "Option1 Value": "Default Title",
        "Variant SKU": sku, "Variant Grams": "",
        "Variant Inventory Tracker": "shopify", "Variant Inventory Qty": "",
        "Variant Inventory Policy": "deny", "Variant Fulfillment Service": "manual",
        "Variant Price": price, "Variant Compare At Price": "",
        "Variant Requires Shipping": "TRUE", "Variant Taxable": "TRUE",
        "Variant Barcode": barcode,
        "Image Src": "", "Image Position": "", "Image Alt Text": "",
        "SEO Title": seo_title, "SEO Description": seo_desc[:320],
        "Status": "DRAFT",
    }


def main():
    rows = []
    for p in CATALOG["products"]:
        h, sv = p["handle"], p["sv"]
        rows.append(row(h, sv["name"], sv["description"], sv["category"],
                        p.get("sku", ""), BARCODES[h], PRICES[h],
                        f'{sv["name"]} {p["step"]} | NEXO', sv["description"]))
    b = CATALOG["bundle"]
    rows.append(row(b["handle"], b["sv"]["name"], b["sv"]["description"], "Ritual",
                    "", "", PRICES["the-ritual"], f'{b["sv"]["name"]} | NEXO', b["sv"]["description"]))
    rows.append(row("borste", "NEXO Borste", "", "Tillbehör", "", "", "",
                    "NEXO Borste | NEXO", ""))

    path = os.path.join(OUT, "products-native.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    print("wrote", os.path.relpath(path, ROOT), f"({len(rows)} products)")


if __name__ == "__main__":
    sys.exit(main())
