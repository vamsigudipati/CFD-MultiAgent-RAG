## 1. Physical Problem Statement

* **Flow Domain & Regime:** Direct Numerical Simulation (DNS) of an incompressible turbulent open-channel flow using a pseudo-spectral code (SIMSON).
  * **Boundary Conditions:** Periodic in streamwise ($x$) and spanwise ($z$) directions; no-slip at lower wall ($y = 0$); symmetry condition at upper boundary ($y = h$). Constant mass flow rate.
  * **Domain Dimensions:** $L_x \times L_y \times L_z = 4\pi h \times h \times 2\pi h$.
* **Flow Configurations:**
  * **$Re_\tau = 180$:** Mesh resolution $N_x \times N_y \times N_z = 192 \times 65 \times 192$. Dataset contains 50,400 training/validation snapshots ($\Delta t_s^+ = 5.08$) and 3,125 uncorrelated test snapshots ($\Delta t_s^+ = 1.69$).
  * **$Re_\tau = 550$:** Mesh resolution $N_x \times N_y \times N_z = 512 \times 193 \times 512$. Dataset contains 19,920 training/validation snapshots ($\Delta t_s^+ = 1.49$) and 3,320 test snapshots ($\Delta t_s^+ = 1.49$).
  * **Train/Validation Split:** 4:1 ratio.
* **Input Features:** 2D wall measurements at $y = 0$: streamwise wall-shear stress ($\tau_{w,x}$), spanwise wall-shear stress ($\tau_{w,z}$), and wall pressure ($p_w$). Input shape: $(3, N_x, N_z)$.
* **Target Outputs:** 2D velocity fluctuation fields $(u, v, w)$ evaluated at target wall-normal planes: $y^+ \in \{15, 30, 50, 100\}$.

---

## 2. Network Architectures

### 2.1 Fully-Convolutional Neural Network (FCN)
Directly maps 2D wall inputs to 2D velocity fluctuation fields $(u, v, w)$ at target wall-normal locations.
* **Input Layer:** 3 channels $(\tau_{w,x}, \tau_{w,z}, p_w)$, padded periodically with 16 grid points in $x$ and $z$.
* **Hidden Layers (Sequential 2D Convolutions):**
  1. `Conv2D`: 64 filters, kernel size $5 \times 5$, stride 1, Batch Normalization, ReLU.
  2. `Conv2D`: 128 filters, kernel size $3 \times 3$, stride 1, Batch Normalization, ReLU.
  3. `Conv2D`: 256 filters, kernel size $3 \times 3$, stride 1, Batch Normalization, ReLU.
  4. `Conv2D`: 256 filters, kernel size $3 \times 3$, stride 1, Batch Normalization, ReLU.
  5. `Conv2D`: 128 filters, kernel size $3 \times 3$, stride 1, Batch Normalization, ReLU.
* **Output Layer:**
  * `Conv2D`: 3 filters ($\hat{u}, \hat{v}, \hat{w}$), kernel size $3 \times 3$, linear activation. Output is cropped to match target resolution $(N_x, N_z)$.
* **Receptive Field:** $15 \times 15$ grid points.
* **Trainable Parameters:** 1,264,131.
* **Optimization Setup:** Adam optimizer, exponential decay learning rate, trained for 50 epochs.

### 2.2 FCN-POD Network
Predicts snapshot-wise Proper Orthogonal Decomposition (POD) temporal coefficients $a_i(t)$ across spatial subdomains.
* **Domain Sub-division (Subdomains):**
  * $Re_\tau = 180$: $12 \times 12$ subdomains of spatial extent $\approx h \times 0.5h$.
  * $Re_\tau = 550$: $32 \times 32$ subdomains of spatial extent $\approx 0.4h \times 0.2h$.
* **Truncated Modes ($N_r$):** Retains $\approx 90\%$ TKE energy.
  * $Re_\tau = 180$: $N_r = 64$ modes.
  * $Re_\tau = 550$: $N_r = 128$ modes.
* **Hidden Layers:** Convolutional layers combined with Max Pooling, Batch Normalization, and ReLU activations.
* **Output Representation:** Predicts a tensor of size $N_{s_x} \times N_{s_z} \times N_r$. Reconstructs velocity fluctuations via linear combination:
  $$\mathbf{u}(\mathbf{x}, t) = \sum_{i=1}^{N_r} a_i(t) \sigma_i \boldsymbol{\phi}_i(\mathbf{x})$$
* **Trainable Parameters:** 4,733,248 ($Re_\tau = 180$); 5,028,224 ($Re_\tau = 550$).
* **Optimizer:** Adam with hyperparameter $\hat{\epsilon} = 0.1$.

---

## 3. Data Scaling & Normalization

* **Input Normalization:** Zero-mean, unit-variance standardization per feature channel $I \in \{\tau_{w,x}, \tau_{w,z}, p_w\}$ based on training set statistics:
  $$\tilde{I}(x, z) = \frac{I(x, z) - \mu_I}{\sigma_I}$$
* **FCN Output Scaling:** Equalizes error gradients across velocity components by scaling targets relative to streamwise RMS intensity:
  $$\hat{u} = u, \quad \hat{v} = v \frac{u_{\text{RMS}}}{v_{\text{RMS}}}, \quad \hat{w} = w \frac{u_{\text{RMS}}}{w_{\text{RMS}}}$$
  * *Inference:* Predicted outputs are multiplied by $v_{\text{RMS}} / u_{\text{RMS}}$ and $w_{\text{RMS}} / u_{\text{RMS}}$ respectively to recover physical magnitudes.
* **FCN-POD Output Scaling:** Velocity components remain unscaled to preserve the physical Turbulent Kinetic Energy (TKE) norm in the snapshot matrix correlation $\mathbf{C} = \mathbf{U}^T \mathbf{U}$.
* **FCN Loss Function (Mean Squared Error):**
  $$\mathcal{L}_{\text{FCN}}(\hat{\mathbf{u}}_{\text{FCN}}; \hat{\mathbf{u}}_{\text{DNS}}) = \frac{1}{N_x N_z} \sum_{i=1}^{N_x} \sum_{j=1}^{N_z} |\hat{\mathbf{u}}_{\text{FCN}}(i, j) - \hat{\mathbf{u}}_{\text{DNS}}(i, j)|^2$$
* **FCN-POD Loss Function:**
  $$\mathcal{L}_{\text{FCN-POD}}(a_{\text{POD}}; a_{\text{DNS}}) = \frac{1}{N_{s_x} N_{s_z} N_r} \sum_{i=1}^{N_{s_x}} \sum_{j=1}^{N_{s_z}} \sum_{k=1}^{N_r} |a_{\text{POD}}(i, j, k) - a_{\text{DNS}}(i, j, k)|^2$$

---

## 4. Required Physics Validation Gates

1. **Instantaneous Field Error:** Mean-squared-error $L_2$ evaluation across test fields for each velocity fluctuation component.
2. **Turbulence Statistics Validation:** Relative RMS profile error relative to DNS ground truth:
   $$E_{\text{RMS}}^+(u) = \frac{\left| u_{\text{RMS,Pred}}^+ - u_{\text{RMS,DNS}}^+ \right|}{u_{\text{RMS,DNS}}^+}$$
   * Model outputs must capture near-wall velocity intensities within $y^+ \le 30$ ($E_{\text{RMS}}^+ < 3\%$ for FCN at $y^+=15$).
3. **Power-Spectral Density ($\phi_{uu}, \phi_{vv}, \phi_{ww}$):** Pre-multiplied 2D energy spectra $k_x k_z \phi_{ij}$ compared against 10%, 50%, and 90% energy contours of DNS ground truth. Models must accurately reconstruct energy distribution across spatial wavelengths $(\lambda_x^+, \lambda_z^+)$.
4. **Coherent Structure Inclination Angle:** Alignment checking via cross-correlation $R_{ij}(\delta x)$ between wall inputs and velocity outputs to monitor the characteristic $\approx 15^\circ$ structural slope angle.

---

## 5. Architectural Innovations & Edge Cases

* **Exact Spatial Periodicity via Padding:** Rather than penalizing boundary mismatches soft-wise in the loss function, input fields are padded using wrap-around (circular) padding matching half the receptive field size (16 points total padding). This enforces hard periodic boundary conditions.
* **Joint Multi-Component Backpropagation:** Shared lower-convolutional representations trained simultaneously on all three velocity components $(\hat{u}, \hat{v}, \hat{w})$ outperform branching output heads, leveraging cross-component physical causality.
* **Subdomain POD Tiling (FCN-POD):** Dividing large fields into subdomains compresses the eigenvalue energy spectrum, allowing 64 modes ($Re_\tau=180$) and 128 modes ($Re_\tau=550$) to capture $90\%$ of total TKE.
* **Subdomain Interface Discontinuities:** FCN-POD tile reconstruction introduces localized high-frequency jumps at subdomain boundaries ($\lambda_x^+ \approx 180$ at $Re_\tau=180$, $\lambda_x^+ \approx 200$ at $Re_\tau=550$).
* **Cross-Reynolds Number Transfer Learning:** Transferring pre-trained weights from $Re_\tau = 180$ to initialize training at $Re_\tau = 550$ allows the network to match full-dataset validation accuracy up to $y^+ = 50$ using only $25\%$ to $50\%$ of the target training dataset, provided a reduced learning rate is applied.

---

## 6. Raw Data Corrections Log

* **Table 1 Resolution Formats:** Reconstruction of raw extraction missing grid parameters. Reconstructed $N_x \times N_y \times N_z = 192 \times 65 \times 192$ for `DNS180` and $512 \times 193 \times 512$ for `DNS550` based on textual references to domain size and Chebyshev/Fourier mode counts.
* **Equation (2.2) Formatting Fix:** Reconstructed corrupted text variable bindings for scaling equations: $\hat{u} = u$, $\hat{v} = v \frac{u_{\text{RMS}}}{v_{\text{RMS}}}$, and $\hat{w} = w \frac{u_{\text{RMS}}}{w_{\text{RMS}}}$.
* **Loss Function Equations (2.3 & 2.7):** Corrected missing summation indices and target notation vectors from raw markdown string fragments into valid standard LaTeX notation.