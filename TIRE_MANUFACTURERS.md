# Tire Manufacturers in Odoo Inventory

Source: `05_odoo_import/import_tire_brand.csv` (the ready-to-load `tire.brand` list),
cross-referenced against `import_product_template.csv` (16,361 tire SKUs).
Snapshot date: 2026-07-27.

**81 manufacturers**, covering all 16,361 tire SKUs in the product master
(every SKU resolves to exactly one brand).

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
- iLink / ZMAX
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
| 14 | iLink | 173 |
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
| 51 | iLink / ZMAX | 5 |
| 52 | RoadBoss | 5 |
| 53 | Anchee | 4 |
| 54 | Sunfull | 4 |
| 55 | DovRoad | 3 |
| 56 | Mazzini | 3 |
| 57 | SureTrac | 3 |
| 58 | Vredestein | 3 |
| 59 | ZMAX | 3 |
| 60 | FISK | 2 |
| 61 | Galaxy | 2 |
| 62 | Gislaved | 2 |
| 63 | Maxxis | 2 |
| 64 | Nankang | 2 |
| 65 | Onyx | 2 |
| 66 | Predator | 2 |
| 67 | RidgeTrak | 2 |
| 68 | RoadKing | 2 |
| 69 | Aeolus | 1 |
| 70 | Annaite | 1 |
| 71 | Evergreen | 1 |
| 72 | Federal | 1 |
| 73 | Fronway | 1 |
| 74 | Imperial | 1 |
| 75 | Ironhead | 1 |
| 76 | Kendra | 1 |
| 77 | Pro Comp | 1 |
| 78 | Rydanz | 1 |
| 79 | Tracmax | 1 |
| 80 | Trail Buster | 1 |
| 81 | Wanli | 1 |
| | **Total** | **16,361** |

## Notes

- `iLink`, `ZMAX`, and `iLink / ZMAX` appear as three separate brand records — an unresolved
  duplicate/merge decision from the manufacturer cleanup sheet (`manufacturers_master.csv`,
  the "11 cleanup decisions"). They likely collapse to a single brand family; kept as-is here
  to match the current import file.
- This is the structural brand master (manufacturers carried across feeds + stocked inventory).
  It is not a stock-on-hand report — inventory/stock levels are a separate, deferred pass.
