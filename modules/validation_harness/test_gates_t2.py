"""T2 -- physics gates: analytic MMS residuals, declared constraints, BC-loss health.

These tests run in float64 on CPU (enforced by the ``pin_precision_for_t2``
fixture in conftest.py) because MPS has no float64 support and MMS/gradient
checks are precision-critical.
"""
import math
import subprocess
import sys
from pathlib import Path

import pytest
import torch

from .mms import MMS_REGISTRY
from .registry import CONSTRAINT_REGISTRY
from .utils import load_generated_monolith

pytestmark = pytest.mark.t2

# MMS residual tolerance: analytic solutions must satisfy the PDE to ~machine eps.
RESIDUAL_TOL = 1e-12

# Constraint kinds asserted in other tiers (T0/T3), not via a T2 handler.
_NON_HANDLER_KINDS = {"param_count", "regression_targets"}

# PDE families for which this module knows how to build the residual operator.
# As new MMS families are added, extend the residual dispatch below in lock-step.
_INCOMPRESSIBLE_NS_FAMILIES = {"incompressible_ns"}
SPECTRAL_GATE_THRESHOLD = 0.15
_VREMAN_SPEC_FILE = "Chan180_S2_specx_u.txt"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _fetch_vreman_spectrum_file() -> Path:
    """Fetch the Vreman reference spectrum through the project utility script."""
    root = _repo_root()
    script = root / "tools" / "fetch_public_datasets.py"
    cmd = [sys.executable, str(script), "--fetch-vreman-file", _VREMAN_SPEC_FILE]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(root))
    if result.returncode != 0:
        raise RuntimeError(
            "Failed to fetch Vreman spectrum file via fetch_public_datasets.py. "
            f"stdout: {result.stdout.strip()} stderr: {result.stderr.strip()}"
        )
    spectrum_path = root / "data" / "public_datasets" / "vreman_channel_dns" / _VREMAN_SPEC_FILE
    if not spectrum_path.is_file():
        raise FileNotFoundError(f"Expected Vreman spectrum file not found at {spectrum_path}")
    return spectrum_path


def _load_reference_spectrum(path: Path) -> torch.Tensor:
    """Load a 1D reference spectrum from a whitespace-delimited text file."""
    values = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            cols = s.replace(",", " ").split()
            nums = []
            for c in cols:
                try:
                    nums.append(float(c))
                except ValueError:
                    continue
            if not nums:
                continue
            values.append(nums[1] if len(nums) > 1 else nums[0])

    if len(values) < 8:
        raise ValueError(f"Reference spectrum in {path} is too short ({len(values)} points)")
    return torch.tensor(values, dtype=torch.float64)


def _extract_primary_axis_signal(prediction: torch.Tensor) -> torch.Tensor:
    """Reduce model output to a 1D signal over the primary spatial axis (last dim)."""
    if prediction.ndim == 0:
        raise ValueError("Model prediction is a scalar; cannot compute spatial spectrum")
    if prediction.ndim == 1:
        return prediction

    primary_axis = prediction.ndim - 1
    reduce_dims = tuple(i for i in range(prediction.ndim) if i != primary_axis)
    signal = prediction.mean(dim=reduce_dims)
    if signal.ndim != 1:
        raise ValueError(f"Expected a 1D signal after reduction, got shape {tuple(signal.shape)}")
    return signal


def _power_spectral_density_1d(signal: torch.Tensor) -> torch.Tensor:
    centered = signal - signal.mean()
    fft_vals = torch.fft.rfft(centered)
    return (fft_vals.abs() ** 2) / max(1, centered.numel())


def _high_frequency_energy(psd: torch.Tensor, frac_start: float = 0.8) -> torch.Tensor:
    n = int(psd.numel())
    if n < 4:
        raise ValueError("PSD is too short for high-frequency integration")
    start = max(1, int(frac_start * n))
    return psd[start:].sum()


def _high_frequency_fraction(psd: torch.Tensor, frac_start: float = 0.8) -> torch.Tensor:
    """Scale-invariant high-frequency energy fraction for spectral-shape checks."""
    total = psd.sum().abs().clamp_min(1e-12)
    return _high_frequency_energy(psd, frac_start=frac_start) / total


def _grad(output, inputs):
    """Elementwise autograd derivative (grad_outputs=ones), graph retained."""
    return torch.autograd.grad(
        output, inputs,
        grad_outputs=torch.ones_like(output),
        create_graph=True,
        retain_graph=True,
    )


def _incompressible_ns_residuals(mms_fn, x, y, t, nu=0.01, rho=1.0):
    """Continuity + 2D momentum residuals of the analytic (u, v, p) field."""
    u, v, p = mms_fn(x, y, t, nu=nu, rho=rho)

    du_dx, = _grad(u, [x]); du_dy, = _grad(u, [y]); du_dt, = _grad(u, [t])
    dv_dx, = _grad(v, [x]); dv_dy, = _grad(v, [y]); dv_dt, = _grad(v, [t])
    dp_dx, = _grad(p, [x]); dp_dy, = _grad(p, [y])

    d2u_dx2, = _grad(du_dx, [x]); d2u_dy2, = _grad(du_dy, [y])
    d2v_dx2, = _grad(dv_dx, [x]); d2v_dy2, = _grad(dv_dy, [y])

    continuity = du_dx + dv_dy
    momentum_x = du_dt + u * du_dx + v * du_dy + dp_dx - nu * (d2u_dx2 + d2u_dy2)
    momentum_y = dv_dt + u * dv_dx + v * dv_dy + dp_dy - nu * (d2v_dx2 + d2v_dy2)
    return continuity, momentum_x, momentum_y


def test_mms_analytic_residual(blueprint_frontmatter, pin_precision_for_t2):
    """The registered analytic solution must satisfy its PDE to < 1e-12."""
    pde_family = blueprint_frontmatter.pde_family
    mms_fn = MMS_REGISTRY.get(pde_family)
    if mms_fn is None:
        pytest.skip(f"No MMS analytic solution registered for pde_family '{pde_family}'")

    if pde_family not in _INCOMPRESSIBLE_NS_FAMILIES:
        pytest.skip(
            f"No T2 residual operator defined for pde_family '{pde_family}' "
            "(add one alongside the MMS entry)"
        )

    # float64 grid of collocation points with per-coordinate gradients.
    n = 8
    coords = torch.linspace(0.0, 2.0 * math.pi, n, dtype=torch.float64)
    times = torch.linspace(0.0, 1.0, 3, dtype=torch.float64)
    gx, gy, gt = torch.meshgrid(coords, coords, times, indexing="ij")
    x = gx.reshape(-1).clone().requires_grad_(True)
    y = gy.reshape(-1).clone().requires_grad_(True)
    t = gt.reshape(-1).clone().requires_grad_(True)

    continuity, momentum_x, momentum_y = _incompressible_ns_residuals(mms_fn, x, y, t)

    for name, residual in (
        ("continuity", continuity),
        ("momentum_x", momentum_x),
        ("momentum_y", momentum_y),
    ):
        max_abs = residual.abs().max().item()
        assert max_abs < RESIDUAL_TOL, (
            f"{pde_family} {name} residual {max_abs:.3e} exceeds tolerance {RESIDUAL_TOL:.0e} "
            "-- analytic MMS solution is not exact (check the registered formula)"
        )


def test_enforced_constraints(blueprint_frontmatter, standard_evaluation_batch):
    """Every declared architectural constraint must pass its registered handler."""
    monolith = load_generated_monolith()
    model = monolith.Model()
    batch = standard_evaluation_batch

    handler_constraints = [
        c for c in blueprint_frontmatter.constraints if c.kind not in _NON_HANDLER_KINDS
    ]
    if not handler_constraints:
        pytest.skip("No handler-backed constraints declared in blueprint frontmatter")

    for constraint in handler_constraints:
        handler_cls = CONSTRAINT_REGISTRY.get(constraint.kind)
        # Unknown kinds must fail loudly (deterministic kill switch), never skip.
        assert handler_cls is not None, (
            f"UNSUPPORTED_CONSTRAINT: no handler registered for kind '{constraint.kind}'"
        )
        handler = handler_cls()
        params = handler.ParamModel(**constraint.params)
        handler.gate_assert(model, batch, params)


def test_boundary_condition_loss_finiteness(standard_evaluation_batch):
    """`model.compute_bc_loss(batch)` must return a finite, non-NaN scalar.

    A missing method is a code defect (SYNTAX class), not a physics failure --
    fail with an explicit message so the taxonomy classifier routes it to the
    framework agent instead of crashing the harness.
    """
    monolith = load_generated_monolith()
    model = monolith.Model()
    batch = standard_evaluation_batch

    if not hasattr(model, "compute_bc_loss"):
        pytest.fail(
            "SYNTAX: generated `Model` does not define `compute_bc_loss(batch)`; "
            "route back to the framework agent to add it"
        )

    bc_loss = model.compute_bc_loss(batch)
    bc_tensor = bc_loss if torch.is_tensor(bc_loss) else torch.as_tensor(bc_loss)
    assert torch.isfinite(bc_tensor).all(), (
        f"Boundary-condition loss is non-finite (NaN/Inf): {bc_loss}"
    )


def test_mms_spectral_fidelity(pin_precision_for_t2, standard_evaluation_batch):
    """Predicted high-frequency PSD energy must match Vreman DNS within tolerance."""
    assert pin_precision_for_t2["device"].type == "cpu"
    assert pin_precision_for_t2["dtype"] == torch.float64

    monolith = load_generated_monolith()
    model = monolith.Model().to(device="cpu", dtype=torch.float64)
    model.eval()
    batch = standard_evaluation_batch

    x = batch.x
    if not torch.is_tensor(x):
        x = torch.as_tensor(x)
    x = x.to(device="cpu", dtype=torch.float64)

    with torch.no_grad():
        prediction = model(x)

    if isinstance(prediction, (tuple, list)):
        prediction = prediction[0]
    elif isinstance(prediction, dict):
        tensor_values = [v for v in prediction.values() if torch.is_tensor(v)]
        if not tensor_values:
            pytest.fail(
                "GATE_FAIL|t2:test_mms_spectral_fidelity model output dict has no tensor values"
            )
        prediction = tensor_values[0]

    if not torch.is_tensor(prediction):
        prediction = torch.as_tensor(prediction)
    prediction = prediction.to(device="cpu", dtype=torch.float64)

    signal = _extract_primary_axis_signal(prediction)
    pred_psd = _power_spectral_density_1d(signal)

    ref_path = _fetch_vreman_spectrum_file()
    ref_signal = _load_reference_spectrum(ref_path)
    ref_psd = _power_spectral_density_1d(ref_signal)

    n = min(pred_psd.numel(), ref_psd.numel())
    if n < 8:
        pytest.fail(
            "GATE_FAIL|t2:test_mms_spectral_fidelity insufficient PSD overlap with reference"
        )

    pred_hf_frac = _high_frequency_fraction(pred_psd[:n])
    ref_hf_frac = _high_frequency_fraction(ref_psd[:n])
    max_allowed_hf_frac = max(ref_hf_frac.item() * 1.5, 0.30)
    pred_hf_frac_value = pred_hf_frac.item()

    assert pred_hf_frac_value <= max_allowed_hf_frac, (
        "GATE_FAIL|t2:test_mms_spectral_fidelity "
        f"high-frequency PSD fraction {pred_hf_frac_value:.3%} exceeds upper bound "
        f"{max_allowed_hf_frac:.3%} (reference {ref_hf_frac.item():.3%})"
    )
