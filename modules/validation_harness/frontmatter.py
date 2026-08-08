from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

class NormalizationSpec(BaseModel):
    spatial_scale: str = "auto"
    velocity_scale: str = "auto"
    pressure_scale: str = "auto"
    expected_input_rms: float = 1.0

class ArchConstraint(BaseModel):
    kind: str
    params: Dict[str, Any]
    gate_assertion: Optional[str] = None

class BlueprintFrontmatter(BaseModel):
    provenance: Dict[str, str] = Field(default_factory=dict)
    closure_status: str
    pde_family: str
    normalization: NormalizationSpec = Field(default_factory=NormalizationSpec)
    constraints: List[ArchConstraint] = Field(default_factory=list)
    traceability_matrix: Dict[str, Any] = Field(default_factory=dict)
    activation_functions: Optional[Any] = None
    layer_depths: Optional[Any] = None

    @classmethod
    def from_yaml(cls, yaml_dict: dict) -> "BlueprintFrontmatter":
        """Loads and strictly validates the parsed YAML dictionary."""
        return cls(**yaml_dict)