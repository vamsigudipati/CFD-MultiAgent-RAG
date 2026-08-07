## 1. Physical Problem Statement

**Note:** N/A — not a fluid-dynamics ML modeling paper. This paper does not propose or train a neural network or machine learning architecture. Instead, it develops a foundational, information-theoretic mathematical framework casting causality, reduced-order modeling, and optimal control for chaotic high-dimensional dynamical systems in terms of Shannon entropy, directed information flux, conditional co-information, and Kullback–Leibler (KL) divergence.

The proposed theoretical formulation is demonstrated on three physical fluid dynamics application cases:

1. **Interscale Energy Cascade Causality (Isotropic Turbulence):**
   - **Regime:** Incompressible, forced, triply periodic isotropic turbulence governed by Navier–Stokes equations:
     $$\frac{\partial u_i}{\partial t} + \frac{\partial u_i u_j}{\partial x_j} = -\frac{1}{\rho} \frac{\partial \Pi}{\partial x_i} + \nu \frac{\partial^2 u_i}{\partial x_j \partial x_j} + f_i, \quad \frac{\partial u_i}{\partial x_i} = 0$$
   - **Parameters:** Taylor-microscale Reynolds number $Re_\lambda \approx 380$; integral-to-Kolmogorov length scale ratio $L_\varepsilon / \eta = 1800$; domain size $L^3$; Fourier spatial grid $1024^3$ ($\approx 10^9$ degrees of freedom); time sampling interval $\Delta t = 0.0076 T_\varepsilon$ over $165 T_\varepsilon$.
   - **Observables:** Volume-averaged interscale kinetic energy transfer $\langle \Sigma_i \rangle(t) = \langle \tau_{ij}^{\text{SGS}, i} \bar{S}_{ij}^i \rangle$ at four inertial-range Gaussian filter scales $\bar{\Delta}_1 = 163\eta$, $\bar{\Delta}_2 = 81\eta$, $\bar{\Delta}_3 = 42\eta$, and $\bar{\Delta}_4 = 21\eta$.

2. **Subgrid-Scale (SGS) Modeling for Large-Eddy Simulation (LES):**
   - **Regime:** Forced isotropic turbulence at $Re_\lambda \approx 260$.
   - **DNS Baseline:** $512^3$ spatial Fourier modes ($\approx 1.3 \times 10^8$ degrees of freedom) with linear forcing $f_i = A u_i$.
   - **LES Setup:** Truncated grid with $64^3$ sharp Fourier filter modes ($\approx 3 \times 10^5$ degrees of freedom).
   - **Model Formulation:** Two-parameter algebraic tensor expansion (Lund–Novikov):
     $$\tau_{ij}^{\text{SGS}} - \frac{1}{3}\tau_{kk}^{\text{SGS}}\delta_{ij} = \theta_1 \bar{\Delta}^2 \bar{S}_{ij}\sqrt{\bar{S}_{nm}\bar{S}_{nm}} + \theta_2 \bar{\Delta}^2(\bar{S}_{ik}\bar{\Omega}_{kj} - \bar{\Omega}_{ik}\bar{S}_{kj})$$
   - **Optimization:** On-the-fly calibration of $\boldsymbol{\theta} = (\theta_1, \theta_2)$ every 100 time-steps via gradient descent minimizing KL divergence between scaled interscale energy transfers $\bar{\Gamma} = (\bar{u}_i \bar{u}_j - \overline{u_i u_j})\bar{S}_{ij} - 2\nu \bar{S}_{ij}\bar{S}_{ij} + \tau_{ij}^{\text{SGS}}\bar{S}_{ij}$ across filter scales:
     $$\boldsymbol{\theta}^* = \arg \min_{\boldsymbol{\theta}'} \text{KL}\left( p(\bar{\Gamma}_{2\gamma}), p(\bar{\Gamma}_1) \right)$$

3. **Optimal Drag Reduction via Opposition Control (Turbulent Channel Flow):**
   - **Regime:** Incompressible turbulent channel flow between parallel walls separated by $2\delta$ at bulk Reynolds number $Re = U_{\text{bulk}}\delta/\nu = 3200$ ($Re_\tau \approx 180$).
   - **DNS Grid:** Spatial discretization of $64 \times 90 \times 64$ ($368,640$ degrees of freedom); time step $\Delta t^+ \approx 5 \times 10^{-3}$.
   - **Actuation Law:** Wall-normal velocity blowing/sucking at wall $y=0$:
     $$v(x, 0, z, t^{n+1}) = -\beta \, v(x, y_s, z, t^n)$$
   - **Parameters:** Controller parameter vector $\boldsymbol{\theta} = [y_s, \beta]$, where $y_s$ is the sensing plane wall-normal location and $\beta$ is the blowing intensity.
   - **Target Variable:** Mean wall shear stress $J^{n+1} = \tau_w$ in statistically steady state ($T^+ = 60$). Target mean $\hat{\mu}^+ = 0$ and standard deviation $\hat{\Xi}^{1/2} \approx 0.1 \langle \tau_{w,u} \rangle$.

---

## 2. Network Architectures

N/A — not a fluid-dynamics ML modeling paper.

---

## 3. Data Scaling & Normalization

N/A — not a fluid-dynamics ML modeling paper.

---

## 4. Required Physics Validation Gates

N/A — not a fluid-dynamics ML modeling paper.

---

## 5. Architectural Innovations & Edge Cases

N/A — not a fluid-dynamics ML modeling paper.

---

## 6. Raw Data Corrections Log

1. **Equation Duplication & Corruption in Section III:**
   - *Original Extraction:* Eq. (12b) duplicated with malformed probability nested terms: `\mathbb{P}[p(q^n|q^n)|p(q^n) \log\{\mathbb{P}[p(q^n|q^n)]\}] = 0`.
   - *Correction:* Reconstructed zero conditional-entropy condition for deterministic systems:
     $$H(\mathbf{Q}^{n+1}|\mathbf{Q}^n) = \sum -p(\mathbf{q}^{n+1}, \mathbf{q}^n) \log_2 [p(\mathbf{q}^{n+1}|\mathbf{q}^n)] = 0$$

2. **Corrupted State Symbol OCR in Section V.A:**
   - *Original Extraction:* `Qe^n`, `Qb^n`, `Q0^n`, and `Q'^n` were inconsistently substituted for LaTeX vector accents.
   - *Correction:* Reconstructed exact theoretical notation:
     - True truncated state: $\tilde{\mathbf{Q}}^n \in \mathbb{R}^{\tilde{N}}$
     - Inaccessible degrees of freedom: $\mathbf{Q}'^n \in \mathbb{R}^{N - \tilde{N}}$
     - Model prediction state: $\hat{\mathbf{Q}}^n$
     - Quantity of interest: $\tilde{\mathbf{Y}}^n = \mathbf{h}(\tilde{\mathbf{Q}}^n)$ and model prediction $\hat{\mathbf{Y}}^n = \mathbf{h}(\hat{\mathbf{Q}}^n)$

3. **Subscript Vector Index Errors in Section IV.A:**
   - *Original Extraction:* Index vector $\bar{\boldsymbol{\iota}}$ was converted to `\bar{\mathbf{z}}`, `\bar{\mathbf{v}}`, or `\bar{v}'` in formulas (17), (25), (26), (31a), (32).
   - *Correction:* Restored uniform index notation $\bar{\boldsymbol{\iota}} = [\bar{\iota}_1, \dots, \bar{\iota}_M]$ representing the subset of active causing variables.

4. **Inequality Glitches in Error Bounds (Section V.A.1):**
   - *Original Extraction:* Eqs. (57), (58), (59), (67a), and (67b) contained OCR errors (e.g., missing fraction bars, misplaced parentheses, missing $\log_2$ arguments).
   - *Correction:* Restored generalized Fano's inequality lower bound for expected error:
     $$\mathbb{E}[\|\hat{\mathbf{Q}}^{n+1} - \tilde{\mathbf{Q}}^{n+1}\|] \geq \varepsilon \frac{H(\tilde{\mathbf{Q}}^{n+1}) - I(\tilde{\mathbf{Q}}^{n+1}; \hat{\mathbf{Q}}^{n+1}) - \log_2(\varepsilon/\Delta_Q) - 1}{\log_2(\tilde{N}) - \log_2(\varepsilon/\Delta_Q)}$$
     and Pinsker's inequality upper bound for probability distribution error:
     $$\|p(\hat{\mathbf{y}}^{n+1}) - p(\tilde{\mathbf{y}}^{n+1})\|_1 \leq \sqrt{2 \ln(2) \, \text{KL}(\tilde{\mathbf{Y}}^{n+1}, \hat{\mathbf{Y}}^{n+1})}$$