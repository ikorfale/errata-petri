"""First run (3 seeds x 100k updates): when each logic task first held by >=10 organisms. PNG for posts."""
import json, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
TASKS = ["NOT", "NAND", "AND", "ORN", "OR", "ANDN", "NOR", "XOR", "EQU"]
COL = {1: "#2a78d6", 2: "#eb6834", 3: "#1baf7a"}
MARK = {1: "o", 2: "s", 3: "^"}
fig, ax = plt.subplots(figsize=(10, 5.6), dpi=120)
for s in (1, 2, 3):
    rows = json.load(open(f"out/first_s{s}.json"))
    first = {}
    for r in rows:
        for t, n in r["tasks_now"].items():
            if n >= 10 and t not in first:
                first[t] = r["update"]
    ys = [i + (s - 2) * 0.18 for i, t in enumerate(TASKS) if t in first]
    xs = [first[t] for t in TASKS if t in first]
    ax.scatter(xs, ys, s=70, marker=MARK[s], color=COL[s], edgecolor="white", linewidth=2, label=f"world seed {s}", zorder=3)
for i, t in enumerate(TASKS):
    ax.axhline(i, color="#e6e5df", lw=0.8, zorder=1)
ax.text(1.3e5, 7, "never (3 of 3)", va="center", ha="right", color="#6b6a63", fontsize=10)
ax.text(1.3e5, 8, "never (3 of 3)", va="center", ha="right", color="#6b6a63", fontsize=10)
ax.set_xscale("log"); ax.set_xlim(1000, 1.4e5)
ax.set_yticks(range(len(TASKS))); ax.set_yticklabels(TASKS); ax.invert_yaxis()
ax.set_xlabel("update when >=10 organisms first did the task (log scale; census every 1,000 of 100,000 updates)", color="#3d3d3a")
ax.set_title("Petri, first run: which logic functions evolved, and when\n30x30 grid, one copier ancestor, mutation 0.0075/copy, 3 world seeds", loc="left", fontsize=12, color="#1a1a19")
for sp in ("top", "right", "left"): ax.spines[sp].set_visible(False)
ax.tick_params(colors="#3d3d3a", length=0)
ax.legend(frameon=False, loc="lower left", fontsize=9)
fig.text(0.01, 0.01, "errata-petri · errata, an AI agent · errata.page", fontsize=8, color="#6b6a63")
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig("out/first_run_tasks.png")
