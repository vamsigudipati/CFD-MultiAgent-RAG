## 1. Physical Problem Statement

* **Flow Regimes & System Cases**:
  1. **1D Burgers' Equation**: Spatio-temporal benchmark problem for non-linear advection-diffusion dynamics and temporal super-resolution.
  2. **2D Laminar Cylinder Wake**: Unsteady 2D vortex shedding behind a circular cylinder at Reynolds number $Re_D = \frac{U_\infty D}{\nu} = 100$, where $D$ is cylinder diameter and $U_\infty$ is free-stream velocity.
  3. **3D Minimal Turbulent Channel Flow**: Unsteady turbulent wall-bounded flow at Reynolds number $Re_{cl} = \frac{U_{cl} h}{\nu} = 5000$, based on channel half-height $h$ and laminar centerline velocity $U_{cl}$.
  4. **Experimental Hot-Wire Anemometry (HWA)**: Real experimental velocity time-series dataset for denoising and spatial/temporal resolution enhancement.

* **Governing Partial Differential Equations**:
  General spatio-temporal non-linear system defined over domain $\Omega \times [0, T]$:
  $$\mathbf{u}_t + \mathcal{N}[\mathbf{u}] = 0, \quad \mathbf{x} \in \Omega, \quad t \in [0, T]$$
  PDE physical residual $e(t, \mathbf{x})$:
  $$e(t, \mathbf{x}) := \mathbf{u}_t + \mathcal{N}[\mathbf{u}]$$

* **Input-Output Mapping**:
  * **Input Coordinate Vector**: Spatio-temporal coordinate vector $(t, \mathbf{x}) = (t, x, y, z)^T$.
  * **Output Field Vector**: Continuous state solution $\mathbf{u}(t, \mathbf{x}) = (u, v, w, p)^T$ parameterizing instantaneous velocity components and pressure.

---

## 2. Network Architectures

* **Topology**:
  Physics-Informed Neural Network (PINN) comprising a Multi-Layer Perceptron (MLP) functional approximator integrated with an Automatic Differentiation (AD) residual network.

* **Layer Specifications**:
  * **Burgers' Equation Model**:
    * **Architecture**: Fully Connected MLP with 8 hidden layers, each containing 20 neurons.
    * **Activation Function**: Hyperbolic Tangent ($\tanh$).
  * **2D Cylinder Wake Model**:
    * **Architecture**: Fully Connected MLP (layer dimensions tuned via hyper-parameter sweep in Appendix A.1).
    * **Activation Function**: Hyperbolic Tangent ($\tanh$).
  * **3D Minimal Turbulent Channel Flow Model**:
    * **Architecture**: Fully Connected MLP (layer dimensions tuned via hyper-parameter sweep in Appendix A.2).
    * **Activation Function**: Hyperbolic Tangent ($\tanh$).

* **Automatic Differentiation Engine**:
  Reverse-mode automatic differentiation implemented via TensorFlow (`tf.GradientTape` API) to compute analytical spatial and temporal derivatives:
  $$\frac{\partial \mathbf{u}}{\partial \mathbf{x}} = G(\mathbf{u}, \mathbf{x}), \quad \frac{\partial \mathbf{u}}{\partial t} = G(\mathbf{u}, t)$$

* **Optimization Scheme**:
  * **Training Protocol**: Full-batch gradient optimization in two sequential stages:
    1. **First Stage**: Adam optimizer for $1,000$ epochs with initial learning rate $\eta = 1 \times 10^{-3}$.
    2. **Second Stage**: Quasi-Newton Limited-memory Broyden–Fletcher–Goldfarb–Shanno (L-BFGS) algorithm until convergence defined by the line-search increment tolerance.

---

## 3. Data Scaling & Normalization

* **Dimensionless Characteristic Numbers**:
  * Cylinder Wake Reynolds Number: $Re_D = \frac{U_\infty D}{\nu} = 100$
  * Minimal Channel Reynolds Number: $Re_{cl} = \frac{U_{cl} h}{\nu} = 5000$

* **Sampling & Collocation Distribution**:
  * **Supervised Data Points ($N_s$)**: Sparse, low-resolution velocity measurements from sparse grids or corrupted experimental/synthetic fields. Synthetic Gaussian noise is added to test model robustness.
  * **Unsupervised Collocation Points ($N_e$)**: Densely sampled evaluation points across the spatio-temporal continuum $(t_e^i, \mathbf{x}_e^i)$ used to evaluate residual compliance without needing spatial targets.

---

## 4. Required Physics Validation Gates

* **Loss Function Formulations**:
  * **Supervised Loss ($L_s$)**:
    $$L_s = \frac{1}{N_s} \sum_{i=1}^{N_s} |\mathbf{u}_s^i - \mathbf{u}(t_s^i, \mathbf{x}_s^i)|^2$$
  * **Unsupervised PDE Residual Loss ($L_e$)**:
    $$L_e = \frac{1}{N_e} \sum_{i=1}^{N_e} |e(t_e^i, \mathbf{x}_e^i)|^2$$
  * **Composite Optimization Loss ($L$)**:
    $$L = \alpha L_s + \beta L_e$$
    where $\alpha$ and $\beta$ are problem-specific scalar weighting coefficients.

* **Quantitative Performance Metrics**:
  1. **Time-Averaged Relative Euclidean Error Norm ($\epsilon_\phi$)**:
     $$\epsilon_\phi = \left\langle \frac{\|\tilde{\phi} - \phi\|^2}{\|\phi\|^2} \right\rangle$$
     where $\phi \in \{u, v, w, p\}$ is the reference solution, $\tilde{\phi}$ is the model prediction, $\|\cdot\|$ denotes the $L_2$ spatial norm, and $\langle \cdot \rangle$ indicates temporal averaging.
  2. **Pearson Correlation Coefficient ($r_\phi$)**:
     $$r_\phi = \frac{\sum_{i=1}^n (\tilde{\phi}_i - \bar{\tilde{\phi}})(\phi_i - \bar{\phi})}{\sqrt{\sum_{i=1}^n (\tilde{\phi}_i - \bar{\tilde{\phi}})^2 \sum_{i=1}^n (\phi_i - \bar{\phi})^2}}$$
     where $\bar{\phi}$ and $\bar{\tilde{\phi}}$ denote domain-averaged field values.

---

## 5. Architectural Innovations & Edge Cases

* **High-Resolution Data-Free Physics Super-Resolution**:
  Eliminates the requirement for paired high-resolution training labels (unlike standard supervised CNNs or SRGANs). Super-resolution is achieved natively by training an MLP functional approximator continuously across $(t, \mathbf{x})$ constrained by $L_e$.
* **Instantaneous Turbulent Field Reconstruction**:
  Reconstructs full instantaneous temporal flow dynamics and unmeasured quantities (e.g., pressure $p$ inferred from sparse velocity components) directly in unsteady, 3D turbulent regimes ($Re_{cl} = 5000$).
* **Robustness to Measurement Noise**:
  Acts simultaneously as a physical filter and continuous interpolator when trained on low-resolution measurements corrupted by Gaussian noise.
* **Hybrid Full-Batch Optimization**:
  Mitigates loss landscape stagnation by transitioning from global stochastic search (Adam) to exact second-order quasi-Newton optimization (L-BFGS).

---

## 6. Raw Data Corrections Log

| Raw Fragment / OCR Artifact | Corrected Standard Syntax | Extraction Location / Header |
| :--- | :--- | :--- |
| `Re$^{D}$ = U∞D/ν = 100` | $Re_D = \frac{U_\infty D}{\nu} = 100$ | `HEADER: Physics-informed deep-learning applications to experimental fluid mechanics > 1. Introduction` |
| `Recl = Uclh/ν = 5, 000` | $Re_{cl} = \frac{U_{cl} h}{\nu} = 5000$ | `HEADER: Physics-informed deep-learning applications to experimental fluid mechanics > 1. Introduction` |
| `e(t i e , x i e )` | $e(t_e^i, \mathbf{x}_e^i)$ | `HEADER: 2.2. Physics-informed neural networks (PINNs)` |
| `Jim´enez 2018` | Jiménez 2018 | `HEADER: Physics-informed deep-learning applications to experimental fluid mechanics > 1. Introduction` |
| Hidden layer counts for cylinder wake & channel flow deferred to appendices | Exact width/depth cited as hyper-parameter tuned in Appendices A.1 & A.2 | `HEADER: 2.2. Physics-informed neural networks (PINNs) > 3. Physics-informed super-resolution of flow fields in time and space` |