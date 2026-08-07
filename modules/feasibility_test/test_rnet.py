"""Feasibility test suite for the R-Net skeleton.

Validates the three plumbing concerns that must hold before real DNS data arrives:
  1. exact trainable-parameter count (2,568,681),
  2. circular (periodic) padding correctness,
  3. crop-on-concat skip-connection correctness,
plus a forward/gradient smoke test on synthetic float32 fields.

All tests run headless on CPU by default.
"""
from __future__ import annotations

import torch

from rnet import (
    FIELD_SIZE,
    INPUT_PAD,
    N_HIDDEN_LAYERS,
    OUT_CHANNELS,
    TARGET_PARAMS,
    WIDTHS,
    RNet,
    build_rnet,
    center_crop,
    circular_pad,
    count_trainable_parameters,
)
from synthetic import synthetic_batch, synthetic_fields


# --- 1. Exact parameter count ---------------------------------------------------

def test_trainable_param_count_is_exact():
    model = build_rnet()
    assert count_trainable_parameters(model) == TARGET_PARAMS


def test_width_schedule_shape():
    assert len(WIDTHS) == N_HIDDEN_LAYERS
    assert WIDTHS[-1] == OUT_CHANNELS


# --- 2. Circular padding correctness -------------------------------------------

def test_circular_pad_output_shape():
    x = synthetic_fields(batch=2, size=FIELD_SIZE, seed=1)
    padded = circular_pad(x, INPUT_PAD)
    expected = FIELD_SIZE + 2 * INPUT_PAD
    assert padded.shape[-2:] == (expected, expected)


def test_circular_pad_wraps_periodically():
    # A tiny known field makes the wrap-around explicit.
    x = torch.arange(16, dtype=torch.float32).reshape(1, 1, 4, 4)
    pad = 1
    padded = circular_pad(x, pad)
    # Left padding column must equal the original last column (periodic wrap).
    assert torch.equal(padded[0, 0, 1:-1, 0], x[0, 0, :, -1])
    # Right padding column must equal the original first column.
    assert torch.equal(padded[0, 0, 1:-1, -1], x[0, 0, :, 0])
    # Top padding row must equal the original bottom row.
    assert torch.equal(padded[0, 0, 0, 1:-1], x[0, 0, -1, :])
    # Bottom padding row must equal the original top row.
    assert torch.equal(padded[0, 0, -1, 1:-1], x[0, 0, 0, :])


# --- 3. Crop-on-concat skip connections ----------------------------------------

def test_center_crop_is_centered():
    # Distinct per-pixel values so an off-center crop would be detectable.
    x = torch.arange(8 * 8, dtype=torch.float32).reshape(1, 1, 8, 8)
    cropped = center_crop(x, (4, 4))
    assert cropped.shape[-2:] == (4, 4)
    # Center 4x4 block of an 8x8 grid starts at offset (2, 2).
    assert torch.equal(cropped, x[:, :, 2:6, 2:6])


def test_crop_on_concat_channel_and_spatial_dims():
    # A skip map (larger) concatenated onto a downstream map (smaller) must be
    # cropped to the downstream spatial size and stacked along the channel dim.
    down = torch.zeros(2, 5, 10, 10)
    skip = torch.ones(2, 7, 14, 14)
    skip_cropped = center_crop(skip, down.shape[-2:])
    fused = torch.cat([down, skip_cropped], dim=1)
    assert fused.shape == (2, 5 + 7, 10, 10)


def test_skip_topology_is_symmetric():
    model = RNet()
    # Decoder layer (30 - i) must pull its skip from encoder layer i, for i in 0..14.
    assert model._skip_source == {30 - i: i for i in range(15)}
    # Middle layer 15 has no skip.
    assert 15 not in model._skip_source


# --- 4. Forward + gradient smoke test on synthetic data ------------------------

def test_forward_output_shape_and_dtype():
    model = build_rnet().eval()
    x = synthetic_fields(batch=2, seed=3)
    with torch.no_grad():
        y = model(x)
    assert y.shape == (2, OUT_CHANNELS, FIELD_SIZE, FIELD_SIZE)
    assert y.dtype == torch.float32


def test_gradients_flow_without_nan():
    torch.manual_seed(0)
    model = build_rnet().train()
    x, target = synthetic_batch(batch=2, seed=5)
    pred = model(x)
    loss = torch.nn.functional.mse_loss(pred, target)
    loss.backward()
    assert torch.isfinite(loss).item()
    grads = [p.grad for p in model.parameters() if p.grad is not None]
    assert grads, "no gradients were populated"
    assert all(torch.isfinite(g).all().item() for g in grads)


def test_output_threshold_floor_is_respected():
    # ThresholdedReLU must not emit values below the configured floor.
    model = build_rnet(output_threshold=-1.0).eval()
    x = synthetic_fields(batch=2, seed=7)
    with torch.no_grad():
        y = model(x)
    assert torch.all(y >= -1.0).item()
