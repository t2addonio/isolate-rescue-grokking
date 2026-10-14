# Errata (14 October 2026)

An audit of this repo (2026-10-14) found that the evidence for its headline results is not in the repo. Full cross-repo errata draft: [residual-stream-grokking `papers/CORRECTIONS_2026-10-14.md`](https://github.com/t2addonio/residual-stream-grokking/blob/main/papers/CORRECTIONS_2026-10-14.md) (section D).

| # | Where | Original | Correction | Status |
|---|---|---|---|---|
| 1 | `INDEX.md` kits table | `kits/*/worker.py` listed as the training code | `worker.py` is **not in the repo** for either kit; `launch.sh` calls it | unbacked — supply `worker.py` |
| 2 | `INDEX.md` "Result packs in this repo" | `summary16.json`, `posthoc_summary.json`, `between_combo_summary.json`, `phase16_summary.json`, `summary_from_logs.json`, `per_seed_science.json` | **none are committed**; `results/` holds only `HEADLINES.md` | unbacked — supply data |
| 3 | `results/HEADLINES.md` | "compact copies live next to this file when uploaded" | no copies were uploaded | corrected |
| 4 | `README.md` "Headline findings (16-seed)"; `INDEX.md` "Claims locked by these runs"; profile README "16-seed isolate/rescue" | stated as findings | unverified: no training code, no data, seeding of seeds 0–15 unconfirmed (`launch.sh` passes `--seed`, but the worker that would use it is missing) | unbacked — remove or supply data |
| 5 | `STATUS.md` | "Kits + compact science JSONs uploaded" | kits uploaded without `worker.py`; JSONs and `MANIFEST.tsv` not uploaded | corrected |
| 6 | `README.md` "All 16 seeds base ≈ 1.0" vs HEADLINES `keep_all` 0.8785 | — | not a contradiction (different metrics); clarified | clarified |

**To close this:** commit both `worker.py` files (calling `set_seed(args.seed, args.deterministic)` from `kits/seeding.py`), the compact result JSONs, and `MANIFEST.tsv`; then re-run `analyze.py` on them.
