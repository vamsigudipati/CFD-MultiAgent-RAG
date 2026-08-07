# Workflows & Use Cases — Functional Deep-Dive

Companion to the [root README](../README.md). This guide walks through the three
core workflows and the concrete use cases the framework was validated against,
including real command transcripts and expected outputs.

All commands run from the repository root. `python3` refers to the interpreter
`requirements.txt` was installed into.

---

## 1. Core Workflows

### Workflow A — Reference Repository Ingestion & AST Indexing

Builds the RAG knowledge base that grounds code generation.

**Step 1: Clone the reference repositories.**

```bash
python3 tools/clone_reference_repos.py --csv CFD_Technical_Papers_Literatur.csv
```

- Scans *every cell* of the CSV for GitHub URLs (handles `https`, `/tree/…`,
  `/blob/…`, `.git` suffixes), de-duplicates case-insensitively while preserving
  the canonical repo name casing.
- Clones (depth-1) into `data/reference_repos/<repo_name>`; re-runs perform
  `git pull --ff-only` instead of re-cloning.
- `--dry-run` lists discovered repos without cloning.

**Step 2: Build the two-tier AST index.**

```bash
python3 tools/ast_indexer.py
```

- **Tier 2 (symbol chunks):** walks every `.py` file, extracting classes that
  subclass `nn.Module`/`keras.Model` or match `*Net*`/`*Model*`, plus functions
  whose names contain `loss`, `residual`, `pde`, `boundary`, `model`, `net`,
  `build`, or `architecture` (the latter four capture Keras function-factory
  style, e.g. `def cnn_model(...)`). Unparseable files are skipped gracefully.
  Results land in `data/ast_index.sqlite` (table `symbol_chunks`, PK
  `repo_name + file_path + qualname`; re-indexing is idempotent).
- **Tier 1 (repo cards):** one markdown card per repo at
  `data/repo_cards/<repo>_card.md` listing detected frameworks (PyTorch /
  TensorFlow / Keras, from AST import analysis) and every extracted qualname.

**Step 3: Retrieve golden symbols (the agents' tool).**

```python
import sys; sys.path.insert(0, "tools")
from ast_indexer import fetch_symbol

src = fetch_symbol("FCN-turbulence-predictions-from-wall-quantities", "cnn_model")
# returns the exact source; raises LookupError on a miss (never a silent empty string)
```

---

### Workflow B — Physics Validation & Green Layer Execution

The immutable T0–T3 gates validate any `train_and_val.py` monolith. The harness
locates the code under test via the `WORKSPACE_DIR` environment variable and
parametrizes its assertions from `modules/workspace/blueprint.yaml`.

**Module contract** — the monolith must export:

| Symbol | Requirement |
|---|---|
| `class Model(nn.Module)` | with `forward(x)` |
| `Model.compute_bc_loss(batch)` | returns a finite scalar |
| `train_short_loop(seed)` | returns `{"val_loss": float}` |

The Green Layer now owns evaluation inputs via `standard_evaluation_batch`
(`modules/validation_harness/conftest.py`), so generated monoliths cannot
provide or manipulate harness calibration batches.

**Run:**

```bash
WORKSPACE_DIR="$(pwd)/modules/workspace" \
  python3 -m pytest modules/validation_harness -v --tb=short
```

Tier-by-tier (fail-fast order):

- **T0** — imports, instantiation, exact parameter count (if the blueprint
  declares a `param_count` constraint; otherwise skipped).
- **T1** — backward-pass finiteness; a 50-step **data-term-only** overfit that
  must drop loss two orders of magnitude *and* keep prediction variance above
  10% of target variance (trivial-solution guard).
- **T2** — *always CPU + float64*: MMS analytic residual for the blueprint's
  `pde_family` must satisfy the PDE to `< 1e-12`; every declared constraint is
  enforced through the handler registry; `compute_bc_loss` must be finite.
  A missing method fails with an explicit `SYNTAX:` tag (routable), and an
  unregistered constraint kind fails loudly as `UNSUPPORTED_CONSTRAINT`.
- **T3** — 3-seed short-train ensemble; the mean validation loss must beat
  `regression_targets.expected_validation_loss` (default 0.1). The module
  carries a hard `pytest.mark.timeout(300)`.

---

### Workflow C — Autonomous Paper-to-Code Orchestration

```
START → Node A → Node A.5 ──BLOCKED_DATA──→ END
                    │ FEASIBLE
                    ▼
              Node B (plan) ←──────────── GATE_FAIL (physics re-plan)
                    ▼                          │
              Node C (codegen) ←── SYNTAX/HANG (code fix)
                    ▼                          │
              Node D (run T0–T3) ──────────────┘
                    │
        PASSED → END        k=3 exhausted / UNSUPPORTED → BLOCKED_PHYSICS → END
```

1. **Node A** reads `modules/workspace/blueprint.yaml`, validates it through the
   Pydantic `BlueprintFrontmatter` schema, and stores both the raw text and the
   parsed dict in state. Malformed YAML degrades to a `BLOCKED_DATA` route
   rather than crashing mid-graph; a *missing* file raises loudly (that is a
   configuration error, not a routable failure).
2. **Node A.5** is the deterministic kill switch: `closure_status != closed` or
   an unresolved `pde_family` (`unknown`/empty) terminates as `BLOCKED_DATA`
   *before* any generation cost is spent. No LLM judgment is involved.
3. **Node B** synthesizes the execution plan: PDE family (tied to the T2 MMS
   gate), normalization scales, every declared constraint, and the mandatory
   module contract.
4. **Node C** generates the monolith, pulling golden reference symbols from the
   AST index; on retries it consumes the failure fingerprint.
5. **Node D** writes the monolith to the workspace, runs the Green Layer in a
   subprocess (600-second ceiling — an import-time infinite loop becomes a
   `HANG` fingerprint instead of a deadlock), and classifies failures into the
   typed taxonomy.

Every state transition is checkpointed to
`data/orchestrator_checkpoints.sqlite`.

---

## 2. Basic Use Cases

### Use Case 1 — Standard closed-blueprint research pipeline

Provide a feasible blueprint, invoke the graph, receive validated code.

```bash
mkdir -p modules/workspace
cat > modules/workspace/blueprint.yaml <<'YAML'
closure_status: closed
pde_family: incompressible_ns
constraints:
  - kind: output_floor
    params: {floor: -100.0}
  - kind: input_rms
    params:
      expected_rms: {u: 1.0, v: 1.0, w: 1.0}
      tolerance: 0.4
  - kind: regression_targets
    params: {expected_validation_loss: 0.1}
YAML
```

```python
from modules.orchestrator.graph import app

result = app.invoke(
    {"paper_id": "demo_paper", "failure_count": 0, "frontmatter": {},
     "status": "", "blueprint_yaml": "", "execution_plan": "",
     "generated_code": "", "error_fingerprint": ""},
    config={"configurable": {"thread_id": "demo_paper-run-001"}},
)
assert result["status"] == "PASSED"
# validated code is now at modules/workspace/train_and_val.py
```

Expected: `status == "PASSED"`, `failure_count == 0`, and the monolith passes
all T0–T3 gates (observed: 7 passed, 1 skipped when no `param_count` is
declared).

### Use Case 2 — Unclosed-data kill switch (`BLOCKED_DATA`)

An unclosed RANS system (or an unresolved `pde_family`) must terminate before
any code is generated:

```yaml
# modules/workspace/blueprint.yaml
closure_status: unclosed          # ← no closure strategy declared
pde_family: incompressible_ns
```

Result: `status == "BLOCKED_DATA"` and `generated_code == ""` — Node B/C/D are
never invoked. This is the cheap-rejection guarantee: infeasible specs cost
zero generation/test cycles. The remediation is human: declare a closure
strategy (`eddy_viscosity`, `ml_closure`, `provided_by_data`) or complete the
missing fields, then re-run under a **new** `thread_id`.

---

## 3. Advanced Use Cases

### Use Case 3 — Processing a real research paper with RAG retrieval

Validated end-to-end against **DeepCFD** (arXiv:2004.08826, Ribeiro et al.):

1. **Extract:** drop the PDF into `pdf_repository/`, extract text (Marker for
   math-heavy layouts; `pdfminer` suffices for text-layer arXiv PDFs), and
   normalize with `python3 tools/normalize_markdown.py <extracted.md>`.
2. **Synthesize the problem spec:** 3 input channels (SDF, SDF, 5-class flow
   region) → 3 outputs (Ux, Uy, p); the paper's key finding is a split loss —
   **MSE on velocity + MAE on pressure**, per-output normalized; AdamW,
   weight decay 0.005.
3. **Ground in the RAG:** query the AST index for structural references —
   e.g. `residual_block` (Conv+BN+Add pattern) and `cnn_model` (fully-conv
   field predictor) — via `fetch_symbol`.
4. **Generate + validate:** the resulting ResUNet implementation lives at
   `modules/generated/deepcfd_resunet/` with its 7-test suite (I/O contract,
   loss-norm semantics L1-vs-L2, gradient health, single-batch overfit):

```bash
python3 -m pytest modules/generated/deepcfd_resunet -v
# 7 passed
```

> Corpus honesty note: the current index is PINN/XAI-heavy. If a paper family
> is under-represented (e.g. CNN surrogates), add reference repos to the CSV
> and re-run Workflow A — grounding quality follows corpus coverage.

### Use Case 4 — Self-healing retries and budget exhaustion

Node D's fingerprint taxonomy drives deterministic repair routing:

| Fingerprint | Meaning | Routed to |
|---|---|---|
| `SYNTAX` | Broken code / missing contract method | Node C (regenerate code; physics plan untouched) |
| `HANG` | Subprocess exceeded the 600 s ceiling | Node C |
| `GATE_FAIL\|t2:test_enforced_constraints` | Physics gate failed (tier + test names) | Node B (re-plan) |
| `UNSUPPORTED_CONSTRAINT` | Constraint kind with no registered handler | Terminal — `BLOCKED_PHYSICS` |
| *(unknown)* | Unclassifiable failure | Terminal — terminate, never thrash |

Fingerprints are built from *(exception class, tier, failing test names)* — never
raw stack traces — so line-number churn between rewrites cannot break dedup.

**Budget exhaustion (k = 3), reproducible demo:** declare a constraint the
generator cannot satisfy —

```yaml
constraints:
  - kind: output_floor
    params: {floor: 0.5}     # tanh-based outputs go below 0.5 → always fails
```

The graph loops B → C → D exactly three times (each a real pytest execution),
increments `failure_count` monotonically 1 → 2 → 3, then terminates:

```
status            = BLOCKED_PHYSICS
failure_count     = 3
error_fingerprint = GATE_FAIL|t2:test_enforced_constraints
```

`BLOCKED_PHYSICS` is a *legitimate scientific result with evidence* — the spec
is unsatisfiable as declared — not a crash.

### Use Case 5 — Inspecting persistent state trajectories (`SqliteSaver`)

Every super-step is checkpointed per `thread_id`. Forensics via the SQLite CLI:

```bash
# What tables does the checkpointer maintain?
sqlite3 data/orchestrator_checkpoints.sqlite ".tables"
# → checkpoints  writes

# How many state transitions did each run record?
sqlite3 data/orchestrator_checkpoints.sqlite \
  "SELECT thread_id, COUNT(*) FROM checkpoints GROUP BY thread_id ORDER BY 2 DESC;"
# e.g. test-exhaustion-1|20   ← 3 healing cycles leave a long trail
#      test-happy-1|13
#      test-blocked-1|10      ← early kill = short trail

# Step-by-step replay metadata for one run
sqlite3 data/orchestrator_checkpoints.sqlite \
  "SELECT checkpoint_id, substr(metadata,1,80) FROM checkpoints
   WHERE thread_id='test-exhaustion-1' ORDER BY checkpoint_id;"
```

Programmatic replay of a run's final state:

```python
from modules.orchestrator.graph import app
cfg = {"configurable": {"thread_id": "test-exhaustion-1"}}
snapshot = app.get_state(cfg)
print(snapshot.values["status"], snapshot.values["error_fingerprint"])
```

**Thread-hygiene rules (important):**
1. `thread_id` is **mandatory** — invoking without one raises
   `ValueError: Checkpointer requires ... thread_id`.
2. **Never reuse a `thread_id` across papers or fresh attempts** — checkpoint
   state (including `failure_count`) persists per thread, so a reused thread
   starts with a partially spent failure budget. Convention:
   `f"{paper_id}-run-{uuid}"`.
3. The checkpoint DB lives under `data/` (gitignored); delete it freely to
   reset all trajectories.
