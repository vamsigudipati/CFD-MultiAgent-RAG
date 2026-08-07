# PyTorch PINN Training Best Practices

Framework reference for generating training/validation logic in continuous
PINN monoliths. Follows the two-stage optimizer pattern common in the PINN
literature (Adam for exploration, then L-BFGS for sharp convergence).

## Contract

- `train_model(model, data, epochs_adam=1000, lbfgs_iters=500, nu=0.01)` — runs
  the full two-stage training and returns a history dict.
- `validate(model, data, nu=0.01)` — computes validation losses without
  optimizer steps and returns a metrics dict.
- All losses must remain differentiable tensors inside the loops; only convert
  to Python floats (`.item()`) when *recording* metrics.

## Two-Stage Training: Adam then L-BFGS

```python
import torch


def train_model(model, data, epochs_adam=1000, lbfgs_iters=500, nu=0.01):
    """Two-stage PINN training: Adam (stage 1) then L-BFGS (stage 2).

    `data` carries collocation points (x_e, y_e), boundary points
    (x_b, y_b) and boundary targets (target_b).
    """
    history = {"adam_loss": [], "lbfgs_loss": []}

    # --- Stage 1: Adam (robust global exploration) -------------------------
    adam = torch.optim.Adam(model.parameters(), lr=1e-3)
    for _ in range(epochs_adam):
        adam.zero_grad()
        loss, loss_e, loss_b = compute_loss(
            model, data.x_e, data.y_e, data.x_b, data.y_b, data.target_b, nu=nu
        )
        loss.backward()
        adam.step()
        history["adam_loss"].append(loss.item())

    # --- Stage 2: L-BFGS (sharp local convergence) --------------------------
    # L-BFGS re-evaluates the loss multiple times per step, so PyTorch requires
    # a closure that zeroes gradients, recomputes the loss, and backpropagates.
    lbfgs = torch.optim.LBFGS(
        model.parameters(),
        max_iter=lbfgs_iters,
        tolerance_grad=1e-9,
        tolerance_change=1e-11,
        history_size=50,
        line_search_fn="strong_wolfe",
    )

    def closure():
        lbfgs.zero_grad()
        loss, _, _ = compute_loss(
            model, data.x_e, data.y_e, data.x_b, data.y_b, data.target_b, nu=nu
        )
        loss.backward()
        history["lbfgs_loss"].append(loss.item())
        return loss

    lbfgs.step(closure)
    return history
```

## Validation

```python
def validate(model, data, nu=0.01):
    """Evaluate PDE-residual and boundary losses without optimizer updates.

    Note: residuals need autograd w.r.t. coordinates, so do NOT wrap the
    residual computation in torch.no_grad(); simply avoid calling backward().
    """
    loss, loss_e, loss_b = compute_loss(
        model, data.x_e, data.y_e, data.x_b, data.y_b, data.target_b, nu=nu
    )
    return {
        "val_loss": loss.item(),
        "residual_loss": loss_e.item(),
        "boundary_loss": loss_b.item(),
    }
```

## Data Handling & Loaders

```python
from dataclasses import dataclass

import torch
from torch.utils.data import Dataset, DataLoader


@dataclass
class MinMaxScaler:
    min_xy: torch.Tensor
    max_xy: torch.Tensor

    def transform(self, xy: torch.Tensor) -> torch.Tensor:
        denom = (self.max_xy - self.min_xy).clamp_min(1e-8)
        return (xy - self.min_xy) / denom


class PINNDataset(Dataset):
    """Stores interior and boundary points with explicit coordinate scaling."""

    def __init__(self, x_all, y_all, u_bc, v_bc, p_bc, boundary_mask):
        xy_all = torch.cat([x_all, y_all], dim=1).float()
        self.scaler = MinMaxScaler(
            min_xy=xy_all.min(dim=0).values,
            max_xy=xy_all.max(dim=0).values,
        )

        xy_scaled = self.scaler.transform(xy_all)
        interior_mask = ~boundary_mask

        # Interior collocation points for PDE residuals
        self.xy_interior = xy_scaled[interior_mask]

        # Boundary points and targets for supervised boundary loss
        self.xy_boundary = xy_scaled[boundary_mask]
        self.bc_targets = torch.cat([u_bc, v_bc, p_bc], dim=1).float()[boundary_mask]

    def __len__(self):
        return self.xy_interior.shape[0]

    def __getitem__(self, idx):
        interior_xy = self.xy_interior[idx]

        # Pair one boundary sample with each interior sample for joint loss updates.
        boundary_idx = idx % self.xy_boundary.shape[0]
        boundary_xy = self.xy_boundary[boundary_idx]
        boundary_target = self.bc_targets[boundary_idx]
        return {
            "x_e": interior_xy[0:1],
            "y_e": interior_xy[1:2],
            "x_b": boundary_xy[0:1],
            "y_b": boundary_xy[1:2],
            "target_b": boundary_target,
        }


dataset = PINNDataset(x_all, y_all, u_bc, v_bc, p_bc, boundary_mask)
loader = DataLoader(
    dataset,
    batch_size=512,
    shuffle=True,
    num_workers=4,
    persistent_workers=True,
)
```

Use the `loader` batches inside `train_model(...)` to feed interior residual and
boundary condition terms every step.

## Pitfalls

1. **L-BFGS without a closure** raises a runtime error — the closure is
   mandatory because L-BFGS re-evaluates the objective during line search.
2. **`torch.no_grad()` around residual validation** silently breaks
   `torch.autograd.grad` on the coordinates; keep the graph alive and just
   skip `backward()`/`step()`.
3. **Reusing the Adam optimizer state for L-BFGS** is invalid — construct a
   fresh `torch.optim.LBFGS` after stage 1.
4. Keep stage sizes small for CPU smoke runs (e.g. `epochs_adam=200`,
   `lbfgs_iters=100`) — the harness enforces wall-clock ceilings.
