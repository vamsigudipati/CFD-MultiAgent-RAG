"""T0 -- static gates: import/instantiation and exact trainable-parameter count.

Cheapest, fastest tier. These must pass before any plumbing (T1) or physics
(T2/T3) test is attempted.
"""
import pytest
import torch.nn as nn

from .utils import load_generated_monolith

pytestmark = pytest.mark.t0


def test_static_instantiation():
    """The generated `Model` must instantiate and be a real nn.Module."""
    monolith = load_generated_monolith()
    model = monolith.Model()
    assert isinstance(model, nn.Module), (
        "Generated `Model` class must subclass torch.nn.Module"
    )


def test_parameter_count(blueprint_frontmatter):
    """If the blueprint declares a param_count constraint, match it exactly."""
    param_constraint = next(
        (c for c in blueprint_frontmatter.constraints if c.kind == "param_count"),
        None,
    )
    if param_constraint is None:
        pytest.skip("No param_count constraint declared in blueprint frontmatter")

    expected = param_constraint.params.get("expected")
    if expected is None:
        pytest.fail("param_count constraint is missing an 'expected' value")

    monolith = load_generated_monolith()
    model = monolith.Model()
    actual = sum(p.numel() for p in model.parameters() if p.requires_grad)

    assert actual == expected, (
        f"Trainable parameter count mismatch: expected {expected}, got {actual}"
    )
