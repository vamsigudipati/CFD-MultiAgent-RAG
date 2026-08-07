# Workflow: From Specification to Verified ML Model

This guide explains the two entry paths for producing a trained, physics-validated
surrogate model **without writing any ML code yourself**:

- **Path A — Drop in a traditional (non-ML) CFD paper.** The platform extracts
  the governing equations and boundary conditions and re-casts them as a
  physics-informed learning problem.
- **Path B — Supply a raw markdown problem statement.** No paper required; a
  structured engineering spec is a complete input.

Both paths converge into the same autonomous pipeline: blueprint → feasibility
check → physics plan → grounded code generation → immutable validation gates →
verified model artifact.

---

## Path A: Traditional CFD Paper → ML Solution

### 1. Ingestion & Extraction
Place the PDF in the paper repository. The extraction pipeline (math-aware OCR +
deterministic normalization) converts it into clean markdown with intact LaTeX
equations. For traditional papers, the items of interest are:

- **Governing equations** — e.g., incompressible Navier-Stokes, Euler, or an
  energy/advection-diffusion equation, exactly as formulated in the methodology
  section (including any turbulence closure such as RANS Reynolds-stress terms).
- **Boundary and initial conditions** — inlet profiles, no-slip walls, symmetry
  planes, far-field conditions, wall temperatures.
- **Domain definition** — geometry, characteristic lengths, non-dimensional
  groups (Re, Pr, Ma) and their reference values.
- **Reported results** — velocity profiles, drag/lift coefficients, Nusselt
  correlations — which become *validation targets*, not training data.

### 2. Blueprint Synthesis
The extracted markdown is distilled into a strict architectural blueprint with
YAML frontmatter: PDE family, closure status, boundary condition inventory,
normalization spec, and quantitative validation targets. A deterministic
feasibility kill-switch blocks papers whose physics is unclosed or whose data
requirements cannot be met — **before** any generation tokens are spent.

### 3. Physics Re-Casting
The physics reasoner maps every numerical-methods concept to its ML equivalent
using the [CFD-to-PINN mapping reference](cfd_to_pinn_mapping.md):

- PDEs become unsupervised residual loss terms evaluated by autograd.
- Boundary conditions become supervised loss terms on explicitly separated
  boundary points.
- The mesh/domain becomes scaled collocation sampling fed through a
  multi-process `DataLoader`.

### 4. Grounded Generation & Validation
The framework supervisor generates a single training/validation monolith,
grounded by the paper's own text (traceability matrix mandatory), framework
best-practice templates, and golden reference symbols. The immutable Green Layer
harness then runs the gate suite; failures are fingerprinted and routed back for
bounded self-healing. A model only exists as an artifact once every gate passes.

---

## Path B: Raw Problem Statement → ML Solution

### 1. Write the Specification
Author a markdown file describing the engineering problem. A complete spec
contains four blocks:

```markdown
# Problem: 2D Lid-Driven Cavity Flow

## Domain
Unit square [0,1] x [0,1]. Steady state. Re = 100 (nu = 0.01).

## Governing Equations
Incompressible Navier-Stokes (continuity + 2D momentum), non-dimensional form.

## Boundary Conditions
- Top lid (y=1): u = 1, v = 0 (moving wall)
- Left/right/bottom walls: u = 0, v = 0 (no-slip)
- Pressure: fixed reference p = 0 at one point.

## Targets
Predict steady (u, v, p) fields. Validate centerline u-velocity profile
against the Ghia et al. (1982) benchmark tabulation.
```

### 2. Automatic Blueprint Promotion
The spec is parsed into the same blueprint/frontmatter schema used for papers.
Missing required fields (unresolved PDE family, unclosed physics, absent
boundary inventory) trigger the deterministic `BLOCKED_DATA` kill-switch with a
precise report of what to add — the system never guesses physics.

### 3. Synthesis & Verification
From this point the pipeline is identical to Path A: the physics reasoner emits
an execution plan, the supervisor generates a grounded PINN/surrogate monolith
(custom `Dataset` with Min-Max coordinate scaling and boundary separation,
multi-process `DataLoader`, two-stage Adam → L-BFGS training), and the Green
Layer gates deliver the verdict. The output is a validated `train_and_val.py`
artifact in an isolated per-run workspace, plus logs and checkpoints for audit.

---

## What You Never Have To Do

- Hand-write residual losses or autograd plumbing.
- Choose optimizers, activations, or sampling strategies.
- Write tests — the validation harness is frozen, human-authored, and reused
  across every problem.
- Debug silent physics errors — gate failures are classified, fingerprinted,
  and either self-healed or reported with a terminal diagnosis.

## Where To Go Next

- Concept translation reference: [cfd_to_pinn_mapping.md](cfd_to_pinn_mapping.md)
- Benchmark problems & gate coverage: [../validation/benchmark_matrix.md](../validation/benchmark_matrix.md)
- Platform rationale for leadership: [../usecases/overview.md](../usecases/overview.md)
