"""Shared data and map helpers for the footpath graphics. Every number comes from results/footpaths_by_council.csv and
results/summary.json (or is computed from them); boundaries from data/raw/lad_buc.geojson (ONS LAD Dec 2024).
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import numpy as np, pandas as pd, geopandas as gpd
from house import *                     # noqa: F401,F403  (BGC, FG, MUT, DISP, SER, MONO, words, headlines, footer ...)
from matplotlib.patches import Patch

P = lambda *a: os.path.join(ROOT, *a)

# ---------- palette ----------
GREENS = ["#E6EBD6", "#C6D8A8", "#97BC80", "#62995B", "#347240", "#164A2B"]   # pale sage to forest
BINS = [0, 1, 2, 3, 4, 5, np.inf]
BIN_LABELS = ["under 1", "1 to 2", "2 to 3", "3 to 4", "4 to 5", "5 or more"]
RUST = "#B5532A"                        # bracken: Ribble Valley
GREY = "#DCD7CC"                        # Scotland and Northern Ireland (no comparable rights of way)
NOMAP = "#FFFFFF"                       # inner London and Isles of Scilly: no definitive map
NOMAP_HATCH = "#B9B2A5"
RV = "E07000124"

# ---------- data ----------
D = pd.read_csv(P("results/footpaths_by_council.csv"))
S = json.load(open(P("results/summary.json")))
EW = D[D.nation.isin(["England", "Wales"])].copy()
TOP = EW.sort_values("rank_sqmi")
R = D[D.code == RV].iloc[0]

N = {
    "top_name": TOP.iloc[0]["name"], "top_val": TOP.iloc[0].prow_per_sqmi,
    "avg": S["ew_prow_per_sqmi"], "total": S["ew_prow_mi"],
    "osm_share": S["ew_osm_share_of_council"], "osm_years": {int(k): v for k, v in S["ew_osm_mi_by_year"].items()},
    "rv_val": R.prow_per_sqmi, "rv_rank": int(R.rank_sqmi), "rv_road": int(R.rank_road), "rv_head": int(R.rank_head),
    "rv_yd_road": R.prow_yd_per_road_mi, "rv_ft_head": R.prow_ft_per_head,
    "road_top": S["top_road"][0]["name"], "head_top": S["top_head"][0]["name"],
    "n_councils": S["ew_councils"], "n_osm": S["ew_osm_source"], "n_council_src": S["ew_council_source"],
    "n_inner": int((EW.source == "inner_london").sum()),
}
assert abs(N["top_val"] - S["top_sqmi"][0]["value"]) < 1e-3


def fmt1(v):
    return f"{v:.1f}"


def ordinal(n):
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


# ---------- geometry ----------
def load_geo(simplify=250):
    g = gpd.read_file(P("data/raw/lad_buc.geojson")).to_crs(27700)
    g["geometry"] = g.geometry.simplify(simplify, preserve_topology=True)
    g = g.set_geometry(g.geometry.scale(1e-3, 1e-3, origin=(0, 0)))
    g = g.merge(D[["code", "nation", "source", "prow_per_sqmi", "rank_sqmi"]], on="code", how="left")
    g["cls"] = pd.cut(g.prow_per_sqmi, BINS, right=False, labels=False)
    return g


def draw_map(ax, g, lw=0.25, edge="#FFFFFF", rv_lw=1.6, hatch_lw=0.4):
    ctx = g[g.nation.isin(["Scotland", "Northern Ireland"])]
    ctx.plot(ax=ax, color=GREY, edgecolor=BGC, linewidth=lw, zorder=1)
    ew = g[g.nation.isin(["England", "Wales"])]
    nomap = ew.source.isin(["inner_london", "none"])
    for i, c in enumerate(GREENS):
        sub = ew[(ew.cls == i) & ~nomap]
        if len(sub):
            sub.plot(ax=ax, color=c, edgecolor=edge, linewidth=lw, zorder=2)
    import matplotlib as mpl
    with mpl.rc_context({"hatch.linewidth": hatch_lw, "hatch.color": NOMAP_HATCH}):
        ew[nomap].plot(ax=ax, color=NOMAP, edgecolor=NOMAP_HATCH, linewidth=lw, hatch="/////", zorder=2)
    g[g.code == RV].plot(ax=ax, facecolor="none", edgecolor=RUST, linewidth=rv_lw, zorder=5)
    ax.set_aspect(1); ax.axis("off")


def legend_handles(include_nomap=True, include_grey=True, include_rv=True):
    h = [Patch(facecolor=c, edgecolor="none", label=l) for c, l in zip(GREENS, BIN_LABELS)]
    if include_nomap:
        h.append(Patch(facecolor=NOMAP, edgecolor=NOMAP_HATCH, hatch="/////", label="no definitive map"))
    if include_grey:
        h.append(Patch(facecolor=GREY, edgecolor="none", label="not comparable"))
    if include_rv:
        h.append(Patch(facecolor="none", edgecolor=RUST, linewidth=1.6, label="Ribble Valley"))
    return h


def rep_point(g, code):
    p = g[g.code == code].geometry.representative_point().iloc[0]
    return p.x, p.y


def style_axis(a, size=9.6):
    for t in a.get_xticklabels() + a.get_yticklabels():
        t.set_family(MONO); t.set_fontsize(size); t.set_color(MUT)
    a.tick_params(length=0)
    for sp in a.spines.values():
        sp.set_visible(False)
