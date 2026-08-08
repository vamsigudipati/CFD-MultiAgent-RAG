import csv
import sys
import time
from pathlib import Path

import yaml

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import tools.batch_execute_corpus as batch_execute_corpus
from modules.validation_harness.frontmatter import BlueprintFrontmatter
from tools.batch_execute_corpus import RESULTS_CSV, execute_batch
from tools.ingest_paper import ingest_paper

WORKSPACE_DIR = ROOT_DIR / "modules" / "workspace"
ACTIVE_BLUEPRINT_PATH = WORKSPACE_DIR / "blueprint.yaml"


PROBLEM_PAPERS = [
    "Samuel_1959_Machine_Learning_Checkers",
    "McCarthy_1955_Dartmouth_AI_Proposal",
    "Silver_2016_Mastering_Game_of_Go_AlphaGo",
    "Lundberg_2017_Kernel_SHAP_NeurIPS",
    "FLI_2023_Pause_Giant_AI_Experiments_Open_Letter",
    "Rumelhart_1986_Backpropagating_Errors",
    "Hey_2009_The_Fourth_Paradigm",
    "Tukey_1962_The_Future_of_Data_Analysis",
    "Kim_2021_Unsupervised_GAN_Fluid_Flow_Super_Resolution",
    "Encinar_2018_Logarithmic_Layer_Turbulence",
]

CONTROL_PAPERS = [
    "Raissi_2020_Hidden_Fluid_Mechanics",
    "Eivazi_2022_PINN_RANS_Navier_Stokes",
    "Eivazi_2024_DeNoising_Fluid_Flow_PINN",
    "Hasanuzzaman_2023_PINN_PIV_Measurements",
    "Kim_2005_Transition_To_Turbulence_Couette_Flow",
]
def _process_paper_with_blueprint(paper_id: str):
    thread_id = f"batch-run-{paper_id}-{int(time.time())}"
    config = {"configurable": {"thread_id": thread_id}}

    paper_yaml_path = ingest_paper(paper_id)
    raw_yaml = paper_yaml_path.read_text(encoding="utf-8")
    frontmatter = yaml.safe_load(raw_yaml) or {}
    ACTIVE_BLUEPRINT_PATH.write_text(raw_yaml, encoding="utf-8")

    # Validate/canonicalize before handing to the graph.
    validated_frontmatter = BlueprintFrontmatter.from_yaml(frontmatter).model_dump()
    initial_state = {
        "paper_id": paper_id,
        "failure_count": 0,
        "status": "PROCESSING",
        "frontmatter": validated_frontmatter,
        "blueprint_yaml": raw_yaml,
    }

    final_node_state = initial_state
    for event in batch_execute_corpus.app.stream(initial_state, config=config):
        for node_name, node_state in event.items():
            status = node_state.get("status", "N/A")
            failures = node_state.get("failure_count", 0)
            log_line = f"    ↳ Node: {node_name} | Status: {status}"
            if failures > 0:
                log_line += f" | Attempts: {failures}"
            print(log_line)
            final_node_state = node_state

    return final_node_state


if __name__ == "__main__":
    papers = PROBLEM_PAPERS + CONTROL_PAPERS

    batch_execute_corpus.process_paper = _process_paper_with_blueprint

    with open(RESULTS_CSV, mode="w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["Paper ID", "Pass", "Status", "Time (s)", "Error Fingerprint"],
        )
        writer.writeheader()

    print(f"Running mini batch with {len(papers)} papers...")
    execute_batch(papers)
    print(f"Mini batch complete. Results written to {RESULTS_CSV}")
