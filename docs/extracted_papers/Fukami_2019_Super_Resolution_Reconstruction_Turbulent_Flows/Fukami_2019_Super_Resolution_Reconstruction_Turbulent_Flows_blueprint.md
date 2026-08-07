## 1. Physical Problem Statement

The paper presents machine learning super-resolution frameworks for reconstructing high-resolution ($128 \times 128$ or $192 \times 112$) laminar and turbulent fluid flow fields from extremely coarse, downsampled input fields ($16 \times 16$, $8 \times 8$, or $4 \times 4$). Two test cases are examined:

### Case 1: Two-Dimensional Laminar Cylinder Wake
* **Flow Regime**: Incompressible 2D unsteady laminar wake past a circular cylinder at Reynolds number $Re_D = \frac{U_\infty D}{\nu} = 100$.
* **Governing Equations**: Incompressible Navier-Stokes equations:
  $$\nabla \cdot \mathbf{u} = 0$$
  $$\frac{\partial \mathbf{u}}{\partial t} + \mathbf{u} \cdot \nabla \mathbf{u} = -\nabla p + \frac{1}{Re_D} \nabla^2 \mathbf{u}$$
* **Computational Domain & Grid**: $(x/D, y/D) \in [-0.7, 15] \times [-5, 5]$ with high-resolution DNS grid $(N_x, N_y) = (192, 112)$ and time step $\Delta t = 2.50 \times 10^{-3}$.
* **Dataset**: $N_{\text{snapshots}} = 1000$ snapshots spanning 8 full vortex shedding cycles. Field attribute: Vorticity scalar $\omega$.

### Case 2: Two-Dimensional Decaying Homogeneous Isotropic Turbulence
* **Flow Regime**: 2D homogeneous decaying turbulent flow exhibiting both direct and inverse energy cascades.
* **Governing Equations**: 2D vorticity transport equation:
  $$\frac{\partial \omega}{\partial t} + \mathbf{u} \cdot \nabla \omega = \frac{1}{Re_0} \nabla^2 \omega$$
* **Computational Domain & Grid**: Bi-periodic domain $[0, 1] \times [0, 1]$, solved via Fourier spectral DNS on high-resolution grid $(N_x, N_y) = (128, 128)$.
* **Reynolds Numbers**: $Re_0 = \frac{u^*(t_0) l^*(t_0)}{\nu} = 74.6$ for training/validation ($0.195 \le t \le 2.145$), and $Re_0 = 87.7$ for test data.
* **Field Attributes**: Velocity vector $\mathbf{u} = \{u, v\}$ ($K=2$ channels) or vorticity field $\omega$ ($K=1$ channel).
* **Coarsening Operations**:
  Downsampling applied via pooling windows of size $M \times M$ ($M \in \{8, 16, 32\}$):
  $$q_{ij}^{\text{LR}} = \left[ \frac{1}{M^2} \sum_{p,s \in P_{i,j}} (q_{ps}^{\text{HR}})^P \right]^{1/P}$$
  - Average pooling ($P = 1$)
  - Max pooling ($P = \infty$)
  - Spatial Downsampling Levels: Medium Resolution (MR, $16 \times 16$), Low Resolution (LR, $8 \times 8$), Super-Low Resolution (SLR, $4 \times 4$).

---

## 2. Network Architectures

Two deep convolutional topologies are evaluated for mapping coarse data $x \in \mathbb{R}^{(N_x/M) \times (N_y/M) \times K}$ to high-resolution flow fields $y \in \mathbb{R}^{N_x \times N_y \times K}$:

```
[Low-Res Input x] ──> [DSC Block: Strided Conv / Skip Connections] ──> [MS Block: Multi-Scale Parallel Filters] ──> [High-Res Output y]
```

### 1. Standard Convolutional Neural Network (CNN)
* **Depth**: 3 convolutional layers ($l_{\text{max}} = 3$).
* **Layer Operation**:
  $$q_{ijm}^{(l)} = \varphi \left( \sum_{k=0}^{K-1} \sum_{p=0}^{H-1} \sum_{s=0}^{H-1} q_{i+p, j+s, k}^{(l-1)} h_{pskm} \right)$$
  where $H \times H$ is the kernel filter size, $K$ is the channel dimension, and $\varphi(\cdot)$ is the activation function.
* **Activation Function**: Rectified Linear Unit ($\text{ReLU}$): $\phi(z) = \max(0, z)$.
* **Padding**: Custom periodic boundary condition padding embedded directly into the convolution operator (zero-padding performs similarly).
* **Optimizer**: Adam optimizer with mean squared error (MSE) loss:
  $$w = \operatorname{argmin}_w \|y - \mathcal{F}(x; w)\|_2^2$$

### 2. Hybrid Downsampled Skip-Connection / Multi-Scale (DSC/MS) Model
* **Downsampled Skip-Connection (DSC) Sub-Block**:
  * Downsampling/triangular operations via convolutional compression to extract scale-invariant representation features.
  * Skip-connections (residual connections) spanning across layers to prevent vanishing gradients and accelerate parameter convergence.
* **Multi-Scale (MS) Sub-Block**:
  * Parallel convolutional pathways containing filters with varying spatial receptive field sizes ($H_1, H_2, \dots, H_m$) to capture multiscale turbulent eddies.
* **Training Regularization**: Early stopping criterion triggered when validation loss fails to decrease after 20 consecutive epochs.

---

## 3. Data Scaling & Normalization

* **Normalization Scheme**: None.
* **Scale Invariance**: Raw numerical flow variables ($u, v, \omega$) are fed directly into the networks without min-max or z-score standardization. This preserves physical scales, rendering the learned super-resolution model scale-invariant across input magnitudes.

---

## 4. Required Physics Validation Gates

To prove physical accuracy, generated super-resolution fields must pass four evaluation metrics against DNS ground truth:

1. **Relative $L^2$ Error Norm**:
   $$E = \frac{\|\mathbf{q}_{\text{HR}} - \mathcal{F}(\mathbf{q}_{\text{LR}})\|_2}{\|\mathbf{q}_{\text{HR}}\|_2}$$
   Evaluated snapshot-by-snapshot and ensemble-averaged over 2,000 unseen test snapshots.

2. **Kinetic Energy Spectra $E(k)$**:
   Energy spectrum evaluated over spatial wavenumber $k$. Model validity is quantified by the wavenumber ratio $\frac{k_{\text{max}}}{k_{\text{cutoff}}}$, where $k_{\text{max}}$ is the maximum wavenumber at which the reconstructed spectrum agrees within $\ge 90\%$ of DNS reference kinetic energy spectrum:
   $$\left| \frac{E_{\text{SR}}(k) - E_{\text{DNS}}(k)}{E_{\text{DNS}}(k)} \right| \le 0.10 \quad \forall k \le k_{\text{max}}$$

3. **Vorticity Probability Density Function $\text{pdf}(\omega)$**:
   Statistical distribution match over all grid nodes between DNS reference and model prediction to ensure subgrid-scale turbulence intermittency is preserved.

4. **Inference Execution Time Gate**:
   Per-snapshot execution time on GPU (NVIDIA Tesla K40):
   $$\text{Execution Time}_{\text{DSC/MS}} \approx 1.32 \times 10^{-2} \text{ s} \ll \text{Bicubic Interpolation} \approx 6.69 \times 10^{-2} \text{ s}$$

---

## 5. Architectural Innovations & Edge Cases

* **Downsampling Operator Sensitivity**: The network performance depends strongly on the physical meaning of the downsampling filter:
  * **Average Pooling ($P=1$)**: Models downscaled mean-filter/grid-filter operations. Highly robust; allows DSC/MS to successfully reconstruct $128 \times 128$ turbulence fields from extreme $4 \times 4$ coarse inputs.
  * **Max Pooling ($P=\infty$)**: Artificially retains peak vorticity/velocity extrema. Degrades learning stability and creates non-physical "staircase" artifacts at coarse scales.
* **Small Data Threshold**: The multi-scale skip-connection topology (DSC/MS) achieves accurate subgrid reconstruction using as few as $N_{\text{snapshots}} = 50$ training snapshots.
* **Input Field Sensitivity**: Reconstructing vorticity ($\omega$) is physically more challenging than velocity ($\mathbf{u}$) due to higher energy spectral content at small scales (amplified by wavenumber $k$).

---

## 6. Raw Data Corrections Log

1. **Equation Parsing (OCR Error)**:
   * Text rendered `0.195 6 t 6 2.145` for decaying turbulence time domain. Reconstructed to $0.195 \le t \le 2.145$.
   * Text rendered error norm definition `kx HR − F(x)k2/kx HRk2`. Reconstructed to valid vector norm notation: $\frac{\|\mathbf{q}_{\text{HR}} - \mathcal{F}(\mathbf{x})\|_2}{\|\mathbf{q}_{\text{HR}}\|_2}$.
2. **Dimension Variable Corrections**:
   * OCR symbols `Lα` and `Lβ` repaired to grid spatial dimensions $L_\alpha$ and $L_\beta$ ($N_x$ and $N_y$).
3. **Training Time Metrics (Table 1 Reconstruction)**:
   * Epoch training times in text reconstructed from OCR fragments:
     * **CNN**: 4.05 h ($18\text{ s/epoch} \times 809\text{ epochs}$)
     * **DSC/MS**: 6.96 h ($90\text{ s/epoch} \times 261\text{ epochs}$)