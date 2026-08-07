# Module 1 — Temporal Modeling & Chaotic Systems

**Source material:** `Lecture0_Introduction.txt`, `Lecture1.txt` (Prof. Ricardo Vinuesa), slide deck `1_Time_PINNs.pdf` (slides 1–33, "Machine learning for fluid mechanics — Part 1: Introduction to deep learning for fluid mechanics").
**Scope:** Multilayer perceptrons (MLP), recurrent networks (RNN/LSTM), Transformers, and the dynamical-systems diagnostics (Lyapunov exponents, Poincaré maps) used to validate temporal predictions of chaotic turbulent systems.

---

## 1. Mathematical Foundations

### 1.1 The reduced-order test bed: nine-equation near-wall model

All temporal-prediction architectures in this module are benchmarked on the **nine-equation model of the near-wall turbulence cycle** (Moehlis, Faisst & Eckhardt, *New J. Phys.* 6, 56, 2004), which is the minimal Galerkin system that retains streamwise vortices, streaks, and their instabilities.

The instantaneous velocity field is expanded on nine fixed spatial modes $\boldsymbol{\phi}_i(\mathbf{x})$ with time-dependent amplitudes $a_i(t)$:

$$
\mathbf{u}(\mathbf{x}, t) = \sum_{i=1}^{9} a_i(t)\, \boldsymbol{\phi}_i(\mathbf{x})
$$

Substituting into the Navier–Stokes equations and performing a Galerkin projection yields a closed system of nine coupled ODEs for the amplitudes:

$$
\frac{da_i}{dt} = f_i(a_1, \dots, a_9; Re), \qquad i = 1, \dots, 9
$$

- $a_1 \to 1$, $a_{2,\dots,9} \to 0$ corresponds to **relaminarization** (turbulence decays) — explicitly excluded from the training distribution.
- The system is **chaotic**: initial perturbations of $O(10^{-6})$ around a seed trajectory (Kim, 2005) are used to generate **>10,000 datasets of 4,000 time units each**, discarding any trajectory that relaminarizes prematurely.
- Because the spatial modes $\boldsymbol{\phi}_i(\mathbf{x})$ are frozen, **all the dynamics lives in the 9 scalar time series** $a_i(t)$ — this is why the prediction task reduces to a pure time-series problem, decoupled from spatial reconstruction (Module 3).

### 1.2 Multilayer perceptron (MLP) — the non-temporal baseline

A layer of an MLP computes:

$$
\mathbf{z}^{(l)} = \mathbf{W}^{(l)} \mathbf{a}^{(l-1)} + \mathbf{b}^{(l)}, \qquad \mathbf{a}^{(l)} = g\!\left(\mathbf{z}^{(l)}\right)
$$

where $g(\cdot)$ is a nonlinear activation (sigmoid or $\tanh$ in this course). Without $g$, the entire network collapses algebraically into a **single matrix**, $\mathbf{W} = \mathbf{W}^{(L)}\mathbf{W}^{(L-1)}\cdots\mathbf{W}^{(1)}$ — depth would be meaningless. It is exactly the nonlinearity that (a) prevents this collapse and (b) gives the network its universal-approximation power.

**Loss function (mean squared error):**

$$
\mathcal{L} = \frac{1}{2N}\sum_{n=1}^{N} \left(\hat{a}_i^{(n)} - a_i^{(n)}\right)^2
$$

The factor $\tfrac{1}{2}$ exists purely so it cancels against the exponent when computing $\partial \mathcal{L}/\partial \mathbf{W}$ (a convention, not a numerical requirement).

**Training = backpropagation + stochastic gradient descent.** Because $\mathcal{L}$ is a composition of layer functions, the chain rule propagates $\partial \mathcal{L}/\partial \mathbf{W}^{(l)}$ backward from the output. SGD is *stochastic* because the full dataset (often $10^4$–$10^5$ points, with $10^6$–$10^8$ parameters) is split into random **batches**; one full pass over all batches is one **epoch**.

**MLP's structural limitation:** since it has no notion of sequence order beyond array position, predicting step $t+1$ from history requires **flattening the entire input window into one long vector**:

$$
\text{input dimension} = d = 9 \times p
$$

where $p$ is the number of past steps used. Because the architecture cannot exploit temporal correlation, $p$ must be made very large (e.g. $p=500 \Rightarrow d = 4{,}500$) purely to give the network enough raw history to infer dynamics — this is the central inefficiency motivating Section 1.3.

### 1.3 Recurrent Neural Networks (RNN) and LSTM

An RNN introduces a **recurrent connection**: the output (hidden state) of step $t-1$ becomes part of the input at step $t$, giving the architecture an explicit notion of sequence. Plain RNNs suffer from **vanishing gradients** — as the recurrence is unrolled many steps into the past, gradient magnitude decays and long-range dependencies are forgotten.

The **LSTM** (Hochreiter & Schmidhuber, 1997) fixes this with a gated memory cell. At each step $t$, given input $x_t$ and previous hidden/cell state $(h_{t-1}, C_{t-1})$:

$$
\begin{aligned}
f_t &= \sigma(W_f [h_{t-1}, x_t] + b_f) &&\text{(forget gate)}\\
i_t &= \sigma(W_i [h_{t-1}, x_t] + b_i) &&\text{(input gate)}\\
\tilde{C}_t &= \tanh(W_C [h_{t-1}, x_t] + b_C) &&\text{(candidate cell state)}\\
C_t &= f_t \odot C_{t-1} + i_t \odot \tilde{C}_t &&\text{(cell update)}\\
o_t &= \sigma(W_o [h_{t-1}, x_t] + b_o) &&\text{(output gate)}\\
h_t &= o_t \odot \tanh(C_t) &&\text{(hidden state / output)}
\end{aligned}
$$

$\odot$ is the Hadamard (element-wise) product. Each gate has **its own weight matrix and bias** — so a single LSTM "layer" carries roughly 4× the parameters of an equivalent dense layer, but needs a far shorter input window ($p=10$–$25$ vs. $p=500$ for the MLP) because the recurrence itself carries temporal information forward.

### 1.4 Transformers and attention

For long, multi-scale time series (high-$Re$ turbulence with well-separated fast/slow scales), even the LSTM's gating is insufficient — information from far in the past that still matters (e.g. a slow large-scale event) must survive many recurrent steps. The **Transformer** replaces recurrence with **attention**, which directly scores the relevance of every past sample to the current prediction, regardless of temporal distance:

$$
\mathrm{Attention}(Q, K, V) = \mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right) V
$$

where $Q$ (query), $K$ (key), $V$ (value) are learned linear projections of the input sequence and $d_k$ is the key dimension (scaling factor prevents saturated softmax gradients). The attention weights are **learned end-to-end** — the network is not told a priori which past samples matter; it discovers this from the data that minimizes prediction error.

### 1.5 Dynamical-systems validation: Lyapunov exponents & Poincaré maps

Because the underlying system is chaotic, **pointwise/instantaneous error is not a meaningful validation metric** on its own — two physically valid trajectories initialized $10^{-6}$ apart diverge exponentially (the butterfly effect). Two complementary diagnostics are used instead:

**Leading Lyapunov exponent.** Given a small initial perturbation $\delta(0)$, the Euclidean-norm separation between the perturbed and reference trajectories grows as:

$$
\|\delta(t)\| \approx \|\delta(0)\|\, e^{\lambda t}
$$

$\lambda$ (the slope of $\ln\|\delta(t)\|$ vs. $t$) is the leading Lyapunov exponent — it measures **how fast the chaotic system amplifies error**, independent of the sign/direction of the error. A model has "learned the correct dynamics" if injecting a perturbation equal to *the model's own prediction error* reproduces the **same slope $\lambda$** as injecting that perturbation into the true governing equations.

**Poincaré map.** A lower-dimensional joint probability density function (e.g. the joint PDF of modes $a_1$ and $a_3$ — the mean flow and streamwise-vortex amplitude) is used to check whether the model reproduces the correct **attractor geometry/correlation structure**, even when instantaneous trajectories have already diverged.

### 1.6 Turbulence-statistics error metric

Throughout this module, the relative error of a predicted mean/statistical profile $\hat{q}(y)$ against the reference $q(y)$ is:

$$
e_q = \frac{\left\| \hat{q}(y) - q(y) \right\|}{\max_y |q(y)|} \times 100\%
$$

normalizing by the profile maximum rather than a pointwise ratio (avoids blow-up near zero-crossings, e.g. in Reynolds shear stress).

---

## 2. Architecture Topology & Hyperparameters

### 2.1 MLP sweep (Srinivasan et al., *Phys. Rev. Fluids*, 2019)

Trained with **TensorFlow/Keras**, 1,000 time series (4,000 time units each), 20% validation split, MSE loss, $\tanh$ activation, Glorot & Bengio (2010) initialization, early stopping.

| Architecture | Hidden layers | Neurons/layer | Input window $p$ | Input dim | Mean-flow error | Fluctuation error | Validation loss |
|---|---|---|---|---|---|---|---|
| MLP1 | 4 | 45  | — | — | 1.84%  | 24.91% | $3.96\times10^{-5}$ |
| MLP2 | 3 | 90  | 500 | 4,500 | 10.96% | 36.16% | $4.38\times10^{-5}$ |
| MLP3 | 4 | 90  | — | — | 7.00%  | 29.04% | $3.90\times10^{-5}$ |
| MLP4 | 5 | 90  | — | — | 3.21%  | 18.61% | $3.84\times10^{-5}$ |
| MLP5 | 4 | 180 | — | — | 5.87%  | 27.85% | $3.99\times10^{-5}$ |

**Reading this table**: MLP2 (3 layers × 90 neurons, the architecture walked through live in Lecture1) is an example of **underfitting** — going deeper (MLP4, 5 layers) roughly halves both error metrics for the same neuron count, confirming that *depth*, not *width* (MLP5), is what buys accuracy here, because deeper hierarchical composition better matches turbulence's own multi-scale hierarchy.

### 2.2 LSTM sweep (same reference)

| Architecture | Input steps $p$ | Hidden layers ($N_1$,$N_2$) | Training datasets | Mean-flow error | Fluctuation error | Validation loss |
|---|---|---|---|---|---|---|
| LSTM1 | 10 | 90, — | 100 | 2.36% | 14.73% | $2.0\times10^{-8}$ |
| LSTM1 | 10 | 90, — | 1,000 | 0.83% | 3.44% | $8.5\times10^{-9}$ |
| **LSTM1** | **10** | **90, —** | **10,000** | **0.45%** | **2.49%** | $5.2\times10^{-9}$ |
| LSTM2 | 10 | 90, 90 | 100 | 1.94% | 6.82% | $2.4\times10^{-8}$ |
| LSTM3 | 25 | 90, — | 100 | 3.53% | 18.28% | $7.4\times10^{-8}$ |

The best model (bold) uses **only $p=10$ input steps** (vs. 500 for the MLP) and achieves an order of magnitude better accuracy — direct, quantitative evidence that exploiting temporal structure (recurrence) is far more data-efficient than brute-forcing a long input window into a non-temporal architecture. Increasing training set size from 100 → 10,000 trajectories is the single biggest lever on accuracy for a fixed architecture.

### 2.3 Higher-complexity regimes: when LSTM breaks down

- **Minimal turbulent channel** (Borrelli et al., *Int. J. Heat Fluid Flow* 96, 109010, 2022): a single LSTM **cannot handle the multi-scale behavior**. Fix: decompose the signal by POD, bin modes into **fast / intermediate / slow** frequency groups, and train **one LSTM per frequency group** — a Koopman-based framework with nonlinear forcing (KNF) was also explored as an alternative/complement.
- **Turbulent inflow generation** (Yousif et al., *J. Fluid Mech.* 957, A6, 2023): full turbulent multi-scale dynamics required a **Transformer**, since attention natively models the multi-scale character of turbulence without hand-splitting frequency bands.

### 2.4 Rule of thumb established in the lecture

> "In general, I would argue there's no reason to use an LSTM nowadays. You just use a transformer." — Prof. Vinuesa

Practical decision rule taught in this module:

| Data has... | Use |
|---|---|
| No temporal/spatial structure, point values only | MLP |
| Temporal structure, single dominant timescale | LSTM |
| Temporal structure, multiple well-separated timescales (turbulent, high $Re$) | Transformer |
| Spatial structure (images/flow fields) | CNN / GAN / U-Net (see Modules 3–4) |

---

## 3. Practical Insights & Edge Cases (Prof. Ricardo's Q&A)

- **Why does the MLP need 500 input steps but the LSTM only needs 10–25?** The MLP has no architectural mechanism to exploit temporal correlation — it treats the flattened input as an undifferentiated array of raw values, so it needs brute-force historical context to indirectly infer dynamics. The LSTM's recurrent connections *are* the temporal model, so far fewer raw samples suffice ("It's like predicting tomorrow's weather using the weather of 500 days, instead of the weather of 10 days.").
- **MAE vs. MSE?** Depends on data normalization. If data is scaled to $[-1,1]$ or $[0,1]$, MSE keeps predictions well-behaved in that range and avoids biasing toward positive/negative errors; this is why MSE is the default choice throughout the course.
- **Overfitting vs. underfitting, concretely:**
  - *Overfitting*: training loss keeps decreasing, but validation loss decreases then **increases** — the network has enough (or too much) capacity to memorize seen data but fails to generalize. Fixes: shrink the network, or get more/more-diverse data.
  - *Underfitting*: **both** training and validation loss stay high — the network doesn't have enough parameters/depth to represent the complexity of the data. Fix: go deeper (not necessarily wider — see §2.1) or change the architecture family entirely.
  - **Early stopping** is explicitly framed with a *Who Wants to Be a Millionaire?* analogy: once the validation loss reaches an acceptable level, stop and keep that checkpoint rather than risking further training pushing you into the overfitting regime.
- **"Why can't we restart training from an early-stopping checkpoint and change the architecture?"** You can restart and tune hyperparameters like learning rate from a checkpoint, but if you change the *architecture* (e.g. shrink a 100M-parameter network to 50M to fight overfitting), the old weights don't transfer — the checkpoint is tied to the specific architecture that produced it.
- **Why is Reynolds shear stress ($\overline{u'v'}$) easier to predict than the normal stresses?** It appears directly in the mean-momentum balance of a channel flow, so the network gets more indirect supervision on it; higher-order moments and normal stresses are structurally harder targets.
- **Error accumulation / the butterfly effect in autoregressive rollout:** a student explicitly raised the concern that feeding the model's own 11th-second prediction back in as input to predict the 12th second means errors compound. Confirmed: yes, this is fundamental to chaotic systems — even the *true* governing equations diverge from a $10^{-6}$-perturbed trajectory. The correct question is not "did the instantaneous values match?" but "did the model learn the correct dynamics (Lyapunov exponent, Poincaré map)?"
- **Is this a RANS model?** No — explicitly clarified as a **reduced-order model** (modal decomposition of an *unsteady* DNS-like system), not a Reynolds-Averaged (steady, mean-flow) description. RANS applications appear later via PINNs (Module 2).
- **Does this generalize to full 3D turbulence, not just the 9-equation model?** Yes — explicitly previewed that later modules (U-Net + 3D DNS, Module 4) show excellent full-turbulence performance; the 9-equation/LSTM material here is deliberately the simplest pedagogical stepping stone.
- **LSTM/Lorenz skepticism:** a student asked why we should trust LSTM for turbulence given known LSTM struggles on the (much simpler, but sensitive) Lorenz system. Answer: the 9-equation model already contains the essential near-wall turbulence physics and the LSTM performs *very well* on it; full 3D turbulence results are even better (shown in Module 4), specifically because the deep 3D U-Net architecture there is far more expressive than a plain LSTM.

---

## 4. Physical Diagnostic Framework

Before accepting any temporal model in this module, report the following (see also `#file:docs/copilot/physics_validation_rules.md` rules 1, 4, 6):

1. **Instantaneous field visualization** — check streak intensity and spanwise meandering qualitatively against the reference (a model that "looks flat" in spanwise meandering is under-resolving nonlinear modulation, see Module 3 §1).
2. **First- and second-order turbulence statistics**, computed via ensemble-averaging (200 fields in the reference study):
   - Mean streamwise velocity $U(y)$
   - Streamwise velocity fluctuation $u_{\mathrm{rms}}(y)$ (two-peak profile in this geometry)
   - Reynolds shear stress $\overline{u'v'}(y)$
   - Higher-order moments: skewness $\overline{u'^3}$, flatness $\overline{u'^4}$
   - RMS vorticity fluctuations in all three directions
3. **Relative error** per §1.6, reported separately for mean and fluctuating quantities — acceptance thresholds are application-dependent (the lecture explicitly refuses a universal number: "in some cases 10% error is acceptable, in some cases 0.1% is not").
4. **Poincaré map** (joint PDF of two low-order modes) — required whenever claiming a model "learned the dynamics" rather than just "fit the data."
5. **Lyapunov exponent slope match** — required for any chaotic/turbulent system; a model whose self-consistent perturbation growth rate slope doesn't match the reference has **not** learned the correct dynamics, regardless of low instantaneous error.
6. **Explicit acceptance table** used in this module:

| Metric | MLP (best, §2.1) | LSTM (best, §2.2) |
|---|---|---|
| Mean-flow relative error | 3.21% | **0.45%** |
| Fluctuation relative error | 18.61% | **2.49%** |
| Learns correct Lyapunov slope? | Not evaluated (point-prediction only) | **Yes** |
| Learns correct Poincaré correlation? | Not evaluated | **Yes** |

---

## 5. Implementation Logic

### 5.1 MLP baseline (PyTorch)

```python
import torch
import torch.nn as nn

class NineEqMLP(nn.Module):
    """Point predictor: p past steps of 9 coefficients -> next-step 9 coefficients.
    Matches MLP4 in the hyperparameter table: 5 hidden layers, 90 neurons/layer.
    """
    def __init__(self, p_steps: int = 500, n_coeffs: int = 9,
                 hidden_layers: int = 5, hidden_dim: int = 90):
        super().__init__()
        input_dim = p_steps * n_coeffs
        layers = [nn.Linear(input_dim, hidden_dim), nn.Tanh()]
        for _ in range(hidden_layers - 1):
            layers += [nn.Linear(hidden_dim, hidden_dim), nn.Tanh()]
        layers += [nn.Linear(hidden_dim, n_coeffs)]
        self.net = nn.Sequential(*layers)

    def forward(self, x_flat: torch.Tensor) -> torch.Tensor:
        # x_flat: (batch, p_steps * n_coeffs)
        return self.net(x_flat)


def train_epoch(model, loader, optimizer, device):
    model.train()
    loss_fn = nn.MSELoss()
    total_loss = 0.0
    for x, y in loader:
        x, y = x.to(device, dtype=torch.float32), y.to(device, dtype=torch.float32)
        optimizer.zero_grad()
        pred = model(x)
        loss = loss_fn(pred, y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * x.size(0)
    return total_loss / len(loader.dataset)
```

### 5.2 LSTM predictor (PyTorch)

```python
class NineEqLSTM(nn.Module):
    """LSTM1-equivalent: p=10 input steps, single hidden layer of 90 units."""
    def __init__(self, n_coeffs: int = 9, hidden_dim: int = 90, num_layers: int = 1):
        super().__init__()
        self.lstm = nn.LSTM(input_size=n_coeffs, hidden_size=hidden_dim,
                             num_layers=num_layers, batch_first=True)
        self.head = nn.Linear(hidden_dim, n_coeffs)

    def forward(self, x_seq: torch.Tensor) -> torch.Tensor:
        # x_seq: (batch, p_steps, n_coeffs) -- NOT flattened, unlike the MLP
        out, (h_n, c_n) = self.lstm(x_seq)
        last_hidden = out[:, -1, :]           # (batch, hidden_dim)
        return self.head(last_hidden)          # (batch, n_coeffs)
```

### 5.3 Lyapunov exponent estimation (diagnostic, not training code)

```python
import numpy as np

def leading_lyapunov_exponent(reference_traj: np.ndarray,
                               perturbed_traj: np.ndarray,
                               dt: float, fit_window: tuple[int, int]) -> float:
    """
    reference_traj, perturbed_traj: shape (T, 9), perturbed_traj[0] differs
    from reference_traj[0] by a small delta (e.g. 1e-6).
    Returns the slope (lambda) of ln||delta(t)|| vs t over the *linear* growth
    region (before saturation) -- select fit_window accordingly.
    """
    delta_norm = np.linalg.norm(perturbed_traj - reference_traj, axis=1)
    t = np.arange(len(delta_norm)) * dt
    lo, hi = fit_window
    coeffs = np.polyfit(t[lo:hi], np.log(delta_norm[lo:hi]), deg=1)
    lam = coeffs[0]
    return lam
```

### 5.4 Physics-validation gate for this module

Per `docs/copilot/physics_validation_rules.md` rule 6, any new temporal model in this module must be validated with:

```python
def validate_temporal_model(model, ref_traj, pert_traj_true, pert_traj_pred, dt):
    lam_true = leading_lyapunov_exponent(ref_traj, pert_traj_true, dt, fit_window=(0, 50))
    lam_pred = leading_lyapunov_exponent(ref_traj, pert_traj_pred, dt, fit_window=(0, 50))
    rel_diff = abs(lam_pred - lam_true) / abs(lam_true)
    assert rel_diff < 0.05, (
        f"Model does not reproduce chaotic growth rate: "
        f"lambda_true={lam_true:.4f}, lambda_pred={lam_pred:.4f}"
    )
```

This is a direct pytest-able regression test, satisfying the repo's test-automation standard ("any solver/ROM change requires a regression test comparing against a known analytical/DNS baseline").
