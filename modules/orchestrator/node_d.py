"""Node D: Test execution runner via subprocess and failure fingerprinting."""
import logging
import os
import re
import sys
import subprocess
import time
from pathlib import Path
from .state import AgentState

LOGGER = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_DIR = REPO_ROOT / "modules" / "workspace"
# Backward-compatibility shim for tests/utilities that still import the legacy
# static monolith path. Runtime execution now uses _resolve_workspace_dir(...).
MONOLITH_PATH = WORKSPACE_DIR / "train_and_val.py"
HARNESS_DIR = REPO_ROOT / "modules" / "validation_harness"


def _resolve_workspace_dir(state: AgentState, config=None) -> Path:
    """Return a thread-isolated workspace for this paper/run.

    Layout: modules/workspace/<paper_id>_<thread_id>/train_and_val.py
    """
    paper_id = str(state.get("paper_id", "unknown_paper"))
    thread_id = "default-thread"
    if config is not None:
        config_block = config.get("configurable", {}) or {}
        thread_id = str(config_block.get("thread_id", thread_id))

    safe_paper_id = re.sub(r"[^A-Za-z0-9_.-]+", "_", paper_id)
    safe_thread_id = re.sub(r"[^A-Za-z0-9_.-]+", "_", thread_id)
    return WORKSPACE_DIR / f"{safe_paper_id}_{safe_thread_id}"


def _classify_failure(output: str) -> str:
    """Classifies pytest output into a normalized failure fingerprint taxonomy."""
    if "SYNTAX:" in output or "SyntaxError" in output:
        return "SYNTAX"
    if "UNSUPPORTED_CONSTRAINT" in output:
        return "UNSUPPORTED_CONSTRAINT"

    failed_lines = []
    test_pattern = re.compile(r"::(test_[A-Za-z0-9_]+)")
    for line in output.splitlines():
        if "FAILED" in line and "test_" in line:
            match = test_pattern.search(line)
            if not match:
                continue

            # Strip parameterization suffixes for stable fingerprints.
            test_name = match.group(1).split("[")[0]

            lower_line = line.lower()
            if "test_gates_t0" in lower_line:
                tier = "t0"
            elif "test_gates_t1" in lower_line:
                tier = "t1"
            elif "test_gates_t2" in lower_line:
                tier = "t2"
            elif "test_gates_t3" in lower_line:
                tier = "t3"
            elif "regression" in test_name or "multi_seed" in test_name:
                tier = "t3"
            else:
                tier = "t2"

            failed_lines.append(f"{tier}:{test_name}")

    if failed_lines:
        # Deduplicate and sort to ensure identical failure sets yield identical fingerprints
        unique_sorted = sorted(list(set(failed_lines)))
        return "GATE_FAIL|" + "|".join(unique_sorted)

    if "AssertionError" in output:
        return "GATE_FAIL|unclassified_assertion"

    return "UNKNOWN"


def node_d_execute_tests(state: AgentState, config=None) -> dict:
    """Executes the PyTest validation harness against the monolith with hang protection."""
    workspace_dir = _resolve_workspace_dir(state, config=config)
    monolith_path = workspace_dir / "train_and_val.py"
    workspace_dir.mkdir(parents=True, exist_ok=True)
    monolith_path.write_text(state.get("generated_code", ""))
    LOGGER.info(
        "Node D: wrote monolith to %s (%s chars) and starting Green Layer run (attempt %s)",
        monolith_path,
        len(state.get("generated_code", "")),
        state.get("failure_count", 0) + 1,
    )
    start_time = time.time()

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        str(HARNESS_DIR),
        "-v",
        "--tb=short",
        "-p",
        "no:cacheprovider",
    ]

    env = {**os.environ, "WORKSPACE_DIR": str(workspace_dir.resolve())}

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
            env=env,
            timeout=600,  # 10-minute hard ceiling against top-level import hangups
        )
    except subprocess.TimeoutExpired:
        new_failures = state.get("failure_count", 0) + 1
        LOGGER.error(
            "Node D: Green Layer HANG after %.1fs (failure_count -> %s)",
            time.time() - start_time, new_failures,
        )
        return {
            "status": "FAILED",
            "error_fingerprint": "HANG",
            "failure_count": new_failures,
        }

    if result.returncode == 0:
        LOGGER.info("Node D: Green Layer PASSED in %.1fs", time.time() - start_time)
        return {
            "status": "PASSED",
            "error_fingerprint": "",
            "failure_count": state.get("failure_count", 0),
        }

    fingerprint = _classify_failure(result.stdout + "\n" + result.stderr)
    new_failures = state.get("failure_count", 0) + 1
    LOGGER.warning(
        "Node D: Green Layer FAILED in %.1fs (failure_count -> %s, fingerprint=%s)",
        time.time() - start_time, new_failures, fingerprint,
    )
    return {
        "status": "FAILED",
        "error_fingerprint": fingerprint,
        "failure_count": new_failures,
    }