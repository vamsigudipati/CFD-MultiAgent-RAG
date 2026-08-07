# Reference: Mapping Traditional CFD Concepts to PINN / Surrogate Equivalents

*A translation table for computational fluid dynamicists moving from numerical
solvers to physics-informed machine learning — no deep-learning background assumed.*

---

## The Core Idea

A traditional CFD solver discretizes the domain into a mesh, then iterates until
the discretized governing equations are satisfied everywhere. A PINN replaces the
mesh with a **neural network** $f_\theta(x, y) \rightarrow (u, v, p, \dots)$ and
replaces the solver iteration with **gradient-based training** that drives a
composite loss to zero:

$$
L = \underbrace{L_e}_{\text{PDE residuals (interior)}} + \underbrace{L_b}_{\text{boundary conditions}}
$$

Everything you already know about the problem — equations, boundaries, domain —
maps one-to-one onto a piece of this loss or its data pipeline.

## Mapping Table

| Traditional CFD Concept | PINN / Surrogate Equivalent | Where It Lives |
|---|---|---|
| Navier-Stokes / Euler equations | Unsupervised PDE residual loss $L_e$, evaluated via autograd | `navier_stokes_residuals(...)` + `compute_loss(...)` |
| Turbulence closure (e.g., RANS Reynolds stresses) | Additional network outputs whose gradients appear in the residual, exactly as the momentum equations specify | `forward_full(...)` output head |
| Inlets, walls, obstacles (BCs) | Supervised boundary loss $L_b$ on explicitly separated boundary points | `PINNDataset` boundary split + `L_b` term |
| Mesh & node distribution | Collocation point sampling over the continuous domain | `PINNDataset` interior points |
| Domain bounds / non-dimensionalization | Min-Max coordinate scaling to a unit hypercube | `MinMaxScaler` inside `PINNDataset` |
| Solver sweeps / batched updates | Mini-batched `DataLoader` with multi-processing workers | `DataLoader(dataset, batch_size, num_workers)` |
| Initial coarse iteration + refinement | Two-stage optimization: Adam (global exploration) then L-BFGS (sharp convergence) | `train_model(...)` |
| Residual convergence monitor | Validation metrics on residual and boundary losses, no optimizer steps | `validate(...)` |
| Grid-independence / verification study | Immutable Green Layer gates (MMS, gradient plumbing, spectral fidelity) | `modules/validation_harness/` |

## Detail: The Three Pillars of the Mapping

### 1. Navier-Stokes / Euler Equations → Unsupervised PDE Residual Loss ($L_e$)

In a solver, momentum and continuity are enforced by the discretization scheme.
In a PINN, the same equations are enforced by **automatic differentiation**: the
network's outputs are differentiated with respect to its coordinate *inputs*
(`torch.autograd.grad`), the residuals of continuity and momentum are assembled
symbolically, and their mean-square becomes $L_e$:

$$
L_e = \frac{1}{N_e}\sum_{i=1}^{N_e} \left( e_1^2 + e_2^2 + e_3^2 \right)\Big|_{(x_i, y_i)}
$$

No labels are needed — the physics *is* the supervision. If the paper (or spec)
uses RANS, every Reynolds-stress gradient term in the momentum equations must
appear in the residual, and the network must output those stresses.

### 2. Inlets, Walls, Obstacles → Supervised Boundary Loss ($L_b$)

Boundary conditions carry known values (no-slip: $u=v=0$; moving lid: $u=1$;
fixed wall temperature: $T=T_w$). These become ordinary supervised targets on
boundary points only:

$$
L_b = \frac{1}{N_b}\sum_{j=1}^{N_b} \left\| f_\theta(x_j, y_j) - \mathbf{g}(x_j, y_j) \right\|^2
$$

**Critical rule:** boundary points must be *explicitly separated* from interior
collocation points in the data pipeline — mixing them corrupts both loss terms.
The custom `Dataset` performs this split with a boundary mask at construction.

### 3. Mesh Conventions & Domain Bounds → Collocation Sampling and Scaling

A mesh is a fixed discretization; collocation points are its continuous
generalization — coordinates sampled anywhere in the domain, at which residuals
are evaluated. Two conventions from the numerical world carry over directly:

- **Non-dimensionalization → Min-Max scaling.** Just as solvers work best in
  non-dimensional form, networks train best when coordinates are normalized to
  $[0, 1]$. The `MinMaxScaler` inside the `Dataset` performs
  $\tilde{x} = (x - x_{\min}) / (x_{\max} - x_{\min})$ once, at ingestion.
- **Sweep batching → DataLoader multiprocessing.** Instead of a solver sweeping
  the mesh, a `DataLoader` streams shuffled mini-batches of collocation and
  boundary points with `num_workers` parallel processes, keeping the training
  loop saturated.

See the executable reference implementation in
[../framework_templates/pytorch_pinn_training.md](../framework_templates/pytorch_pinn_training.md)
(sections *Data Handling & Loaders* and *Two-Stage Training*).

## Common Pitfalls for CFD Practitioners

1. **Expecting a mesh-quality analogue.** Collocation density matters, but there
   is no CFL condition; instead watch the residual-loss plateau and the Green
   Layer gate results.
2. **Wrapping validation in `no_grad`.** PDE residuals need autograd with
   respect to coordinates even at validation time — skip `backward()`, not the
   graph.
3. **Treating reported paper results as training data.** Benchmark tabulations
   (e.g., Ghia et al. centerline profiles) are *validation targets* consumed by
   the harness, never fed into the loss.
4. **Generic templates for specific closures.** A RANS paper needs RANS
   residuals; the platform's traceability matrix enforces this, but spec authors
   should state the closure explicitly.
