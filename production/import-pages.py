#!/usr/bin/env python3
"""Create/update NEXO pages + journal blog via Shopify Admin REST API.

- ingredienser (template page.ingredients)
- om-nexo (template page.brand)
- legal pages (default template) from production/legal/*.md — published
  since 2026-08-31 (company data filled; legal review still recommended)
- blog 'journal' (no articles — empty state by design)

Idempotent by handle; existing pages get body/publish-state updated.
Stdlib only. Usage: python3 production/import-pages.py
"""
import json
import os
import re
import sys
import urllib.request
import urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOP = "wju0k3-q1.myshopify.com"
API = f"https://{SHOP}/admin/api/2026-07"

with open(os.path.join(ROOT, "production", ".secrets", "admin-api-token"), encoding="utf-8") as f:
    TOKEN = f.read().strip()


def call(method, path, payload=None):
    req = urllib.request.Request(f"{API}{path}",
        data=json.dumps(payload).encode() if payload is not None else None, method=method)
    req.add_header("X-Shopify-Access-Token", TOKEN)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            body = r.read().decode()
            return r.status, json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:400]}


def md_to_html(md):
    """Minimal converter for our legal drafts: h2, lists, bold, paragraphs."""
    html, in_list = [], False
    for raw in md.split("\n"):
        line = raw.rstrip()
        if line.startswith("## "):
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("- "):
            if not in_list:
                html.append("<ul>")
                in_list = True
            item = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line[2:])
            html.append(f"<li>{item}</li>")
        elif not line.strip():
            if in_list:
                html.append("</ul>")
                in_list = False
        elif line.startswith("*Utkast") or line.startswith("**DRAFT") or line.startswith("# "):
            continue  # review banners and the md h1 live in the repo, not on the page
        else:
            if in_list:
                html.append("</ul>")
                in_list = False
            text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)
            html.append(f"<p>{text}</p>")
    if in_list:
        html.append("</ul>")
    return "\n".join(html)


PAGES = [
    ("Ingredienser", "ingredienser", "ingredients", None, True),
    ("Om NEXO", "om-nexo", "brand", None, True),
    ("Integritetspolicy", "integritetspolicy", None, "integritetspolicy.md", True),
    ("Köpvillkor", "kopvillkor", None, "kopvillkor.md", True),
    ("Frakt & leverans", "frakt-och-leverans", None, "frakt-och-leverans.md", True),
    ("Returer & ångerrätt", "returer-och-angerratt", None, "returer-och-angerratt.md", True),
]


def main():
    for title, handle, suffix, mdfile, publish in PAGES:
        body = ""
        if mdfile:
            with open(os.path.join(ROOT, "production", "legal", mdfile), encoding="utf-8") as f:
                body = md_to_html(f.read())
        status, existing = call("GET", f"/pages.json?handle={handle}&fields=id")
        if status == 200 and existing.get("pages"):
            pid = existing["pages"][0]["id"]
            payload = {"page": {"id": pid, "published": publish}}
            if mdfile:
                payload["page"]["body_html"] = body
            status, resp = call("PUT", f"/pages/{pid}.json", payload)
            if status == 200:
                print(f"  updated: {handle} [{'published' if publish else 'unpublished'}]")
            else:
                print(f"  FAIL update {status}: {handle} → {resp.get('error')}")
            continue
        payload = {"page": {
            "title": title,
            "handle": handle,
            "body_html": body,
            "template_suffix": suffix or "",
            "published": publish,
        }}
        status, resp = call("POST", "/pages.json", payload)
        if status in (200, 201):
            state = "published" if publish else "UNPUBLISHED (org-token pending)"
            print(f"  created: {handle} [{state}]")
        else:
            print(f"  FAIL {status}: {handle} → {resp.get('error')}")

    status, existing = call("GET", "/blogs.json?handle=journal&fields=id")
    if status == 200 and existing.get("blogs"):
        print("  skip (exists): blog journal")
    else:
        status, resp = call("POST", "/blogs.json", {"blog": {"title": "Journal", "handle": "journal"}})
        if status in (200, 201):
            print("  created: blog journal")
        else:
            print(f"  FAIL blog {status}: {resp.get('error')}")


if __name__ == "__main__":
    sys.exit(main())
