#!/usr/bin/env python3
"""List tire manufacturers (brands) present in the Odoo staging inventory.

Reads all records of the `x_tire_brands` model and, optionally, counts how many
products reference each brand via `x_studio_brand_tire`.

Usage:
    export ODOO_URL="https://staging.example.com"
    export ODOO_DB="staging_db_name"
    export ODOO_USER="your-login"
    export ODOO_PASSWORD="your-password-or-api-key"
    python3 scripts/list_tire_brands.py

Only depends on the Python standard library (xmlrpc.client).
"""
import os
import sys
import xmlrpc.client

URL = os.environ.get("ODOO_URL")
DB = os.environ.get("ODOO_DB")
USER = os.environ.get("ODOO_USER")
PASSWORD = os.environ.get("ODOO_PASSWORD")

if not all([URL, DB, USER, PASSWORD]):
    sys.exit("Set ODOO_URL, ODOO_DB, ODOO_USER and ODOO_PASSWORD environment variables.")

common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
uid = common.authenticate(DB, USER, PASSWORD, {})
if not uid:
    sys.exit("Authentication failed — check credentials/database name.")

models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")


def execute(model, method, *args, **kwargs):
    return models.execute_kw(DB, uid, PASSWORD, model, method, list(args), kwargs)


# 1) All defined tire brands.
brands = execute("x_tire_brands", "search_read", [], fields=["id", "x_name"])
brands = sorted(brands, key=lambda b: (b.get("x_name") or "").lower())

# 2) Count products per brand (brands actually used on inventory items).
counts = {}
try:
    grouped = execute(
        "product.template",
        "read_group",
        [["x_studio_brand_tire", "!=", False]],
        ["x_studio_brand_tire"],
        ["x_studio_brand_tire"],
    )
    for g in grouped:
        rel = g.get("x_studio_brand_tire")
        if rel:
            counts[rel[0]] = g.get("x_studio_brand_tire_count", g.get("__count", 0))
except Exception as exc:  # noqa: BLE001
    print(f"(product counts unavailable: {exc})\n", file=sys.stderr)

print(f"Tire manufacturers in Odoo ({len(brands)} brands defined):\n")
for b in brands:
    n = counts.get(b["id"])
    suffix = f"  ({n} products)" if n is not None else ""
    print(f"- {b['x_name']}{suffix}")
