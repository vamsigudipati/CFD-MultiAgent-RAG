## 1. Physical Problem Statement

The framework solves an inverse data assimilation problem: inferring latent 2D/3D velocity $\mathbf{u} = (u, v, w)$ and pressure $p$ fields in arbitrary fluid domains solely from spatio-temporal observations of a passive scalar concentration $c(t, x, y, z)$.

### Governing Equations (Non-Dimensional)
1. **Passive Scalar Transport Equation**:
   $$e_1 := c_t + u c_x + v c_y + w c_z - \text{Pec}^{-1} (c_{xx} + c_{yy} + c_{zz}) = 0$$

2. **Auxiliary Complement Scalar Transport Equation** ($d := 1 - c$):
   $$e_2 := d_t + u d_x + v d_y + w d_z - \text{Pec}^{-1} (d_{xx} + d_{yy} + d_{zz}) = 0$$

3. **Incompressible Navier-Stokes Momentum Equations**:
   $$e_3 := u_t + u u_x + v u_y + w u_z + p_x - \text{Re}^{-1} (u_{xx} + u_{yy} + u_{zz}) = 0$$
   $$e_4 := v_t + u v_x + v v_y + w v_z + p_y - \text{Re}^{-1} (v_{xx} + v_{yy} + v_{zz}) = 0$$
   $$e_5 := w_t + u w_x + v w_y + w w_z + p_z - \text{Re}^{-1} (w_{xx} + w_{yy} + w_{zz}) = 0$$

4. **Incompressibility (Continuity) Condition**:
   $$e_6 := u_x + v_y + w_z = 0$$

### Flow Regimes & Physical Setup
* **2D Flow Past a Circular Cylinder (External)**: $\text{Re} = 100$, $\text{Pec} = 100$, $U_\infty = 1$, cylinder diameter $D = 1$, kinematic viscosity $\nu = 0.01$, diffusivity $\kappa = 0.01$. Passive scalar injected at inlet $x \in [-2.5, 2.5]$.
* **3D Flow Past a Finite Cylinder (External)**: $\text{Re} = 100$, $\text{Pec} = 100$, $D = 1$, confined between parallel plates $10D$ apart along the $z$-axis with an open wake.
* **2D Transient Channel Flow Over an Obstacle (Internal)**: $\text{Re} = 60$, $\text{Pec} = 180$, mean velocity $\bar{U} = 1$, channel height $H = 12$, $\nu = 1/60$, $\kappa = 1/180$. Pulsatile inflow profile $u(t)$.
* **3D Intracranial Aneurysm (ICA) Sac (Internal)**: Real-world pulsatile blood flow waveform $Q(t)$ in a patient-specific carotid artery sac, $\text{Re} = \text{Pec} = 98.2$.

---

## 2. Network Architectures

* **Topology**: Fully Connected Physics-Informed Neural Network (PINN).
* **Input Vector**: $(t, x, y, z) \in \mathbb{R}^4$ (or $(t, x, y) \in \mathbb{R}^3$ for 2D cases).
* **Output Vector**: $(c, d, u, v, w, p) \in \mathbb{R}^6$ (or $(c, d, u, v, p) \in \mathbb{R}^5$ for 2D cases).
* **Layer Configuration**: 10 hidden layers, 50 neurons per hidden layer per output variable (total 300 neurons per hidden layer for 6 output variables).
* **Activation Function**: Sinusoidal activation function $\sigma(x) = \sin(x)$ applied at all hidden layers.
* **Optimization & Training Protocols**:
  * **Optimizer**: Adam.
  * **Batch Size**: Mini-batch size of 10,000 spatial-temporal points.
  * **Learning Rate Schedule**:
    * Epochs 1–250: $\eta = 10^{-3}$
    * Epochs 251–750: $\eta = 10^{-4}$
    * Epochs 751–1000: $\eta = 10^{-5}$
  * **Execution Graph**: Static computational graph defined in TensorFlow; derivative evaluations ($\partial_t, \partial_x, \partial_y, \partial_z$) computed via reverse-mode Automatic Differentiation (AD).

---

## 3. Data Scaling & Normalization

* **Dimensional Reduction**:
  * Length scale: $x^* = x / D$ or $x / H$
  * Velocity scale: $\mathbf{u}^* = \mathbf{u} / U_\infty$ or $\mathbf{u} / \bar{U}$
  * Time scale: $t^* = t U / L$
  * Pressure scale: $p^* = p / (\rho U^2)$
  * Concentration: Normalized to $c \in [0, 1]$
* **Auxiliary Complement Transformation**: $d(t, x, y, z) = 1 - c(t, x, y, z)$ enforces implicit domain bounds without needing explicit geometric mesh parameterizations.
* **Inverse Parameter Identification**: $\text{Re}$ and $\text{Pec}$ are represented as trainable scalar variables in the computational graph when estimated as free physical parameters.

---

## 4. Required Physics Validation Gates

### Total Loss Objective Function (Sum of Squared Errors)
$$\mathcal{L}_{\text{total}} = \sum_{n=1}^N |c(t^n, x^n, y^n, z^n) - c^n|^2 + \sum_{n=1}^N |d(t^n, x^n, y^n, z^n) - d^n|^2 + \sum_{i=1}^6 \sum_{n=1}^N |e_i(t^n, x^n, y^n, z^n)|^2$$

### Quantitative Field & Derived Validation Metrics
1. **Field Reconstruction Error**: Relative $L^2$-norm error between predicted variables $(c, u, v, w, p)$ and DNS ground truth (computed via high-order spectral/hp-element solver NekTar).
2. **Integrated Hydrodynamic Surface Forces**:
   * **Lift Force ($F_L$)**:
     $$F_L = \oint \left[ -p n_y + 2\text{Re}^{-1} v_y n_y + \text{Re}^{-1} (u_y + v_x) n_x \right] \mathrm{d}s$$
   * **Drag Force ($F_D$)**:
     $$F_D = \oint \left[ -p n_x + 2\text{Re}^{-1} u_x n_x + \text{Re}^{-1} (u_y + v_x) n_y \right] \mathrm{d}s$$
3. **Wall Shear Stress (WSS)**:
   $$\text{WSS}(x, t) = \sqrt{\tau_x^2 + \tau_y^2}$$
   where:
   $$\tau_x = 2\text{Re}^{-1} \left[ u_x n_x + \frac{1}{2} (v_x + u_y) n_y \right], \quad \tau_y = 2\text{Re}^{-1} \left[ \frac{1}{2} (u_y + v_x) n_x + v_y n_y \right]$$
4. **Parameter Discovery Precision**:
   * **2D Cylinder**: $\text{Re}_{\text{learned}} = 92.47$ (7.52% error), $\text{Pec}_{\text{learned}} = 92.39$ (7.60% error).
   * **2D Obstacle Channel**: $\text{Re}_{\text{learned}} = 59.92$ (0.12% error), $\text{Pec}_{\text{learned}} = 178.95$ (0.58% error).

---

## 5. Architectural Innovations & Edge Cases

* **Auxiliary Variable Transformation ($d = 1 - c$)**: Implicitly conveys domain boundary wall conditions (where $c=0 \implies d=1$). This eliminates the requirement to enforce explicit no-slip velocity boundary conditions on complex physical boundaries.
* **Geometry- and BC-Agnostic Data Assimilation**: Model training does not require knowledge of inflow, outflow, or wall boundary conditions, operating strictly within arbitrary spatial crops where scalar concentration gradients $\nabla c \neq 0$ exist.
* **Analytic Stress Tensor Evaluation**: Velocity derivatives required for wall shear stress ($\text{WSS}$) and surface forces ($F_L, F_D$) are evaluated via exact analytical backpropagation through the network, preventing finite-difference discretization noise.
* **Temporal Edge Artifacts (Known Failure Mode)**: Significant error spikes occur at the initial ($t \to 0$) and final time boundaries ($t \to T_{\max}$) due to a lack of temporal padding in the training window.

---

## 6. Raw Data Corrections Log

1. **Equation (3) Typographical Error**:
   * *Extracted OCR*: $v_t + v v_x + v v_y + w v_z = -p_y + \text{Re}^{-1}(v_{xx} + v_{yy} + v_{zz})$
   * *Corrected Equation*: $v_t + u v_x + v v_y + w v_z = -p_y + \text{Re}^{-1}(v_{xx} + v_{yy} + v_{zz})$ (the convective velocity in the $x$-direction was misprinted as $v$ instead of $u$).
2. **Residual Network Equation (5) $e_4$ Corrected**:
   * *Extracted OCR*: $e_4 := v_t + v u_x + v v_y + w v_z + p_y - \text{Re}^{-1}(v_{xx} + v_{yy} + v_{zz})$
   * *Corrected Equation*: $e_4 := v_t + u v_x + v v_y + w v_z + p_y - \text{Re}^{-1}(v_{xx} + v_{yy} + v_{zz})$ (corrected convective term $v u_x \to u v_x$).
3. **Wall Shear Stress Component Formula Scaling**:
   * *Extracted Text*: $\tau_x = 2\text{Re} \left[ u_x n_x + \frac{1}{2} (v_x + u_y) n_y \right]$
   * *Corrected Formula*: $\tau_x = 2\text{Re}^{-1} \left[ u_x n_x + \frac{1}{2} (v_x + u_y) n_y \right]$ (the non-dimensional stress scale requires multiplication by dimensionless viscosity $1/\text{Re}$, not $\text{Re}$).