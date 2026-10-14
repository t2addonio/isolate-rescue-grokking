> **Pipeline stage 2 of 4 — Isolation + additive / distributed representations**  
> Grokking → causal residual isolation → **distributed/additive representations** → cross-domain residual addressing → real-world signal experiments.  
> Previous: [`residual-stream-grokking`](https://github.com/t2addonio/residual-stream-grokking) · Next: [`residual-causal-toolkit`](https://github.com/t2addonio/residual-causal-toolkit) · Map: [github.com/t2addonio](https://github.com/t2addonio)

# Isolate + Rescue Grokking

Indexed science pack for residual-stream **isolate / rescue / freeze-at-transition** experiments on modular-addition grokking (P=113, 1-layer Transformer, d=128).

Public repo: https://github.com/t2addonio/isolate-rescue-grokking

Companion paper repo: https://github.com/t2addonio/residual-stream-grokking

This repo is where the single-component claim becomes geometry: no one PCA direction is sufficient, fail sets are nearly disjoint, logit deltas add, and the transition subspace dies after the jump. That is the distributed / additive representation stage.

## Headline findings (16-seed, 2026-08-16)

- All 16 seeds grokked (`base ≈ 1.0`).
- No single PCA direction is sufficient: `keep_only ≈ 1.8%` on every seed.
- Failure sets across dirs are nearly disjoint (mean Jaccard ≈ 0).
- Logit remove-deltas are nearly additive (ratio ≈ 1.03, corr ≈ 0.998).
- Joint cancel creates thousands of extra fails beyond the union of singles.
- Phase: median transition at 3375 steps. Early-post `cxl8` and `max1` collapse; late-post `cxl8` rises again (mean ~0.52) while singles stay tiny — weight-decay redistribution, not a one-dir stream.
- Freeze-at-transition: the transition subspace is highly load-bearing at discovery, then dies by the final step. The solution basis keeps moving after the jump.
- WD ablation (0.3 / 1.0 / 3.0): late concentration into final PCA is strongly WD-dependent; transition subspace dies under all WDs. `wd=0.1` never grokked.

Hypothesis: **additive tributaries** (partial tasks that sum), not a single-dir full stream.

## Layout

```
kits/
  isolate-rescue-vast/   train + isolate + rescue + combo + phase + freeze
  joint-residual/        contrastive C + residual PCA P on the same snapshots
  gpt2_extract/          GPT-2 isolate-and-rescue probe
results/
  streams_run/           8-seed isolation+rescue
  streams_run16/         16-seed + posthoc + between-class + combinatorial
  phase_run16/           16-seed phase timing (save_every=250)
  phase_freeze_run/      freeze-at-transition
  wd_ablation/           WD 0.1 / 0.3 compact isolation
INDEX.md                 human index of kits, runs, claims
MANIFEST.tsv             sha256 + size of every local artifact file (1057 files)
```

## What is not in git

Per-seed `ckpt.pt`, snapshot `.pt`, direction `.npy`, raw logs, and full `phase_timing.json` curves stay in the working store (`/home/workdir/artifacts`). They are catalogued in `MANIFEST.tsv`. Re-run the kits to regenerate.

## Quick start

```bash
cd kits/isolate-rescue-vast
bash onstart.sh
bash launch.sh grok --save_every 250
```

Joint C+P geometry:

```bash
cd kits/joint-residual
bash launch.sh grok --save_every 250 --wd 1.0 --n_contrastive 2
```

## License

MIT. See `LICENSE`.

## Reproducibility: seeds

`kits/seeding.py` provides `set_seed(seed, deterministic=False)` (seeds python `random`, numpy, torch, torch.cuda; optional cuDNN deterministic flags) and `add_seed_args(parser)` (adds `--seed`, default 0, and `--deterministic`).

The 16-seed results are seeds **0-15**: `bash kits/<kit>/launch.sh grok` runs `worker.py --seed $s` for `s in 0..15` (override with `N_SEEDS=8` or `SEEDS="0 1 2"`). Single seed: `python worker.py --backend grok --seed 3 --device cuda --out results`.

**Note:** `worker.py` is not yet in this repo (it lives in the working store). Until it is committed, the seed handling cannot be verified here. When adding it, call `add_seed_args(ap)` and then `set_seed(args.seed, args.deterministic)` before any data, model, or optimizer setup.

Test: `pip install -r kits/isolate-rescue-vast/requirements.txt pytest && pytest tests/`

## Stage 1 dependency

This repo depends on [t2addonio/residual-stream-grokking](https://github.com/t2addonio/residual-stream-grokking), tested at commit `d92591ee6f4d1c7ddc62fa9da0b0d502ec8e3512`. That repo has no `pyproject.toml` or `setup.py`, so a `git+https` pip dependency would not install anything importable. Clone it next to this repo instead and add it to `PYTHONPATH`:

```bash
git clone https://github.com/t2addonio/residual-stream-grokking ../residual-stream-grokking
git -C ../residual-stream-grokking checkout d92591ee6f4d1c7ddc62fa9da0b0d502ec8e3512
export PYTHONPATH="$PWD/../residual-stream-grokking:$PYTHONPATH"
```

Both kits pin the same versions as Stage 1 (torch 2.14.1, numpy 2.5.4, tqdm 4.70.1, transformers 5.19.0).
