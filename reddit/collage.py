"""r/dataisbeautiful collage: footpath_capital_of_britain.png (2400 x 3000), in the house collage style.
Every number is read from ../results/footpaths_by_council.csv and ../results/summary.json, or computed from them.
Run: python3 collage.py
"""
import os, sys
OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(OUT), "graphics"))
from common import *
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

g = load_geo(250)
top10 = TOP.head(10)
pennine = [c for c in top10.code if c != "E07000235"]          # all but Malvern Hills sit in the South Pennines
assert len(pennine) == 9
yrs = sorted(N["osm_years"]); osm = [N["osm_years"][y] for y in yrs]

fig = new_fig()
words(fig, 0.045, 0.972, [("Which part of Britain has", FG)])
words(fig, 0.045, 0.924, [("the", FG), ("most footpaths?", GREENS[4])])
fig.text(0.045, 0.862, "Miles of public right of way (footpaths, bridleways and byways) per square mile of land, by council area.\n"
         f"Councils' own open data for England and Wales, with OpenStreetMap for the {N['n_osm']} councils that publish none.",
         family=SER, fontsize=14.5, color=FG, va="top", linespacing=1.15)

ax = fig.add_axes([0.0, 0.25, 0.6, 0.575]); ax.set_facecolor(BGC)
draw_map(ax, g, lw=0.3, rv_lw=2.4, hatch_lw=0.5)
ax.set_xlim(130, 660); ax.set_ylim(5, 665)


def note(txt, xy, xyt, ha="left", col=FG):
    ax.annotate(txt, xy=xy, xytext=xyt, family=MONO, fontsize=10.2, color=col, ha=ha, va="center", zorder=8,
                arrowprops=dict(arrowstyle="-", color=col, lw=.8, shrinkB=4), path_effects=halo(3))


r1 = TOP.iloc[0]
note(f"{r1['name']}: {fmt1(r1.prow_per_sqmi)}", rep_point(g, r1.code), (470, 470))
ax.text(470, 452, "and eight neighbours in the\nSouth Pennines: 9 of the\ntop 10 council areas",
        family=MONO, fontsize=10.2, color=FG, va="top", zorder=8, path_effects=halo(3), linespacing=1.3)
note(f"Ribble Valley: {fmt1(N['rv_val'])}", rep_point(g, RV), (225, 520), ha="center", col=RUST)
mal = TOP[TOP.code == "E07000235"].iloc[0]
note(f"{mal['name']}: {fmt1(mal.prow_per_sqmi)}", rep_point(g, mal.code), (215, 330), ha="center")
note("inner London:\nno definitive map", rep_point(g, "E09000033"), (590, 60), ha="center")

# key: a horizontal scale for the greens, then the three special cases
fig.text(0.62, 0.8, "MILES PER SQUARE MILE", family=MONO, fontsize=11, color=MUT)
kx, ky, kw = 0.627, 0.77, 0.052
for i, c in enumerate(GREENS):
    fig.patches.append(Rectangle((kx + i * kw, ky), kw, 0.016, color=c, transform=fig.transFigure, figure=fig))
for i, t in enumerate(["0", "1", "2", "3", "4", "5", fmt1(N["top_val"])]):
    fig.text(kx + i * kw, ky - 0.004, t, family=MONO, fontsize=10, color=MUT, ha="center", va="top")
yy = 0.733
def swatch(y, fc, ec="none", hatch=None, lw=0):
    with plt.rc_context({"hatch.color": NOMAP_HATCH, "hatch.linewidth": 0.6}):
        fig.patches.append(Rectangle((0.627, y - 0.0075), 0.02, 0.015, facecolor=fc, edgecolor=ec, hatch=hatch, lw=lw,
                                     transform=fig.transFigure, figure=fig))
swatch(yy, NOMAP, NOMAP_HATCH, "/////", 0.8)
fig.text(0.656, yy, "no definitive map: inner London,\nIsles of Scilly", family=MONO, fontsize=10.5, color=FG, va="center", linespacing=1.15); yy -= 0.028
swatch(yy, GREY)
fig.text(0.656, yy, "Scotland, Northern Ireland: not\ncomparable (see footnote)", family=MONO, fontsize=10.5, color=FG,
         va="center", linespacing=1.15); yy -= 0.026
swatch(yy, "none", RUST, None, 2.4)
fig.text(0.656, yy, "Ribble Valley", family=MONO, fontsize=10.5, color=FG, va="center")

items = [
    (fmt1(N["top_val"]), GREENS[5],
     f"miles of right of way per square mile in\n{N['top_name']}, top of {N['n_councils']} council areas.\n"
     "The South Pennine mill-town belt leads."),
    (fmt1(N["avg"]), GREENS[3],
     f"miles per square mile across England and\nWales: {N['total']:,.0f} miles of path in all."),
    (ordinal(N["rv_road"]), RUST,
     f"Ribble Valley per mile of road, and {ordinal(N['rv_head'])} per\nresident, but {ordinal(N['rv_rank'])} per square mile "
     f"({fmt1(N['rv_val'])}).\n{N['road_top']} is top on both."),
    (f"{N['osm_share'] * 100:.0f}%", GREENS[4],
     f"of the councils' path length is mapped in\nOpenStreetMap: {osm[-1]:,.0f} miles in {yrs[-1]}, up\n"
     f"from {osm[0]:,.0f} in {yrs[0]}."),
]
assert N["road_top"] == N["head_top"]
headlines(fig, [0.62, 0.245, 0.37, 0.41], items, big=34, step=0.25, sub_off=0.09)

# bottom: top 10 and OSM by year
label(fig, 0.045, 0.232, "TOP 10 COUNCIL AREAS, MILES PER SQUARE MILE")
a = fig.add_axes([0.22, 0.094, 0.29, 0.128]); a.set_facecolor(BGC)
names = list(top10.name) + ["Ribble Valley"]
vals = list(top10.prow_per_sqmi) + [N["rv_val"]]
ys = list(range(10)) + [10.8]
a.barh(ys, vals, color=[GREENS[4]] * 10 + [RUST], height=0.72)
for y, v, c in zip(ys, vals, [FG] * 10 + [RUST]):
    a.text(v + 0.12, y, fmt1(v), family=MONO, fontsize=9.6, color=c, va="center")
a.axvline(N["avg"], color=FG, lw=1, ls=(0, (3, 2)))
a.text(N["avg"] + 0.1, 11.9, f"average {fmt1(N['avg'])}", family=MONO, fontsize=9.6, color=FG, va="center")
a.set_yticks(ys, [n.replace("Blackburn with Darwen", "Blackburn w. Darwen") for n in names])
a.set_ylim(12.5, -0.6); a.set_xlim(0, 8.8); a.set_xticks([])
style_axis(a)
for t in a.get_yticklabels():
    t.set_color(FG)
a.get_yticklabels()[-1].set_color(RUST)

label(fig, 0.57, 0.232, "MILES OF RIGHT OF WAY MAPPED IN OPENSTREETMAP")
b = fig.add_axes([0.62, 0.104, 0.34, 0.112]); b.set_facecolor(BGC)
b.bar(yrs, [v / 1000 for v in osm], width=1.3, color=GREENS[3])
for y, v in zip(yrs, osm):
    b.text(y, v / 1000 + 3, f"{v / 1000:.0f}k", family=MONO, fontsize=9.6, color=FG, ha="center", va="bottom")
tot = N["total"] / 1000
b.axhline(tot, color=FG, lw=1, ls=(0, (3, 2)))
b.text(yrs[0] - 1, tot + 4, f"all rights of way in this study: {N['total']:,.0f} miles", family=MONO, fontsize=9.6,
       color=FG, va="bottom")
b.set_ylim(0, 165); b.set_xlim(yrs[0] - 1.2, yrs[-1] + 1.2)
b.set_xticks(yrs, [str(y) for y in yrs]); b.set_yticks([0, 50, 100], ["0", "50k", "100k"])
style_axis(b)
b.grid(axis="y", color="#DDD6C8", lw=.6); b.set_axisbelow(True)
b.axhline(0, color=FG, lw=.8)

footer(fig, "Data: councils' rights of way open data via rowmaps.com (OGL v3; contains OS data © Crown copyright and database right\n"
       "2026); OpenStreetMap contributors via ohsome (ODbL); ONS boundaries Dec 2024, mid-2025 population (OGL v3). Scotland has a right\n"
       "of responsible access to most land; Northern Ireland has very few recorded rights of way. Analysis and chart: Tristan Hotham,\n"
       "with Python and matplotlib.", y=0.07)
fig.savefig(os.path.join(OUT, "footpath_capital_of_britain.png"), dpi=200, facecolor=BGC)
print("collage", round(N["top_val"], 1), round(N["avg"], 1), round(N["total"]), N["rv_road"], N["rv_head"], N["rv_rank"],
      round(N["rv_val"], 1), N["osm_share"], osm[0], osm[-1], [(n, round(v, 1)) for n, v in zip(names, vals)])
