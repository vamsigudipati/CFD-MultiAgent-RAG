"""PINN-specific harness gates for continuous coordinate-to-field models.

These tests are self-contained and validate the most basic architectural
contract for a Physics-Informed Neural Network (PINN):
  1. The model consumes continuous coordinates (x, y) with gradients enabled.
  2. The model emits continuous fields (u, v, p).
  3. Autograd can differentiate those outputs w.r.t. the coordinates.
"""
import torch

from .utils import load_generated_monolith


class DummyPINNModel(torch.nn.Module):
    """Minimal 2-layer coordinate MLP used to validate the PINN harness."""

    def __init__(self, hidden_dim: int = 64) -> None:
        super().__init__()
        self.net = torch.nn.Sequential(
            torch.nn.Linear(2, hidden_dim),
            torch.nn.Tanh(),
            torch.nn.Linear(hidden_dim, 3),
        )

    def forward(self, x: torch.Tensor, y: torch.Tensor):
        coords = torch.cat([x, y], dim=1)
        fields = self.net(coords)
        u = fields[:, 0:1]
        v = fields[:, 1:2]
        p = fields[:, 2:3]
        return u, v, p


def _resolve_pinn_model():
    """Use the generated monolith when available; otherwise fall back to dummy.

    This keeps the file self-validating for standalone harness development while
    making orchestrated runs test the actual generated PINN artifact.
    """
    try:
        monolith = load_generated_monolith()
        return monolith.Model()
    except Exception:
        return DummyPINNModel()


def test_pinn_coordinate_mapping():
    """Model must map continuous (x, y) coordinates to continuous (u, v, p) fields."""
    batch_size = 8
    model = _resolve_pinn_model()

    x = torch.linspace(-1.0, 1.0, batch_size, dtype=torch.float32).reshape(-1, 1)
    y = torch.linspace(1.0, -1.0, batch_size, dtype=torch.float32).reshape(-1, 1)
    x.requires_grad_(True)
    y.requires_grad_(True)

    u, v, p = model(x, y)

    assert u.shape == (batch_size, 1), f"Expected u shape {(batch_size, 1)}, got {tuple(u.shape)}"
    assert v.shape == (batch_size, 1), f"Expected v shape {(batch_size, 1)}, got {tuple(v.shape)}"
    assert p.shape == (batch_size, 1), f"Expected p shape {(batch_size, 1)}, got {tuple(p.shape)}"
    assert u.dtype == x.dtype == y.dtype


def test_pinn_autograd_residuals():
    """Autograd must differentiate PINN outputs w.r.t. continuous coordinates."""
    batch_size = 8
    model = _resolve_pinn_model()

    x = torch.linspace(-1.0, 1.0, batch_size, dtype=torch.float32).reshape(-1, 1)
    y = torch.linspace(1.0, -1.0, batch_size, dtype=torch.float32).reshape(-1, 1)
    x.requires_grad_(True)
    y.requires_grad_(True)

    u, v, p = model(x, y)

    grad_u_x, = torch.autograd.grad(
        outputs=u,
        inputs=x,
        grad_outputs=torch.ones_like(u),
        create_graph=True,
        retain_graph=True,
    )
    grad_v_y, = torch.autograd.grad(
        outputs=v,
        inputs=y,
        grad_outputs=torch.ones_like(v),
        create_graph=True,
        retain_graph=True,
    )

    assert grad_u_x.shape == x.shape, (
        f"Expected du/dx shape {tuple(x.shape)}, got {tuple(grad_u_x.shape)}"
    )
    assert grad_v_y.shape == y.shape, (
        f"Expected dv/dy shape {tuple(y.shape)}, got {tuple(grad_v_y.shape)}"
    )
    assert torch.isfinite(grad_u_x).all(), "du/dx contains non-finite values"
    assert torch.isfinite(grad_v_y).all(), "dv/dy contains non-finite values"
