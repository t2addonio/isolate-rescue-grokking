#!/usr/bin/env bash
# Optional: create a Vast.ai instance via the CLI if you have it installed locally.
#   export VAST_API_KEY=...
#   bash vast_create.sh
# You can also just use the website: rent 4–8× 4090, image pytorch 2.4 cuda 12, 32 GB disk.
set -euo pipefail

echo "Search 4090 offers (cheapest 4+):"
if command -v vastai >/dev/null 2>&1; then
  vastai search offers 'gpu_name=RTX_4090 num_gpus>=4 reliability>0.98 inet_down>200' \
    --order 'dph_total' | head -20
  echo
  echo "Create with (edit the offer id):"
  echo "  vastai create instance OFFER_ID \\"
  echo "    --image pytorch/pytorch:2.4.0-cuda12.4-cudnn9-runtime \\"
  echo "    --disk 32 \\"
  echo "    --ssh \\"
  echo "    --direct \\"
  echo "    --onstart-cmd 'sleep 1'"
  echo
  echo "Then scp this folder to /workspace/isolate-rescue-vast and run onstart.sh + launch.sh"
else
  echo "vastai CLI not installed. pip install vastai && vastai set api-key YOUR_KEY"
  echo "Or rent from https://cloud.vast.ai  — filter RTX 4090, 4–8 GPUs, PyTorch + CUDA 12."
fi
