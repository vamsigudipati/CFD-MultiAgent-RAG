import argparse
import re
from pathlib import Path

import yaml

from tools.normalize_markdown import normalize_markdown
from tools.synthesize_blueprint import synthesize_paper

ROOT_DIR = Path(__file__).resolve().parent.parent
EXTRACTED_PAPERS_DIR = ROOT_DIR / "docs" / "extracted_papers"
WORKSPACE_DIR = ROOT_DIR / "modules" / "workspace"


def _find_paper_dir(paper_id: str) -> Path:
    paper_dir = EXTRACTED_PAPERS_DIR / paper_id
    if not paper_dir.is_dir():
        raise FileNotFoundError(
            f"No extracted paper directory found for {paper_id} in {EXTRACTED_PAPERS_DIR}"
        )
    return paper_dir


def _find_source_markdown(paper_id: str) -> Path:
    paper_dir = _find_paper_dir(paper_id)
    normalized = paper_dir / f"{paper_id}_normalized.md"
    if normalized.is_file():
        return normalized

    source = paper_dir / f"{paper_id}.md"
    if not source.is_file():
        raise FileNotFoundError(f"No source markdown found for {paper_id} at {source}")

    normalize_markdown(source)
    if not normalized.is_file():
        raise FileNotFoundError(f"Normalization did not produce expected file {normalized}")
    return normalized


def _find_blueprint_markdown(paper_id: str) -> Path | None:
    candidate = _find_paper_dir(paper_id) / f"{paper_id}_blueprint.md"
    return candidate if candidate.is_file() else None


def _extract_line_value(text: str, labels: tuple[str, ...]) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        for label in labels:
            if label.lower() in stripped.lower():
                parts = stripped.split(":", 1)
                if len(parts) == 2:
                    value = parts[1].strip().strip("*").strip()
                    if value:
                        return value
    return "UNAVAILABLE"


def _infer_pde_formulation(text: str) -> str:
    governing_match = re.search(
        r"###\s+Governing Equations.*?(?=\n##\s+2\.|\Z)",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )
    if governing_match:
        snippet = " ".join(governing_match.group(0).split())
        return snippet[:600]
    if re.search(r"navier|continuity|momentum|rans", text, flags=re.IGNORECASE):
        return "Incompressible Navier-Stokes / RANS equations"
    return "UNAVAILABLE"


def _build_frontmatter_from_blueprint_markdown(paper_id: str, text: str) -> dict:
    non_cfd = "N/A — not a fluid-dynamics ML modeling paper" in text
    activation = _extract_line_value(text, ("Activation Function", "Activation Functions"))
    layers = _extract_line_value(
        text,
        ("Depth & Width", "Layer Configuration", "Layer Architecture", "Hidden layers"),
    )
    pde_formulation = _infer_pde_formulation(text)

    if non_cfd:
        activation = "UNAVAILABLE"
        layers = "UNAVAILABLE"
        pde_family = "unknown"
        pde_formulation = "UNAVAILABLE"
    else:
        pde_family = "incompressible_ns" if re.search(
            r"navier|continuity|momentum|rans|reynolds", text, flags=re.IGNORECASE
        ) else "unknown"

    return {
        "provenance": {"paper_id": paper_id, "title": paper_id},
        "closure_status": "closed",
        "pde_family": pde_family,
        "constraints": [],
        "traceability_matrix": {
            "activation_functions": {
                "value": activation,
                "section": "2" if activation != "UNAVAILABLE" else "UNAVAILABLE",
                "page": "UNAVAILABLE",
            },
            "layer_depths": {
                "value": layers,
                "section": "2" if layers != "UNAVAILABLE" else "UNAVAILABLE",
                "page": "UNAVAILABLE",
            },
            "pde_formulation": {
                "value": pde_formulation,
                "section": "1" if pde_formulation != "UNAVAILABLE" else "UNAVAILABLE",
                "page": "UNAVAILABLE",
            },
        },
    }


def ingest_paper(paper_id: str) -> Path:
    """Prepare a per-paper workspace and return the dedicated blueprint.yaml path."""
    paper_workspace = WORKSPACE_DIR / paper_id
    paper_workspace.mkdir(parents=True, exist_ok=True)
    paper_yaml_path = paper_workspace / "blueprint.yaml"

    if paper_yaml_path.is_file():
        return paper_yaml_path

    blueprint_md_path = _find_blueprint_markdown(paper_id)
    if blueprint_md_path is None:
        source_md_path = _find_source_markdown(paper_id)
        blueprint_md_path = source_md_path.with_name(f"{paper_id}_blueprint.md")
        synthesize_paper(source_md_path, blueprint_md_path)

    blueprint_text = blueprint_md_path.read_text(encoding="utf-8")
    frontmatter = _build_frontmatter_from_blueprint_markdown(paper_id, blueprint_text)
    raw_yaml = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True)
    paper_yaml_path.write_text(raw_yaml, encoding="utf-8")
    return paper_yaml_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare per-paper blueprint.yaml in modules/workspace/<paper_id>/")
    parser.add_argument("paper_id", help="Paper identifier matching docs/extracted_papers/<paper_id>/")
    args = parser.parse_args()
    path = ingest_paper(args.paper_id)
    print(path)