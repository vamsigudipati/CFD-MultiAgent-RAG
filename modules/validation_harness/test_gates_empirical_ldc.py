"""Empirical benchmark gate for 2D lid-driven cavity flow.

This file is intentionally isolated from the generic PINN gates so the
benchmark only runs when Node D explicitly appends it for lid-driven cavity
papers/benchmarks.
"""
import pytest
import torch

from .utils import load_generated_monolith


def _resolve_pinn_model():
    """Load the generated monolith model for empirical benchmark validation."""
    try:
        monolith = load_generated_monolith()
        return monolith.Model()
    except Exception as exc:
        pytest.skip(f"Empirical LDC gate requires generated monolith: {exc}")


@pytest.mark.t2
def test_lid_driven_cavity_boundary_and_continuity():
    """Check cavity wall BCs and approximate continuity on the unit square.

    Boundary conditions:
      - Top lid (y=1): u=1, v=0
      - Left/right/bottom walls: u=0, v=0

    Interior physics:
      - Approximate mass conservation: du/dx + dv/dy ~= 0
    """
    model = _resolve_pinn_model()
    model.eval()

    dtype = torch.float64
    device = torch.device("cpu")

    n_boundary = 64
    lin = torch.linspace(0.0, 1.0, n_boundary, dtype=dtype, device=device).reshape(-1, 1)

    # Top lid: y = 1, u = 1, v = 0
    x_top = lin.clone().requires_grad_(True)
    y_top = torch.ones_like(x_top, requires_grad=True)
    u_top, v_top, _ = model(x_top, y_top)

    # Bottom wall: y = 0, u = 0, v = 0
    x_bot = lin.clone().requires_grad_(True)
    y_bot = torch.zeros_like(x_bot, requires_grad=True)
    u_bot, v_bot, _ = model(x_bot, y_bot)

    # Left wall: x = 0, u = 0, v = 0
    y_left = lin.clone().requires_grad_(True)
    x_left = torch.zeros_like(y_left, requires_grad=True)
    u_left, v_left, _ = model(x_left, y_left)

    # Right wall: x = 1, u = 0, v = 0
    y_right = lin.clone().requires_grad_(True)
    x_right = torch.ones_like(y_right, requires_grad=True)
    u_right, v_right, _ = model(x_right, y_right)

    bc_tol = 0.15

    top_u_error = torch.mean(torch.abs(u_top - 1.0))
    top_v_error = torch.mean(torch.abs(v_top))

    bot_u_error = torch.mean(torch.abs(u_bot))
    bot_v_error = torch.mean(torch.abs(v_bot))

    left_u_error = torch.mean(torch.abs(u_left))
    left_v_error = torch.mean(torch.abs(v_left))

    right_u_error = torch.mean(torch.abs(u_right))
    right_v_error = torch.mean(torch.abs(v_right))

    assert top_u_error < bc_tol, f"Top-lid u BC violated: mean |u-1| = {top_u_error.item():.4e}"
    assert top_v_error < bc_tol, f"Top-lid v BC violated: mean |v| = {top_v_error.item():.4e}"

    assert bot_u_error < bc_tol, f"Bottom-wall u BC violated: mean |u| = {bot_u_error.item():.4e}"
    assert bot_v_error < bc_tol, f"Bottom-wall v BC violated: mean |v| = {bot_v_error.item():.4e}"

    assert left_u_error < bc_tol, f"Left-wall u BC violated: mean |u| = {left_u_error.item():.4e}"
    assert left_v_error < bc_tol, f"Left-wall v BC violated: mean |v| = {left_v_error.item():.4e}"

    assert right_u_error < bc_tol, f"Right-wall u BC violated: mean |u| = {right_u_error.item():.4e}"
    assert right_v_error < bc_tol, f"Right-wall v BC violated: mean |v| = {right_v_error.item():.4e}"

    n_interior = 32
    eps = 1e-3
    xs = torch.linspace(eps, 1.0 - eps, n_interior, dtype=dtype, device=device)
    ys = torch.linspace(eps, 1.0 - eps, n_interior, dtype=dtype, device=device)
    gy, gx = torch.meshgrid(ys, xs, indexing="ij")

    x_int = gx.reshape(-1, 1).clone().detach().requires_grad_(True)
    y_int = gy.reshape(-1, 1).clone().detach().requires_grad_(True)

    u_int, v_int, _ = model(x_int, y_int)

    du_dx, = torch.autograd.grad(
        outputs=u_int,
        inputs=x_int,
        grad_outputs=torch.ones_like(u_int),
        create_graph=True,
        retain_graph=True,
    )
    dv_dy, = torch.autograd.grad(
        outputs=v_int,
        inputs=y_int,
        grad_outputs=torch.ones_like(v_int),
        create_graph=True,
        retain_graph=True,
    )

    continuity = du_dx + dv_dy
    continuity_tol = 1e-1
    mean_continuity_residual = torch.mean(torch.abs(continuity))

    assert torch.isfinite(continuity).all(), "Continuity residual contains non-finite values"
    assert mean_continuity_residual < continuity_tol, (
        f"Continuity violated: mean |du/dx + dv/dy| = {mean_continuity_residual.item():.4e}"
    )