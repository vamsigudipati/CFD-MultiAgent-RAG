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


def _classify_architecture_mode(state: AgentState, frontmatter: BlueprintFrontmatter) -> str:
    """Classify high-level model family for downstream prompt/test routing."""
    paper_id = str(state.get("paper_id", "")).lower()
    provenance_text = " ".join(str(v).lower() for v in frontmatter.provenance.values())
    haystack = " ".join([paper_id, provenance_text, frontmatter.pde_family.lower()])
    if "pinn" in haystack or "eivazi" in haystack:
        return "continuous_pinn"
    return "cnn_field"


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
    architecture_mode = _classify_architecture_mode(state, frontmatter)
    # NormalizationSpec is a Pydantic model -- dump to a dict for iteration.
    normalization = frontmatter.normalization.model_dump() if frontmatter.normalization else {}
    constraints = frontmatter.constraints or []

    lines = [
        "==================================================",
        "EXECUTION PLAN -- Scientific ML Code Generation",
        f"Paper ID: {state.get('paper_id', 'unknown')}",
        f"Architecture Mode: {architecture_mode}",
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
        "",
        "4. OUTPUT DIRECTIVE:",
        "   Emit a single valid Python code monolith. Never alter test files in modules/validation_harness/.",
    ])

    if architecture_mode == "continuous_pinn":
        lines.extend([
            "",
            "5. PINN-SPECIFIC DIRECTIVES:",
            "   - Use a coordinate-based MLP: inputs are continuous x, y tensors of shape (B, 1).",
            "   - Model.forward(x, y) must output three continuous fields (u, v, p), each shaped (B, 1).",
            "   - Use only Linear/Tanh-style MLP blocks; avoid convolutional layers for this paper family.",
            "   - Preserve autograd connectivity so du/dx and dv/dy are differentiable via torch.autograd.grad.",
        ])
    else:
        lines.extend([
            "",
            "5. CNN-SPECIFIC DIRECTIVES:",
            "   - Model.forward(x) consumes field tensors shaped (B, C, H, W) and returns the same spatial shape.",
            "   - Def compute_bc_loss(self, batch): boundary condition / residual loss callable.",
            "   - Def train_short_loop(seed=0): executes training and returns dictionary with val_loss.",
        ])

    execution_plan = "\n".join(lines)
    LOGGER.info(
        "Node B: execution plan synthesized (%s chars, pde_family=%s, mode=%s, %s constraints)",
        len(execution_plan), pde_family, architecture_mode, len(constraints),
    )
    return {"execution_plan": execution_plan, "architecture_mode": architecture_mode}