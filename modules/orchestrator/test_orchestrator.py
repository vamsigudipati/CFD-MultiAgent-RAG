"""Committed test suite for the orchestrator graph, verifying happy path, 
feasibility kill-switches, and budget exhaustion behavior.
"""
import pytest
from pathlib import Path
from modules.orchestrator.graph import app
from modules.orchestrator.nodes import BLUEPRINT_YAML_PATH
from modules.orchestrator.node_d import MONOLITH_PATH, WORKSPACE_DIR

@pytest.fixture(autouse=True)
def clean_workspace():
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    yield
    if BLUEPRINT_YAML_PATH.exists():
        BLUEPRINT_YAML_PATH.unlink()
    if MONOLITH_PATH.exists():
        MONOLITH_PATH.unlink()


def test_happy_path_execution():
    BLUEPRINT_YAML_PATH.write_text(
        "closure_status: closed\n"
        "pde_family: incompressible_ns\n"
        "constraints:\n"
        "  - kind: output_floor\n"
        "    params: {floor: -100.0}\n"
    )
    state = {
        "paper_id": "test_happy",
        "failure_count": 0,
        "frontmatter": {},
        "status": "",
        "blueprint_yaml": "",
        "execution_plan": "",
        "generated_code": "",
        "error_fingerprint": "",
    }
    result = app.invoke(state, config={"configurable": {"thread_id": "test-happy-1"}})
    assert result["status"] == "PASSED"
    assert result["failure_count"] == 0


def test_blocked_data_kill_switch():
    BLUEPRINT_YAML_PATH.write_text("closure_status: unclosed\npde_family: incompressible_ns\n")
    state = {
        "paper_id": "test_blocked",
        "failure_count": 0,
        "frontmatter": {},
        "status": "",
        "blueprint_yaml": "",
        "execution_plan": "",
        "generated_code": "",
        "error_fingerprint": "",
    }
    result = app.invoke(state, config={"configurable": {"thread_id": "test-blocked-1"}})
    assert result["status"] == "BLOCKED_DATA"
    assert result["generated_code"] == ""


def test_budget_exhaustion_blocks_physics():
    # Enforcing an impossible output floor forces recurring failure up to MAX_FAILURES (3)
    BLUEPRINT_YAML_PATH.write_text(
        "closure_status: closed\n"
        "pde_family: incompressible_ns\n"
        "constraints:\n"
        "  - kind: output_floor\n"
        "    params: {floor: 0.5}\n"
    )
    state = {
        "paper_id": "test_exhaustion",
        "failure_count": 0,
        "frontmatter": {},
        "status": "",
        "blueprint_yaml": "",
        "execution_plan": "",
        "generated_code": "",
        "error_fingerprint": "",
    }
    result = app.invoke(state, config={"configurable": {"thread_id": "test-exhaustion-1"}})
    assert result["status"] == "BLOCKED_PHYSICS"
    assert result["failure_count"] == 3