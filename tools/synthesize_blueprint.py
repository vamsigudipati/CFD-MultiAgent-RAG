import argparse
import os
import re
import time
from pathlib import Path

from google import genai
from google.genai import errors
from langchain_text_splitters import MarkdownHeaderTextSplitter


# Deterministic semantic relevance keywords for chunk selection.
KEYWORD_WEIGHTS = {
    "architecture": 5,
    "network": 5,
    "model": 4,
    "method": 4,
    "methodology": 5,
    "equation": 5,
    "equations": 5,
    "pde": 5,
    "navier": 5,
    "continuity": 4,
    "momentum": 4,
    "boundary": 5,
    "boundary condition": 6,
    "initial condition": 5,
    "loss": 5,
    "objective": 4,
    "residual": 5,
    "normalization": 4,
    "non-dimensional": 4,
    "reynolds": 4,
    "dns": 3,
    "les": 3,
    "rans": 4,
    "training": 3,
    "optimizer": 3,
    "validation": 3,
}


def _load_markdown(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _split_markdown_by_headers(markdown_text: str):
    """Split markdown using semantic header boundaries."""
    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "h1"),
            ("##", "h2"),
            ("###", "h3"),
        ],
        strip_headers=False,
    )
    docs = splitter.split_text(markdown_text)
    return docs


def _score_chunk(text: str) -> int:
    low = text.lower()
    score = 0
    for key, w in KEYWORD_WEIGHTS.items():
        # Whole-word-ish matching for single words, substring for phrases.
        if " " in key:
            if key in low:
                score += w
        else:
            if re.search(rf"\b{re.escape(key)}\b", low):
                score += w
    return score


def _select_high_value_chunks(markdown_text: str, max_chunks: int = 18, max_chars: int = 32000) -> str:
    """Select semantically relevant sections for architecture/PDE/BC extraction."""
    docs = _split_markdown_by_headers(markdown_text)

    scored = []
    for idx, doc in enumerate(docs):
        chunk_text = (doc.page_content or "").strip()
        if not chunk_text:
            continue
        score = _score_chunk(chunk_text)
        scored.append((idx, score, chunk_text, doc.metadata or {}))

    # Keep high-scoring chunks first; tie-break by original order.
    scored.sort(key=lambda x: (-x[1], x[0]))

    selected = []
    selected_idx = set()

    # Primary pass: positive-score chunks.
    for idx, score, chunk_text, meta in scored:
        if score <= 0:
            continue
        if len(selected) >= max_chunks:
            break
        selected.append((idx, score, chunk_text, meta))
        selected_idx.add(idx)

    # Fallback: if too little selected, include early structural chunks.
    if not selected:
        for idx, score, chunk_text, meta in scored[:max_chunks]:
            selected.append((idx, score, chunk_text, meta))
            selected_idx.add(idx)

    # Restore original document order for coherent reading context.
    selected.sort(key=lambda x: x[0])

    out_sections = []
    used_chars = 0
    for idx, score, chunk_text, meta in selected:
        header = " > ".join(
            str(meta.get(k, "")).strip()
            for k in ("h1", "h2", "h3")
            if str(meta.get(k, "")).strip()
        )
        prefix = f"\n\n--- CHUNK {idx} | SCORE {score}"
        if header:
            prefix += f" | HEADER: {header}"
        prefix += " ---\n"

        block = prefix + chunk_text
        if used_chars + len(block) > max_chars:
            break
        out_sections.append(block)
        used_chars += len(block)

    return "".join(out_sections).strip()


def synthesize_paper(input_md_path: Path, output_md_path: Path) -> None:
    client = genai.Client()

    paper_content = _load_markdown(input_md_path)
    selected_context = _select_high_value_chunks(paper_content)

    prompt = f"""
Act as an expert Machine Learning Fluid Dynamics Engineer. Execute this task in three strict steps.

### Step 1: Extraction Quality Audit (internal, silent)
Review the extracted markdown for OCR fragmentation, broken LaTeX equations, or
parameters lost during batch extraction. Do NOT rewrite the paper. Hold any
corrections in mind and document them later in section 6.

### Step 2: Chain-of-Thought Synthesis (internal, silent)
Reason step-by-step about THIS paper's domain and identify:
  1. The exact flow regime and physical parameters (DNS/LES/RANS, Re, boundary conditions).
  2. The exact neural-network topology (PINN/CNN/RNN/GAN/...), layer counts, activations.
  3. The specific data normalization, scaling, or non-dimensionalization applied.
  4. The exact physical metrics used to validate the model (MSE, energy spectra, conservation laws).
  5. Any novel loss functions, unique architectural modifications, or specialized
     physics constraints that deviate from standard ML practice.

### Step 3: Blueprint Generation
Strip away ALL academic narrative. Use valid LaTeX ($...$ and $$...$$) for every
equation and symbol. Output ONLY the blueprint, formatted EXACTLY as:

## 1. Physical Problem Statement
## 2. Network Architectures
## 3. Data Scaling & Normalization
## 4. Required Physics Validation Gates
## 5. Architectural Innovations & Edge Cases
## 6. Raw Data Corrections Log

Rules:
- Be concrete and code-ready; prefer exact numbers, shapes, and equations over prose.
- In section 6, list every OCR fix, reconstructed equation, or missing/ambiguous
  parameter you had to infer. If the extraction was clean, write "No corrections required."
- LATEX SANITY RULE: Ensure all LaTeX macros are standard TeX commands (e.g., use `\\delta_{{ij}}`, NEVER `\\deltaij`).
- RAW TEXT FORMATTING RULE: In Section 6, when displaying raw broken OCR strings, malformed math, or invalid syntax, ALWAYS enclose them in code backticks.
- METADATA RULE: For the `section` field in the Traceability Matrix, you MUST use the exact text provided in the `HEADER:` prefix of the chunk where you found the information. Do not output "UNAVAILABLE" for `section` if a header is present. If you cannot find a physical page number, write "UNAVAILABLE" for `page` but still provide the `section`.
- GUARDRAIL: If this paper is NOT a fluid-dynamics ML modeling paper (e.g. a foundational AI,
  ethics, interpretability, or pure-methods paper with no flow regime and no trainable flow model),
  do not fabricate physics. Emit the same six headings but fill non-applicable sections with
  "N/A — not a fluid-dynamics ML modeling paper" and briefly state what the paper actually is in section 1.
- CONTEXT RULE: The source below is a semantic subset selected from the full paper by header-aware chunking.
  Treat missing details as unknown; never fabricate section/page evidence.

Here is the selected paper context:
{selected_context}
"""

    print(f"Synthesizing blueprint for {input_md_path.name}...")
    print(f"Selected context length: {len(selected_context):,} chars")

    fallback_models = [
        "gemini-3.6-flash",
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-flash",
    ]

    max_retries = 5
    base_delay = 60

    for _attempt in range(max_retries):
        for model_name in fallback_models:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )

                output_md_path.parent.mkdir(parents=True, exist_ok=True)
                output_md_path.write_text(response.text, encoding="utf-8")

                print(f"Blueprint saved to {output_md_path} (Model used: {model_name})")
                return

            except errors.ClientError as e:
                if e.code == 429:
                    print(
                        f"[Warning] API Rate Limit hit (429) on {model_name}. "
                        f"Sleeping for {base_delay} seconds..."
                    )
                    time.sleep(base_delay)
                    base_delay *= 2
                    break
                if e.code == 404:
                    print(f"[Info] {model_name} threw 404 NOT_FOUND. Routing to next fallback...")
                    continue

                raise e

    print(f"[Error] Failed to synthesize {input_md_path.name} after {max_retries} attempts.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Synthesize code-ready blueprints from normalized papers using semantic chunking."
    )
    parser.add_argument("input_file", type=Path, help="Path to normalized markdown.")
    parser.add_argument("output_file", type=Path, help="Path to save generated blueprint.")
    args = parser.parse_args()

    synthesize_paper(args.input_file, args.output_file)
