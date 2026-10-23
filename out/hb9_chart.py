"""Chart for the lab page: the 9-insertion route 'ycuopcuyq' (before parent position 84), one prefix at a time.
Reads out/hb9_prefixes.txt (hb9_prefixes.py). Bar = merit proxy relative to the parent (log scale); blue = tasks of the
parent, orange = AND credited too. Writes out/hb9_route.png (--dark: out/hb9_route_dark.png)."""
import re, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
rows = []
for l in open("out/hb9_prefixes.txt"):
    m = re.match(r"k=(\d) \+(\S*)\s+len (\d+) mod3 (\d) instr/gest\s+(\d+) tasks (\S+)\s+rel.rate\s+([\d.]+)\s+solo pop, parent-identical: (.*)", l)
    if m: k, ins, ln, md, ig, t, r, pop = m.groups(); rows.append((int(k), ins, int(md), int(ig), "AND" in t.split(","), float(r), [int(a) for a in re.findall(r"\((\d+),", pop)]))
DARK = "--dark" in __import__("sys").argv  # dark variant for lab.errata.page
BLUE, ORANGE, INK, MUTED, SURF = ("#3987e5", "#d95926", "#dbe7e3", "#7f948f", "#0a1110") if DARK else ("#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#fcfcfb")
fig, ax = plt.subplots(figsize=(10, 5.2), facecolor=SURF); ax.set_facecolor(SURF)
for k, ins, md, ig, has_and, r, pop in rows:
    ax.bar(k, max(r, 0.005), width=0.62, color=ORANGE if has_and else BLUE, edgecolor=SURF, linewidth=2)
    lab = f"{r:.2f}" if r >= 0.1 else "0.01\nstalls"
    ax.text(k, max(r, 0.005) * 1.15, lab, ha="center", va="bottom", fontsize=9, color=INK)
ax.set_yscale("log"); ax.set_ylim(0.005, 12); ax.axhline(1, color=MUTED, lw=1, ls=(0, (4, 3)))
ax.set_xticks([r[0] for r in rows]); ax.set_xticklabels([(("+" + r[1]) if r[1] else "parent") + f"\nlen%3={r[2]}\npop {round(sum(r[6]) / 3)}" for r in rows], fontsize=8, family="monospace")
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.spines["left"].set_color(MUTED); ax.spines["bottom"].set_color(MUTED); ax.tick_params(colors=MUTED)
ax.set_ylabel("replication rate vs parent (log; length x 2^bonus / gestation)", color=INK, fontsize=9)
ax.set_title("Petri: the 9-letter route to a five-task replicator, one insertion at a time", color=INK, fontsize=12, loc="left")
from matplotlib.patches import Patch
leg = ax.legend(labelcolor=INK, handles=[Patch(color=BLUE, label="4 tasks (parent's)"), Patch(color=ORANGE, label="AND credited too"), plt.Line2D([], [], color=MUTED, lw=1, ls=(0, (4, 3)), label="parent rate")], frameon=False, loc="upper left", fontsize=9)
fig.text(0.01, 0.01, "Only lengths with the parent's length mod 3 replicate well: the route is passable in three steps of three, not letter by letter.\n"
         "pop = mean solo population after 150 updates (3 seeds), all parent-identical. Data: out/hb9_prefixes.txt, errata-petri.", fontsize=7.5, color=MUTED)
fig.subplots_adjust(bottom=0.25, top=0.9, left=0.08, right=0.98)
fig.savefig("out/hb9_route_dark.png" if DARK else "out/hb9_route.png", dpi=130, facecolor=SURF)
