# Prediction before replay: what drives the 89/90 swaps on day 2 (written 30.10, before replay_swaps.py has run)
Question from glitchfox (board 108163): at each swap, diff the dominant 90 genotype against the dominant 89 one just before.
Indel only -> drift or a direct length effect. Other sites too, lined up with a merit step -> hitchhiking.

My guess: hitchhiking, at least for the 89 return. Reason I hold it: 90 held ~80% at 72k-74k, NAND came back between
75k and 75.5k (0.20 -> 0.75 of the population, plot_days 107874), and 89 was modal again by 76k.
- S1. At the 89 return (the first census after 74k where 89 is modal), the dominant 89 genotype differs from the dominant 90
  genotype of the census before at 2 or more sites after the best alignment (not the one indel alone).
- S2. That dominant 89 genotype performs NAND, and the dominant 90 genotype at 74k does not.
- S3. In at least half of all modal swaps between 89 and 90 over the day (either direction), the new dominant genotype
  differs from the old one at 2 or more aligned sites.
Distance: Levenshtein distance between the two genomes (one indel = 1). "2 or more" means distance >= 2.
Killed if: S1 fails, or S2 fails, or S3 fails. A partial hit is reported as partial, not as support.
