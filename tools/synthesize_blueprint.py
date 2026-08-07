import os
import time
import argparse
from pathlib import Path
from google import genai
from google.genai import errors

def synthesize_paper(input_md_path, output_md_path):
    client = genai.Client()

    with open(input_md_path, "r", encoding="utf-8") as f:
        paper_content = f.read()

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
    - RAW TEXT FORMATTING RULE: In Section 6, when displaying raw broken OCR strings, malformed math, or invalid syntax, ALWAYS enclose them in code backticks (e.g., `deltaij`), NOT inside LaTeX math delimiters ($...).
    - GUARDRAIL: If this paper is NOT a fluid-dynamics ML modeling paper (e.g. a
      foundational AI, ethics, interpretability, or pure-methods paper with no flow
      regime and no trainable flow model), do not fabricate physics. Emit the same six
      headings but fill the non-applicable sections with "N/A — not a fluid-dynamics ML
      modeling paper" and briefly state what the paper actually is in section 1.

    Here is the paper:
    {paper_content}
    """

    print(f"Synthesizing blueprint for {input_md_path.name}...")
    
    # Priority list starting with verified active model
    fallback_models = [
        'gemini-3.6-flash',
        'gemini-2.5-flash',
        'gemini-2.0-flash',
        'gemini-1.5-flash'
    ]
    
    max_retries = 5
    base_delay = 60
    
    for attempt in range(max_retries):
        for model_name in fallback_models:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                
                output_md_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_md_path, "w", encoding="utf-8") as f:
                    f.write(response.text)
                    
                print(f"Blueprint saved to {output_md_path} (Model used: {model_name})")
                return  # Success, exit the function entirely
                
            except errors.ClientError as e:
                if e.code == 429:
                    print(f"[Warning] API Rate Limit hit (429) on {model_name}. Sleeping for {base_delay} seconds...")
                    time.sleep(base_delay)
                    base_delay *= 2
                    break  # Break the inner model loop, retry outer attempt loop
                elif e.code == 404:
                    print(f"[Info] {model_name} threw 404 NOT_FOUND. Routing to next fallback...")
                    continue  # Try the next model in the list
                else:
                    raise e  # Raise any other critical errors (e.g., 403 Forbidden)
                    
    print(f"[Error] Failed to synthesize {input_md_path.name} after {max_retries} attempts.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synthesize code-ready blueprints from normalized papers.")
    parser.add_argument("input_file", type=Path, help="Path to the normalized markdown file.")
    parser.add_argument("output_file", type=Path, help="Path to save the generated blueprint.")
    args = parser.parse_args()
    
    synthesize_paper(args.input_file, args.output_file)