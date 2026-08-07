"""LangGraph wiring for the ML-CFD multi-agent orchestrator (Phase 4 final).

Topology:

    START -> node_a_ingest -> node_a5_feasibility_check
                 |-- FEASIBLE      --> node_b_physics_reasoner
                 |-- BLOCKED_DATA  --> END                       (kill switch 1)
    node_b_physics_reasoner -> node_c_framework_supervisor -> node_d_execute_tests
    node_d_execute_tests:
                 |-- PASSED                                  --> END
                 |-- budget >= 3 or UNSUPPORTED_CONSTRAINT   --> node_block_physics -> END
                 |-- SYNTAX / HANG                           --> node_c (code fix)
                 |-- GATE_FAIL*                              --> node_b (physics fix)

Routing is keyed exclusively off typed state fields (status / fingerprint /
failure_count) -- never prose.
Persistent state checkpointing is enabled via SqliteSaver.
"""
from pathlib import Path
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph

from .node_c import node_c_framework_supervisor
from .node_d import node_d_execute_tests
from .nodes import node_a_ingest, node_a5_feasibility_check, node_b_physics_reasoner
from .state import AgentState

MAX_FAILURES = 3

# Absolute anchor from repo root (modules/orchestrator/graph.py -> root is parents[2])
REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKPOINT_DB_PATH = REPO_ROOT / "data" / "orchestrator_checkpoints.sqlite"
CHECKPOINT_DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def node_block_physics(state: AgentState) -> dict:
    """Terminal stamp: budget exhausted or unenforceable constraint."""
    return {"status": "BLOCKED_PHYSICS"}


def _route_after_feasibility(state: AgentState) -> str:
    """Deterministic conditional edge keyed exclusively off the typed status."""
    return "feasible" if state["status"] == "FEASIBLE" else "blocked"


def _route_after_tests(state: AgentState) -> str:
    """Deterministic self-healing router (typed fields only)."""
    if state["status"] == "PASSED":
        return "done"
    fingerprint = state.get("error_fingerprint", "")
    if state.get("failure_count", 0) >= MAX_FAILURES or fingerprint == "UNSUPPORTED_CONSTRAINT":
        return "blocked"
    if fingerprint in ("SYNTAX", "HANG"):
        return "fix_code"
    if fingerprint.startswith("GATE_FAIL"):
        return "fix_physics"
    return "blocked"  # UNKNOWN -> terminate rather than thrash


workflow = StateGraph(AgentState)

workflow.add_node("node_a_ingest", node_a_ingest)
workflow.add_node("node_a5_feasibility_check", node_a5_feasibility_check)
workflow.add_node("node_b_physics_reasoner", node_b_physics_reasoner)
workflow.add_node("node_c_framework_supervisor", node_c_framework_supervisor)
workflow.add_node("node_d_execute_tests", node_d_execute_tests)
workflow.add_node("node_block_physics", node_block_physics)

workflow.add_edge(START, "node_a_ingest")
workflow.add_edge("node_a_ingest", "node_a5_feasibility_check")

workflow.add_conditional_edges(
    "node_a5_feasibility_check",
    _route_after_feasibility,
    {
        "feasible": "node_b_physics_reasoner",
        "blocked": END,  # status already BLOCKED_DATA
    },
)

workflow.add_edge("node_b_physics_reasoner", "node_c_framework_supervisor")
workflow.add_edge("node_c_framework_supervisor", "node_d_execute_tests")

workflow.add_conditional_edges(
    "node_d_execute_tests",
    _route_after_tests,
    {
        "done": END,                                   # status PASSED
        "blocked": "node_block_physics",               # stamp BLOCKED_PHYSICS
        "fix_code": "node_c_framework_supervisor",     # SYNTAX/HANG -> code mechanics
        "fix_physics": "node_b_physics_reasoner",      # GATE_FAIL -> re-plan
    },
)

workflow.add_edge("node_block_physics", END)

# Compile graph with persistent SQLite checkpointer attached
conn = sqlite3.connect(str(CHECKPOINT_DB_PATH), check_same_thread=False)
checkpointer = SqliteSaver(conn)
app = workflow.compile(checkpointer=checkpointer)