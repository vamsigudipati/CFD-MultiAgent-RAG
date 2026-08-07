"""Constraint handler for thresholded ("modified") ReLU output floors.

Some architectures (e.g. the Balasubramanian et al. 2023 R-Net) clamp their
output activation at a fixed floor instead of 0, to admit signed normalized
fluctuation quantities. This handler enforces that no output value falls
below the floor declared in the paper's blueprint frontmatter.
"""
from pydantic import BaseModel

from ..registry import ConstraintHandler, register


@register("output_floor")
class OutputFloorHandler(ConstraintHandler):
    class ParamModel(BaseModel):
        floor: float

    def gate_assert(self, model, batch, params: "OutputFloorHandler.ParamModel") -> None:
        output = model(batch.x)
        actual_min = output.min().item()
        assert actual_min >= params.floor, (
            f"Output floor violated: minimum output value {actual_min} "
            f"is below the required floor {params.floor}"
        )
