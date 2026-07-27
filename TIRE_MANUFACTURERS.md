# Tire Manufacturers in Odoo Inventory

Source: `odoo_import/import_tire_brand.csv` (ready-to-load `tire.brand` list),
cross-referenced against `odoo_import/import_product_template.csv` (16,361 tire SKUs).
Snapshot date: 2026-07-27.

**80 manufacturers**, covering all 16,361 tire SKUs in the product master
(every SKU resolves to exactly one brand).

> `iLink` and `ZMAX` are two independent brands (the former combined `iLink / ZMAX`
> record was split; its 5 SKUs mapped to existing iLink lines). Count: 81 → 80.

## Alphabetical

- Aeolus
- Anchee
- Annaite
- Antares
- BFGoodrich
- Bridgestone
- Carlisle
- Continental
- Cooper
- Double Star
- DovRoad
- Dunlop
- Evergreen
- Falken
- Farroad
- Federal
- Firestone
- FISK
- Fortune
- Fronway
- Fuzion
- Galaxy
- General Tire
- Gislaved
- Goodride
- Goodyear
- Greentrac
- GT Radial
- Hankook
- Hercules
- iLink
- Imperial
- Ironhead
- Ironman
- Kapsen
- Kelly
- Kendra
- Kinforest
- Kumho
- Laufenn
- Maxtrek
- Maxxis
- Mazzini
- Michelin
- Mickey Thompson
- Minerva
- Mirage
- Nankang
- Nexen
- Nitto
- Nokian
- Nordman
- Onyx
- Ovation
- Pirelli
- Predator
- Pro Comp
- Radar
- RidgeTrak
- RoadBoss
- RoadKing
- RoadX
- Rovelo
- Rydanz
- Sailun
- Starfire
- Sumitomo
- Sunfull
- SureTrac
- TBC
- Toyo
- Tracmax
- Trail Buster
- Triangle
- Uniroyal
- Vredestein
- Wanli
- Westlake
- Yokohama
- ZMAX

## By SKU count (descending)

| # | Manufacturer | SKUs |
|---:|---|---:|
| 1 | Michelin | 2,702 |
| 2 | Bridgestone | 2,435 |
| 3 | Continental | 1,741 |
| 4 | Goodyear | 1,420 |
| 5 | Nexen | 1,052 |
| 6 | Pirelli | 1,001 |
| 7 | BFGoodrich | 914 |
| 8 | Firestone | 848 |
| 9 | Nokian | 670 |
| 10 | Minerva | 506 |
| 11 | Ovation | 466 |
| 12 | Uniroyal | 444 |
| 13 | Fuzion | 245 |
| 14 | iLink | 178 |
| 15 | Toyo | 167 |
| 16 | General Tire | 124 |
| 17 | Cooper | 114 |
| 18 | Yokohama | 111 |
| 19 | Greentrac | 102 |
| 20 | Kumho | 94 |
| 21 | Kapsen | 88 |
| 22 | Maxtrek | 88 |
| 23 | Hankook | 84 |
| 24 | Sumitomo | 76 |
| 25 | Dunlop | 62 |
| 26 | Antares | 54 |
| 27 | Sailun | 54 |
| 28 | Falken | 50 |
| 29 | Laufenn | 47 |
| 30 | Nitto | 41 |
| 31 | Goodride | 39 |
| 32 | RoadX | 34 |
| 33 | Westlake | 31 |
| 34 | Nordman | 28 |
| 35 | Carlisle | 23 |
| 36 | Kelly | 20 |
| 37 | Kinforest | 19 |
| 38 | Starfire | 16 |
| 39 | Rovelo | 15 |
| 40 | Mirage | 13 |
| 41 | Fortune | 12 |
| 42 | Hercules | 12 |
| 43 | Ironman | 11 |
| 44 | TBC | 10 |
| 45 | Double Star | 8 |
| 46 | Triangle | 8 |
| 47 | Mickey Thompson | 7 |
| 48 | Radar | 7 |
| 49 | GT Radial | 6 |
| 50 | Farroad | 5 |
| 51 | RoadBoss | 5 |
| 52 | Anchee | 4 |
| 53 | Sunfull | 4 |
| 54 | DovRoad | 3 |
| 55 | Mazzini | 3 |
| 56 | SureTrac | 3 |
| 57 | Vredestein | 3 |
| 58 | ZMAX | 3 |
| 59 | FISK | 2 |
| 60 | Galaxy | 2 |
| 61 | Gislaved | 2 |
| 62 | Maxxis | 2 |
| 63 | Nankang | 2 |
| 64 | Onyx | 2 |
| 65 | Predator | 2 |
| 66 | RidgeTrak | 2 |
| 67 | RoadKing | 2 |
| 68 | Aeolus | 1 |
| 69 | Annaite | 1 |
| 70 | Evergreen | 1 |
| 71 | Federal | 1 |
| 72 | Fronway | 1 |
| 73 | Imperial | 1 |
| 74 | Ironhead | 1 |
| 75 | Kendra | 1 |
| 76 | Pro Comp | 1 |
| 77 | Rydanz | 1 |
| 78 | Tracmax | 1 |
| 79 | Trail Buster | 1 |
| 80 | Wanli | 1 |
| | **Total** | **16,361** |

## SKU normalization — restored dropped zeros

Manufacturer SKUs are fixed-width per brand, but numeric export dropped leading
zeros. Restored **571** codes to canonical width:

| Brand | Width | Codes fixed | Example |
|---|---:|---:|---|
| Michelin | 5 | 346 | `3995` → `03995` |
| BFGoodrich | 5 | 149 | `1727` → `01727` |
| Uniroyal | 5 | 69 | `6930` → `06930` |
| Bridgestone | 6 | 2 | `7147` → `007147` |
| Firestone | 6 | 1 | `24975` → `024975` |
| Dunlop | 9 | 4 | `57000010` → `057000010` |

Goodyear and Cooper are also 9-digit, but every code is already full-width — no
change needed. All padding is leading (left-pad).

This resolved the duplicate manufacturer SKU **`24975`**: Michelin `24975` (5-digit)
vs Firestone `024975` (6-digit) are distinct once zero-padded. **0 duplicate SKUs remain.**

### Brands left as-is (mixed code systems — not zero-drops)

- **Greentrac** — mixes 13-digit UPCs with 7-digit part numbers (different systems).
- **Kapsen** (6/7/9), **Double Star** (7/8), **Carlisle** (6/7) — genuinely variable
  widths; left untouched unless a conflict surfaces.

## Other data-quality flags

- **2,950 SKUs (18%)** have a brand but no product-line link — back-fill pending per-brand feeds.
