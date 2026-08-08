import sys
from pathlib import Path

# Add project root directory to sys.path so 'modules' can be imported cleanly
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import os
import time
import csv
import concurrent.futures
from modules.orchestrator.graph import app

PDF_DIR = "pdf_repository"
RESULTS_CSV = "batch_execution_results.csv"
TIMEOUT_SECONDS = 600  # 10 minutes max per paper execution


def get_paper_ids():
    """Extract paper IDs from the PDF filenames."""
    if not os.path.exists(PDF_DIR):
        print(f"❌ Error: Directory '{PDF_DIR}' not found.")
        return []
    return [f.replace('.pdf', '') for f in os.listdir(PDF_DIR) if f.endswith('.pdf')]


def process_paper(paper_id):
    """Encapsulated execution for a single paper with verbose streaming."""
    thread_id = f"batch-run-{paper_id}-{int(time.time())}"
    config = {"configurable": {"thread_id": thread_id}}
    initial_state = {
        "paper_id": paper_id,
        "failure_count": 0,
        "status": "PROCESSING",
    }

    final_node_state = initial_state

    # Stream events for verbose logging instead of a silent invoke
    for event in app.stream(initial_state, config=config):
        for node_name, node_state in event.items():
            status = node_state.get('status', 'N/A')
            failures = node_state.get('failure_count', 0)

            log_line = f"    ↳ Node: {node_name} | Status: {status}"
            if failures > 0:
                log_line += f" | Attempts: {failures}"

            print(log_line)
            final_node_state = node_state  # Keep updating to return the final state

    return final_node_state


def execute_batch(papers, is_retry=False):
    """Executes a list of papers and writes results incrementally to the CSV."""
    results = []
    failed_queue = []
    total_papers = len(papers)

    pass_label = "RETRY PASS" if is_retry else "MAIN PASS"

    # Use max_workers=1 to process sequentially while still supporting timeouts
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        for index, paper_id in enumerate(papers, 1):
            print(f"\n[{pass_label} {index}/{total_papers}] Processing: {paper_id}")
            start_time = time.time()

            future = executor.submit(process_paper, paper_id)

            try:
                # Wait for execution with a hard timeout
                final_state = future.result(timeout=TIMEOUT_SECONDS)
                elapsed = time.time() - start_time
                status = final_state.get('status', 'UNKNOWN')
                fingerprint = final_state.get('error_fingerprint', 'None')

                print(f"  ↳ Status: {status} (Elapsed: {elapsed:.1f}s)")

                result_row = {
                    "Paper ID": paper_id,
                    "Pass": pass_label,
                    "Status": status,
                    "Time (s)": round(elapsed, 1),
                    "Error Fingerprint": fingerprint
                }

                if status == "CRASH" and not is_retry:
                    failed_queue.append(paper_id)

            except concurrent.futures.TimeoutError:
                elapsed = time.time() - start_time
                print(f"  ⏳ TIMEOUT: Paper exceeded {TIMEOUT_SECONDS}s limit. Moving on.")
                result_row = {
                    "Paper ID": paper_id,
                    "Pass": pass_label,
                    "Status": "TIMEOUT",
                    "Time (s)": round(elapsed, 1),
                    "Error Fingerprint": "Exceeded maximum execution time"
                }
                if not is_retry:
                    failed_queue.append(paper_id)

            except Exception as e:
                elapsed = time.time() - start_time
                print(f"  ❌ CRITICAL FAILURE: {str(e)}")
                result_row = {
                    "Paper ID": paper_id,
                    "Pass": pass_label,
                    "Status": "CRASH",
                    "Time (s)": round(elapsed, 1),
                    "Error Fingerprint": str(e)
                }
                if not is_retry:
                    failed_queue.append(paper_id)

            # Append immediately to CSV so data is not lost on crash
            with open(RESULTS_CSV, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["Paper ID", "Pass", "Status", "Time (s)", "Error Fingerprint"])
                writer.writerow(result_row)

            results.append(result_row)
            time.sleep(2)  # Brief pause between runs

    return results, failed_queue


def main():
    papers = get_paper_ids()
    if not papers:
        return

    print(f"🚀 Initiating Batch Execution for {len(papers)} papers...")
    print("=" * 60)

    # Initialize the CSV file with headers before starting
    with open(RESULTS_CSV, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Paper ID", "Pass", "Status", "Time (s)", "Error Fingerprint"])
        writer.writeheader()

    # 1. Main Pass
    _, failed_queue = execute_batch(papers, is_retry=False)

    # 2. Retry Pass (1 repetition for failures)
    if failed_queue:
        print("\n" + "=" * 60)
        print(f"🔁 Initiating Retry Pass for {len(failed_queue)} failed papers...")
        print("=" * 60)
        execute_batch(failed_queue, is_retry=True)

    print("\n" + "=" * 60)
    print(f"🏁 Batch complete! Results saved to {RESULTS_CSV}")


if __name__ == "__main__":
    main()
