# Headlines from local runs (2026-08-16)

Source files in the working store; compact copies live next to this file when uploaded.

## streams_run16 — isolation / rescue

All 16 seeds `base ≈ 1.0`. `keep_only` is chance (~1.8%) on every seed.

| seed | keep_all | max_single_drop | cancel_drop | best_pair_rec |
|-----:|---------:|----------------:|------------:|--------------:|
| 0 | 0.9671 | 0.0000 | 0.0288 | 0.0286 |
| 1 | 1.0000 | 0.0373 | 0.0283 | 0.0230 |
| 2 | 0.8785 | 0.0129 | 0.1055 | 0.0863 |
| 3 | 0.8919 | 0.0026 | 0.0829 | 0.0741 |
| 4 | 0.9998 | 0.0022 | 0.1005 | 0.1005 |
| 5 | 1.0000 | 0.0274 | 0.0774 | 0.0728 |
| 6 | 1.0000 | 0.0000 | 0.0003 | 0.0003 |
| 7 | 1.0000 | 0.0097 | 0.3033 | 0.2985 |
| 8 | 1.0000 | 0.0314 | 0.2925 | 0.2764 |
| 9 | 0.9994 | 0.0000 | 0.0000 | 0.0000 |
| 10 | 0.9959 | 0.0501 | 0.3646 | 0.2933 |
| 11 | 1.0000 | 0.0152 | 0.3968 | 0.3968 |
| 12 | 0.9992 | 0.0013 | 0.0967 | 0.0967 |
| 13 | 1.0000 | 0.0000 | 0.0202 | 0.0202 |
| 14 | 0.9998 | 0.0000 | 0.0418 | 0.0418 |
| 15 | 1.0000 | 0.0001 | 0.0117 | 0.0115 |

Strong joint-cancel seeds: **7, 8, 10, 11** (Δcxl 0.29–0.40).

## phase_run16 — timing regimes

- Median transition @ 3375 steps (range 2500–4250).
- At first `base ≥ 0.9`, cxl8 often 0.05–0.3.
- Early-post (to ~+5k): cxl8 and max1 collapse toward 0.
- Late rise after ~10–12k; final cxl8 mean ~0.52; 9/16 > 0.5.
- Ratio cxl8 / sum of singles climbs to ~10–20 late.
- Jaccard ≈ 0, addR ≈ 1.03, pair synergy slightly positive.
- Strong late seeds: 1, 7, 13.

## freeze-at-transition

Transition dirs highly load-bearing at discovery (peak cxl often > 0.85),
then die: mean trans_cxl at final ≈ 0.016 vs final-dir cxl ≈ 0.78.
`keep_all` of the transition basis still ~0.86. Bases moderately aligned
(mean row-max |cos| ~ 0.45). Solution subspace keeps moving after the jump.

## WD ablation

| wd | grokked | final_cxl | trans_cxl_end | trans_peak | trans_step |
|---:|:-------:|----------:|--------------:|-----------:|-----------:|
| 0.1 | no | — | — | — | — |
| 0.3 | yes | 0.12 | 0.006 | 0.72 | 12.6k |
| 1.0 | yes | 0.58 | 0.000 | 0.84 | 3.4k |
| 3.0 | yes | 0.82 | 0.026 | 0.89 | 2.7k |

Late concentration into final PCA is WD-dependent. Transition subspace dies under all WDs.
