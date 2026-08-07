## 1. Physical Problem Statement

The central physical objective is closing the Reynolds-Averaged Navier–Stokes (RANS) partial differential equations for incompressible and compressible turbulent flows by using data-driven and machine-learning (ML) techniques to model unclosed turbulent terms or correct baseline closure discrepancies.

### Governing Partial Differential Equations
$$\nabla \cdot \mathbf{U} = 0$$

$$\mathbf{U} \cdot \nabla \mathbf{U} = -\frac{1}{\rho}\nabla P + \nu \nabla^2 \mathbf{U} - \nabla \cdot \boldsymbol{\tau}$$

where $\mathbf{U} = \langle \mathbf{u} \rangle$ is the mean velocity vector, $P = \langle p \rangle$ is the mean pressure, $\rho$ is fluid density, $\nu$ is kinematic viscosity, and $\boldsymbol{\tau} = \langle \mathbf{u}' \otimes \mathbf{u}' \rangle$ is the unclosed Reynolds stress tensor.

### Closure Formulations Targetted by ML
1. **Explicit Reynolds Stress Tensor Expansion (L2/L3 Level):**
   $$\boldsymbol{\tau} = 2k \left( \frac{1}{3}\mathbf{I} + \mathbf{a} \right) = 2k \left( \frac{1}{3}\mathbf{I} + \sum_{n=1}^{10} c^{(n)}(\boldsymbol{\eta}) \mathcal{T}^{(n)} \right)$$
   where $k = \frac{1}{2}\text{Tr}(\boldsymbol{\tau})$ is the turbulent kinetic energy, $\mathbf{a}$ is the anisotropy tensor, $\mathcal{T}^{(n)}$ are isotropic tensor bases formed from normalized strain rate $\mathbf{S}$ and rotation rate $\boldsymbol{\Omega}$ tensors, and $c^{(n)}(\boldsymbol{\eta})$ are scalar coefficients predicted by machine learning as functions of non-dimensional input features $\boldsymbol{\eta}$.

2. **Embedded Transport Discrepancy Multiplier (FIML Framework):**
   $$\mathcal{M}(\mathbf{w}; \mathcal{P}(\mathbf{w})) \implies \mathcal{P}_{\tilde{\nu}}^{\text{corrected}} = \beta(\boldsymbol{\eta}) \cdot \mathcal{P}_{\tilde{\nu}}^{\text{baseline}}$$
   where $\beta(\boldsymbol{\eta}) = 1 + \delta(\boldsymbol{\eta})$ is a spatial discrepancy field learned via ML and injected into turbulence transport source/production terms (e.g., Spalart–Allmaras or $k$-$\omega$ SST models).

### Physical Flow Regimes & Boundary Configurations
- **Fully Developed Wall-Bounded Shear Flows:** Plane channel flow across Reynolds numbers $Re_\tau \in [180, 5200]$.
- **Separated & Recirculating Flows:** Flow over periodic hills, backward-facing step, and airfoils at high angles of attack.
- **Curved & Secondary Flows:** Convex/concave channel flows, square duct secondary motions of the second kind.
- **Free Shear Layers & Jets:** Circular jets, plane jets, wakes, and jet-in-crossflow configurations.

---

## 2. Network Architectures

The review surveys three primary machine learning computational architectures for turbulence modeling:

```
                            [ Flow Field Variables: U, ∇U, k, ε, d ]
                                               │
                                               ▼
                             [ Non-Dimensionalization & Invariants ]
                             (S, Ω, I_1..I_5, Barycentric Coords)
                                               │
                       ┌───────────────────────┴───────────────────────┐
                       ▼                                               ▼
        [ Tensor Basis Neural Network ]                    [ Field Inversion + ML ]
                       │                                               │
          Fully Connected Hidden Layers                   Adjoint / EnKF Inverse Step
        ℓ = σ(W^(1) η + β^(1)), σ = tanh                              │
                       │                                    Inferred Field δ(x)
                       ▼                                               │
          Scalar Coefficients c^(n)(η)                        Regression Mapping (MLP)
                       │                                   η(x) ↦ δ(η)
                       ▼                                               │
      Anisotropy Basis Tensor Layer                                    ▼
       τ = 2k(1/3 I + ∑ c^(n) T^(n))                     Augmented RANS PDE Correction
                       │                                   P_modified = β(η) P_base
                       └───────────────────────┬───────────────────────┘
                                               │
                                               ▼
                                  [ Closed-Loop RANS Solver ]
```

### 1. Tensor Basis Neural Network (TBNN)
- **Input Topology:** Non-dimensional scalar tensor invariants $\boldsymbol{\eta} = \{I_1, I_2, I_3, I_4, I_5\} \in \mathbb{R}^5$.
- **Hidden Layers:** $L$ fully connected dense layers.
  $$\mathbf{l}^{(1)} = \sigma \left( \mathbf{W}^{(1)} \boldsymbol{\eta} + \boldsymbol{\beta}^{(1)} \right)$$
  $$\mathbf{l}^{(k)} = \sigma \left( \mathbf{W}^{(k)} \mathbf{l}^{(k-1)} + \boldsymbol{\beta}^{(k)} \right), \quad k = 2, \dots, L$$
- **Activation Functions:** Hyperbolic tangent $\sigma(z) = \tanh(z)$ or LeakyReLU.
- **Output Layer:** Linear projection to 10 scalar coefficients $\mathbf{c} = [c^{(1)}, \dots, c^{(10)}]^\top \in \mathbb{R}^{10}$.
- **Tensor Embedding Layer:** Non-trainable tensor product layer enforcing invariance:
  $$\mathbf{a}(\boldsymbol{\eta}) = \sum_{n=1}^{10} c^{(n)}(\boldsymbol{\eta}) \mathcal{T}^{(n)}(\mathbf{S}, \boldsymbol{\Omega})$$

### 2. Field Inversion & Machine Learning (FIML) Architecture
- **Inversion Stage (Adjoint / EnKF):** Solves a Maximum A Posteriori (MAP) optimization problem over the discretized spatial domain:
  $$\boldsymbol{\delta}_{\text{MAP}}(\mathbf{x}) = \arg\min_{\boldsymbol{\delta}} \frac{1}{2} \left( \mathbf{y}_{\text{obs}} - \mathbf{o}(\mathcal{M}(\boldsymbol{\delta})) \right)^\top \mathbf{Q}_\theta^{-1} \left( \mathbf{y}_{\text{obs}} - \mathbf{o}(\mathcal{M}(\boldsymbol{\delta})) \right) + \frac{1}{2} (\boldsymbol{\delta} - \boldsymbol{\delta}_{\text{prior}})^\top \mathbf{Q}_c^{-1} (\boldsymbol{\delta} - \boldsymbol{\delta}_{\text{prior}})$$
- **Regression Stage:** Deep Multi-Layer Perceptrons (MLP) or Random Forest Regressors mapping physical features $\boldsymbol{\eta}(\mathbf{x}) \in \mathbb{R}^d \to \delta(\boldsymbol{\eta}) \in \mathbb{R}$.

### 3. Random Forests for Eigenspace Perturbations
- **Ensemble Topology:** Decision tree ensemble mapping local invariant features to perturbations in Reynolds stress magnitude $\delta k$, anisotropy eigenvalues $\delta \boldsymbol{\Lambda} = (\delta \lambda_1, \delta \lambda_2, \delta \lambda_3)$, and orientation eigenvectors $\delta \mathbf{V}$ (encoded via unit quaternions $\mathbf{q} \in \mathbb{R}^4$).

---

## 3. Data Scaling & Normalization

To ensure frame independence, Galilean invariance, and dimensional consistency across different flow scales, all input variables are normalized prior to model evaluation.

### Non-Dimensional Rate-of-Strain and Rate-of-Rotation Tensors
$$\mathbf{S} = \frac{1}{2} \tau_{\text{turb}} \left( \nabla \mathbf{U} + (\nabla \mathbf{U})^\top \right), \quad \boldsymbol{\Omega} = \frac{1}{2} \tau_{\text{turb}} \left( \nabla \mathbf{U} - (\nabla \mathbf{U})^\top \right)$$

where $\tau_{\text{turb}}$ is the characteristic turbulent timescale defined as $\tau_{\text{turb}} = \frac{k}{\epsilon}$ (or $\tau_{\text{turb}} = \frac{1}{\omega}$).

### Five Fundamental Scalar Tensor Invariants ($\boldsymbol{\eta}$)
$$I_1 = \text{Tr}(\mathbf{S}^2), \quad I_2 = \text{Tr}(\boldsymbol{\Omega}^2), \quad I_3 = \text{Tr}(\mathbf{S}^3), \quad I_4 = \text{Tr}(\boldsymbol{\Omega}^2 \mathbf{S}), \quad I_5 = \text{Tr}(\boldsymbol{\Omega}^2 \mathbf{S}^2)$$

### Ten Isotropic Tensor Bases ($\mathcal{T}^{(n)}$)
$$\mathcal{T}^{(1)} = \mathbf{S}, \quad \mathcal{T}^{(2)} = \mathbf{S}\boldsymbol{\Omega} - \boldsymbol{\Omega}\mathbf{S}, \quad \mathcal{T}^{(3)} = \mathbf{S}^2 - \frac{1}{3}\text{Tr}(\mathbf{S}^2)\mathbf{I}$$
$$\mathcal{T}^{(4)} = \boldsymbol{\Omega}^2 - \frac{1}{3}\text{Tr}(\boldsymbol{\Omega}^2)\mathbf{I}, \quad \mathcal{T}^{(5)} = \boldsymbol{\Omega}\mathbf{S}^2 - \mathbf{S}^2\boldsymbol{\Omega}$$
$$\mathcal{T}^{(6)} = \boldsymbol{\Omega}^2\mathbf{S} + \mathbf{S}\boldsymbol{\Omega}^2 - \frac{2}{3}\text{Tr}(\mathbf{S}\boldsymbol{\Omega}^2)\mathbf{I}, \quad \mathcal{T}^{(7)} = \boldsymbol{\Omega}\mathbf{S}\boldsymbol{\Omega}^2 - \boldsymbol{\Omega}^2\mathbf{S}\boldsymbol{\Omega}$$
$$\mathcal{T}^{(8)} = \mathbf{S}\boldsymbol{\Omega}\mathbf{S}^2 - \mathbf{S}^2\boldsymbol{\Omega}\mathbf{S}, \quad \mathcal{T}^{(9)} = \boldsymbol{\Omega}^2\mathbf{S}^2 + \mathbf{S}^2\boldsymbol{\Omega}^2 - \frac{2}{3}\text{Tr}(\mathbf{S}^2\boldsymbol{\Omega}^2)\mathbf{I}$$
$$\mathcal{T}^{(10)} = \boldsymbol{\Omega}\mathbf{S}^2\boldsymbol{\Omega}^2 - \boldsymbol{\Omega}^2\mathbf{S}^2\boldsymbol{\Omega}$$

### Barycentric Coordinates for Anisotropy Eigenvalues
Given sorted anisotropy eigenvalues $\lambda_1 \ge \lambda_2 \ge \lambda_3$ from $\mathbf{a} = \mathbf{V} \boldsymbol{\Lambda} \mathbf{V}^\top$:
$$C_1 = \lambda_1 - \lambda_2, \quad C_2 = 2(\lambda_2 - \lambda_3), \quad C_3 = 3\lambda_3 + 1$$
$$\text{Constraint: } C_1 + C_2 + C_3 = 1, \quad C_i \ge 0 \quad \forall i \in \{1, 2, 3\}$$

---

## 4. Required Physics Validation Gates

```
                    [ Predicted Reynolds Stress / Discrepancy ]
                                         │
                                         ▼
                       [ Gate 1: Realizability Verification ]
                       • k ≥ 0
                       • Anisotropy Eigenvalues inside Barycentric Triangle
                                         │ (Pass)
                                         ▼
                       [ Gate 2: Invariance Verification ]
                       • Galilean & Rotational Objectivity: Q τ Qᵀ
                                         │ (Pass)
                                         ▼
                       [ Gate 3: Closed-Loop RANS PDE Integration ]
                       • Iterative Solver Stability & Convergence
                       • Check for Divergence/Ill-Conditioning
                                         │ (Pass)
                                         ▼
                       [ Gate 4: Quantitative Field Error Metrics ]
                       • Skin Friction (C_f) MSE
                       • Wall Pressure (C_p) MSE
                       • Velocity Profile L_2 Relative Error
```

### Gate 1: Realizability Constraints (Lumley & Schumann Bounds)
- Non-negativity of turbulent kinetic energy: $k(\mathbf{x}) \ge 0$.
- Positivity of individual normal Reynolds stresses: $\tau_{ii} \ge 0 \quad \forall i \in \{1, 2, 3\}$.
- Cauchy–Schwarz inequality for shear stresses: $\tau_{ij}^2 \le \tau_{ii} \tau_{jj}$.
- Eigenvalue bounds of anisotropy matrix $\mathbf{a}$:
  $$-\frac{1}{3} \le \lambda_3 \le \lambda_2 \le \lambda_1 \le \frac{2}{3}, \quad \text{Tr}(\mathbf{a}) = 0$$

### Gate 2: Galilean and Rotational Invariance (Objectivity)
For any proper orthogonal transformation matrix $\mathbf{Q} \in SO(3)$ (where $\mathbf{Q}\mathbf{Q}^\top = \mathbf{I}$ and $\det(\mathbf{Q}) = 1$):
$$\tilde{\boldsymbol{\tau}}(\mathbf{Q} \mathbf{S} \mathbf{Q}^\top, \mathbf{Q} \boldsymbol{\Omega} \mathbf{Q}^\top) = \mathbf{Q} \tilde{\boldsymbol{\tau}}(\mathbf{S}, \boldsymbol{\Omega}) \mathbf{Q}^\top$$

### Gate 3: PDE Solver Integration Stability & Convergence
- The ML model output must yield stable iterative convergence when integrated directly into the non-linear coupled RANS equations.
- Non-physical oscillations or ill-conditioning in the numerical gradient operators $\nabla \cdot \tilde{\boldsymbol{\tau}}$ must be zero.

### Gate 4: Quantitative Flow Metrics (Validation Loss)
- **Skin Friction Error:**
  $$\text{MSE}_{C_f} = \frac{1}{N_{\text{wall}}} \sum_{i=1}^{N_{\text{wall}}} \left( C_{f, \text{pred}}^{(i)} - C_{f, \text{ref}}^{(i)} \right)^2, \quad C_f = \frac{\tau_w}{\frac{1}{2}\rho U_\infty^2}$$
- **Surface Pressure Coefficient Error:**
  $$\text{MSE}_{C_p} = \frac{1}{N_{\text{wall}}} \sum_{i=1}^{N_{\text{wall}}} \left( C_{p, \text{pred}}^{(i)} - C_{p, \text{ref}}^{(i)} \right)^2, \quad C_p = \frac{P - P_\infty}{\frac{1}{2}\rho U_\infty^2}$$
- **Velocity Profile Relative $L_2$ Metric:**
  $$E_U = \frac{\|\mathbf{U}_{\text{pred}} - \mathbf{U}_{\text{DNS}}\|_2}{\|\mathbf{U}_{\text{DNS}}\|_2}$$

---

## 5. Architectural Innovations & Edge Cases

### 1. Embedded Invariance Layers (TBNN Architecture)
Unlike standard neural networks that rely on data augmentation to learn rotational symmetries, the TBNN embeds rotational invariance directly into the architecture. By mapping non-dimensional invariants $\boldsymbol{\eta}$ to scalar coefficients $c^{(n)}$ and performing an explicit matrix multiplication with tensor bases $\mathcal{T}^{(n)}$ in the final layer, exact frame indifference is mathematically guaranteed.

### 2. Two-Stage Field Inversion Machine Learning (FIML)
Direct training of ML models on raw DNS data creates a severe consistency mismatch ("learning environment vs. injection environment") because scale-providing RANS variables (e.g., $\epsilon, \omega, \nu_t$) deviate significantly from true physical values. FIML circumvents this by using adjoint or EnKF field inversion within the baseline RANS solver to extract an intermediate operational discrepancy field $\delta(\mathbf{x})$, which is subsequently learned by ML regressors.

### 3. Unit Quaternion Parametrization of Stress Eigenvectors
When predicting Reynolds stress orientation discrepancies, using Euler angles leads to gimbal lock singularities. Utilizing unit quaternions $\mathbf{q} = [q_0, q_1, q_2, q_3]^\top \in \mathbb{S}^3$ with constraint $\|\mathbf{q}\|_2 = 1$ ensures continuous and singularity-free coordinate transformations for eigenvector rotation matrices $\mathbf{V}(\mathbf{q})$.

### 4. RANS Ill-Conditioning Under Direct Stress Injection
Injecting high-fidelity Reynolds stress fields $\boldsymbol{\tau}_{\text{DNS}}$ directly into standard RANS solvers routinely leads to numerical instability or degraded velocity fields (Wu et al. 2018c). This edge case occurs because the explicit stress gradient term $\nabla \cdot \boldsymbol{\tau}$ lacks the implicit numerical damping provided by the eddy-viscosity Laplacian $\nabla \cdot (\nu_t \nabla \mathbf{U})$. Robust implementations retain an implicit baseline eddy-viscosity operator and apply ML predictions as explicit residual corrections.

---

## 6. Raw Data Corrections Log

| Source Text / Location | Identified Error / Ambiguity | Reconstructed / Corrected Form |
| :--- | :--- | :--- |
| Lexicon Equations (Page 4) | Broken duplicated raw text: `$$\widetilde{\mathcal{M}} \equiv \mathcal{M}(\mathbf{w}; \mathcal{P}(\mathbf{w}); \mathbf{c}; \boldsymbol{\theta}; \boldsymbol{\delta}; \boldsymbol{\epsilon}_{\boldsymbol{\theta}})$$` | Unified mathematical definition of data-driven model $\widetilde{\mathcal{M}} \equiv \mathcal{M}(\mathbf{w}; \mathcal{P}(\mathbf{w}); \mathbf{c}; \boldsymbol{\theta}; \boldsymbol{\delta}; \boldsymbol{\epsilon}_{\boldsymbol{\theta}})$. |
| Section 2, Layer L4 (Page 6) | OCR artifact generating HTML tags: `<math>\mathcal{M}(\mathbf{w}; \mathcal{P}(\mathbf{w}); \mathbf{c})</math>`. | Replaced with standard LaTeX notation $\mathcal{M}(\mathbf{w}; \mathcal{P}(\mathbf{w}); \mathbf{c})$. |
| Section 5.3, Equation 11 (Page 14) | OCR fragmentation causing detached text blocks around equation: `$$\tau = \sum_{n=1}^{10} c^{(n)} \mathcal{T}^{(n)}$$ 11.` | Reconstructed as numbered equation $$\boldsymbol{\tau} = \sum_{n=1}^{10} c^{(n)} \mathcal{T}^{(n)}$$. |
| Section 5.3, Equation 12 (Page 15) | Disjointed output annotation: `$$\tilde{\tau} = \sum_{n=1}^{10} c^{(n)}(\boldsymbol{\theta}, \boldsymbol{\eta}) \mathcal{T}^{(n)} \quad . 12.$$` | Formatted properly as $$\tilde{\boldsymbol{\tau}} = \sum_{n=1}^{10} c^{(n)}(\boldsymbol{\theta}, \boldsymbol{\eta}) \mathcal{T}^{(n)}$$. |
| Section 6, Equation 1.1 (Page 17) | Ambiguous section numbering layout for final summary model: `$$\widetilde{\mathcal{M}} = ...$$ 1.1` | Restructured as $$\widetilde{\mathcal{M}} = \mathcal{M}(\mathbf{w}; \mathcal{P}(\mathbf{w}; \boldsymbol{\theta}); \mathbf{c}(\boldsymbol{\theta}); \boldsymbol{\delta}(\boldsymbol{\theta}, \boldsymbol{\eta}); \boldsymbol{\epsilon}_{\boldsymbol{\theta}})$$. |
| Invariants $I_1 \dots I_5$ (Section 3) | Text mentions invariants without explicit matrix trace formulations. | Explicitly derived $I_1 = \text{Tr}(\mathbf{S}^2), \dots, I_5 = \text{Tr}(\boldsymbol{\Omega}^2 \mathbf{S}^2)$ using Cayley–Hamilton theory definitions. |