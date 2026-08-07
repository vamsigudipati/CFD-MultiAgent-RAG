## 1. Physical Problem Statement

The paper investigates physics-informed deep learning for continuous spatio-temporal super-resolution, reconstruction, and denoising of sparse, noisy flow-field measurements without high-resolution targets across four specific benchmarks:

1. **1D Burgers' Equation (Shock Formation):**
   - **Governing Equation:** 
     $$u_t + u u_x - \left(\frac{0.01}{\pi}\right) u_{xx} = 0, \quad x \in [-1, 1], \; t \in [0, 0.99]$$
   - **Boundary Conditions:** Dirichlet $u(t, -1) = u(t, 1) = 0$.
   - **Initial Condition:** $u(0, x) = -\sin(\pi x)$.
   - **Data Regimes:** Unsteady ill-posed interpolation using data constrained strictly at $t = 0.0$ and $t = 0.99$ ($N_s = 512$ points total across both time-steps).

2. **2D Cylinder Wake (Vortex Shedding):**
   - **Governing Equations:** $2\text{D}$ Incompressible Navier-Stokes:
     $$\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla) \mathbf{u} = -\nabla p + \frac{1}{Re_D} \nabla^2 \mathbf{u}, \quad \nabla \cdot \mathbf{u} = 0$$
   - **Parameters:** $Re_D = \frac{U_\infty D}{\nu} = 100$, domain $(x, y) \in \Omega$, time $t \in [0, 7]$ ($\approx 1$ shedding cycle).
   - **Data Downsampling:** Reference DNS grid $(N_x, N_y, N_t) = (100, 50, 200)$ with $\Delta t = 0.1$. Downsampled spatial resolution by $10\times$ in $x$ and $y$, restricted to 3 temporal snapshots ($t = 0.0, 3.5, 7.0$). $N_s = 150$ total supervised points ($0.14\%$ of full field).

3. **3D Minimal Turbulent Channel Flow:**
   - **Governing Equations:** $3\text{D}$ Incompressible Navier-Stokes equations at centerline Reynolds number $Re_{cl} = \frac{U_{cl} h}{\nu} = 5000$.
   - **Domain & Subdomain:** Full box size $(x_l, y_l, z_l) = (0.6\pi h, 2h, 0.18\pi h)$; evaluated subdomain $(x_d, y_d, z_d) = (0.6\pi h, h, 0.01125\pi h)$ over $t \in [0, 4]$.
   - **Data Downsampling:** Reference resolution $(N_x, N_y, N_z) = (32, 129, 16)$. Downsampled configurations: $(n_x, n_y, n_z) \in \{(8, 8, 2), (16, 16, 2)\}$ with non-uniform wall-normal spacing $\delta y$. Time resolution downsampled to 5 snapshots ($\Delta t = 1.0$) or 3 snapshots ($\Delta t = 2.0$).

4. **Experimental Turbulent Boundary Layer (Hot-Wire Anemometry - HWA):**
   - **Governing Equations:** $2\text{D}$ Incompressible Reynolds-Averaged Navier-Stokes (RANS) without molecular viscous terms (far-wall approximation):
     $$\bar{U} \frac{\partial \bar{U}}{\partial x} + \bar{V} \frac{\partial \bar{U}}{\partial y} = -\frac{\partial \bar{P}}{\partial x} - \frac{\partial \overline{u'^2}}{\partial x} - \frac{\partial \overline{u'v'}}{\partial y}$$
     $$\bar{U} \frac{\partial \bar{V}}{\partial x} + \bar{V} \frac{\partial \bar{V}}{\partial y} = -\frac{\partial \bar{P}}{\partial y} - \frac{\partial \overline{u'v'}}{\partial x} - \frac{\partial \overline{v'^2}}{\partial y}$$
     $$\frac{\partial \bar{U}}{\partial x} + \frac{\partial \bar{V}}{\partial y} = 0$$
   - **Flow Setup:** Inflow boundary layer over rough terrain for wind turbine arrays ($u_\tau = 0.48 \text{ m/s}$). Retained wall-normal spatial resolution reduced from 13 down to 7, 5, or 3 points across boundary layer height $\delta_{99}$.

---

## 2. Network Architectures

All configurations utilize Multi-Layer Perceptrons (MLPs) parameterized by weights $\mathbf{W}^i$ and biases $\mathbf{b}^i$, trained via reverse-mode Automatic Differentiation (`tf.GradientTape`).

```
  [ Input Coordinates ]
  (t, x, y, z) or (x, y)
          │
          ▼
  ┌──────────────────────────────┐
  │ Fully Connected MLP          │
  │ Activation: tanh             │
  │ Layers & Widths: Case-based  │
  └──────────────┬───────────────┘
                 │
                 ├───> Primary State Outputs: u, v, w, p, U, V, u'2, v'2, u'v'
                 │
                 ▼
  ┌──────────────────────────────┐
  │ Residual Network (AD Tape)   │
  │ Evaluates PDE Operators N[u] │
  └──────────────┬───────────────┘
                 │
                 ▼
  [ Loss Minimization L_s + L_e ]
```

### Precise Architectural Parameters:

1. **1D Burgers' Model:**
   - **Inputs:** $(t, x) \in \mathbb{R}^2$
   - **Outputs:** $u \in \mathbb{R}^1$
   - **Topology:** 8 hidden layers, 20 neurons/layer.
   - **Activation:** Hyperbolic Tangent ($\tanh$).

2. **2D Cylinder Wake Model:**
   - **Inputs:** $(t, x, y) \in \mathbb{R}^3$
   - **Outputs:** $(u, v, p) \in \mathbb{R}^3$
   - **Topology:** 4 hidden layers, 20 neurons/layer.
   - **Activation:** Hyperbolic Tangent ($\tanh$).

3. **3D Minimal Turbulent Channel Model:**
   - **Inputs:** $(t, x, y, z) \in \mathbb{R}^4$
   - **Outputs:** $(u, v, w, p) \in \mathbb{R}^4$
   - **Topology:** 10 hidden layers, 100 neurons/layer.
   - **Activation:** Hyperbolic Tangent ($\tanh$).

4. **Experimental HWA Boundary Layer Model:**
   - **Inputs:** $(x, y) \in \mathbb{R}^2$
   - **Outputs:** $(\bar{U}, \bar{V}, \overline{u'^2}, \overline{v'^2}, \overline{u'v'}, \bar{P}) \in \mathbb{R}^6$
   - **Topology:** 4 hidden layers, 40 neurons/layer.
   - **Activation:** Hyperbolic Tangent ($\tanh$).

### Training Pipeline & Optimization Protocol:
- **Optimizer:** Two-stage full-batch optimization pipeline.
  - Stage 1: Adam optimizer for $1,000$ epochs with learning rate $\eta = 1 \times 10^{-3}$.
  - Stage 2: Limited-memory Broyden-Fletcher-Goldfarb-Shanno (L-BFGS) algorithm, terminating on machine-precision increment tolerance.

---

## 3. Data Scaling & Normalization

### 1. Spatial & Temporal Non-Dimensionalization:
- **Cylinder Flow:** Coordinates and velocities scaled by cylinder diameter $D$ and freestream velocity $U_\infty$. $t = \frac{t^* U_\infty}{D}$.
- **Turbulent Channel Flow:** Length scaled by channel half-height $h$, velocity scaled by laminar centerline velocity $U_{cl}$.
  - Inner Viscous Scaling: Viscous length $l^* = \frac{\nu}{u_\tau}$, viscous time $t^* = \frac{\nu}{u_\tau^2}$.
  - Spatial separations for DNS: $\delta x^+ = 11.90$, $\min \delta y^+ = 0.06$, $\max \delta y^+ = 4.95$, $\delta z^+ = 7.14$, $\delta t^+ = 1.63$.
  - Spatial separations for downsampled cases (`PINN-t3-s8`): $\delta x^+ = 47.60$, $\min \delta y^+ = 1.94$, $\max \delta y^+ = 39.22$, $\delta z^+ = 7.14$, $\delta t^+ = 16.32$.
- **Experimental HWA Data:** Quantities scaled in inner units $\phi^+$ via friction velocity $u_\tau = 0.48 \text{ m/s}$ based on log-law fitting.

### 2. Synthetic Noise Injection:
- **Flow Field Multiplicative Gaussian Noise (Cylinder & Channel):**
  $$\hat{Q}_l = Q_l \cdot (\mathbf{I} + c \boldsymbol{\epsilon})$$
  where $Q_l$ is the downsampled exact velocity vector, $\boldsymbol{\epsilon} \sim \mathcal{N}(0, \mathbf{I})$, $\mathbf{I}$ is the identity matrix, and noise level $c \in \{0.025, 0.05, 0.10\}$.
- **Experimental Profile Additive Gaussian Noise (HWA):**
  Adjusted via the $3\sigma$ rule on inner-scaled quantities $\phi^+$:
  $$\sigma = \frac{N}{100} \cdot \frac{\phi^+}{3}$$
  where noise level $N \in \{2\%, 5\%, 8\%\}$.

---

## 4. Required Physics Validation Gates

The validation suite enforces strict numerical error metrics and turbulent spectral density gates:

1. **Relative Euclidean Error Norm ($\epsilon_\phi$):**
   $$\epsilon_\phi = \left\langle \frac{\|\tilde{\phi} - \phi\|^2}{\|\phi\|^2} \right\rangle$$
   where $\tilde{\phi}$ is the network inference, $\phi$ is the high-resolution target/reference, $\|\cdot\|$ denotes the $L_2$ norm, and $\langle \cdot \rangle$ represents temporal averaging.

2. **Cross-Correlation Coefficient ($r_\phi$):**
   $$r_\phi = \frac{\sum_{i=1}^n (\tilde{\phi}_i - \bar{\tilde{\phi}})(\phi_i - \bar{\phi})}{\sqrt{\sum_{i=1}^n (\tilde{\phi}_i - \bar{\tilde{\phi}})^2 \sum_{i=1}^n (\phi_i - \bar{\phi})^2}}$$

3. **POD Mode Temporal Coefficients Reconstruction ($a_i(t)$):**
   Projection of inferred velocity snapshot onto POD modes computed from full reference datasets:
   $$a_i(t) = \int_{\Omega} \mathbf{u}(t, \mathbf{x}) \cdot \boldsymbol{\psi}_i(\mathbf{x}) \, d\mathbf{x}$$
   Validation requires tracking coefficients for high-frequency modes (e.g., modes 3, 5, 7) across time.

4. **1D Premultiplied Power Spectral Density (PSD):**
   Inner-scaled streamwise $1\text{D}$ premultiplied PSD at $y^+ = 30$:
   $$k_x E_{\phi\phi}(k_x) \quad \text{vs.} \quad \lambda_x^+ = \frac{2\pi}{k_x l^*}$$
   Validation threshold: PINN reconstruction must retain spectral match down to small-scale cutoff wavelengths ($\lambda_x^+ \ge 51.0$ for $u$, $\lambda_x^+ \ge 39.7$ for $v$, and $\lambda_x^+ \ge 32.4$ for $w$).

---

## 5. Architectural Innovations & Edge Cases

### 1. Hybrid Loss Formulation & Weighting Schedule:
The optimization objective combines supervised measurement loss $L_s$ and unsupervised PDE residual loss $L_e$:
$$L = \alpha L_s + \beta L_e$$
$$L_s = \frac{1}{N_s} \sum_{i=1}^{N_s} |\mathbf{u}_s^i - \mathbf{u}(t_s^i, \mathbf{x}_s^i)|^2$$
$$L_e = \frac{1}{N_e} \sum_{i=1}^{N_e} |e(t_e^i, \mathbf{x}_e^i)|^2$$

- **Hyperparameter Weight Allocations ($\alpha, \beta$):**
  - Burgers' Equation: $\alpha = 1, \beta = 1$
  - 2D Cylinder Wake: $\alpha = 1, \beta = 10$ ($N_s = 150, N_e = 2000$)
  - Minimal Channel Flow: $\alpha = 1, \beta = 1$ ($N_e = 2000$)
  - Experimental HWA Profiles: $\alpha = 10, \beta = 1$ ($N_s \in \{3, 5, 7\}, N_e = 50$)

### 2. Unsupervised Pressure Recovery from Sparse Velocity Inputs:
Pressure $p$ (or $\bar{P}$) is never supplied as a training target ($p$ is absent in $L_s$). It is inferred as a continuous hidden fluid state constrained purely by forcing the momentum PDE residual $L_e \to 0$.

### 3. Mean Pressure Constant Shift Post-Processing:
Because incompressible Navier-Stokes equations determine pressure up to an arbitrary spatial constant, evaluation of pressure error $\epsilon_p$ requires shifting the predicted mean pressure to match the reference spatial mean:
$$\tilde{p}_{\text{shifted}}(\mathbf{x}, t) = \tilde{p}(\mathbf{x}, t) - \bar{\tilde{p}} + \bar{p}_{\text{reference}}$$

---

## 6. Raw Data Corrections Log

| Log Item | Original Extraction / Location | Correction / Inferred Parameter | Reason / Justification |
| :--- | :--- | :--- | :--- |
| **01** | Section 2.2.1, text notation $u^t$ | Reconstructed as temporal derivative $\mathbf{u}_t$ or $\frac{\partial \mathbf{u}}{\partial t}$ | Broken superscript OCR rendering of time-derivative subscript notation. |
| **02** | Section 4, Figure 11 Schematic | Reconstructed scalar system of 2D Inviscid RANS equations for mean profile $(\bar{U}, \bar{V}, \bar{P})$ and stresses $(\overline{u'^2}, \overline{v'^2}, \overline{u'v'})$ | Unlabeled diagram details restored into concrete analytical LaTeX expressions. |
| **03** | Appendix A.2, Table A4 Column 1 & 2 headers | Inverted entry restored: $l = 10, n = 100$ | Table A4 printed $l=100, n=10$ in header due to a LaTeX source column swap, contradicting text in Appendix A.2 and Table A3 ($l=10$ layers, $n=100$ neurons). |
| **04** | Section 3.2, Burgers' Equation parameter | Viscosity parameter $\nu = \frac{0.01}{\pi}$ explicitly written | Explicit expansion of $0.01/\pi$ coefficient in momentum equation. |