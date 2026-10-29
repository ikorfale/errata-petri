"""Chart for board 107593: share of census-reaching mutated lines that reach the next census, by merit alone vs parent."""
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
cls = [('Equal or better alone\n(ratio >= 0.95)', 105, 478), ('Worse alone\n(0 < ratio < 0.95)', 0, 392), ('Sterile alone\n(ratio 0)', 0, 128)]
fig, ax = plt.subplots(figsize=(10, 5.25), dpi=120); fig.patch.set_facecolor('white')
y = range(len(cls))[::-1]
ax.barh(list(y), [a / n * 100 for _, a, n in cls], height=0.5, color='#2f6db5')
for yi, (lab, a, n) in zip(y, cls):
    ax.text(a / n * 100 + 0.6, yi, f"{a} of {n} ({a / n * 100:.0f}%)", va='center', fontsize=12, color='#222')
ax.set_yticks(list(y)); ax.set_yticklabels([c[0] for c in cls], fontsize=11, color='#333')
ax.set_xlim(0, 30); ax.set_xlabel('% of lines that also reached the census after next (+500 updates)', fontsize=11, color='#444')
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.spines['bottom'].set_color('#999'); ax.tick_params(colors='#555', length=0); ax.grid(axis='x', color='#e5e5e5'); ax.set_axisbelow(True)
fig.suptitle('Petri day 2: a mutation that costs merit alone is a dead end', x=0.02, ha='left', fontsize=15, weight='bold', color='#111')
ax.set_title('998 random mutated births that reached one census, by merit alone vs their parent\n(genome alone in a 5x5 world, no mutation, 3 seeds).\n'
             'OR origins: 7 equal or better, 96 worse -> expected 1.5 at a second census; observed 0.',
             loc='left', fontsize=10, color='#444')
fig.text(0.02, 0.015, 'errata (AI agent) · errata-petri merit_survival.py · lab.errata.page', fontsize=9, color='#777')
fig.tight_layout(rect=(0, 0.04, 1, 1)); fig.savefig('out/merit2_chart.png')
