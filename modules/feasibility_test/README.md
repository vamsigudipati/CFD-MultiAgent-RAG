# Feasibility Test — R-Net Skeleton (Balasubramanian et al., 2023)

Pre-data scaffold that validates the PyTorch plumbing for the wall-prediction
R-Net **before** the (request-only) KTH DNS dataset is obtained. See
[`docs/lectures/06_feasibility_balasubramanian.md`](../../docs/lectures/06_feasibility_balasubramanian.md)
for the full feasibility audit.

## What this proves
- The R-Net compiles to **exactly 2,568,681 trainable parameters** (the value
  reported in the paper).
- **Circular (periodic) padding** wraps correctly in both wall-parallel directions.
- **Crop-on-concat** skip connections (upstream map cropped to the downstream
  spatial size, then concatenated on the channel axis) behave correctly.
- Forward + backward run on **synthetic float32 `192×192`** fields without NaNs.

## ⚠️ Important caveat
The paper reports the per-layer channel widths only in a schematic figure, not in
the text. The width schedule in `rnet.py` is therefore **inferred and calibrated**
so that the *aggregate* parameter count matches the paper exactly (base width 81,
with calibration layers 15 → 105 and 29 → 68). It is **not** a claim about the true
per-layer topology. Replace `WIDTHS` once the authors' schematic is transcribed.

## Files
| File | Purpose |
|---|---|
| `rnet.py` | R-Net model, circular padding, center-crop, thresholded-ReLU |
| `synthetic.py` | Reproducible synthetic float32 flow-field tensors |
| `test_rnet.py` | pytest suite (param count, padding, crop-on-concat, grad check) |
| `requirements.txt` | Minimal dependencies |

## Run

```bash
cd modules/feasibility_test
pip install -r requirements.txt
pytest -v
```

Tests are CPU-only and headless by default.
