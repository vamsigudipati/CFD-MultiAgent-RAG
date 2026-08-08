"""Guardrail regression suite: locks in Issue #04 (architectural kill-switch)
and Issue #05 (PDE-domain / hyperparameter enforcement).

Run: python3 -m pytest tests/test_guardrails.py -v
"""

from modules.orchestrator.nodes import node_b_physics_reasoner


def _base_frontmatter(**overrides) -> dict:
    """Minimal valid frontmatter dict; override specific fields per test."""
    fm = {
        "closure_status": "closed",
        "pde_family": "incompressible_ns",
        "provenance": {"paper_id": "dummy"},
        "constraints": [],
        "traceability_matrix": {
            "activation_functions": {"value": "SiLU", "section": "3", "page": "4"},
            "layer_depths": {"value": "4 conv layers", "section": "3", "page": "4"},
            "pde_formulation": {
                "value": "Incompressible NS",
                "section": "2",
                "page": "2",
            },
        },
    }
    fm.update(overrides)
    return fm


def _run_node_b(frontmatter: dict) -> dict:
    return node_b_physics_reasoner({"paper_id": "dummy", "frontmatter": frontmatter})


def test_blocks_when_activation_functions_unavailable() -> None:
    tm = {
        "activation_functions": {
            "value": "UNAVAILABLE",
            "section": "UNAVAILABLE",
            "page": "UNAVAILABLE",
        },
        "layer_depths": {"value": "4 conv layers", "section": "3", "page": "4"},
    }
    result = _run_node_b(_base_frontmatter(traceability_matrix=tm))
    assert result["status"] == "BLOCKED_DATA"
    assert result["error_fingerprint"] == "BLOCKED_DATA|MISSING_ARCH_SPEC"


def test_blocks_when_layer_depths_unavailable() -> None:
    tm = {
        "activation_functions": {"value": "SiLU", "section": "3", "page": "4"},
        "layer_depths": {
            "value": "UNAVAILABLE",
            "section": "UNAVAILABLE",
            "page": "UNAVAILABLE",
        },
    }
    result = _run_node_b(_base_frontmatter(traceability_matrix=tm))
    assert result["status"] == "BLOCKED_DATA"
    assert result["error_fingerprint"] == "BLOCKED_DATA|MISSING_ARCH_SPEC"


def test_allows_fully_specified_architecture() -> None:
    """Positive control: complete spec must NOT be blocked."""
    result = _run_node_b(_base_frontmatter())
    assert result.get("status") != "BLOCKED_DATA"
    assert "execution_plan" in result
    assert result["architecture_mode"] in ("cnn_field", "continuous_pinn")


def test_rejects_non_cfd_paper_about_checkers() -> None:
    fm = _base_frontmatter(
        pde_family="unknown",
        provenance={"paper_id": "Samuel_1959_Machine_Learning_Checkers"},
        traceability_matrix={
            "activation_functions": {"value": "ReLU", "section": "2", "page": "3"},
            "layer_depths": {"value": "3 layers", "section": "2", "page": "3"},
            "pde_formulation": {
                "value": "Incompressible Navier-Stokes residual formulation",
                "section": "UNAVAILABLE",
                "page": "UNAVAILABLE",
            },
        },
    )
    result = _run_node_b(fm)
    assert result["status"] == "BLOCKED_DATA"
    assert result["error_fingerprint"] == "BLOCKED_DATA|NON_CFD_DOMAIN"
