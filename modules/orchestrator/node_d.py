"""Node D: Test execution runner via subprocess and failure fingerprinting."""
import os
import sys
import subprocess
from pathlib import Path
from .state import AgentState

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_DIR = REPO_ROOT / "modules" / "workspace"
MONOLITH_PATH = WORKSPACE_DIR / "train_and_val.py"
HARNESS_DIR = REPO_ROOT / "modules" / "validation_harness"


def _classify_failure(output: str) -> str:
    """Classifies pytest output into a normalized failure fingerprint taxonomy."""
    if "SYNTAX:" in output or "SyntaxError" in output:
        return "SYNTAX"
    if "UNSUPPORTED_CONSTRAINT" in output:
        return "UNSUPPORTED_CONSTRAINT"

    failed_lines = []
    for line in output.splitlines():
        if "FAILED" in line and "test_" in line:
            # Extract test name token for normalization
            parts = line.strip().split()
            for token in parts:
                if token.startswith("test_"):
                    # Strip out parameterization suffixes for stable fingerprinting
                    test_name = token.split("[")[0]
                    # Identify tier from test name prefix or path context
                    tier = "t3" if "regression" in test_name or "multi_seed" in test_name else "t2"
                    failed_lines.append(f"{tier}:{test_name}")
                    break

    if failed_lines:
        # Deduplicate and sort to ensure identical failure sets yield identical fingerprints
        unique_sorted = sorted(list(set(failed_lines)))
        return "GATE_FAIL|" + "|".join(unique_sorted)

    if "AssertionError" in output:
        return "GATE_FAIL|unclassified_assertion"

    return "UNKNOWN"


def node_d_execute_tests(state: AgentState) -> dict:
    """Executes the PyTest validation harness against the monolith with hang protection."""
    MONOLITH_PATH.parent.mkdir(parents=True, exist_ok=True)
    MONOLITH_PATH.write_text(state.get("generated_code", ""))

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

    env = {**os.environ, "WORKSPACE_DIR": str(WORKSPACE_DIR.resolve())}

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
        return {
            "status": "FAILED",
            "error_fingerprint": "HANG",
            "failure_count": new_failures,
        }

    if result.returncode == 0:
        return {
            "status": "PASSED",
            "error_fingerprint": "",
            "failure_count": state.get("failure_count", 0),
        }

    fingerprint = _classify_failure(result.stdout + "\n" + result.stderr)
    new_failures = state.get("failure_count", 0) + 1
    return {
        "status": "FAILED",
        "error_fingerprint": fingerprint,
        "failure_count": new_failures,
    }