## Title

[OC] Which part of Britain has the most public footpaths? Rossendale in Lancashire has 7.7 miles of right of way per square mile of land, more than three times the England and Wales average of 2.4 (councils' rights of way open data via rowmaps.com, OpenStreetMap, ONS)

## Body (optional)

I added up the public rights of way (footpaths, bridleways and byways) in all 318 council areas of England and Wales, 139,409 miles in all, and divided by land area. Rossendale is top at 7.7 miles per square mile, then Calderdale (6.2), Pendle (5.9), Rochdale (5.5) and Blackburn with Darwen (5.4): nine of the top ten are South Pennine mill-town districts either side of the Lancashire and Yorkshire border, with Malvern Hills (5.3) the one outsider. Wales has 2.8 miles per square mile and England 2.3. It depends how you count: per person Powys comes top with 249 feet of path each, and per mile of road too (3,388 yards), though it is only 72nd per square mile. At the other end, Harrow has 0.06 miles per square mile, the fewest outside inner London, and the inner London boroughs have no definitive map of rights of way at all. OpenStreetMap holds 57% of the length in councils' own data, up from 28,275 miles mapped in 2016 to 79,896 in 2026.

Caveat: 10 councils publish no open rights of way data, so OpenStreetMap fills in for them, and Scotland (right of responsible access to most land) and Northern Ireland (very few recorded rights of way) are not comparable.

Interactive version: https://tristan-hotham.github.io/footpaths/

## Source comment

Sources: public rights of way from councils' own open data, collected and standardised by rowmaps.com (Open Government Licence v3; contains OS data © Crown copyright and database right 2026), each path section placed in a council area by its midpoint. Check and fallback for the 10 councils with no open data: OpenStreetMap contributors via the ohsome API (HeiGIT), snapshot 27 July 2026 and history 2016 to 2026 (ODbL). Council areas: ONS local authority district boundaries, December 2024 (Open Government Licence v3). Population: ONS mid-2025 population estimates via Nomis (Open Government Licence v3).

Tools: Python (pandas, GeoPandas, pyproj, matplotlib).

Interactive: https://tristan-hotham.github.io/footpaths/
Blog post: https://blog.tristanhotham.com/2026/10/28/footpaths/
Paper: https://doi.org/10.5281/zenodo.23736299
