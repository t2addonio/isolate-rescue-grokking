#!/usr/bin/env bash
# Launch workers across visible GPUs in waves.
#
# Defaults: 16 seeds (0..15) on whatever GPUs nvidia-smi sees.
# With 8 GPUs → two waves of 8. One seed per GPU at a time (no VRAM fights).
#
#   bash launch.sh                          # grok, 16 seeds
#   bash launch.sh grok
#   bash launch.sh gpt2
#   N_SEEDS=8 bash launch.sh grok           # original 8-seed density
#   SEEDS="0 1 2 3" bash launch.sh grok
#   QUICK=1 bash launch.sh                  # smoke test
#   bash launch.sh grok --steps 30000
set -euo pipefail
cd "$(dirname "$0")"

BACKEND="${1:-grok}"
EXTRA=("${@:2}")

if ! command -v nvidia-smi >/dev/null 2>&1; then
  echo "nvidia-smi not found. Run on the Vast.ai GPU box."
  exit 1
fi

N=$(nvidia-smi -L | wc -l)
echo "GPUs detected: $N"
nvidia-smi -L

if [[ -n "${SEEDS:-}" ]]; then
  read -r -a SEED_ARR <<< "$SEEDS"
else
  N_SEEDS="${N_SEEDS:-16}"
  SEED_ARR=()
  for ((i=0; i<N_SEEDS; i++)); do SEED_ARR+=("$i"); done
fi

mkdir -p results logs
echo "backend=$BACKEND  n_seeds=${#SEED_ARR[@]}  seeds=${SEED_ARR[*]}  extra=${EXTRA[*]:-}"
echo "schedule: ${#SEED_ARR[@]} seeds across $N GPUs in waves of $N"

fail=0
wave=0
i=0
while (( i < ${#SEED_ARR[@]} )); do
  wave=$((wave + 1))
  PIDS=()
  echo "===== wave $wave ====="
  for ((g=0; g<N && i<${#SEED_ARR[@]}; g++, i++)); do
    seed="${SEED_ARR[$i]}"
    log="logs/seed_$(printf '%03d' "$seed").log"
    echo "→ seed=$seed  gpu=$g  log=$log"
    cmd=(python worker.py --backend "$BACKEND" --seed "$seed" --device cuda --out results)
    if [[ "${QUICK:-0}" == "1" ]]; then
      cmd+=(--quick)
    fi
    if [[ ${#EXTRA[@]} -gt 0 ]]; then
      cmd+=("${EXTRA[@]}")
    fi
    CUDA_VISIBLE_DEVICES="$g" "${cmd[@]}" >"$log" 2>&1 &
    PIDS+=($!)
  done
  for pid in "${PIDS[@]}"; do
    if ! wait "$pid"; then
      echo "worker pid $pid failed"
      fail=1
    fi
  done
done

echo "===== analyze ====="
python analyze.py results || true

if [[ "$fail" -ne 0 ]]; then
  echo "one or more workers failed — check logs/"
  exit 1
fi
echo "all workers finished (${#SEED_ARR[@]} seeds)"
