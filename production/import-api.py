#!/usr/bin/env python3
"""NEXO product import via Shopify Admin REST API.

Creates the five products (3 ritual + bundle + brush) with variants,
decided prices, EAN barcodes and the nexo.* metafields, plus the
shop-level nexo.ingredient_functions metafield. Idempotent: products
that already exist (by handle) are skipped, not duplicated.

Token: production/.secrets/admin-api-token (gitignored). Stdlib only.

Usage: python3 production/import-api.py [--dry-run]
"""
import json
import os
import sys
import urllib.request
import urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOP = "wju0k3-q1.myshopify.com"
API = f"https://{SHOP}/admin/api/2026-07"
DRY = "--dry-run" in sys.argv

sys.path.insert(0, os.path.join(ROOT, "production"))
from build import VOLUMES, USAGES, BARCODES, PRICES  # noqa: E402

with open(os.path.join(ROOT, "content", "products.json"), encoding="utf-8") as f:
    CATALOG = json.load(f)
with open(os.path.join(ROOT, "content", "ingredient-functions.json"), encoding="utf-8") as f:
    FUNCTIONS = json.load(f)["functions"]
with open(os.path.join(ROOT, "production", ".secrets", "admin-api-token"), encoding="utf-8") as f:
    TOKEN = f.read().strip()


def call(method, path, payload=None):
    url = f"{API}{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("X-Shopify-Access-Token", TOKEN)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            body = r.read().decode()
            return r.status, json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:400]}


def money(ore_str):
    return f"{int(ore_str) / 100:.2f}"


def mf(key, value, mtype):
    return {"namespace": "nexo", "key": key, "value": value, "type": mtype}


def product_payload(handle, title, body, ptype, sku, barcode, price, metafields, seo_title, seo_desc):
    return {
        "product": {
            "title": title,
            "handle": handle,
            "body_html": f"<p>{body}</p>" if body else "",
            "vendor": "NEXO",
            "product_type": ptype,
            "status": "draft",
            "options": [{"name": "Title", "values": ["Default Title"]}],
            "variants": [{
                "option1": "Default Title",
                "sku": sku,
                "barcode": barcode,
                "price": price,
                "inventory_policy": "continue",     # sell without stock check (decided 2026-08-31)
                "inventory_management": None,       # untracked
                "requires_shipping": True,
                "taxable": True,
            }],
            "metafields": metafields,
            "metafields_global": {"title_tag": seo_title, "description_tag": seo_desc[:320]},
        }
    }


def main():
    jobs = []
    for p in CATALOG["products"]:
        h, sv = p["handle"], p["sv"]
        jobs.append(product_payload(
            h, sv["name"], sv["description"], sv["category"],
            p.get("sku", ""), BARCODES[h], money(PRICES[h]),
            [
                mf("tagline", sv["tagline"], "single_line_text_field"),
                mf("volume", VOLUMES[h], "single_line_text_field"),
                mf("usage", USAGES[h], "multi_line_text_field"),
                mf("key_ingredients", json.dumps(sv["keyIngredients"], ensure_ascii=False), "json"),
                mf("inci", json.dumps(sv["inci"], ensure_ascii=False), "json"),
            ],
            f'{sv["name"]} {p["step"]} | NEXO', sv["description"],
        ))
    b = CATALOG["bundle"]
    jobs.append(product_payload(
        b["handle"], b["sv"]["name"], b["sv"]["description"], "Ritual",
        "", "", money(PRICES["the-ritual"]), [],
        f'{b["sv"]["name"]} | NEXO', b["sv"]["description"],
    ))
    jobs.append(product_payload(
        "borste", "NEXO Borste", "", "Tillbehör", "", "", money(PRICES["borste"]), [],
        "NEXO Borste | NEXO", "",
    ))

    created, skipped, failed = 0, 0, 0
    for payload in jobs:
        handle = payload["product"]["handle"]
        status, existing = call("GET", f"/products.json?handle={handle}&fields=id")
        pid = existing["products"][0]["id"] if status == 200 and existing.get("products") else None
        if pid:
            print(f"  skip (exists): {handle}")
            skipped += 1
        elif DRY:
            print(f"  DRY would create: {handle} @ {payload['product']['variants'][0]['price']}")
            continue
        else:
            status, resp = call("POST", "/products.json", payload)
            if status in (200, 201):
                pid = resp["product"]["id"]
                print(f"  created: {handle} (id {pid})")
                created += 1
            else:
                print(f"  FAIL {status}: {handle} → {resp.get('error')}")
                failed += 1
                continue
        # publish to the online store channel (status=active alone is NOT
        # enough for all_products — needs published + published_scope=web;
        # the storefront itself stays password-protected)
        if pid and not DRY:
            status, resp = call("PUT", f"/products/{pid}.json",
                                {"product": {"id": pid, "status": "active",
                                             "published": True, "published_scope": "web"}})
            if status != 200:
                print(f"  FAIL publish {status}: {handle} → {resp.get('error')}")
                failed += 1

    if not DRY:
        status, resp = call("POST", "/metafields.json", {"metafield": {
            "namespace": "nexo", "key": "ingredient_functions",
            "value": json.dumps(FUNCTIONS, ensure_ascii=False), "type": "json",
            "owner_resource": "shop",
        }})
        if status in (200, 201):
            print("  shop metafield nexo.ingredient_functions: set")
        else:
            print(f"  FAIL shop metafield {status}: {resp.get('error')}")
            failed += 1

    print(f"done: {created} created, {skipped} skipped, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
