# Joint Residual Geometry Kit

Combines two complementary residual analyses on the **same** model and snapshots:

| Object | Extraction | Intervention |
|--------|------------|--------------|
| **C** — Contrastive decision subspace | Train-vs-held-out mean difference → SVD → QR | Hard remove / keep |
| **P** — Residual PCA subspace | Top-n PCA of residual activations | Hard remove / keep / cancel span |

Reports geometry (principal angles, energy overlap) and cross-interventions: cancel-C / cancel-P / cancel-both, plus the full isolate-rescue suite on P.

```bash
cd kits/joint-residual
bash onstart.sh
bash launch.sh grok --save_every 250 --wd 1.0 --n_contrastive 2
```

`worker.py` is in the working store at `artifacts/joint-residual/worker.py`.

## Seeds

`launch.sh` runs seeds 0-15 by default (`--seed N`). `worker.py` must call `set_seed(args.seed, args.deterministic)` from `seeding.py` (symlink to `../seeding.py`). The kit pins are in `requirements.txt` and match the other kit and Stage 1.
