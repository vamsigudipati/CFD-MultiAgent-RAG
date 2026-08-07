## 1. Physical Problem Statement

* **Governing Equations**: 3D Unsteady Compressible Navier-Stokes equations in conservative form for a Newtonian fluid and ideal gas equation of state:
  $$\frac{\partial \rho}{\partial t} + \frac{\partial (\rho u_j)}{\partial x_j} = 0$$
  $$\frac{\partial (\rho u_i)}{\partial t} + \frac{\partial (\rho u_i u_j + p \delta_{ij})}{\partial x_j} = \frac{\partial \sigma_{ij}}{\partial x_j}, \quad i=1,2,3$$
  $$\frac{\partial (\rho e)}{\partial t} + \frac{\partial [(\rho e + p) u_j]}{\partial x_j} = -\frac{\partial q_j}{\partial x_j} + \frac{\partial (\sigma_{ij} u_i)}{\partial x_j}$$
  $$\rho e = \rho \left( \frac{1}{2} u_i u_i + c_v T \right)$$

* **Flow Regime & Domain**:
  * **Flow Case**: Decaying Homogeneous Isotropic Turbulence (DHIT).
  * **Reynolds Number**: $Re_\lambda \approx 180$ based on Taylor micro-scale at the onset of exponential energy decay ($T^* \approx 0.5 T_{\text{eddy}}$).
  * **Mach Number**: $M_{\max} = 0.1$ (weakly compressible).
  * **Domain**: 3D Periodic Box $\Omega = [0, 2\pi]^3$.
  * **Initial Spectrum**: $E(k, t=0) = \frac{1}{2} a_s u_0^2 k_p^{-1} \left( \frac{k}{k_p} \right)^s \exp \left[ -\frac{1}{2} s \left( \frac{k}{k_p} \right)^2 \right]$ with $s=4$, $u_0^2=5$, $k_p=4$.

* **Discretization & Grid Schemes**:
  * **DNS Reference**: Discontinuous Galerkin Spectral Element Method (DGSEM), $64^3$ cubical elements with tensor-product polynomial basis of degree $N=7$ ($P^7$, 8 LGL points per direction, $512^3$ total DOFs).
  * **LES Target Grid**: Coarsened by $8\times$ per spatial dimension to $8^3 = 512$ cubical elements; polynomial degree $N=5$ ($P^5$, $p = N+1 = 6$ LGL points per direction, $6^3 = 216$ DOFs per element).
  * **LES Operators**: Kinetic-energy-preserving DGSEM with skew-symmetric flux splitting on LGL nodes, low-dissipation Roe Riemann solver for inviscid fluxes, Bassi-Rebay 1 (BR1) for viscous fluxes.
  * **Time Integration**: 3rd-order Adams-Bashforth scheme with $\Delta t = 4 \times 10^{-5} T^*$ ($\text{CFL} \approx 0.2$).

* **Perfect LES Subgrid Operator-Filtered Closure**:
  $$\frac{\partial \bar{U}}{\partial t} + \tilde{R}(F(\bar{U})) = \tilde{R}(F(\bar{U})) - \overline{R(F(U))}$$
  where $\bar{U}$ is the $L_2$-projected DNS solution on the LES grid, $R(F(U))$ is the DNS spatial divergence operator, and $\tilde{R}(F(\bar{U}))$ is the discretized coarse-grid LES spatial operator. The learning target maps coarse features to the filtered DNS flux derivative $\overline{R(F(U))}$ for the 3 momentum components.

---

## 2. Network Architectures

* **Topology**: Deep 3D Residual Neural Network (3D-RNN) operating on local volumetric DG element patches ($p \times p \times p$).
* **Input Feature Tensor ($\hat{X}$)**: Shape $\mathbb{R}^{6 \times p \times p \times p}$ ($p=6$ LGL points/direction):
  $$\hat{X} = \left( \bar{u}, \bar{v}, \bar{w}, \tilde{R}(F(\bar{U}^1)), \tilde{R}(F(\bar{U}^2)), \tilde{R}(F(\bar{U}^3)) \right)$$
* **Output Label Tensor ($\hat{Y}$)**: Shape $\mathbb{R}^{3 \times p \times p \times p}$:
  $$\hat{Y} = \left( \overline{R(F(U^1))}, \overline{R(F(U^2))}, \overline{R(F(U^3))} \right)$$

* **Detailed Layer Configuration (RNN-d)**:
  1. **Input Layer**: Pre-processed volumetric tensor $\mathbb{R}^{N_{batch} \times 6 \times p \times p \times p}$.
  2. **Initial Convolution**: 3D Conv ($k=3\times 3\times 3$, $n_f=16$ filters, padding='same') $\rightarrow$ Batch Normalization $\rightarrow$ ReLU.
  3. **Residual Tower ($d$ Residual Blocks)**:
     For block $l = 1, \dots, d$:
     * Path A (Non-linear Residual $F(x)$):
       * 3D Conv ($k=3\times 3\times 3$, $n_f=16$, padding='same') $\rightarrow$ Batch Normalization $\rightarrow$ ReLU
       * 3D Conv ($k=3\times 3\times 3$, $n_f=32$, padding='same') $\rightarrow$ Batch Normalization
     * Path B (Identity Shortcut $h(x)$):
       * Channel projection via 3D Conv ($k=1\times 1\times 1$, $n_f=32$) to match output dimension if $n_{f,in} \neq n_{f,out}$.
     * Combine: $A^l = \text{ReLU}(F(A^{l-1}) + h(A^{l-1}))$.
  4. **Compression / Output Head**:
     * 3D Conv ($k=1\times 1\times 1$, $n_f=32$) $\rightarrow$ Batch Normalization $\rightarrow$ ReLU
     * 3D Conv ($k=1\times 1\times 1$, $n_f=16$) $\rightarrow$ Batch Normalization $\rightarrow$ ReLU
     * 3D Conv ($k=1\times 1\times 1$, $n_f=3$) $\rightarrow$ Linear activation.

* **Evaluated Variants**:
  * `RNN0`: $d=0$ residual blocks.
  * `RNN1`: $d=1$ residual block.
  * `RNN4`: $d=4$ residual blocks.
  * `RNN8`: $d=8$ residual blocks.
  * `MLP100` (Baseline): Point-to-point Multilayer Perceptron with 1 hidden layer of 100 neurons.

---

## 3. Data Scaling & Normalization

* **Dataset Generation & Size**:
  * 20 independent DNS runs with randomized initial velocity phases.
  * Train/Val/Test Split: 18 runs (Training) / 1 run (Validation) / 1 run (Hidden Test).
  * Time Sampling: 11 snapshots per run spanning $t \in [1.0 T^*, 2.0 T^*]$ at intervals $\Delta t_{sample} = 0.1 T^*$.
  * Total Elements: $n_{runs} \times n_{samples} \times n_{elems} = 18 \times 11 \times 512 = 101,376$ element tensors per feature channel.

* **Data Augmentation**:
  Tripling training size to $304,128$ samples via spatial cyclic coordinate/vector rotation:
  $$\hat{x}^{(1)} = (\bar{u}, \bar{v}, \bar{w}, \tilde{R}_1, \tilde{R}_2, \tilde{R}_3)$$
  $$\hat{x}^{(2)} = (\bar{v}, \bar{w}, \bar{u}, \tilde{R}_2, \tilde{R}_3, \tilde{R}_1)$$
  $$\hat{x}^{(3)} = (\bar{w}, \bar{u}, \bar{v}, \tilde{R}_3, \tilde{R}_1, \tilde{R}_2)$$

* **Loss Function & Quadrature Mass Weighting**:
  Loss re-weighted by local DG LGL mass matrix $w_{\text{LGL}} \in \mathbb{R}^{p \times p \times p}$ (tensor product of 1D LGL weights $w_i w_j w_k$) to eliminate metric Jacobian bias:
  $$C = \frac{1}{N_{batch}} \sum_{m=1}^{N_{batch}} \sum_{n=1}^{3} \sum_{i,j,k=0}^{p-1} w_{\text{LGL}, ijk} \left( \hat{y}_{m, n, ijk} - y_{m, n, ijk} \right)^2$$

* **Optimization Parameters**:
  * Optimizer: Adam ($\beta_1 = 0.9, \beta_2 = 0.999$).
  * Batch Size: Mini-batch size $N_{batch} \approx 250$.
  * Training Duration: 50 epochs ($\approx 60,000$ iterations).
  * Layer Normalization: Batch Normalization applied post-convolution across mini-batches.

---

## 4. Required Physics Validation Gates

* **Cross-Correlation Metrics ($\mathcal{CC}$)**:
  $$\mathcal{CC}(a, b) = \frac{\sum_i (a_i - \bar{a})(b_i - \bar{b})}{\sqrt{\sum_i (a_i - \bar{a})^2} \sqrt{\sum_i (b_i - \bar{b})^2}}$$
  * Gate 1 (Global Correlation): $\mathcal{CC} > 0.45$ across full element domain (Achieved $\mathcal{CC} \approx 0.477$ for `RNN8`).
  * Gate 2 (Inner Tensor Element Correlation): $\mathcal{CC}_{\text{inner}} > 0.70$ evaluated on interior nodes $i,j,k \in [1, p-2]^3$ (Achieved $\mathcal{CC}_{\text{inner}} \approx 0.766$ for `RNN4`).
  * Gate 3 (Boundary Surface Correlation): $\mathcal{CC}_{\text{surf}}$ monitored on element boundary faces ($i,j,k \in \{0, p-1\}$) (Achieved $\mathcal{CC}_{\text{surf}} \approx 0.29 - 0.34$).

* **Dissipative Energy Validation ($\partial e$)**:
  Integrated dissipation error computed over mini-batch domain $\Omega^{mb}$:
  $$\partial e = \frac{\int_{\Omega^{mb}} \left( \overline{R(U)}^{\text{ANN}} - \overline{R(U)} \right) \cdot \bar{U} \, d\Omega}{\int_{\Omega^{mb}} \overline{R(U)} \cdot \bar{U} \, d\Omega}$$
  * Requirement: $\partial e > 0$ and $\partial e \sim \mathcal{O}(10^{-1})$, proving net dissipation without unnatural energy growth.

* **A Posteriori Online LES Validation**:
  * Kinetic Energy Decay Curve $K(t) = \frac{1}{2|\Omega|} \int_\Omega \bar{u}_i \bar{u}_i \, d\Omega$.
  * Kinetic Energy Spectrum $E(k, t)$ at cut-off frequencies. Must eliminate high-wavenumber energy pile-up present in no-model LES without over-damping mid-range modes (outperforming standard Smagorinsky $C_s=0.17$).

---

## 5. Architectural Innovations & Edge Cases

* **Operator-Aware Feature Space**:
  Including the discretized coarse-grid spatial operator $\tilde{R}(F(\bar{U}))$ in tandem with velocity fields $(\bar{u}, \bar{v}, \bar{w})$ increases offline prediction correlation from $\mathcal{CC} \approx 0.36$ to $\mathcal{CC} \approx 0.47$. This forces the network to learn both approximate subgrid scale deconvolution and numerical discretization error cancellation simultaneously.

* **Instability of Direct Network Evaluation in ODEs**:
  Direct insertion of the ANN predictions $\bar{R}^{\text{ANN}}$ into the governing equations ($\frac{\partial \bar{U}}{\partial t} = -\overline{R(F(U))}^{\text{ANN}}$) cancels out the discrete spatial operator $\tilde{R}$. Accumulation of high-frequency spatial aliasing errors causes blow-up over long temporal integration horizons despite positive net dissipation.

* **Data-Adaptive Eddy Viscosity Translation ($\mu_{\text{ANN}}$)**:
  To stabilize online deployments, the high-dimensional tensor output is projected via a zero-bias scalar least-squares optimization onto the viscous flux discretization operator:
  $$\tilde{R}(F(\bar{U}^i)) - \overline{R(F(U^i))}^{\text{ANN}} \approx \mu_{\text{ANN}} \tilde{R}\left(F^{\text{visc}}(\bar{U}^i, \nabla \bar{U}^i)\right)$$
  $$\mu_{\text{ANN}} = \mathcal{L}\left( \frac{\tilde{R}(F(\bar{U}^i)) - \overline{R(F(U^i))}^{\text{ANN}}}{\tilde{R}\left(F^{\text{visc}}(\bar{U}^i, \nabla \bar{U}^i)\right)} \right)$$

* **Physical Viscosity Bounding (Clipping Rule)**:
  To accommodate localized backscatter without inducing numerical divergence, $\mu_{\text{ANN}}$ is bounded element-wise:
  $$\mu_{\text{ANN, limit}} = \min\left( \max\left( \mu_{\text{ANN}}, -\mu_0 \right), 20\mu_0 \right)$$
  where $\mu_0$ is the dynamic physical fluid viscosity.

---

## 6. Raw Data Corrections Log

* **Equation (2.1)**: Reconstructed inline Kronecker delta notation $`deltaij` \rightarrow \delta_{ij}$ and spatial derivative $\frac{\partial \sigma_{ij}}{\partial x_j}$.
* **Equation (2.6)**: Corrected broken spatial and temporal closure bracket underbraces disrupted during OCR parsing:
  $$\text{Spatial Closure: } \tilde{R}(F(\bar{U})) - \overline{R(F(U))}, \quad \text{Temporal Closure: } \frac{\partial \bar{U}}{\partial t} - \overline{\frac{\partial U}{\partial t}}$$
* **Equation (2.10) & (2.11)**: Reconstructed distorted tensor dimensions and indexing bounds:
  $$\hat{Y} \in \mathbb{R}^{3 \times p \times p \times p}, \quad \hat{X} \in \mathbb{R}^{6 \times p \times p \times p}$$
  Inferred grid indexing range $i,j,k = 0, \dots, p-1$ with $p = N+1 = 6$. Corrected sample count product $n_{runs} \times n_{samples} \times n_{elems} = 18 \times 11 \times 8^3$.
* **Section 4.3 / Equation (4.2)**: Reconstructed vector-valued linear least squares expression for $\mu_{\text{ANN}}$ and operator-only viscosity $\mu_{\text{OP}}$, which suffered missing numerator/denominator fraction formatting in the raw text extract.
* **Table 1 & Table 4**: Fixed corrupted character strings where vector components were split across line breaks (e.g., $R e ( F ( U 1 )) \rightarrow \tilde{R}(F(\bar{U}^1))$).