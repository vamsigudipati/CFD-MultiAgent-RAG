#!/usr/bin/env python3
"""AST-based knowledge-base builder for the reference repositories.

Scans ``data/reference_repos/`` and extracts two tiers of index:

  Tier 2 (symbol chunks): the raw source of every model class and every
      physics-relevant function, stored in ``data/ast_index.sqlite``.
  Tier 1 (repo cards): a per-repo markdown summary at
      ``data/repo_cards/<repo_name>_card.md`` listing detected frameworks and
      all extracted qualnames.

The module also exposes ``fetch_symbol(repo_name, qualname)`` -- the primary
retrieval tool handed to the LangGraph framework agents.
"""
from __future__ import annotations

import argparse
import ast
import sqlite3
import sys
from pathlib import Path
from typing import Iterator

REPO_ROOT = Path(__file__).resolve().parent.parent
REPOS_DIR = REPO_ROOT / "data" / "reference_repos"
DB_PATH = REPO_ROOT / "data" / "ast_index.sqlite"
CARDS_DIR = REPO_ROOT / "data" / "repo_cards"

# Directories never worth parsing.
SKIP_DIRS = {".git", "__pycache__", ".ipynb_checkpoints", "node_modules",
             ".venv", "venv", "env", "build", "dist", ".mypy_cache", ".pytest_cache"}

# A class is a "model" if it subclasses nn.Module / keras.Model (base attr) or
# its name contains one of these fragments.
CLASS_NAME_KEYWORDS = ("net", "model")
MODEL_BASE_ATTRS = {"Module", "Model"}
# A function is "physics-relevant" if its name contains one of these. The last
# four ("model"/"net"/"build"/"architecture") capture Keras function-factory
# style models (e.g. `def cnn_model(...) -> keras.Model`), which the class-based
# rules above miss.
FUNC_NAME_KEYWORDS = ("loss", "residual", "pde", "boundary",
                      "model", "net", "build", "architecture")

FRAMEWORK_MAP = {"torch": "PyTorch", "tensorflow": "TensorFlow", "keras": "Keras"}


# --------------------------------------------------------------------------- #
# SQLite setup
# --------------------------------------------------------------------------- #
def connect_db(db_path: Path = DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS symbol_chunks (
            repo_name   TEXT NOT NULL,
            file_path   TEXT NOT NULL,
            qualname    TEXT NOT NULL,
            source_code TEXT NOT NULL,
            PRIMARY KEY (repo_name, file_path, qualname)
        )
        """
    )
    conn.commit()
    return conn


# --------------------------------------------------------------------------- #
# AST extraction
# --------------------------------------------------------------------------- #
def _base_attr_name(base: ast.expr) -> str | None:
    if isinstance(base, ast.Name):
        return base.id
    if isinstance(base, ast.Attribute):
        return base.attr
    return None


def _class_is_model(node: ast.ClassDef) -> bool:
    for base in node.bases:
        if _base_attr_name(base) in MODEL_BASE_ATTRS:
            return True
    name_lower = node.name.lower()
    return any(kw in name_lower for kw in CLASS_NAME_KEYWORDS)


def _func_is_relevant(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    name_lower = node.name.lower()
    return any(kw in name_lower for kw in FUNC_NAME_KEYWORDS)


def extract_symbols(source: str) -> list[tuple[str, str]]:
    """Return (qualname, source_code) pairs for matching classes/functions."""
    tree = ast.parse(source)
    out: list[tuple[str, str]] = []

    def walk(body: list[ast.stmt], prefix: str) -> None:
        for node in body:
            if isinstance(node, ast.ClassDef):
                qualname = prefix + node.name
                if _class_is_model(node):
                    segment = ast.get_source_segment(source, node)
                    if segment:
                        out.append((qualname, segment))
                walk(node.body, qualname + ".")
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                qualname = prefix + node.name
                if _func_is_relevant(node):
                    segment = ast.get_source_segment(source, node)
                    if segment:
                        out.append((qualname, segment))
                walk(node.body, qualname + ".")

    walk(tree.body, "")
    return out


def detect_frameworks(source: str) -> set[str]:
    """Return the set of frameworks (PyTorch/TensorFlow/Keras) imported in source."""
    frameworks: set[str] = set()
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return frameworks
    for node in ast.walk(tree):
        roots: list[str] = []
        if isinstance(node, ast.Import):
            roots = [alias.name.split(".")[0] for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots = [node.module.split(".")[0]]
        for root in roots:
            if root in FRAMEWORK_MAP:
                frameworks.add(FRAMEWORK_MAP[root])
    return frameworks


# --------------------------------------------------------------------------- #
# Repository walking / indexing
# --------------------------------------------------------------------------- #
def iter_python_files(repo_dir: Path) -> Iterator[Path]:
    for path in repo_dir.rglob("*.py"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def index_repository(conn: sqlite3.Connection, repo_dir: Path) -> dict:
    """Parse one repo, upsert its symbols, and return a summary for the card."""
    repo_name = repo_dir.name
    # Refresh: drop any prior rows for this repo so re-indexing is idempotent.
    conn.execute("DELETE FROM symbol_chunks WHERE repo_name = ?", (repo_name,))

    frameworks: set[str] = set()
    qualnames: list[str] = []

    for py_file in iter_python_files(repo_dir):
        try:
            source = py_file.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue  # skip unreadable files
        try:
            symbols = extract_symbols(source)
        except (SyntaxError, ValueError, RecursionError):
            continue  # skip unparseable files gracefully

        frameworks |= detect_frameworks(source)
        rel_path = str(py_file.relative_to(repo_dir))
        for qualname, segment in symbols:
            conn.execute(
                "INSERT OR REPLACE INTO symbol_chunks "
                "(repo_name, file_path, qualname, source_code) VALUES (?, ?, ?, ?)",
                (repo_name, rel_path, qualname, segment),
            )
            qualnames.append(f"{rel_path}::{qualname}")

    conn.commit()
    return {"repo_name": repo_name, "frameworks": sorted(frameworks), "qualnames": qualnames}


def write_repo_card(summary: dict, cards_dir: Path = CARDS_DIR) -> Path:
    cards_dir.mkdir(parents=True, exist_ok=True)
    card_path = cards_dir / f"{summary['repo_name']}_card.md"
    frameworks = ", ".join(summary["frameworks"]) or "None detected"
    lines = [
        f"# Repo Card — {summary['repo_name']}",
        "",
        f"**Frameworks detected:** {frameworks}",
        "",
        f"**Extracted symbols ({len(summary['qualnames'])}):**",
        "",
    ]
    if summary["qualnames"]:
        lines += [f"- `{qn}`" for qn in summary["qualnames"]]
    else:
        lines.append("- _(none)_")
    card_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return card_path


def build_index(repos_dir: Path = REPOS_DIR, db_path: Path = DB_PATH,
                cards_dir: Path = CARDS_DIR) -> None:
    if not repos_dir.is_dir():
        print(f"ERROR: reference repos directory not found: {repos_dir}", file=sys.stderr)
        return

    conn = connect_db(db_path)
    repo_dirs = sorted(p for p in repos_dir.iterdir() if p.is_dir())
    if not repo_dirs:
        print(f"No repositories found under {repos_dir}")
        return

    print(f"Indexing {len(repo_dirs)} repositor(y/ies) -> {db_path}")
    for repo_dir in repo_dirs:
        summary = index_repository(conn, repo_dir)
        card_path = write_repo_card(summary, cards_dir)
        print(
            f"  {summary['repo_name']}: {len(summary['qualnames'])} symbol(s), "
            f"frameworks={summary['frameworks'] or '[]'} -> {card_path.name}"
        )
    conn.close()


# --------------------------------------------------------------------------- #
# Retrieval tool for the LangGraph framework agents
# --------------------------------------------------------------------------- #
def fetch_symbol(repo_name: str, qualname: str, db_path: Path = DB_PATH) -> str:
    """Return the exact source code for a symbol from the AST index.

    Matches on ``(repo_name, qualname)``. If the same qualname exists in
    multiple files of the repo, the first match (ordered by file path) is
    returned. Raises ``LookupError`` if no match is found, so a bad request
    surfaces loudly rather than returning an empty string the agent might
    treat as valid.
    """
    conn = sqlite3.connect(db_path)
    try:
        row = conn.execute(
            "SELECT source_code FROM symbol_chunks "
            "WHERE repo_name = ? AND qualname = ? ORDER BY file_path LIMIT 1",
            (repo_name, qualname),
        ).fetchone()
    finally:
        conn.close()

    if row is None:
        raise LookupError(f"No symbol '{qualname}' found in repo '{repo_name}'")
    return row[0]


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the AST symbol index and repo cards.")
    parser.add_argument("--repos", type=Path, default=REPOS_DIR, help="Reference repos directory.")
    parser.add_argument("--db", type=Path, default=DB_PATH, help="SQLite index path.")
    parser.add_argument("--cards", type=Path, default=CARDS_DIR, help="Repo cards output directory.")
    args = parser.parse_args()
    build_index(args.repos, args.db, args.cards)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
