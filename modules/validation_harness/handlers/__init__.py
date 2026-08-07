"""Import every handler module so its @register decorator fires exactly once.

Adding a new constraint kind means dropping a new module here -- no other
framework code needs to change (open/closed registry pattern).
"""
from . import input_rms, output_floor  # noqa: F401
