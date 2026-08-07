# Module 3 — Spatial Predictions, Non-Intrusive Sensing & Super-Resolution

**Source material:** `Lecture2.txt` (final section), `Lecture3.txt` (majority), slide deck `2_Space.pptx` (slides 1–33, "Machine learning for fluid mechanics — Part 2: Spatial predictions and sensing in turbulent flows").
**Scope:** Convolutional neural networks (CNN) for non-intrusive wall-based sensing, the FCN vs. FCN-POD hybrid, transfer learning across wall-normal distance and Reynolds number, GAN-based super-resolution from coarse/sparse measurements, and CNN-based near-wall (outer→inner) prediction with residual blocks.

---

## 1. Mathematical Foundations

### 1.1 Discrete 2D convolution

For an input image/field $f(x,y)$ and a kernel $\omega(s,t)$ of size $K\times K$:

$$
g(x,y) = (\omega * f)(x,y) = \sum_{s}\sum_{t} \omega(s,t)\, f(x-s,\, y-t)
$$

**Mechanically** (as walked through live with a lettered $3\times3$ example): flip the kernel's rows and columns (180° rotation), overlay it on the input neighborhood, multiply element-wise, and sum. Three canonical example kernels illustrate the operation:

- **Identity** kernel (all zero except center = 1): output equals input exactly.
- **Box blur** (all nine entries $= 1/9$): diffuses/spreads local information — a smoothing/low-pass filter.
- **Edge detection** (center $=8$, all neighbors $=-1$, sums to 0): produces a sharp contrast response at intensity discontinuities — a high-pass filter.

**The key insight for turbulence data:** a trained CNN's kernels are *learned* generalizations of these hand-crafted filters — the network discovers which spatial filters best extract the flow features (streaks, vortices, shear layers) relevant to the prediction target.

### 1.2 Multi-channel convolution and feature maps

For an input with $C_{\text{in}}$ channels (e.g. wall pressure + 2 wall-shear-stress components), a single **filter** consists of $C_{\text{in}}$ stacked kernels — one per input channel — whose convolution outputs are summed into **one** output feature map:

$$
g(x,y) = \sum_{c=1}^{C_{\text{in}}} \omega_c * f_c \,(x,y)
$$

Applying $C_{\text{out}}$ independent filters yields $C_{\text{out}}$ feature maps, i.e. an output tensor of depth $C_{\text{out}}$. Parameter count for one convolutional layer:

$$
\#\text{params} = (K \times K \times C_{\text{in}} + 1) \times C_{\text{out}}
$$

(the $+1$ is the per-filter bias.) E.g. a $5\times5$ kernel over $C_{\text{in}}=3$ input channels has $5\times5\times3 = 75$ weights per filter.

### 1.3 Pooling and transpose convolution

- **Max pooling**: within each kernel window, keep only the maximum value — reduces spatial resolution while retaining the strongest local feature response, and *enlarges the effective receptive field* of subsequent layers (addresses the "small receptive field" problem, §3).
- **Transpose convolution** ("deconvolution"): the inverse operation — copies/redistributes values to *increase* resolution, used in the decoder/upsampling path of U-Net-style architectures.

### 1.4 Proper Orthogonal Decomposition (POD) coupling

As in Module 1, a spatiotemporal signal can be decomposed as:

$$
\mathbf{u}(\mathbf{x}, t) = \sum_{i} a_i(t)\, \boldsymbol{\phi}_i(\mathbf{x})
$$

**FCN-POD** exploits this: instead of predicting the full output field directly, the CNN predicts only the **temporal coefficients** $a_i(t)$ of a pre-computed POD basis (computed per sub-domain), and the field is reconstructed by superposition. This embeds known structure (energy ranking of POD modes) directly into the learning target.

### 1.5 Generative Adversarial Network (GAN) objective

$$
\min_{G} \max_{D} \; \mathbb{E}_{\mathbf{x}\sim p_{\text{data}}}\left[\log D(\mathbf{x})\right] + \mathbb{E}_{\mathbf{z}\sim p_z}\left[\log\left(1 - D(G(\mathbf{z}))\right)\right]
$$

- **Generator** $G$: coarse/low-resolution field $\to$ high-resolution field.
- **Discriminator** $D$: classifies whether a high-resolution field is *real* (from the dataset) or *generated* (fake, from $G$).
- Trained jointly (a minimax game): $G$ improves at producing realistic high-resolution fields, $D$ improves at telling them apart, until (ideally) $D$ can no longer distinguish real from generated.

### 1.6 Energy spectra diagnostic

A 2D pre-multiplied power spectral density $k_x k_z E(k_x, k_z)$ (streamwise wavelength $\lambda_x$ vs. spanwise wavelength $\lambda_z$) is used to diagnose **which length scales are lost** under downsampling or reconstruction — large-scale energy content is retained even under aggressive downsampling, while small-scale (high-wavenumber) content is progressively lost.

### 1.7 Relative error metric

Identical convention to Module 1 §1.6:

$$
e_q = \frac{\left\|\hat q(y) - q(y)\right\|}{\max_y |q(y)|}\times 100\%
$$

---

## 2. Architecture Topology & Hyperparameters

### 2.1 Non-intrusive wall sensing — problem setup (Guastoni et al., *J. Fluid Mech.* 928, A27, 2021)

- **DNS solver**: Fourier–Chebyshev pseudo-spectral code **SIMSON** (Chevalier et al., 2007), KTH.
- **Geometry**: turbulent open channel flow, $(L_x, L_y, L_z) = (4\pi h, h, 2\pi h)$, no-slip at $y/h=0$, symmetry (open) condition at $y/h=1$.
- **Reynolds numbers**: $Re_\tau = 180$ and $550$.
- **Inputs** (3 channels, at the wall): streamwise wall shear stress $\tau_{w,x}$, spanwise wall shear stress $\tau_{w,z}$, wall pressure $p_w$.
- **Outputs** (3 channels, at a plane above the wall): $u', v', w'$ at $y^+ = 15, 30, 50, 100$.

### 2.2 CNN architecture (fully convolutional, no dense layers)

| Layer | Kernel size | Depth (in → out) | Notes |
|---|---|---|---|
| 1 | $5\times5$ | 3 → 64 | 75 parameters/filter ($5\times5\times3$); first layers use **larger** kernels |
| 2 | $3\times3$ | 64 → 128 | |
| 3 | $3\times3$ | 128 → 256 | |
| 4 | $3\times3$ | 256 → 256 | |
| 5 | $3\times3$ | 256 → 128 | |
| 6 (output) | $3\times3$ | 128 → 3 | 3 output channels: $u', v', w'$ |

Total: **6 hidden layers**. As depth increases, kernel size shrinks ($5\times5\to3\times3$) while channel depth grows then contracts (**64 → 128 → 256 → 256 → 128 → 3**) — a classic encoder-ish depth profile even without explicit pooling in this simplest variant. **Periodic padding** is used (matches the periodic streamwise/spanwise domain), making the CNN's output deterministic and purely locally-influenced.

### 2.3 FCN vs. FCN-POD

| Variant | Predicts | Best regime |
|---|---|---|
| **FCN** (fully convolutional network) | Full output plane directly, pixel-by-pixel | **Close to the wall** ($y^+=15$): broadband, entangled scales — direct field regression wins |
| **FCN-POD** (Güemes et al., *Phys. Fluids*, 2019) | POD temporal coefficients per sub-domain, then reconstructs by superposition | **Farther from the wall** ($y^+=100$): energy concentrated in few POD modes — embedding that structure wins |
| **EPOD** (extended POD) | Linear mapping, formally equivalent to Linear Stochastic Estimation (LSE) | Baseline only — always the weakest, since it captures only linear superposition, not nonlinear scale modulation |

### 2.4 Quantitative performance (Re$_\tau=550$, from Guastoni et al. 2021)

| Method | $y^+=15$ error | $y^+=100$ error |
|---|---|---|
| FCN | **<1%** | worse (correlation between wall and far-field input/output degrades with distance) |
| FCN-POD | worse close to wall | **~26%** — best at this distance |
| EPOD (linear) | worst | worst |

### 2.5 Transfer learning — two distinct strategies

**(a) Across wall-normal distance** (Guastoni et al., *J. Phys.: Conf. Ser.*, 2020), $Re_\tau=180$:
- Freeze the **first 3 layers** (trained to predict at $y^+=15$) — these encode small-scale features common to all wall-normal distances.
- **Retrain only the last 3 layers** to predict at $y^+=50$.

| | Mean error | Fluctuation error | Training time (relative) |
|---|---|---|---|
| Fully trainable | 2.94% | 1.35% (see note below) / 28.5% | 100% |
| Transfer learning (first 3 frozen) | 3.17% | 0.5% / 30.2% | **23–25%** |

(Slide table columns are compressed in extraction; the headline, repeatedly confirmed verbally, is: **same error levels, ~4× less training time**, because only half the network needs retraining.)

**(b) Across Reynolds number** ($Re_\tau=180 \to 550$):
- Initialize the $Re_\tau=550$ network with **all weights** from the converged $Re_\tau=180$ network (not just early layers — full initialization).
- Reduce the learning rate.
- Result: **equivalent error using only 25% of the expensive high-$Re$ training data.**
- **Practical motivation** (explicitly quantified): a $Re_\tau=180$ simulation runs in a few hours on a laptop; a $Re_\tau=550$ simulation requires a supercomputer and multiple weeks. Transfer learning cuts the *expensive* data requirement to a quarter.

### 2.6 GAN-based super-resolution (Güemes et al., *Phys. Fluids* 33, 075121, 2021; Kim et al., 2021)

- **Two-stage pipeline**: (1) generator produces a **high-resolution wall field** from coarse/downsampled input; (2) that reconstructed high-resolution wall field feeds the CNN sensing model (§2.1–2.2) to predict off-wall velocity fluctuations.
- **Downsampling factors tested**: $4^2$, $8^2$, $16^2$ (i.e., resolution reduced by these squared factors).
- **Key qualitative finding**: even at $16^2$ downsampling (severely coarse input), the reconstructed streaks retain **correct size, location, and intensity** — critical for flow-control applications that target these structures, even though fine detail is lost.
- **Loss focus**: training is *not* optimized to produce the best possible super-resolved wall field in isolation — it is optimized so that the wall reconstruction is the best possible **intermediate representation for the downstream off-wall prediction**.

### 2.7 Near-wall (outer → inner) prediction with residual blocks (Balasubramanian et al., *Int. J. Heat Fluid Flow*, 2023)

- **Task**: predict closer to the wall ($y^+=50$) from data **farther** from the wall ($y^+=100$), at $Re_\tau=550$ — motivated by wall-modeling (replacing the near-wall region with a boundary condition derived from outer-region data), building on the self-similarity argument of Mizuno & Jiménez (2013).
- **This is fundamentally harder than wall→off-wall sensing**, because:
  - **Small receptive field**: standard convolutions can't "see" the large structures needed.
  - **Missing scales**: the small-scale information needed to reconstruct near-wall detail simply isn't present in the coarser far-field input.
- **Architectural fixes**:
  - **Max pooling** — enlarges the effective receptive field so large structures are captured.
  - **Residual blocks with skip connections** — combine shallow-layer (simple/small-scale) feature maps with deep-layer (complex/large-scale) feature maps by addition, improving reconstruction of both scales simultaneously.
  - **Deeper networks (same parameter count) outperform shallower/wider ones** — attributed to turbulence's own nonlinear hierarchical scale interaction being better matched by hierarchical network depth (same principle as Module 1 §2.1).
- **Result**: 19–30% error range — "decent but not perfect"; the missing small-scale spectral content is visible directly in the 2D pre-multiplied spectrum (§1.6) as an energy gap at high wavenumbers.

---

## 3. Practical Insights & Edge Cases (Prof. Ricardo's Q&A)

- **Why not just use an MLP on flow-field images?** A flattened image fed to an MLP discards spatial adjacency information — nearby pixels lose their "nearness" once flattened into a 1D vector, and the resulting dense layers require an enormous parameter count. The convolution kernel's local sliding-window structure is what lets a CNN exploit spatial correlation with far fewer parameters — directly analogous to why LSTM/Transformer beat MLP for *temporal* correlation in Module 1.
- **Kernel vs. filter terminology** (explicitly clarified after a student question): a **kernel** is a single 2D window/matrix; a **filter** is the full stack of kernels (one per input channel) that together produce one output feature map. "Filter of depth 3" = 3 stacked $5\times5$ kernels = 75 parameters.
- **Why do first layers use larger kernels ($5\times5$) and later layers smaller ($3\times3$) but greater depth?** Mirrors the hierarchical-feature argument from Module 1: early layers extract simple local features (edges, small streak fragments); later layers combine these non-linearly into progressively more complex, larger-scale patterns — deliberately paralleling turbulence's own multi-scale hierarchical structure.
- **Direction-dependence of filters** — a student asked whether sweeping a filter top-to-bottom vs. bottom-to-top changes the result. Answer: in principle it should not, since every pixel is exposed to the same filter application regardless of sweep order.
- **The repeated three-way transfer-learning clarification** (a student needed the explanation four times in Lecture3): transfer learning here means **freezing early-layer weights from Model 1 and copying them as-is into Model 2**, then training *only* the later layers of Model 2 from scratch. It is *not* just a smarter initialization for the whole network (that's technique (b) in §2.5) — for the *wall-normal-distance* transfer, the frozen layers **never update**, because the small-scale features they encode are assumed (and empirically confirmed) to be common across nearby wall-normal planes.
- **FCN vs. FCN-POD, restated simply** (asked multiple times): FCN predicts the output field directly in physical space; FCN-POD predicts POD mode coefficients (temporal information only — the spatial structure comes from the pre-computed POD basis).
- **Does CNN performance degrade with distance from the wall?** Yes, confirmed directly — correlation between wall input and off-wall output weakens with increasing $y^+$, which is *why* FCN-POD's mode-based encoding becomes competitive/better farther out (§2.3), and why the outer→inner (§2.7) direction is fundamentally harder than inner→outer.
- **Do these CNN models generalize across geometries/flow conditions?** No — explicitly stated as a **design limitation**, not a bug: "this model is designed to make spatial predictions... if you want a model that generalizes very well across cases, then a generative [diffusion-based] model will be the answer." Foundation-model-style generalization is out of scope for this module and previewed as a separate research direction (e.g. the group's own foundation-model work, referenced across lectures).
- **Structured vs. unstructured meshes**: CNNs require a structured grid (regular spacing is not mandatory — non-uniform spacing can be handled via volume-weighting — but connectivity must be regular/structured). For genuinely unstructured meshes, use a **Graph Neural Network**, which encodes mesh connectivity explicitly; conceptually similar to a CNN but generalizes the convolution to graph neighborhoods. GNNs are more expensive/harder to train, so interpolating unstructured CFD data onto a regular grid and using a CNN is often the pragmatic choice.
- **3D fields do not need to be projected to 2D** — CNNs (and the GAN/U-Net architectures in Module 4) operate natively in 3D by using 3D convolutions; an explicit student question about projecting a 3D iso-surface to 2D was answered "you can do it in 3D directly... no problem at all."
- **Lagrangian data (bubbles/particles)**: CNNs are natively an Eulerian-framework tool; Lagrangian tracking is better served by graph-based approaches (particle positions as graph nodes across snapshots) or transformer/recurrent architectures per-particle, though CNNs can still contribute if the Lagrangian information is first rasterized into an Eulerian field/mask representation.
- **GAN vs. autoencoder**: explicitly *not* opposites, but different tools. An autoencoder is generally used for compressive **modeling/reduced-order representation** (reconstruct the same input, forcing a compressed bottleneck); a GAN here is used specifically for **super-resolution** (generate physically-plausible fine detail beyond what a simple upsampling would produce), with the generator/discriminator playing adversarial (not encoder/decoder) roles.

---

## 4. Physical Diagnostic Framework

1. **Instantaneous field comparison** (streak intensity, spanwise meandering) — a strictly *qualitative* first check; a model exhibiting attenuated fluctuation intensity or under-resolved meandering has captured only the **linear superposition** mechanism, not the nonlinear **modulation** mechanism (an explicit distinction drawn between linear scale interaction — captured even by LSE — and nonlinear scale interaction, which requires a nonlinear model).
2. **Turbulence statistics vs. wall-normal distance**: $u'_{\text{rms}}(y)$, $v'_{\text{rms}}(y)$, $w'_{\text{rms}}(y)$, compared across FCN / FCN-POD / EPOD / DNS reference on a log-scaled wall-normal axis.
3. **Relative error, reported separately per method and per $y^+$ plane** (§2.4) — do not average across wall-normal distance, since the best method *changes* with distance (FCN near-wall, FCN-POD far-field).
4. **2D pre-multiplied energy spectrum** $k_x k_z E(k_x,k_z)$ (streamwise $\lambda_x$ vs. spanwise $\lambda_z$ wavelength) — required whenever claiming successful reconstruction under downsampling or outer→inner prediction, since aggregate statistics can look acceptable while high-wavenumber content is silently missing.
5. **Wall-shear-stress/wall-pressure field reconstruction fidelity** (visual + relative error) at each tested downsampling factor ($4^2$, $8^2$, $16^2$) before trusting the downstream off-wall prediction built on top of it.
6. **Transfer-learning validation**: report error **and** training-time/data-cost savings side by side (§2.5) — a transfer-learning result is only a genuine win if error parity is demonstrated at reduced cost, not just "close enough" accuracy alone.
7. **Explicit non-generalization disclosure**: state the Reynolds number / geometry the model was trained and evaluated on; per this module's own admission, these architectures are not expected to generalize outside that regime.

---

## 5. Implementation Logic

### 5.1 Non-intrusive sensing CNN (PyTorch, periodic padding)

```python
import torch
import torch.nn as nn

class WallSensingCNN(nn.Module):
    """Predicts off-wall (u', v', w') from wall (tau_wx, tau_wz, p_w).
    6 hidden layers, channel depth 64-128-256-256-128-3, periodic padding
    to match the periodic streamwise/spanwise domain.
    """
    def __init__(self):
        super().__init__()

        def conv_block(c_in, c_out, k):
            pad = k // 2
            return nn.Sequential(
                nn.Conv2d(c_in, c_out, kernel_size=k, padding=pad, padding_mode="circular"),
                nn.ReLU(inplace=True),
            )

        self.layers = nn.Sequential(
            conv_block(3, 64, k=5),
            conv_block(64, 128, k=3),
            conv_block(128, 256, k=3),
            conv_block(256, 256, k=3),
            conv_block(256, 128, k=3),
            nn.Conv2d(128, 3, kernel_size=3, padding=1, padding_mode="circular"),
        )

    def forward(self, wall_fields: torch.Tensor) -> torch.Tensor:
        # wall_fields: (batch, 3, H, W) -> (batch, 3, H, W) [u', v', w']
        return self.layers(wall_fields)
```

### 5.2 FCN-POD hybrid head

```python
class FCN_POD(nn.Module):
    """Predicts POD temporal coefficients (not the raw field) from wall data.
    The spatial reconstruction u'(x,y,z,t) = sum_i a_i(t) * phi_i(x,y,z)
    happens outside the network using a precomputed POD basis `phi`.
    """
    def __init__(self, backbone: nn.Module, n_pod_modes: int):
        super().__init__()
        self.backbone = backbone           # e.g. WallSensingCNN's conv trunk
        self.pool = nn.AdaptiveAvgPool2d(1)
        self.coeff_head = nn.Linear(128, n_pod_modes)

    def forward(self, wall_fields: torch.Tensor) -> torch.Tensor:
        feats = self.backbone(wall_fields)      # (batch, 128, H, W)
        pooled = self.pool(feats).flatten(1)     # (batch, 128)
        return self.coeff_head(pooled)           # (batch, n_pod_modes)


def reconstruct_field(coeffs: torch.Tensor, pod_basis: torch.Tensor) -> torch.Tensor:
    """coeffs: (batch, n_modes), pod_basis (phi_i): (n_modes, H, W, 3)."""
    return torch.einsum("bn,nhwc->bhwc", coeffs, pod_basis)
```

### 5.3 Transfer learning — freeze-and-retrain across wall-normal distance

```python
def build_transfer_model(pretrained_model: WallSensingCNN, freeze_first_n: int = 3):
    """Freezes the first `freeze_first_n` conv blocks (trained at y+=15)
    and leaves the rest trainable (to be retrained at y+=50)."""
    new_model = WallSensingCNN()
    new_model.load_state_dict(pretrained_model.state_dict())  # start identical

    for i, block in enumerate(new_model.layers):
        if i < freeze_first_n:
            for p in block.parameters():
                p.requires_grad = False   # frozen: never updated by the optimizer

    trainable_params = [p for p in new_model.parameters() if p.requires_grad]
    optimizer = torch.optim.Adam(trainable_params, lr=1e-4)
    return new_model, optimizer
```

### 5.4 Minimal GAN skeleton for wall super-resolution

```python
class Generator(nn.Module):
    def __init__(self, upsample_factor: int):
        super().__init__()
        self.body = nn.Sequential(
            nn.Conv2d(3, 64, 9, padding=4), nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, 3, padding=1), nn.ReLU(inplace=True),
        )
        self.upsample = nn.Sequential(
            nn.Upsample(scale_factor=upsample_factor, mode="bicubic", align_corners=False),
            nn.Conv2d(64, 3, 9, padding=4),
        )

    def forward(self, coarse_wall_fields):
        return self.upsample(self.body(coarse_wall_fields))


class Discriminator(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(3, 64, 3, stride=2, padding=1), nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(64, 128, 3, stride=2, padding=1), nn.LeakyReLU(0.2, inplace=True),
            nn.AdaptiveAvgPool2d(1), nn.Flatten(),
            nn.Linear(128, 1),  # logit: real (high-res DNS) vs. fake (generated)
        )

    def forward(self, field):
        return self.net(field)


def gan_training_step(generator, discriminator, opt_g, opt_d,
                       coarse_field, real_hires_field, bce_loss):
    # --- Discriminator step ---
    opt_d.zero_grad()
    fake_hires = generator(coarse_field).detach()
    real_logits = discriminator(real_hires_field)
    fake_logits = discriminator(fake_hires)
    d_loss = bce_loss(real_logits, torch.ones_like(real_logits)) + \
             bce_loss(fake_logits, torch.zeros_like(fake_logits))
    d_loss.backward()
    opt_d.step()

    # --- Generator step ---
    opt_g.zero_grad()
    fake_hires = generator(coarse_field)
    fake_logits = discriminator(fake_hires)
    g_loss = bce_loss(fake_logits, torch.ones_like(fake_logits))  # fool the discriminator
    g_loss.backward()
    opt_g.step()

    return {"d_loss": d_loss.item(), "g_loss": g_loss.item()}
```

### 5.5 Physics-validation gate for this module

Per `docs/copilot/physics_validation_rules.md` and `docs/copilot/mlops_scaling_rules.md`:

```python
def validate_spatial_prediction(pred_field, ref_field, ref_spectrum_fn, tol_stat=0.15):
    """Checks both statistical-profile error AND spectral content, since
    aggregate stats alone can hide missing small-scale (high-wavenumber) energy."""
    rel_err = (pred_field - ref_field).norm() / ref_field.abs().max()
    assert rel_err < tol_stat, f"Relative error {rel_err:.2%} exceeds {tol_stat:.0%}"

    pred_spectrum = ref_spectrum_fn(pred_field)
    ref_spectrum = ref_spectrum_fn(ref_field)
    # Flag (not necessarily fail) high-wavenumber energy deficit for manual review:
    high_k_deficit = 1.0 - (pred_spectrum[-10:].sum() / ref_spectrum[-10:].sum())
    return {"relative_error": rel_err.item(), "high_wavenumber_deficit": high_k_deficit.item()}
```
