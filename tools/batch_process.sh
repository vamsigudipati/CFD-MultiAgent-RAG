#!/bin/bash

PDF_DIR="pdf_repository"
EXTRACT_DIR="docs/extracted_papers"
NORMALIZER="tools/normalize_markdown.py"

echo "=================================================="
echo " Starting ML-CFD Batch Extraction & Normalization"
echo "=================================================="

for pdf_file in "$PDF_DIR"/*.pdf; do
    [ -e "$pdf_file" ] || continue
    
    filename=$(basename -- "$pdf_file")
    basename="${filename%.*}"
    paper_dir="$EXTRACT_DIR/$basename"
    raw_md="$paper_dir/$basename.md"
    log_file="$EXTRACT_DIR/${basename}_marker_debug.log"
    
    echo "--------------------------------------------------"
    echo "Processing: $filename"
    echo "--------------------------------------------------"
    
    # Skip if already successfully processed
    if [ -f "$raw_md" ]; then
        echo ">> Already processed. Skipping to next paper."
        continue
    fi
    
    # Step 1: Extract (Marker OCR) with explicit logging
    echo ">> [1/3] Running Marker OCR... (Logging to $log_file)"
    
    if ! marker_single "$pdf_file" --output_dir "$EXTRACT_DIR" > "$log_file" 2>&1; then
        echo ">> [FATAL ERROR] Marker crashed while processing $filename!"
        echo ">> --- BEGIN DEBUG TRACEBACK ---"
        tail -n 20 "$log_file"
        echo ">> --- END DEBUG TRACEBACK ---"
        echo ">> Aborting batch process. Please inspect the PDF or the full log file."
        exit 1
    fi
    
    # Step 2: Organize Images into Subfolder
    if [ -d "$paper_dir" ]; then
        echo ">> [2/3] Isolating images into subfolder..."
        mkdir -p "$paper_dir/images"
        mv "$paper_dir"/*.jpeg "$paper_dir/images/" 2>/dev/null || true
        mv "$paper_dir"/*.png "$paper_dir/images/" 2>/dev/null || true
        
        # Step 3: Normalize LaTeX & Update Image Links
        if [ -f "$raw_md" ]; then
            echo ">> [3/3] Normalizing LaTeX & updating image links..."
            
            # Fix Markdown image relative paths
            sed -i '' 's|!\[\(.*\)\](\(_page_.*\.\(jpeg\|png\)\))|![\1](images/\2)|g' "$raw_md"
            
            # Normalize LaTeX and clean up temporary file
            python "$NORMALIZER" "$raw_md"
            mv "${raw_md%.md}_normalized.md" "$raw_md"
            
            echo ">> Success: $basename organized and normalized."
        fi
    else
        echo ">> ERROR: Expected folder $paper_dir not found. Skipping."
    fi
done

echo "=================================================="
echo " Batch Processing Complete!"
echo " All papers neatly organized in $EXTRACT_DIR."
echo "=================================================="