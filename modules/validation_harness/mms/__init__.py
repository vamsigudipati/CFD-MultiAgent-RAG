"""Registry for analytic Method-of-Manufactured-Solutions (MMS) targets.

Mirrors the constraint-handler pattern in ``registry.py``: a plain dict keyed
by string, populated via a decorator. MMS entries are pure, hand-derived
analytic formulas (never LLM-generated -- see project design notes), so a
lightweight function registry is used rather than a stateful handler class.

Adding a new PDE family means dropping a new module in this package and
registering it -- no other framework code changes (open/closed).
"""
from typing import Callable, Dict

MMS_REGISTRY: Dict[str, Callable] = {}


def register_mms(pde_family: str):
    """Decorator to register an analytic MMS solution for a given PDE family."""
    def decorator(fn: Callable) -> Callable:
        MMS_REGISTRY[pde_family] = fn
        return fn
    return decorator


# Import every MMS module so its @register_mms decorator fires exactly once.
from . import incompressible_ns  # noqa: E402, F401
