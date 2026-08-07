"""Tests for the DeepCFD ResUNet surrogate.

Validates I/O contract, loss behavior, gradient health, and single-batch
overfit — the same categories as the T0-T3 validation harness, adapted to the
DeepCFD 3-in/3-out image-to-image spec. CPU-only, headless.
"""
import torch

from .model import (
    IN_CHANNELS,
    OUT_CHANNELS,
    ResUNet,
    ResidualBlock,
    deepcfd_loss,
)

FILTERS = (16, 32, 64)
H = W = 64  # divisible by 2 ** len(FILTERS) = 8


def _dummy(batch=2, seed=0):
    g = torch.Generator().manual_seed(seed)
    x = torch.randn(batch, IN_CHANNELS, H, W, generator=g, dtype=torch.float32)
    y = torch.randn(batch, OUT_CHANNELS, H, W, generator=g, dtype=torch.float32)
    return x, y


def test_output_shape_and_dtype():
    model = ResUNet(filters=FILTERS).eval()
    x, _ = _dummy()
    with torch.no_grad():
        out = model(x)
    assert out.shape == (2, OUT_CHANNELS, H, W)
    assert out.dtype == torch.float32


def test_residual_block_channel_projection():
    # in_ch != out_ch must still add cleanly via the 1x1 projection.
    block = ResidualBlock(3, 16)
    out = block(torch.randn(2, 3, 8, 8))
    assert out.shape == (2, 16, 8, 8)


def test_rejects_indivisible_resolution():
    model = ResUNet(filters=FILTERS)
    try:
        model(torch.randn(1, IN_CHANNELS, 30, 30))  # 30 not divisible by 8
    except ValueError:
        return
    raise AssertionError("expected ValueError for indivisible spatial dims")


def test_loss_is_finite_and_zero_at_perfect_fit():
    _, y = _dummy()
    assert deepcfd_loss(y, y).item() < 1e-6           # exact match -> ~0
    assert torch.isfinite(deepcfd_loss(y + 0.5, y))    # off-target -> finite


def test_loss_uses_l1_for_pressure_l2_for_velocity():
    # A pure pressure (channel 2) error should scale linearly (L1),
    # while a velocity error scales quadratically (L2).
    y = torch.zeros(1, 3, 8, 8)
    p_err = torch.zeros_like(y); p_err[:, 2] = 2.0
    v_err = torch.zeros_like(y); v_err[:, 0] = 2.0
    # unnormalized to compare raw norm behavior
    l_p = deepcfd_loss(p_err, y, normalize=False).item()   # L1(2) = 2
    l_v = deepcfd_loss(v_err, y, normalize=False).item()   # L2(2) = 4
    assert abs(l_p - 2.0) < 1e-5
    assert abs(l_v - 4.0) < 1e-5


def test_gradients_flow_without_nan():
    torch.manual_seed(0)
    model = ResUNet(filters=FILTERS).train()
    x, y = _dummy(seed=5)
    loss = deepcfd_loss(model(x), y)
    loss.backward()
    assert torch.isfinite(loss).item()
    grads = [p.grad for p in model.parameters() if p.grad is not None]
    assert grads and all(torch.isfinite(g).all().item() for g in grads)


def test_single_batch_overfit():
    # High-capacity model must drive a small structured batch's loss down sharply.
    torch.manual_seed(0)
    model = ResUNet(filters=FILTERS).train()
    x = torch.randn(1, IN_CHANNELS, H, W)
    # structured target: smooth function of the input (not pure noise)
    y = torch.tanh(x[:, :OUT_CHANNELS] * 1.5)
    opt = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=0.005)
    init = deepcfd_loss(model(x), y).item()
    for _ in range(100):
        opt.zero_grad()
        loss = deepcfd_loss(model(x), y)
        loss.backward()
        opt.step()
    assert loss.item() < 0.25 * init  # clear downward trend
