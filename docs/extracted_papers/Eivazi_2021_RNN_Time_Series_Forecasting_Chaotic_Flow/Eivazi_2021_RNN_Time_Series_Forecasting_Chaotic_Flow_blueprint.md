## 1. Physical Problem Statement
* **Flow System & Regime**: Low-order 9-mode representation of near-wall turbulent shear flow (Moehlis et al., 2004).
* **Domain Geometry**: Box dimensions $L_x = 4\pi$, $L_y = 2$, $L_z = 2\pi$, where $x, y, z$ denote streamwise, wall-normal, and spanwise coordinates.
* **Governing ODE System**: Galerkin projection of Navier-Stokes equations yielding a 9-dimensional dynamic mode amplitude system:
  $$\frac{\mathrm{d}\mathbf{a}(t)}{\mathrm{d}t} = \mathbf{L}\mathbf{a}(t) + \mathbf{N}\mathbf{q}(t) + \mathbf{c}$$
  where $\mathbf{a}(t) = [a_1(t), a_2(t), \dots, a_9(t)]^T \in \mathbb{R}^9$, $\mathbf{q}(t) \in \mathbb{R}^m$ contains quadratic interaction terms $a_i(t)a_j(t)$, $\mathbf{L} \in \mathbb{R}^{9 \times 9}$, $\mathbf{N} \in \mathbb{R}^{9 \times m}$, and $\mathbf{c} \in \mathbb{R}^9$.
* **Velocity Field Reconstruction**:
  $$\mathbf{u}_{\text{inst}}(\mathbf{x}, t) = \sum_{j=1}^9 a_j(t) \mathbf{u}_j(\mathbf{x})$$
* **Flow Parameters**: Model Reynolds number $Re = 400$, defined using channel full height $2h$ and reference laminar velocity $U_0$ at distance $y = h/2$ from the top wall.
* **Temporal Discretization**: Trajectories generated over $T = 4000$ time units with sampling time steps $\Delta t \in \{0.1, 1.0, 10.0\}$ ($\Delta t = 1.0$ nominal).

---

## 2. Network Architectures

### A. Long Short-Term Memory (LSTM) Architecture
* **Input Sequence Dimensionality**: $\mathbf{\chi} \in \mathbb{R}^{p \times 9}$ with temporal window $p = 10$.
* **Layer Composition**:
  * **Recurrent Backbone**: 1 or 2 stacked LSTM layers with $n = 90$ hidden units per layer.
  * **Output Projection**: Fully-Connected (FC) linear layer mapping state $\zeta^t \in \mathbb{R}^{90} \to \hat{\mathbf{a}}(t+1) \in \mathbb{R}^9$.
* **Internal Gate Equations** (per time step $t$):
  $$f^t = \sigma\left(\mathbf{W}_f [\mathbf{\chi}^t, \zeta^{t-1}] + \mathbf{b}_f\right)$$
  $$i^t = \sigma\left(\mathbf{W}_i [\mathbf{\chi}^t, \zeta^{t-1}] + \mathbf{b}_i\right)$$
  $$\tilde{\mathbf{C}}^t = \tanh\left(\mathbf{W}_c [\mathbf{\chi}^t, \zeta^{t-1}] + \mathbf{b}_c\right)$$
  $$\mathbf{C}^t = f^t \odot \mathbf{C}^{t-1} + i^t \odot \tilde{\mathbf{C}}^t$$
  $$o^t = \sigma\left(\mathbf{W}_o [\mathbf{\chi}^t, \zeta^{t-1}] + \mathbf{b}_o\right)$$
  $$\zeta^t = o^t \odot \tanh(\mathbf{C}^t)$$
  where $\odot$ is the Hadamard product and $\sigma(\cdot)$ is the logistic sigmoid function.

### B. Koopman with Nonlinear Forcing (KNF)
* **Delay Embedding**: State trajectories formatted as a Hankel matrix with delay dimension $q = 5$:
  $$\mathbf{X}^m = \begin{bmatrix} \mathbf{a}^{m-q+1} \\ \mathbf{a}^{m-q+2} \\ \vdots \\ \mathbf{a}^m \end{bmatrix} \in \mathbb{R}^{(9q) \times 1}$$
* **Nonlinear Library Construction**:
  $$\mathbf{F}^i = \begin{bmatrix} 1 & (\mathbf{a}^i)^{p_2} & (\mathbf{a}^i)^{p_3} & (\mathbf{a}^i)^{p_4} \end{bmatrix}^T$$
  containing quadratic ($p_2$), cubic ($p_3$), and quartic ($p_4$) combinations of state variables.
* **Sparse Identification (SINDy)**: Iterative Ridge Regression with hard threshold $\epsilon = 0.05$ (max iterations = 20) isolates active forcing terms $\mathbf{f}^i \in \mathbb{R}^{n'}$.
* **Discrete Space Linear Evolution**:
  $$\mathbf{X}^{m+1} = \mathbf{A}\mathbf{X}^m + \mathbf{B}\mathcal{F}^m$$
  where $\mathcal{F}^m \in \mathbb{R}^{(n' q) \times 1}$ is the delay-embedded active forcing vector. Operators $\mathbf{A} \in \mathbb{R}^{r \times r}$ and $\mathbf{B} \in \mathbb{R}^{r \times (n' q)}$ are identified using Singular Value Decomposition via Dynamic Mode Decomposition with Control (DMDc):
  $$\mathbf{A} = \mathbf{\hat{U}}^* \mathbf{Y} \mathbf{\tilde{V}} \mathbf{\tilde{S}}^{-1} \mathbf{\tilde{U}}_1^* \mathbf{\hat{U}}, \quad \mathbf{B} = \mathbf{\hat{U}}^* \mathbf{Y} \mathbf{\tilde{V}} \mathbf{\tilde{S}}^{-1} \mathbf{\tilde{U}}_2^*$$

### C. Baseline Benchmarks
* **MLP**: 5 hidden layers, 90 neurons/layer, input window $p = 500$ ($d = 4500$ inputs), output $9$.
* **GRU**: 1 layer, 90 units, update/reset gate mechanism, $p = 10$, output $9$.
* **Hankel-DMD (HDMD)**: Linear unforced approximation $\tilde{\mathbf{A}}_{\text{HDMD}} = \mathbf{U}^* \mathbf{Y} \mathbf{V} \mathbf{S}^{-1}$ with $q = 5$.

---

## 3. Data Scaling & Normalization
* **Non-dimensionalization**: All variables scaled by channel half-width $h$ and laminar centerline/reference velocity $U_0$.
* **Noise Contamination Modeling**: Gaussian white noise added to training sets to test robustness:
  $$\mathbf{a}_{\text{noisy}}(t) = \mathbf{a}(t) + \mathcal{N}\left(0, \sigma_{\text{noise}}^2\right)$$
  Noise ratio defined as $\eta = \frac{\sigma_{\text{noise}}}{\sigma_{\text{data}}} \times 100\%$, evaluated at $\eta \in \{0.5\%, 1.0\%, 5.0\%, 10.0\%\}$.
* **Error Normalization Factor**: Statistical spatial errors normalized by peak model values to eliminate near-zero divergence along the channel centerline $y = 0$.

---

## 4. Required Physics Validation Gates

### A. Mean Flow Profile Error Gate
$$E_{\bar{u}} = \frac{1}{2 \max(\bar{u}_{\text{mod}})} \int_{-1}^1 \left| \bar{u}_{\text{mod}}(y) - \bar{u}_{\text{pred}}(y) \right| \mathrm{d}y \le 0.01 \quad (1\%)$$

### B. Velocity Fluctuation Profile Error Gate
$$E_{u'^2} = \frac{1}{2 \max(u'^2_{\text{mod}})} \int_{-1}^1 \left| u'^2_{\text{mod}}(y) - u'^2_{\text{pred}}(y) \right| \mathrm{d}y \le 0.025 \quad (2.5\%)$$

### C. Short-Term Trajectory Divergence Metric
Averaged relative Euclidean error in 9-dimensional phase space:
$$\epsilon(t) = \left\langle \frac{\left[ \sum_{i=1}^9 \left(a_{i,\text{mod}}(t) - a_{i,\text{pred}}(t)\right)^2 \right]^{1/2}}{\left\langle \left[ \sum_{i=1}^9 \left(a_{i,\text{mod}}(t)\right)^2 \right]^{1/2} \right\rangle_t} \right\rangle_{\text{ens}}$$
* Accurate short-term prediction horizon defined by threshold $\epsilon(t) < 0.3$.
* Required horizons: $t_{\text{pred}} \ge 280$ time units for KNF, $t_{\text{pred}} \ge 130$ time units for standard LSTM.

### D. Phase-Space & Dynamic Invariant Gates
1. **Poincaré Section Mapping**: Reconstruction of probability density functions on the $a_1 - a_3$ plane at slice $a_2 = 0$ with $\frac{\mathrm{d}a_2}{\mathrm{d}t} < 0$.
2. **Maximum Lyapunov Exponent Matching**: Phase space trajectory separation metric:
   $$|\delta \mathbf{A}(t)| = \left[ \sum_{i=1}^9 \left(a_{i,1}(t) - a_{i,2}(t)\right)^2 \right]^{1/2}$$
   Target exponential growth rate $\lambda$ from initial perturbation $|\delta \mathbf{A}_0| = 10^{-6}$:
   $$\lambda_{\text{ref}} \approx 0.0296, \quad \lambda_{\text{KNF}} \approx 0.0281, \quad \lambda_{\text{LSTM}} \approx 0.0264$$

---

## 5. Architectural Innovations & Edge Cases

```
  [ Input Window: p steps ] 
             │
             ▼
   ┌───────────────────┐
   │  LSTM / KNF Step  │ ──► Predict Step t+1
   └───────────────────┘
             │
             ▼
   [ Concatenate Pred ] ──► Feed back as input (Autoregressive Rollout)
             │
             ▼
  ┌─────────────────────┐
  │  Multi-Step Loss /  │ ──► Compute multi-step error gradient (n^p steps)
  │ Selection Criterion │ ──► Evaluate Long-Term Flow Statistics (E_u, E_u'^2)
  └─────────────────────┘
```

1. **Long-Term Statistics Selection Criterion (Early Stopping)**:
   * *Edge Case*: One-step-ahead MSE loss overfits to local instantaneous transitions, causing physical divergence in long-term statistical metrics ($E_{\bar{u}}, E_{u'^2}$) as training epochs increase.
   * *Fix*: Implement validation monitoring based directly on long-term time-averaged statistics ($E_{\bar{u}}, E_{u'^2}$) across autoregressive rollouts to trigger early stopping.
2. **Autoregressive Multi-Step Batching Routine**:
   * For LSTM updates, concatenate predicted state back into the input sequence $n^p$ times ($n^p \in [8, 16]$) during training batch construction.
   * Minimizes exposure bias during continuous inference rollouts over $T = 4000$ steps without requiring high-order full backpropagation through time.
3. **Data Efficiency**:
   * KNF achieves equal statistical accuracy to LSTM using $0.025\%$ of the training data size ($1$ trajectory of $10,000$ steps vs. $10,000$ trajectories of $4,000$ steps) and trains $\sim 10^4 \times$ faster due to direct SVD/DMDc closed-form solution.

---

## 6. Raw Data Corrections Log
* **Equation 1 Reconstruction**: Corrected typography from OCR text $\frac{\mathrm{d}\mathbf{a}(t)}{\mathrm{d}t} = \mathbf{La}(t) + N\mathbf{q}(t) + \mathbf{c}$ to proper matrix-vector notation $\frac{\mathrm{d}\mathbf{a}(t)}{\mathrm{d}t} = \mathbf{L}\mathbf{a}(t) + \mathbf{N}\mathbf{q}(t) + \mathbf{c}$.
* **Equation 2 Notation**: Restored spatial integral limits $[-1, 1]$ and normalized error definitions $E_{\bar{u}}$ and $E_{u'^2}$ for mean and fluctuation profiles.
* **Algorithm 1 & 2 Cleanup**:
  * Reconstructed broken LaTeX in Algorithm 1 for LSTM gates ($\sigma(\mathbf{W}_f [\mathbf{\chi}^t, \zeta^{t-1}] + \mathbf{b}_f)$, candidate state $\tilde{\mathbf{C}}^t$).
  * Formatted active term selection algorithm (SINDy with Ridge Regression) with structural matrix thresholding variables $\mathbf{C}[j, \mathbf{I}_j]$ and mask vector $\mathbf{I}_{\text{active}}$.
* **Variables & Dimensions**: Fixed formatting of delay embedding dimensions $q$, truncated rank variables $r, k$, and noise standard deviations $\sigma_{\text{noise}}$.