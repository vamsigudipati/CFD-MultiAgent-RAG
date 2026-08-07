# Architectural Blueprint — CNN Wall Predictions (Balasubramanian et al., 2023)

> Code-ready synthesis of "Predicting the wall-shear stress and wall pressure through
> convolutional neural networks." Narrative stripped; only implementable specs retained.

## 1. Physical Problem Statement
- **Flow regime:** Turbulent open channel flow (single wall of interest), DNS-generated.
- **Solver / data source:** Pseudo-spectral solver SIMSON (Chevalier et al., 2007).
- **Friction Reynolds numbers:** $Re_\tau = 180$ and $Re_\tau = 550$.
- **Domain size (wall-parallel):** $L_x \times L_z = 4\pi h \times 2\pi h$, $h$ = open-channel height. Periodic BCs in $x$ (streamwise) and $z$ (spanwise).
- **Sampled wall-normal planes (inner units):** $y^+ = 15, 30, 50, 100, 150$.
- **Field resolution:** $(N_x, N_z) = (192, 192)$ at $Re_\tau = 180$; $(512, 512)$ at $Re_\tau = 550$.

### Prediction tasks
1. **Inner prediction (baseline):** predict velocity-fluctuation fields at $y^+_{\text{target}}$ from fields farther from the wall at $y^+_{\text{input}}$, with $y^+_{\text{input}} > y^+_{\text{target}}$. Separation $\Delta y^+ = y^+_{\text{input}} - y^+_{\text{target}}$.
2. **Self-similarity prediction (key result):** at $Re_\tau = 550$, predict $y^+ = 50$ ($y/h = 0.1$) from $y^+ = 100$ ($y/h = 0.2$), exploiting the linear eddy-size scaling in the logarithmic region.
3. **Wall prediction (deployment target):** predict the two wall-shear-stress components ($\tau_{x} \equiv u_y$, $\tau_{z} \equiv w_y$) and wall pressure $p$ from a velocity-fluctuation plane at a given $y^+$.

### Hard performance boundary
- Prediction quality degrades sharply for $\Delta y^+ > 80$ (streamwise RMS error > 30%). Keep input–target separation $\Delta y^+ \le 80$; accuracy is highest as $y^+_{\text{input}} \to$ wall.

---

## 2. Network Architectures

Two fully-convolutional topologies. Both operate on 2D wall-parallel planes; input channels = 3 velocity components $(u, v, w)$.

### 2.1 Common convolution spec
- **Kernel size:** $3 \times 3$ for every convolutional layer.
- **Convolution definition:** $F_{i,j} = \sum_m \sum_n I_{i-m,j-n} K_{m,n}$.
- **Activation:** ReLU after each hidden convolutional layer.
- **Batch normalization:** applied after every convolutional layer **except the last**.
- **Output-layer activation:** a *modified ReLU* (thresholded ReLU) applied just before output:
  - threshold $= -1$ when predicting velocity fluctuations,
  - threshold $= -25$ when predicting fluctuating wall quantities.
- **Padding:** periodic padding in both wall-parallel directions — **64 points total (32 per side)** — to enforce periodicity. Output is larger than the DNS field and is **center-cropped** back to DNS size.
- **Receptive field:** $63 \times 63$.

### 2.2 FCN (fully-convolutional network)
- **Hidden layers:** 31.
- **Trainable parameters:** 2,902,791.
- Plain stack of $3\times3$ conv + BN + ReLU (no skip connections).

### 2.3 R-Net (residual skip-connection network)
- **Hidden layers:** 31.
- **Trainable parameters:** 2,568,681 (≈ **11% smaller** than FCN).
- **Skip connections:** between hidden layer $i$ and layer $N - i - 1$, where $N$ = total hidden layers. Style resembles U-Net skips but **without up-sampling**.
- **Crop-on-concat:** upstream feature maps differ in size from downstream maps, so each upstream map is cropped to the target shape before concatenation to the downstream map.

---

## 3. Data Scaling & Normalization

### 3.1 Input velocity-fluctuation scaling (Eq. 2)
Rescale the three input components to comparable magnitudes:
$$ \hat{u} = u, \quad \hat{v} = v \frac{u_{\text{RMS}}}{v_{\text{RMS}}}, \quad \hat{w} = w \frac{v_{\text{RMS}}}{w_{\text{RMS}}} $$

### 3.2 Wall-quantity output normalization (Eq. 3)
Normalize each predicted wall quantity by its own RMS:
$$ \frac{\partial u}{\partial y} = \frac{\partial u / \partial y}{\partial u / \partial y_{\text{RMS}}}, \quad \frac{\partial w}{\partial y} = \frac{\partial w / \partial y}{\partial w / \partial y_{\text{RMS}}}, \quad \bar{p} = \frac{p}{p_{\text{RMS}}} $$

---

## 4. Required Physics Validation Gates

### Gate 1 — MSE loss (training objective, Eq. 4)
$$ \mathcal{L}(u_{\text{pred}}; u_{\text{DNS}}) = \frac{1}{N_x N_z} \sum_{i=1}^{N_x} \sum_{j=1}^{N_z} \left| u_{\text{pred}}(i,j) - u_{\text{DNS}}(i,j) \right|^2 $$

### Gate 2 — RMS-fluctuation statistical error (Eq. 5)
$$ E_{\text{RMS}}(u) = \frac{\left| u_{\text{RMS,pred}} - u_{\text{RMS,DNS}} \right|}{u_{\text{RMS,DNS}}} $$
- **Acceptance targets:** ≈ 10% streamwise RMS error in the self-similar case; < ~15% RMS error for wall quantities.

### Gate 3 — Instantaneous correlation coefficient (Eq. 6)
$$ R_{\text{pred;DNS}}(u) = \frac{\langle u_{\text{pred}}\, u_{\text{DNS}} \rangle_{x,z,t}}{u_{\text{RMS,pred}}\, u_{\text{RMS,DNS}}} $$
- **Hard threshold:** $R_{\text{pred;DNS}}(u) \ge 0.8$ (streamwise) is the minimum for a "convincing" prediction.

### Gate 4 — 2D pre-multiplied power-spectral density
- **Check:** contour overlap at the 10%, 50%, 90% levels of max DNS PSD. Flag if energetic scales diverge.
