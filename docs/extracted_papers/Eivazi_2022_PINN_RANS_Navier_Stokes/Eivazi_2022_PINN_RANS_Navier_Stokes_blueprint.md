## 1. Physical Problem Statement

The paper presents a physics-informed neural network (PINN) framework to solve the two-dimensional incompressible Navier–Stokes and Reynolds-averaged Navier–Stokes (RANS) equations without applying traditional turbulence closure models (e.g., eddy-viscosity hypotheses or transport models). The system is closed implicitly by incorporating reference boundary data for mean velocities, pressure, and Reynolds stress tensor components.

### Flow Regimes & Test Cases
1. **Falkner–Skan Boundary Layer (FSBL):**
   - Regime: 2D steady laminar flow with adverse pressure gradient.
   - Flow parameters: $Re = 100$, pressure gradient parameter $m = -0.08$, Hartree parameter $\beta_{\text{FS}} = \frac{2m}{m+1} = -0.1739$. Reference analytical solution.
2. **Zero-Pressure-Gradient (ZPG) Turbulent Boundary Layer:**
   - Regime: Incompressible turbulent boundary layer over a flat plate.
   - Flow parameters: $1000 < Re_\theta < 7000$ (based on momentum thickness $\theta$). Reference DNS data from Eitel-Amor et al. (2014).
3. **Adverse-Pressure-Gradient (APG) Turbulent Boundary Layer:**
   - Regime: Incompressible turbulent boundary layer with non-zero pressure gradient.
   - Flow parameters: $910 < Re_\theta < 3360$, Clauser pressure-gradient parameter $\beta = \frac{\delta^*}{\tau_w} \frac{dP_\infty}{dx} \approx 1.0$. Reference DNS data from Bobke et al. (2017).
4. **NACA4412 Airfoil:**
   - Regime: Turbulent boundary layer over the suction side of an airfoil.
   - Flow parameters: Spatial domain $0.5 < x/c < 1.0$, chord Reynolds number $Re_c = \frac{U_\infty c}{\nu} = 200,000$. Reference high-resolution LES data from Vinuesa et al. (2018).
5. **Periodic Hill:**
   - Regime: Separated turbulent flow over periodic geometry.
   - Flow parameters: Spatial domain $1 < x/H < 5$, bulk Reynolds number $Re_b = \frac{U_b H}{\nu} = 2,800$ based on hill crest height $H$ and bulk velocity $U_b$. Reference DNS data.

### Governing Differential Equations
1. **Continuity Equation:**
$$\frac{\partial U}{\partial x} + \frac{\partial V}{\partial y} = 0$$

2. **Streamwise RANS Momentum Equation:**
$$U \frac{\partial U}{\partial x} + V \frac{\partial U}{\partial y} + \frac{1}{\rho} \frac{\partial P}{\partial x} - \nu \left( \frac{\partial^2 U}{\partial x^2} + \frac{\partial^2 U}{\partial y^2} \right) + \frac{\partial \overline{u^2}}{\partial x} + \frac{\partial \overline{uv}}{\partial y} = 0$$

3. **Wall-Normal RANS Momentum Equation:**
$$U \frac{\partial V}{\partial x} + V \frac{\partial V}{\partial y} + \frac{1}{\rho} \frac{\partial P}{\partial y} - \nu \left( \frac{\partial^2 V}{\partial x^2} + \frac{\partial^2 V}{\partial y^2} \right) + \frac{\partial \overline{uv}}{\partial x} + \frac{\partial \overline{v^2}}{\partial y} = 0$$

*(Note: For laminar FSBL, all Reynolds stress components $\overline{u^2}, \overline{uv}, \overline{v^2}$ are set to zero).*

---

## 2. Network Architectures

### Network Topology
- **Type:** Deep Fully-Connected Neural Network (FNN / PINN).
- **Depth:** $8$ hidden layers.
- **Width:** $20$ neurons per hidden layer.
- **Activation Functions:** Hyperbolic tangent ($\tanh$) across all hidden layers.
- **Inputs:** 
  - Cartesian domain coordinates $(x, y)$ or wall-normal spatial coordinates $(x^n, y^n)$ (for NACA4412).
- **Outputs:**
  - FSBL: $\tilde{\mathbf{U}} = [U, V, P]^T$
  - ZPG: $\tilde{\mathbf{U}} = [U, V, \overline{uv}]^T$
  - APG: $\tilde{\mathbf{U}} = [U, V, P, \overline{uv}]^T$
  - NACA4412 & Periodic Hill: $\tilde{\mathbf{U}} = [U, V, P, \overline{u^2}, \overline{uv}, \overline{v^2}]^T$

### Optimization Pipeline & Differentiation
- **Framework:** TensorFlow (`tf.GradientTape` for reverse-mode automatic differentiation).
- **Optimizer Strategy:**
  1. Initial training phase: First-order Adam optimizer (`Kingma and Ba, 2017`).
  2. Fine-tuning phase: Full-batch Quasi-Newton L-BFGS (Broyden–Fletcher–Goldfarb–Shanno) optimization algorithm, terminated automatically based on parameter increment tolerances.

---

## 3. Data Scaling & Normalization

### Boundary Layer & Near-Wall Scaling Relations
- **Friction Velocity:**
$$u_\tau = \sqrt{\frac{\tau_w}{\rho}}$$
where $\tau_w = \mu \left. \frac{\partial U}{\partial y} \right|_{y=0}$ is the wall shear stress.

- **Viscous Length Scale:**
$$\ell^* = \frac{\nu}{u_\tau}$$

- **Inner-Scaled Coordinates & Velocities:**
$$y^+ = \frac{y}{\ell^*} = \frac{y u_\tau}{\nu}, \quad U^+ = \frac{U}{u_\tau}$$

- **Inner-Scaled Reynolds Stresses:**
$$uv^+ = \frac{\overline{uv}}{u_\tau^2}, \quad u^{2+} = \frac{\overline{u^2}}{u_\tau^2}, \quad v^{2+} = \frac{\overline{v^2}}{u_\tau^2}$$

- **Nondimensional Coefficients:**
  - Skin-friction coefficient: $c_f = 2 \left( \frac{u_\tau}{U_\infty} \right)^2$
  - Boundary layer shape factor: $H_{12} = \frac{\delta^*}{\theta}$, where $\delta^*$ is displacement thickness and $\theta$ is momentum thickness.
  - Spatial non-dimensionalization: $x/c$ (airfoil chord length $c$), $x/H$ ( periodic hill height $H$).

---

## 4. Required Physics Validation Gates

### Error Metric
Validation is conducted using the relative $L_2$-norm percentage error over all computational points $N_{total}$:
$$E_i = \frac{\|\mathbf{U}_i - \tilde{\mathbf{U}}_i\|_2}{\|\mathbf{U}_i\|_2} \times 100\% = \frac{\sqrt{\sum_{k=1}^{N_{total}} \left( \mathbf{U}_{i,k} - \tilde{\mathbf{U}}_{i,k} \right)^2}}{\sqrt{\sum_{k=1}^{N_{total}} \left( \mathbf{U}_{i,k} \right)^2}} \times 100\%$$

### Validation Benchmarks & Threshold Targets

| Test Case | $E_U$ (%) | $E_V$ (%) | $E_P$ (%) | $E_{\overline{u^2}}$ (%) | $E_{\overline{uv}}$ (%) | $E_{\overline{v^2}}$ (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **FSBL** | $0.07$ | $0.12$ | $0.001$ | N/A | N/A | N/A |
| **ZPG** | $1.02$ | $4.25$ | N/A | N/A | $6.46$ | N/A |
| **APG** | $0.28$ | $1.57$ | $4.60$ | N/A | $7.96$ | N/A |
| **NACA4412** | $1.56$ | $2.17$ | $7.30$ | $9.43$ | $11.36$ | $4.69$ |
| **Periodic Hill** | $2.77$ | $19.70$ | $8.61$ | $28.18$ | $16.70$ | $20.24$ |

### Integral & Profile Validation Criteria
1. Boundary layer parameters $c_f(x)$ and $H_{12}(x)$ prediction matching DNS/LES profiles.
2. Inner-scaled profile matching ($U^+$, $uv^+$, $u^{2+}$, $v^{2+}$ vs $y^+$) at $Re_\theta \in \{2500, 4000, 5500\}$ (ZPG) and $Re_\theta \in \{1623, 2138, 2588\}$ (APG).
3. Streamwise velocity and stress profiles at $x/c \in \{0.625, 0.75, 0.875\}$ (NACA4412).
4. Prediction of separation zone bubble extent and reattachment location across $1 < x/H < 5$ (Periodic Hill).

---

## 5. Architectural Innovations & Edge Cases

### Innovations
1. **Model-Free RANS Closure:** The neural network solves unclosed RANS momentum equations without eddy viscosity models ($k-\epsilon$, $k-\omega$, SA) by directly optimizing mean fields and Reynolds stress outputs constrained by boundary conditions and governing momentum balances.
2. **Boundary-Only Data Supervision:** Supervised training data is supplied strictly at domain boundaries ($N_b$).
3. **Loss Function Structure:**
$$L = L_e + L_b$$
$$L_e = \frac{1}{N_e} \sum_{i=1}^{M} \sum_{n=1}^{N_e} \left| \epsilon_i^n \right|^2$$
$$L_b = \frac{1}{N_b} \sum_{n=1}^{N_b} \left| \mathbf{U}_b^n - \tilde{\mathbf{U}}_b^n \right|^2$$
where $M$ is the number of governing differential equations active in the domain, $N_e$ is the number of equation evaluation points (interior + boundary), and $\epsilon_i^n$ is the $i$-th PDE residual evaluated via automatic differentiation at point $n$.

### Edge Cases & Boundary Constraints
- **Periodic Hill Wall Conditions:** Velocities and Reynolds stresses on top and bottom walls are set identically to zero ($U=0, V=0, \overline{u^2}=0, \overline{uv}=0, \overline{v^2}=0$) due to non-slip constraints; physical supervised data is only provided at inlet and outlet profiles, alongside pressure at domain boundaries.

---

## 6. Raw Data Corrections Log

| Source Chunk | Header Section Name | Original Raw / Corrupted Text | Corrected / Reconstructed Representation | Context / Correction Description |
| :--- | :--- | :--- | :--- | :--- |
| Chunk 3 | `3 Results` | `U n b = [U n b , V n b , P n b , u 2 n b , uv n b , v 2 n b T` | $\mathbf{U}_b^n = [U_b^n, V_b^n, P_b^n, \overline{u^2}_b^n, \overline{uv}_b^n, \overline{v^2}_b^n]^T$ | Reconstructed boundary state vector indices and transposed vector superscript. |
| Chunk 3 | `3 Results` | `U~ n b` | $\tilde{\mathbf{U}}_b^n$ | Reconstructed network output prediction vector on boundary. |
| Chunk 3 | `3 Results` | `n i is the residual` | $\epsilon_i^n$ | Corrected missing Greek letter symbol for equation residual. |
| Chunk 4 | `3 Results` | ``relative `2-norm of errors E i`` | Relative $L_2$-norm error $E_i$ | Converted fragmented character back to LaTeX norm symbol. |
| Chunk 4 | `3 Results` | `E u 2` / `E v 2` | $E_{\overline{u^2}}$ / $E_{\overline{v^2}}$ | Fixed missing subscript/superscript formatting for normal stress error components. |
| Chunk 5 | `3 Results > Falkner–Skan boundary layer (FSBL)` | `m = −0.08 leading to β FS = 2m/(m + 1) = −0.1739` | $m = -0.08$, $\beta_{\text{FS}} = \frac{2m}{m+1} = -0.1739$ | Reconstructed Hartree parameter definition equation. |
| Chunk 6 | `3 Results > ZPG turbulent boundary layer` | `c f = 2(u τ /U∞) 2` | $c_f = 2 \left( \frac{u_\tau}{U_\infty} \right)^2$ | Fixed broken power exponents and parentheses in skin-friction formula. |
| Chunk 6 | `3 Results > ZPG turbulent boundary layer` | `u τ = p τw/ρ` | $u_\tau = \sqrt{\frac{\tau_w}{\rho}}$ | Reconstructed square root operation (`p` OCR artifact). |
| Chunk 6 | `3 Results > ZPG turbulent boundary layer` | `` ` * = ν/u τ `` | $\ell^* = \nu / u_\tau$ | Corrected viscous length scale symbol ($\ell^*$). |
| Chunk 7 | `3 Results > ZPG turbulent boundary layer > APG turbulent boundary layer` | `u 2 + , and v 2 +` | $u^{2+}$ and $v^{2+}$ | Restored superscripts for inner-scaled Reynolds normal stresses. |