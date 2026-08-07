"""Constraint handler for per-variable RMS normalization checks.

Verifies that each named input channel (e.g. u, v, w velocity fluctuations)
has been scaled to its expected RMS magnitude, as declared in the blueprint's
normalization spec. Catches silent scale mismatches between the paper's
non-dimensionalization and the generated data pipeline.
"""
from typing import Dict, List, Optional

from pydantic import BaseModel

from ..registry import ConstraintHandler, register

DEFAULT_TOLERANCE = 0.10  # 10% relative tolerance


@register("input_rms")
class InputRMSHandler(ConstraintHandler):
    class ParamModel(BaseModel):
        expected_rms: Dict[str, float]
        tolerance: float = DEFAULT_TOLERANCE

    def gate_assert(self, model, batch, params: "InputRMSHandler.ParamModel") -> None:
        variable_names: Optional[List[str]] = getattr(batch, "variable_names", None)
        names = variable_names or list(params.expected_rms.keys())

        if len(names) != batch.x.shape[1]:
            raise AssertionError(
                f"Channel count mismatch: batch.x has {batch.x.shape[1]} channels "
                f"but {len(names)} variable name(s) were provided: {names}"
            )

        for channel_idx, name in enumerate(names):
            if name not in params.expected_rms:
                continue  # variable not constrained by this handler instance
            expected = params.expected_rms[name]
            actual = batch.x[:, channel_idx, ...].std().item()
            rel_error = abs(actual - expected) / expected if expected != 0 else abs(actual)
            assert rel_error <= params.tolerance, (
                f"RMS mismatch for '{name}': expected {expected} (+/- "
                f"{params.tolerance * 100:.0f}%), got {actual:.4f} "
                f"(relative error {rel_error * 100:.1f}%)"
            )
