#!/usr/bin/env bash
# Vast.ai On-start script. Paste as the instance onstart, OR run after SSH:
#   bash onstart.sh
# Assumes this directory is already on the box (scp / wget the tarball first).
set -euo pipefail
cd "$(dirname "$0")"

echo "=== isolate-rescue onstart $(date -Is) ==="
python -V
python -c "import torch; print('torch', torch.__version__, 'cuda', torch.cuda.is_available(), 'n', torch.cuda.device_count())"

python -m pip install -q --upgrade pip
python -m pip install -q -r requirements.txt

# GPT-2 weights cache (only needed for --backend gpt2)
if [[ "${BACKEND:-grok}" == "gpt2" ]]; then
  python - <<'PY'
from pathlib import Path
try:
    from transformers import GPT2Model, GPT2TokenizerFast
    GPT2TokenizerFast.from_pretrained("gpt2")
    GPT2Model.from_pretrained("gpt2")
    print("cached gpt2")
except Exception as e:
    print("gpt2 cache skip:", e)
PY
fi

# Optional: auto-launch. Set AUTORUN=1 in Vast env to kick off immediately.
# N_SEEDS defaults to 16 inside launch.sh.
if [[ "${AUTORUN:-0}" == "1" ]]; then
  bash launch.sh "${BACKEND:-grok}"
fi

echo "=== ready. launch with:  bash launch.sh grok ==="
echo "=== 16 seeds default (2 waves on 8 GPUs). Override: N_SEEDS=8 bash launch.sh grok ==="
