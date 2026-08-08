"""Node C5: Semantic code reviewer (LLM-as-a-judge with offline fallback).

Placed after Node C and before Node D test execution. This node compares the
traceability matrix embedded in generated_code against the code body and blocks
silent hallucinations:

1) Hardcoded optimizers / learning rates absent from traceability.
2) Hallucinated Navier-Stokes residual logic when traceability does not specify it.
"""
from __future__ import annotations

import json
import logging
import os
import re

from pydantic import BaseModel, Field

from .node_c import _load_env_file_if_present, _resolve_model_names, genai
from .state import AgentState

LOGGER = logging.getLogger(__name__)
MAX_REWRITES = 2


class ReviewResult(BaseModel):
    passed: bool
    critique: str = Field(default="")


REVIEWER_SYSTEM_PROMPT = (
    "You are a strict Semantic Code Reviewer for a Scientific-ML CFD pipeline.\n"
    "You are given (A) a JSON Traceability Matrix and (B) a generated PyTorch module.\n"
    "Judge ONLY whether the code is faithful to the matrix. Reject if:\n"
    "1. The code hardcodes an optimizer (torch.optim.*) or learning rate (lr=...) that is NOT "
    "explicitly specified in the matrix.\n"
    "2. The code computes a Navier-Stokes / continuity / momentum PDE residual loss when the "
    "matrix pde_formulation is UNAVAILABLE, empty, or does not specify these equations.\n"
    "Return STRICT JSON only: {\"passed\": bool, \"critique\": \"...\"}."
)


def _extract_matrix(code: str) -> dict:
    """Parse traceability JSON from the first triple-quoted block."""
    if not code:
        return {}
    match = re.search(r"^'''\s*(\{.*?\})\s*'''", code, re.S | re.M)
    if not match:
        match = re.search(r'^"""\s*(\{.*?\})\s*"""', code, re.S | re.M)
    if not match:
        return {}
    try:
        return json.loads(match.group(1))
    except Exception:
        return {}


def _matrix_value(matrix: dict, key: str) -> str:
    value = matrix.get(key)
    if isinstance(value, dict):
        return str(value.get("value", ""))
    return str(value or "")


def _contains_ns_equations(text: str) -> bool:
    low = text.lower()
    patterns = (
        r"du_dx", r"dv_dy", r"continuity", r"navier", r"momentum", r"divergence",
        r"torch\.autograd\.grad", r"residual",
    )
    return any(re.search(pat, low) for pat in patterns)


def _static_review(code: str, matrix: dict) -> ReviewResult:
    """Deterministic fallback review used when no live LLM is available."""
    matrix_blob = json.dumps(matrix).lower()
    critiques: list[str] = []

    optimizers = sorted(set(re.findall(r"torch\.optim\.(\w+)", code)))
    learning_rates = sorted(set(re.findall(r"lr\s*=\s*([0-9.eE-]+)", code)))

    if optimizers and not any(opt.lower() in matrix_blob for opt in optimizers):
        critiques.append(
            f"Hardcoded optimizer(s) {optimizers} absent from traceability matrix."
        )

    has_lr_evidence = (
        "learning rate" in matrix_blob
        or "learning_rate" in matrix_blob
        or any(lr.lower() in matrix_blob for lr in learning_rates)
    )
    if learning_rates and not has_lr_evidence:
        critiques.append(
            f"Hardcoded learning rate(s) {learning_rates} absent from traceability matrix."
        )

    pde_text = _matrix_value(matrix, "pde_formulation").strip().lower()
    matrix_has_ns = any(token in pde_text for token in ("navier", "continuity", "momentum", "incompressible"))
    if _contains_ns_equations(code) and not matrix_has_ns:
        critiques.append(
            "Code appears to implement Navier-Stokes/continuity residual logic but "
            "traceability matrix pde_formulation does not specify it."
        )

    if critiques:
        return ReviewResult(passed=False, critique=" ".join(critiques))
    return ReviewResult(
        passed=True,
        critique="Semantic review passed: no matrix/code contradictions detected.",
    )


def _llm_review(code: str, matrix: dict) -> ReviewResult | None:
    """Live LLM review path; returns None on any non-fatal failure."""
    _load_env_file_if_present()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key or genai is None:
        return None

    try:
        client = genai.Client(api_key=api_key)
    except Exception as exc:
        LOGGER.warning("Node C5: failed to initialize Gemini client (%s); using static fallback", exc)
        return None

    prompt = (
        f"{REVIEWER_SYSTEM_PROMPT}\n\n"
        f"TRACEABILITY MATRIX:\n{json.dumps(matrix, indent=2)}\n\n"
        f"GENERATED CODE:\n```python\n{code}\n```\n"
    )

    for model_name in _resolve_model_names():
        try:
            response = client.models.generate_content(model=model_name, contents=prompt)
            text = getattr(response, "text", None) or ""
            json_match = re.search(r"\{.*\}", text, re.S)
            if not json_match:
                continue
            payload = json.loads(json_match.group(0))
            return ReviewResult(**payload)
        except Exception as exc:
            LOGGER.warning("Node C5: review failed for model '%s' (%s)", model_name, exc)

    return None


def node_c5_code_reviewer(state: AgentState) -> dict:
    """Judge generated code against traceability before running test harness."""
    code = state.get("generated_code", "") or ""
    rewrite_count = int(state.get("rewrite_count", 0) or 0)
    matrix = _extract_matrix(code)

    result = _llm_review(code, matrix) or _static_review(code, matrix)

    if result.passed:
        LOGGER.info("Node C5: semantic review passed")
        return {
            "review_passed": True,
            "review_critique": "",
            "rewrite_count": 0,
        }

    LOGGER.warning(
        "Node C5: semantic review failed (rewrite_count=%s): %s",
        rewrite_count,
        result.critique,
    )
    return {
        "review_passed": False,
        "review_critique": result.critique,
        "rewrite_count": rewrite_count + 1,
    }
