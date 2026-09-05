#!/usr/bin/env python3
"""Merge seed_* result folders and print isolation / rescue / phase / contrib tables."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def load_seeds(root: Path) -> List[Dict[str, Any]]:
    rows = []
    for d in sorted(root.glob("seed_*")):
        meta_p = d / "meta.json"
        iso_p = d / "isolation.json"
        res_p = d / "rescue.json"
        if not (meta_p.exists() and iso_p.exists() and res_p.exists()):
            print(f"skip incomplete {d}")
            continue
        row = {
            "dir": str(d),
            "meta": json.loads(meta_p.read_text()),
            "iso": json.loads(iso_p.read_text()),
            "rescue": json.loads(res_p.read_text()),
        }
        for name in ("contribution", "phase_timing", "combinatorial", "between_rescue"):
            p = d / f"{name}.json"
            if p.exists():
                row[name] = json.loads(p.read_text())
        rows.append(row)
    return rows


def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default="results")
    args = ap.parse_args()
    root = Path(args.root)
    rows = load_seeds(root)
    if not rows:
        print(f"no complete seeds in {root}")
        return

    print("=" * 72)
    print(f"seeds: {len(rows)}   backend={rows[0]['meta'].get('backend')}   P={rows[0]['meta'].get('P')}")
    print(f"save_every={rows[0]['meta'].get('save_every')}  steps={rows[0]['meta'].get('steps')}")
    print("=" * 72)

    print("\n## per-seed headline")
    print(f"{'seed':>6}  {'base':>8}  {'cancel':>8}  {'keep_all':>8}  {'Jac':>7}  {'joint+':>7}  {'addR':>7}  {'pairSyn':>8}  {'snaps':>5}")
    for r in rows:
        m, iso, res = r["meta"], r["iso"], r["rescue"]
        base = iso["base"]["acc"]
        cancel = res["cancel_top"]["acc"]
        keep_all = list(iso.get("keep_all_subspace", {}).values())
        ka = keep_all[0]["acc"] if keep_all else float("nan")
        c = r.get("contribution", {})
        jac = c.get("mean_offdiag_jaccard", float("nan"))
        joint = c.get("joint_only_extra_fails", -1)
        add_r = c.get("mean_additivity_ratio", float("nan"))
        combo = r.get("combinatorial", {})
        psyn = combo.get("mean_pair_synergy", float("nan"))
        snaps = m.get("n_snapshots", 0)
        print(
            f"{m['seed']:6d}  {base:8.4f}  {cancel:8.4f}  {ka:8.4f}  "
            f"{jac:7.3f}  {joint:7d}  {add_r:7.3f}  {psyn:+8.4f}  {snaps:5d}"
        )

    print("\n## isolation mean across seeds")
    n_dirs = rows[0]["iso"]["n_dirs"]
    print(f"{'dir':>5}  {'keep_only':>10}  {'remove':>10}  {'drop':>10}")
    for i in range(n_dirs):
        kacc, racc, base = [], [], []
        for r in rows:
            b = r["iso"]["base"]["acc"]
            base.append(b)
            ke = r["iso"]["keep_only"][i] if i < len(r["iso"]["keep_only"]) else None
            re = r["iso"]["remove"][i] if i < len(r["iso"]["remove"]) else None
            if not ke:
                continue
            sk = [k for k in ke if k.startswith("scale_")]
            key = "scale_1.0" if "scale_1.0" in sk else sk[0]
            kacc.append(ke[key]["acc"])
            racc.append(re[key]["acc"])
        print(f"{i:5d}  {mean(kacc):10.4f}  {mean(racc):10.4f}  {mean(base)-mean(racc):10.4f}")

    phase_rows = [r for r in rows if "phase_timing" in r and r["phase_timing"].get("rows")]
    if phase_rows:
        print("\n## phase timing — cancel_all_drop vs step (mean across seeds)")
        by_step: Dict[int, List[float]] = {}
        by_step_base: Dict[int, List[float]] = {}
        by_step_max1: Dict[int, List[float]] = {}
        for r in phase_rows:
            for row in r["phase_timing"]["rows"]:
                s = row["step"]
                by_step.setdefault(s, []).append(row["cancel_all_drop"])
                by_step_base.setdefault(s, []).append(row["base_acc"])
                by_step_max1.setdefault(s, []).append(max(d["drop"] for d in row["per_dir"]))
        print(f"{'step':>6}  {'base':>8}  {'maxΔ1':>8}  {'cancel8':>8}  n")
        for s in sorted(by_step.keys()):
            print(
                f"{s:6d}  {mean(by_step_base[s]):8.4f}  {mean(by_step_max1[s]):8.4f}  "
                f"{mean(by_step[s]):8.4f}  {len(by_step[s])}"
            )

    print("\n## interpretation")
    print("  keep_only ~ chance     → partial contribution (additive tributaries)")
    print("  keep_all ~ base        → 8-D subspace contains the solution")
    print("  Jac ~ 0                → dirs tip different borderline examples")
    print("  joint+ large           → cancel hurts examples no single removal breaks")
    print("  addR ~ 1.0             → logit contributions nearly linear-additive")
    print("  pairSyn > 0            → accuracy damage superadditive")
    print("  phase: cancel8 rises with base_acc through grokking jump")


if __name__ == "__main__":
    main()
