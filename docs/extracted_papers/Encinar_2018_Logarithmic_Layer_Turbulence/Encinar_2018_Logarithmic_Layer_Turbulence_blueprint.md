## 1. Physical Problem Statement

- **Flow Regime & Governing Equations**: Incompressible turbulent channel flow governed by the 3D incompressible Navier-Stokes equations:
  $$\nabla \cdot \mathbf{u} = 0$$
  $$\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla)\mathbf{u} = -\nabla p + \nu \nabla^2 \mathbf{u}$$
  where $\mathbf{u} = (u, v, w)^T$ represent velocity fluctuations in the streamwise ($x$), wall-normal ($y$), and spanwise ($z$) directions, $p$ is kinematic pressure fluctuation, and $\nu$ is kinematic viscosity.
- **Domain Geometry & Boundary Conditions**:
  - Spatial domain: Periodic in streamwise ($x \in [0, L_x]$) and spanwise ($z \in [0, L_z]$) directions. No-slip conditions at channel walls ($y = 0$ and $y = 2h$, where $h$ is the channel half-height).
  - Target domain: Reconstruction of velocity fields across the logarithmic layer ($80\nu/u_\tau \le y \le 0.2h$).
- **DNS Simulation Cases & Parameters**:
  - **S1000**: $Re_\tau = 932$, $(L_x, L_z)/h = (2\pi, \pi)$, Grid $(N_x, N_y, N_z) = (512, 385, 512)$, Spatial resolution $\Delta x^+ = 12$, $\Delta z^+ = 6$, $\Delta y^+ \in [0.03, 7.7]$, Discretization: Chebyshev polynomials ($CH$).
  - **S2000**: $Re_\tau = 2003$, $(L_x, L_z)/h = (2\pi, \pi)$, Grid $(N_x, N_y, N_z) = (1024, N_y, 1024)$, Spatial resolution $\Delta x^+ = 6$, $\Delta z^+ = 6$, $\Delta y^+ \in [0.3, 8.9]$, Discretization: Compact finite differences ($FD$).
  - **F2000**: $Re_\tau = 2003$, $(L_x, L_z)/h = (8\pi, 3\pi)$, Grid $(N_x, N_y, N_z) = (512, N_y, 512)$, Stored resolution $\delta x^+ \approx 120, \delta z^+ \approx 90$, Grid resolution $\Delta x^+ = 9$, $\Delta z^+ = 12$, $\Delta y^+ \in [1.7, 10.6]$, Discretization: Compact finite differences ($FD$).
  - **F5300**: $Re_\tau = 5300$, $(L_x, L_z)/h = (8\pi, 3\pi)$, Grid $(N_x, N_y, N_z) = (1024, N_y, 1084)$, Stored resolution $\delta x^+ \approx 120, \delta z^+ \approx 90$, Grid resolution $\Delta x^+ = 12$, $\Delta z^+ = 30$, $\Delta y^+ \in [1.27, 14]$, Discretization: Compact finite differences ($FD$).
- **Input Wall Observables Vector $\mathbf{E}(x, z)$**:
  Contemporaneous noiseless wall measurements at $y=0$:
  $$\mathbf{E}(x, z) = \left[ p(x, 0, z), \, \frac{\partial u}{\partial y}(x, 0, z), \, \frac{\partial w}{\partial y}(x, 0, z) \right]^T = [E_1, E_2, E_3]^T$$
- **Target Outputs**:
  Reconstructed internal velocity fluctuation fields $u^\dagger(x, y, z)$, $v^\dagger(x, y, z)$, and $w^\dagger(x, y, z)$ at wall-normal distances $y$.

---

## 2. Network Architectures

- **Model Topology**: Spectral Linear Stochastic Estimation (SLSE) / Optimal Linear Convolution Operator. The model maps 2D wall boundary observables $\mathbf{E}(x, z)$ to 3D interior velocity components $a^\dagger(x, y, z)$ for $a \in \{u, v, w\}$.
- **Physical-Space Convolution Mapping**:
  $$a^\dagger(x, y, z) = \sum_{s=1}^{3} \iint \tilde{L}_{s}^{(a)}(x - x', y, z - z') E_s(x', z') \, dx' \, dz'$$
  In discrete form:
  $$a^\dagger(i_x, y, i_z) = \sum_{j_x=1}^{N_x} \sum_{j_z=1}^{N_z} \sum_{s=1}^{3} \tilde{L}_{s}^{(a)}(i_x - j_x, y, i_z - j_z) E_s(j_x, j_z)$$
- **Spectral Domain Decoupling (SLSE System)**:
  Applying a 2D spatial Fourier transform along wall-parallel directions yields uncoupled $3 \times 3$ linear systems for each wavenumber pair $(k_x, k_z)$:
  $$\begin{bmatrix} 
  \langle \hat{E}_1 \hat{E}_1^* \rangle & \langle \hat{E}_1 \hat{E}_2^* \rangle & \langle \hat{E}_1 \hat{E}_3^* \rangle \\
  \langle \hat{E}_2 \hat{E}_1^* \rangle & \langle \hat{E}_2 \hat{E}_2^* \rangle & \langle \hat{E}_2 \hat{E}_3^* \rangle \\
  \langle \hat{E}_3 \hat{E}_1^* \rangle & \langle \hat{E}_3 \hat{E}_2^* \rangle & \langle \hat{E}_3 \hat{E}_3^* \rangle 
  \end{bmatrix} (k_x, k_z)
  \begin{bmatrix} 
  \hat{L}_1^{(a)}(k_x, y, k_z) \\ 
  \hat{L}_2^{(a)}(k_x, y, k_z) \\ 
  \hat{L}_3^{(a)}(k_x, y, k_z) 
  \end{bmatrix} =
  \begin{bmatrix} 
  \langle \hat{a}(k_x, y, k_z) \hat{E}_1^*(k_x, k_z) \rangle \\ 
  \langle \hat{a}(k_x, y, k_z) \hat{E}_2^*(k_x, k_z) \rangle \\ 
  \langle \hat{a}(k_x, y, k_z) \hat{E}_3^*(k_x, k_z) \rangle 
  \end{bmatrix}$$
  where $\hat{(\cdot)}$ denotes the 2D spatial Fourier transform, $(\cdot)^*$ denotes complex conjugation, and $\langle \cdot \rangle$ represents ensemble averaging over snapshots.
- **Parameterization**:
  - Number of trainable/solvable transfer functions: $3 \times N_x \times N_z$ complex parameters per target field $a \in \{u, v, w\}$ per wall-normal slice $y$.
  - Exact Optimization Objective: Analytical $L_2$-norm minimization of expected mean-squared reconstruction error:
    $$\min_{\tilde{L}_{ij(s)}} \left\langle \left( u_i(y) - \tilde{L}_{ij(s)}(y) E_{j(s)} \right)^2 \right\rangle$$

---

## 3. Data Scaling & Normalization

- **Inner Unit Scaling (Wall Units Superscript '$+$')**:
  - Velocity scale: Friction velocity $u_\tau = \sqrt{\tau_w / \rho}$, where $\tau_w = \nu \rho \left. \frac{\partial U}{\partial y} \right|_{y=0}$.
  - Length scale: Viscous length scale $\delta_v = \frac{\nu}{u_\tau}$.
  - Wall-normal distance: $y^+ = \frac{y u_\tau}{\nu}$.
  - Wavelengths / Grid spacing: $\lambda_x^+ = \frac{\lambda_x u_\tau}{\nu}$, $\lambda_z^+ = \frac{\lambda_z u_\tau}{\nu}$, $\Delta x^+ = \frac{\Delta x u_\tau}{\nu}$, $\Delta z^+ = \frac{\Delta z u_\tau}{\nu}$.
  - Shears and Pressure: $\partial_y u^+ = \frac{\nu}{u_\tau^2} \frac{\partial u}{\partial y}$, $p^+ = \frac{p}{\rho u_\tau^2}$.
- **Outer Unit Scaling**:
  - Lengths scaled by channel half-height $h$: $y/h, \lambda_x/h, \lambda_z/h$.
  - Scaling collapse regimes: Buffer layer ($y^+ \le 20\text{--}100$) collapses in inner units; logarithmic layer ($150\nu/u_\tau < y \le 0.2h$) collapses in outer units.
- **Spatial Low-Pass Filtering Kernel**:
  To isolate reconstructible scales ($\ge 50\%$ accuracy threshold), target true fields are filtered via a 2D Gaussian kernel:
  $$G(x, z) = \left( \frac{2\pi}{\Delta_x \Delta_z} \right)^{1/2} \exp \left[ -\pi^2 \left( \frac{x^2}{\Delta_x^2} + \frac{z^2}{\Delta_z^2} \right) \right]$$
  Filter widths for logarithmic layer ($y/h = 0.1$): $\Delta_x \times \Delta_z = 4y \times 2y$ for $u$, and $2y \times 2y$ for $v$.

---

## 4. Required Physics Validation Gates

- **1. Fractional Spectral Error Gate $R_{ab}(k_x, y, k_z)$**:
  $$R_{ab}(k_x, y, k_z) = \frac{\text{Re} \left\langle (a - a^\dagger)(b - b^\dagger)^* \right\rangle (k_x, y, k_z)}{\text{Re} \langle a b^* \rangle (k_x, y, k_z)}$$
  - Metric requirement: $R_{ab}(k_x, y, k_z) < 0.5$ defines the boundary of reconstructible turbulent structures.
- **2. Linear Coherence Spectrum $\gamma_{ab}^2(k_x, y, k_z)$**:
  $$\gamma_{ab}^2(k_x, y, k_z) = \frac{\left| \text{Re}\langle a^\dagger (b^\dagger)^* \rangle (k_x, y, k_z) \right|^2}{\text{Re}\langle a a^* \rangle (k_x, y, k_z) \cdot \text{Re}\langle b b^* \rangle (k_x, y, k_z)}$$
  Relation to $R_{ab}$ for LSE: $R_{ab} = 1 - \gamma_{ab}^2$.
- **3. Reconstructed Energy Ratio $\beta_{ab}(y)$**:
  $$\beta_{ab}(y) = \frac{\sum_{k_x, k_z} \text{Re} \left\langle a^\dagger (b^\dagger)^* \right\rangle (k_x, y, k_z)}{\sum_{k_x, k_z} \text{Re} \left\langle a b^* \right\rangle (k_x, y, k_z)}$$
  - Validation Gate Targets:
    - $\beta_{uu}(y) \ge 0.5$ for $y/h \le 0.2$.
    - Tangential Reynolds stress recovery: $\beta_{uv}(y) \ge 0.5$ for $y/h \le 0.2$.
    - Cross-flow kinetic energy: $\beta_{vv}(y), \beta_{ww}(y) \ge 0.5$ maintained strictly within $y^+ \le 100$.
- **4. Incompressible Kinematic Constraints**: Reconstructed instantaneous velocity fields satisfy continuity $\nabla \cdot \mathbf{u}^\dagger = 0$ in physical space.

---

## 5. Architectural Innovations & Edge Cases

- **Single-Observable Reduced Operators**:
  To decouple the individual physics of each observable $E_s \in \{p, \partial_y u, \partial_y w\}$, reduced single-input transfer functions $\hat{L}_{i, s}(k_x, y, k_z)$ are computed via scalar systems:
  $$\langle \hat{E}_s \hat{E}_s^* \rangle (k_x, k_z) \, \hat{L}_{i, s}(k_x, y, k_z) = \langle \hat{u}_i(y) \hat{E}_s^* \rangle (k_x, k_z)$$
- **Pressure Decomposition & High-$Re_\tau$ Spectral Degradation**:
  Wall pressure $p(x,0,z)$ decomposes into inertial ($p_I$) and Stokes ($p_s$) components:
  $$\nabla^2 p_I = -\nabla \cdot (\mathbf{u} \cdot \nabla \mathbf{u}), \quad \left. \frac{\partial p_I}{\partial y} \right|_{y=0} = 0$$
  $$\nabla^2 p_s = 0, \quad \left. \frac{\partial p_s}{\partial y} \right|_{y=0} = \nu \left. \frac{\partial^2 v}{\partial y^2} \right|_{y=0}$$
  Stokes component is explicitly determined by wall shears via continuity:
  $$\hat{p}_s^+(0) = -i \frac{k_x^+ \widehat{\partial_y u}^+(0) + k_z^+ \widehat{\partial_y w}^+(0)}{|\mathbf{k}|^+}$$
  As $Re_\tau \to \infty$, the ratio $\hat{p}_s / \hat{p}_I \to 0$ for outer scales ($\lambda_x \sim h$). Single-observable models based strictly on pressure $v^\dagger_p$ lose performance at higher $Re_\tau$ due to contamination from $p_s$, whereas the full 3-observable model remains invariant to $Re_\tau$ scaling by using shear inputs to cancel $p_s$.
- **Forward-Tilted Spatial Kernels**:
  Physical-space reconstruction kernels $\tilde{L}_s^{(a)}(\Delta x, y, \Delta z)$ derived for shear observables exhibit a forward structural tilt in the streamwise direction at an angle of $10^\circ \text{--} 20^\circ$ relative to the wall, accounting for advective delay times $t_l \sim y / u_\tau$. Pressure kernels $\tilde{L}_p^{(a)}$ show zero spatial tilt along $\Delta x$ due to elliptic velocity-pressure coupling.
- **Coarse Sensor Discrete Aliasing**:
  Coarse spatial sampling at sensor intervals $(\Delta x_s, \Delta z_s)$ aliases high-wavenumber wall shear noise into low wavenumbers, severely degrading outer-layer estimations.
  - *Mitigation*: Physical spatial integration over finite rectangular sensor areas ($\Delta x_s \times \Delta z_s = 0.1h \times 0.05h$) combined with temporal low-pass filtering matching local turnover times ($t_l \approx y/u_\tau$).

---

## 6. Raw Data Corrections Log

- **Grid Size Parameter Reconstruction**: In Table I, $N_z = 108$ listed for case `F5300` is an extraction truncation of $N_z = 1084$ (or $1080$), based on the storage aspect ratio $(L_x, L_z) = (8\pi, 3\pi)$ and $N_x = 1024$.
- **Fourier Transform Operator Notation**: Standardized conjugate notation in equation (7) and (11) from text OCR artifacts ($\hat{E}_r^*$ and complex conjugates) to ensure proper power spectral density scaling.
- **Equation Reconstruction**:
  - Reconstructed Stokes pressure relation (17): $\widehat{p}_s^+(0) = -i \left[ k_x^+ \widehat{u}_y(0)^+ + k_z^+ \widehat{w}_y(0)^+ \right] / |k|^+$, where $u_y \equiv \partial_y u$ and $w_y \equiv \partial_y w$.
  - Reconstructed operator derivative identity (19): $-k_x^2 \langle \hat{p}^* \hat{p} \rangle \hat{L}_{\partial_{x}p}^{(u)} = i k_x \langle \hat{p}^* \hat{u} \rangle$.
- **Definition Clarification**: Reconstructed $a^\dagger$ and $E_s$ in Section III as zero-mean spatial fluctuation components to preserve consistency with ensemble cross-correlation tensors.