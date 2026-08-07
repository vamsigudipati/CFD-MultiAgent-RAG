## 1. Physical Problem Statement

The physical target is the temporal dynamics of a low-order model representing the near-wall cycle of turbulent shear flow between two infinite parallel free-slip walls under a sinusoidal body force (Moehlis et al., 2004).

*   **Governing Representation**: Galerkin projection of the incompressible Navier-Stokes equations onto $9$ Fourier modes $\mathbf{u}_j(\mathbf{x})$:
    $$\tilde{\mathbf{u}}(\mathbf{x}, t) = \sum_{j=1}^9 a_j(t) \mathbf{u}_j(\mathbf{x})$$
    where $a_j(t) \in \mathbb{R}$ for $j=1,\dots,9$ are the time-dependent mode amplitudes governed by a system of 9 coupled nonlinear Ordinary Differential Equations (ODEs).
*   **Domain Geometry**: Spatial coordinates $\mathbf{x} = (x, y, z)^T$ in streamwise ($x$), wall-normal ($y$), and spanwise ($z$) directions:
    $$L_x = 4\pi, \quad L_y = 2, \quad L_z = 2\pi$$
*   **Flow Parameters & Regime**:
    *   Model Reynolds Number: $Re = \frac{U_0 h}{\nu} = 400$, defined using channel full height $2h$ (half-height $h$) and laminar reference velocity $U_0$ at $y = h/2$ from the top wall.
    *   Boundary Conditions: Free-slip at $y = \pm 1$; periodic in $x$ and $z$.
*   **Data Generation Details**:
    *   Integration length per trajectory: $T = 4000$ time units ($h/U_0$).
    *   Sampling interval: $\Delta t = 1.0$ time unit.
    *   Dataset size: Over $10,000$ independent turbulent trajectories ($N_s = 4000$ steps per trajectory).
    *   Initial Conditions ($t=0$):
        $$(a_1^0, a_2^0, a_3^0, a_4^0, a_5^0, a_6^0, a_7^0, a_8^0, a_9^0) = (1.0, \, 0.07066, \, -0.07076, \, \delta a_4, \, 0, \, 0, \, 0, \, 0, \, 0)$$
        where $\delta a_4 \sim \mathcal{U}(-\epsilon, \epsilon)$ is a random zero-mean perturbation. Non-sustained turbulent orbits (decaying to laminar or periodic states) are discarded.

---

## 2. Network Architectures

Two core neural network topologies are implemented to predict $a_j(t)$ sequentially:

### A. Multilayer Perceptron (MLP Baseline — Model `MLP4`)
*   **Input Dimension**: $d = m \times p = 9 \times 500 = 4500$, where $p=500$ lagged time steps are concatenated:
    $$\chi(t) = \left[ \mathbf{a}(t-p+1), \, \mathbf{a}(t-p+2), \, \dots, \, \mathbf{a}(t) \right]^T \in \mathbb{R}^{4500}$$
*   **Output Dimension**: $m = 9$, representing predicted mode coefficients $\mathbf{\zeta}(t+1) = \mathbf{a}(t+1) \in \mathbb{R}^9$.
*   **Layer Structure**: $l = 5$ hidden layers, each with $n = 90$ units.
    $$h^1 = \mathbf{W}^1 \chi + \mathbf{b}^1, \quad \zeta^1 = \tanh(h^1)$$
    $$h^i = \mathbf{W}^i \zeta^{i-1} + \mathbf{b}^i, \quad \zeta^i = \tanh(h^i) \quad \text{for } i = 2, \dots, 5$$
    $$\mathbf{a}_{\text{pred}}(t+1) = \mathbf{W}^{6} \zeta^5 + \mathbf{b}^6$$
*   **Weight Initialization**: Glorot (Xavier) normal distribution:
    $$W_{ij} \sim \mathcal{N}\left(0, \, \sigma^2\right), \quad \sigma = \sqrt{\frac{2}{n_{in} + n_{out}}}$$
*   **Optimizer**: Adam with standard adaptive settings.
*   **Regularization**: $L^2$ weight regularization combined with early stopping on validation loss ($20\%$ validation split).

### B. Long Short-Term Memory Network (LSTM — Model `LSTM1` & `LSTM2`)
*   **Input Context**: Sequence of length $p = 10$ time steps ($d = 9$ per step).
*   **Topology Options**:
    *   `LSTM1`: 1 hidden LSTM layer with $n_1 = 90$ units, followed by a dense linear layer to $m = 9$ outputs.
    *   `LSTM2`: 2 stacked hidden LSTM layers with $n_1 = 90$ and $n_2 = 90$ units, followed by a dense output layer ($m=9$).
*   **Recurrent Recurrence Equations** (per timestep $t$):
    $$f_t = \sigma\left(\mathbf{W}_f \mathbf{x}_t + \mathbf{U}_f \mathbf{h}_{t-1} + \mathbf{b}_f\right)$$
    $$i_t = \sigma\left(\mathbf{W}_i \mathbf{x}_t + \mathbf{U}_i \mathbf{h}_{t-1} + \mathbf{b}_i\right)$$
    $$\tilde{\mathbf{c}}_t = \tanh\left(\mathbf{W}_c \mathbf{x}_t + \mathbf{U}_c \mathbf{h}_{t-1} + \mathbf{b}_c\right)$$
    $$\mathbf{c}_t = f_t \odot \mathbf{c}_{t-1} + i_t \odot \tilde{\mathbf{c}}_t$$
    $$o_t = \sigma\left(\mathbf{W}_o \mathbf{x}_t + \mathbf{U}_o \mathbf{h}_{t-1} + \mathbf{b}_o\right)$$
    $$\mathbf{h}_t = o_t \odot \tanh(\mathbf{c}_t)$$
*   **Optimizer**: Adam optimizer. Training with $10,000$ datasets required $\sim 70$ hours on an Intel Core i7-4930K CPU.

---

## 3. Data Scaling & Normalization

*   **Non-Dimensionalization**:
    Length scale $h$, velocity scale $U_0$, time scale $t^* = h/U_0$.
    Coordinate space: $x^* = x/h \in [0, 4\pi]$, $y^* = y/h \in [-1, 1]$, $z^* = z/h \in [0, 2\pi]$.
*   **State Space Scaling**: Mode amplitudes $a_j(t)$ are maintained in physical non-dimensional units directly (no additional MinMax or $Z$-score scaling applied), as $a_1(t)$ operates around $a_{1,\text{lam}} = 1.0$ and remaining modes $a_2, \dots, a_9$ naturally fluctuate within $[-0.5, 0.5]$.

---

## 4. Required Physics Validation Gates

To validate model predictions beyond raw step-loss, model outputs must clear six physical gates calculated over ensembles of 500 test trajectories ($T=4000$):

1.  **Mean Velocity Field Error ($E_{\bar{u}}$)**:
    $$E_{\bar{u}} = \frac{1}{2 \max(\bar{u}_{\text{mod}})} \int_{-1}^1 \left| \bar{u}_{\text{mod}}(y) - \bar{u}_{\text{pred}}(y) \right| dy \le 0.5\% \quad (\text{Target for LSTM1 w/ 10k trajectories: } 0.45\%)$$

2.  **Streamwise Velocity Fluctuation Error ($E_{u'^2}$)**:
    $$E_{u'^2} = \frac{1}{\max(u'^2_{\text{mod}})} \int_{-1}^1 \left| u'^2_{\text{mod}}(y) - u'^2_{\text{pred}}(y) \right| dy \le 2.5\% \quad (\text{Target for LSTM1 w/ 10k trajectories: } 2.49\%)$$

3.  **Vorticity Fluctuation Profile Errors**:
    Relative errors in RMS spatial vorticity components $\omega_{x,\text{rms}}, \omega_{y,\text{rms}}, \omega_{z,\text{rms}}$:
    $$\text{Errors: } \varepsilon(\omega_{x,\text{rms}}) \le 0.6\%, \quad \varepsilon(\omega_{y,\text{rms}}) \le 0.7\%, \quad \varepsilon(\omega_{z,\text{rms}}) \le 1.3\%$$

4.  **Integrated Streamwise Momentum Balance**:
    Total shear stress profile must satisfy the analytical momentum balance:
    $$\tau_{\text{total}}(y) = \frac{1}{Re} \frac{d\bar{u}}{dy} - \overline{u'v'} = \frac{2\sqrt{2}\pi}{4 Re} \cos\left(\frac{\pi y}{2}\right)$$
    The amplitude error relative to the theoretical analytical constant must be $\le 3.1\%$.

5.  **Attractor Topology via Poincaré Section**:
    Probability Density Function (PDF) matching on the hyperplane intersection:
    $$\Sigma = \left\{ (a_1, a_3) \in \mathbb{R}^2 \; \middle| \; a_2 = 0, \, \frac{da_2}{dt} < 0 \right\}$$
    PDF of predicted trajectories must visually coincide with true attractor distribution.

6.  **Lyapunov Exponent Spectrum ($\lambda$)**:
    Rate of divergence $|\delta \mathbf{A}(t)| = \left[ \sum_{i=1}^9 (a_{i,1}(t) - a_{i,2}(t))^2 \right]^{1/2}$ for an initial perturbation $|\delta \mathbf{A}_0| = 10^{-6}$:
    $$|\delta \mathbf{A}(t')| = \exp(\lambda t') |\delta \mathbf{A}_0| \implies \lambda_{\text{pred}} \approx 0.0264 \quad (\text{Reference: } \lambda_{\text{mod}} = 0.0296)$$

---

## 5. Architectural Innovations & Edge Cases

*   **Sequence Context Reduction via Recurrence**:
    The MLP requires a massive sliding window context ($p=500$, $d=4500$) to achieve basic convergence, yet yields poor second-order statistics ($E_{u'^2} = 18.61\%$). In contrast, an LSTM processes sequence history via internal cell state vectors $\mathbf{c}_t$, reducing the explicit input sequence length to $p=10$ ($d=9$), while achieving $E_{u'^2} = 2.49\%$.
*   **Chaotic Trajectory Divergence (Positive Lyapunov Exponent Edge Case)**:
    Pointwise temporal error $e_1 = \frac{1}{(N_s - p)a_{1,\text{lam}}} \sum_{j=p+1}^{N_s} |a_{1,\text{mod}}^j - a_{1,\text{pred}}^j|$ remains high ($\approx 13.08\%$) even for validation losses as low as $5.2 \times 10^{-9}$. This is **not** an architectural failure, but a physical consequence of system chaos ($\lambda > 0$). Machine learning evaluation for chaotic fluid systems must rely on invariant measure statistical metrics (attractors, moments, exponents) rather than deterministic trajectory correlation over long time horizons.

---

## 6. Raw Data Corrections Log

*   **Equation 3 / Equation 5 Normalization Factor**: Corrected LaTeX notation from the raw extraction where $a 0 1$ and $a_{1,lam}$ were mixed; standardized to $a_{1,\text{lam}} = 1$.
*   **Total Shear Stress Balance Equation (Section III)**: Reconstructed the broken derivative inline text `1/Re d u/d y − uv` into explicit differential notation: $\frac{1}{Re}\frac{d\bar{u}}{dy} - \overline{u'v'}$.
*   **Poincaré Map Hyperplane Condition**: Restored missing derivative sign in section definition: fixed text `da2/dt < 0` to explicit LaTeX operator $\frac{da_2}{dt} < 0$.
*   **Initial Conditions Parameter**: Corrected OCR artifact `(a 0 1 , a 0 2 ...)` to standard notation $(a_1^0, a_2^0, a_3^0, a_4^0, a_5^0, a_6^0, a_7^0, a_8^0, a_9^0)$.