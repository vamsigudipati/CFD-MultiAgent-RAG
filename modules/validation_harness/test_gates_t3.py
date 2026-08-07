"""T3 -- short-train regression: multi-seed training against blueprint thresholds.

Most expensive tier; runs a brief real training loop. Chaotic/stochastic flow
models are only meaningfully evaluated as an ensemble, so this asserts on the
mean validation loss across multiple seeds rather than a single run. A module
timeout prevents a hung training loop from deadlocking the LangGraph loop.
"""
import pytest
import torch

from .utils import get_monolith_symbol

# A hung training loop must never deadlock the orchestrator -> hard timeout.
pytestmark = [pytest.mark.t3, pytest.mark.timeout(300)]

N_SEEDS = 3
DEFAULT_VALIDATION_TOLERANCE = 0.1


def _resolve_validation_threshold(blueprint_frontmatter) -> float:
    """Read `regression_targets.expected_validation_loss`, defaulting to 0.1."""
    for constraint in blueprint_frontmatter.constraints:
        if constraint.kind == "regression_targets":
            return float(
                constraint.params.get("expected_validation_loss", DEFAULT_VALIDATION_TOLERANCE)
            )
    return DEFAULT_VALIDATION_TOLERANCE


def test_short_train_regression_multi_seed(blueprint_frontmatter):
    """Ensemble-mean validation loss over 3 seeds must beat the blueprint threshold."""
    train_short_loop = get_monolith_symbol("train_short_loop", required=False)
    if train_short_loop is None:
        pytest.fail(
            "SYNTAX: generated monolith does not define `train_short_loop()`; "
            "route back to the framework agent to add it"
        )

    threshold = _resolve_validation_threshold(blueprint_frontmatter)

    val_losses = []
    for seed in range(N_SEEDS):
        torch.manual_seed(seed)
        result = train_short_loop(seed=seed)
        val_loss = result["val_loss"] if isinstance(result, dict) else result
        val_loss = float(val_loss.item() if torch.is_tensor(val_loss) else val_loss)
        assert val_loss == val_loss, f"Seed {seed} produced a NaN validation loss"  # NaN guard
        val_losses.append(val_loss)

    ensemble_mean = sum(val_losses) / len(val_losses)
    assert ensemble_mean < threshold, (
        f"Ensemble-mean validation loss {ensemble_mean:.6g} over {N_SEEDS} seeds "
        f"exceeds threshold {threshold:.6g} (per-seed: {val_losses})"
    )
