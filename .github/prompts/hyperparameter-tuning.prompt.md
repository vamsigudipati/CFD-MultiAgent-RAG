---
description: "Generate a hyperparameter sweep plan (search space + tool config) for a CFD/ML training run, following this repo's MLOps scaling rules."
agent: "agent"
argument-hint: "Name the model/script to tune and the metric to optimize"
---
# Hyperparameter Tuning

For the model/script the user names:

1. **Identify tunable hyperparameters** actually present in the code (learning rate, batch size, network width/depth, PDE-loss weight terms for PINNs, sequence length for LSTM/RNN). Don't invent parameters that don't exist in the script.
2. **Propose a search space** (ranges or discrete choices) sized to the compute budget the user states; default to a small grid/random search (≤20 trials) unless told otherwise.
3. **Generate the sweep config** for the tool already used in this repo (Optuna, Ray Tune, or W&B Sweeps — ask if none is set up yet, don't assume).
4. **Apply MLOps rules automatically** from `docs/copilot/mlops_scaling_rules.md`: seed fixing, config-driven hyperparameters, experiment tracking fields — cite the rule, don't restate its full text.
5. **Note the physics guardrail**: if the loss includes a PDE/physics term, remind the user that the winning config still must pass `docs/copilot/physics_validation_rules.md` checks, not just minimize validation loss.
6. Output the config file/script diff only — no extra explanation of what hyperparameter tuning is.
