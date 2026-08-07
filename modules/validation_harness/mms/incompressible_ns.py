"""Analytic 2D Taylor-Green Vortex solution for the incompressible-NS MMS gate.

This is the classical textbook analytic solution to the *unforced* 2D
incompressible Navier-Stokes equations on the periodic domain
[0, 2*pi] x [0, 2*pi] -- not fitted, not approximated. It decays
exponentially due to viscosity, so it exercises both the convective and
diffusive terms of the residual. It is hand-derived and reviewed, never
LLM-generated, per the project's zero-hallucination requirement for T2
physics targets.
"""
from typing import Tuple

import torch

from . import register_mms


@register_mms("incompressible_ns")
def taylor_green_vortex_2d(
    x: torch.Tensor,
    y: torch.Tensor,
    t: torch.Tensor,
    nu: float = 0.01,
    rho: float = 1.0,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """Evaluate the classical 2D Taylor-Green vortex at (x, y, t).

    Satisfies the 2D incompressible Navier-Stokes equations exactly for any
    nu >= 0, on the periodic domain [0, 2*pi] x [0, 2*pi]:

        u(x, y, t) =  cos(x) sin(y) F(t)
        v(x, y, t) = -sin(x) cos(y) F(t)
        p(x, y, t) = -(rho/4) (cos(2x) + cos(2y)) F(t)^2
        F(t)       = exp(-2 nu t)

    Parameters
    ----------
    x, y, t:
        Coordinate/time tensors of a common broadcastable shape.
    nu:
        Kinematic viscosity.
    rho:
        Fluid density.

    Returns
    -------
    (u, v, p): velocity components and pressure, broadcast to the common
    shape of x, y, t.
    """
    decay = torch.exp(-2.0 * nu * t)
    u = torch.cos(x) * torch.sin(y) * decay
    v = -torch.sin(x) * torch.cos(y) * decay
    p = -(rho / 4.0) * (torch.cos(2.0 * x) + torch.cos(2.0 * y)) * decay**2
    return u, v, p
