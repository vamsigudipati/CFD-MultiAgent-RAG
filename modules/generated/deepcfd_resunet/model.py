"""DeepCFD ResUNet -- paper-faithful surrogate for steady laminar flow.

Reproduces the architecture/loss of Ribeiro et al. (2020),
"DeepCFD: Efficient Steady-State Laminar Flow Approximation with Deep
Convolutional Neural Networks" (arXiv:2004.08826), with the residual-block
enhancement (architecture #2 from the RAG-grounded analysis).

Grounded in RAG golden symbols:
  * Identifying-regions-of-importance-...::residual_block   (Conv+BN+Add block)
  * FCN-turbulence-predictions-from-wall-quantities::cnn_model (conv field predictor)

Problem spec (from the paper):
  * Input : 3 channels  (SDF_obstacle, SDF_region, 5-class flow-region label)
  * Output: 3 channels  (U_x, U_y, p)  at full grid resolution
  * Loss  : MSE (L2) on velocity components + MAE (L1) on pressure,
            each normalized so no output dominates
  * Optim : AdamW (weight_decay = 0.005), batch 64

PyTorch only. Device/dtype are explicit; seeds set by the caller.
"""
from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F

IN_CHANNELS = 3   # SDF_obstacle, SDF_region, flow-region label
OUT_CHANNELS = 3  # U_x, U_y, p


class ResidualBlock(nn.Module):
    """Two 3x3 conv layers (BN + activation) with an additive skip.

    Mirrors the RAG `residual_block` (Conv2D -> BN -> Activation, then Add),
    with a 1x1 projection on the skip when channel counts differ.
    """

    def __init__(self, in_ch: int, out_ch: int, kernel_size: int = 3) -> None:
        super().__init__()
        pad = kernel_size // 2
        self.conv1 = nn.Conv2d(in_ch, out_ch, kernel_size, padding=pad, bias=False)
        self.bn1 = nn.BatchNorm2d(out_ch)
        self.conv2 = nn.Conv2d(out_ch, out_ch, kernel_size, padding=pad, bias=False)
        self.bn2 = nn.BatchNorm2d(out_ch)
        self.act = nn.ReLU(inplace=False)
        self.proj = (
            nn.Conv2d(in_ch, out_ch, kernel_size=1, bias=False)
            if in_ch != out_ch else nn.Identity()
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        identity = self.proj(x)
        h = self.act(self.bn1(self.conv1(x)))
        h = self.bn2(self.conv2(h))
        return self.act(h + identity)


class ResUNet(nn.Module):
    """Residual U-Net: encoder -> latent geometry rep -> decoder with skips.

    Parameters
    ----------
    in_channels, out_channels:
        3 / 3 for the DeepCFD task.
    filters:
        Encoder channel schedule; the decoder mirrors it (paper: e.g.
        [16, 32, 64] encoder -> [64, 32, 16] decoder). Down/up-sampling by 2
        per level, so H and W must be divisible by ``2 ** len(filters)``.
    kernel_size:
        Conv kernel (paper swept 3/5).
    """

    def __init__(
        self,
        in_channels: int = IN_CHANNELS,
        out_channels: int = OUT_CHANNELS,
        filters: tuple[int, ...] = (16, 32, 64),
        kernel_size: int = 5,
    ) -> None:
        super().__init__()
        self.filters = tuple(filters)
        self.depth = len(self.filters)

        # --- Encoder: residual block per level + max-pool downsample ---------
        self.enc_blocks = nn.ModuleList()
        prev = in_channels
        for f in self.filters:
            self.enc_blocks.append(ResidualBlock(prev, f, kernel_size))
            prev = f
        self.pool = nn.MaxPool2d(2)

        # --- Bottleneck (latent geometry representation) ---------------------
        bottleneck_ch = self.filters[-1] * 2
        self.bottleneck = ResidualBlock(self.filters[-1], bottleneck_ch, kernel_size)

        # --- Decoder: upsample + concat skip + residual block ----------------
        self.up_convs = nn.ModuleList()
        self.dec_blocks = nn.ModuleList()
        prev = bottleneck_ch
        for f in reversed(self.filters):
            self.up_convs.append(nn.Conv2d(prev, f, kernel_size=1, bias=False))
            # after concat with the encoder skip (also f channels) -> 2*f in
            self.dec_blocks.append(ResidualBlock(f * 2, f, kernel_size))
            prev = f

        self.head = nn.Conv2d(self.filters[0], out_channels, kernel_size=1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        divisor = 2 ** self.depth
        if x.shape[-1] % divisor or x.shape[-2] % divisor:
            raise ValueError(
                f"H and W must be divisible by {divisor}; got {tuple(x.shape[-2:])}"
            )

        skips = []
        h = x
        for block in self.enc_blocks:
            h = block(h)
            skips.append(h)
            h = self.pool(h)

        h = self.bottleneck(h)

        for up, block, skip in zip(self.up_convs, self.dec_blocks, reversed(skips)):
            h = F.interpolate(h, scale_factor=2, mode="bilinear", align_corners=False)
            h = up(h)
            h = torch.cat([h, skip], dim=1)
            h = block(h)

        return self.head(h)


def deepcfd_loss(
    pred: torch.Tensor,
    target: torch.Tensor,
    normalize: bool = True,
    eps: float = 1e-8,
) -> torch.Tensor:
    """Combined loss: MSE on (U_x, U_y) + MAE on p, per-output normalized.

    ``pred``/``target`` are ``(B, 3, H, W)`` with channel order (U_x, U_y, p).
    Per the paper: L2 for velocity (channels 0,1), L1 for pressure (channel 2),
    each normalized by the target's magnitude so no output biases the optimizer.
    """
    ux_p, uy_p, p_p = pred[:, 0], pred[:, 1], pred[:, 2]
    ux_t, uy_t, p_t = target[:, 0], target[:, 1], target[:, 2]

    l_ux = F.mse_loss(ux_p, ux_t)
    l_uy = F.mse_loss(uy_p, uy_t)
    l_p = F.l1_loss(p_p, p_t)

    if normalize:
        l_ux = l_ux / (ux_t.pow(2).mean() + eps)
        l_uy = l_uy / (uy_t.pow(2).mean() + eps)
        l_p = l_p / (p_t.abs().mean() + eps)

    return l_ux + l_uy + l_p
