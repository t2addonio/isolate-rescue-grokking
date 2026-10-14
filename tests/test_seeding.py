import sys, pathlib, random
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "kits"))
import numpy as np, torch
from seeding import set_seed, add_seed_args
import argparse

def _run(seed):
    set_seed(seed, deterministic=True)
    m = torch.nn.Sequential(torch.nn.Linear(8, 16), torch.nn.ReLU(), torch.nn.Linear(16, 4))
    opt = torch.optim.AdamW(m.parameters(), lr=1e-2)
    x = torch.randn(32, 8); y = torch.randint(0, 4, (32,))
    for _ in range(20):
        opt.zero_grad(); torch.nn.functional.cross_entropy(m(x), y).backward(); opt.step()
    return random.random(), np.random.rand(3), torch.cat([p.flatten() for p in m.parameters()]).detach()

def test_same_seed_identical():
    a, b = _run(7), _run(7)
    assert a[0] == b[0] and np.array_equal(a[1], b[1]) and torch.equal(a[2], b[2])

def test_different_seed_differs():
    assert not torch.equal(_run(0)[2], _run(1)[2])

def test_seed_arg_default():
    assert add_seed_args(argparse.ArgumentParser()).parse_args([]).seed == 0
