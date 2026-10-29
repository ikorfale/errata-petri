# Guess before the merit-vs-survival split (29.10 ~10:20 UTC, written before out/origin_genomes_day2_r2.json exists)

Context: out/origin_merit_day2.txt (b861b5c). Origins and census-reaching mutated births both have median merit ratio 0.50;
origins are almost never neutral (7/103 equal-or-better vs 176/398). Question: does merit alone predict whether a
census-reaching mutated line also reaches the census after that (next_census + 500)? Baseline enlarged to 1000 (same random
order, so the first 400 are the old sample; check: their ratios must reproduce out/origin_merit_day2.txt).

N1. Equal-or-better (ratio >= 0.95) lines reach the second census more often than worse (< 0.95) lines; my guess ~40% vs ~20%.
N2. Sterile-alone lines (ratio 0) almost never reach it (< 5%).
N3. Weighting the class rates by the origins' mix (7 neutral, 96 worse) gives an expected count of origins at a second census
    clearly below the unweighted expectation (~6.3), i.e. merit explains part of the deficit, not necessarily all.
Falsifier for "merit predicts the deficit": neutral rate <= worse rate, or the 95% interval of the difference includes 0.
