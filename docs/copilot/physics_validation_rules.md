# Physics Validation Rules

Pull this file in with `#file:docs/copilot/physics_validation_rules.md` for any task touching a solver, reduced-order model (ROM), PINN loss, or turbulence-prediction network.

## Non-negotiable checks before accepting a model/solver change

1. **Conservation residuals.** Report mass/momentum (and energy, if compressible) residuals on the validation set. A change that increases residual norm by >5% vs. the last accepted baseline is a regression, not an improvement, even if the loss curve looks better.
2. **Non-dimensional consistency.** State Reynolds number (Re), CFL number, and any other governing non-dimensional parameters used to generate/validate data. Never compare runs across different Re without saying so explicitly.
3. **Boundary conditions.** Confirm BCs (no-slip, periodic, inflow/outflow) are enforced the same way in training data generation and in inference — a silent BC mismatch is the most common source of "the network learned the wrong physics" bugs.
4. **Baseline comparison required.** Any new architecture must be compared against at least one of:
   - An analytical/low-order reference (e.g., the Moehlis et al. 2004 nine-equation shear-flow model) where applicable.
   - A DNS/experimental dataset already used elsewhere in this project.
   - A prior model checkpoint (regression test), if no external baseline exists.
5. **Statistical validation, not just pointwise error.** Report first- and second-order turbulence statistics (mean, RMS, Reynolds stresses) in addition to instantaneous field error — a model can have low pointwise MSE and still fail to reproduce turbulence statistics.
6. **Dynamical behavior for time-series/ROM models.** For LSTM/Koopman/RNN-based temporal predictors, report Lyapunov exponents and/or Poincaré maps, not just short-horizon prediction error — long-term statistical fidelity is the actual goal, per the chaotic-flow literature in this repo's reference list.

## PINN-specific rules
- Report each loss term (data, PDE residual, BC, IC) separately, not just the summed loss — weight imbalance between terms is the #1 PINN failure mode.
- State the collocation point sampling strategy and count; random reshuffling per epoch must be seeded for reproducibility.

## What "done" looks like for a physics validation task
- A short table: metric name, baseline value, new value, pass/fail against the 5% threshold in rule 1.
- Explicit note of which Re/geometry/BC configuration was tested.
- If any rule above can't be checked (e.g., no baseline exists yet), say so — don't silently skip it.
