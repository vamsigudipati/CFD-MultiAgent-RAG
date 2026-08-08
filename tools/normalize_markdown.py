import argparse
import re
import unicodedata
from pathlib import Path


def normalize_markdown(file_path: Path) -> None:
    """Lightweight, non-destructive markdown normalization.

    Principle:
    - Trust Marker's native math/table output.
    - Avoid aggressive regex rewrites that mutate equations.
    - Only clean transport/noise artifacts and spacing issues.
    """
    text = file_path.read_text(encoding="utf-8")

    # Normalize Unicode composition while preserving semantic content.
    text = unicodedata.normalize("NFC", text)

    # Standardize line endings.
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove zero-width/control artifacts frequently introduced by OCR/PDF conversion.
    text = (
        text.replace("\ufeff", "")
        .replace("\u200b", "")
        .replace("\u200c", "")
        .replace("\u200d", "")
        .replace("\u2060", "")
    )

    # Normalize common spacing artifacts without touching math tokens.
    text = text.replace("\u00a0", " ")
    text = text.replace("\t", "    ")

    # Remove internal page anchor links/spans (layout noise, not scientific content).
    text = re.sub(
        r"\[([^\]\[]*(?:\[[^\]]*\][^\]\[]*)*)\]\(#page-[\w\-]+\)",
        r"\1",
        text,
    )
    text = re.sub(r"\(#page-[\w\-]+\)", "", text)
    text = re.sub(r'<span id="page-[\w\-]+"></span>\s*', "", text)
    text = re.sub(r"</?span[^>]*>", "", text)

    # Trim trailing spaces and collapse excessive blank lines.
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Ensure file ends with a single trailing newline.
    text = text.rstrip() + "\n"

    output_path = file_path.with_name(f"{file_path.stem}_normalized.md")
    output_path.write_text(text, encoding="utf-8")
    print(f"Normalization complete. Saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Lightweight normalization for Marker markdown outputs."
    )
    parser.add_argument("file", type=Path, help="Path to the markdown file to normalize.")
    args = parser.parse_args()
    normalize_markdown(args.file)