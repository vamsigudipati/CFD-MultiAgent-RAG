"""Synthetic float32 flow-field tensors standing in for the (blocked) DNS data.

These are placeholders so the architecture plumbing can be validated before the
real KTH open-channel dataset is obtained. They are NOT physically meaningful.
"""
from __future__ import annotations

import torch

from rnet import IN_CHANNELS, OUT_CHANNELS, FIELD_SIZE


def synthetic_fields(
    batch: int = 4,
    channels: int = IN_CHANNELS,
    size: int = FIELD_SIZE,
    seed: int = 0,
    device: torch.device | str = "cpu",
) -> torch.Tensor:
    """Return a reproducible ``(batch, channels, size, size)`` float32 tensor.

    Values are unit-Gaussian to loosely mimic RMS-normalized velocity fluctuations
    (which are signed and O(1)).
    """
    gen = torch.Generator(device="cpu").manual_seed(seed)
    x = torch.randn(batch, channels, size, size, generator=gen, dtype=torch.float32)
    return x.to(device)


def synthetic_batch(
    batch: int = 4,
    seed: int = 0,
    device: torch.device | str = "cpu",
) -> tuple[torch.Tensor, torch.Tensor]:
    """Return an ``(input, target)`` pair for a quick gradient-flow check."""
    x = synthetic_fields(batch, IN_CHANNELS, FIELD_SIZE, seed=seed, device=device)
    y = synthetic_fields(batch, OUT_CHANNELS, FIELD_SIZE, seed=seed + 1, device=device)
    return x, y
