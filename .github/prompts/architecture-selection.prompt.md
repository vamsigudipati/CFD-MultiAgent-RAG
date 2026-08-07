---
description: "Recommend a deep learning architecture (CNN, LSTM, Transformer, PINN, FNO, GNN) for a given CFD/turbulence modeling task."
agent: "agent"
argument-hint: "Describe the flow problem and prediction goal (e.g., 'predict near-wall velocity from wall shear stress, minimal channel flow, Re_tau=180')"
---
# Architecture Selection

Given the problem the user describes, do the following — concisely, no filler:

1. **Classify the task** into one of: spatial field reconstruction/super-resolution, temporal/dynamical forecasting, PDE-constrained regression (PINN), or reduced-order modeling (ROM).
2. **Recommend one primary architecture** and at most one alternative, justified in 2-3 bullet points referencing:
   - Input/output tensor structure (grid vs. point cloud vs. time series).
   - Whether the task needs to enforce PDE constraints (→ PINN) vs. purely data-driven (→ CNN/Transformer/LSTM).
   - Whether long-horizon dynamical fidelity matters (→ check Lyapunov/Poincaré requirements in `docs/copilot/physics_validation_rules.md`, prefer LSTM/Koopman-based frameworks).
3. **State the validation bar** this architecture must clear, pulling from `docs/copilot/physics_validation_rules.md` — don't repeat that file's content, just name which rules apply (e.g., "rules 4 and 6 apply here").
4. **Flag scaling implications** only if relevant (large 3D fields, high-res grids) by referencing `docs/copilot/mlops_scaling_rules.md`.
5. Stop there — do not generate the full implementation unless explicitly asked.
