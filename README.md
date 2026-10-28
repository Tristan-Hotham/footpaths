# The footpath capital of Britain

**Interactive map and league table:** https://tristan-hotham.github.io/footpaths/

**Archived data and code:** [doi:10.5281/zenodo.23736299](https://doi.org/10.5281/zenodo.23736299)

Which part of Britain has the most public footpaths, bridleways and byways for every square mile of land? This project measures every council area (local authority district) in England and Wales from the councils' own rights of way data, checks it against OpenStreetMap, and ranks the councils per square mile, per mile of road and per resident.

## Findings

- England and Wales have 139,409 miles of public rights of way in the councils' open data, 2.4 miles for every square mile of land (England 2.3, Wales 2.8). 77% of the length is footpath.
- **Rossendale** has the most per square mile: 7.7 miles of right of way per square mile (407 miles in 53 square miles). Nine of the top ten are in the South Pennines either side of the Lancashire and Yorkshire border: Rossendale, Calderdale (6.2), Pendle (5.9), Rochdale (5.5), Blackburn with Darwen (5.4), Oldham (5.2), Hyndburn (5.2), Burnley (5.1) and Bury (5.1). Malvern Hills (5.3) is the exception.
- Per mile of road, **Powys** leads with 3,388 yards of right of way per mile of road, then Malvern Hills and Rossendale. Per resident, Powys leads by far (249 feet per person), then Ceredigion and Gwynedd. Per square mile Powys is only 72nd.
- The fewest per square mile, outside inner London: Harrow (0.06), Enfield (0.11), Norwich, Havering and Barnet (about 0.16 to 0.18).
- The fourteen inner London boroughs never had to keep a definitive map and have no rights of way to count. Scotland has no comparable system (a right of responsible access to most land since 2003) and Northern Ireland very few recorded rights of way, so they are not ranked.
- OpenStreetMap holds 57% of the council length. Its mapped rights of way grew from 28,275 miles in 2016 to 79,896 in 2026.

## Method

1. **Council data.** rowmaps.com collects the open rights of way data of 149 highway authorities and gives each path section in a standard form, with its type, length in miles and end points (the "augmented" CSV files). 537,075 sections were downloaded on 28 October 2026. 4,233 sections that appear twice in overlapping datasets (two national parks, the old and new Cumbria datasets) were removed.
2. **Placing paths.** Each section was assigned to a local authority district (ONS, December 2024, ultra-generalised boundaries) by the midpoint of its two ends, with points just offshore given to the nearest district within 3 km. Inside Westmorland and Furness, the old Cumbria dataset was dropped in favour of the new one.
3. **OpenStreetMap check.** Ways tagged `designation` = `public_footpath`, `public_bridleway`, `restricted_byway` or `byway_open_to_all_traffic` (and `core_path` in Scotland) were measured inside each district (ONS generalised boundaries) with the ohsome API, snapshot 27 July 2026, every two years from 2016. Where a council's own total came to under 80% of OpenStreetMap's, which happens only where the council publishes no open data, OpenStreetMap was used instead: ten councils, marked `osm` in the results.
4. **Denominators.** Land area from the ONS generalised clipped boundaries (spherical area). Road length: OpenStreetMap public roads (motorway to residential and living streets, with links; not service roads or tracks) from ohsome. Population: ONS mid-2025 estimates via Nomis.

`analysis.py` reproduces every figure from the files in `data/raw/`.

## Limits

- Council data are an interpretation of the definitive map, not the map itself, and some files are years old.
- Placing a section by its midpoint puts paths that cross a boundary wholly on one side; small districts are most affected.
- A mile of path counts the same on a moor or in a town. This measures how much right of way there is, not how good, open or well used it is.
- Land area includes water bodies inside the coastline only where the ONS boundaries do.

## Files

| Path | What it is |
|---|---|
| `analysis.py` | The analysis |
| `data/raw/rowmaps_prow_midpoints.csv.gz` | Every council path section: authority code, type (F footpath, B bridleway, R restricted byway, O byway open to all traffic), miles, midpoint lon/lat |
| `data/raw/rowmaps_authorities.json` | The 149 authorities and the licence line of each file |
| `data/raw/footpaths_by_lad.json` | OpenStreetMap lengths (metres) by designation and year, road and off-road path lengths, area and population, per district |
| `data/raw/lad_buc.geojson` | ONS local authority districts, December 2024, ultra-generalised clipped |
| `results/footpaths_by_council.csv` | Every district with lengths, rates, ranks and source |
| `results/summary.json` | Headline figures |
| `index.html`, `data/lad.json`, `data/lad.geojson` | The interactive page and its data |
| `img/`, `header.png` | Graphics |
| `reddit/` | r/dataisbeautiful collage and post |

## Sources and licences

- Rights of way: data from each highway authority via rowmaps.com (Barry Cornelius), released under the Open Government Licence v3.0 (or the earlier OS OpenData licence). Contains Ordnance Survey data © Crown copyright and database right 2026. The details are an interpretation of each council's Definitive Map and should not be relied on for the line of any right of way.
- OpenStreetMap data © OpenStreetMap contributors, Open Database Licence, via the ohsome API (HeiGIT).
- Boundaries: Office for National Statistics, Open Government Licence v3. Contains OS data © Crown copyright and database right 2026.
- Population: ONS mid-2025 population estimates via Nomis, Open Government Licence v3.
- Map tiles on the page: Esri, HERE, Garmin, © OpenStreetMap contributors.

Code is MIT licensed. Derived data follow the licences above.

AI use: written with drafting, data and coding help from Claude (Anthropic).

Tristan Hotham, independent researcher, 2026.
