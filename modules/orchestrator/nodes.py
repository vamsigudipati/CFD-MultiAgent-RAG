"""Deterministic ingestion nodes for the LangGraph orchestrator.

Node A loads and validates the frozen blueprint frontmatter (the trust anchor
produced offline by the rule-based enrichment + human sign-off). Node A.5 is
the deterministic kill switch: it reads only validated YAML fields -- never an
LLM judgment -- to decide whether the run may proceed to the Physics Reasoner.
"""
from pathlib import Path

import yaml

from modules.validation_harness.frontmatter import BlueprintFrontmatter

from .state import AgentState

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BLUEPRINT_YAML_PATH = REPO_ROOT / "modules" / "workspace" / "blueprint.yaml"

# Fields Node A.5 requires to be present and meaningfully populated.
CRITICAL_FIELDS = ("pde_family", "closure_status")
# Values that mean "the rule-based enrichment could not determine this".
UNRESOLVED_VALUES = {"", "unknown", "n/a", "none"}


def node_a_ingest(state: AgentState) -> dict:
    """Node A -- load and strictly validate the blueprint frontmatter.

    Raises loudly on a missing/invalid file: a broken trust anchor is a
    harness-level configuration error, not a routable agent failure.
    """
    if not BLUEPRINT_YAML_PATH.is_file():
        raise FileNotFoundError(
            f"Blueprint frontmatter not found at {BLUEPRINT_YAML_PATH}. "
            "Run the enrichment step (tools/enrich_blueprints.py) first."
        )

    raw_text = BLUEPRINT_YAML_PATH.read_text(encoding="utf-8")
    parsed = yaml.safe_load(raw_text) or {}
    frontmatter = BlueprintFrontmatter.from_yaml(parsed)  # Pydantic validation

    return {
        "blueprint_yaml": raw_text,
        "frontmatter": frontmatter.model_dump(),
    }


def node_a5_feasibility_check(state: AgentState) -> dict:
    """Node A.5 -- deterministic kill switch.

    Blocks the run (BLOCKED_DATA) when the spec is unusable:
      * any critical field is absent or unresolved ("unknown"/empty), or
      * the PDE system is declared unclosed with no closure strategy.
    Otherwise marks the run FEASIBLE for the Physics Reasoner (Node B).
    """
    frontmatter = state.get("frontmatter") or {}

    for field in CRITICAL_FIELDS:
        value = frontmatter.get(field)
        if value is None or str(value).strip().lower() in UNRESOLVED_VALUES:
            return {"status": "BLOCKED_DATA"}

    if str(frontmatter["closure_status"]).strip().lower() == "unclosed":
        return {"status": "BLOCKED_DATA"}

    return {"status": "FEASIBLE"}


def node_b_physics_reasoner(state: AgentState) -> dict:
    """Node B -- Physics Reasoner.

    Re-hydrates the validated frontmatter and synthesizes the execution plan:
    the system prompt handed to the Framework Supervisor (Node C). The actual
    LLM reasoning call will be injected later; for the structural compile this
    deterministically assembles the plan from the typed spec.
    """
    frontmatter = BlueprintFrontmatter(**state["frontmatter"])

    pde_family = frontmatter.pde_family
    normalization = frontmatter.normalization
    constraints = frontmatter.constraints

    constraint_lines = []
    for c in constraints:
        params = ", ".join(f"{k}={v}" for k, v in c.params.items())
        gate = f" (gate: {c.gate_assertion})" if c.gate_assertion else ""
        constraint_lines.append(f"  - kind='{c.kind}' with {params or 'no params'}{gate}")
    constraints_block = "\n".join(constraint_lines) or "  - (none declared)"

    execution_plan = (
        "EXECUTION PLAN -- Scientific ML Code Generation\n"
        f"Paper ID: {state.get('paper_id', 'unknown')}\n"
        "\n"
        f"1. TARGET PDE FAMILY: {pde_family}\n"
        f"   The generated model MUST implement the physics of '{pde_family}'.\n"
        "   The T2 validation gate will check the analytic MMS residual for this family.\n"
        "\n"
        "2. NORMALIZATION (apply EXACTLY as specified; T2 asserts on these):\n"
        f"   - spatial_scale:  {normalization.spatial_scale}\n"
        f"   - velocity_scale: {normalization.velocity_scale}\n"
        f"   - pressure_scale: {normalization.pressure_scale}\n"
        f"   - expected_input_rms: {normalization.expected_input_rms}\n"
        "\n"
        "3. REQUIRED CONSTRAINT RULES (each is enforced by a registered gate handler):\n"
        f"{constraints_block}\n"
        "\n"
        "4. MANDATORY MODULE CONTRACT (the validation harness imports these):\n"
        "   - class Model(nn.Module) with forward(x)\n"
        "   - Model.compute_bc_loss(batch) returning a finite scalar\n"
        "   - def get_dummy_batch() returning a batch with .x, .y (small, STRUCTURED\n"
        "     targets -- not pure noise) and .variable_names\n"
        "   - def train_short_loop(seed:int) returning {'val_loss': float}\n"
        "\n"
        "5. OUTPUT: a single monolith file train_and_val.py in $WORKSPACE_DIR.\n"
        "   Do NOT write or modify any test file; the harness is immutable.\n"
    )

    return {"execution_plan": execution_plan}
