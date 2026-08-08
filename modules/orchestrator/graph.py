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
import logging
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph

from .node_c import node_c_framework_supervisor
from .node_c5_code_reviewer import MAX_REWRITES, node_c5_code_reviewer
from .node_d import node_d_execute_tests
from .nodes import node_a_ingest, node_a5_feasibility_check, node_b_physics_reasoner
from .state import AgentState

MAX_FAILURES = 3

# Absolute anchor from repo root (modules/orchestrator/graph.py -> root is parents[2])
REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKPOINT_DB_PATH = REPO_ROOT / "data" / "orchestrator_checkpoints.sqlite"
CHECKPOINT_DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# --- File-based observability -------------------------------------------------
LOGS_DIR = REPO_ROOT / "logs"
ORCHESTRATOR_LOG_PATH = LOGS_DIR / "orchestrator.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def configure_orchestrator_logging(level: int = logging.INFO) -> logging.Logger:
    """Attach a shared FileHandler to the root logger (idempotent).

    Every module logger (modules.orchestrator.*, validation harness, run
    scripts) propagates to root, so a single file handler captures the full
    orchestration trace in logs/orchestrator.log.
    """
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    root = logging.getLogger()
    already_attached = any(
        isinstance(h, logging.FileHandler)
        and getattr(h, "baseFilename", "") == str(ORCHESTRATOR_LOG_PATH)
        for h in root.handlers
    )
    if not already_attached:
        handler = logging.FileHandler(ORCHESTRATOR_LOG_PATH, encoding="utf-8")
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
        root.addHandler(handler)
    if root.level > level or root.level == logging.NOTSET:
        root.setLevel(level)
    return logging.getLogger("modules.orchestrator")


LOGGER = configure_orchestrator_logging()


def node_block_physics(state: AgentState) -> dict:
    """Terminal stamp: budget exhausted or unenforceable constraint."""
    LOGGER.error(
        "Terminal BLOCKED_PHYSICS: failure_count=%s fingerprint=%s",
        state.get("failure_count", 0), state.get("error_fingerprint", ""),
    )
    return {"status": "BLOCKED_PHYSICS"}


def node_block_review(state: AgentState) -> dict:
    """Terminal stamp: semantic reviewer rewrite budget exhausted."""
    LOGGER.error(
        "Terminal BLOCKED_REVIEW: rewrite_count=%s critique=%s",
        state.get("rewrite_count", 0),
        state.get("review_critique", ""),
    )
    return {"status": "BLOCKED_REVIEW"}


def _route_after_feasibility(state: AgentState) -> str:
    """Deterministic conditional edge keyed exclusively off the typed status."""
    route = "feasible" if state["status"] == "FEASIBLE" else "blocked"
    LOGGER.info("Feasibility route: %s (status=%s)", route, state["status"])
    return route


def _route_after_planner(state: AgentState) -> str:
    """Route after Node B so planner kill-switch can halt before code generation."""
    route = "blocked" if state.get("status") == "BLOCKED_DATA" else "continue"
    LOGGER.info("Planner route: %s (status=%s)", route, state.get("status", ""))
    return route


def _route_after_tests(state: AgentState) -> str:
    """Deterministic self-healing router (typed fields only)."""
    fingerprint = state.get("error_fingerprint", "")
    failure_count = state.get("failure_count", 0)
    if state["status"] == "PASSED":
        route = "done"
    elif failure_count >= MAX_FAILURES or fingerprint == "UNSUPPORTED_CONSTRAINT":
        route = "blocked"
    elif fingerprint in ("SYNTAX", "HANG"):
        route = "fix_code"
    elif fingerprint.startswith("GATE_FAIL"):
        route = "fix_physics"
    else:
        route = "blocked"  # UNKNOWN -> terminate rather than thrash
    LOGGER.info(
        "Self-healing route: %s (status=%s failures=%s fingerprint=%s)",
        route, state["status"], failure_count, fingerprint or "None",
    )
    return route


def _route_after_semantic_review(state: AgentState) -> str:
    """Semantic judge route: proceed, request rewrite, or stop after budget."""
    if state.get("review_passed"):
        route = "approved"
    elif int(state.get("rewrite_count", 0) or 0) > MAX_REWRITES:
        route = "blocked"
    else:
        route = "rewrite"
    LOGGER.info(
        "Semantic review route: %s (review_passed=%s rewrite_count=%s)",
        route,
        state.get("review_passed", False),
        state.get("rewrite_count", 0),
    )
    return route


workflow = StateGraph(AgentState)

workflow.add_node("node_a_ingest", node_a_ingest)
workflow.add_node("node_a5_feasibility_check", node_a5_feasibility_check)
workflow.add_node("node_b_physics_reasoner", node_b_physics_reasoner)
workflow.add_node("node_c_framework_supervisor", node_c_framework_supervisor)
workflow.add_node("node_c5_code_reviewer", node_c5_code_reviewer)
workflow.add_node("node_d_execute_tests", node_d_execute_tests)
workflow.add_node("node_block_physics", node_block_physics)
workflow.add_node("node_block_review", node_block_review)

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

workflow.add_conditional_edges(
    "node_b_physics_reasoner",
    _route_after_planner,
    {
        "continue": "node_c_framework_supervisor",
        "blocked": END,
    },
)
workflow.add_edge("node_c_framework_supervisor", "node_c5_code_reviewer")

workflow.add_conditional_edges(
    "node_c5_code_reviewer",
    _route_after_semantic_review,
    {
        "approved": "node_d_execute_tests",
        "rewrite": "node_c_framework_supervisor",
        "blocked": "node_block_review",
    },
)

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
workflow.add_edge("node_block_review", END)

# Compile graph with persistent SQLite checkpointer attached
conn = sqlite3.connect(str(CHECKPOINT_DB_PATH), check_same_thread=False)
checkpointer = SqliteSaver(conn)
app = workflow.compile(checkpointer=checkpointer)