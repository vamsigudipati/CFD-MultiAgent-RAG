# Benchmark Validation Matrix: Spec-Driven Generation Targets

Canonical CFD benchmark problems selected for the spec-driven generation pillar.
Each is a rigorously documented *traditional* benchmark with authoritative
reference data but **no out-of-the-box ML implementation** — making them ideal
proving grounds for specification-to-surrogate synthesis.

Status legend: `PLANNED` → `SPEC_DRAFTED` → `GENERATED` → `GATES_PASSED` → `VALIDATED`

---

## Benchmark 1: 2D Lid-Driven Cavity Flow

| Field | Value |
|---|---|
| **Physics** | Steady incompressible Navier-Stokes; recirculating flow driven by a moving lid |
| **Domain** | Unit square $[0,1] \times [0,1]$ |
| **Conditions** | $Re = 100$ (extendable to 400, 1000); lid $u=1, v=0$ at $y=1$; no-slip on remaining walls |
| **Reference data** | Ghia, Ghia & Shin (1982) centerline velocity tabulations |
| **Why it's ideal** | The canonical incompressible benchmark: simple geometry, closed physics, singular corner behavior stresses residual formulation quality |
| **Architecture mode** | `continuous_pinn` (steady MLP, outputs $u, v, p$) |
| **Status** | `PLANNED` |

## Benchmark 2: Flow Over a Circular Cylinder at $Re = 100$

| Field | Value |
|---|---|
| **Physics** | Unsteady incompressible Navier-Stokes; laminar vortex shedding (von Kármán street) |
| **Domain** | Rectangular channel with cylinder of diameter $D$; time-dependent, $t$ added as network input |
| **Conditions** | Uniform inlet; no-slip cylinder surface; far-field/outflow conditions; $Re = 100$ |
| **Reference data** | Strouhal number $St \approx 0.164$; mean drag coefficient $\bar{C}_D \approx 1.33$; Williamson (1996) shedding correlations |
| **Why it's ideal** | Tests unsteady transition: periodic dynamics, wake spectra, and curved-boundary separation — the hardest of the three |
| **Architecture mode** | `continuous_pinn` (space-time inputs $x, y, t$; outputs $u, v, p$) |
| **Status** | `PLANNED` |

## Benchmark 3: Flat Plate Thermal Boundary Layer

| Field | Value |
|---|---|
| **Physics** | Laminar boundary layer with convective heat transfer (momentum + energy equations) |
| **Domain** | Semi-infinite flat plate, similarity region $0 < x \le L$ |
| **Conditions** | Uniform free stream $U_\infty, T_\infty$; isothermal wall $T_w$; $Pr = 0.7$ (air) |
| **Reference data** | Blasius similarity solution (momentum); Pohlhausen solution and $Nu_x = 0.332\,Re_x^{1/2} Pr^{1/3}$ (thermal) |
| **Why it's ideal** | Adds a scalar transport equation (temperature) to the output head and residual, exercising multi-physics loss composition with an exact analytical target |
| **Architecture mode** | `continuous_pinn` (outputs $u, v, T$; energy-equation residual added to $L_e$) |
| **Status** | `PLANNED` |

---

## Gate Coverage Matrix

Mapping of each benchmark to the immutable Green Layer validation gates.
✅ = gate applies as-is · 🔧 = gate applies with benchmark-specific parametrization · ➕ = new gate/fixture required

| Green Layer Gate | Purpose | Cavity | Cylinder $Re{=}100$ | Thermal Plate |
|---|---|---|---|---|
| **T0 — Static audit** (param count, symbol contract) | Catches structural drift before any compute | ✅ | ✅ | ✅ |
| **T1 — Gradient plumbing** (overfit sanity, ≤10x margin) | Verifies loss → gradient → update path is alive | ✅ | ✅ | ✅ |
| **T2 — MMS residual** (CPU/float64, Taylor-Green analytic) | Proves residual math is exact to machine precision | ✅ | 🔧 unsteady MMS variant with $\partial_t$ terms | ➕ energy-equation MMS entry in the registry |
| **T2 — Spectral fidelity** (one-sided HF upper bound) | Rejects noisy/checkerboard predictions | ✅ | 🔧 evaluated on wake-region slices | ✅ |
| **PINN gates** (coordinate mapping, autograd continuity) | Ensures $\partial u/\partial x$, $\partial v/\partial y$ connectivity survives | ✅ | 🔧 extended to $\partial/\partial t$ | 🔧 extended to $\partial T/\partial x, \partial T/\partial y$ |
| **T3 — Short-train regression** (multi-seed, timeout-guarded) | Confirms trainability within wall-clock ceilings | ✅ | ✅ | ✅ |

## Benchmark-Specific Validation Targets (beyond gates)

| Benchmark | Quantitative acceptance criterion | Source of truth |
|---|---|---|
| Lid-driven cavity | Centerline $u(y)$ and $v(x)$ profiles within 5% RMS of tabulated values at $Re=100$ | Ghia et al. (1982) |
| Circular cylinder | Predicted $St$ within ±10% of 0.164; $\bar{C}_D$ within ±10% of 1.33 | Williamson (1996) |
| Thermal flat plate | Local Nusselt number within 5% of $0.332\,Re_x^{1/2}Pr^{1/3}$ over the similarity region | Pohlhausen / Blasius |

## Execution Plan

1. Draft each problem as a raw markdown specification per
   [../workflows/specification_to_ml.md](../workflows/specification_to_ml.md) (Path B).
2. Land the two harness extensions flagged ➕/🔧 above **before** the first
   generation run (unsteady MMS variant; energy-equation MMS registry entry) —
   gates must precede generation to preserve the trust model.
3. Run each benchmark through the orchestrator on its own thread
   (`cavity-spec-run-NNN`, `cylinder-spec-run-NNN`, `thermal-plate-spec-run-NNN`)
   and update the **Status** rows in this file as evidence accumulates.
