# Copilot Instructions — CFD Deep Learning / MLOps Workspace

## Repo map
- `Technical_Papers_List.md` — curated reference list (papers grouped by topic: PINNs, ROM/LSTM, non-intrusive sensing, XAI).
- `CFD_Technical_Papers/` — downloaded PDFs, named `<Author>_<Year>_<Short_Title>.pdf`.
- `download_papers.py` — standalone script (ThreadPoolExecutor, 5 workers, 15s timeout) that fetches the paper list.
- `Transcripts_And_Slides/` — lecture material (PINNs, spatial discretization).
- No model/training code exists yet. When `src/`, `tests/`, or `configs/` are created, follow the rules below.

## Response rules (token efficiency)
- Be concise. No restating the user's request, no "Here is the code" preambles.
- Show only the diff/function being changed, not the whole file, unless asked.
- Don't re-explain a decision already stated in a linked `docs/copilot/*.md` file — reference it by path instead of repeating it.
- One question at a time if clarification is needed; otherwise proceed with the most reasonable assumption and state it in one line.

## Framework precision (PyTorch / TensorFlow)
- Never mix PyTorch and TensorFlow tensors/ops in the same module. One framework per file.
- PyTorch: explicit `device` and `dtype` on every tensor creation (`torch.zeros(..., device=device, dtype=torch.float32)`); use `nn.Module` + `forward`, never bare functions holding state; wrap training loops with `model.train()`/`model.eval()` and `torch.no_grad()` for inference.
- TensorFlow: use `tf.function`-compiled steps for training loops; prefer `tf.keras.Model` subclassing over ad-hoc layer stacking for anything with custom physics losses.
- No deprecated APIs (`torch.Tensor.new_tensor` chains, TF1-style `Session`/`placeholder`).
- Random seeds must be set explicitly (`torch.manual_seed`, `tf.random.set_seed`, plus `numpy`/`random`) in any training entrypoint — reproducibility is non-negotiable for CFD experiments.

## Test automation standards
- Every new model/module ships with a `pytest` test covering: output shape, dtype/device, and a gradient check (loss.backward() doesn't NaN).
- Any solver, ROM, or physics-loss change requires a regression test comparing against a known analytical/DNS baseline (see `docs/copilot/physics_validation_rules.md`).
- One assertion concern per test function; no multi-scenario mega-tests.
- Tests must run headless/CPU by default; GPU-only tests marked `@pytest.mark.gpu` and skipped by default.

## Pulling in extra context (do this, don't dump everything)
- Physics/CFD correctness rules: `#file:docs/copilot/physics_validation_rules.md`
- Training scale-up / experiment tracking rules: `#file:docs/copilot/mlops_scaling_rules.md`
- Only attach these when the task actually touches that domain — don't load both for a plain refactor.

## Reusable workflows
Use the slash-command prompts in `.github/prompts/` instead of re-explaining the task each time:
`/architecture-selection`, `/hyperparameter-tuning`, `/physics-validation`.
