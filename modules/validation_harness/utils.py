"""Execution utilities for loading the LLM-generated monolith under test.

The generated code lives outside the validation_harness package (it is the
one LLM-mutable artifact in the pipeline -- see modules/workspace/<paper_id>/
train_and_val.py) and is loaded dynamically so the harness never hard-imports
paper-specific code.
"""
import importlib.util
import os
import sys
from pathlib import Path
from typing import NamedTuple, Type

import torch.nn as nn

MONOLITH_FILENAME = "train_and_val.py"
MODULE_NAME = "generated_train_and_val"


class GeneratedMonolith(NamedTuple):
    Model: Type[nn.Module]


def _import_monolith_module():
    """Dynamically import ``train_and_val.py`` from ``$WORKSPACE_DIR`` and return the module.

    Raises a clear, harness-level error (never a silent skip) if the
    environment is misconfigured, so a missing workspace never gets
    misclassified as a physics gate failure downstream.
    """
    workspace_dir = os.environ.get("WORKSPACE_DIR")
    if not workspace_dir:
        raise RuntimeError(
            "WORKSPACE_DIR environment variable is not set. Point it at the "
            "paper-specific workspace directory containing "
            f"{MONOLITH_FILENAME} (e.g. modules/workspace/<paper_id>)."
        )

    monolith_path = Path(workspace_dir) / MONOLITH_FILENAME
    if not monolith_path.is_file():
        raise FileNotFoundError(f"No {MONOLITH_FILENAME} found at {monolith_path}")

    spec = importlib.util.spec_from_file_location(MODULE_NAME, monolith_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not create an import spec for {monolith_path}")

    module = importlib.util.module_from_spec(spec)
    # Register under sys.modules before exec so the module's own relative
    # imports / dataclasses / pickling resolve correctly.
    sys.modules[MODULE_NAME] = module
    spec.loader.exec_module(module)
    return module


def load_generated_monolith() -> GeneratedMonolith:
    """Load the generated monolith and return its ``Model`` class."""
    module = _import_monolith_module()

    if not hasattr(module, "Model"):
        raise AttributeError(f"{MONOLITH_FILENAME} does not define a `Model` class")

    return GeneratedMonolith(Model=module.Model)


def get_monolith_symbol(name: str, required: bool = True):
    """Fetch a top-level symbol (function/class) from the generated monolith.

    Returns the attribute if present. If ``required`` and the symbol is missing,
    raises ``AttributeError`` so the failure is classified as a code (SYNTAX)
    defect and routed to the framework agent -- not silently skipped. If not
    ``required``, returns ``None`` when absent.
    """
    module = _import_monolith_module()
    if hasattr(module, name):
        return getattr(module, name)
    if required:
        raise AttributeError(f"{MONOLITH_FILENAME} does not define `{name}`")
    return None

