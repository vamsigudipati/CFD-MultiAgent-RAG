## 1. Physical Problem Statement

* **Flow Regime**: Incompressible, fully developed wall-bounded turbulent channel flow governed by the 3D incompressible Navier–Stokes equations:
  $$\nabla \cdot \mathbf{U} = 0$$
  $$\frac{\partial \mathbf{U}}{\partial t} + (\mathbf{U} \cdot \nabla)\mathbf{U} = -\frac{1}{\rho}\nabla P + \nu \nabla^2 \mathbf{U}$$
  Velocity decomposition: $\mathbf{U}(x,y,z,t) = \bar{\mathbf{U}}(y) + \mathbf{u}(x,y,z,t)$, where $\mathbf{u} = (u, v, w)^T$ are the fluctuating components in the streamwise ($x$), wall-normal ($y$), and spanwise ($z$) directions.

* **Simulation Setup (DNS via LISO Code)**:
  * **Numerical Discretization**: Seventh-point compact finite-difference scheme in the wall-normal direction $y$ (4th-order consistency, spectral-like resolution); Fourier spectral discretization in $x$ and $z$; 3rd-order semi-implicit Runge–Kutta temporal integration.
  * **Case 1 ($Re_\tau = 125$)**:
    * Friction Reynolds number: $Re_\tau = \frac{u_\tau h}{\nu} = 125$
    * Domain dimensions: $L_x \times L_y \times L_z = 8\pi h \times 2h \times 3\pi h$
    * Grid points: $N_x \times N_y \times N_z = 384 \times 201 \times 288$
    * Resolution: $\Delta x^+ \approx 8.2$, $\Delta z^+ \approx 4.1$, $\Delta y = 1.5\eta$ (where $\eta = (\nu^3 / \varepsilon)^{1/4}$)
  * **Case 2 ($Re_\tau = 550$)**:
    * Friction Reynolds number: $Re_\tau = \frac{u_\tau h}{\nu} = 550$
    * Domain dimensions: $L_x \times L_y \times L_z = 2\pi h \times 2h \times \pi h$
    * Grid points: $N_x \times N_y \times N_z = 384 \times 251 \times 384$
    * Resolution: $\Delta x^+ \approx 8.9$, $\Delta z^+ \approx 4.3$, $\Delta y = 1.5\eta$

* **Boundary Conditions**: Periodic in streamwise ($x$) and spanwise ($z$) directions; no-slip ($\mathbf{u} = \mathbf{0}$) at the bottom wall ($y^+ = 0$) and top wall ($y^+ = 2Re_\tau$).
* **Prediction Time Horizon**: Temporal forecasting of velocity fluctuation fields across interval $\Delta t^+ = \frac{\Delta t \cdot u_\tau^2}{\nu} = 5$.

---

## 2. Network Architectures

* **Model Type**: 3D Encoder-Decoder U-Net for spatial-temporal flow surrogate modeling.
* **Input Tensor**: $\mathbf{u}^t \in \mathbb{R}^{3 \times N_y \times N_z \times N_x}$ containing velocity fluctuation components $(u^t, v^t, w^t)$.
* **Output Tensor**: Predicted fluctuation field $\mathbf{u}^{t+\Delta t} \in \mathbb{R}^{3 \times N_y \times N_z \times N_x}$.

* **Layer & Channel Specifications**:
  * **Case $Re_\tau = 125$ (4-Level Architecture)**:
    * *Periodic Padding Layer*: Input padded from $201 \times 288 \times 384$ to $201 \times 318 \times 414$ along $z$ and $x$ axes.
    * *Encoder Level 1*: 2 $\times$ 3D Conv (32 filters), 3D Mean Pooling $\rightarrow$ Tensor shape: $100 \times 159 \times 207 \times 64$.
    * *Encoder Level 2*: 2 $\times$ 3D Conv (64 filters), 3D Mean Pooling $\rightarrow$ Tensor shape: $50 \times 79 \times 103 \times 128$.
    * *Encoder Level 3*: 2 $\times$ 3D Conv (128 filters), 3D Mean Pooling $\rightarrow$ Tensor shape: $25 \times 39 \times 51 \times 256$.
    * *Bottleneck (Level 4)*: 2 $\times$ 3D Conv (256 filters).
    * *Decoder Level 3*: Transposed 3D Conv + Channel Concatenation (Skip connection from Encoder L3) + 1 $\times$ 3D Conv.
    * *Decoder Level 2*: Transposed 3D Conv + Channel Concatenation (Skip connection from Encoder L2) + 1 $\times$ 3D Conv.
    * *Decoder Level 1*: Transposed 3D Conv + Channel Concatenation (Skip connection from Encoder L1) + 1 $\times$ 3D Conv (32 filters) + Output 3D Conv (3 filters).
    * *Cropping Layer*: Output cropped back to target grid dimensions $201 \times 288 \times 384$.
  * **Case $Re_\tau = 550$**:
    * Channel filter scaling across levels 1 to 4: $24 \rightarrow 48 \rightarrow 96 \rightarrow 192$.
    * Tensor shape sequence adapted from input grid size $251 \times 384 \times 384$.

* **Explainability Optimization Head**:
  * For gradient-SHAP attribution, the model output is passed to a scalar mean-squared-error head comparing prediction $\hat{\mathbf{u}}^{t+\Delta t}$ to DNS ground truth $\mathbf{u}^{t+\Delta t}_{\text{DNS}}$:
    $$F(\mathbf{x}_{\text{in}}) = \text{MSE}\left(\hat{\mathbf{u}}^{t+\Delta t}, \mathbf{u}^{t+\Delta t}_{\text{DNS}}\right) = \frac{1}{3 N_x N_y N_z} \sum_{j \in \{u,v,w\}} \sum_{i=1}^{N_x N_y N_z} \left(\hat{\mathbf{u}}_{j,i}^{t+\Delta t} - \mathbf{u}_{\text{DNS}, j,i}^{t+\Delta t}\right)^2$$

* **Training Hyperparameters**:
  * Optimizer: RMSprop (learning rate $= 5 \times 10^{-5}$, momentum $= 0.9$).
  * Training Data Volume: $10,000$ instantaneous snapshot fields ($80\%$ training, $20\%$ validation).
  * Feature Attribution Evaluation: $8,000$ fields processed for gradient-SHAP analysis.

---

## 3. Data Scaling & Normalization

* **Velocity Scaling (Inner Viscous Units)**:
  $$u^+ = \frac{u}{u_\tau}, \quad v^+ = \frac{v}{u_\tau}, \quad w^+ = \frac{w}{u_\tau}$$
  where $u_\tau = \sqrt{\frac{\tau_w}{\rho}}$ is the friction velocity derived from wall shear stress $\tau_w$ and fluid density $\rho$.

* **Spatial Coordinate Scaling**:
  $$y^+ = \frac{y u_\tau}{\nu}, \quad x^+ = \frac{x u_\tau}{\nu}, \quad z^+ = \frac{z u_\tau}{\nu}$$

* **Time Step Non-dimensionalization**:
  $$\Delta t^+ = \frac{\Delta t \cdot u_\tau^2}{\nu} = 5$$

* **XAI Reference (Non-Informative) Baseline**:
  * Baseline input $\mathbf{x}_{\text{ref}}$ is set to the mean velocity field ($\mathbf{u}_{\text{ref}} = \mathbf{0}$).
  * Interpolated state for expected gradients calculation:
    $$\mathbf{x}_{\text{interp}}(\alpha) = \mathbf{x}_{\text{ref}} + \alpha (\mathbf{x}_{\text{in}} - \mathbf{x}_{\text{ref}}) = \alpha \mathbf{x}_{\text{in}}, \quad \alpha \sim U(0,1)$$

---

## 4. Required Physics Validation Gates

* **Surrogate Model Accuracy Gate**:
  * Relative predictive MSE across all domain points must remain $\le 1\%$ relative to the maximum velocity fluctuation magnitude across the entire dataset:
    * $Re_\tau = 125$: $1.15\%$ ($u'$), $0.98\%$ ($v'$), $1.08\%$ ($w'$).
    * $Re_\tau = 550$: $0.74\%$ ($u'$), $1.15\%$ ($v'$), $0.88\%$ ($w'$).

* **Coherent Structure Cross-Validation Metrics**:
  * **Intense Reynolds-Stress Events ($Q$ events)**:
    $$|u(x,y,z,t) v(x,y,z,t)| > \beta u'(y) v'(y)$$
    where $u'(y)$ and $v'(y)$ are root-mean-square fluctuation profiles, and $\beta$ is a spatial percolation parameter.
  * **High/Low Streamwise Streaks**:
    $$\sqrt{u^2(x,y,z,t) + w^2(x,y,z,t)} > \alpha u_\tau$$
  * **Vorticity/Rotation Discriminant (Chong et al.)**:
    $$\lambda^3 - P\lambda^2 + Q\lambda - R = 0$$
    For incompressible flow ($P = A_{ii} = 0$):
    $$Q = -\frac{1}{2}\left(S_{ij}S_{ji} + \Omega_{ij}\Omega_{ji}\right), \quad R = -\frac{1}{3}\left(S_{ij}S_{jk}S_{ki} + 3\Omega_{ij}\Omega_{jk}S_{ki}\right)$$
    $$D = Q^3 + \frac{27}{4}R^2 > \gamma D'(y)$$
    where $S_{ij} = \frac{1}{2}(\partial_j u_i + \partial_i u_j)$, $\Omega_{ij} = \frac{1}{2}(\partial_j u_i - \partial_i u_j)$, and $D'(y)$ is the wall-normal standard deviation of $D$.

* **Volumetric Structure Coincidence Validation**:
  * Evaluate wall-normal overlap profiles $\frac{\text{Vol}(\text{SHAP} \cap \text{Structure})}{\text{Vol}(\text{SHAP})}$ and $\frac{\text{Vol}(\text{SHAP} \cap \text{Structure})}{\text{Vol}(\text{Structure})}$ against $Q$ events, streaks, and vortices.

---

## 5. Architectural Innovations & Edge Cases

* **Boundary-Aware Periodic Circular Padding**:
  * To eliminate edge convolution artifacts in turbulent channel flows, $x$ (streamwise) and $z$ (spanwise) boundaries are padded circularly according to flow domain periodicity prior to 3D convolutional filtering.

* **Gradient-SHAP Expected Gradients Formulation**:
  * Node importance $\phi_{j, i}(\mathbf{x}_{\text{in}})$ for grid node $i$ and velocity component $j \in \{u,v,w\}$ is computed via expected gradients:
    $$\phi_{j, i}(\mathbf{x}_{\text{in}}) = \mathbb{E}_{\alpha \sim U(0,1)} \left[ x_{\text{in}, j, i} \cdot \frac{\partial F(\alpha \mathbf{x}_{\text{in}})}{\partial x_{\text{in}, j, i}} \right]$$
  * Summation identity guarantees full error attribution:
    $$\text{MSE}(\mathbf{x}_{\text{in}}) = \phi_0 + \sum_{j \in \{u,v,w\}} \sum_{i=1}^{N} \phi_{j, i} z_i$$
    where $\phi_0$ is the error of the reference field, and $z_i \in \{0, 1\}$.

* **SHAP Spatial Ensemble Denoising**:
  * To suppress gradient attribution spatial noise, raw SHAP fields are computed across 10 periodic spatial translations along $x$ and $z$ and averaged:
    $$\bar{\mathbf{\Phi}}(x,y,z) = \frac{1}{10} \sum_{k=1}^{10} \mathbf{\Phi}\left(x + \Delta x_k, y, z + \Delta z_k\right)$$

* **Vectorial SHAP Feature Percolation Criterion**:
  * Identification of high-importance spatial structures ($\text{SHAP structures}$) is defined by the localized vector magnitude exceeding a threshold based on wall-normal mean profiles:
    $$\sqrt{\phi_u^2(x,y,z,t) + \phi_v^2(x,y,z,t) + \phi_w^2(x,y,z,t)} > H \sqrt{\bar{\phi}_u^2(y) + \frac{1}{2}\bar{\phi}_v^2(y) + \frac{1}{2}\bar{\phi}_w^2(y)}$$
    where percolation index $H = 2$.

---

## 6. Raw Data Corrections Log

* **Equation (1) Reconstruction**: The extracted text contained typographical indexing errors ($\phi_2^2$ repeated for all three velocity vector components). Reconstructed using valid component notation $(\phi_u, \phi_v, \phi_w)$ and wall-normal planar mean profiles:
  $$\sqrt{\phi_u^2(x,y,z,t) + \phi_v^2(x,y,z,t) + \phi_w^2(x,y,z,t)} > H \sqrt{\bar{\phi}_u^2(y) + \frac{1}{2}\bar{\phi}_v^2(y) + \frac{1}{2}\bar{\phi}_w^2(y)}$$
* **Equation (4) Indexing Fix**: Corrected OCR string $\phi_{ji} z_i$ to explicitly account for velocity components $j \in \{u, v, w\}$ and total spatial grid nodes $N$.
* **Equations (7)–(9) Tensor Cleanups**: Corrected tensorial contraction indices for $S_{ij}$ and $\Omega_{ij}$ in velocity gradient tensor invariants $P$, $Q$, and $R$.
* **Implicit Activation & Convolution Operations**: Activation functions in the U-Net were omitted in the text; standard LeakyReLU/ReLU activations between 3D convolutional blocks are inferred for code compilation readiness.