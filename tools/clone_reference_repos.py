#!/usr/bin/env python3
"""Clone reference GitHub repositories listed in the literature CSV.

Scans every cell of ``CFD_Technical_Papers_Literatur.csv`` for GitHub URLs,
normalizes them to canonical ``owner/repo`` clone URLs, and clones each into
``data/reference_repos/<repo_name>``. Existing clones are updated via
``git pull`` rather than re-cloned.
"""
from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CSV = REPO_ROOT / "CFD_Technical_Papers_Literatur.csv"
CLONE_DIR = REPO_ROOT / "data" / "reference_repos"

# Matches github.com/owner/repo (https, ssh, or bare), stopping before any
# trailing path like /tree/... /blob/... or query/fragment.
GITHUB_RE = re.compile(
    r"github\.com[/:]([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)",
    re.IGNORECASE,
)


def extract_github_repos(csv_path: Path) -> list[tuple[str, str]]:
    """Return a de-duplicated list of (repo_name, clone_url) from the CSV."""
    if not csv_path.is_file():
        raise FileNotFoundError(f"Literature CSV not found at {csv_path}")

    seen: dict[str, tuple[str, str]] = {}  # lowercased key -> (owner, repo) original case
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        for row in csv.reader(f):
            for cell in row:
                for owner, repo in GITHUB_RE.findall(cell or ""):
                    repo = repo[:-4] if repo.lower().endswith(".git") else repo
                    repo = repo.rstrip(".")  # trailing punctuation from prose
                    if not repo or repo.lower() in {"tree", "blob"}:
                        continue
                    key = f"{owner}/{repo}".lower()
                    if key not in seen:
                        seen[key] = (owner, repo)  # preserve original casing
    # repo_name is the last path segment; collisions across owners are rare but
    # disambiguated by prefixing the owner when they occur.
    result: list[tuple[str, str]] = []
    names: dict[str, int] = {}
    for owner, repo in seen.values():
        name = repo
        if repo in names:
            name = f"{owner}__{repo}"
        names[repo] = names.get(repo, 0) + 1
        result.append((name, f"https://github.com/{owner}/{repo}.git"))
    return result


def clone_or_update(repo_name: str, clone_url: str, dest_root: Path) -> str:
    """Clone the repo, or ``git pull`` if it already exists. Returns a status."""
    dest = dest_root / repo_name
    if dest.exists():
        if not (dest / ".git").exists():
            return f"SKIP  {repo_name} (exists but is not a git repo)"
        proc = subprocess.run(
            ["git", "-C", str(dest), "pull", "--ff-only"],
            capture_output=True, text=True,
        )
        if proc.returncode != 0:
            return f"WARN  {repo_name} pull failed: {proc.stderr.strip().splitlines()[-1:] or ''}"
        return f"PULL  {repo_name}"

    dest_root.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        ["git", "clone", "--depth", "1", clone_url, str(dest)],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        return f"ERROR {repo_name} clone failed: {proc.stderr.strip().splitlines()[-1:] or ''}"
    return f"CLONE {repo_name}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Clone reference GitHub repos from the literature CSV.")
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV, help="Path to the literature CSV.")
    parser.add_argument("--dest", type=Path, default=CLONE_DIR, help="Destination root for clones.")
    parser.add_argument("--dry-run", action="store_true", help="List discovered repos without cloning.")
    args = parser.parse_args()

    try:
        repos = extract_github_repos(args.csv)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    if not repos:
        print("No GitHub URLs found in the CSV.")
        return 0

    print(f"Discovered {len(repos)} unique GitHub repositor(y/ies):")
    for name, url in repos:
        print(f"  {name}  <-  {url}")

    if args.dry_run:
        return 0

    print("\nCloning / updating:")
    for name, url in repos:
        print("  " + clone_or_update(name, url, args.dest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
