## 1. Physical Problem Statement

The paper presents an unsupervised deep-learning methodology for super-resolution reconstruction of 2D slices of 3D turbulent flow fields using Cycle-Consistent Generative Adversarial Networks (CycleGAN). Three specific flow configurations and data settings are evaluated:

1. **Filtered Homogeneous Isotropic Turbulence (HIT)**
   - **Flow Regime:** Forced incompressible homogeneous isotropic turbulence at Taylor-scale Reynolds number $Re_\lambda = 418$.
   - **Source Data:** Direct Numerical Simulation (DNS) from the Johns Hopkins Turbulence Database (JHTDB) on a $1024^3$ grid over a $2\pi \times 2\pi \times 2\pi$ domain.
   - **Domain & Boundary Conditions:** $x-y$ 2D slices of velocity vectors $(u, v, w)$. Spatial domain sub-region size $128\Delta x \approx 0.785$ (greater than the integral length scale $0.373$). Triply periodic boundary conditions.
   - **Coarsening Operator:** Local average pooling (top-hat filtering) downsampled by resolution ratios $r \in \{4, 8, 16\}$.

2. **Partially Measured Wall-Bounded Channel Flow**
   - **Flow Regime:** Fully developed turbulent channel flow at friction Reynolds number $Re_\tau = \frac{u_\tau \delta}{\nu} = 1000$.
   - **Source Data:** DNS JHTDB dataset over $L_x \times L_y \times L_z = 8\pi\delta \times 2\delta \times 3\pi\delta$ with $N_x \times N_y \times N_z = 2048 \times 512 \times 1536$.
   - **Domain & Boundary Conditions:** Wall-parallel $x-z$ planes at $y^+ = 15$ (near-wall region) and $y^+ = 100$ (outer layer). Periodic in $x$ and $z$; no-slip at wall boundaries ($y=0, 2\delta$). Sub-patch input size $16 \times 16$, output size $128 \times 128$ ($128\Delta x = 1.57$, exceeding the streamwise integral length scale $1.14$).
   - **Coarsening Operator:** Pointwise sparse sub-sampling at every 8th grid point in $x$ and $z$ directions (mimicking sparse PIV/sensor arrays).

3. **Large Eddy Simulation (LES) to DNS Reconstruction**
   - **Flow Regime:** Wall-bounded turbulent channel flow at $Re_\tau = 1000$.
   - **Source Data:** 
     - **DNS:** Domain $8\pi\delta \times 2\delta \times 3\pi\delta$ on $2048 \times 1536$ grid ($x-z$ plane at $y^+ = 15$).
     - **LES:** Domain $2\pi\delta \times 2\delta \times \pi\delta$ on $128 \times 128$ grid ($x-z$ plane at $y^+ = 15$). Solved using Vreman or Smagorinsky ($C_s = 0.17$, van Driest damping) subgrid-scale models.
   - **Resolution Ratio:** Spatial factor of $4 \times 4$ in $x$ and $z$ directions. Input patch size $32 \times 32$, target resolution patch size $128 \times 128$. Datasets are inherently unpaired.

---

## 2. Network Architectures

The unsupervised super-resolution framework utilizes a CycleGAN setup consisting of two generators ($G: X \to Y$, $F: Y \to X$) and two discriminators ($D_Y, D_X$).

```
Low-Res Domain (X) ------ Generator G -----> Reconstructed High-Res (G(x))
        ^                                                   |
        |                                                   v
Reconstructed Low-Res (F(y)) <--- Generator F ------ High-Res Domain (Y)
```

### Generator Architecture ($G, F$)
- **Input Channels:** 3 (corresponding to 2D velocity fields $u, v, w$).
- **Convolutions:** Discrete $3 \times 3$ kernel convolutions throughout.
- **Up-Sampling Operator (in $G$):** $2 \times 2$ Nearest-Neighbor interpolation followed by $3 \times 3$ convolution.
- **Down-Sampling Operator (in $F$):** $2 \times 2$ Average Pooling followed by $3 \times 3$ convolution.
- **Padding:** Zero-padding during training; periodic padding during testing to preserve fluid periodicity.
- **Activation Functions:** Leaky ReLU with negative slope $\alpha = 0.2$ for hidden layers; linear output layer.

### Discriminator Architecture ($D_X, D_Y$)
- **Input Channels:** 3 (for $D_X$ and $D_Y$ in standard CycleGAN) or 6 (for conditional discriminator in benchmark cGAN).
- **Convolutions:** Repeated blocks of $3 \times 3$ convolutions and $2 \times 2$ Average Pooling down-sampling layers.
- **Dense Layers:** 2 Fully Connected (FC) layers at the output processing flattened feature maps to scalar validity scores.
- **Activation Functions:** Leaky ReLU ($\alpha = 0.2$) across all internal layers.

### Hyperparameters & Optimization
- **Optimizer:** Adam ($\beta_1 = 0.5, \beta_2 = 0.999$).
- **Base Learning Rate:** $\eta = 1.0 \times 10^{-4}$ (CycleGAN, cGAN); $\eta = 5.0 \times 10^{-4}$ with step-decay by $1/5$ on validation plateau (benchmark CNN).
- **Batch Size:** 16.
- **Total Training Iterations:** $500,000$.
- **Adversarial Objective Scheme:** Wasserstein GAN with Gradient Penalty (WGAN-GP) to eliminate mode collapse and ensure stable divergence optimization.

---

## 3. Data Scaling & Normalization

1. **Velocity Field Normalization:**
   Velocity components $u, v, w$ are non-dimensionalized by dividing by the standard deviation of the high-resolution DNS flow field ($\sigma_{\text{DNS}}$):
   $$\tilde{u}_i = \frac{u_i}{\sigma_{\text{DNS}, u_i}}$$

2. **Wall-Bounded Non-Dimensionalization:**
   Spatial coordinates and velocities in channel flows are scaled by the friction velocity $u_\tau$ and kinematic viscosity $\nu$:
   $$u^+ = \frac{u}{u_\tau}, \quad y^+ = \frac{y u_\tau}{\nu}, \quad x^+ = \frac{x u_\tau}{\nu}, \quad z^+ = \frac{z u_\tau}{\nu}$$

3. **Domain Sampling Dimensions:**
   - **HIT:** DNS grid spacing $\Delta x = 2\pi / 1024$. Sub-region target size $N_x \times N_y = 128 \times 128$.
   - **Channel Flow (Pointwise):** Input $16 \times 16 \to$ Target $128 \times 128$.
   - **LES-to-DNS:** Input $32 \times 32 \to$ Target $128 \times 128$.

---

## 4. Required Physics Validation Gates

To validate that the reconstructed flow fields are physically consistent with true turbulence, models are verified against the following quantitative gates:

1. **Pixel-Wise Normalized Mean Squared Error (MSE):**
   $$\text{MSE} = \frac{\mathbb{E}_{x \sim P_X} \left[ \| G(x) - y \|_2^2 \right]}{\sigma_{\text{DNS}}^2}$$

2. **Fourier Phase Error:**
   Absolute error of phase angles across spatial wavenumbers $\kappa_x, \kappa_z$:
   $$E_{\text{phase}}(\kappa_x, \kappa_z) = \left| \text{phase}\left(\hat{u}_i^{\text{CycleGAN}}(\kappa_x, \kappa_z)\right) - \text{phase}\left(\hat{u}_i^{\text{DNS}}(\kappa_x, \kappa_z)\right) \right|$$

3. **1D Energy Spectra:**
   Streamwise and spanwise velocity power spectra evaluating tail energy recovery beyond the cutoff wavenumber $\kappa_{\text{cutoff}}$:
   $$E(\kappa_x) = \frac{1}{2\pi} \int_{-\infty}^{\infty} e^{-i p \kappa_x} \langle V_i(x, y) V_i(x+p, y) \rangle dp$$

4. **Probability Density Functions (PDF):**
   PDF profiles matching higher-order fluctuations of out-of-plane vorticity components:
   $$\omega_z = \frac{\partial v}{\partial x} - \frac{\partial u}{\partial y}, \quad \omega_y = \frac{\partial u}{\partial z} - \frac{\partial w}{\partial x}$$

5. **Spatial and Temporal Auto-Correlations:**
   - Spatial two-point velocity correlation: $R_{V_i V_i}(r) = \langle V_i(\mathbf{x}) V_i(\mathbf{x} + r\hat{\mathbf{e}}) \rangle$
   - Temporal velocity correlation: $R_{V_i V_i}(\tau) = \langle V_i(t) V_i(t + \tau) \rangle$

6. **Higher-Order Statistical Moments:**
   Verification of Mean, RMS, Reynolds Shear Stress ($\langle u'v' \rangle$), Skewness ($S = \frac{\langle u'^3 \rangle}{\langle u'^2 \rangle^{3/2}}$), and Flatness ($F = \frac{\langle u'^4 \rangle}{\langle u'^2 \rangle^2}$).

---

## 5. Architectural Innovations & Edge Cases

### Overall CycleGAN Objective Function
$$\mathcal{L}_{\text{total}}(G, F, D_Y, D_X) = \mathcal{L}_{\text{WGAN-GP}}(G, D_Y) + \mathcal{L}_{\text{WGAN-GP}}(F, D_X) + \lambda_{\text{cycle}} \mathcal{L}_{\text{cycle}}(G, F) + \mathcal{L}_{\text{custom}}$$
where $\lambda_{\text{cycle}} = 10$, and the cycle loss is formulated as:
$$\mathcal{L}_{\text{cycle}}(G, F) = \mathbb{E}_{x \sim P_X} \left[ \| F(G(x)) - x \|_2^2 \right] + \mathbb{E}_{y \sim P_Y} \left[ \| G(F(y)) - y \|_2^2 \right]$$

### Edge Case 1: Pointwise Measurement Constraints ($\mathcal{L}_{\text{pixel}}$)
In spatially homogeneous domains, pure unsupervised adversarial loss suffers from arbitrary spatial phase shifts. When low-resolution inputs represent pointwise grid measurements (Example 2), a pixel-consistency loss is added to enforce exact spatial phase lock:
$$\mathcal{L}_{\text{pixel}} = \lambda_{\text{pixel}} \mathbb{E}_{x \sim P_X} \left[ \frac{1}{N_p} \sum_{i=1}^{N_p} \left( x^{\text{LR}}(p_i) - G(x)(p_i) \right)^2 \right]$$
where $p_i$ denotes the $N_p$ sparse measurement pixel locations, and $\lambda_{\text{pixel}} = 10$.

### Edge Case 2: LES-to-DNS Consistency Loss ($\mathcal{L}_{\text{LR}}$)
When mapping independently generated LES fields to DNS resolution (Example 3), paired true data do not exist. To prevent spatial phase drift while allowing small-scale synthesis, top-hat domain filtering $\mathcal{I}$ is applied to the generator output to enforce large-scale conservation:
$$\mathcal{L}_{\text{LR}} = \lambda_{\text{LR}} \mathbb{E}_{x \sim P_X} \left[ \frac{1}{N_p} \sum_{i=1}^{N_p} \left( x(p_i) - \left(\mathcal{I} G(x)\right)(p_i) \right)^2 \right]$$
where $\mathcal{I}$ acts as an explicit low-pass spatial filter operator matching the LES filter scale, and $\lambda_{\text{LR}} = 10$.

---

## 6. Raw Data Corrections Log

| Source Text / Equation | Extraction Error / Ambiguity | Corrected / Inferred Form |
| :--- | :--- | :--- |
| Eq. 2.1: $\min_G \frac{V(D, G)}{D} = \dots$ | Fragmented fraction/operator in adversarial objective | $\min_G \max_D V(D, G) = \mathbb{E}_{x \sim P_X} [\log D(x)] + \mathbb{E}_{z \sim P_Z} [\log(1 - D(G(z)))]$ |
| Eq. 2.3: $\mathcal{C}_{\text{GAN}}(F, D_X) = \dots$ | Typo in equation label ($\mathcal{C}$ instead of $\mathcal{L}$) | $\mathcal{L}_{\text{GAN}}(F, D_X) = \mathbb{E}_{x \sim P_X} [\log D_X(x)] + \mathbb{E}_{y \sim P_Y} [\log(1 - D_X(F(y)))]$ |
| Eq. 2.4: $kk^2_2$ | Broken LaTeX OCR for norm operation | $\| F(G(x)) - x \|_2^2$ and $\| G(F(y)) - y \|_2^2$ |
| Eq. 2.5: $\mathcal{L} = \mathcal{L}_{\text{GAN}} + \mathcal{L}_{\text{GAN}} + \mathcal{L}_{\text{cycle}}$ | Missing weighting factor $\lambda$ in displayed formula | $\mathcal{L}(G, F, D_Y, D_X) = \mathcal{L}_{\text{GAN}}(G, D_Y) + \mathcal{L}_{\text{GAN}}(F, D_X) + \lambda \mathcal{L}_{\text{cycle}}(G, F)$ with $\lambda = 10$ |
| Eq. 2.8: $\mathcal{C}_{\text{CGAN}}$, $D(G(x\mid y))$ | Incorrect sub/superscripts and conditional syntax | $\mathcal{L}_{\text{cGAN}} = \mathbb{E}_{y \sim P_Y} [\log D(y \mid x)] + \mathbb{E}_{x \sim P_X} [\log(1 - D(G(x) \mid x))]$ |
| Section 3.1: $Re^\lambda = 418$ | Superscript distortion on Taylor Reynolds number | $Re_\lambda = 418$ |
| Eq. 3.1: $hi$ | Missing expectation brackets for auto-correlation | $\langle V_i(x, y) V_i(x+p, y) \rangle$ |
| Eq. 3.4: $(x(p_i) - \mathcal{I}G(p_i))^2$ | Ambiguous operator notation for filtered generated output | $\left( x(p_i) - (\mathcal{I} G(x))(p_i) \right)^2$ |
| Appendix C: Eq. C1, C2 | Missing overbars and missing stress tensor indices | $\frac{\partial \bar{u}_i}{\partial x_i} = 0$, $\frac{\partial \bar{u}_i}{\partial t} + \frac{\partial \bar{u}_j \bar{u}_i}{\partial x_j} = -\frac{\partial \bar{p}}{\partial x_i} + \frac{1}{Re_\tau} \frac{\partial^2 \bar{u}_i}{\partial x_j \partial x_j} - \frac{\partial \tau_{ij}}{\partial x_j}$ |