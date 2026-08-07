# Autonomous Scientific ML-CFD Multi-Agent RAG Framework

An end-to-end pipeline that turns fluid-dynamics research papers into **validated,
physics-tested machine-learning code** — autonomously. Papers are extracted into
structured blueprints, grounded against a code knowledge base of reference
implementations, synthesized into PyTorch models by a LangGraph multi-agent
orchestrator, and gated by an immutable physics validation harness before anything
is accepted.

---

## 1. System Architecture Overview

The system is organized as three trust-separated layers. The separation is the core
design principle: **the layer that writes code can never touch the layer that
validates it.**

```
┌─────────────────────────────────────────────────────────────────────┐
│  KNOWLEDGE BASE (RAG)                    data/ · tools/             │
│  PDF extraction → blueprints → YAML frontmatter                     │
│  Reference repos → AST symbol index (SQLite) → fetch_symbol tool    │
├─────────────────────────────────────────────────────────────────────┤
│  ORCHESTRATOR ENGINE (Yellow Layer)      modules/orchestrator/      │
│  LangGraph StateGraph: Node A → A.5 → B → C → D                     │
│  Self-healing loop (k=3 budget) · SqliteSaver checkpointing         │
│  The ONLY layer where LLM-generated code is produced                │
├─────────────────────────────────────────────────────────────────────┤
│  GREEN LAYER (Immutable Validation)      modules/validation_harness/│
│  T0–T3 PyTest gates · constraint handler registry · MMS analytic    │
│  targets · float64/CPU precision pinning · human-authored only      │
└─────────────────────────────────────────────────────────────────────┘
```

### The Green Layer — `modules/validation_harness/`
A human-authored, runtime-immutable PyTest harness that every piece of generated
code must pass. No LLM ever writes to this layer.

| Tier | Gate | Checks |
|------|------|--------|
| T0 | Static | Imports, `nn.Module` instantiation, exact trainable-parameter counts |
| T1 | Plumbing | `loss.backward()` finiteness, data-term-only single-batch overfit, trivial-solution guard |
| T2 | Physics | Method of Manufactured Solutions (MMS) analytic PDE residuals (`< 1e-12`), registered constraint handlers, boundary-condition loss finiteness |
| T3 | Regression | Multi-seed short-train ensemble vs. blueprint thresholds, hard timeout |

Key components:
- **Constraint handler registry** (`registry.py`, `handlers/`) — open/closed
  pattern: new physics constraints (output floors, RMS normalization checks) are
  drop-in modules; unknown kinds terminate deterministically with
  `UNSUPPORTED_CONSTRAINT`.
- **MMS registry** (`mms/`) — hand-derived analytic solutions per PDE family
  (e.g., the 2D Taylor–Green vortex for incompressible Navier–Stokes), verified
  to machine epsilon via autograd.
- **Precision pinning** (`conftest.py`) — all T2 physics tests are forced to
  **CPU + float64**. This is mandatory, not stylistic: Apple Silicon's MPS
  backend has no float64 support, and float32 `gradcheck` produces false
  failures that would poison the self-healing loop.

### The Knowledge Base (RAG) — `tools/` + `data/`
- `tools/clone_reference_repos.py` — extracts GitHub URLs from
  `CFD_Technical_Papers_Literatur.csv`, clones them into `data/reference_repos/`.
- `tools/ast_indexer.py` — AST-parses every repo into a two-tier index:
  **Tier 1** repo cards (`data/repo_cards/*.md`: frameworks, symbol inventory)
  and **Tier 2** symbol chunks (`data/ast_index.sqlite`: model classes, network
  factories, loss/residual/PDE functions — 155+ symbols across ~10 repos).
- `fetch_symbol(repo, qualname)` — deterministic source-code lookup used by the
  code-generation agents to ground output in proven reference implementations.
- Paper ingestion: `tools/normalize_markdown.py` (deterministic OCR-artifact
  cleanup), `tools/synthesize_blueprint.py` + `tools/synthesize_all.sh`
  (Markdown → 6-section architectural blueprints).

### The Orchestrator Engine — `modules/orchestrator/`
A LangGraph `StateGraph` over a typed `AgentState` (`state.py`):

| Node | Role |
|------|------|
| **A** (`nodes.py`) | Ingests and Pydantic-validates `modules/workspace/blueprint.yaml` (the frozen trust anchor) |
| **A.5** (`nodes.py`) | Deterministic feasibility kill switch — unclosed/unknown specs terminate as `BLOCKED_DATA` *before* any generation cost |
| **B** (`nodes.py`) | Physics Reasoner — synthesizes the execution plan (PDE family, normalization, constraints, module contract) |
| **C** (`node_c.py`) | Framework Supervisor — generates the code monolith, grounded by RAG golden symbols; consumes retry diagnostics |
| **D** (`node_d.py`) | Test Execution Engine — runs the Green Layer in a subprocess (600 s hang ceiling) and emits a normalized failure fingerprint |

**Self-healing routing** (typed fields only, never prose): `SYNTAX`/`HANG` →
back to Node C (code fix); `GATE_FAIL|tier:test` → back to Node B (physics
re-plan); `UNSUPPORTED_CONSTRAINT` or budget exhaustion (**k = 3**) →
`BLOCKED_PHYSICS` terminal. All state transitions are checkpointed to
`data/orchestrator_checkpoints.sqlite` via `SqliteSaver`.

---

## 2. System Prerequisites & Hardware Requirements

| Requirement | Detail |
|---|---|
| **Python** | 3.13+ (developed against the python.org framework build) |
| **PyTorch** | ≥ 2.2 (validated on 2.9.1); CPU is sufficient for the harness and orchestrator |
| **SQLite** | Bundled `sqlite3` module + `sqlite3` CLI for checkpoint inspection |
| **Git** | Required by the reference-repo cloner |
| **OS** | macOS (incl. Apple Silicon) or Linux |
| **RAM / disk** | ≥ 8 GB RAM; ~1 GB disk for reference repos + indices |
| **GPU** | Optional. **Note:** T2 physics gates always run CPU/float64 by design — MPS has no float64 support |

Optional (Stage-1 blueprint synthesis only): `google-genai` + a `GEMINI_API_KEY`,
and [Marker](https://github.com/datalab-to/marker) for PDF → Markdown extraction.

## 3. Installation & Dependency Setup

```bash
git clone <this-repo>
cd CFD_Technical_Papers

# Install all pipeline dependencies
python3 -m pip install -r requirements.txt
```

`requirements.txt` pins the seven core dependencies: `torch`, `pydantic`,
`pyyaml`, `pytest`, `pytest-timeout`, `langgraph`, `langgraph-checkpoint-sqlite`.

> **Multiple-interpreter note:** on machines with several Pythons (conda + system
> + framework), always invoke the interpreter you installed into explicitly, e.g.
> `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3`, rather than
> relying on `PATH` resolution. All commands below assume `python3` resolves to
> that interpreter.

Verify the environment:

```bash
python3 - <<'EOF'
import torch, pydantic, yaml, pytest, langgraph
import langgraph.checkpoint.sqlite
print("environment OK — torch", torch.__version__)
EOF
```

## 4. Quick-Start Guide

All commands run from the repository root.

**Run the platform smoke test** (does everything still work?) — a deterministic,
offline regression that drives both proven end-to-end threads (a CNN-field paper
and a continuous-PINN paper) through the full graph + Green Layer gates and
asserts each reaches `PASSED`. `GEMINI_API_KEY` is unset for the run, so Node C
uses its deterministic fallback templates (no network or cost):

```bash
tools/smoke_test.sh
# override interpreter if needed:  PYTHON=/path/to/python3 tools/smoke_test.sh
```

**Run the orchestrator test suite** (happy path, kill switch, budget exhaustion):

```bash
python3 -m pytest modules/orchestrator/test_orchestrator.py -v --tb=short
```

**Run the Green Layer validation gates** against a workspace monolith:

```bash
# The harness validates the code in $WORKSPACE_DIR/train_and_val.py
WORKSPACE_DIR="$(pwd)/modules/workspace" \
  python3 -m pytest modules/validation_harness -v --tb=short
```

**Build the RAG knowledge base:**

```bash
python3 tools/clone_reference_repos.py --csv CFD_Technical_Papers_Literatur.csv
python3 tools/ast_indexer.py
```

**Invoke the full orchestration graph programmatically:**

```python
from modules.orchestrator.graph import app

result = app.invoke(
    {"paper_id": "my_paper", "failure_count": 0, "frontmatter": {},
     "status": "", "blueprint_yaml": "", "execution_plan": "",
     "generated_code": "", "error_fingerprint": ""},
    config={"configurable": {"thread_id": "my_paper-run-001"}},  # REQUIRED
)
print(result["status"])   # PASSED | BLOCKED_DATA | BLOCKED_PHYSICS
```

> A unique `thread_id` per run is **required** (the checkpointer enforces it),
> and thread IDs must **never be reused across papers** — checkpoint state
> (including the failure budget) persists per thread.

See [docs/workflows_and_use_cases.md](docs/workflows_and_use_cases.md) for the
full workflow deep-dive, kill-switch semantics, and checkpoint forensics.

## Repository Map

```
├── requirements.txt                  # pinned pipeline dependencies
├── CFD_Technical_Papers_Literatur.csv  # literature + reference-repo source list
├── pdf_repository/                   # 48+ research paper PDFs
├── docs/
│   ├── extracted_papers/             # Marker-extracted + normalized markdown per paper
│   ├── framework_templates/          # framework RAG references (PyTorch PINN training, data loaders)
│   ├── usecases/                     # user-centric "why it matters" overview
│   ├── workflows/                    # spec-to-ML workflow + CFD-to-PINN concept mapping
│   ├── validation/                   # benchmark matrix (gate coverage per canonical problem)
│   ├── project_journal.md            # engineering decision log
│   └── workflows_and_use_cases.md    # functional deep-dive (this doc's companion)
├── tools/                            # ingestion, synthesis, cloning, AST indexing, smoke_test.sh
├── data/                             # (gitignored) repos, AST index, checkpoints
└── modules/
    ├── validation_harness/           # GREEN LAYER — immutable T0–T3 gates
    ├── orchestrator/                 # LangGraph engine (Nodes A–D, graph, state)
    ├── workspace/                    # (gitignored) LLM-mutable monolith zone
    ├── generated/                    # human-reviewed generated model examples
    └── feasibility_test/             # R-Net tracer-bullet scaffold (Phase 1)
```
