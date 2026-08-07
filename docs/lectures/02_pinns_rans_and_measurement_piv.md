# Module 2 — Physics-Informed Neural Networks (PINNs), RANS Closures & Measurement Enhancement

**Source material:** `Lecture1.txt` (final section), `Lecture2.txt` (full), slide deck `1_Time_PINNs.pdf` (slides 34–end, PINNs section).
**Scope:** PINN formulation for the 2D RANS equations, automatic-differentiation mechanics, five progressively harder test cases (laminar → separated turbulent flow), and two experimental-measurement applications (PIV correction, denoising).

---

## 1. Mathematical Foundations

### 1.1 Governing equations: 2D incompressible RANS

No turbulence model or closure assumption is introduced. The raw, unclosed 2D RANS equations are:

**Continuity:**
$$
\frac{\partial U}{\partial x} + \frac{\partial V}{\partial y} = 0
$$

**Streamwise momentum:**
$$
U\frac{\partial U}{\partial x} + V\frac{\partial U}{\partial y} = -\frac{\partial P}{\partial x} + \frac{1}{Re}\left(\frac{\partial^2 U}{\partial x^2} + \frac{\partial^2 U}{\partial y^2}\right) - \frac{\partial \overline{u'^2}}{\partial x} - \frac{\partial \overline{u'v'}}{\partial y}
$$

**Wall-normal momentum:**
$$
U\frac{\partial V}{\partial x} + V\frac{\partial V}{\partial y} = -\frac{\partial P}{\partial y} + \frac{1}{Re}\left(\frac{\partial^2 V}{\partial x^2} + \frac{\partial^2 V}{\partial y^2}\right) - \frac{\partial \overline{u'v'}}{\partial x} - \frac{\partial \overline{v'^2}}{\partial y}
$$

Capital letters denote mean quantities. The Reynolds stresses $\overline{u'^2}, \overline{v'^2}, \overline{u'v'}$ are **additional unknowns with no extra equations** — this is the classical RANS closure problem. Instead of an eddy-viscosity/mixing-length model, **the PINN solves for all unknowns simultaneously as direct network outputs.**

### 1.2 PINN construction via automatic differentiation

The network is a standard MLP:

$$
(x, y) \;\longrightarrow\; \text{MLP} \;\longrightarrow\; (U, V, P, \overline{u'^2}, \overline{v'^2}, \overline{u'v'})
$$

Because the same automatic-differentiation machinery used for backpropagation can compute *any* partial derivative of the network's output with respect to its input, the PDE terms are built directly:

$$
U_x = \frac{\partial U}{\partial x}, \quad U_y = \frac{\partial U}{\partial y}, \quad U_{xx} = \frac{\partial^2 U}{\partial x^2}, \quad \ldots
$$

using `autograd`/`GradientTape`, and assembled into the three residuals:

$$
f_1 = U U_x + V U_y + P_x - \frac{1}{Re}(U_{xx}+U_{yy}) + (\overline{u'^2})_x + (\overline{u'v'})_y
$$
$$
f_2 = U V_x + V V_y + P_y - \frac{1}{Re}(V_{xx}+V_{yy}) + (\overline{u'v'})_x + (\overline{v'^2})_y
$$
$$
f_3 = U_x + V_y
$$

with all terms moved to one side so that $f_1 = f_2 = f_3 = 0$ at convergence.

**Critical distinction (a recurring point of student confusion in Lecture2):** the spatial partial derivatives ($U_x$, etc.) are used only to *construct* $f_1, f_2, f_3$. The loss gradient used for *training* is $\partial \mathcal{L}/\partial(\text{weights})$, computed by a **separate** backpropagation pass through the whole computational graph (including the derivative-taking operations) — not a derivative with respect to $x$ or $y$.

### 1.3 Total loss: supervised + unsupervised

$$
\mathcal{L} = \underbrace{\frac{1}{N_c}\sum_{k=1}^{N_c}\left(f_1^2 + f_2^2 + f_3^2\right)_k}_{\text{unsupervised: PDE residual at collocation points}} \;+\; \underbrace{\frac{1}{N_b}\sum_{k=1}^{N_b}\left\| \hat{\mathbf{q}}_k - \mathbf{q}_k \right\|^2}_{\text{supervised: boundary-condition loss}}
$$

- $N_c$ = number of **collocation points** (interior, unsupervised — governing-equation residual only).
- $N_b$ = number of **boundary points** (known/measured data — Dirichlet values in every case shown).
- Both terms can be independently weighted; the reference implementation uses equal (1:1) weighting.
- **This is a soft constraint, not a hard one.** Boundary values are *not* strictly enforced as in a classical solver — they are minimized in a least-squares sense, exactly like the interior residual.

### 1.4 Laminar reference case: Falkner–Skan similarity equation

Test case 1 (a laminar boundary layer with pressure gradient, the pressure-gradient extension of the Blasius solution) reduces under a similarity transform $f(\eta)$ to a single ODE:

$$
f''' + f f'' + \beta\left(1 - f'^2\right) = 0
$$

This is solvable in seconds by conventional means — its purpose here is purely as a **near-exact validation baseline** for the full-equation PINN before moving to turbulent cases where no closed-form reference exists.

### 1.5 Diagnostic quantities used across all test cases

$$
H = \frac{\delta^*}{\theta} \quad \text{(shape factor: displacement thickness / momentum thickness)}
$$
$$
C_f = \frac{\tau_w}{\tfrac{1}{2}\rho U_\infty^2} \quad \text{(skin-friction coefficient)}
$$

Both are reported as functions of streamwise development, in addition to inner-scaled ($+$-unit) mean-velocity and Reynolds-shear-stress profiles at multiple streamwise stations.

---

## 2. Architecture Topology & Hyperparameters

**Reference implementation:** Eivazi et al., *Physics of Fluids* 34, 075117 (2022) — TensorFlow 2, full open-source code and data.

| Hyperparameter | Value |
|---|---|
| Network type | Multilayer perceptron (MLP) |
| Hidden layers | **8** |
| Neurons per layer | **20** |
| Activation function | Hyperbolic tangent ($\tanh$) |
| Optimizers | Adam, then **BFGS / L-BFGS-B** refinement |
| Training mode | Full-batch (no mini-batching) |
| Pre-processing | Data normalization |
| Inputs | $(x, y)$ coordinates only |
| Outputs | $U, V, P, \overline{u'^2}, \overline{v'^2}, \overline{u'v'}$ |
| Training data required | **Boundary/domain data only** — no interior labels |

### 2.1 Test-case-by-test-case results

| Test case | Flow regime | Data source | Mean-flow error | Reynolds-stress error | Notes |
|---|---|---|---|---|---|
| 1. Falkner–Skan boundary layer | Laminar, pressure gradient | Similarity solution | **<0.1%** in $U, V$ | Pressure error ≈ 0 | No Reynolds stresses (laminar) |
| 2. ZPG turbulent boundary layer | Turbulent, zero pressure gradient, $Re_\theta$ up to 7,000 | Eitel-Amor et al., *IJHFF* 47, 57 (2014) — DNS | **1%** | **6%** | Shape factor & $C_f$ in good agreement |
| 3. APG turbulent boundary layer | Turbulent, adverse pressure gradient (decelerating flow) | Bobke et al., *JFM* 820, 667 (2017) — DNS | **<1%** | **8%** | |
| 4. NACA4412 airfoil | Turbulent, strong/rapidly-growing pressure gradient | Vinuesa et al., *IJHFF* 72, 86 (2018), $Re=200{,}000$ (data up to $Re=1{,}000{,}000$ available) | **<2%** | **~10%** | Pronounced Reynolds-stress anisotropy well captured |
| 5. Periodic hill | Turbulent, **separated** flow, recirculation + reattachment | — | **~3%** | **15–30%** | Hardest case: separation is notoriously difficult for RANS/LES too |

**Framing used throughout:** these accuracy levels are explicitly claimed to be **better than a typical industrial RANS solver**, which relies on a Boussinesq/eddy-viscosity closure with inherent modeling error — the PINN gets no such closure and instead solves the exact (unclosed-but-unmodeled) equations by construction.

### 2.2 Experimental-measurement applications

| Application | Reference | Task |
|---|---|---|
| PIV correction (ZPG TBL) | Hasanuzzaman et al., *Meas. Sci. Technol.* 34, 044002 (2023) | Correct the wall-normal velocity component $V$ (3 orders of magnitude smaller than $U$, essentially unmeasurable directly by PIV) using the governing-equation constraint |
| Denoising (2D cylinder wake, unsteady) | Eivazi et al., *Meas. Sci. Technol.* 35, 075303 (2024) | Remove artificially injected Gaussian noise from an unsteady flow field using an LSTM-augmented PINN; POD-mode evolution recovered accurately |

---

## 3. Practical Insights & Edge Cases (Prof. Ricardo's Q&A)

- **"Are PINNs faster than CFD?"** — Asked and answered *repeatedly and emphatically* across all three lectures: **No.** "PINNs are much, much, much, much slower than finite elements or CFD... at least an order of magnitude slower... keep in mind that the claim that PINNs are faster is wrong." This is flagged as one of the most common misconceptions.
- **When are PINNs actually worth the extra cost?**
  1. Complex meshes that are hard to mesh conventionally — PINNs are more robust to mesh complexity.
  2. Embedding sparse/scattered experimental data directly into the solve.
  3. Coarser meshes suffice because automatic differentiation gives **exact** derivatives — you don't need to numerically resolve steep gradients the way a finite-difference/volume stencil does.
  4. High-value Reynolds-stress accuracy without a closure assumption (RANS solvers cannot match this).
- **PINNs are not a CFD replacement, and not combinable with a commercial solver as a hybrid accuracy booster** — both approaches solve the same PDEs by different means; you pick one or the other for a given case, you don't splice them together.
- **Unsteady/transient problems are a known weak point.** Two failure modes discussed:
  1. Treating time as an extra MLP input coordinate — the MLP fundamentally can't learn temporal dependencies (same limitation as Module 1 §1.2).
  2. Combining PINNs with LSTM-like temporal architectures — technically possible (and used for the 2024 denoising paper) but "not always very robust" to train; the joint residual+loss optimization becomes fragile.
  - Direct quote: *"I would just not prioritize unsteady problems with PINNs."*
- **High-frequency content in unsteady PINNs** is a non-issue *by construction* here, since the course's PINN applications target **statistics**, not instantaneous unsteady fields — so the question of "does it resolve high-frequency signals" doesn't arise for the RANS use case.
- **Boundary conditions are Dirichlet-only** in this framework; Neumann conditions are "potentially possible" (automatic differentiation can compute the needed gradient and set a residual on it) but **untested by this group**, and expected to be more numerically unstable, likely requiring denser collocation points near the boundary.
- **No formal mesh-convergence study exists for PINNs** the way it does for FEM/FVM. The practical substitute is: choose collocation-point distributions dense enough that information propagates from the interior to the boundaries, and monitor whether the *loss* (not a discretization-error estimate) is acceptably low.
- **PINNs can converge to unphysical solutions.** Unlike a classical numerical solver, convergence of the PINN loss does **not** guarantee a physically valid result — poor boundary-condition placement or inadequate collocation sampling can converge to something numerically low-residual but wrong. This is an explicit, named risk, distinguishing PINNs from traditional solvers.
- **What can go wrong if total loss is small but the solution is still inaccurate?** If the boundary term dominates the loss weighting, you can get an excellent boundary reconstruction and a poor interior solution — loss-term balance matters and is not automatic.
- **Denoising without a reference/ground truth ("blind denoising"):** the key advantage over autoencoder-based denoising is that PINNs **do not require a paired clean/noisy training set** — the governing equations themselves act as the implicit prior/regularizer that any physically consistent (denoised) field must satisfy. (Contrast: an autoencoder-based denoiser needs a canonical high-fidelity dataset to learn a clean/noisy mapping from.)
- **"Should I add flow-invariant terms to the loss to help convergence?"** — Explicitly discouraged: added complexity to the loss definition is more likely to hurt convergence than help it for this class of problem.
- **ROM vs. PINN**: different philosophies — ROM primarily leverages *data* (and optionally the governing equations via Galerkin projection); PINNs primarily leverage the *governing equations* (and minimal boundary data). Neither is universally "more accurate" — it depends on whether trustworthy governing equations exist for the phenomenon of interest.
- **Multi-phase / discontinuous flows**: PINNs have been applied but face additional interface-stability challenges; efficiency trade-off vs. CFD is the same (slower, but can tolerate a coarser mesh).

---

## 4. Physical Diagnostic Framework

Any PINN-based RANS solve or measurement-correction task in this repo must report:

1. **Per-equation residual**, not just total loss — report $f_1$ (x-momentum), $f_2$ (y-momentum), and $f_3$ (continuity) residual norms **separately**, since a small total loss can hide an imbalanced/poorly-converged individual equation.
2. **Supervised vs. unsupervised loss split** — report $\mathcal{L}_{\text{BC}}$ and $\mathcal{L}_{\text{residual}}$ individually, and the weighting used between them.
3. **Boundary-layer development diagnostics**: shape factor $H(x)$ and skin-friction coefficient $C_f(x)$ compared against the DNS/reference baseline across the full streamwise extent, not just at isolated stations.
4. **Inner-scaled profile comparison** ($U^+$, $\overline{u'v'}^+$ vs. $y^+$) at a minimum of three streamwise/spanwise stations per case.
5. **Relative error, split by quantity type** — mean-flow error and Reynolds-stress error must be reported **separately** (they differ by up to an order of magnitude in every test case above; conflating them hides where the model is weak).
6. **For measurement-correction tasks** (PIV/denoising): report the corrected quantity against an independent higher-fidelity reference (LES/DNS), *not* just internal consistency, since the whole point is correcting a measurement that has no self-consistent ground truth.
7. **Acceptance bar for this repo** (derived from the observed results above): mean-flow error under ~2% and Reynolds-stress error under ~10% for attached flows; a separated-flow case (periodic-hill-like) may reasonably run to 15–30% Reynolds-stress error and should be flagged as such rather than compared against the attached-flow bar.

---

## 5. Implementation Logic

### 5.1 PINN forward pass and residual construction (PyTorch)

```python
import torch
import torch.nn as nn

class RANS_PINN(nn.Module):
    """8 hidden layers, 20 neurons/layer, tanh activation.
    Input: (x, y). Output: (U, V, P, uu, vv, uv) -- mean flow + Reynolds stresses.
    """
    def __init__(self, hidden_layers: int = 8, hidden_dim: int = 20):
        super().__init__()
        layers = [nn.Linear(2, hidden_dim), nn.Tanh()]
        for _ in range(hidden_layers - 1):
            layers += [nn.Linear(hidden_dim, hidden_dim), nn.Tanh()]
        layers += [nn.Linear(hidden_dim, 6)]  # U, V, P, uu, vv, uv
        self.net = nn.Sequential(*layers)

    def forward(self, xy: torch.Tensor) -> torch.Tensor:
        return self.net(xy)


def rans_residuals(model: RANS_PINN, xy: torch.Tensor, inv_Re: float):
    """xy: (N, 2) collocation points, requires_grad=True."""
    xy = xy.clone().requires_grad_(True)
    out = model(xy)
    U, V, P, uu, vv, uv = out.unbind(dim=1)

    grad_outputs = torch.ones_like(U)

    def d(f, wrt_idx):
        return torch.autograd.grad(f, xy, grad_outputs=grad_outputs,
                                    create_graph=True)[0][:, wrt_idx]

    U_x, U_y = d(U, 0), d(U, 1)
    V_x, V_y = d(V, 0), d(V, 1)
    P_x, P_y = d(P, 0), d(P, 1)
    uu_x = d(uu, 0)
    uv_x, uv_y = d(uv, 0), d(uv, 1)
    vv_y = d(vv, 1)

    # second derivatives for the viscous term
    U_xx = torch.autograd.grad(U_x, xy, grad_outputs=grad_outputs, create_graph=True)[0][:, 0]
    U_yy = torch.autograd.grad(U_y, xy, grad_outputs=grad_outputs, create_graph=True)[0][:, 1]
    V_xx = torch.autograd.grad(V_x, xy, grad_outputs=grad_outputs, create_graph=True)[0][:, 0]
    V_yy = torch.autograd.grad(V_y, xy, grad_outputs=grad_outputs, create_graph=True)[0][:, 1]

    f1 = U * U_x + V * U_y + P_x - inv_Re * (U_xx + U_yy) + uu_x + uv_y
    f2 = U * V_x + V * V_y + P_y - inv_Re * (V_xx + V_yy) + uv_x + vv_y
    f3 = U_x + V_y
    return f1, f2, f3
```

### 5.2 Total loss assembly

```python
def pinn_loss(model, xy_collocation, xy_boundary, q_boundary, inv_Re,
              w_residual: float = 1.0, w_boundary: float = 1.0):
    f1, f2, f3 = rans_residuals(model, xy_collocation, inv_Re)
    loss_residual = (f1.pow(2) + f2.pow(2) + f3.pow(2)).mean()

    q_pred_boundary = model(xy_boundary)[:, :3]   # compare U, V, P at BCs
    loss_boundary = ((q_pred_boundary - q_boundary) ** 2).mean()

    total = w_residual * loss_residual + w_boundary * loss_boundary
    return total, {"residual": loss_residual.item(), "boundary": loss_boundary.item()}
```

### 5.3 Two-stage optimization (Adam → L-BFGS-B), matching the reference setup

```python
def train_pinn(model, xy_collocation, xy_boundary, q_boundary, inv_Re,
               adam_steps: int = 20000, lbfgs_steps: int = 5000):
    adam = torch.optim.Adam(model.parameters(), lr=1e-3)
    for step in range(adam_steps):
        adam.zero_grad()
        loss, parts = pinn_loss(model, xy_collocation, xy_boundary, q_boundary, inv_Re)
        loss.backward()
        adam.step()

    lbfgs = torch.optim.LBFGS(model.parameters(), max_iter=lbfgs_steps,
                               line_search_fn="strong_wolfe")

    def closure():
        lbfgs.zero_grad()
        loss, _ = pinn_loss(model, xy_collocation, xy_boundary, q_boundary, inv_Re)
        loss.backward()
        return loss

    lbfgs.step(closure)
    return model
```

### 5.4 Physics-validation gate (per-equation residual check)

Per `docs/copilot/physics_validation_rules.md` rule 1 and the PINN-specific rule, the residuals must be reported **individually**, not just as a summed loss:

```python
def validate_pinn_residuals(model, xy_test, inv_Re, tol: float = 1e-3):
    f1, f2, f3 = rans_residuals(model, xy_test, inv_Re)
    report = {
        "continuity_rms": f3.pow(2).mean().sqrt().item(),
        "x_momentum_rms": f1.pow(2).mean().sqrt().item(),
        "y_momentum_rms": f2.pow(2).mean().sqrt().item(),
    }
    for name, val in report.items():
        assert val < tol, f"{name} residual {val:.2e} exceeds tolerance {tol:.2e}"
    return report
```
