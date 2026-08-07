## 1. Physical Problem Statement

* **Flow Regime & Physics**: Incompressible turbulent open-channel flow governed by the Navier-Stokes equations, simulated via Direct Numerical Simulation (DNS) using the pseudo-spectral solver SIMSON.
* **Reynolds Number**: Friction Reynolds number $Re_\tau = \frac{u_\tau h}{\nu} = 180$, where $h$ is the channel height, $u_\tau = \sqrt{\frac{\tau_w}{\rho}}$ is the friction velocity, $\tau_w$ is the wall shear stress magnitude, $\rho$ is the fluid density, and $\nu$ is the kinematic viscosity.
* **Domain & Computational Grid**:
  * Physical domain size: $L_x \times L_y \times L_z = 4\pi h \times h \times 2\pi h$ in the streamwise ($x$), wall-normal ($y$), and spanwise ($z$) directions.
  * Spatial discretisation: $N_x \times N_y \times N_z = 192 \times 65 \times 192$ grid points (Fourier modes in $x, z$; 65 Chebyshev modes in $y$).
* **Input-Output Mapping Tasks**:
  1. *Task 1 (Wall Resolution Enhancement)*: Super-resolution mapping from low-resolution wall measurement fields $(\tau_w^x, \tau_w^z, p_w)_{\text{coarse}}$ to high-resolution wall fields $(\tau_w^x, \tau_w^z, p_w)_{\text{fine}}$ for downsampling factors $f_d \in \{4, 8, 16\}$.
  2. *Task 2 (Wall-to-Flow Field Reconstruction)*: Cross-plane estimation of two-dimensional wall-parallel velocity fluctuation fields $(u, v, w)$ at target inner-scaled wall distances $y^+ \in \{15, 30, 50, 100\}$ using coarse wall measurement inputs $(\tau_w^x, \tau_w^z, p_w)_{\text{coarse}}$ with downsampling factors $f_d \in \{1, 4, 8, 16\}$.
* **Dataset Characteristics**:
  * Training set: 50,400 temporal snapshots with step interval $\Delta t^+ = \frac{\Delta t \cdot u_\tau^2}{\nu} = 5.08$.
  * Testing set: 3,125 temporal snapshots with step interval $\Delta t^+ = 1.69$.

---

## 2. Network Architectures

### Primary Model: Super-Resolution Generative Adversarial Network (SRGAN)
* **Generator ($G$) Topology**:
  * **Backbone**: Fully convolutional architecture with 16 Residual Blocks (ResNet style).
  * **Residual Block Unit**: $[ \text{Conv2D} \to \text{Batch Normalization (BN)} \to \text{PReLU} \to \text{Conv2D} \to \text{BN} \to \text{Elementwise Addition} ]$.
  * **Upsampling Head**: $\log_2(f_d)$ sequential Sub-Pixel Convolution (PixelShuffle) layers for spatial reconstruction when $f_d > 1$. Sub-pixel layers are omitted for full-resolution input ($f_d = 1$).
  * **Activations**: Parametric ReLU (PReLU) in intermediate layers; linear output layer.
* **Discriminator ($D$) Topology**:
  * **Backbone**: Sequential 2D Convolutional layers with strided convolutions for spatial reduction.
  * **Dense Head**: Two Fully-Connected (FC) layers.
  * **Activations**: LeakyReLU in convolutional layers; Sigmoid activation at the final FC node outputting real vs. generated domain probability $D(\cdot) \in [0, 1]$.

### Baseline Model: POD-based Fully-Convolutional Network (FCN-POD)
* **Domain Decomposition**: $12 \times 12$ spatial subdomains, each containing $16 \times 16$ grid points ($N_p \times N_p$).
* **Topology**:
  * FCN maps input wall parameters to a 3D tensor of Proper Orthogonal Decomposition (POD) coefficients corresponding to $O(10^2)$ spatial POD modes per subdomain (retaining $\ge 90\%$ flow kinetic energy).
  * Predicted POD coefficients are projected onto pre-computed spatial POD bases to reconstruct velocity fields.
  * For coarse inputs ($f_d > 1$), $\log_2(f_d)$ max-pooling layers are removed from the standard baseline architecture.

---

## 3. Data Scaling & Normalization

* **Field Centering**: All inputs (streamwise wall shear stress $\tau_w^x$, spanwise wall shear stress $\tau_w^z$, wall pressure $p_w$) and outputs (velocity fluctuations $u, v, w$) are centered by subtracting their spatial-temporal mean values:
  $$\phi(x, y, z, t) = \Phi(x, y, z, t) - \overline{\Phi}(y)$$
* **Variance Standardisation**: Each fluctuating input and target component is non-dimensionalized by its corresponding field standard deviation ($\sigma_{\phi}$):
  $$\phi^* = \frac{\phi}{\sigma_\phi}, \quad \phi \in \{\tau_w^x, \tau_w^z, p_w, u, v, w\}$$
* **Viscous Non-Dimensionalization (Inner Units)**:
  $$u^+ = \frac{u}{u_\tau}, \quad y^+ = \frac{y u_\tau}{\nu}, \quad x^+ = \frac{x u_\tau}{\nu}, \quad z^+ = \frac{z u_\tau}{\nu}$$
* **Normalized Downsampling Metric ($\tilde{f}_d$)**: To enable physical comparisons across different friction Reynolds numbers ($Re_\tau$), downsampling factor $f_d$ is scaled by grid spacing in viscous units:
  $$\tilde{f}_d = f_d \sqrt{(\Delta x^+)^2 + (\Delta z^+)^2}$$
  For $Re_\tau = 180$: $f_d = 4 \implies \tilde{f}_d \approx 52$; $f_d = 8 \implies \tilde{f}_d \approx 105$; $f_d = 16 \implies \tilde{f}_d \approx 210$.

---

## 4. Required Physics Validation Gates

* **Normalized Mean-Squared Error (MSE)**:
  $$\text{MSE}_\phi(y) = \frac{1}{N_x N_z} \sum_{i=1}^{N_x} \sum_{j=1}^{N_z} \left( \frac{\hat{\phi}(x_i, y, z_j) - \phi(x_i, y, z_j)}{\sigma_\phi(y)} \right)^2$$
  Evaluated individually across components $\phi \in \{\tau_w^x, \tau_w^z, p_w, u, v, w\}$.
* **Pre-Multiplied 2D Power Spectral Density (PSD)**:
  Pre-multiplied spectra $k_x k_z \Phi_{\phi\phi}(k_x, k_z)$ at inner-scaled spatial wavenumbers $k_x, k_z$. Models must preserve the $10\%$, $50\%$, and $90\%$ isolines of maximum energy content relative to reference DNS spectra.
* **Spectral Fractional Error ($R_{ab}$)**:
  Calculated across streamwise wavenumber $k_x$ and spanwise wavenumber $k_z$ to assess scale-dependent error:
  $$R_{ab}(k_x, y, k_z) = \frac{\mathcal{Re}\left( \mathcal{F}\{a - a^\dagger\} \cdot \mathcal{F}\{b - b^\dagger\}^* \right)(k_x, y, k_z)}{\mathcal{Re}\left( \mathcal{F}\{a\} \cdot \mathcal{F}\{b\}^* \right)(k_x, y, k_z)}$$
  where $\mathcal{F}\{\cdot\}$ denotes the 2D spatial Fourier transform, $\dagger$ denotes estimated quantities, $*$ denotes complex conjugate, and $a, b \in \{u, v, w\}$. Validation threshold set at iso-contour $R_{ab} = 0.5$.
* **Coherent Structure / Streak Filtering Gate**:
  Comparison of predictions with low-pass spatial filtered DNS fields using spectral cut-off thresholds derived from $R_{ab} < 0.5$ ($\lambda_x^+ \approx 500$, $\lambda_z^+ \approx 100$) to verify capture of large-scale streak topologies.

---

## 5. Architectural Innovations & Edge Cases

* **Composite Loss Function**:
  * **Discriminator Loss**:
    $$\mathcal{L}_D = -\mathbb{E}_{H_R}\left[ \log D(H_R) \right] - \mathbb{E}_{L_R}\left[ \log\left(1 - D(G(L_R))\right) \right]$$
  * **Generator Content-Adversarial Loss**:
    $$\mathcal{L}_G = \frac{1}{N_x N_z} \sum_{i=1}^{N_x} \sum_{j=1}^{N_z} \left| G(L_R)_{i,j} - H_{R\,i,j} \right|^2 - \lambda \mathcal{L}_D$$
    where $H_R$ is the high-resolution reference tensor, $L_R$ is the low-resolution input tensor, and $\lambda = 10^{-3}$ balances pixel-wise MSE against adversarial generation.
* **Resolution Enhancement via Sub-Pixel Convolution**: Use of periodic spatial rearrangement layers ($\log_2(f_d)$ sub-pixel layers) in generator to prevent spatial checkerboard artifacts caused by standard deconvolution.
* **Optimization Specifications**:
  * **SRGAN Training**: Adam optimizer, learning rate $= 10^{-4}$, weight update period $= 30$ epochs.
  * **FCN-POD Training**: Adam optimizer, initial learning rate $= 10^{-3}$ with exponential decay starting at epoch 10, hyperparameter $\epsilon = 0.1$, total epochs $= 30$.

---

## 6. Raw Data Corrections Log

1. **Equation (1) & (2) Formatting**: Reconstructed broken adversarial loss operator notation in the original text to clean mathematical forms: $\mathcal{L}_D$ and composite Generator loss $\mathcal{L}_G$.
2. **Equation (3) Typo**: Fixed exponent placement for grid spacing in viscous units; corrected $\tilde{f}_d = f_d \sqrt{\Delta x^{+2} + \Delta z^{+2}}$ to explicit squared distance metric $\tilde{f}_d = f_d \sqrt{(\Delta x^+)^2 + (\Delta z^+)^2}$.
3. **Equation (4) Spectral Fractional Error**: Reconstructed complex conjugate notation $(b - b^\dagger)^*$ and real-part operator $\mathcal{Re}(\cdot)$ from fragmented raw OCR text.
4. **Sub-Pixel Layer Terminology**: Reconstructed OCR artifact `log2(fd)` as $\log_2(f_d)$ layers across model descriptions.
5. **Viscous Length Scale Notation**: Reconstructed missing viscous length definition `∗ = ν/uτ` to standard notation $\ell^* = \frac{\nu}{u_\tau}$.