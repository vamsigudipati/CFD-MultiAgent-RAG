from abc import ABC, abstractmethod
from typing import Dict, Type, Any
from pydantic import BaseModel

class ConstraintHandler(ABC):
    """
    Abstract base class for all physics constraint handlers.
    Each handler must define its own Pydantic ParamModel for validation
    and a gate_assert method for enforcement during T2 testing.
    """
    # The Pydantic model specific to this constraint's parameters
    ParamModel: Type[BaseModel]

    @abstractmethod
    def gate_assert(self, model: Any, batch: Any, params: BaseModel) -> None:
        """
        Executes the assertion against the tensor output or model weights.
        """
        pass

# The core registry mapping string kinds to handler classes
CONSTRAINT_REGISTRY: Dict[str, Type[ConstraintHandler]] = {}

def register(kind: str):
    """Decorator to register a new constraint handler dynamically."""
    def decorator(cls: Type[ConstraintHandler]):
        CONSTRAINT_REGISTRY[kind] = cls
        return cls
    return decorator