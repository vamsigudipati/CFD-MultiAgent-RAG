## 1. Physical Problem Statement
* **Flow Regimes & Dynamics**:
  * Incompressible, steady two-dimensional Reynolds-Averaged Navier–Stokes (RANS) boundary layer flows.
  * Canonical Zero-Pressure-Gradient Turbulent Boundary Layer (ZPGTBL) and Adverse-Pressure-Gradient (APG) turbulent boundary layer over a NACA4412 airfoil suction side ($Re_c = 2 \times 10^5$).
  * Active flow control configurations: Upstream uniform blowing (UB) at blowing ratios $\text{BR} = (V_w / U_\infty) \times 100 \in \{0\%, 0.1\%, 0.5\%, 1.0\%, 3\%, 6\%\}$.
* **Reynolds Numbers**:
  * Experimental stereo-PIV ZPGTBL: $Re_\theta = \frac{U_\infty \theta}{\nu} \in [7500, 19763]$.
  * DNS flat-plate boundary layer: $Re_\theta \in [400, 500]$.
  * NACA4412 Airfoil simulation: $Re_c = 200,000$.
* **Governing Partial Differential Equations (2D Incompressible RANS)**:
  $$\frac{\partial U_i}{\partial x_i} = 0, \quad i \in \{1, 2\}$$
  $$U_j \frac{\partial U_i}{\partial x_j} = -\frac{1}{\rho} \frac{\partial P}{\partial x_i} - \frac{\partial (\overline{u_i u_j})}{\partial x_j} + \nu \frac{\partial^2 U_i}{\partial x_j \partial x_j}, \quad i,j \in \{1, 2\}$$
  Where $x_1 = x, x_2 = y$, $U_1 = U, U_2 = V$, and $\overline{u_i u_j}$ represents the Reynolds stress components ($\overline{uu}, \overline{uv}, \overline{vv}$).

---

## 2. Network Architectures
* **Model Type**: Physics-Informed Neural Network (PINN) featuring a Multilayer Perceptron (MLP) coupled with automatic differentiation (AD) residual evaluator.
* **Input Vector**: Spatial coordinates $\mathbf{x} = (x, y) \in \mathbb{R}^2$.
* **Output Vector**: Scaled mean flow quantities $\mathbf{u} = [U, \overline{uv}, \overline{uu}, \overline{vv}, V]^T \in \mathbb{R}^5$.
* **Layer Architecture**:
  * Input layer: 2 units.
  * Hidden layers: 4 dense layers, each containing 20 hidden units (total 4 hidden layers).
  * Output layer: 5 units.
* **Activation Functions**: Hyperbolic tangent ($\tanh$) across all hidden layers.
* **Optimizer Setup**:
  * **Phase 1**: Adam optimizer for $20,000$ epochs.
  * **Learning Rate Schedule**: Exponential decay:
    $$\ell r = \ell r_0 \cdot \alpha_d^{\left(n_c / n_d\right)}$$
    Where $\ell r_0 = 0.01$ (initial rate), $\alpha_d = 0.1$ (decay rate), $n_d = 5000$ (decay step), and $n_c$ is current epoch step.
  * **Phase 2**: L-BFGS (Limited-memory Broyden–Fletcher–Goldfarb–Shanno) optimizer for full convergence, terminated based on increment tolerance.
* **Training Batching**: Full-batch gradient descent.

---

## 3. Data Scaling & Normalization
* **Coordinate & Velocity Scaling**:
  * Spatial positions normalized by domain/outer boundary layer thickness scale: $x / \delta$, $y / \delta$.
  * Velocity quantities non-dimensionalized by free-stream velocity: $U / U_\infty$, $V / U_\infty$.
  * Reynolds stress components non-dimensionalized by $U_\infty^2$: $\overline{uu} / U_\infty^2$, $\overline{uv} / U_\infty^2$, $\overline{vv} / U_\infty^2$.
* **Sampling Distribution**:
  * Boundary/Training Data Points ($N_s$): Selected at domain boundaries using logarithmic distribution in $y$-direction.
    * DNS datasets: $N_s = 188$.
    * Experimental PIV datasets: $N_s = 350$.
  * Collocation Points ($N_e$):
    * DNS datasets: $N_e = 17,000$.
    * Experimental PIV datasets: $N_e = 3,350$.

---

## 4. Required Physics Validation Gates
* **Loss Function Formulation**:
  $$L = L_e + L_s$$
  $$L_e = \frac{1}{N_e} \sum_{i=1}^{3} \sum_{n=1}^{N_e} \left| e_i^n \right|^2$$
  $$L_s = \frac{1}{N_s} \sum_{n=1}^{N_s} \left| \mathbf{u}_s^n - \tilde{\mathbf{u}}_s^n \right|^2$$
  Where $e_1^n, e_2^n, e_3^n$ are residuals of continuity and $x,y$-momentum RANS equations, and target training vector is $\mathbf{u}_s = [U, \overline{uv}, \overline{uu}, \overline{vv}]^T$ ($\tilde{\mathbf{u}}_s$ represents boundary data targets).
* **Validation Thresholds & Performance Metrics**:
  * Relative error metric across domain:
    $$\epsilon = \frac{|\text{Pred.} - \text{Ref.}|}{|\text{Ref.}|}$$
  * Streamwise velocity ($\hat{U}$): Maximum domain relative error $\epsilon_{\hat{U}} < 1\%$.
  * Wall-normal velocity ($\hat{V}$): Maximum domain relative error $\epsilon_{\hat{V}} < 5\%$.
  * Reynolds stresses ($\overline{uv}, \overline{uu}, \overline{vv}$): Mean relative error across domain $< 3\%$ (local peak relative errors $\le 11\% - 15\%$).

---

## 5. Architectural Innovations & Edge Cases
* **Model-Free Turbulence Reconstruction**: No eddy-viscosity model, Boussinesq hypothesis, or $k-\epsilon / k-\omega$ closures are implemented. The network infers Reynolds stress divergence directly from boundary observations combined with automatic differentiation of PDE residuals.
* **Unsupervised Wall-Normal Velocity ($V$) Inference**: The target data vector $\mathbf{u}_s$ explicitly excludes $V$. $V$ is solved as a pure unconstrained latent output of the MLP, guided purely by the unsupervised physical residual $L_e$. This bypasses high measurement noise and laser reflections in PIV datasets near $y^+ < 16$.
* **Handling Variable Upstream History**: Robust inference under strong upstream mass-flux injection (uniform blowing up to $\text{BR} = 6\%$) using only boundary values, maintaining accuracy without explicit history parameterization.

---

## 6. Raw Data Corrections Log
* Reconstructed malformed momentum equation diffusion term in Equation (1b): `\nu \frac{\partial^2 U_i}{\partial x_i \partial x_j}` corrected to standard laplacian form $\nu \frac{\partial^2 U_i}{\partial x_j \partial x_j}$ (or $\nabla^2 U_i$).
* Reconstructed inconsistent subscript notations in equation text: corrected variable formatting for Reynolds stresses from raw text `uu`, `uv`, `vv` to tensor component notation $\overline{uu}, \overline{uv}, \overline{vv}$ or $u_i u_j$.
* Corrected variable definition text: `n_c/n_d` inside equation (3) formatted into exponent expression $\alpha_d^{(n_c / n_d)}$.