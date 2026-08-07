import re
import argparse
from pathlib import Path

def normalize_markdown(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # --- 1. Unescape markdown-escaped parens from citations/equation refs
    text = text.replace("\\(", "(").replace("\\)", ")")

    # --- 2. Remove internal PDF page-anchor links and span tags
    text = re.sub(r'\[([^\]\[]*(?:\[[^\]]*\][^\]\[]*)*)\]\(#page-[\w\-]+\)', r'\1', text)
    text = re.sub(r'\(#page-[\w\-]+\)', '', text)
    text = re.sub(r'<span id="page-[\w\-]+"></span>\s*', '', text)
    text = re.sub(r'</?span[^>]*>', '', text)

    # --- 2.5. Convert Marker's table-formatted numbered equations to LaTeX blocks.
    # Marker right-aligns equation numbers by wrapping the equation in a 1-row table:
    #     | $\hat{u} = u$ , ... | (2) |
    #     |---------------------|-----|
    #     |---------------------|-----|   (sometimes a duplicated divider row)
    # This collapses that structure into a standard block equation:
    #     $$ \hat{u} = u , ... \quad (2) $$
    eq_table_pattern = re.compile(
        r'^[ \t]*\|(?P<eq>.+?)\|[ \t]*\((?P<num>\d+)\)[ \t]*\|[ \t]*\n'  # equation + number row
        r'(?:[ \t]*\|[\s\-|:]+\|[ \t]*\n)+',                             # one or more divider rows
        re.MULTILINE,
    )

    def _eq_table_repl(m):
        eq = m.group("eq").strip()
        num = m.group("num")
        eq = eq.replace("$", "")           # drop inline math delimiters
        eq = " ".join(eq.split())          # collapse internal whitespace
        eq = eq.strip().rstrip(",").strip()  # trim trailing comma from the last cell
        return f"$$ {eq} \\quad ({num}) $$\n"

    text = eq_table_pattern.sub(_eq_table_repl, text)

    # --- 3. Fix broken angle-bracket averaging notation
    text = text.replace("with h·i corresponding", "with $\\langle \\cdot \\rangle$ corresponding")
    text = text.replace("h·i", "$\\langle \\cdot \\rangle$")

    # --- 4. Specific multi-token CFD reconstructions
    specific = [
        (r"where <sup>I</sup> ∈ <sup>R</sup> d1×d<sup>2</sup>", r"where $I \in \mathbb{R}^{d_1 \times d_2}$"),
        (r"<sup>L</sup><sup>x</sup> × <sup>L</sup><sup>z</sup> <sup>=</sup>", r"$L_x \times L_z =$"),
        (r"O\(Re<sup>2</sup> τ \)", r"$O(Re_\tau^2)$"),
        (r"kzkxφij \(λ \+ x , λ<sup>\+</sup> z \)", r"$k_z k_x \phi_{ij}(\lambda_x^+, \lambda_z^+)$"),
        (r"i\.e\. y <sup>\+</sup> <sup>=</sup> \{15, <sup>30</sup>, <sup>50</sup>, <sup>100</sup>, <sup>150</sup>\}", r"i.e. $y^+ =$ {15, 30, 50, 100, 150}"),
        (r"friction velocity u<sup>τ</sup> = p τw/ρ", r"friction velocity $u_\tau = \sqrt{\tau_w / \rho}$"),
        (r"nearly constant β ' 1\.4", r"nearly constant $\beta \approx 1.4$"),
        (r"Re<sup>c</sup> = 10<sup>7</sup>", r"$Re_c = 10^7$"),
        (r"correlation coefficient <sup>R</sup>FCN;DNS\(u\)", r"correlation coefficient $R_{\text{FCN;DNS}}(u)$"),
        (r"at y \+ target using the velocity-fluctuation fields farther from the wall at y \+\s*input", r"at $y^+_{\text{target}}$ using the velocity-fluctuation fields farther from the wall at $y^+_{\text{input}}$"),
        (r"defined as: \$\\Delta y\^\+\$ = y \+\s*input − \$\^\{y\}\$ \+ target\.", r"defined as: $\\Delta y^+ = y^+_{\text{input}} - y^+_{\\text{target}}$."),
    ]
    for pat, repl in specific:
        text = re.sub(pat, lambda m, r=repl: r, text, flags=re.DOTALL)

    # --- 5. General Re^X and y+ subscript patterns
    text = re.sub(r"Re<sup>τ</sup>", lambda m: r"$Re_\tau$", text)
    text = re.sub(r"Re<sup>θ</sup>", lambda m: r"$Re_\theta$", text)
    text = re.sub(r"Re<sup>c</sup>", lambda m: r"$Re_c$", text)
    text = re.sub(r"u<sup>τ</sup>", lambda m: r"$u_\tau$", text)
    text = re.sub(r"τ<sup>w</sup>", lambda m: r"$\tau_w$", text)
    text = re.sub(r"∆y\s*<sup>\+</sup>", lambda m: r"$\Delta y^+$", text)
    text = re.sub(r"y\s*<sup>\+</sup>", lambda m: r"$y^+$", text)

    # --- 6. Generic <sup> and <sub> to LaTeX conversion
    def sup_repl(m):
        content = m.group(1).replace("τ", r"\tau").replace("θ", r"\theta")
        return f"$^{{{content}}}$"
    
    def sub_repl(m):
        content = m.group(1).replace("τ", r"\tau").replace("θ", r"\theta")
        return f"$_{{{content}}}$"

    text = re.sub(r"<sup>∗</sup>", lambda m: r"$^{*}$", text)
    text = re.sub(r"<sup>([^<]*)</sup>", sup_repl, text)
    text = re.sub(r"<sub>([^<]*)</sub>", sub_repl, text)

    # Save output
    output_path = file_path.with_name(f"{file_path.stem}_normalized.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    
    print(f"Normalization complete. Saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Normalize Marker PDF Markdown outputs.")
    parser.add_argument("file", type=Path, help="Path to the markdown file to normalize.")
    args = parser.parse_args()
    normalize_markdown(args.file)