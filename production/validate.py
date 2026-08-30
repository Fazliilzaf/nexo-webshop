#!/usr/bin/env python3
"""NEXO pre-import validation.

Bad data must be stopped BEFORE Shopify, not discovered visually after
import. Validates locked sources AND generated import files.

Exit 0 = PASS (integrity). Exit 1 = FAIL.
Empty-but-expected fields (price, inventory, weight) are reported as
BLOCKED — they do not fail the run, but they are printed loudly.

Stdlib only. Usage: python3 production/validate.py
"""
import csv
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMPORT = os.path.join(ROOT, "production", "import")

FAILURES = []
BLOCKED = []
NOTES = []

BANNED_CLAIMS = re.compile(
    r"vegan|cruelty|hårväxt|hair\s?growth|läkning|healing|transplant",
    re.IGNORECASE,
)
REQUIRED_HANDLES = ["lather-me-up", "mist-me-crazy", "whip-me-good", "the-ritual"]
RITUAL_HANDLES = REQUIRED_HANDLES[:3]
VOLUMES = {"lather-me-up": "250 ml", "mist-me-crazy": "100 ml", "whip-me-good": "30 ml"}


def fail(msg):
    FAILURES.append(msg)


def blocked(msg):
    BLOCKED.append(msg)


def note(msg):
    NOTES.append(msg)


def read_csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    # ---- sources ----
    with open(os.path.join(ROOT, "content", "products.json"), encoding="utf-8") as f:
        catalog = json.load(f)
    with open(os.path.join(ROOT, "content", "ingredient-functions.json"), encoding="utf-8") as f:
        functions = json.load(f)["functions"]

    # ---- generated files must exist (run build.py first) ----
    for name in ["products.csv", "products-accessory.csv", "shop-metafields.csv"]:
        if not os.path.exists(os.path.join(IMPORT, name)):
            fail(f"missing generated file: production/import/{name} — run build.py")
    if FAILURES:
        return report()

    products = read_csv(os.path.join(IMPORT, "products.csv"))
    accessory = read_csv(os.path.join(IMPORT, "products-accessory.csv"))
    all_rows = products + accessory

    # ---- 1. handles ----
    handles = {r["Handle"] for r in products}
    for h in REQUIRED_HANDLES:
        if h not in handles:
            fail(f"missing handle in products.csv: {h}")
    if not any(r["Handle"] == "borste" for r in accessory):
        fail("missing accessory handle: borste")

    # ---- 2. no +4 / unknown ritual index anywhere ----
    for r in all_rows:
        blob = " ".join(str(v) for v in r.values())
        if re.search(r"\+4", blob):
            fail(f"+4 reference found in row: {r['Handle']}")

    # ---- 3. volumes present for ritual products ----
    vol_col = "Metafield: nexo.volume [single_line_text_field]"
    for r in products:
        if r["Handle"] in VOLUMES and not r.get(vol_col):
            fail(f"missing volume for {r['Handle']}")

    # ---- 4. INCI format + duplicates + functions coverage ----
    inci_col = "Metafield: nexo.inci [json]"
    ki_col = "Metafield: nexo.key_ingredients [json]"
    unique_names = set()
    for p in catalog["products"]:
        h = p["handle"]
        inci = p["sv"]["inci"]
        seen = set()
        for entry in inci:
            if not (isinstance(entry, list) and len(entry) == 2
                    and all(isinstance(x, str) and x.strip() for x in entry)):
                fail(f"bad INCI entry format in {h}: {entry!r}")
                continue
            name = entry[0]
            if name in seen:
                fail(f"duplicate ingredient within {h}: {name}")
            seen.add(name)
            unique_names.add(name)
            if name not in functions:
                fail(f"INCI name has no function classification: {name} ({h})")
        # every product row must carry its INCI + key ingredients
        row = next((r for r in products if r["Handle"] == h), None)
        if row and not row.get(inci_col):
            fail(f"empty nexo.inci for {h}")
        if row and not row.get(ki_col):
            fail(f"empty nexo.key_ingredients for {h}")
    note(f"unique ingredients across range: {len(unique_names)}")

    # bundle must NOT carry INCI
    bundle_row = next((r for r in products if r["Handle"] == "the-ritual"), None)
    if bundle_row and bundle_row.get(inci_col):
        fail("the-ritual carries INCI — bundle has no formula of its own")

    # ---- 5. functions map must not contain stray keys ----
    for key in functions:
        if key not in unique_names:
            note(f"function classification without matching INCI entry: {key}")

    # ---- 6. dev-only assets / ECRAZY / pump in import-bound data ----
    for r in all_rows:
        blob = " ".join(str(v) for v in r.values())
        if ".dev." in blob:
            fail(f"dev-only asset referenced in import row: {r['Handle']}")
        if re.search(r"ecrazy", blob, re.IGNORECASE):
            fail(f"ECRAZY string in import row: {r['Handle']}")
    whip = next((r for r in products if r["Handle"] == "whip-me-good"), None)
    if whip and re.search(r"pump|combo", " ".join(whip.values()), re.IGNORECASE):
        fail("pump/combo reference in +3 row — jar is canonical")

    # ---- 7. banned claims in import-bound strings ----
    for r in all_rows:
        for col in ["Title", "Body (HTML)", "Tags", "SEO Title", "SEO Description",
                    "Metafield: nexo.tagline [single_line_text_field]",
                    "Metafield: nexo.usage [multi_line_text_field]"]:
            v = r.get(col, "")
            m = BANNED_CLAIMS.search(v or "")
            if m:
                fail(f"unapproved claim '{m.group(0)}' in {r['Handle']} → {col}")

    # ---- 8. asset manifest: approved files must exist, statuses sane ----
    mpath = os.path.join(ROOT, "production", "asset-manifest.csv")
    if not os.path.exists(mpath):
        fail("missing production/asset-manifest.csv — run build.py")
    else:
        for row in read_csv(mpath):
            status = row["production_status"]
            if status.startswith("approved"):
                asset = os.path.join(ROOT, "theme", "assets", row["asset"])
                if not os.path.exists(asset):
                    fail(f"approved asset missing from theme/assets: {row['asset']}")
            if status == "approved" and ".dev." in row["asset"]:
                fail(f"dev asset marked production-ready: {row['asset']}")
            if row["handle"] == "whip-me-good" and "combo" in row["asset"] and status.startswith("approved"):
                fail("pump-combo approved for +3 — jar is canonical")

    # ---- 9. empty-but-expected (BLOCKED, not failures) ----
    for r in all_rows:
        if not r["Variant Price"]:
            blocked(f"Variant Price empty: {r['Handle']} (hard blocker)")
        if not r["Variant Grams"]:
            blocked(f"Variant Grams empty: {r['Handle']}")
        if not r["Variant Inventory Qty"]:
            blocked(f"Variant Inventory Qty empty: {r['Handle']}")

    return report()


def report():
    print("=" * 60)
    print("NEXO pre-import validation")
    print("=" * 60)
    for n in NOTES:
        print(f"  note:    {n}")
    for b in BLOCKED:
        print(f"  BLOCKED: {b}")
    for f_ in FAILURES:
        print(f"  FAIL:    {f_}")
    print("-" * 60)
    if FAILURES:
        print(f"RESULT: FAIL — {len(FAILURES)} integrity failure(s), "
              f"{len(BLOCKED)} blocked field(s)")
        return 1
    print(f"RESULT: PASS — 0 integrity failures, "
          f"{len(BLOCKED)} blocked field(s) awaiting hard-blocker decisions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
