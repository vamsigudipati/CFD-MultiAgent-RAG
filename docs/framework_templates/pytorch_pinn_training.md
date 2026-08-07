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
