"""Shared pytest fixtures and hooks for the validation harness.

Enforces the three determinism guarantees required by the pipeline design:
  1. A single, session-scoped source of truth for per-paper frontmatter.
  2. Global reproducibility (fixed seed + PyTorch deterministic algorithms).
  3. Strict CPU/float64 pinning for T2 (MMS/gradcheck) tests, since Apple
     Silicon's MPS backend does not support float64 at all -- running these
     tests on MPS would either hard-error or silently fall back, producing
     false-failure fingerprints that poison the self-healing loop.
"""
from pathlib import Path
from collections import namedtuple

import pytest
import torch
import yaml

from .frontmatter import BlueprintFrontmatter

# Import the handler and MMS packages so their @register / @register_mms
# decorators populate CONSTRAINT_REGISTRY / MMS_REGISTRY before any test runs.
from . import handlers  # noqa: F401  (registration side effect)
from . import mms  # noqa: F401  (registration side effect)

SEED = 42
BLUEPRINT_YAML_PATH = Path(__file__).resolve().parent.parent / "workspace" / "blueprint.yaml"
Batch = namedtuple("Batch", ["x", "y", "variable_names"])


# --- 1. Frontmatter loading (session-scoped, immutable for the whole run) ------

@pytest.fixture(scope="session")
def blueprint_frontmatter() -> BlueprintFrontmatter:
    """Load and strictly validate the active paper's frontmatter once per session."""
    if not BLUEPRINT_YAML_PATH.exists():
        pytest.skip(f"No blueprint frontmatter found at {BLUEPRINT_YAML_PATH}")
    with open(BLUEPRINT_YAML_PATH, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    return BlueprintFrontmatter.from_yaml(raw)


# --- 2. Global determinism enforcement -----------------------------------------

def pytest_configure(config: pytest.Config) -> None:
    """Register tier markers and enforce reproducibility before any test runs."""
    for tier in ("t0", "t1", "t2", "t3"):
        config.addinivalue_line("markers", f"{tier}: validation harness tier {tier}")
    config.addinivalue_line("markers", "gpu: requires a GPU/MPS device (skipped by default)")

    torch.manual_seed(SEED)
    # warn_only=False: a non-deterministic op must fail loudly, not drift silently.
    torch.use_deterministic_algorithms(True, warn_only=False)


@pytest.fixture(autouse=True)
def _reseed_each_test():
    """Reseed before every test so ordering never affects reproducibility."""
    torch.manual_seed(SEED)
    yield


@pytest.fixture
def standard_evaluation_batch(request: pytest.FixtureRequest):
    """Deterministic Green Layer batch used across T1/T2 gates.

    This closes the trust leak where generated monoliths could game tests by
    supplying a favorable batch. The harness now owns x/y generation.
    """
    is_t2 = request.node.get_closest_marker("t2") is not None
    dtype = torch.float64 if is_t2 else torch.float32

    g = torch.Generator(device="cpu")
    g.manual_seed(SEED)

    b, c, h, w = 2, 3, 64, 64
    x_noise = torch.randn((b, c, h, w), generator=g, dtype=dtype)

    ys = torch.linspace(0.0, 2.0 * torch.pi, h, dtype=dtype)
    xs = torch.linspace(0.0, 2.0 * torch.pi, w, dtype=dtype)
    gy, gx = torch.meshgrid(ys, xs, indexing="ij")
    pattern = torch.stack(
        [
            torch.sin(gx),
            torch.cos(gy),
            torch.sin(gx + gy),
        ],
        dim=0,
    ).unsqueeze(0)

    x = 0.85 * x_noise + 0.15 * pattern
    y = torch.tanh(0.7 * x + 0.15 * x.roll(shifts=1, dims=-1) - 0.10 * x.roll(shifts=1, dims=-2))
    return Batch(x=x, y=y, variable_names=["u", "v", "p"])


# --- 3. Strict CPU / float64 pinning for T2 (MMS + gradcheck) tests ------------

@pytest.fixture(autouse=True)
def pin_precision_for_t2(request: pytest.FixtureRequest):
    """Force CPU + float64 for any test marked ``@pytest.mark.t2``.

    MPS has no float64 support, so T2 tests must never run on it. This fixture
    pins torch's default dtype for the duration of a t2 test and restores the
    previous default afterward so other tiers are unaffected.
    """
    is_t2 = request.node.get_closest_marker("t2") is not None
    if not is_t2:
        yield None
        return

    previous_default_dtype = torch.get_default_dtype()
    torch.set_default_dtype(torch.float64)
    device = torch.device("cpu")
    try:
        yield {"device": device, "dtype": torch.float64}
    finally:
        torch.set_default_dtype(previous_default_dtype)
