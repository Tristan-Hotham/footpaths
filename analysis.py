"""Which council area has the most public footpaths per square mile?

Main measure (England and Wales): public rights of way from councils' open data (149 highway authorities, collected and
standardised by rowmaps.com; Open Government Licence), each path section placed in a local authority district (ONS, Dec 2024)
by the midpoint of its two ends, with its length as given by rowmaps (miles).
Check and fallback: rights of way mapped in OpenStreetMap (designation=public_footpath|public_bridleway|restricted_byway|
byway_open_to_all_traffic), measured inside each district with the ohsome API (snapshot 27 July 2026, history 2016 to 2026).
Scotland has no rights-of-way system like England's (access rights apply to most land) and Northern Ireland very few
recorded rights of way, so for the whole UK the page also gives core paths (Scotland) and all mapped off-road paths.

Inputs (data/raw/): rowmaps_prow_midpoints.csv.gz, rowmaps_authorities.json, footpaths_by_lad.json, lad_buc.geojson
Outputs: results/footpaths_by_council.csv, results/summary.json, data/lad.json, data/lad.geojson
"""
import json, os
import pandas as pd, geopandas as gpd

HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: os.path.join(HERE, *a)
MI, YEARS = 1609.344, [2016, 2018, 2020, 2022, 2024, 2026]
SQMI = MI * MI
NATION = {"E": "England", "W": "Wales", "S": "Scotland", "N": "Northern Ireland"}
INNER_LONDON = {"E09000001", "E09000007", "E09000011", "E09000012", "E09000013", "E09000019", "E09000020", "E09000022",
                "E09000023", "E09000025", "E09000028", "E09000030", "E09000032", "E09000033"}  # no definitive map duty

# ---------- official rights of way (rowmaps) ----------
rw = pd.read_csv(P("data/raw/rowmaps_prow_midpoints.csv.gz"))
n0 = len(rw)
rw = rw[~rw.duplicated(["lon", "lat", "miles"])]           # the same section supplied by two overlapping datasets
lad = gpd.read_file(P("data/raw/lad_buc.geojson")).to_crs(27700)
pts = gpd.GeoDataFrame(rw, geometry=gpd.points_from_xy(rw.lon, rw.lat), crs=4326).to_crs(27700)
j = gpd.sjoin(pts, lad[["code", "geometry"]], how="left", predicate="within").drop(columns="index_right")
out = j[j.code.isna()].drop(columns="code")
near = gpd.sjoin_nearest(out, lad[["code", "geometry"]], how="left", max_distance=3000).drop(columns="index_right")
j = pd.concat([j[~j.code.isna()], near])
# old Cumbria dataset overlaps the newer Westmorland and Furness one: keep W&F inside W&F
j = j[~((j.auth == "CU") & (j.code == "E06000064"))]
off = j.pivot_table(index="code", columns="type", values="miles", aggfunc="sum", fill_value=0)
off["all"] = off.sum(axis=1)
main_auth = j.groupby(["code", "auth"]).miles.sum().reset_index().sort_values("miles").groupby("code").tail(1).set_index("code").auth
dup_removed = n0 - len(rw)

# ---------- OpenStreetMap (ohsome) ----------
RAW = json.load(open(P("data/raw/footpaths_by_lad.json")))
rows = []
for code, r in RAW.items():
    L = lambda k: r["len"].get("designation=" + k, [0] * 6)
    osm_series = [sum(L(k)[i] for k in ("public_footpath", "public_bridleway", "restricted_byway", "byway_open_to_all_traffic"))
                  for i in range(6)]
    o = off.loc[code] if code in off.index else None
    rows.append({
        "code": code, "name": r["name"], "nation": NATION[code[0]], "area_sqmi": r["area_m2"] / SQMI, "pop": r.get("pop") or 0,
        "road_mi": r.get("roads", 0) / MI, "offroad_mi": r.get("offroad", 0) / MI, "core_mi": L("core_path")[-1] / MI,
        "osm_mi": osm_series[-1] / MI, **{f"osm_mi_{y}": v / MI for y, v in zip(YEARS, osm_series)},
        "osm_footpath_mi": L("public_footpath")[-1] / MI,
        "off_mi": float(o["all"]) if o is not None else 0.0,
        "off_footpath_mi": float(o.get("F", 0)) if o is not None else 0.0,
        "off_bridleway_mi": float(o.get("B", 0)) if o is not None else 0.0,
        "off_byway_mi": float(o.get("R", 0) + o.get("O", 0)) if o is not None else 0.0,
        "auth": main_auth.get(code, ""),
    })
df = pd.DataFrame(rows)
ew = df.nation.isin(["England", "Wales"])
df["source"] = ""
df.loc[ew, "source"] = "council"
df.loc[ew & (df.off_mi < 0.8 * df.osm_mi), "source"] = "osm"        # no open council data: OpenStreetMap instead
df.loc[df.code.isin(INNER_LONDON), "source"] = "inner_london"
df.loc[df.code == "E06000053", "source"] = "none"                      # Isles of Scilly: no recorded rights of way
df["prow_mi"] = df.off_mi.where(df.source != "osm", df.osm_mi)
df.loc[~ew, "prow_mi"] = df.osm_mi
df["footpath_mi"] = df.off_footpath_mi.where(df.source == "council", df.osm_footpath_mi)
df["prow_per_sqmi"] = df.prow_mi / df.area_sqmi
df["prow_yd_per_road_mi"] = 1760 * df.prow_mi / df.road_mi
df["prow_ft_per_head"] = 5280 * df.prow_mi / df["pop"].where(df["pop"] > 0)
df["offroad_per_sqmi"] = df.offroad_mi / df.area_sqmi
df["core_per_sqmi"] = df.core_mi / df.area_sqmi
df["osm_cover"] = (df.osm_mi / df.off_mi.where(df.source == "council")).clip(upper=2)
df["bridle_share"] = (df.prow_mi - df.footpath_mi) / df.prow_mi.where(df.prow_mi > 0)
E = df[ew].copy()
for col, rk in [("prow_per_sqmi", "rank_sqmi"), ("prow_yd_per_road_mi", "rank_road"), ("prow_ft_per_head", "rank_head")]:
    E[rk] = E[col].rank(ascending=False, method="min")
df = df.merge(E[["code", "rank_sqmi", "rank_road", "rank_head"]], on="code", how="left")
df["rank_offroad_uk"] = df.offroad_per_sqmi.rank(ascending=False, method="min")

os.makedirs(P("results"), exist_ok=True)
df.sort_values(["rank_sqmi", "rank_offroad_uk"]).round(4).to_csv(P("results/footpaths_by_council.csv"), index=False)

def top(d, col, n=10, asc=False):
    t = d.dropna(subset=[col]).sort_values(col, ascending=asc).head(n)
    return [{"name": r["name"], "code": r.code, "value": round(float(r[col]), 3), "source": r.source} for _, r in t.iterrows()]

E = df[ew]
nat = {}
for n, g in df.groupby("nation"):
    nat[n] = {"councils": int(len(g)), "area_sqmi": round(g.area_sqmi.sum(), 1), "pop": int(g["pop"].sum()),
              "prow_mi": round(g.prow_mi.sum(), 1), "osm_prow_mi": round(g.osm_mi.sum(), 1), "core_mi": round(g.core_mi.sum(), 1),
              "offroad_mi": round(g.offroad_mi.sum(), 1), "road_mi": round(g.road_mi.sum(), 1),
              "prow_per_sqmi": round(g.prow_mi.sum() / g.area_sqmi.sum(), 3),
              "offroad_per_sqmi": round(g.offroad_mi.sum() / g.area_sqmi.sum(), 3),
              "core_per_sqmi": round(g.core_mi.sum() / g.area_sqmi.sum(), 3)}
rv = df[df.code == "E07000124"].iloc[0]
def f(v):
    return round(float(v), 3) if isinstance(v, (float, int)) or hasattr(v, "item") else v
S = {
    "osm_snapshot": "2026-07-27", "rowmaps_authorities": len(json.load(open(P("data/raw/rowmaps_authorities.json")))["authorities"]),
    "rowmaps_sections": int(n0), "rowmaps_duplicates_removed": int(dup_removed),
    "ew_councils": int(len(E)), "ew_council_source": int((E.source == "council").sum()), "ew_osm_source": int((E.source == "osm").sum()),
    "ew_prow_mi": round(E.prow_mi.sum(), 1), "ew_osm_mi": round(E.osm_mi.sum(), 1),
    "ew_osm_share_of_council": round(E[E.source == "council"].osm_mi.sum() / E[E.source == "council"].off_mi.sum(), 3),
    "ew_prow_per_sqmi": round(E.prow_mi.sum() / E.area_sqmi.sum(), 3), "ew_median_per_sqmi": round(E.prow_per_sqmi.median(), 3),
    "ew_footpath_share": round(E.footpath_mi.sum() / E.prow_mi.sum(), 3),
    "nations": nat,
    "top_sqmi": top(E, "prow_per_sqmi", 20), "bottom_sqmi_outside_inner_london": top(E[~E.source.isin(["inner_london", "none"])], "prow_per_sqmi", 10, True),
    "top_road": top(E, "prow_yd_per_road_mi", 10), "top_head": top(E, "prow_ft_per_head", 10),
    "top_bridle_share": top(E[E.prow_mi > 50], "bridle_share", 10),
    "top_offroad_uk": top(df, "offroad_per_sqmi", 10), "top_core_scotland": top(df[df.nation == "Scotland"], "core_per_sqmi", 10),
    "worst_osm_cover": top(E[(E.source == "council") & (E.off_mi > 50)], "osm_cover", 10, True),
    "ribble_valley": {k: f(rv[k]) for k in ["name", "area_sqmi", "pop", "prow_mi", "footpath_mi", "off_bridleway_mi", "prow_per_sqmi",
                                           "prow_yd_per_road_mi", "prow_ft_per_head", "rank_sqmi", "rank_road", "rank_head",
                                           "osm_mi", "offroad_per_sqmi", "source"]},
    "rv_osm_mi_by_year": {y: round(float(rv[f"osm_mi_{y}"]), 1) for y in YEARS},
    "ew_osm_mi_by_year": {y: round(float(E[f"osm_mi_{y}"].sum()), 1) for y in YEARS},
}
json.dump(S, open(P("results/summary.json"), "w"), indent=1, default=str)

# page data
cols = ["code", "name", "nation", "area_sqmi", "pop", "prow_mi", "footpath_mi", "road_mi", "offroad_mi", "core_mi", "osm_mi",
        "source", "rank_sqmi", "rank_road", "rank_head"]
page = df[cols].copy()
for c in ["area_sqmi", "prow_mi", "footpath_mi", "road_mi", "offroad_mi", "core_mi", "osm_mi"]:
    page[c] = page[c].round(1)
page["nation"] = page.nation.str[0]
page = page.astype(object).where(page.notna(), None)
json.dump({"cols": cols, "rows": page.values.tolist()}, open(P("data/lad.json"), "w"), separators=(",", ":"), default=lambda v: int(v))
g = gpd.read_file(P("data/raw/lad_buc.geojson"))
g["geometry"] = g.geometry.simplify(0.003, preserve_topology=True)
g[["code", "geometry"]].to_file(P("data/lad.geojson"), driver="GeoJSON", COORDINATE_PRECISION=4)
print(json.dumps({k: S[k] for k in ["ew_prow_mi", "ew_osm_mi", "ew_osm_share_of_council", "ew_prow_per_sqmi", "ew_median_per_sqmi",
                                    "ew_council_source", "ew_osm_source", "ribble_valley"]}, indent=1, default=str))
print("TOP", [(t["name"], t["value"]) for t in S["top_sqmi"]])
print("ROAD", [(t["name"], round(t["value"])) for t in S["top_road"]])
print("HEAD", [(t["name"], round(t["value"])) for t in S["top_head"]])
print("BOTTOM", [(t["name"], t["value"]) for t in S["bottom_sqmi_outside_inner_london"]])
print("NATIONS", {k: (v["prow_per_sqmi"], v["offroad_per_sqmi"], v["core_per_sqmi"]) for k, v in nat.items()})
print("OFFROAD UK", [(t["name"], t["value"]) for t in S["top_offroad_uk"]])
print("CORE", [(t["name"], t["value"]) for t in S["top_core_scotland"][:5]])
print("BRIDLE", [(t["name"], t["value"]) for t in S["top_bridle_share"][:5]])
