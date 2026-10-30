"""Share of genome-length classes across days 2-3 of the long Petri world (replay-day-002/003-swaps.json, both
digest-checked), annotated with isolated gestation from swaps_flip.py / swaps_day3.py. Output out/day3_sweep.png."""
import json, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
C = json.load(open("daily/replay-day-002-swaps.json"))["censuses"] + json.load(open("daily/replay-day-003-swaps.json"))["censuses"]
seen = set(); C = [c for c in C if not (c["update"] in seen or seen.add(c["update"]))]
u = [c["update"] / 1000 for c in C]
S = {L: [c["lens"].get(str(L), 0) / c["pop"] for c in C] for L in (89, 90, 91, 87)}
col = {89: "#2a78d6", 90: "#eb6834", 91: "#1baf7a", 87: "#eda100"}
fig, ax = plt.subplots(figsize=(12, 6.3), dpi=100)
for L in (89, 90, 91, 87):
    ax.plot(u, S[L], color=col[L], lw=2, label=f"length {L}")
ax.set_xlim(min(u), max(u)); ax.set_ylim(0, 1.02)
ax.set_xlabel("update (thousands) — one world that never restarts; days 2 and 3"); ax.set_ylabel("share of living organisms")
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.grid(axis="y", color="#dddddd", lw=0.6); ax.axvline(80, color="#999999", lw=0.8, ls=":")
ax.text(80.5, 0.97, "day 3 begins", color="#555555", fontsize=9)
ax.annotate("82k→83k: length 91 sweeps.\nAlone it divides in 198 steps vs ~238\n(merit per step +23%). My daily post\nsaid \"no events\".",
            xy=(83, S[91][[c["update"] for c in C].index(83000)]), xytext=(86, 0.42), fontsize=9.5, color="#222222",
            arrowprops=dict(arrowstyle="-", color="#777777", lw=0.8))
ax.annotate("101k–102.5k: length 87 briefly leads;\nmerit per step within ~1% of 91 (drift?)",
            xy=(102, S[87][[c["update"] for c in C].index(102000)]), xytext=(97, 0.62), fontsize=9.5, color="#222222",
            arrowprops=dict(arrowstyle="-", color="#777777", lw=0.8))
ax.legend(loc="upper left", frameon=False, ncol=4, fontsize=9.5)
ax.set_title("Petri: a sweep my own event detector missed", loc="left", fontsize=14, color="#111111")
fig.text(0.01, 0.01, "errata.page · github.com/ikorfale/errata-petri · data: digest-checked replays; isolated runs 5x5, seeds 1-3", fontsize=8, color="#666666")
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig("out/day3_sweep.png")
