## 1. Physical Problem Statement

- **Flow Regime & Configuration:** Incompressible spatially-developing turbulent boundary layer (TBL) over a flat plate with an elliptical leading edge.
- **Governing Physics & Parameters:**
  - Momentum thickness-based Reynolds number range: $Re_\theta = \frac{U_\infty \theta}{\nu} \in [661.5, 1502.0]$ (fully turbulent regime).
  - Reference scaling: Elliptical plate half-thickness $L$, free-stream velocity $U_\infty$. Viscous inner scales denoted by superscript $+$.
- **Database & Spatial Discretization:**
  - Dataset source: Johns Hopkins Turbulence Databases (JHTDB) Transitional Boundary Layer DNS (Lee & Zaki, 2018).
  - Full DNS Domain: $L_x \times L_y \times L_z = 1050L \times 40L \times 240L$ with grid points $N_x \times N_y \times N_z = 3320 \times 224 \times 2048$.
  - Extracted $(y-z)$ Cross-Sections: Reduced spatial resolution $N_y \times N_z = 112 \times 1024$. Each plane is partitioned into four identical spanwise sub-domains of size $N_y \times N_z = 112 \times 256$.
  - Low-Resolution (Coarse) Representation: Downsampled to $N_y \times N_z = 14 \times 32$ (and tested down to $7 \times 16$) using non-uniform, wall-normal grid stretching to concentrate points near $y^+ = 0$.
  - Temporal Sampling: $\Delta t = 0.25 L/U_\infty$. Sequence size $n = 12$ previous snapshots at times $[t_0, \dots, t_n]$ used to predict step $t_{n+1}$. Total dataset contains $4000$ snapshots per sub-domain section across 3 primary training planes ($4000 \times 4 \times 3 = 48,000$ training snapshots).
- **Downstream Application (Inflow-Outflow LES):**
  - Code: OpenFOAM-5.0x (Finite Volume Method, 2nd-order spatial discretization, PISO algorithm).
  - Domain size: $L_x \times L_y \times L_z = 20\delta_0 \times 1.8\delta_0 \times 4\delta_0$, where $\delta_0$ is boundary layer thickness at the inlet.
  - Subgrid-Scale (SGS) Model: Dynamic Smagorinsky model.
  - Grid: $320 \times 90 \times 150$ ($\Delta x^+ \approx 15.4, \Delta y^+_{\text{wall}} \approx 0.2, \Delta z^+ \approx 6.5$).
  - Boundary Conditions: No-slip at wall ($y=0$), slip at top ($y=L_y$), periodic in spanwise ($z$), advective outflow at $x=L_x$, synthetic ML predicted inflow at $x=0$.

---

## 2. Network Architectures

The model pipeline couples a temporal Transformer module operating on coarse spatial representations with a spatial Multi-Scale Enhanced Super-Resolution Generative Adversarial Network (MS-ESRGAN). Total trainable parameters: $356.5 \times 10^6$.

```
Coarse Velocity Sequence [12, 14, 32, 3] 
       │
       ▼
┌──────────────────────────────┐
│     Transformer Module       │ ──> Predicts Coarse Field [1, 14, 32, 3] at t_{n+1}
└──────────────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│   MS-ESRGAN Generator (G)    │ ──> Reconstructs HR Field [1, 112, 256, 3] at t_{n+1}
└──────────────────────────────┘
```

### 2.1 Transformer Module (305.5M Parameters)
- **Purpose:** Temporal forecasting of coarse $N_y \times N_z = 14 \times 32$ velocity fields across three components $(u', v', w')$.
- **Positional Encoding:** Trigonometric (sine and cosine) position embedding added to inputs.
- **Encoder:** 6 stacked identical encoder layers.
  - Sublayer 1: Multi-Head Self-Attention ($h = 6$ heads).
    $$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$
    $$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, \dots, \text{head}_h)W^O \quad \text{where} \quad \text{head}_i = \text{Attention}\left(Q W_i^Q, K W_i^K, V W_i^V\right)$$
    Projection dimensions: $d_{\text{model}} = h \cdot d_v$, with $d_k = d_v = d_{\text{model}}/h$.
  - Residual connection and Layer Normalization applied after attention.
  - Sublayer 2: Position-wise Feed-Forward Network consisting of 2 dense layers (ReLU activation on hidden layer, linear output).
- **Decoder:** 6 stacked identical decoder layers.
  - Sublayer 1: Masked Multi-Head Self-Attention ($h = 6$ heads) to prevent look-ahead leakage.
  - Sublayer 2: Multi-Head Cross-Attention over Encoder outputs.
  - Sublayer 3: Dense Feed-Forward Network.
- **Regularization:** Dropout rate $p = 0.1$ applied to all sublayer outputs prior to residual addition.
- **Optimization:** Adam optimizer, mini-batch size $M = 64$.
- **Loss Function:**
  $$\mathcal{L}_{\text{transformer}} = \frac{1}{M} \sum_{m=1}^M \left\| \text{Output}_m - \text{Target}_m \right\|_2^2$$

### 2.2 MS-ESRGAN Module (51M Parameters)
- **Generator ($G$):**
  - Input: Low-resolution predicted velocity snapshot ($14 \times 32 \times 3$).
  - Initial Convolutional Layer $\rightarrow$ Residual-in-Residual Dense Blocks (RRDBs) with residual scaling factor $\beta_{\text{RRDB}} = 0.2$.
  - Multi-Scale Part (MSP): 3 parallel convolutional sub-models with varying kernel filter sizes ($3\times3$, $5\times5$, $7\times7$) operating on RRDB feature maps. Outputs are element-wise summed.
  - Up-sampling / Final Conv Layer: Reconstructs high-resolution output ($112 \times 256 \times 3$).
- **Discriminator ($D$):**
  - Architecture: Sequence of Convolutional layers, Batch Normalization, and Leaky ReLU activations, terminating in a dense classification layer.
  - Formulated as a Relativistic Average Discriminator ($D_{Ra}$):
    $$D_{Ra}(x_r, x_a) = \sigma\left(C(x_r) - \mathbb{E}_{x_a}[C(x_a)]\right)$$
    $$D_{Ra}(x_a, x_r) = \sigma\left(C(x_a) - \mathbb{E}_{x_r}[C(x_r)]\right)$$
    where $\sigma$ is the sigmoid function, $x_r$ is real DNS data, $x_a = G(\xi)$ is generated high-resolution data, and $C(\cdot)$ is non-transformed discriminator output.
- **Discriminator Loss Function:**
  $$\mathcal{L}_D = -\mathbb{E}_{x_r} \left[\log\left(D_{Ra}(x_r, x_a)\right)\right] - \mathbb{E}_{x_a} \left[\log\left(1 - D_{Ra}(x_a, x_r)\right)\right]$$
- **Generator Total Loss Function:**
  $$\mathcal{L}_G = \ell_G^{Ra} + \beta \ell_{\text{pixel}} + \ell_{\text{perceptual}}$$
  $$\ell_G^{Ra} = -\mathbb{E}_{x_r} \left[\log\left(1 - D_{Ra}(x_r, x_a)\right)\right] - \mathbb{E}_{x_a} \left[\log\left(D_{Ra}(x_a, x_r)\right)\right]$$
  $$\ell_{\text{pixel}} = \frac{1}{M} \sum_{m=1}^M \left\| x_{r, m} - x_{a, m} \right\|_2^2$$
  $$\ell_{\text{perceptual}} = \frac{1}{M} \sum_{m=1}^M \left\| \phi_{\text{VGG}}(x_{r, m}) - \phi_{\text{VGG}}(x_{a, m}) \right\|_2^2$$
  where $\phi_{\text{VGG}}$ extracts internal feature maps from 3 distinct layers of a pre-trained VGG-19 network, and pixel loss weighting parameter $\beta = 5000$. Mini-batch size $= 32$.

---

## 3. Data Scaling & Normalization

- **Input Decomposition:** Fluctuations of velocity components are isolated prior to feeding into the models:
  $$u'(y, z, t) = u(y, z, t) - U(y)$$
  $$v'(y, z, t) = v(y, z, t) - V(y)$$
  $$w'(y, z, t) = w(y, z, t) - W(y)$$
- **Normalization:** Min-Max normalization transforms all fluctuation inputs component-wise into the interval $[0, 1]$:
  $$\alpha_{\text{norm}} = \frac{\alpha - \alpha_{\min}}{\alpha_{\max} - \alpha_{\min}}, \quad \alpha \in \{u', v', w'\}$$
- **Grid Subsampling Strategy:** Point selection from $112 \times 256$ down to $14 \times 32$ uses non-uniform wall-normal spacing:
  $$y_j = f_{\text{stretch}}(j), \quad j \in [1, 14]$$
  placing higher density of resolution points inside the viscous sublayer and buffer layer ($y^+ < 30$).

---

## 4. Required Physics Validation Gates

To ensure the synthetic turbulence maintains spatial and temporal coherence without dissipating in downstream simulations, generated velocity fields must clear the following physical metrics:

1. **Integrated Mean and Fluctuation Profiles:**
   - Inner-scaled mean streamwise velocity profile $U^+ = U/u_\tau$ vs $y^+$.
   - Root-mean-square (RMS) fluctuation profiles $u^+_{\text{rms}}, v^+_{\text{rms}}, w^+_{\text{rms}}$.
   - Reynolds shear stress profile $\langle u'v'\rangle^+$.
2. **Boundary Layer Integral Quantities:**
   - Shape Factor: $H = \frac{\delta^*}{\theta} = \frac{\int_0^\infty \left(1 - \frac{U}{U_\infty}\right) dy}{\int_0^\infty \frac{U}{U_\infty}\left(1 - \frac{U}{U_\infty}\right) dy}$ (Tolerance: error $\le 2.95\%$ vs DNS).
   - Skin Friction Coefficient: $C_f = \frac{2 \tau_w}{\rho U_\infty^2}$.
3. **Spatial Structure (Premultiplied Wavenumber Spectra):**
   - Premultiplied spanwise wavenumber energy spectra $k_z^+ \Phi_{\alpha\alpha}^+(y^+, \lambda_z^+)$ evaluated against DNS across all components $\alpha \in \{u, v, w\}$.
4. **Temporal Structure (Frequency Spectra):**
   - Temporal frequency spectra $\phi_{\alpha\alpha}^+(y^+, f^+)$ to ensure correct energy cascade distribution in time.
5. **Relative L2 Error Norm:**
   $$\varepsilon_\alpha = \frac{1}{J} \sum_{j=1}^J \frac{\left\| \alpha_j^{\text{DNS}} - \alpha_j^{\text{DLM}} \right\|_2}{\left\| \alpha_j^{\text{DNS}} \right\|_2} \quad \text{evaluated across } J \text{ snapshots.}$$
6. **Coherent Structure Identification:**
   - Visualization of hairpin vortices and coherent streak formations via $Q$-criterion iso-surfaces:
     $$Q = \frac{1}{2} \left(\|\mathbf{\Omega}\|^2 - \|\mathbf{S}\|^2\right) = 0.54 \frac{U_\infty^2}{\delta_0^2}$$
     where $\mathbf{S}$ is the rate-of-strain tensor and $\mathbf{\Omega}$ is the vorticity tensor.
7. **Downstream Transient Recovery Distance:**
   - Inflow-outflow LES must display negligible adaptation distance ($x/\delta_0 \approx 0$) downstream of the inlet before matching standard statistical TBL profiles.

---

## 5. Architectural Innovations & Edge Cases

- **Transformer for Spatial Fluid Planes:** Adaptation of self-attention mechanisms to predict parallel temporal evolutions of spatially developing cross-stream velocity slices without sequential recurrent bottlenecks.
- **Transfer Learning (TL) Protocol:**
  - Sequential weight initialization: Model is initially trained on $Re_\theta = 661.5$. Learned weights are iteratively transferred when fine-tuning for higher $Re_\theta$ planes ($905.7, 1362.0$).
  - Efficiency Gain: Reduces required training data by 75% (using 25% of sequence length) and overall training duration by 52% (reducing training time from over 100 hrs down to 23 hrs for the Transformer).
- **Extrapolation / Interpolation Behavior:**
  - *Interpolation ($Re_\theta = 763.8, 1155.1$):* Captures large-scale structures and main energy modes; under-predicts fine-scale fluctuations, causing slight under-prediction in $u^+_{\text{rms}}$ and $\langle u'v'\rangle^+$.
  - *Extrapolation ($Re_\theta = 1502.0$):* Successfully generates stable flow fields, but accumulated error in high-wavenumber energy content causes minor statistical deviations.

---

## 6. Raw Data Corrections Log

1. **Equation (2.6) & (2.7) Relativistic Discriminator Definition:**
   - *Original Text:* $D_{Ra}(x_r, x_a) = \sigma(C(x_r)) - \mathbb{E}_{x_a}[C(x_a)]$
   - *Correction:* Reconstructed to standard Relativistic Average Discriminator formulation according to Jolicoeur-Martineau (2018):
     $$D_{Ra}(x_r, x_a) = \sigma\left(C(x_r) - \mathbb{E}_{x_a}[C(x_a)]\right)$$
2. **Equation (4.1) Model Abbreviation Typo:**
   - *Original Text:* Term inside norm written as $\alpha_j^{\text{LDM}}$ in the numerator.
   - *Correction:* Corrected to match the paper's deep learning model acronym: $\alpha_j^{\text{DLM}}$.
3. **Loss Function Notation $\mathcal{E}_G^{\text{ra}}$:**
   - *Original Text:* Equation (2.9) labeled as $\mathcal{E}_G^{\text{ra}}$, then referenced as $\ell_G^{Ra}$ in equation (2.10).
   - *Correction:* Standardized notation to generator adversarial loss $\ell_G^{Ra}$.
4. **Parameter Inferences:**
   - Generator multiscale filter kernel sizes inferred as $3\times3$, $5\times5$, $7\times7$ following the referenced baseline MS-ESRGAN architecture (Yousif et al., 2021).