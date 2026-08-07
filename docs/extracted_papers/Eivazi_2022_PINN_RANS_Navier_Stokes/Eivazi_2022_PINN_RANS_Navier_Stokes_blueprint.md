## 1. Physical Problem Statement

The goal is to solve the 2D incompressible Reynolds-Averaged Navier–Stokes (RANS) and Navier–Stokes equations without explicit turbulence closure models or eddy-viscosity assumptions, relying solely on domain boundary data and PDE residual constraints.

### Governing Equations (2D Incompressible RANS)
- **Continuity Residual ($\epsilon_1$):**
  $$\epsilon_1 = \frac{\partial U}{\partial x} + \frac{\partial V}{\partial y} = 0$$

- **Streamwise Momentum Residual ($\epsilon_2$):**
  $$\epsilon_2 = U \frac{\partial U}{\partial x} + V \frac{\partial U}{\partial y} + \frac{1}{\rho} \frac{\partial P}{\partial x} - \nu \left( \frac{\partial^2 U}{\partial x^2} + \frac{\partial^2 U}{\partial y^2} \right) + \frac{\partial \overline{u^2}}{\partial x} + \frac{\partial \overline{uv}}{\partial y} = 0$$

- **Wall-Normal Momentum Residual ($\epsilon_3$):**
  $$\epsilon_3 = U \frac{\partial V}{\partial x} + V \frac{\partial V}{\partial y} + \frac{1}{\rho} \frac{\partial P}{\partial y} - \nu \left( \frac{\partial^2 V}{\partial x^2} + \frac{\partial^2 V}{\partial y^2} \right) + \frac{\partial \overline{uv}}{\partial x} + \frac{\partial \overline{v^2}}{\partial y} = 0$$

### Evaluated Flow Regimes & Boundary Conditions
1. **Falkner–Skan Boundary Layer (FSBL):**
   - Regime: Laminar, $Re = 100$, adverse pressure gradient parameter $m = -0.08$, $\beta_{\text{FS}} = \frac{2m}{m+1} = -0.1739$.
   - Boundary condition: Velocity vector $(U, V)$ provided on boundaries.
2. **Zero-Pressure-Gradient (ZPG) Turbulent Boundary Layer:**
   - Regime: Incompressible turbulent flow, $1000 < Re_\theta < 7000$.
   - Governing set: $\{\epsilon_1, \epsilon_2\}$, output set: $\{U, V, \overline{uv}\}$.
3. **Adverse-Pressure-Gradient (APG) Turbulent Boundary Layer:**
   - Regime: Incompressible turbulent flow, $910 < Re_\theta < 3360$, Clauser parameter $\beta = \frac{\delta^*}{\tau_w} \frac{dP_\infty}{dx} \approx 1.0$.
   - Governing set: $\{\epsilon_1, \epsilon_2, \epsilon_3\}$, output set: $\{U, V, P, \overline{uv}\}$.
4. **NACA4412 Airfoil (Suction Side):**
   - Regime: Turbulent boundary layer at chord Reynolds number $Re_c = \frac{U_\infty c}{\nu} = 200,000$, domain $0.5 \le x/c \le 1.0$.
   - Inputs: Curved wall-normal coordinate system $(x^n, y^n)$. Output set: $\{U, V, P, \overline{u^2}, \overline{uv}, \overline{v^2}\}$.
5. **Periodic Hill:**
   - Regime: Separated turbulent flow at $Re_b = \frac{U_b H}{\nu} = 2,800$, domain $1.0 \le x/H \le 5.0$.
   - Boundary condition: No-slip $(U=0, V=0, \text{Reynolds stresses}=0)$ on top/bottom walls. Mean profiles and pressure provided at inlet/outlet boundaries.

---

## 2. Network Architectures

### Primary Model Architecture
- **Topology:** Fully Connected Neural Network (FNN / MLP).
- **Depth & Width:** 8 hidden layers, 20 neurons per hidden layer across all benchmark cases.
- **Activation Functions:** Hyperbolic tangent ($\tanh$) for all hidden layers; identity linear activation for output layer.
- **Input Dimensions:** 2 ($x, y$) or wall-normal aligned coordinates ($x^n, y^n$).
- **Output Dimensions:** 3 to 6 field variables depending on the test case:
  $$\hat{\mathbf{Y}} = [U, V, P, \overline{u^2}, \overline{uv}, \overline{v^2}]^T$$

```
Input (x, y) [2] ---> [ FC: 20, tanh ] x 8 ---> Output [3 to 6]
                            |
                     (Automatic Diff)
                            |
                     [ Residual Loss L_e ]
```

### Loss Function Formulation
The total loss function $L$ balances boundary data fit ($L_b$) and domain residual adherence ($L_e$):

$$L = L_e + L_b$$

$$L_e = \frac{1}{N_e} \sum_{i=1}^{M} \sum_{n=1}^{N_e} \left| \epsilon_i^n \right|^2$$

$$L_b = \frac{1}{N_b} \sum_{n=1}^{N_b} \left\| \mathbf{U}_b^n - \tilde{\mathbf{U}}_b^n \right\|_2^2$$

- $N_b$: Number of supervised boundary points.
- $N_e$: Number of residual evaluation points distributed across the interior domain and boundaries.
- $M$: Number of active PDE residual equations ($M=3$ for full 2D RANS).
- $\mathbf{U}_b^n$: Target reference vector at boundary point $n$.
- $\tilde{\mathbf{U}}_b^n$: PINN predicted vector at boundary point $n$.

---

## 3. Data Scaling & Normalization

- **Spatial Normalization:**
  - FSBL / ZPG / APG: Boundary layer domain lengths scaled by momentum thickness $\theta$ or local boundary layer scales.
  - NACA4412: Coordinates normalized by chord length $c$ ($x/c \in [0.5, 1.0]$) and transformed to body-fitted wall-normal coordinates $(x^n, y^n)$.
  - Periodic Hill: Normalized by crest height $H$ ($x/H \in [1.0, 5.0]$).
- **Inner-Scale Velocity & Stress Transformations (for validation/loss evaluation):**
  - Inner velocity scaling: $U^+ = \frac{U}{u_\tau}$
  - Inner spatial scaling: $y^+ = \frac{y}{\ell^*}$ where $\ell^* = \frac{\nu}{u_\tau}$
  - Inner stress scaling: $\tau_{ij}^+ = \frac{\overline{u_i u_j}}{u_\tau^2}$
  - Friction velocity: $u_\tau = \sqrt{\frac{\tau_w}{\rho}}$ where $\tau_w = \mu \left. \frac{\partial U}{\partial y} \right|_{y=0}$

---

## 4. Required Physics Validation Gates

Validation is performed globally against DNS / high-resolution LES reference datasets using relative $L_2$-norm error metrics:

$$E_i = \frac{\|\mathbf{U}_i - \tilde{\mathbf{U}}_i\|_2}{\|\mathbf{U}_i\|_2} \times 100\%$$

### Validation Targets & Achieved Baseline Errors
1. **Falkner–Skan Boundary Layer:**
   - $E_U = 0.07\%$, $E_V = 0.12\%$, $E_P = 0.001\%$.
2. **ZPG Turbulent Boundary Layer:**
   - $E_U = 1.02\%$, $E_V = 4.25\%$, $E_{\overline{uv}} = 6.46\%$.
3. **APG Turbulent Boundary Layer:**
   - $E_U = 0.28\%$, $E_V = 1.57\%$, $E_P = 4.60\%$, $E_{\overline{uv}} = 7.96\%$.
4. **NACA4412 Airfoil:**
   - $E_U = 1.56\%$, $E_V = 2.17\%$, $E_P = 7.30\%$, $E_{\overline{u^2}} = 9.43\%$, $E_{\overline{uv}} = 11.36\%$, $E_{\overline{v^2}} = 4.69\%$.
5. **Periodic Hill:**
   - $E_U = 2.77\%$, $E_V = 19.70\%$, $E_P = 8.61\%$, $E_{\overline{u^2}} = 28.18\%$, $E_{\overline{uv}} = 16.70\%$, $E_{\overline{v^2}} = 20.24\%$.

### Derived Physical Consistency Gates
- **Shape Factor Integrity:** $H_{12} = \frac{\delta^*}{\theta}$ matching reference DNS across $Re_\theta$.
- **Skin Friction Tracking:** $c_f = 2 \left( \frac{u_\tau}{U_\infty} \right)^2$ matching profile progression.
- **Separation & Reattachment:** Accurate identification of the recirculation zone and reattachment location $x/H$ for periodic hill flow via streamlines of $U$ and $V$.

---

## 5. Architectural Innovations & Edge Cases

1. **Unclosed RANS System Resolution:**
   - Rather than closing RANS via traditional Boussinesq or transport-equation turbulence models ($k-\epsilon$, $k-\omega$, SST), the neural network treats the Reynolds stresses ($\overline{u^2}, \overline{uv}, \overline{v^2}$) as independent co-outputs constrained strictly by boundary values and the underdetermined differential equations via Automatic Differentiation.
2. **Two-Stage Optimization Strategy:**
   - Training utilizes initial global optimization via the **Adam** optimizer, followed by fine-tuning with the quasi-Newton **L-BFGS** (Broyden–Fletcher–Goldfarb–Shanno) algorithm until increment tolerance is reached.
3. **Boundary Data Minimization:**
   - Training relies exclusively on supervised boundary points ($N_b$), treating the interior field completely unsupervised ($N_e$) where field predictions are constrained solely through automatic differentiation of the embedded differential equations.
4. **Coordinate Transformation for Complex Geometries:**
   - Airfoil cases utilize body-fitted wall-normal coordinates $(x^n, y^n)$ directly as network inputs to account for surface curvature.

---

## 6. Raw Data Corrections Log

| Source Text / OCR Error | Correction / Reconstruction | Reason / Justification |
| :--- | :--- | :--- |
| `U^n_b = [U n b , V^n b , P^n b , u 2 n b , uv^n b , v 2 n b T` | $\mathbf{U}_b^n = [U_b^n, V_b^n, P_b^n, \overline{u^2}_b^n, \overline{uv}_b^n, \overline{v^2}_b^n]^T$ | Malformed vector syntax and subscript/superscript formatting from OCR text extraction. |
| `u 2`, `uv`, `v 2` | $\overline{u^2}$, $\overline{uv}$, $\overline{v^2}$ | Restored standard fluid dynamics mathematical notation for kinematic Reynolds stress components. |
| Missing explicit form of RANS residual components $\epsilon_i^n$ in Section 2 | Formructured explicit PDE residual equations $\epsilon_1, \epsilon_2, \epsilon_3$ in Section 1 | Paper references RANS differential formulation verbally; full mathematical forms required for code implementation. |
| `H^12` | $H_{12}$ | Fixed boundary layer shape factor notation. |
| `c^f` | $c_f$ | Corrected skin friction coefficient notation. |
| Table 1 column header layout unformatted in text | Structured into systematic physical metric error targets in Section 4 | Fragmented ASCII layout in source document. |