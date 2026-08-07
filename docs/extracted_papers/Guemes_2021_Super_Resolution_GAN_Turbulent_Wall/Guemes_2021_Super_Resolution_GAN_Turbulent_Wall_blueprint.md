## 1. Physical Problem Statement
- **Domain & Geometry**: Incompressible turbulent open-channel flow solved via direct numerical simulation (DNS) using the pseudo-spectral solver SIMSON.
  - Domain size: $L_x \times L_y \times L_z = 4\pi h \times h \times 2\pi h$, where $h$ is the channel height.
  - Discretization / Resolution: $192 \times 65 \times 192$ modes ($192$ Fourier modes in streamwise $x$ and spanwise $z$, $65$ Chebyshev modes in wall-normal $y$).
- **Flow Regime & Reynolds Number**: 
  - Friction Reynolds number: $Re_\tau = \frac{u_\tau h}{\nu} = 180$.
  - Friction velocity: $u_\tau = \sqrt{\frac{\tau_w}{\rho}}$.
- **Input Quantities**:
  - Wall measurement snapshot vector at wall grid $(N_x^d, N_z^d)$:
    $$\mathbf{q}_w(x, z) = \left[ \tau_w^x(x, z), \tau_w^z(x, z), p^w(x, z) \right]^T$$
    where $\tau_w^x$ is the streamwise wall-shear-stress fluctuation, $\tau_w^z$ is the spanwise wall-shear-stress fluctuation, and $p^w$ is the wall pressure fluctuation.
  - Downsampling factors applied per axis: $f_d \in \{1, 4, 8, 16\}$, corresponding to input grid resolution $N_x^d \times N_z^d = \left(\frac{192}{f_d}\right) \times \left(\frac{192}{f_d}\right)$.
- **Target Quantities**:
  1. High-resolution wall fields $\mathbf{q}_w \in \mathbb{R}^{192 \times 192 \times 3}$.
  2. Wall-parallel velocity fluctuation vector $\mathbf{u}(x, y^+, z) = [u, v, w]^T \in \mathbb{R}^{192 \times 192 \times 3}$ at inner-scaled wall-normal planes $y^+ \in \{15, 30, 50, 100\}$, where $y^+ = \frac{y u_\tau}{\nu}$.

---

## 2. Network Architectures

### Super-Resolution Generative Adversarial Network (SRGAN)
- **Generator Network ($G$)**:
  - Input shape: $\left(\frac{192}{f_d}, \frac{192}{f_d}, 3\right)$ for downsampled inputs; $(192, 192, 3)$ when $f_d = 1$.
  - Core block: $16$ Residual Blocks (ResBlocks).
    - ResBlock structure: $\text{Conv2D} \rightarrow \text{BatchNorm} \rightarrow \text{PReLU} \rightarrow \text{Conv2D} \rightarrow \text{BatchNorm} \rightarrow \text{Elementwise Add}$.
  - Resolution Enhancement / Upsampling: $\log_2(f_d)$ sub-pixel convolution layers (PixelShuffle) placed after residual blocks. Omitted if $f_d = 1$.
  - Output shape: $(192, 192, 3)$.
- **Discriminator Network ($D$)**:
  - Input shape: $(192, 192, 3)$ (real high-resolution sample $H_R$ or generated sample $G(L_R)$).
  - Convolutional feature extractor blocks followed by $2$ Fully Connected (FC) layers.
  - Final Activation: Sigmoid ($\sigma$).
- **Loss Functions**:
  - Discriminator Binary Cross-Entropy Loss:
    $$\mathcal{L}_D = -\mathbb{E}_{H_R \sim p_{\text{data}}}\left[\log D(H_R)\right] - \mathbb{E}_{L_R \sim p_{L_R}}\left[\log\left(1 - D(G(L_R))\right)\right]$$
  - Generator Composite Loss:
    $$\mathcal{L}_G = \mathcal{L}_{\text{MSE}} + \lambda \mathcal{L}_{\text{adv}}$$
    $$\mathcal{L}_{\text{MSE}} = \frac{1}{N_x N_z} \sum_{i=1}^{N_x} \sum_{j=1}^{N_z} \left\| G(L_R)_{i,j} - H_{R, i,j} \right\|_2^2$$
    $$\mathcal{L}_{\text{adv}} = -\mathbb{E}_{L_R \sim p_{L_R}}\left[\log D(G(L_R))\right]$$
    where $N_x = 192$, $N_z = 192$, and hyperparameter weight $\lambda = 10^{-3}$.
- **Optimization Parameters**:
  - Optimizer: Adam ($\beta_1 = 0.9, \beta_2 = 0.999$).
  - Learning Rate: $10^{-4}$.
  - Epochs: $30$.

### Baseline Architecture: Subdomain FCN-POD
- **Subdomain Spatial Decomposition**:
  - Field divided into $N_s = 12 \times 12 = 144$ subdomains of spatial size $N_p \times N_p = 16 \times 16$ grid points.
  - Proper Orthogonal Decomposition (POD) computed on each $16 \times 16$ subdomain to retain modes capturing $\ge 90\%$ kinetic energy ($O(10^2)$ modes).
- **Network Pipeline**:
  - Fully Convolutional Network predicts $3\text{D}$ tensor of POD coefficients per subdomain from input wall quantities.
  - For downsampled input ($f_d > 1$), $\log_2(f_d)$ pooling layers are removed to match input/output spatial constraints.
  - Output reconstructed by projection of predicted coefficients onto local POD modes.
- **Optimization Parameters**:
  - Optimizer: Adam ($\epsilon = 0.1$).
  - Base Learning Rate: $10^{-3}$ with exponential decay starting at epoch $10$.
  - Epochs: $30$.

---

## 3. Data Scaling & Normalization
- **Physical Non-Dimensionalization**:
  - Velocities scaled by friction velocity $u_\tau$: $u^+ = \frac{u}{u_\tau}, v^+ = \frac{v}{u_\tau}, w^+ = \frac{w}{u_\tau}$.
  - Spatial coordinates inner-scaled by viscous length scale $\ell^* = \frac{\nu}{u_\tau}$: $x^+ = \frac{x}{\ell^*}, y^+ = \frac{y}{\ell^*}, z^+ = \frac{z}{\ell^*}$.
- **Statistical Scaling**:
  - Input wall quantities ($\tau_w^x, \tau_w^z, p^w$) and target velocity components ($u, v, w$) are zero-mean centered and divided by their respective field standard deviations $\sigma_\phi$:
    $$\hat{\phi}(x, z) = \frac{\phi(x, z) - \bar{\phi}}{\sigma_\phi}, \quad \text{where } \phi \in \{\tau_w^x, \tau_w^z, p^w, u, v, w\}$$
- **Dataset Partitioning & Temporal Sampling**:
  - **Training Set**: $50,400$ snapshots, sampled at time interval $\Delta t^+ = 5.08$.
  - **Testing Set**: $3,125$ snapshots, sampled at time interval $\Delta t^+ = 1.69$.

---

## 4. Required Physics Validation Gates
1. **Standardized Mean-Squared Error (MSE)**:
   $$\text{MSE}_\phi(y^+) = \frac{1}{N_x N_z} \sum_{i=1}^{N_x} \sum_{j=1}^{N_z} \left( \frac{\phi_{\text{pred}}(i,j) - \phi_{\text{DNS}}(i,j)}{\sigma_{\phi,\text{DNS}}} \right)^2$$
   - Target metrics for wall super-resolution ($f_d = 4$): $\text{MSE}_{\tau_w^x} = 0.0187$, $\text{MSE}_{\tau_w^z} = 0.0244$, $\text{MSE}_{p^w} = 0.0153$.
2. **Pre-Multiplied 2D Power Spectral Density**:
   $$k_x k_z \Phi_{\phi\phi}(k_x, k_z, y^+)$$
   - Must capture $10\%$, $50\%$, and $90\%$ energy isolines of DNS reference spectrum across streamwise wavenumber $k_x$ and spanwise wavenumber $k_z$.
3. **Spectral Fractional Error ($R_{ab}$)**:
   $$R_{ab}(k_x, y^+, k_z) = \frac{\mathcal{R}e \left\{ \mathcal{F}\left(a - a^\dagger\right) \cdot \mathcal{F}\left(b - b^\dagger\right)^* \right\}(k_x, y^+, k_z)}{\mathcal{R}e \left\{ \mathcal{F}(a) \cdot \mathcal{F}(b)^* \right\}(k_x, y^+, k_z)}$$
   where $a, b \in \{u, v, w\}$, $\mathcal{F}$ is the 2D spatial Fourier transform, $(\cdot)^\dagger$ indicates predicted field, and $(\cdot)^*$ denotes complex conjugation.
   - Spatial validation threshold: $R_{ab} \le 0.5$ contour bounds.
4. **Filtered DNS Structural Agreement**:
   - Comparison against sharp spectral low-pass filtered DNS data with cutoff wavenumbers matching $R_{ab}(k_x, k_z) = 0.5$ (e.g., at $y^+=50, f_d=8$: $\lambda_x^+ \approx 500$, $\lambda_z^+ \approx 100$). MSE must decrease when evaluated against filtered DNS (e.g., error drop from $0.603$ to $0.317$).

---

## 5. Architectural Innovations & Edge Cases
- **Viscous-Scaled Downsampling Metric**:
  To enable scale-consistent downsampling evaluation across differing $Re_\tau$, downsampling ratio $f_d$ is generalized to the inner-scaled spatial grid distance $\tilde{f}_d$:
  $$\tilde{f}_d = f_d \sqrt{(\Delta x^+)^2 + (\Delta z^+)^2}$$
  - For $Re_\tau = 180$: $f_d = 4 \implies \tilde{f}_d \approx 52$; $f_d = 8 \implies \tilde{f}_d \approx 105$; $f_d = 16 \implies \tilde{f}_d \approx 210$.
- **High Downsampling / Outer Region Structural Degradation**:
  At extreme downsampling ($f_d = 16$, $\tilde{f}_d \approx 210$) or high wall distances ($y^+ = 100$), the network loses high-wavenumber energy capacity ($R_{ab} > 0.5$ for small scales) and acts as an implicit spatial low-pass filter, recovering only large-scale streaky coherent structures.
- **Subdomain Boundary Continuity in FCN-POD**:
  FCN-POD operates on independent $16 \times 16$ subdomains without explicit inter-block boundary continuity constraints, causing spectral discontinuities at subdomain wavelengths; SRGAN operates globally on $192 \times 192$ fields via convolutions, eliminating patch boundary artifacts.

---

## 6. Raw Data Corrections Log
- **Equation 2 Notation**: Text presents generator loss with $-\lambda \mathcal{L}_D$ where $\mathcal{L}_D$ is the discriminator loss definition. Corrected in Blueprint to standard adversarial loss formulation $\mathcal{L}_G = \mathcal{L}_{\text{MSE}} + \lambda \mathcal{L}_{\text{adv}}$ with $\mathcal{L}_{\text{adv}} = -\mathbb{E}[\log D(G(L_R))]$ to ensure optimizer gradient direction consistency.
- **Equation 3 Typo**: Reconstructed missing parentheses in inner-scaled grid metric: $\tilde{f}_d = f_d \sqrt{\Delta x^{+2} + \Delta z^{+2}} \longrightarrow \tilde{f}_d = f_d \sqrt{(\Delta x^+)^2 + (\Delta z^+)^2}$.
- **Text Parameter Formatting Fixes**:
  - Fixed OCR degradation of superscript notation ($Re^\tau \rightarrow Re_\tau = 180$, $y^+ \in [15, 30, 50, 100]$, $f^d \rightarrow f_d$).
  - Corrected exponent signs for optimizer parameters: Adam learning rate $10-4 \rightarrow 10^{-4}$; loss weight $\lambda = 10-3 \rightarrow 10^{-3}$.
  - Restored domain size expression $4\pi h \times h \times 2\pi h$ from corrupted string `4πh × h × 2πh`.