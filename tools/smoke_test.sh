#!/usr/bin/env bash
#
# smoke_test.sh -- Platform regression smoke test.
#
# Purpose: a single command that answers "does the platform still work?" after
# dependency drift or a long hiatus. It re-runs the two proven end-to-end
# orchestration threads (a CNN-field paper and a continuous-PINN paper) through
# the full LangGraph engine + immutable Green Layer gates, and asserts that each
# reaches a PASSED terminal state.
#
# Design choices:
#   * OFFLINE / DETERMINISTIC: GEMINI_API_KEY is unset for the run so Node C uses
#     its deterministic fallback templates. This exercises the graph, routing,
#     gates, and checkpointing WITHOUT depending on a live LLM, network, or cost
#     -- exactly what a regression smoke test needs.
#   * SELF-CONTAINED: modules/workspace/ is gitignored, so this script recreates
#     the trust-anchor blueprint.yaml if it is missing.
#   * FRESH THREAD IDS: the SqliteSaver checkpointer forbids thread-id reuse, so
#     each invocation uses a unique timestamped thread id.
#
# Usage:
#   tools/smoke_test.sh
#   PYTHON=/path/to/python3 tools/smoke_test.sh   # override interpreter
#
# Exit code: 0 if BOTH runs PASSED, non-zero otherwise.

set -euo pipefail

# --- Resolve repo root (this script lives in tools/) -------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

PYTHON="${PYTHON:-python3}"
STAMP="$(date +%Y%m%d-%H%M%S)"

echo "=================================================================="
echo " Platform Smoke Test  (deterministic / offline)"
echo " Repo:        ${REPO_ROOT}"
echo " Interpreter: ${PYTHON}"
echo " Run stamp:   ${STAMP}"
echo "=================================================================="

# --- Ensure the trust-anchor blueprint exists (workspace is gitignored) ------
mkdir -p modules/workspace
BLUEPRINT="modules/workspace/blueprint.yaml"
if [[ ! -f "${BLUEPRINT}" ]]; then
  echo "[smoke] blueprint.yaml missing -- writing known-good incompressible_ns anchor"
  cat > "${BLUEPRINT}" <<'YAML'
closure_status: closed
pde_family: incompressible_ns
constraints:
  - kind: output_floor
    params: {floor: -10.0}
  - kind: regression_targets
    params: {expected_validation_loss: 0.8}
YAML
fi

# --- Drive both proven threads through the graph -----------------------------
# GEMINI_API_KEY is unset so Node C uses its deterministic fallback templates.
env -u GEMINI_API_KEY SMOKE_STAMP="${STAMP}" "${PYTHON}" - <<'PY'
import os
import sys

from modules.orchestrator.graph import app

stamp = os.environ["SMOKE_STAMP"]

# (paper_id, architecture it should route to, thread_id)
CASES = [
    ("2004.08826v3", "cnn_field", f"smoke-deepcfd-{stamp}"),
    ("Eivazi_2022_PINN_RANS_Navier_Stokes", "continuous_pinn", f"smoke-eivazi-{stamp}"),
]

BASE_STATE = {
    "failure_count": 0,
    "frontmatter": {},
    "status": "",
    "blueprint_yaml": "",
    "execution_plan": "",
    "generated_code": "",
    "error_fingerprint": "",
}

all_passed = True
for paper_id, expected_mode, thread_id in CASES:
    state = dict(BASE_STATE, paper_id=paper_id)
    config = {"configurable": {"thread_id": thread_id}}
    print(f"\n[smoke] running paper_id={paper_id!r} (expect {expected_mode}) thread={thread_id}")
    try:
        result = app.invoke(state, config=config)
        status = result.get("status")
        attempts = result.get("failure_count", 0)
        fingerprint = result.get("error_fingerprint") or "None"
        ok = status == "PASSED"
        all_passed = all_passed and ok
        mark = "PASS" if ok else "FAIL"
        print(f"[smoke] {mark}: status={status} attempts={attempts} fingerprint={fingerprint}")
    except Exception as exc:  # pragma: no cover - surfaced as a failure below
        all_passed = False
        print(f"[smoke] FAIL: paper_id={paper_id!r} crashed: {exc}")

print("\n==================================================================")
if all_passed:
    print("SMOKE TEST PASSED -- both proven threads reached PASSED.")
    sys.exit(0)
else:
    print("SMOKE TEST FAILED -- see per-case output above.")
    sys.exit(1)
PY
