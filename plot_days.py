"""Two days of the Petri long world in one picture: share of the population performing each logic task at every census
(heatmap, blue = more), median genome length, and censuses flagged as sweeps (depth-4 coalescence >= 0.5, day 2 only:
lineage.jsonl starts at day 2). Reads daily/series.jsonl and daily/lineage.jsonl. Writes out/petri-days.png."""
import json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
S = [json.loads(l) for l in open("daily/series.jsonl")]
L = [json.loads(l) for l in open("daily/lineage.jsonl")]
T = ["NOT", "NAND", "AND", "ORN", "OR", "ANDN", "NOR", "XOR", "EQU"]
u = np.array([s["update"] for s in S]) / 1000
M = np.array([[s["tasks_now"][t] / s["pop"] for s in S] for t in T])
sweeps = [r["update"] / 1000 for r in L if len(r["coal"]) >= 4 and r["coal"][3] >= 0.5]
ink, mute, grid = "#2b2b29", "#6b6b66", "#e4e3df"
cmap = LinearSegmentedColormap.from_list("b", ["#fcfcfb", "#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "text.color": ink, "axes.labelcolor": mute,
                     "xtick.color": mute, "ytick.color": mute, "axes.edgecolor": grid})
fig, (a, b) = plt.subplots(2, 1, figsize=(12, 6.3), sharex=True, gridspec_kw={"height_ratios": [3, 1.2], "hspace": 0.08})
fig.patch.set_facecolor("#fcfcfb")
du = u[1] - u[0]
im = a.imshow(M, aspect="auto", cmap=cmap, vmin=0, vmax=1, interpolation="nearest",
              extent=[u[0] - du / 2, u[-1] + du / 2, len(T) - 0.5, -0.5])
a.set_yticks(range(len(T))); a.set_yticklabels(T)
for x in sweeps: a.plot([x, x], [-0.5, len(T) - 0.5], color="#c2452d", lw=1, alpha=0.8)
a.axvline(40, color=ink, lw=1, ls=(0, (3, 3)))
a.text(20, -0.9, "day 1", ha="center", color=mute); a.text(60, -0.9, "day 2", ha="center", color=mute)
cb = fig.colorbar(im, ax=[a, b], fraction=0.025, pad=0.01, ticks=[0, .25, .5, .75, 1])
cb.ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"]); cb.set_label("share of organisms doing the task")
cb.outline.set_visible(False)
b.plot(u, [s["median_len"] for s in S], color="#2a78d6", lw=2)
for x in sweeps: b.axvline(x, color="#c2452d", lw=1, alpha=0.8)
b.axvline(40, color=ink, lw=1, ls=(0, (3, 3)))
b.set_ylabel("median genome\nlength"); b.set_xlabel("update (thousands)")
b.grid(axis="y", color=grid, lw=0.8); b.set_facecolor("#fcfcfb")
for s in ("top", "right"): b.spines[s].set_visible(False)
a.set_title("Petri long world, days 1–2: which logic tasks the population performs\n"
            "red lines: censuses where one recent ancestor took over (sweep flag, tracked from day 2)",
            loc="left", fontsize=11.5, pad=20)
fig.text(0.01, 0.005, "errata.page · github.com/ikorfale/errata-petri · real simulation data, 160 censuses every 500 updates",
         color=mute, fontsize=8)
fig.savefig("out/petri-days.png", dpi=130, bbox_inches="tight", facecolor="#fcfcfb")
print("censuses", len(S), "sweep flags", sweeps)
print("end shares", {t: round(M[i, -1], 2) for i, t in enumerate(T)}, "len", S[0]["median_len"], "->", S[-1]["median_len"])
