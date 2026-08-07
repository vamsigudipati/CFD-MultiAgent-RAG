## 1. Physical Problem Statement
* **Flow Regime & Geometry:** Incompressible minimal turbulent channel flow between two parallel infinite plates separated by $y \in [0, 2h]$ ($h=1$). Homogeneous streamwise ($x$) and spanwise ($z$) directions.
* **Domain Dimensions:** $(L_x, L_y, L_z) = (0.6\pi h, 2h, 0.18\pi h) \approx (1.885h, 2h, 0.565h)$.
* **Grid Resolution:** $N_x \times N_y \times N_z = 32 \times 129 \times 16$ grid points (economy SVD rank $e = N_y = 129$).
* **Reynolds Numbers:**
  * Laminar centerline-velocity-based Reynolds number: $Re_{cl} = \frac{U_{cl} h}{\nu} = 5,000$.
  * Friction Reynolds number: $Re_\tau = \frac{u_\tau h}{\nu} = 202$.
* **Numerical Simulation Scheme:** Direct Numerical Simulation (DNS) via Fourier–Chebyshev pseudo-spectral solver `SIMSON`. Time integration employs a 2nd-order Crank–Nicholson (CN) scheme for linear terms and a 3rd-order 4-stage Runge–Kutta (RK3) scheme for non-linear terms. Streamwise pressure gradient is dynamically updated to maintain constant mass flux.
* **Dataset Generation:**
  * Total duration: $T = 160,000$ time units (after discarding initial transient $t < 10,000$).
  * Total snapshots: $800,000$ saved at constant interval $\Delta t^s = 0.2$.
* **Modal Decomposition (FFT-POD):**
  * 2D Fast Fourier Transform along homogeneous $x$ and $z$ directions followed by Proper Orthogonal Decomposition (1D POD via SVD) along the wall-normal direction $y$:
    $$\mathbf{u}_{\text{POD}} = \mathbf{U}(\mathbf{x}) \mathbf{V}(t)^{\text{H}}$$
  * Decomposition targets the streamwise velocity component $u(x, y, z, t)$.
  * Energy Truncation: Primary data-driven model retains $M = 100$ most energetic spatial-temporal mode triplets $(m, n, k)$, capturing $78.8\%$ of total streamwise turbulent kinetic energy $u'$ with a relative $L_2$ field reconstruction error of $22.2\%$:
    $$\frac{\|\mathbf{u}_{\text{orig}} - \mathbf{u}_{\text{recon}}\|_2}{\|\mathbf{u}_{\text{orig}}\|_2} = 0.222$$
  * Excluded Mode Dynamics: Mean net-flux modes associated with wavenumber pair $(m,n) = (0,0)$ are excluded from network training; remaining modes account for $97\%$ of non-zero wavenumber fluctuation energy.

---

## 2. Network Architectures

### Architecture 1: Long Short-Term Memory Network (LSTM)
* **Task:** Autoregressive single-step prediction of POD temporal mode coefficients $a_j(t+1)$ given input history sequence $\mathbf{\chi} = [\hat{a}_j(t-p+1), \dots, \hat{a}_j(t)]$.
* **Topology:**
  * **Input Layer:** Sequence length $p \in \{5, 10, 20, 40\}$ (Optimal: $p = 10$).
  * **Recurrent Hidden Layers:** 1 or 2 stacked LSTM layers with cell counts $n_{\text{cell}} \in \{90, 150, 200, 300\}$ (Optimal: 1 layer, $n_{\text{cell}} = 200$).
  * **Recurrent Gate Mechanics:**
    $$f^t = \sigma(W^f [\chi^t, \zeta^{t-1}] + b^f)$$
    $$i^t = \sigma(W^i [\chi^t, \zeta^{t-1}] + b^i)$$
    $$\tilde{C}^t = \tanh(W^c [\chi^t, \zeta^{t-1}] + b^c)$$
    $$C^t = f^t \otimes C^{t-1} + i^t \otimes \tilde{C}^t$$
    $$o^t = \sigma(W^o [\chi^t, \zeta^{t-1}] + b^o)$$
    $$\zeta^t = o^t \otimes \tanh(C^t)$$
  * **Hidden Activation:** Hyperbolic tangent ($\tanh$).
  * **Output Layer:** Dense (fully connected) projection layer with linear activation.
* **Hyperparameters & Training Parameters:**
  * **Loss Function:** Mean Squared Error (MSE):
    $$\mathcal{L}_{\text{MSE}} = \frac{1}{N_{\text{batch}}} \sum_{k=1}^{N_{\text{batch}}} (\hat{a}_{j, \text{pred}}^k - \hat{a}_{j, \text{true}}^k)^2$$
  * **Optimizer:** Adam with batch size $N_{\text{batch}} = 32$, total epochs $= 2,000$.
  * **Learning Rate Decay:** Exponential decay initialized at $\text{LR}_0 = 0.001$:
    $$\text{LR} = \text{LR}_0 \cdot \alpha_D^{n_C / n_D} = 0.001 \cdot 0.96^{n_C / n_D}$$
  * **Data Split:** $80\%$ training set, $20\%$ validation set. Best validation loss model preserved.

### Architecture 2: Koopman with Non-linear Forcing (KNF / SINDy + DMDc)
* **Task:** Linear state-space advancement with sparse exogenous polynomial forcing:
  $$\mathbf{x}^{t+1} = \mathbf{A}\mathbf{x}^t + \mathbf{B}\mathbf{f}^t$$
* **Parameters:**
  * Delay-embedding Hankel dimension: $q \in [4, 5]$.
  * State variables $\mathbf{x} \in \mathbb{R}^{m_0}$, forcing vector $\mathbf{f} \in \mathbb{R}^{n_0}$ consisting of candidate polynomial combinations up to degree $d_{\text{poly}} \in [2, 7]$.
  * Sparse Identification of Non-linear Dynamics (SINDy): Iterative thresholded ridge regression with threshold $\epsilon$.
  * Matrices $\mathbf{A}$ and $\mathbf{B}$ solved via Dynamic Mode Decomposition with Control (DMDc) minimizing $\|\mathbf{Y}' - \mathbf{A}\mathbf{X}' - \mathbf{B}\mathcal{F}\|_F$.
  * SVD energy truncation threshold ranks: $e_r, e_p \in [10^{-10}, 10^{-5}]$.

---

## 3. Data Scaling & Normalization

* **Z-Score Normalization:** Every POD temporal coefficient $a_j(t)$ is zero-mean centered and unit-variance scaled prior to training sequence assembly:
  $$\hat{a}_j(t) = \frac{a_j(t) - \langle a_j(t) \rangle}{\sigma[a_j(t)]}$$
  where $\langle a_j(t) \rangle$ is the temporal mean and $\sigma[a_j(t)]$ is the standard deviation over the dataset.
* **Physical Domain Inverse Transformation:** Predicted normalized coefficients $\hat{a}_{j, \text{pred}}(t)$ are rescaled back to physical units $a_{j, \text{pred}}(t) = \hat{a}_{j, \text{pred}}(t) \cdot \sigma[a_j] + \langle a_j \rangle$. Physical velocity fluctuations are reconstructed via:
  $$\mathbf{u}(\mathbf{x}, t) = \sum_{i=0}^M \left( \text{Re}\{a_i(t) \boldsymbol{\mathcal{U}}_i(\mathbf{x})\} - \text{Im}\{a_i(t) \boldsymbol{\mathcal{U}}_i(\mathbf{x})\} \right)$$
  where $\boldsymbol{\mathcal{U}}_i(\mathbf{x})$ is the spatial POD basis mode associated with frequency/quantum triplet $i = (m, n, k)$.

---

## 4. Required Physics Validation Gates

1. **Streamwise Velocity Fluctuation RMS Profile Error ($E_{u_{\text{RMS}}}$):**
   $$E_{u_{\text{RMS}}} = \frac{\| u_{\text{RMS, ref}}(y) - u_{\text{RMS, pred}}(y) \|_2}{\| u_{\text{RMS, ref}}(y) \|_2} \times 100\%$$
   * Target: $E_{u_{\text{RMS}}} \le 1.3\%$ (achieved by `LSTM-1-200-10-100` evaluated over $T = 4,000$ time units).
2. **Validation MSE Loss Gates:**
   * Low-frequency modes (Group [1]): $\mathcal{L}_{\text{val}} \approx 7.74 \times 10^{-6}$.
   * High-frequency modes (Group [2]): $\mathcal{L}_{\text{val}} \approx 2.03 \times 10^{-3}$.
3. **Chaotic Divergence via Largest Lyapunov Exponent ($\lambda$):**
   * Evolution of trajectory divergence under infinitesimal initial state perturbation $|\delta \mathbf{A}_0| \approx 10^{-7}$:
     $$|\delta \mathbf{A}(t)| = \left[ \sum_{j=1}^M (a_{j, \text{orig}}(t) - a_{j, \text{pert}}(t))^2 \right]^{1/2} \approx e^{\lambda t} |\delta \mathbf{A}_0|$$
   * **Validation Criterion:**
     * Group [1] Real $\lambda_1$: Ref $= 0.1258$, LSTM $= 0.1015$.
     * Group [2] Imaginary $\lambda_2$: Ref $= 0.1763$, LSTM $= 0.1873$.
4. **Phase-Space Poincaré Map Topography:**
   * Poincaré section defined by directional hyperplane intersections: $a_\gamma = 0$ with $\frac{da_\gamma}{dt} < 0$.
   * Topological match required for mode pairs $(a_1, a_6)$ on $a_4 = 0$ (low-freq) and $(a_{10}, a_{14})$ on $a_{12} = 0$ (high-freq).
5. **Reconstructed Fluctuation Energy Percentage:**
   * Full data-driven model ($M=100$ modes): $97.05\%$ of fluctuation TKE.
   * Alternative ROM2 ($12$ modes): $20.71\%$ of fluctuation TKE.
   * Alternative ROM1 ($6$ modes): $10.74\%$ of fluctuation TKE.

---

## 5. Architectural Innovations & Edge Cases

* **Multi-Frequency Partitioning Scheme:** Temporal POD modes exhibit distinct spectral content. To prevent stiffness and gradient degradation, modes are split into separate sub-networks:
  * Group [1] (Low-frequency modes): Sub-sampled with step size $\Delta t^{[1]} = 0.8$.
  * Group [2] (High-frequency modes): Sub-sampled with step size $\Delta t^{[2]} = 0.4$.
  * Separation justified by cross-group correlation factors ($3 \times 10^{-4}$ to $2 \times 10^{-3}$) being orders of magnitude lower than intra-group correlations ($4 \times 10^{-3}$ to $3 \times 10^{-1}$).
* **Structure-Based Reduced-Order Models (ROMs):** Modes categorized into 6 wavenumber-pair sub-groups based on physical coherent structures (roll modes $m=0$, streamwise modes $n=0$, propagating tilted vortices):
  * **ROM1:** Retains 1 mode per wavenumber pair ($6$ total trained modes).
  * **ROM2:** Retains 2 modes per wavenumber pair ($12$ total trained modes).
* **Mode Degeneracy Handling:** Wavenumber pairs with opposite signs $(m, n)$ and $(-m, -n)$ possess identical energy content. They are treated as single degenerate modes during energy ranking, but predicted independently as complex-conjugate components.
* **KNF Stability Failure Edge Case:** For minimal-channel data-driven dynamics, KNF fails to generate sustained trajectories. Linear operator matrix $\mathbf{A}$ eigenvalues lie strictly inside or on the unit circle ($|\lambda| \le 1$). High-dimensional non-linear forcing matrix $\mathbf{B}\mathbf{f}^t$ fails to supply stable balance, causing trajectories to either decay rapidly to zero or collapse non-physically.

---

## 6. Raw Data Corrections Log

1. **Algorithm 1 Notation Repair:** Corrupted OCR output for LSTM updates restored to standard mathematical formulation:
   * $^C e^t \to \tilde{C}^t$ (candidate cell state).
   * $^C^t \to C^t$ (updated cell state).
   * $^b^f \to b^c$ (bias term for candidate cell state).
   * $W^f [ \chi^t, \zeta^{t-1} ] + ^b^f \to W^c [ \chi^t, \zeta^{t-1} ] + b^c$.
2. **Equation (7) Symbol Artifact:** Fixed corrupted string $b^a^j(t)$ in text to match equation variable $\hat{a}_j(t)$.
3. **Equation (8) Variable Typo:** Corrected decay formula variables $R \to \text{LR}$, $R_0 \to \text{LR}_0$, and $\alpha_p^{nc/np} \to \alpha_D^{n_C/n_D}$.
4. **Equation (18) Matrix Formatting:** Reconstructed block-matrix Hermitian transpositions $\hat{\mathbf{U}}_1^H$ and $\hat{\mathbf{U}}_2^H$ from fragmented OCR typesetting.
5. **Economy SVD Size Inference:** Inferred missing explicit definition of economy-SVD rank $e = \min(N_t, N_y) = N_y = 129$, which sets the total mode spatial dimension across Fourier modes to $N_x \times N_y \times N_z = 66,048$.