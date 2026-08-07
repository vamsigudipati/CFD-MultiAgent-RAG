"""LangGraph state schema for the ML-CFD multi-agent orchestrator.

The AgentState payload flows through every node. Nodes return partial update
dictionaries; LangGraph merges them into this schema.
"""
from typing import TypedDict


class AgentState(TypedDict):
    paper_id: str            # identifies the current run
    blueprint_yaml: str      # raw text of the blueprint frontmatter file
    frontmatter: dict        # parsed + validated YAML fields
    execution_plan: str      # filled by Node B (Physics Reasoner)
    generated_code: str      # filled by Node C (Framework Sub-Agent)
    failure_count: int       # monotonic self-healing budget (k=3)
    error_fingerprint: str   # normalized failure-taxonomy fingerprint
    status: str              # routing state: 'FEASIBLE' | 'BLOCKED_DATA' | 'BLOCKED_PHYSICS' | ...
