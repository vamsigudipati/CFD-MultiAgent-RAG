"""LangGraph wiring for the ML-CFD multi-agent orchestrator.

Topology (Phase 4 structural compile):

    START -> node_a_ingest -> node_a5_feasibility_check
                 |-- status == FEASIBLE     --> node_b_physics_reasoner
                 |-- status == BLOCKED_DATA --> END        (kill switch)
    node_b_physics_reasoner -> node_c_supervisor -> END

Node C is a stub for now; the framework sub-agent dispatch will replace it.
"""
from langgraph.graph import END, START, StateGraph

from .nodes import node_a_ingest, node_a5_feasibility_check, node_b_physics_reasoner
from .state import AgentState


def node_c_supervisor(state: AgentState) -> dict:
    """Stub Framework Supervisor -- will route to PyTorch/TF/Keras sub-agents."""
    return {"status": "GENERATED"}


def _route_after_feasibility(state: AgentState) -> str:
    """Deterministic conditional edge keyed exclusively off the typed status."""
    return "feasible" if state["status"] == "FEASIBLE" else "blocked"


workflow = StateGraph(AgentState)

workflow.add_node("node_a_ingest", node_a_ingest)
workflow.add_node("node_a5_feasibility_check", node_a5_feasibility_check)
workflow.add_node("node_b_physics_reasoner", node_b_physics_reasoner)
workflow.add_node("node_c_supervisor", node_c_supervisor)

workflow.add_edge(START, "node_a_ingest")
workflow.add_edge("node_a_ingest", "node_a5_feasibility_check")

workflow.add_conditional_edges(
    "node_a5_feasibility_check",
    _route_after_feasibility,
    {
        "feasible": "node_b_physics_reasoner",
        "blocked": END,
    },
)

workflow.add_edge("node_b_physics_reasoner", "node_c_supervisor")
workflow.add_edge("node_c_supervisor", END)

app = workflow.compile()
