"""img/fig1.png (1600 x 2000): rights of way per square mile by council area, top 10 labelled, Ribble Valley marked."""
from common import *
from matplotlib.patches import Rectangle, ConnectionPatch

g = load_geo(200)
fig = plt.figure(figsize=(8, 9), dpi=200, facecolor=BGC)
words(fig, 0.05, 0.975, [("Where are Britain's", FG), ("footpaths?", GREENS[4])], size=25, gap=0.012)
fig.text(0.05, 0.915, "Miles of public right of way (footpaths, bridleways and byways) per square mile of land,\n"
         f"by council area, England and Wales. Average {fmt1(N['avg'])}; {N['top_name']} is top at {fmt1(N['top_val'])}.",
         family=SER, fontsize=10.5, color=FG, va="top", linespacing=1.25)

ax = fig.add_axes([0.0, 0.1, 0.63, 0.75]); ax.set_facecolor(BGC); ax.set_anchor("N")
draw_map(ax, g, lw=0.2, rv_lw=1.3)
ax.set_xlim(-10, 665); ax.set_ylim(5, 690)

X0, X1, Y0, Y1 = 350, 424, 396, 466
ax.add_patch(Rectangle((X0, Y0), X1 - X0, Y1 - Y0, fill=False, ec=FG, lw=0.9, zorder=6))
ax.text(X1 + 6, Y1 - 4, "inset", family=MONO, fontsize=7.4, color=FG, va="top", path_effects=halo(2.5), zorder=8)

def note(a, txt, xy, xyt, ha="left", size=7.6):
    a.annotate(txt, xy=xy, xytext=xyt, family=MONO, fontsize=size, color=FG, ha=ha, va="center", zorder=8,
               arrowprops=dict(arrowstyle="-", color=FG, lw=.6, shrinkB=2), path_effects=halo(2.5))

top10 = TOP.head(10)
mal = top10[top10.name == "Malvern Hills"].iloc[0]
note(ax, f"{int(mal.rank_sqmi)} {mal['name']}\n{fmt1(mal.prow_per_sqmi)} per sq mile", rep_point(g, mal.code), (190, 130), ha="center")
note(ax, "inner London:\nno definitive map", rep_point(g, "E09000033"), (575, 45), ha="center")
fig.text(0.05, 0.255, "Grey: not comparable. Scotland has a right of responsible access\nto most land instead of a rights-of-way network like England's;\nNorthern Ireland has very few recorded rights of way.", family=MONO, fontsize=7.2, color=MUT, va="top", linespacing=1.4)

fig.text(0.65, 0.835, "MILES PER SQUARE MILE", family=MONO, fontsize=8.3, color=MUT)
fig.legend(handles=legend_handles(), loc="upper left", bbox_to_anchor=(0.645, 0.83), frameon=False,
           prop={"family": MONO, "size": 8.1}, labelcolor=FG, handlelength=1.6, handleheight=1.0, labelspacing=0.4)

ia = fig.add_axes([0.65, 0.315, 0.33, 0.28]); ia.set_facecolor(BGC)
draw_map(ia, g, lw=0.6, rv_lw=2.2)
ia.set_xlim(X0, X1); ia.set_ylim(Y0, Y1)
ia.axis("on"); ia.set_xticks([]); ia.set_yticks([]); ia.set_xlabel(""); ia.set_ylabel("")
for sp in ia.spines.values():
    sp.set_visible(True); sp.set_color(FG); sp.set_linewidth(0.9)
fig.text(0.65, 0.605, "INSET: THE SOUTH PENNINES", family=MONO, fontsize=8.3, color=MUT)
for _, r in top10.iterrows():
    if r.code == mal.code:
        continue
    x, y = rep_point(g, r.code)
    ia.text(x, y, f"{int(r.rank_sqmi)}", fontproperties=DISP, fontsize=11, color="white", ha="center", va="center", zorder=9,
            path_effects=[pe.withStroke(linewidth=2.2, foreground=GREENS[5])])
x, y = rep_point(g, RV)
ia.text(x + 1, y - 1, f"Ribble Valley\n{ordinal(N['rv_rank'])}, {fmt1(N['rv_val'])}", family=MONO, fontsize=8, color=RUST,
        ha="center", va="center", zorder=9, path_effects=halo(3))

fig.text(0.65, 0.29, "TOP 10, MILES PER SQUARE MILE", family=MONO, fontsize=8.3, color=MUT, va="top")
rows = [f"{int(r.rank_sqmi):>2} {r['name']:<22}{fmt1(r.prow_per_sqmi)}" for _, r in top10.iterrows()]
fig.text(0.65, 0.27, "\n".join(rows), family=MONO, fontsize=7.2, color=FG, va="top", linespacing=1.32)

fig.text(0.05, 0.06, f"Data: councils' rights of way open data via rowmaps.com (OGL v3; contains OS data © Crown copyright and database\n"
         f"right 2026); OpenStreetMap contributors via ohsome (ODbL) for {N['n_osm']} councils with no open data; ONS boundaries Dec 2024 (OGL v3).\n"
         "Dr Tristan Hotham · Independent researcher", family=MONO, fontsize=6.3, color=MUT, va="top", linespacing=1.4)
fig.savefig(P("img/fig1.png"), dpi=200, facecolor=BGC)
print("fig1", [(r['name'], round(r.prow_per_sqmi, 1)) for _, r in top10.iterrows()], N["rv_rank"], round(N["rv_val"], 1))
