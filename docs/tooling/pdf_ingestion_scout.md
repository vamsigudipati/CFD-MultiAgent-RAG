# PDF Ingestion Scout — Tooling Survey for CFD Paper Pipeline

> Scout report: verified against each project's live GitHub page (stars, last release,
> license, benchmark scores as of the fetch). Rankings weight **academic
> math/table/two-column fidelity → LLM integration → community adoption + active
> maintenance → Python/PyTorch ecosystem fit**, matching the pipeline goal
> (dense DL/CFD PDFs → extract → LLM "flatten").

## Objective

Build an automated pipeline that ingests the CFD papers in `CFD_Technical_Papers/`,
converts them to structured Markdown with faithful equations and tables, and exposes a
retrieval-augmented QA layer over the resulting corpus.

Target stages:

```
Extract  →  Normalize (math/tables)  →  Index/RAG  →  QA / Orchestration
```

## Ranked Candidates

| # | Repository | Primary Capability | Integration Readiness | Why it ranks here |
|---|---|---|---|---|
| 1 | [Marker](https://github.com/datalab-to/marker) | VLM-assisted PDF→Markdown/JSON; native inline-math LaTeX, table & multi-column handling | **Excellent** — `pip install marker-pdf`, pure-Python, PyTorch/MPS/CPU, `--use_llm` hybrid mode (Gemini/Claude/OpenAI/Ollama), FastAPI server, chunk output for RAG | Best-in-class on math-heavy pages (**83.9 arXiv-math**, 76.0 overall olmocr-bench); Apache-2.0 code; **v2.0.0 released 2 weeks ago** (38.5k★). Ideal drop-in for the extract→LLM step. |
| 2 | [MinerU](https://github.com/opendatalab/MinerU) | Document parsing engine → Markdown/JSON; auto LaTeX formulas + HTML tables, 109-lang OCR, reading-order | **Excellent** — `pip install mineru[all]`, CLI/FastAPI/Gradio, CPU or GPU/MPS, VLM+pipeline backends | Highest community adoption of the parsers (**77.0k★**), **v3.4.4 last month**, purpose-built "for scientific literature." Apache-2.0-based license. Strongest all-rounder for CFD/physics layouts. |
| 3 | [Docling](https://github.com/docling-project/docling) | Layout/table/formula/code parsing → unified `DoclingDocument`, Markdown/JSON/DocTags | **Excellent (best framework fit)** — MIT, native LangChain/LlamaIndex/CrewAI/Haystack integrations + MCP server; air-gapped/local execution | LF AI & Data (IBM) project, **64.3k★**, **v2.118.0 3 days ago**. Wins if wiring into an agentic/RAG framework rather than raw scripting. |
| 4 | [PaperQA2](https://github.com/Future-House/paper-qa) | Agentic **RAG + QA + summarization + contradiction detection** over scientific PDFs, with grounded in-text citations | **Very good** — `pip install paper-qa`, LiteLLM (any provider), local embeddings, **bundles Docling + Nvidia-nemotron readers**, multimodal (tables/figures/math) | This is the **"LLM-flatten/explain" layer**, not just a parser. Apache-2.0, 9.0k★, actively maintained. Pair it on top of Marker/MinerU output. |
| 5 | [olmOCR](https://github.com/allenai/olmocr) | 7B VLM OCR → clean Markdown; equations, tables, handwriting, complex multi-column | **Good (GPU-gated)** — `pip install olmocr[gpu]`, vLLM local or OpenAI-compatible remote server, Docker, S3 multi-node batch | Top raw accuracy (**82.4 olmocr-bench**, and it *ships* the benchmark). AI2/Apache-2.0. Docked to #5 only because it **requires a ≥12GB GPU** and last release was 5 months ago. |
| 6 | [RAGFlow](https://github.com/infiniflow/ragflow) | Full production **RAG engine** with DeepDoc deep-document parser, template chunking, grounded citations | **Good (heavyweight)** — Docker-compose stack (ES/MySQL/MinIO/Redis), Python/JS SDK, MCP; can use MinerU & Docling as parsers | Massive adoption (**87.0k★**, commits hourly, Apache-2.0). Choose it for a turnkey end-to-end platform rather than composing libraries; overkill for a lean script. |
| 7 | [Nougat](https://github.com/facebookresearch/nougat) | Transformer VLM specialized in **academic LaTeX math + tables** → Mathpix-Markdown (.mmd) | **Fair** — `pip install nougat-ocr`, PyTorch, CLI + API; English/Latin papers only | The original academic-math OCR model (10.1k★) and still a strong math baseline, but **last commit ~1 year ago** and CC-BY-NC weights (non-commercial) drop it to the bottom. Use as a reference/fallback, not the backbone. |

## Bottom Line

Compose **Marker or MinerU** (extraction: math/tables/two-column) → **PaperQA2**
(LLM flattening, QA, grounded explanations). Add **Docling** if you standardize on
LangChain/LlamaIndex; reach for **olmOCR** when you have GPU budget and want max
accuracy on scanned/gnarly PDFs.

## Environment Notes

- Present locally: `pdfminer.six`.
- Missing locally: `pptx`, `PyPDF2`, `pypdf`, `pdftotext`, `unoconv`.
- GPU-backed tools (olmOCR, vLLM) require ≥12GB GPU.

## Next Steps

1. Benchmark Marker vs. MinerU vs. Docling vs. olmOCR on a representative CFD PDF set
   (equation + table fidelity).
2. Wire the selected parser → PaperQA2 and add a CI smoke test.
3. Save sample conversions to `docs/samples/` for manual inspection.
