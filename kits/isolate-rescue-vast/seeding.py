"""Shared seeding helper for the isolate-rescue kits.

Every worker entry point should call ``set_seed(args.seed)`` before building
data, models or optimizers. ``launch.sh`` passes ``--seed 0..15`` for the
16-seed runs.
"""
from __future__ import annotations

import argparse
import os
import random


def set_seed(seed: int = 0, deterministic: bool = False) -> int:
    """Seed python ``random``, numpy, torch and torch.cuda.

    deterministic=True also sets cuDNN deterministic flags and
    ``torch.use_deterministic_algorithms(True, warn_only=True)`` (slower on GPU).
    """
    seed = int(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    try:
        import numpy as np
        np.random.seed(seed)
    except ImportError:
        pass
    try:
        import torch
    except ImportError:
        return seed
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    if deterministic:
        os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        torch.use_deterministic_algorithms(True, warn_only=True)
    return seed


def add_seed_args(ap: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Add --seed (default 0) and --deterministic to an argparse parser."""
    ap.add_argument("--seed", type=int, default=0, help="random seed (16-seed runs use 0..15)")
    ap.add_argument("--deterministic", action="store_true", help="cuDNN deterministic mode")
    return ap
