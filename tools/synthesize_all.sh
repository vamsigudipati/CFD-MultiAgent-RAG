#!/bin/bash
# Synthesize architectural blueprints for EVERY already-extracted paper.
#
# This is the "synthesize-only" batch loop: it assumes Marker extraction +
# normalization already ran (docs/extracted_papers/<name>/<name>.md exists) and
# only calls the LLM synthesizer. It NEVER modifies the extracted markdown.
#
# Prerequisites (the automated synthesizer is otherwise blocked):
#   1. export GEMINI_API_KEY=...        # set this yourself in your shell
#   2. a Python interpreter with `google-genai` installed (base conda has it)
#
# Usage:
#   export GEMINI_API_KEY=...
#   PY=/Users/vamsigudipati/miniconda3/bin/python3 tools/synthesize_all.sh
#
# Set FORCE=1 to overwrite existing blueprints (default: skip them).
set -euo pipefail

EXTRACT_DIR="docs/extracted_papers"
SYNTHESIZER="tools/synthesize_blueprint.py"
PY="${PY:-python3}"
FORCE="${FORCE:-0}"

if [[ -z "${GEMINI_API_KEY:-}" ]]; then
    echo "ERROR: GEMINI_API_KEY is not set. Run 'export GEMINI_API_KEY=...' first." >&2
    exit 1
fi

if ! "$PY" -c "import google.genai" >/dev/null 2>&1; then
    echo "ERROR: '$PY' cannot import google.genai. Set PY to an interpreter that has google-genai." >&2
    exit 1
fi

total=0; made=0; skipped=0; failed=0
echo "=================================================="
echo " Synthesizing blueprints for all extracted papers"
echo "=================================================="

for paper_dir in "$EXTRACT_DIR"/*/; do
    name="$(basename "$paper_dir")"
    raw_md="${paper_dir}${name}.md"
    
    # UPDATED: Blueprint now saves directly into the paper's specific folder
    blueprint_md="${paper_dir}${name}_blueprint.md"

    [[ -f "$raw_md" ]] || { echo ">> SKIP $name (no extracted markdown)"; continue; }
    total=$((total+1))

    if [[ -f "$blueprint_md" && "$FORCE" != "1" ]]; then
        echo ">> SKIP $name (blueprint exists; set FORCE=1 to overwrite)"
        skipped=$((skipped+1))
        continue
    fi

    echo "--------------------------------------------------"
    echo ">> Synthesizing: $name"
    if "$PY" "$SYNTHESIZER" "$raw_md" "$blueprint_md"; then
        made=$((made+1))
    else
        echo ">> ERROR synthesizing $name" >&2
        failed=$((failed+1))
    fi
done

echo "=================================================="
echo " Done. eligible=$total  created=$made  skipped=$skipped  failed=$failed"
echo " Blueprints saved in $EXTRACT_DIR/<name>/"
echo "=================================================="