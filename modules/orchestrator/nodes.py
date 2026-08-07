"""Orchestrator nodes for ingestion, feasibility pre-check, and physics reasoning."""
import logging
import yaml
from pathlib import Path
from modules.validation_harness.frontmatter import BlueprintFrontmatter
from .state import AgentState

LOGGER = logging.getLogger(__name__)

# Absolute path anchor from repo root
REPO_ROOT = Path(__file__).resolve().parents[2]
BLUEPRINT_YAML_PATH = REPO_ROOT / "modules" / "workspace" / "blueprint.yaml"


def node_a_ingest(state: AgentState) -> dict:
    """Ingests and parses the workspace blueprint YAML with robust error protection."""
    if not BLUEPRINT_YAML_PATH.exists():
        raise FileNotFoundError(f"Critical trust anchor missing: {BLUEPRINT_YAML_PATH}")
    
    raw_text = BLUEPRINT_YAML_PATH.read_text()
    try:
        parsed = yaml.safe_load(raw_text) or {}
        frontmatter = BlueprintFrontmatter.from_yaml(parsed)
        LOGGER.info(
            "Node A: blueprint ingested (pde_family=%s, closure_status=%s, %s constraints)",
            frontmatter.pde_family, frontmatter.closure_status, len(frontmatter.constraints),
        )
        return {
            "blueprint_yaml": raw_text,
            "frontmatter": frontmatter.model_dump(),
        }
    except (yaml.YAMLError, ValueError) as e:
        # Gracefully capture malformed syntax into state instead of crashing mid-stream
        LOGGER.error("Node A: malformed blueprint YAML, degrading to BLOCKED_DATA (%s)", e)
        return {
            "blueprint_yaml": raw_text,
            "frontmatter": {"closure_status": "unclosed", "pde_family": "unknown"},
            "status": "BLOCKED_DATA",
        }


def node_a5_feasibility_check(state: AgentState) -> dict:
    """Deterministic pre-check acting as a kill switch based on frontmatter data."""
    frontmatter_dict = state.get("frontmatter", {})
    closure_status = frontmatter_dict.get("closure_status", "unclosed")
    pde_family = frontmatter_dict.get("pde_family", "unknown")

    # Trigger kill switch if unclosed or if pde_family is unresolved/unknown
    if closure_status != "closed" or pde_family in ("", "unknown", "n/a", None):
        return {"status": "BLOCKED_DATA"}
    return {"status": "FEASIBLE"}


def node_b_physics_reasoner(state: AgentState) -> dict:
    """Synthesizes the execution plan string from the parsed blueprint frontmatter."""
    frontmatter_dict = state.get("frontmatter", {})
    frontmatter = BlueprintFrontmatter(**frontmatter_dict)

    pde_family = frontmatter.pde_family
    # NormalizationSpec is a Pydantic model -- dump to a dict for iteration.
    normalization = frontmatter.normalization.model_dump() if frontmatter.normalization else {}
    constraints = frontmatter.constraints or []

    lines = [
        "==================================================",
        "EXECUTION PLAN -- Scientific ML Code Generation",
        f"Paper ID: {state.get('paper_id', 'unknown')}",
        f"Target PDE Family (T2 MMS Gate): {pde_family}",
        "==================================================",
        "",
        "1. DIMENSIONAL NORMALIZATION SCALES:",
    ]
    for scale_name, scale_expr in normalization.items():
        lines.append(f"   - {scale_name}: {scale_expr}")

    lines.extend([
        "",
        "2. DECLARED CONSTRAINTS & HARNESS GATES:",
    ])
    if constraints:
        for idx, constraint in enumerate(constraints, 1):
            lines.append(f"   Constraint {idx}: kind={constraint.kind}, params={constraint.params}")
    else:
        lines.append("   - None declared (standard unconstrained surrogate)")

    lines.extend([
        "",
        "3. MANDATORY MODULE CONTRACT FOR GENERATED CODE:",
        "   The generated monolith (train_and_val.py) must export:",
        "   - class Model(torch.nn.Module): architecture supporting input/output mappings",
        "   - def compute_bc_loss(self, batch): boundary condition / residual loss callable",
        "   - def train_short_loop(seed=0): executes training and returns dictionary with val_loss",
        "",
        "4. OUTPUT DIRECTIVE:",
        "   Emit a single valid Python code monolith. Never alter test files in modules/validation_harness/.",
    ])

    execution_plan = "\n".join(lines)
    LOGGER.info(
        "Node B: execution plan synthesized (%s chars, pde_family=%s, %s constraints)",
        len(execution_plan), pde_family, len(constraints),
    )
    return {"execution_plan": execution_plan}