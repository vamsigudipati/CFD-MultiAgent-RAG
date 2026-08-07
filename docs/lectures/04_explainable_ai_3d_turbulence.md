# Module 4 — Explainable AI & 3D Coherent Structures

**Source material:** `Lecture3.txt` (final section), slide deck `2_Space.pptx` (slides 34–56, "Understanding turbulence through explainable AI").
**Scope:** 3D U-Net architecture for instantaneous flow-field prediction, Q-event segmentation, Kernel SHAP and Gradient SHAP for quantifying coherent-structure importance, and cross-validation against an independent experimental (PIV) dataset.

---

## 1. Mathematical Foundations

### 1.1 Defining "important" regions — three competing approaches

The lecture explicitly frames this module against two prior methodologies before introducing the course's own hybrid approach:

| Approach | Reference | Mechanism | Intrusive? |
|---|---|---|---|
| Perturbation-growth analysis | Encinar & Jiménez, *JFM* (2023) | Introduce perturbations into the flow, analyze their time evolution to define importance (identifies **strain-dominated vortex clusters**) | **Intrusive** — modifies the real flow, relies on simulation |
| Information-theoretic causality | Lozano-Durán & Arranz, *PRR* (2022) | Time-series causality: measure the effect on prediction error of one variable when another is removed | **Non-intrusive** — relies on temporal data only, flow itself is not modified |
| **Deep-learning + SHAP (this module)** | Cremades et al., *Nat. Commun.* 15, 3864 (2024) | Train a surrogate deep-learning predictor, then use game-theoretic feature attribution to score structure importance | **Intrusive on the surrogate model only** — the real flow/experiment is never touched, so it is applicable even to **data-limited settings such as experiments** |

### 1.2 Q-events: defining a coherent structure to attribute importance to

A **Q-event** (Lozano-Durán et al., 2012) is a 3D region where the instantaneous Reynolds-shear-stress contribution $u'v'$ is intense relative to the RMS of the individual components:

$$
\left|u'(\mathbf{x},t)\, v'(\mathbf{x},t)\right| > H\, u'_{\mathrm{rms}}(y)\, v'_{\mathrm{rms}}(y)
$$

for a chosen **hyperbolic-hole threshold** $H$ (the "percolation" parameter). Segmenting the domain by this criterion, then applying **percolation analysis**, groups adjacent intense-event grid points into discrete 3D (or 2D, for experimental slices) objects — these objects are the "features" whose importance is subsequently scored.

### 1.3 3D U-Net forward task

$$
\left(u'(\mathbf{x}, t_i),\, v'(\mathbf{x}, t_i),\, w'(\mathbf{x}, t_i)\right) \;\xrightarrow{\text{3D U-Net}}\; \left(u'(\mathbf{x}, t_{i+1}),\, v'(\mathbf{x}, t_{i+1}),\, w'(\mathbf{x}, t_{i+1})\right)
$$

with a fixed time-advancement horizon $t^+ = 5$ (viscous units); results were confirmed consistent for $t^+$ ranging from 1 to 10, i.e. the conclusions are not an artifact of one specific prediction horizon.

### 1.4 Shapley value (game-theoretic attribution)

For a "coalition game" where the players are the segmented flow structures and the "payout" is prediction accuracy, the Shapley value of structure $i$ is the *weighted average marginal contribution* of including that structure across all possible orderings/subsets $S$ of the other structures:

$$
\phi_i = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!\,\left(|F| - |S| - 1\right)!}{|F|!} \Big[ f(S \cup \{i\}) - f(S) \Big]
$$

where $F$ is the full set of structures and $f(\cdot)$ is the model's prediction accuracy given only the structures in the argument set present (others zeroed out).

### 1.5 Kernel SHAP — the tractable approximation actually used

Computing the exact Shapley sum above is combinatorially intractable for hundreds/thousands of structures. **Kernel SHAP** (Lundberg & Lee, 2017 — ~19k citations, described as "very well established in ML") instead fits a **linear surrogate model** $g$ of the true error function $f$:

$$
g(z') = \phi_0 + \sum_{i=1}^{M} \phi_i\, z'_i, \qquad z'_i \in \{0, 1\} \;\;(\text{structure } i \text{ present/absent})
$$

fit by minimizing a **weighted least-squares** loss over sampled coalitions $z'$:

$$
\mathcal{L}(f, g, \pi) = \sum_{z' \in Z} \Big[f(h(z')) - g(z')\Big]^2\, \pi_{z'}(z')
$$

where $\pi_{z'}$ is the Shapley kernel weighting function that up-weights very small and very large coalitions (these are the most informative for isolating individual marginal contributions), and $h(\cdot)$ maps the binary coalition vector back to an actual (partially-masked) flow field.

### 1.6 Gradient SHAP (used on the experimental dataset for efficiency)

Gradient SHAP (Erion et al., *Nat. Mach. Intell.*, 2021 — from the Su-In Lee group, same lineage as Kernel SHAP) computes attributions via **expected gradients**, integrating gradients of the model output along paths from random baseline samples to the input — computationally far cheaper than the coalition-sampling approach of Kernel SHAP, at the cost of losing the explicit combinatorial-coalition interpretation. Used here specifically because it is **more computationally efficient** and provides point-by-point SHAP values for $u'$ and $v'$ directly on the experimental grid.

### 1.7 The two core assumptions of Kernel SHAP (explicitly called out on the slides)

1. **Linearity of the surrogate model $g$.** In practice, because there are so many structures (features), the discrepancy between the true error function $f$ and the linear surrogate $g$ is empirically very small: $(f-g)^2 \sim 10^{-7}$.
2. **Coalition-weighted contribution accounting for inter-structure interaction.** Although any single structure's contribution is ultimately reported as one number, the underlying computation samples many **coalitions** (groups of co-present structures), which is what allows the method to account for inter-structure interactions in a highly chaotic, nonlinearly-coupled system like turbulence — a single-structure-removal experiment alone could not capture this.

---

## 2. Architecture Topology & Hyperparameters

### 2.1 3D U-Net

| Property | Value |
|---|---|
| Input | 3D velocity fluctuation field, 3 channels ($u', v', w'$) at time $t_i$ |
| Output | 3D velocity fluctuation field, 3 channels at time $t_{i+1}$ ($t^+=5$, validated for $t^+=1$–$10$) |
| Core operation | 3D convolutions (spatial information in all three directions) |
| Downsampling path | Convolution blocks + **max pooling**, 2 resolution-reduction levels |
| Bottleneck | Convolution blocks at lowest resolution |
| Upsampling path | **Transpose convolution**, 2 resolution-restoring levels, symmetric to the downsampling path |
| Skip connections | Feature maps from each encoder resolution level are concatenated/added to the matching decoder resolution level (the "U" shape) |
| Residual blocks | Combined with the convolution + pooling stack throughout |
| Padding | Periodic (matches the periodic streamwise/spanwise DNS domain) |
| Training data | DNS of turbulent channel flow, $Re_\tau = 125$, **~6,000 3D snapshots** |
| Baseline accuracy | **Mean relative error ≈ 2%** for $u'$ prediction (must be validated *before* any explainability analysis is meaningful) |

### 2.2 Explainability pipeline (end-to-end)

```
DNS 3D flow field (t_i)
        │
        ▼
Q-event segmentation (percolation, threshold H)  ──►  set of 3D structures (the "features")
        │
        ▼
3D U-Net predicts flow field at t_{i+1}
        │
        ▼
For each structure: zero its fluctuations, re-run U-Net prediction, measure error increase
        │
        ▼
Kernel SHAP: fit linear surrogate over sampled coalitions → SHAP value (importance score) per structure
```

### 2.3 Experimental cross-validation setup

| Property | Value |
|---|---|
| Facility | University of Melbourne towing-tank, collaboration with Ivan Marušić's group |
| Reference | Lee et al., *TSFP11* (2019) |
| Measurement technique | PIV (Particle Image Velocimetry) |
| Data volume | ~6,000 snapshots |
| Dimensionality | **2D** fields of $u$ and $v$ only (no $w$) |
| Reynolds number | $Re_\tau = 1{,}377$ (much higher than the $Re_\tau=125$ DNS) |
| Prediction horizon | $t^+ = 1.5$ |
| Structure sizing | **Area** (2D) instead of **volume** (3D) |
| First measurable point | $y^+=40$ — too far from the wall to distinguish attached vs. detached structures |
| Attribution method used | **Gradient SHAP** (§1.6), for computational efficiency on this larger, noisier, lower-resolution dataset |

### 2.4 Comparison with classically studied coherent structures (Cremades, Hoyas & Vinuesa, *Nat. Commun.* 16, 10189, 2025 — the follow-up study)

| Wall-normal location | SHAP structures agree most with... | Approximate coincidence |
|---|---|---|
| $y^+ = 15$ (very close to wall) | **Streaks** | **>90%** |
| Close to wall / channel center (intermediate) | **Q-events** | 60–70% |
| Channel center | **Vortices** | ~25% (moderate) |

**Headline conclusion of the follow-up paper**: *"The classically studied coherent structures only paint a partial picture of wall-bounded turbulence."* SHAP identifies importance that is not fully explained by any single classical structure category (Q-events, streaks, or vortices) at any wall-normal location.

---

## 3. Practical Insights & Edge Cases (Prof. Ricardo's Q&A)

- **"Are you removing structures across all time and length scales, or a specific range?"** Structures are removed **in the physical domain** (zeroing the fluctuation field within the segmented 3D volume for one snapshot) — **not** in spectral/Fourier space. This is an important distinction: the method operates entirely in physical space, structure by structure.
- **"Is this equivalent to classifying cats vs. dogs and inspecting which layer learned the whisker length?"** Yes, conceptually — a student explicitly drew this analogy to standard CNN interpretability (inspecting feature maps layer-by-layer), and the professor confirmed the same intuition applies: early layers encode simple/small features, later layers encode complex/large features, and this hierarchy is exactly what is exploited for transfer learning in Module 3.
- **"Is SINDy also an explainable-AI algorithm?"** No — explicitly distinguished: SINDy (Sparse Identification of Nonlinear Dynamics) discovers **governing equations** from data; explainability (SHAP) instead identifies **which input features/structures matter most** for a given (already-trained) model's predictions. They are connected in spirit (both aim at interpretability) but serve different purposes.
- **"What data is the U-Net trained on — is it seeing $t_i \to t_{i+1}$ pairs?"** Confirmed: yes, a repeated pattern of (current snapshot → future snapshot) pairs, where "future" specifically means a **few viscous time units ahead**, not literally the next saved snapshot.
- **Why use SHAP instead of directly ranking structures by their contribution to the Reynolds shear stress?** This is a central result of the module, not just a technical aside: SHAP importance and Reynolds-stress contribution are **correlated but not identical**. A dedicated joint-PDF analysis (SHAP value vs. structure volume) reveals three regions:
  - **Region A**: the SHAP-vs-volume relationship is a "band" that becomes a wide cone at larger volumes (increasing scatter/uncertainty).
  - **Region B**: structures with the **highest Reynolds-stress contribution** — the "classically" most important structures.
  - **Region C**: structures with the **highest SHAP value** — dominated by **medium-size, wall-attached ejections** (not the largest structures), plus some inward-interaction events. **Region C ≠ Region B.**
  - Practical implication raised directly in the lecture: *for flow control, target the high-SHAP structures (Region C), not simply the highest-Reynolds-stress structures (Region B)* — a different (and potentially more effective) actuation target than the traditional drag-reduction-by-largest-structure paradigm.
- **Per-unit-volume importance ranking** (a finer-grained finding): medium-size ejections have the **highest SHAP importance per unit volume**; attached structures have higher importance-per-volume than detached ones; large ejections have only medium importance-per-volume (their large total SHAP is partly just a volume effect); smaller sweeps and ejections have similar SHAP-per-volume to each other.
- **Does this generalize beyond the DNS training conditions?** This is explicitly tested, not assumed — the same framework was applied unchanged to a **completely different regime**: 2D (not 3D), much higher Reynolds number, lower spatial resolution, experimental (noisy) PIV data instead of clean DNS. Results were **qualitatively consistent** with the DNS-only conclusions ("results very similar to those in the DNS, with small differences"), which is presented as meaningful evidence that the SHAP-based importance ranking reflects real physics rather than a DNS-specific artifact.
- **Quantitative cross-validation number**: on the experimental dataset, there is a **70% overlap** between classical Q-events and the newly identified high-SHAP structures — high, but explicitly *not* 100%, meaning SHAP is finding importance that classical Q-event segmentation alone misses.
- **Why switch to Gradient SHAP for the experimental dataset instead of reusing Kernel SHAP?** Purely a computational-efficiency decision for the larger, real-world dataset — Gradient SHAP avoids the expensive coalition-sampling procedure of Kernel SHAP while still producing a usable point-by-point importance field.
- **Suggested future direction raised explicitly**: since SHAP identifies structures with different importance than classical Reynolds-stress-based ranking, this opens the door to **deep reinforcement learning (DRL) flow control policies that explicitly target SHAP-important structures** rather than simply minimizing drag or targeting the largest coherent structures.

---

## 4. Physical Diagnostic Framework

Before trusting any SHAP-based importance ranking in this repo, validate in this order:

1. **Baseline predictive accuracy of the surrogate (U-Net) itself** — report mean relative error of the *unperturbed* next-step prediction (reference: ~2% for $u'$). SHAP values computed on top of an inaccurate surrogate are meaningless; this check must pass first.
2. **Consistency across prediction horizon** — confirm importance rankings are stable for at least two different $t^+$ values (reference range validated: $t^+=1$ to $10$), not just a single arbitrarily chosen horizon.
3. **Surrogate-linearity sanity check for Kernel SHAP** — report $(f-g)^2$ (true error vs. linear-surrogate error) and confirm it is small (reference: $\sim10^{-7}$) before trusting the linear attribution decomposition.
4. **Joint PDF: SHAP value vs. structure volume/area** — required output, not optional; a single mean SHAP number per category hides the volume-confounding effect explicitly flagged in this module (§3, per-unit-volume ranking).
5. **Correlation analysis: SHAP value vs. Reynolds-stress contribution** — must be reported explicitly, since the entire scientific contribution of this method rests on demonstrating SHAP importance is *not* redundant with the classical Reynolds-stress-based ranking.
6. **Percolation-based overlap percentage** against each classical structure category (Q-events, streaks, vortices), stratified by wall-normal location — single-number "average agreement" is insufficient given the documented wall-distance dependence (90% at $y^+=15$ vs. ~25% at the centerline).
7. **Independent-dataset cross-validation** — wherever feasible, validate conclusions against a second dataset that differs in at least one of {dimensionality, Reynolds number, resolution, simulation vs. experiment}, following the DNS→PIV validation pattern in this module.

---

## 5. Implementation Logic

### 5.1 3D U-Net (PyTorch)

```python
import torch
import torch.nn as nn

class ConvBlock3D(nn.Module):
    def __init__(self, c_in, c_out):
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv3d(c_in, c_out, kernel_size=3, padding=1, padding_mode="circular"),
            nn.ReLU(inplace=True),
            nn.Conv3d(c_out, c_out, kernel_size=3, padding=1, padding_mode="circular"),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.block(x)


class UNet3D(nn.Module):
    """Predicts (u', v', w') at t_{i+1} from (u', v', w') at t_i.
    Two downsampling levels (max pool) + bottleneck + two upsampling
    levels (transpose conv) with skip connections, matching the
    Cremades et al. (2024) architecture description.
    """
    def __init__(self, in_channels: int = 3, base_channels: int = 32):
        super().__init__()
        self.enc1 = ConvBlock3D(in_channels, base_channels)
        self.pool1 = nn.MaxPool3d(2)
        self.enc2 = ConvBlock3D(base_channels, base_channels * 2)
        self.pool2 = nn.MaxPool3d(2)

        self.bottleneck = ConvBlock3D(base_channels * 2, base_channels * 4)

        self.up2 = nn.ConvTranspose3d(base_channels * 4, base_channels * 2, kernel_size=2, stride=2)
        self.dec2 = ConvBlock3D(base_channels * 4, base_channels * 2)  # doubled: skip concat
        self.up1 = nn.ConvTranspose3d(base_channels * 2, base_channels, kernel_size=2, stride=2)
        self.dec1 = ConvBlock3D(base_channels * 2, base_channels)      # doubled: skip concat

        self.head = nn.Conv3d(base_channels, in_channels, kernel_size=1)

    def forward(self, x):
        e1 = self.enc1(x)
        e2 = self.enc2(self.pool1(e1))
        b = self.bottleneck(self.pool2(e2))

        d2 = self.up2(b)
        d2 = self.dec2(torch.cat([d2, e2], dim=1))   # skip connection
        d1 = self.up1(d2)
        d1 = self.dec1(torch.cat([d1, e1], dim=1))   # skip connection

        return self.head(d1)   # (batch, 3, D, H, W) -- (u', v', w') at t_{i+1}
```

### 5.2 Q-event segmentation (percolation-style)

```python
import numpy as np
from scipy import ndimage

def segment_q_events(u_fluc: np.ndarray, v_fluc: np.ndarray, H: float) -> np.ndarray:
    """
    u_fluc, v_fluc: 3D arrays (Nx, Ny, Nz) of instantaneous fluctuations.
    H: hyperbolic-hole threshold (percolation parameter).
    Returns an integer-labeled array where each connected region above
    threshold is a distinct Q-event structure (label 0 = background).
    """
    u_rms = u_fluc.std()
    v_rms = v_fluc.std()
    intensity = np.abs(u_fluc * v_fluc)
    mask = intensity > (H * u_rms * v_rms)
    labeled, n_structures = ndimage.label(mask)
    return labeled, n_structures
```

### 5.3 Structure-removal + error-based importance (the "brute-force" step behind SHAP)

```python
def prediction_error_with_structures_removed(model, field_t, field_t1_true,
                                              labeled_structures, keep_labels):
    """Zeros out fluctuations for all structures NOT in `keep_labels`,
    re-runs the U-Net, and returns the prediction error -- this is f(S)
    in the Shapley-value formula (Section 1.4/1.5)."""
    masked_field = field_t.clone()
    for label_id in np.unique(labeled_structures):
        if label_id == 0 or label_id in keep_labels:
            continue
        mask = torch.from_numpy(labeled_structures == label_id)
        masked_field[:, mask] = 0.0  # zero fluctuations for removed structures

    with torch.no_grad():
        pred_t1 = model(masked_field.unsqueeze(0))

    error = (pred_t1.squeeze(0) - field_t1_true).pow(2).mean().sqrt()
    return error.item()
```

### 5.4 Kernel SHAP importance scoring (conceptual, using the `shap` library)

> Note: the KTH-FlowAI group publishes a companion tutorial repository for this exact workflow — see `KTH-FlowAI/Tutorial_SHAP` (referenced in this project's prior GitHub-repository research) for a working Kernel/Gradient/Deep SHAP example adapted from `shap.readthedocs.io`.

```python
import shap
import numpy as np

def compute_structure_shap_values(model, field_t, field_t1_true,
                                   labeled_structures, n_structures, n_samples=2000):
    """Fits a Kernel SHAP linear surrogate over sampled structure coalitions."""

    def f(coalition_matrix: np.ndarray) -> np.ndarray:
        # coalition_matrix: (n_coalitions, n_structures), binary presence/absence
        errors = np.zeros(coalition_matrix.shape[0])
        for i, coalition in enumerate(coalition_matrix):
            keep_labels = set(np.nonzero(coalition)[0] + 1)  # labels are 1-indexed
            errors[i] = prediction_error_with_structures_removed(
                model, field_t, field_t1_true, labeled_structures, keep_labels
            )
        return errors

    background = np.zeros((1, n_structures))       # "all structures removed" baseline
    explainer = shap.KernelExplainer(f, background)
    all_present = np.ones((1, n_structures))
    shap_values = explainer.shap_values(all_present, nsamples=n_samples)
    return shap_values   # one importance score (phi_i) per structure
```

### 5.5 Physics-validation gate for this module

Per `docs/copilot/physics_validation_rules.md`, any explainability result must be reported alongside the underlying surrogate's own validated accuracy:

```python
def validate_xai_pipeline(model, val_loader, shap_values, reynolds_stress_contrib,
                           tol_baseline_error=0.03, min_corr_with_reynolds_stress=None):
    # 1. Baseline surrogate accuracy must be validated first (rule: garbage in, garbage out)
    rel_errors = []
    for field_t, field_t1_true in val_loader:
        with torch.no_grad():
            pred = model(field_t)
        rel_errors.append(((pred - field_t1_true).norm() / field_t1_true.abs().max()).item())
    mean_rel_error = float(np.mean(rel_errors))
    assert mean_rel_error < tol_baseline_error, (
        f"U-Net baseline error {mean_rel_error:.2%} too high to trust SHAP attributions"
    )

    # 2. SHAP must NOT be redundant with Reynolds-stress contribution (that's the whole point)
    correlation = np.corrcoef(shap_values, reynolds_stress_contrib)[0, 1]
    report = {"mean_rel_error": mean_rel_error, "shap_vs_reynolds_stress_corr": correlation}
    if min_corr_with_reynolds_stress is not None:
        # Explicitly check SHAP finds *different* information, not just re-deriving Re-stress ranking
        assert correlation < 0.95, "SHAP appears redundant with Reynolds-stress contribution"
    return report
```
