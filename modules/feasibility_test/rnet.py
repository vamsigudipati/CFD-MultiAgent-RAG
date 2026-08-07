"""PyTorch R-Net skeleton for the Balasubramanian et al. (2023) wall-prediction task.

This is a FEASIBILITY SCAFFOLD, not the published network. The paper reports the
R-Net topology only in a schematic figure (Figure 1); the exact per-layer channel
widths are NOT given in the text. The width schedule below is therefore *inferred*
and calibrated so that the aggregate trainable-parameter count matches the value
reported in the paper EXACTLY:

    Reported R-Net trainable parameters = 2,568,681

The pieces that ARE faithfully reproduced from the paper's description:
  * 31 hidden convolutional layers, all 3x3 kernels, VALID (no) padding.
  * Periodic (circular) padding of 32 points per side applied once at the input.
  * Residual skip connections between hidden layer ``i`` and layer ``N-1-i``,
    implemented as center-crop-on-concat (upstream maps are larger -> cropped).
  * BatchNorm after every conv except the last.
  * ReLU on hidden layers; a thresholded ("modified") ReLU before the output
    (threshold -1 for velocity fields, -25 for wall quantities).
  * Output is center-cropped back to the DNS field size.

Framework: PyTorch only (no TensorFlow ops in this file).
"""
from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F

# --- Fixed problem constants (from the blueprint) -------------------------------
IN_CHANNELS = 3          # (u, v, w) velocity-fluctuation planes
OUT_CHANNELS = 3         # velocity components OR (tau_x, tau_z, p) wall quantities
N_HIDDEN_LAYERS = 31
KERNEL_SIZE = 3
INPUT_PAD = 32           # circular padding per side (64 total)
FIELD_SIZE = 192         # DNS field size at Re_tau = 180
TARGET_PARAMS = 2_568_681

# --- Inferred + calibrated per-layer output-channel schedule --------------------
# Base width 81, with two calibration layers (index 15 -> 105, index 29 -> 68)
# chosen solely to pin the total parameter count to TARGET_PARAMS. Layer 30 emits
# OUT_CHANNELS. See module docstring for the important caveat.
WIDTHS = [81] * 30 + [OUT_CHANNELS]
WIDTHS[15] = 105
WIDTHS[29] = 68


def circular_pad(x: torch.Tensor, pad: int = INPUT_PAD) -> torch.Tensor:
    """Periodic padding in both wall-parallel directions (last two dims)."""
    return F.pad(x, (pad, pad, pad, pad), mode="circular")


def center_crop(x: torch.Tensor, size_hw: tuple[int, int]) -> torch.Tensor:
    """Center-crop the last two dims of ``x`` to ``(H, W) = size_hw``."""
    _, _, h, w = x.shape
    th, tw = size_hw
    if th > h or tw > w:
        raise ValueError(f"crop target {size_hw} larger than input {(h, w)}")
    top = (h - th) // 2
    left = (w - tw) // 2
    return x[:, :, top:top + th, left:left + tw]


class ThresholdedReLU(nn.Module):
    """Modified ReLU that clamps at ``threshold`` instead of 0.

    Normalized fluctuation quantities are signed, so the output activation must
    admit negative values down to the reported floor (-1 for velocity, -25 for
    wall quantities).
    """

    def __init__(self, threshold: float = -1.0) -> None:
        super().__init__()
        self.threshold = float(threshold)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return torch.clamp(x, min=self.threshold)


class RNet(nn.Module):
    """Fully-convolutional residual network (no up-sampling) with crop-on-concat skips.

    Parameters
    ----------
    in_channels, out_channels:
        Input/output channel counts (default 3 / 3).
    widths:
        Per-layer output-channel schedule of length ``N_HIDDEN_LAYERS``; the last
        entry must equal ``out_channels``.
    output_threshold:
        Floor for the modified-ReLU output activation (-1 velocity, -25 wall).
    """

    def __init__(
        self,
        in_channels: int = IN_CHANNELS,
        out_channels: int = OUT_CHANNELS,
        widths: list[int] | None = None,
        output_threshold: float = -1.0,
        input_pad: int = INPUT_PAD,
        field_size: int = FIELD_SIZE,
    ) -> None:
        super().__init__()
        widths = list(widths) if widths is not None else list(WIDTHS)
        if len(widths) != N_HIDDEN_LAYERS:
            raise ValueError(f"expected {N_HIDDEN_LAYERS} widths, got {len(widths)}")
        if widths[-1] != out_channels:
            raise ValueError("last width must equal out_channels")

        self.widths = widths
        self.input_pad = input_pad
        self.field_size = field_size
        # encoder layers 0..14 provide skips into decoder layers 30..16 (i <-> N-1-i)
        self._skip_source = {30 - i: i for i in range(15)}  # decoder_idx -> encoder_idx

        self.convs = nn.ModuleList()
        self.norms = nn.ModuleList()
        prev = in_channels
        for k in range(N_HIDDEN_LAYERS):
            in_ch = prev
            if k in self._skip_source:                 # decoder layer receives a skip
                in_ch = prev + widths[self._skip_source[k]]
            self.convs.append(
                nn.Conv2d(in_ch, widths[k], KERNEL_SIZE, stride=1, padding=0, bias=True)
            )
            # BatchNorm after every conv except the last
            self.norms.append(nn.BatchNorm2d(widths[k]) if k < N_HIDDEN_LAYERS - 1 else None)
            prev = widths[k]

        self.act = nn.ReLU(inplace=False)
        self.out_act = ThresholdedReLU(output_threshold)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if x.shape[-2:] != (self.field_size, self.field_size):
            raise ValueError(
                f"expected input HxW = {(self.field_size, self.field_size)}, got {tuple(x.shape[-2:])}"
            )
        h = circular_pad(x, self.input_pad)
        encoder_feats: dict[int, torch.Tensor] = {}

        for k in range(N_HIDDEN_LAYERS):
            if k in self._skip_source:                        # crop-on-concat skip
                skip = encoder_feats[self._skip_source[k]]
                skip = center_crop(skip, h.shape[-2:])
                h = torch.cat([h, skip], dim=1)
            h = self.convs[k](h)
            if k < N_HIDDEN_LAYERS - 1:
                h = self.norms[k](h)
                h = self.act(h)
                if k < 15:                                    # store encoder outputs
                    encoder_feats[k] = h
            else:
                h = self.out_act(h)

        return center_crop(h, (self.field_size, self.field_size))


def count_trainable_parameters(model: nn.Module) -> int:
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def build_rnet(output_threshold: float = -1.0) -> RNet:
    """Convenience builder for the calibrated 2,568,681-parameter R-Net."""
    return RNet(output_threshold=output_threshold)
