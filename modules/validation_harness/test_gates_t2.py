"""T2 -- physics gates: analytic MMS residuals, declared constraints, BC-loss health.

These tests run in float64 on CPU (enforced by the ``pin_precision_for_t2``
fixture in conftest.py) because MPS has no float64 support and MMS/gradient
checks are precision-critical.
"""
import math

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


def test_enforced_constraints(blueprint_frontmatter):
    """Every declared architectural constraint must pass its registered handler."""
    monolith = load_generated_monolith()
    model = monolith.Model()
    batch = monolith.get_dummy_batch()

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


def test_boundary_condition_loss_finiteness():
    """`model.compute_bc_loss(batch)` must return a finite, non-NaN scalar.

    A missing method is a code defect (SYNTAX class), not a physics failure --
    fail with an explicit message so the taxonomy classifier routes it to the
    framework agent instead of crashing the harness.
    """
    monolith = load_generated_monolith()
    model = monolith.Model()
    batch = monolith.get_dummy_batch()

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
