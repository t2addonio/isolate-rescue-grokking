# Isolation + Rescue + Phase Timing + Freeze-at-Transition — Vast.ai 4090 kit

16 seeds by default (2 waves on 8×4090). Each seed:

1. **Trains** modular-addition grokking model with **snapshots every 500 steps**
2. Extracts 8 residual directions (PCA + between-class)
3. **Isolation + rescue** (keep_only / remove / cancel-top-k / restore)
4. **Contribution** — per-example failure sets, Jaccard, logit additivity
5. **Between-class** isolation + rescue
6. **Combinatorial** full 2^8 subset cancel + pair synergy
7. **Phase timing** — probes *final* solution dirs on every snapshot
8. **Freeze-at-transition** — extract PCA dirs at first base≥0.9, probe those *fixed* axes across later snapshots + final-state isolation of the transition basis

Hypothesis: additive tributaries (partial tasks that sum), not one-dir full streams.

## Launch

```bash
cd kits/isolate-rescue-vast
bash onstart.sh
QUICK=1 bash launch.sh grok
bash launch.sh grok --save_every 250 --wd 3.0
```

`worker.py` lives in the working store at `artifacts/isolate-rescue-vast/worker.py` until the next push of the 50 kB trainer (too large for a single content-API batch with the binaries).
