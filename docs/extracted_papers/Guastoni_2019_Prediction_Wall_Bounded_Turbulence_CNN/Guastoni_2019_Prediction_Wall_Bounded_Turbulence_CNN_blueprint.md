## 1. Physical Problem Statement

* **Flow Regime & Geometry:** Turbulent open-channel flow driven at constant mass flow rate.
  * Wall-normal domain: No-slip condition at $y = 0$, symmetry (free-slip) condition at upper boundary $y = h$.
  * Boundary conditions: Periodic in streamwise ($x$) and spanwise ($z$) directions.
  * Spatial domain size: $\Omega = L_x \times L_y \times L_z = 2\pi h \times h \times \pi h$.
* **Governing Parameters:**
  * Friction Reynolds number: $Re_\tau = \frac{u_\tau h}{\nu} = 180$.
  * Target plane heights (inner-scaled): $y^+ \in \{15, 30, 50\}$, where $y^+ = \frac{y u_\tau}{\nu}$.
* **Numerical Source Data (DNS):**
  * Solver: Pseudospectral code `SIMSON`.
  * Spatial discretization: $N_x = 128$ Fourier modes, $N_y = 129$ Chebyshev polynomials, $N_z = 128$ Fourier modes (3/2 dealiasing rule in $x, z$).
  * Temporal advancing: 3rd-order Runge-Kutta for non-linear terms, 2nd-order Crank-Nicolson for linear terms.
  * Sampling intervals evaluated: $\Delta t_s^+ \in \{0.56, 1.69, 5.08, 15.25\}$.
  * Dataset partition: 25,200 total snapshots split 4:1 for training (20,160) and validation (5,040). Testing data extracted from an independent DNS run generated with a distinct random seed.
* **Mapping Objective:** Predict instantaneous 2D streamwise velocity fields $u(x, z)\vert_{y^+}$ from two 2D wall-shear-stress component input fields at the wall ($y=0$):
  $$\mathbf{X}(x, z) = \left[ \tau_x(x, z)\vert_{y=0},\, \tau_z(x, z)\vert_{y=0} \right] \in \mathbb{R}^{2 \times N_x \times N_z} \longrightarrow \mathbf{Y}(x, z) = u(x, z)\vert_{y^+} \in \mathbb{R}^{1 \times N_x \times N_z}$$

---

## 2. Network Architectures

### 2.1 Single-Output Fully Convolutional Network (FCN)
* **Input Tensor Shape:** $\mathbb{R}^{2 \times 156 \times 156}$ (includes 14-grid-point periodic padding on each boundary for $N_x = N_z = 128$).
* **Topology:**
  * Layer 1: Conv2D ($5 \times 5$ kernel), Batch Normalization, ReLU.
  * Layers 2 to $N-1$: Conv2D ($3 \times 3$ kernels), Batch Normalization, ReLU.
  * Final Layer: Conv2D ($3 \times 3$ kernel), Linear activation (outputs 1 channel corresponding to $u^+$ at $y^+$).
* **Output Tensor Shape:** $\mathbb{R}^{1 \times 128 \times 128}$.
* **Optimizer & Hyperparameters:**
  * Algorithm: Adam optimizer with default parameters ($\beta_1 = 0.9$, $\beta_2 = 0.999$, $\epsilon = 10^{-8}$).
  * Learning rate schedule: Exponential decay.
  * Training duration: 100 epochs per run; ensemble averaged over 5 random weight initializations.

### 2.2 Multiple-Output Branching FCN
* **Shared Representation:** Common convolutional trunk processes input $\mathbf{X}$ to extract low-level spatial shear-stress features.
* **Branching Structure:** Splits into two parallel, dedicated convolutional sub-networks to simultaneously predict velocity fields at $y_1^+ = 15$ and $y_2^+ \in \{30, 50\}$.
* **Loss Combination:** Joint gradient update with equal weight allocation:
  $$\mathcal{L}_{\text{multi}} = 0.5 \cdot \mathcal{L}(u_{\text{FCN}}^{y_1^+}; u_{\text{DNS}}^{y_1^+}) + 0.5 \cdot \mathcal{L}(u_{\text{FCN}}^{y_2^+}; u_{\text{DNS}}^{y_2^+})$$

### 2.3 Fine-Tuning via Transfer Learning
* **Source Task:** FCN fully trained on $y^+ = 15$.
* **Target Task:** Fine-tuned prediction at $y^+ = 50$.
* **Optimization Protocol:** Initialize weights from $y^+ = 15$ model; freeze early feature-extraction layers; backpropagate loss exclusively through the final 3 convolutional layers using a reduced learning rate and rapid exponential decay.

---

## 3. Data Scaling & Normalization

* **Nondimensionalization:** All quantities are normalized by viscous inner scales:
  * Friction velocity: $u_\tau = \sqrt{\frac{\tau_w}{\rho}}$
  * Viscous length scale: $l^* = \frac{\nu}{u_\tau}$
* **Input Field Normalization:**
  $$\tau_x^+ = \frac{\tau_x}{\rho u_\tau^2}, \quad \tau_z^+ = \frac{\tau_z}{\rho u_\tau^2}$$
* **Output Target Scaling:**
  $$u^+ = \frac{u}{u_\tau}$$
* **Spatial Padding:** Periodic spatial padding of 14 points added symmetrically along $x$ and $z$ axes:
  $$\mathbf{X}_{\text{padded}}(x_i, z_j) = \mathbf{X}(x_i \bmod N_x, z_j \bmod N_z) \quad \text{for } -14 \le i < N_x + 14, \; -14 \le j < N_z + 14$$

---

## 4. Required Physics Validation Gates

### 4.1 Training Loss Metric
* Mean Squared Error (MSE) over the domain grid points:
  $$\mathcal{L}(u_{\text{FCN}}; u_{\text{DNS}}) = \frac{1}{N_x N_z} \sum_{j=1}^{N_x} \sum_{i=1}^{N_z} \left| u_{\text{FCN}}(i, j) - u_{\text{DNS}}(i, j) \right|^2$$

### 4.2 Statistical Validation Metrics
* **Relative Error on Mean Streamwise Velocity:**
  $$E_{\langle u \rangle^+} = \frac{\left| \langle u_{\text{FCN}} \rangle^+ - \langle u_{\text{DNS}} \rangle^+ \right|}{\langle u_{\text{DNS}} \rangle^+}$$
* **Relative Error on Streamwise Velocity Fluctuation Intensity ($u_{\text{RMS}}^+$):**
  $$E_{u_{\text{RMS}}^+} = \frac{\left| u_{\text{RMS, FCN}}^+ - u_{\text{RMS, DNS}}^+ \right|}{u_{\text{RMS, DNS}}^+}, \quad \text{where } u_{\text{RMS}}^+ = \sqrt{\frac{1}{N_x N_z} \sum_{i,j} (u^+(i,j) - \langle u \rangle^+)^2}$$

### 4.3 Baseline Comparison (Linear Stochastic Estimation - LSE)
* Linear reconstruction operator $\mathbf{L}$ derived from cross-correlation tensors:
  $$\langle \mathbf{E}^T \mathbf{E} \rangle \mathbf{L} = \langle u_{\text{DNS}}^T \mathbf{E} \rangle \implies u_{\text{LSE}} = \mathbf{L} \mathbf{E}$$
  where $\mathbf{E} = [\tau_x^+, \tau_z^+]^T$.

### 4.4 Quantitative Benchmark Performance Summary

| Model / Baseline | Sampling $\Delta t_s^+$ | Plane $y^+$ | $E_{\langle u \rangle^+} [\%]$ | $E_{u_{\text{RMS}}^+} [\%]$ |
| :--- | :--- | :--- | :--- | :--- |
| **LSE (Linear)** | $0.56$ | $15$ | $1.55$ | $9.14$ |
| **LSE (Linear)** | $0.56$ | $30$ | $1.33$ | $24.50$ |
| **LSE (Linear)** | $0.56$ | $50$ | $1.37$ | $35.90$ |
| **FCN (Single Output)** | $15.25$ | $15$ | $0.66 \pm 0.70$ | $2.11 \pm 0.90$ |
| **FCN (Single Output)** | $15.25$ | $30$ | $0.81 \pm 0.47$ | $10.65 \pm 2.11$ |
| **FCN (Single Output)** | $15.25$ | $50$ | $0.31 \pm 0.23$ | $25.57 \pm 1.92$ |
| **FCN (Multi-Output $15, 30$)** | $15.25$ | $15$ / $30$ | $1.13 \pm 0.67$ / $0.52 \pm 0.53$ | $2.79 \pm 0.80$ / $10.54 \pm 1.22$ |
| **FCN (Multi-Output $15, 50$)** | $15.25$ | $15$ / $50$ | $1.03 \pm 0.25$ / $0.21 \pm 0.22$ | $1.79 \pm 1.05$ / $24.46 \pm 1.68$ |
| **FCN (Transfer Learning)** | $5.08$ | $50$ | $0.50$ | $30.20$ |

---

## 5. Architectural Innovations & Edge Cases

* **Fully-Convolutional Non-Linear Reconstruction:** Replaces fully-connected/dense layers with spatial convolutions to retain structural grid integrity, reducing trainable parameter count and enabling scaling across spatial dimensions.
* **Input Temporal Decorrelation:**
  * Training on temporally close samples ($\Delta t_s^+ = 0.56, 1.69$) leads to severe overfitting due to high sample correlation (validation loss diverges with epoch count).
  * Training on temporally decorrelated samples ($\Delta t_s^+ = 15.25$) eliminates the generalization gap, making the model network-capacity limited rather than data limited.
* **Transfer Learning Speedup:**
  * Fine-tuning the $y^+=15$ pre-trained weights for the $y^+=50$ target task requires updating only the last 3 convolutional layers.
  * Reduces total training compute wall-clock time to $23\%$ of the baseline (a $>4\times$ speedup) while achieving a target MSE of $3.17 \times 10^{-3}$ vs $3.04 \times 10^{-3}$ for full retrain.
* **Receptive Field Limitations on Periodicity:**
  * Standard $14$-point periodic padding prevents boundary artifacts, but true periodicity preservation requires padding matching or exceeding the full theoretical receptive field footprint of the network.

---

## 6. Raw Data Corrections Log

* **Table 1 Text Fragmentation Fixes:**
  * Re-assembled fragmented column headings and entry values for relative errors $E_{\langle u \rangle^+}$ and $E_{u_{\text{RMS}}^+}$.
  * Reconstructed LSE baseline error values at $y^+ = 15, 30, 50$ ($9.14\%, 24.5\%, 35.9\%$).
  * Reconstructed standard deviation ranges for FCN single-output metrics across $\Delta t_s^+$ variants.
* **Table 2 Text Extraction Fixes:**
  * Corrected corrupted multi-output table strings for $y^+ = (15, 30)$ and $y^+ = (15, 50)$ pairings into structured numeric evaluations.
* **Equation Reconstruction:**
  * Reconstructed mathematical formulation for the LSE system equation:
    $$\langle \mathbf{E}^T \mathbf{E} \rangle \mathbf{L} = \langle u^T \mathbf{E} \rangle$$
  * Restored equation subscript formatting for mean squared loss $\mathcal{L}(u_{\text{FCN}}; u_{\text{DNS}})$ and relative error metrics $E_{\langle u \rangle^+}$, $E_{u_{\text{RMS}}^+}$.