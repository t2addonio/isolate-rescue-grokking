# Isolate + Rescue Grokking — repository index

Public repo: https://github.com/t2addonio/isolate-rescue-grokking
Working store: `/home/workdir/artifacts` (1057 files, sha256 in `MANIFEST.tsv`)
Paper lineage: https://github.com/t2addonio/residual-stream-grokking

Indexed 2026-09-05.

## Claims locked by these runs

1. Single PCA dir is never the solution (`keep_only ~ 1.7–1.8%` all seeds).
2. The 8-D residual PCA span often carries most of the solution (`keep_all ≥ 0.95` on 14/16 in streams_run16).
3. Dirs fail on nearly disjoint example sets (Jaccard ≈ 0) with nearly additive logit deltas (addR ≈ 1.03).
4. Joint cancel > union of singles on the strong seeds (7 / 8 / 10 / 11).
5. Pair synergy is mixed; mean slightly positive in the 2^8 combinatorial, not a reliable superadditive rescue.
6. Transition subspace is load-bearing at first `base ≥ 0.9`, then dies. Late `cxl8` rise of *final* PCA is basis rotation under WD, not redistribution inside a frozen transition span.
7. Late concentration into final PCA scales with WD (final_cxl means ≈ 0.12 / 0.58 / 0.82 at WD 0.3 / 1.0 / 3.0).

## Kits (runnable)

| Path | Role |
|------|------|
| `kits/isolate-rescue-vast/worker.py` | Train modular add, extract 8 PCA + between-class dirs, isolate/rescue, contribution, combinatorial, phase timing, freeze-at-transition |
| `kits/isolate-rescue-vast/launch.sh` | Wave launch across GPUs (`N_SEEDS=16` default) |
| `kits/joint-residual/worker.py` | Same + contrastive subspace C, geometry vs P, cancel-C / cancel-P / cancel-both |
| `kits/gpt2_extract/isolate_and_rescue.py` | GPT-2 extract / isolate probe |

Flags worth knowing: `--save_every`, `--wd`, `--no_freeze`, `--trans_threshold`, `--n_contrastive`, `--no_joint`, `--no_combo`, `--no_phase`.

## Result packs in this repo

| Path | What it is |
|------|------------|
| `results/streams_run16/summary16.json` | 16-seed keep_all / cancel / pair-restore headline |
| `results/streams_run16/analysis/posthoc_summary.json` | Failure-set Jaccard, logit additivity, joint-extra fails, cross-seed dir alignment |
| `results/streams_run16/analysis/between_combo_summary.json` | Between-class dirs + 2^8 combinatorial / pair synergy |
| `results/phase_run16/analysis/phase16_summary.json` | Per-seed jac / addR / pair_syn / final_cxl8 |
| `results/phase_run16/summary_from_logs.json` | Phase curves reconstructed from logs |
| `results/*/per_seed_science.json` | Compact isolation / rescue / contribution / combo / freeze JSON per seed (no timing curves) |

## Local-only working store (MANIFEST.tsv)

```
artifacts/
  isolate-rescue-vast/          kit (also in git)
  isolate-rescue-*.tar.gz       launch tarballs
  joint-residual/               kit (also in git)
  joint-residual.tar.gz
  streams_run/                  8-seed run
  streams_run16/                16-seed run + analysis plots/masks
  phase_run16/                  phase timing + phase_mean_curves.png
  phase_freeze_run/             freeze-at-transition
  wd_ablation/                  wd0.1 (never grokked) + wd0.3
  gpt2_extract/                 GPT-2 probe + multi-GPU logs
```

Per-seed output schema (local):

```
results/seed_XXX/
  ckpt.pt
  dirs_pca.npy  dirs_ortho.npy  dirs_between.npy
  dirs_transition.npy           # freeze
  isolation.json  rescue.json  contribution.json
  between_isolation.json  combinatorial.json
  phase_timing.json
  phase_timing_transition.json
  transition_final_isolation.json
  meta.json
```

## How to re-run

Vast 8×4090, PyTorch 2.x CUDA 12, 64 GB disk:

```bash
cd kits/isolate-rescue-vast
bash onstart.sh
bash launch.sh grok --save_every 250 --wd 3.0
```

Science pack (exclude snapshots):

```bash
find results logs -type f ! -path '*/snapshots/*' ! -name 'combinatorial_full.json' \
  -print0 | tar -czvf isolate-science.tar.gz --null -T -
```

## Cross-links

- Paper code: `t2addonio/residual-stream-grokking`
- Domain toolkit (optical / RF / NV / audio / ISA): `t2addonio/residual-causal-toolkit`
