"""img/header.png (1200 x 630) social card, also copied to ../header.png for the web page."""
import shutil
from common import *

g = load_geo(400)
fig = plt.figure(figsize=(6, 3.15), dpi=200, facecolor=BGC)
words(fig, 0.05, 0.93, [("Where are", FG)], size=21)
words(fig, 0.05, 0.80, [("Britain's", FG), ("footpaths?", GREENS[4])], size=21, gap=0.012)
fig.text(0.05, 0.635, "Miles of public right of way per square mile\nof land, by council area, England and Wales",
         family=SER, fontsize=7.4, color=FG, va="top", linespacing=1.25)
# horizontal key
kx, ky, kw = 0.05, 0.445, 0.05
for i, c in enumerate(GREENS):
    fig.patches.append(plt.Rectangle((kx + i * kw, ky), kw, 0.03, color=c, transform=fig.transFigure, figure=fig))
for i, t in enumerate(["0", "1", "2", "3", "4", "5", ""]):
    fig.text(kx + i * kw, ky - 0.012, t, family=MONO, fontsize=4.8, color=MUT, ha="center", va="top")
fig.text(kx + 6 * kw + 0.012, ky + 0.015, "miles per\nsquare mile", family=MONO, fontsize=4.8, color=MUT, va="center",
         linespacing=1.1)

fig.text(0.05, 0.36, fmt1(N["top_val"]), fontproperties=DISP, fontsize=24, color=GREENS[5], va="top")
fig.text(0.05, 0.24, f"{N['top_name']}, the\nfootpath capital", family=SER, fontsize=6.8, color=FG, va="top", linespacing=1.15)
fig.text(0.27, 0.36, fmt1(N["avg"]), fontproperties=DISP, fontsize=24, color=GREENS[3], va="top")
fig.text(0.27, 0.24, "England and Wales\naverage", family=SER, fontsize=6.8, color=FG, va="top", linespacing=1.15)
fig.text(0.05, 0.055, "Dr Tristan Hotham · Independent researcher", family=MONO, fontsize=5.4, color=MUT, va="bottom")

ax = fig.add_axes([0.56, 0.02, 0.43, 0.96]); ax.set_facecolor(BGC)
draw_map(ax, g, lw=0.12, rv_lw=0, hatch_lw=0.25)
ax.set_xlim(150, 660); ax.set_ylim(5, 670)
x, y = rep_point(g, "E07000125")
ax.annotate(N["top_name"], xy=(x, y), xytext=(500, 560), family=MONO, fontsize=6, color=FG, ha="left", va="center",
            arrowprops=dict(arrowstyle="-", color=FG, lw=.5, shrinkB=1), path_effects=halo(2), zorder=9)
fig.savefig(P("img/header.png"), dpi=200, facecolor=BGC)
shutil.copyfile(P("img/header.png"), P("header.png"))
print("header", round(N["top_val"], 1), round(N["avg"], 1))
