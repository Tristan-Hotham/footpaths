"""img/fig2.png (1600 x 1200): top 20 council areas per square mile (with the England and Wales average), and
OpenStreetMap miles of right of way mapped by year against the council total."""
from common import *

fig = plt.figure(figsize=(8, 6), dpi=200, facecolor=BGC)
words(fig, 0.05, 0.965, [("The", FG), ("footpath capital", GREENS[4]), ("is Rossendale", FG)], size=21, gap=0.01)
fig.text(0.05, 0.885, "Miles of public right of way per square mile of land: the top 20 council areas in England and Wales,\n"
         "and how much of the network volunteers have mapped in OpenStreetMap.", family=SER, fontsize=9.6, color=FG, va="top",
         linespacing=1.25)

# ---- league ----
fig.text(0.05, 0.79, "TOP 20, MILES PER SQUARE MILE", family=MONO, fontsize=7.6, color=MUT)
a = fig.add_axes([0.25, 0.115, 0.33, 0.655]); a.set_facecolor(BGC)
t20 = TOP.head(20)
names = [f"{int(r.rank_sqmi)}. {r['name']}" for _, r in t20.iterrows()]
vals = list(t20.prow_per_sqmi)
cols = [GREENS[4]] * len(vals)
ys = list(range(len(vals)))
a.barh(ys, vals, color=cols, height=0.72)
for y, v in zip(ys, vals):
    a.text(v + 0.1, y, fmt1(v), family=MONO, fontsize=7, color=FG, va="center")
a.set_yticks(ys, names)
a.set_xlim(0, 8.6); a.set_xticks([0, 2, 4, 6, 8])
style_axis(a, 7.2)
for t in a.get_yticklabels():
    t.set_color(FG)
a.axvline(N["avg"], color=FG, lw=0.9, ls=(0, (3, 2)), zorder=3)
a.text(N["avg"] + 0.08, len(vals) + 0.1, f"England and Wales average {fmt1(N['avg'])}", family=MONO, fontsize=6.6, color=FG,
       va="top")
a.set_ylim(len(vals) + 1.4, -0.7)

# ---- OSM by year ----
yrs = sorted(N["osm_years"])
osm = [N["osm_years"][y] for y in yrs]
fig.text(0.66, 0.79, "MILES MAPPED IN OPENSTREETMAP", family=MONO, fontsize=7.6, color=MUT)
b = fig.add_axes([0.70, 0.30, 0.27, 0.45]); b.set_facecolor(BGC)
b.bar(yrs, [v / 1000 for v in osm], width=1.3, color=GREENS[3])
for y, v in zip(yrs, osm):
    b.text(y, v / 1000 + 2, f"{v / 1000:.0f}k", family=MONO, fontsize=6.8, color=FG, ha="center", va="bottom")
tot = N["total"] / 1000
b.axhline(tot, color=FG, lw=0.9, ls=(0, (3, 2)))
b.text(yrs[0] - 1, tot - 5, f"all rights of way in the\nstudy: {N['total']:,.0f} miles", family=MONO, fontsize=6.6, color=FG,
       va="top")
b.set_ylim(0, 150); b.set_xlim(yrs[0] - 1.2, yrs[-1] + 1.2)
b.set_xticks(yrs, [str(y) for y in yrs]); b.set_yticks([0, 50, 100], ["0", "50k", "100k"])
style_axis(b, 7)
b.grid(axis="y", color="#DDD6C8", lw=.6); b.set_axisbelow(True)
b.axhline(0, color=FG, lw=.8)
fig.text(0.66, 0.235, f"OpenStreetMap has {N['osm_share'] * 100:.0f}% of the length in\ncouncils' own data, up from "
         f"{osm[0]:,.0f}\nmiles in {yrs[0]} to {osm[-1]:,.0f} in {yrs[-1]}.", family=SER, fontsize=8.2, color=FG, va="top",
         linespacing=1.25)

fig.text(0.05, 0.06, "Data: councils' rights of way open data via rowmaps.com (OGL v3; contains OS data © Crown copyright and database right 2026);\n"
         "OpenStreetMap contributors via ohsome (ODbL); ONS boundaries Dec 2024 (OGL v3). Dr Tristan Hotham · Independent researcher",
         family=MONO, fontsize=5.9, color=MUT, va="top", linespacing=1.4)
fig.savefig(P("img/fig2.png"), dpi=200, facecolor=BGC)
print("fig2", [(n, round(v, 1)) for n, v in zip(names, vals)], osm, N["total"])
