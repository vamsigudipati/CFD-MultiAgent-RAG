# MLOps Scaling Rules

Pull this file in with `#file:docs/copilot/mlops_scaling_rules.md` for any task touching training infrastructure, distributed training, experiment tracking, or dataset pipelines.

## Experiment tracking
- Every training run must log: config (full hyperparameters), git commit hash, dataset version/hash, and final validation metrics to a tracked run (MLflow or Weights & Biases — pick one per project and stay consistent, don't mix).
- No hyperparameters hardcoded in training scripts — use a config file (Hydra/YAML or equivalent) so runs are diffable and reproducible.

## Reproducibility
- Fix all seeds (framework RNG, numpy, python `random`) at the top of every entrypoint.
- Log the exact package versions (`pip freeze` / `environment.yml` snapshot) alongside the run, since CFD numerics are sensitive to BLAS/cuDNN version drift.

## Distributed / scaled training
- Default to single-GPU correctness first; only introduce `DistributedDataParallel` (PyTorch) or `tf.distribute.MirroredStrategy`/`MultiWorkerMirroredStrategy` (TensorFlow) once the single-GPU run is validated against the physics baseline.
- Scale learning rate with effective batch size (linear or sqrt scaling — state which) whenever changing GPU/worker count; don't change batch size silently without adjusting LR.
- Use mixed precision (`torch.cuda.amp` / `tf.keras.mixed_precision`) only after confirming it doesn't degrade conservation residuals (see physics validation rules) — some PDE losses are numerically sensitive to fp16.

## Data pipeline
- Large CFD datasets (DNS fields, simulation snapshots) must be versioned (DVC, or equivalent content hash) — never assume "the data on disk" is stable across runs.
- Data loaders must document units and normalization applied (min-max, z-score, or physical rescaling) since silently changing normalization breaks physics-loss terms that reference dimensional quantities.

## CI/CD for training code
- Any PR touching training code must pass a fast smoke test: 1-epoch run on a tiny synthetic/subsampled dataset, asserting the loss is finite and decreasing.
- Full training runs are not part of CI — they're triggered manually or on a schedule, and their results are tracked, not gated.

## What "done" looks like for a scaling/infra task
- State the hardware target (# GPUs, single-node vs multi-node).
- State the tracking backend and where the run can be found (run ID/link).
- Confirm the smoke test passes before requesting a full run.
