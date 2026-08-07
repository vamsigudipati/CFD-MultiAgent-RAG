# Why This Platform Matters

*A user-centric overview for researchers, computational fluid dynamicists, and engineering leaders.*

---

## The Problem We Solve

Machine learning for fluid dynamics has a reproducibility crisis. Every published
SciML paper ships with (at best) a one-off codebase that rots within months:
dependencies pin themselves to dead versions, datasets move or disappear, and the
subtle physics assumptions baked into the training script are documented nowhere.
Meanwhile, decades of *traditional* CFD literature — finite-volume solvers,
benchmark validations, boundary-layer correlations — contain rigorously verified
physics that has **no ML implementation at all**.

This platform closes both gaps. It is an automated research-to-production factory
that converts three kinds of input into **verified, physics-validated ML models**:

1. **ML-CFD papers** (e.g., PINN or CNN surrogate papers) — reproduced faithfully,
   with every architecture claim traced back to the paper's own text.
2. **Traditional, non-ML CFD papers** — governing equations and boundary conditions
   are extracted and re-cast as physics-informed learning problems.
3. **Raw engineering problem specifications** — a plain markdown problem statement
   (domain, equations, boundary conditions, targets) is enough to synthesize a
   trained surrogate model.

## What Makes It Different

### Industrialized Trust
Generated code is never trusted on sight. Every model must pass an **immutable
validation harness** — a frozen suite of physics gates (parameter audits, gradient
plumbing checks, Method-of-Manufactured-Solutions residual tests, spectral fidelity
checks) that the code-generating AI cannot see, edit, or game. If an LLM writes
code that merely *looks* plausible, the gates fail loudly and the system self-heals
with a bounded retry budget. The result is "prove it passes," not "trust me."

### Elimination of Code Rot
Instead of preserving fragile repositories, the platform preserves the
**specification**: the blueprint, the physics constraints, and the validation
gates. Code is regenerated on demand against current frameworks, then re-verified.
When PyTorch moves forward, your models move with it — the physics contract is the
durable artifact, not the script.

### Cross-Paper Normalization
Every paper — regardless of author style, framework, or notation — is distilled
into the same structured blueprint format with typed physical constraints. This
means results across dozens of papers become *comparable*: same gates, same
tolerances, same failure taxonomy. Engineering leaders get an apples-to-apples
portfolio view of which methods actually validate, instead of a pile of
incompatible readmes.

### Anti-Hallucination by Construction
Generation is grounded, not free-form. The system injects:
- **the paper's own extracted text** (so architectural claims are cited, not invented),
- **a mandatory traceability matrix** (every design decision maps to a section and page),
- **framework best-practice templates** (verified optimizer patterns, data pipelines),
- **golden reference code** from AST-indexed, state-of-the-art repositories.

### Spec-Driven ML Generation
You do not need a paper at all. A raw problem statement — *"incompressible flow in
a lid-driven cavity, Re = 100, no-slip walls, predict the steady velocity and
pressure fields"* — is a complete input. The platform maps equations to residual
losses, boundaries to supervised losses, and the domain to scaled collocation
sampling, then trains and validates the surrogate autonomously. See
[docs/workflows/specification_to_ml.md](../workflows/specification_to_ml.md).

## Who Benefits

| Audience | What you get |
|---|---|
| **Researchers** | Faithful, cited reproductions of literature models; a harness that catches silent physics errors before they contaminate results. |
| **Computational fluid dynamicists** | A bridge from familiar numerical concepts (meshes, BCs, residuals) to their ML equivalents — without learning deep-learning plumbing. See the [CFD-to-PINN mapping guide](../workflows/cfd_to_pinn_mapping.md). |
| **Engineering leaders** | A dependable pipeline: papers or specs in, validated surrogate models out, with auditable logs, checkpoints, and pass/fail evidence for every run. |

## The Three Pillars

1. **Paper Reproduction** — ML-CFD literature → traced, validated reimplementation.
2. **Traditional CFD Conversion** — classic numerical papers → physics-informed ML solutions.
3. **Spec-Driven Synthesis** — raw engineering problem statements → trained, gate-verified surrogates.

Progress against canonical benchmark problems for pillars 2 and 3 is tracked in the
[benchmark validation matrix](../validation/benchmark_matrix.md).
