## 1. Physical Problem Statement
* **Flow Domain & Regime:** Spatially evolving, statistically two-dimensional Zero-Pressure-Gradient (ZPG) Turbulent Boundary Layer (TBL) over a flat plate.
* **Governing Data Generation:** High-resolution Large-Eddy Simulation (LES) produced using the pseudo-spectral code SIMSON.
* **Domain Dimensions:** $L_x \times L_y \times L_z = 13500 \times 400 \times 540$ non-dimensionalized by inlet displacement thickness $\delta^*$.
* **Grid Resolution:** $13824 \times 513 \times 1152$ collocation points in $x, y, z$. Spanwise grid spacing $\Delta z^+ = 12$ across 768 physical domain points.
* **Reynolds Numbers Evaluated:**
  * Primary Design/Validation Baseline: $Re_\theta = 4430$ ($Re_\tau = 1324$).
  * Secondary / Robustness Cases: $Re_\theta = 2240$ ($Re_\tau = 704$), $Re_\theta = 8200$ ($Re_\tau = 2370$).
  * Low-$Re$ Training Set for Off-Design Transfers: $Re_\theta = 880$.
* **Target Output ($O(z,t)$):** Streamwise velocity fluctuation $u^+(z,t)$ in the near-wall buffer layer ($y_{out}^+ = 15$).
* **Input Measurements ($I(z,t)$):** Streamwise velocity fluctuations $u^+(z,t)$ at logarithmic/outer positions ($y_{in}^+ = 50, 75, 100, 150, 200$) or wall-shear stress fluctuations $\tau_w'(z,t)$.
* **Temporal Sampling:** $N = 19410$ time snapshots with spacing $\Delta t^+ = 0.5$. Data is split into $50\%$ training (model identification) and $50\%$ testing/validation.

---

## 2. Network Architectures

### 2.1 Single-Input Single-Output (SISO) Linear Transfer Kernel
The input $I(z,t)$ is mapped to output $O(z,t)$ via a double space-time convolution kernel $g_{IO}(z,t)$:
$$O(z, t) = g_{IO}(z, t) \otimes I(z, t) = \int_{-z_{max}/2}^{z_{max}/2} \int_{-\infty}^{\infty} g_{IO}(\zeta, \tau) I(z - \zeta, t - \tau) \, d\zeta \, d\tau$$

In the frequency-wavenumber domain $(\beta, \omega)$, the optimal $H^1$ transfer function estimator is computed as:
$$G_{IO}(\beta, \omega) = \frac{S_{IO}(\beta, \omega)}{S_{II}(\beta, \omega)}$$
where $S_{II}$ is the input auto-spectral density and $S_{IO}$ is the cross-spectral density. $g_{IO}(z,t)$ is retrieved via 2D Inverse Fast Fourier Transform (IFFT):
$$g_{IO}(z, t) = \int_{-\infty}^{+\infty} \int_{-\beta_n}^{+\beta_n} G_{IO}(\beta, \omega) e^{i\beta z} e^{-i\omega t} d\beta d\omega$$

### 2.2 Multiple-Input Single-Output (MISO) Linear Model
For $n$ inputs $I_i(z,t)$, the field superposition is expressed as:
$$O(z, t) = \sum_{i=1}^n g_{I_i O}(z, t) \otimes I_i(z, t)$$
The transfer functions vector $\mathbf{G}_O(\beta, \omega) = [G_{I_1 O}, G_{I_2 O}, \dots, G_{I_n O}]^T$ is solved per $(\beta, \omega)$ mode from:
$$\begin{pmatrix} S_{I_1 O}(\beta, \omega) \\ \vdots \\ S_{I_n O}(\beta, \omega) \end{pmatrix} = \begin{pmatrix} S_{I_1 I_1}(\beta, \omega) & \dots & S_{I_1 I_n}(\beta, \omega) \\ \vdots & \ddots & \vdots \\ S_{I_n I_1}(\beta, \omega) & \dots & S_{I_n I_n}(\beta, \omega) \end{pmatrix} \begin{pmatrix} G_{I_1 O}(\beta, \omega) \\ \vdots \\ G_{I_n O}(\beta, \omega) \end{pmatrix}$$

Inputs are decoupled using Spectral Conditioning ( Gram-Schmidt orthogonalization in spectral domain):
$$\hat{I}_{2-1}(\beta, \omega) = \hat{I}_2(\beta, \omega) - \frac{S_{I_1 I_2}(\beta, \omega)}{S_{I_1 I_1}(\beta, \omega)} \hat{I}_1(\beta, \omega)$$

### 2.3 Single-Input Non-Linear Polynomial Model (Volterra-Equivalent)
The single-input non-linear system $O(z,t) = g(I(z,t))$ is expanded into $N_{TF}$ polynomial terms:
$$O(z, t) = \sum_{i=1}^{N_{TF}} g_i\left(I^i(z, t)\right)$$
Synthetic inputs $\tilde{I}_i(z,t) = I^i(z,t)$ transform the system into an $N_{TF}$-input MISO system. Optimal truncation degree is quadratic ($N_{TF} = 2$):
$$O(z, t) = g_1(z,t) \otimes I(z,t) + g_2(z,t) \otimes \left(I^2(z,t)\right)$$

---

## 3. Data Scaling & Normalization
* **Viscous Inner Units (Superscript $+$):**
  * Friction velocity: $u_\tau = \sqrt{\tau_w / \rho}$
  * Viscous length scale: $l^* = \nu / u_\tau$
  * Viscous time scale: $t^* = \nu / u_\tau^2$
  * Variable non-dimensionalization: $y^+ = y/l^*$, $z^+ = z/l^*$, $t^+ = t/t^*$, $u^+ = u/u_\tau$.
* **Spectral Density Convergence (Welch’s Method):**
  * Time series segment length: $N_f = 256$ snapshots ($\Delta T^+ = 128$).
  * Overlap: $75\%$ ($N_o = 192$ snapshots).
  * Windowing: Triangular windowing applied along time blocks.
  * Frequency resolution: $\Delta \omega^+ = 0.05$.
  * Spanwise transformation: Spatial Discrete Fourier Transform (DFT) over 768 physical spanwise grid points.

---

## 4. Required Physics Validation Gates

```
                      +-----------------------------------+
                      |   Target Field Evaluation Gate    |
                      |        (y_out^+ = 15, u^+)        |
                      +-----------------------------------+
                                        |
       +--------------------------------+--------------------------------+
       |                                |                                |
[SISO Outer Input]            [SISO Wall Shear]             [MISO (4 Inputs)]
y_in^+ = 50                   Input: \tau_w                 \tau_w + y^+=[50,100,200]
       |                                |                                |
       v                                v                                v
Variance Rec: ~45%            Variance Rec: Underpredicted  Variance Rec: > 70%
Correlation:  0.62            Correlation:  0.79            Correlation:  0.82
e_MS Error:   55%             e_MS Error:   36%             e_MS Error:   33%
err_peak:     84%             err_peak:     27%             err_peak:     25%
       |                                |                                |
       +--------------------------------+--------------------------------+
                                        |
                                        v
                       +----------------------------------+
                       |    Quadratic Non-Linear Gate     |
                       |          (Input: \tau_w)         |
                       +----------------------------------+
                       | Variance Rec: Substantially Imp. |
                       | Correlation:  0.84               |
                       | e_MS Error:   31%                |
                       | err_peak:     20%                |
                       | err_mean:     36%                |
                       +----------------------------------+
```

1. **Normalized Space-Time Cross-Correlation ($Corr$):**
   $$Corr = \frac{\int_{-\pi}^{\pi} \int_{-\infty}^{\infty} O_{LES}(t, z) O_{est}(t, z) \, dt \, dz}{\sqrt{\int_{-\pi}^{\pi} \int_{-\infty}^{\infty} O_{LES}^2(t, z) \, dt \, dz} \sqrt{\int_{-\pi}^{\pi} \int_{-\infty}^{\infty} O_{est}^2(t, z) \, dt \, dz}}$$
   * Gate: $Corr \ge 0.80$ at $y_{out}^+ = 15$ for wall-shear stress input under MISO or non-linear models.

2. **Mean-Square Relative Error ($e_{MS}$):**
   $$e_{MS} = \frac{\int_{-z_{max}/2}^{z_{max}/2} \int_0^{t_{max}} \left(u_{est}^+(z,t) - u_{LES}^+(z,t)\right)^2 dt \, dz}{\int_{-z_{max}/2}^{z_{max}/2} \int_0^{t_{max}} \left(u_{est}^+(z,t)\right)^2 dt \, dz} \times 100\%$$
   * Target Benchmarks ($y_{out}^+ = 15$):
     * Linear SISO ($y_{in}^+ = 50$): $e_{MS} = 55\%$
     * Linear SISO ($\tau_w$ input): $e_{MS} = 36\%$
     * Linear MISO ($\tau_w + y_{in}^+=50$): $e_{MS} = 33\%$
     * Quadratic Non-linear ($\tau_w$ input): $e_{MS} = 31\%$

3. **Spectral Peak Relative Error ($err_{peak}$) & Mean Error ($err_{mean}$):**
   $$err_{mean} = \frac{\int_{\beta_1}^{\beta_2} \int_{\omega_1}^{\omega_2} E_{ee}(\omega, \beta) \, d\omega \, d\beta}{\int_{\beta_1}^{\beta_2} \int_{\omega_1}^{\omega_2} E_{uu}(\omega, \beta) \, d\omega \, d\beta} \times 100\%$$
   where $E_{ee}$ is the power spectrum of $e(z,t) = u_{est}^+(z,t) - u_{LES}^+(z,t)$.
   * Gate ($y_{out}^+ = 15$):
     * Linear SISO ($\tau_w$ input): $err_{peak} = 27\%$, $err_{mean} = 42\%$
     * Quadratic Non-linear ($\tau_w$ input): $err_{peak} = 20\%$, $err_{mean} = 36\%$

4. **Structure Inclination Angle $\theta$ Invariance:**
   For separation $\Delta y^+ = 35$ ($y_{in}^+=50 \to y_{out}^+=15$), measured kernel time delay $\Delta t^+ = 9.4$ at local convective speed $U_c^+ \approx 14$ yields:
   $$\theta = \arctan\left(\frac{\Delta y^+}{U_c^+ \cdot \Delta t^+}\right) = \arctan\left(\frac{35}{14 \cdot 9.4}\right) \approx 14.9^\circ$$

---

## 5. Architectural Innovations & Edge Cases

* **Directional Causality Dual-State:**
  * Downward Estimation ($y_{in}^+ > y_{out}^+$): Kernels are strictly causal ($g_{IO}(z,\tau) \approx 0$ for $\tau < 0$). This enables real-time closed-loop flow control without temporal lookahead.
  * Upward Estimation ($y_{in}^+ < y_{out}^+$ or wall-shear input $\tau_w$): Kernels are non-causal ($\tau < 0$). On-line implementation requires spatial streamwise offsets ($\Delta x > 0$) between sensor and estimator location to recover physical causality.
* **Overfitting via Higher Polynomial Order:**
  Expanding non-linear TFs beyond quadratic degree ($N_{TF} > 2$) causes time-domain performance degradation (correlation drops below $0.84$ and $e_{MS}$ increases beyond $31\%$) due to high-order noise amplifications. Truncation must be fixed at $N_{TF} = 2$.
* **Extreme Reynolds-Number Off-Design Generalization:**
  Models trained at $Re_\theta = 880$ and tested at $Re_\theta = 8200$ (spanning nearly an order of magnitude) preserve near-wall prediction fidelity ($Corr > 0.80$ near the wall; $Corr > 0.60$ up to $y^+ = 180$ using 4-input MISO). This verifies that the interaction kernel between wall shear and inner-layer velocity structures is $Re$-invariant.

---

## 6. Raw Data Corrections Log

* **Equation (3.1) Coherence Definition:** The double-hat symbol formatting was normalized to standard Fourier transform notation $\hat{u}(y, \omega, \beta)$.
* **Section 4.1, Equation (4.5):** Reconstructed the post-multiplication error derivation:
  $$S_{OI}(\beta, \omega) = G_{IO}(\beta, \omega) S_{II}(\beta, \omega) + S_{\epsilon I}(\beta, \omega)$$
  and validated that the $H^1$ estimator setting $S_{\epsilon I}(\beta, \omega) = 0$ yields the orthogonality of prediction error.
* **Appendix A, Equation (A4):** Corrected markdown artifact `(\mathbf{A} \mathbf{A})` to standard equation tag `(A4)`.
* **Appendix B, Equation (B3)–(B4):** Corrected indexing syntax for iterative spectral conditioning operators $I_{N-(N-1)!}$.