## 1. Physical Problem Statement

* **Flow Regime:** Incompressible turbulent open channel flow.
* **Governing Equations:** Incompressible Navier-Stokes equations:
  $$\nabla \cdot \mathbf{u} = 0$$
  $$\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla)\mathbf{u} = -\frac{1}{\rho}\nabla p + \nu \nabla^2 \mathbf{u}$$
* **Reynolds Number:** Friction Reynolds number based on channel height $h$ and friction velocity $u_\tau$:
  $$Re_\tau = \frac{u_\tau h}{\nu} = 180$$
* **Computational Domain:**
  $$\Omega = L_x \times L_y \times L_z = 2\pi h \times h \times \pi h$$
* **Boundary Conditions:**
  * **Streamwise ($x$) and Spanwise ($z$):** Periodic boundary conditions.
  * **Wall-normal ($y$):** No-slip condition at the lower wall ($y = 0$); symmetry condition at the upper boundary ($y = h$).
* **DNS Numerical Solver & Discretization:**
  * Pseudospectral solver SIMSON.
  * Grid resolution: $N_x \times N_y \times N_z = 128 \times 129 \times 128$ ($129$ Chebyshev modes in $y$, $128 \times 128$ Fourier modes in $x, z$).
  * Dealiasing: $3/2$-rule in $x$ and $z$.
  * Time advancing: 2nd-order Crank-Nicolson for linear terms, 3rd-order Runge-Kutta for non-linear terms at constant mass flow rate.
  * DNS base sampling interval: $\Delta t^+ = 0.56$.
* **Target Prediction Task:** Reconstruct instantaneous 2D streamwise velocity fields $u^+(x, z)$ at wall-normal locations $y^+ \in \{15, 30, 50\}$ using 2D wall-shear-stress component fields in the streamwise ($\tau_{w,x}^+(x, z)$) and spanwise ($\tau_{w,z}^+(x, z)$) directions.

---

## 2. Network Architectures

* **Model Type:** Fully-Convolutional Neural Network (FCN).
* **Input Tensor Shape:** $(B, C_{\text{in}}, H_{\text{in}}, W_{\text{in}}) = (B, 2, 128 + 2\cdot 14, 128 + 2\cdot 14) = (B, 2, 156, 156)$ incorporating periodic boundary padding.
  * Channels: Channel 0 = $\tau_{w,x}^+(x, z)$, Channel 1 = $\tau_{w,z}^+(x, z)$.
* **Output Tensor Shape:** $(B, C_{\text{out}}, H_{\text{out}}, W_{\text{out}}) = (B, 1, 128, 128)$ for single-output FCN, predicting instantaneous $u^+(x, z)$ at a specified $y^+$.
* **Detailed Layer Architecture (Single-Output FCN):**
  1. **Conv2D Layer 1:** $C_{\text{in}} = 2 \to C_{\text{out}} = 64$, Kernel Size $= 5 \times 5$, Stride $= 1$, Padding $= 0$ $\to$ Batch Normalization $\to$ ReLU
  2. **Conv2D Layer 2:** $C_{\text{in}} = 64 \to C_{\text{out}} = 128$, Kernel Size $= 3 \times 3$, Stride $= 1$, Padding $= 0$ $\to$ Batch Normalization $\to$ ReLU
  3. **Conv2D Layer 3:** $C_{\text{in}} = 128 \to C_{\text{out}} = 256$, Kernel Size $= 3 \times 3$, Stride $= 1$, Padding $= 0$ $\to$ Batch Normalization $\to$ ReLU
  4. **Conv2D Layer 4:** $C_{\text{in}} = 256 \to C_{\text{out}} = 128$, Kernel Size $= 3 \times 3$, Stride $= 1$, Padding $= 0$ $\to$ Batch Normalization $\to$ ReLU
  5. **Conv2D Layer 5:** $C_{\text{in}} = 128 \to C_{\text{out}} = 64$, Kernel Size $= 3 \times 3$, Stride $= 1$, Padding $= 0$ $\to$ Batch Normalization $\to$ ReLU
  6. **Conv2D Layer 6 (Output Layer):** $C_{\text{in}} = 64 \to C_{\text{out}} = 1$, Kernel Size $= 3 \times 3$, Stride $= 1$, Padding $= 0$ (Linear Activation)
* **Optimization & Training Hyperparameters:**
  * **Optimizer:** Adam ($\beta_1 = 0.9, \beta_2 = 0.999, \epsilon = 10^{-8}$).
  * **Learning Rate Schedule:** Exponential learning-rate decay.
  * **Dataset Size:** $25,200$ DNS snapshots, split $4:1$ into $20,160$ training snapshots and $5,040$ validation snapshots.
  * **Test Dataset:** Separate DNS execution initialized with a distinct random seed to guarantee spatial/temporal independence.
  * **Epochs:** $100$ epochs per network. Statistics evaluated over an ensemble of $5$ independent weight initializations.

---

## 3. Data Scaling & Normalization

* **Non-Dimensionalization (Viscous Inner Units $^+$):**
  * **Length Scale:** $l^* = \frac{\nu}{u_\tau}$, where viscous distance $y^+ = \frac{y u_\tau}{\nu}$.
  * **Velocity Scale:** Friction velocity $u_\tau = \sqrt{\frac{\tau_w}{\rho}}$, where $\tau_w = \mu \left. \frac{\partial u}{\partial y} \right|_{y=0}$.
  * **Time Scale:** Inner time $t^+ = t \frac{u_\tau^2}{\nu}$.
* **Input Feature Fields:**
  * Streamwise wall-shear stress: $\tau_{w,x}^+(x, z) = \left. \frac{\partial u^+}{\partial y^+} \right|_{y^+=0}$
  * Spanwise wall-shear stress: $\tau_{w,z}^+(x, z) = \left. \frac{\partial w^+}{\partial y^+} \right|_{y^+=0}$
* **Target Output Field:**
  * Streamwise velocity fluctuation/total field $u^+(x, z)$ at target $y^+ \in \{15, 30, 50\}$.
* **Spatial Grid Processing:** Input dimensions match spatial Fourier modes ($128 \times 128$) extended via periodic wrapping prior to feeding through unpadded convolutional layers.

---

## 4. Required Physics Validation Gates

* **Objective Loss Function (Training Gate):** Mean Squared Error (MSE) over the horizontal domain:
  $$\mathcal{L}(u_{\text{FCN}}; u_{\text{DNS}}) = \frac{1}{N_x N_z} \sum_{j=1}^{N_x} \sum_{i=1}^{N_z} \left| u_{\text{FCN}}(i, j) - u_{\text{DNS}}(i, j) \right|^2$$

* **Statistical Physics Validation Metrics:**
  1. **Relative Mean Streamwise Velocity Error:**
     $$E_{\langle u \rangle^+} = \frac{\left| \langle u_{\text{FCN}} \rangle^+ - \langle u_{\text{DNS}} \rangle^+ \right|}{\langle u_{\text{DNS}} \rangle^+}$$
  2. **Relative Streamwise Turbulence Intensity Error:**
     $$E_{u_{\text{RMS}}^+} = \frac{\left| u_{\text{RMS, FCN}}^+ - u_{\text{RMS, DNS}}^+ \right|}{u_{\text{RMS, DNS}}^+}, \quad \text{where } u_{\text{RMS}}^+ = \sqrt{\langle (u^+ - \langle u^+ \rangle)^2 \rangle}$$

* **Baseline Benchmark (Linear Stochastic Estimation - LSE):**
  * Linear estimator $u \approx \mathbf{L} E$, where $E = [\tau_{w,x}^+, \tau_{w,z}^+]^T$.
  * Operator computed via least-squares tensor system:
    $$\langle E^T E \rangle \mathbf{L} = \langle u^T E \rangle$$
  * Comparison Baseline Performance ($\Delta t^+ = 0.56$):
    * $y^+ = 15$: $E_{\langle u \rangle^+} = 1.55\%$, $E_{u_{\text{RMS}}^+} = 9.14\%$
    * $y^+ = 30$: $E_{\langle u \rangle^+} = 1.33\%$, $E_{u_{\text{RMS}}^+} = 24.5\%$
    * $y^+ = 50$: $E_{\langle u \rangle^+} = 1.37\%$, $E_{u_{\text{RMS}}^+} = 35.9\%$

* **FCN Model Performance ($\Delta t^+ = 15.25$):**
  * $y^+ = 15$: $E_{\langle u \rangle^+} = 0.66 \pm 0.70\%$, $E_{u_{\text{RMS}}^+} = 2.11 \pm 0.90\%$
  * $y^+ = 30$: $E_{\langle u \rangle^+} = 0.81 \pm 0.47\%$, $E_{u_{\text{RMS}}^+} = 10.65 \pm 2.11\%$
  * $y^+ = 50$: $E_{\langle u \rangle^+} = 0.31 \pm 0.23\%$, $E_{u_{\text{RMS}}^+} = 25.57 \pm 1.92\%$

---

## 5. Architectural Innovations & Edge Cases

* **Periodic Edge Padding Strategy:**
  * Convolutional layers use valid convolutions ($p=0$). Total spatial size reduction across the 6 layers is $2 \cdot (2 + 1 + 1 + 1 + 1 + 1) = 14$ grid units per boundary ($28$ points total per axis).
  * Inputs are padded using periodic boundary values: $14$ grid points wrapped from opposing sides in both $x$ and $z$ directions, converting input dimensions from $128 \times 128$ to $156 \times 156$.
* **Multi-Output Shared-Backbone Architecture:**
  * Joint prediction of two planes simultaneously (e.g., $y^+ \in (15, 30)$ or $y^+ \in (15, 50)$).
  * Common convolutional backbone extracts shared low-level turbulent structures, splitting into two independent output branches.
  * Loss function combines branch losses with equal weighting:
    $$\mathcal{L}_{\text{multi}} = \mathcal{L}(u_{\text{FCN}, y_1^+}; u_{\text{DNS}, y_1^+}) + \mathcal{L}(u_{\text{FCN}, y_2^+}; u_{\text{DNS}, y_2^+})$$
  * Delivers a $12\%$ computational speedup over training separate networks with equivalent predictive accuracy.
* **Transfer Learning / Fine-Tuning across Wall-Normal Planes:**
  * Target plane $y^+ = 50$ initialized with optimal weights derived from source model trained at $y^+ = 15$.
  * Layers 1–3 are frozen; only the final 3 convolutional layers are fine-tuned using a reduced learning rate and accelerated decay.
  * Reduces total training runtime to **$23\%$** of full training ($4.35\times$ speedup), maintaining MSE $= 3.17 \times 10^{-3}$ vs. $3.04 \times 10^{-3}$ for fully trained baseline.
* **Temporal Sampling Decoupling ($\Delta t^+$ Sensitivity):**
  * Evaluated sampling gaps $\Delta t^+ \in \{0.56, 1.69, 5.08, 15.25\}$.
  * Increasing temporal separation lowers inter-sample correlation, preventing network overfitting and closing the training-to-validation loss gap without degrading statistical accuracy.

---

## 6. Raw Data Corrections Log

* **Reconstructed Fractured Tables:** Tables 1, 2, and 3 were severely fragmented due to multi-column OCR parsing. Restructured all values, standard deviations, and metric column alignments for $E_{\langle u \rangle^+}$, $E_{u_{\text{RMS}}^+}$, MSE, and Relative Time.
* **Restructured Equation 1:** Fixed broken math text $F_{i,j} = \sum_m \sum_n I_{i-m,j-n} K_{m,n}$ and clarified kernel indices.
* **Reconstructed Equation 4:** Corrected broken character formatting in the linear stochastic estimation system $\langle E^T E \rangle \mathbf{L} = \langle u^T E \rangle$.
* **Clarified Padding Specification:** Resolved text description vs diagram regarding output dimensions: input $128 \times 128$ is padded by 14 points on each side ($156 \times 156$) so that six successive unpadded conv operations yield an output exact size of $128 \times 128$.