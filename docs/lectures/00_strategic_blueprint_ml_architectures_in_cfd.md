# Chapter: Strategic Blueprint for ML Architectures in CFD Workflows

> **Provenance note:** This chapter was verified against the four source-grounded reference manuals in [`docs/lectures/`](./) (extracted from the course transcripts and slide decks). All architecture choices, ROI figures, and validation thresholds below are traceable to that material. Additions relative to the original draft are marked **[Added]**; nothing was removed, only clarified.

This chapter outlines the strategic integration of Deep Learning (DL) architectures into classical Computational Fluid Dynamics (CFD) workflows. Rather than treating ML as a black-box replacement for Navier-Stokes solvers, we deploy specific architectures to target known computational bottlenecks: accelerating Direct Numerical Simulations (DNS), refining turbulence closures, and developing stable Reduced-Order Models (ROMs).

## 1. Architecture Selection Decision Matrix

The selection of a neural architecture is dictated strictly by the physical and temporal structure of the fluid regime.

- **Pointwise / No Spatial Structure:** Multilayer Perceptrons (MLPs). *Note: Highly inefficient for temporal sequences due to flattened input windows (e.g. 500 past steps needed vs. 10 for an LSTM on the same problem).*
- **Temporal Dynamics (Single Dominant Timescale):** Long Short-Term Memory (LSTM) networks. Suitable for low-dimensional chaotic systems (e.g., 9-equation near-wall cycle). **[Added]** For an intermediate regime — a minimal channel with a *few* well-separated timescales but not yet broadband turbulence — a single LSTM is insufficient; the validated fallback is **one LSTM per POD-frequency band** (fast/intermediate/slow) before committing to the higher cost of a full Transformer.
- **Temporal Dynamics (Broadband / High $Re$):** Transformers. Self-attention natively handles the multi-scale character of turbulence without manual frequency-band splitting. Working rule of thumb from the source lectures: *if the flow is turbulent and multi-scale, default to a Transformer over an LSTM.*
- **Unclosed / Unmodeled Steady PDEs:** Physics-Informed Neural Networks (PINNs). Ideal for RANS closures and denoising sparse experimental (PIV) data. **[Added — see caveat in §3.1]** PINNs are computationally slower than a conventional solver on an equivalent mesh; the ROI case rests on closure-free accuracy and coarser-mesh tolerance, not on raw speed.
- **Spatial Field Reconstruction (Near-Wall):** Fully Convolutional Networks (FCNs). Captures highly entangled, non-linear modulation.
- **Spatial Field Reconstruction (Far-Field):** FCN-POD Hybrids. Predicts temporal coefficients of pre-computed POD bases where energy is concentrated in few large-scale modes.
- **Super-Resolution & Sparse Sensing:** Generative Adversarial Networks (GANs). Generator/Discriminator pairs reliably reconstruct high-frequency structures (e.g., streaks) from heavily downsampled ($16^2\times$) inputs.
- **3D Spatial-Temporal Trajectories & Explainability:** 3D U-Nets with skip connections. Essential for volumetric tracking of coherent structures (Q-events) and SHAP-based importance attribution.

**[Added] Generalization caveat applicable to the whole matrix:** the CNN/FCN/GAN architectures above are, by design, **case-specific** — they are trained and validated for a fixed Reynolds number and geometry and are not expected to generalize across flow conditions. Where cross-case generalization is the actual requirement, the validated path in the source material is a generative/diffusion-based foundation-model approach, not an incremental extension of these architectures.

## 2. Direct Numerical Simulation (DNS) Acceleration

DNS is computationally prohibitive at high Reynolds numbers. We leverage spatial ML architectures to bypass expensive grid resolution requirements and accelerate convergence.

### 2.1 Spatial Transfer Learning Across $Re_\tau$

- **Strategy:** Train a spatial prediction network (e.g., CNN or FCN) on cheap, low-Reynolds-number DNS data (e.g., $Re_\tau = 180$). To deploy at a higher Reynolds number ($Re_\tau = 550$), initialize the network with the converged low-$Re$ weights (full-network initialization, not partial freezing) and reduce the learning rate.
- **ROI:** Achieves baseline accuracy while cutting the expensive high-$Re$ DNS data requirement by **75%**.
- **[Added] Complementary, cheaper strategy — cross-wall-distance transfer:** when the deployment target is a *different wall-normal plane* at the *same* $Re_\tau$ (not a different Reynolds number), freeze only the first ~3 (shallow, small-scale) layers and retrain the last ~3 (deep, large-scale) layers. This is a distinct lever from the $Re_\tau$-transfer strategy above and yields comparable accuracy at roughly **4× lower training time** — cheaper to apply when the deployment change is "where in the domain," not "which Reynolds number."

### 2.2 Super-Resolution via GANs

- **Strategy:** Deploy a two-stage GAN pipeline. The Generator takes coarse wall fields and predicts high-resolution wall data. The generated data is then fed into a CNN to predict off-wall velocity fluctuations ($u', v', w'$).
- **ROI:** Accurately locates and scales streaks and large-scale footprints even at $16^2\times$ downsampling, drastically reducing the sensor/grid resolution needed for near-wall flow control.

### 2.3 Required Validation (per `#file:docs/copilot/physics_validation_rules.md`)

- **Energy Spectra:** Pointwise MSE is insufficient. 2D pre-multiplied power spectral density ($k_x k_z E(k_x, k_z)$) must be evaluated to guarantee high-wavenumber (small-scale) kinetic energy is not artificially smoothed out by the convolutions.

## 3. Turbulence Model Refinement (RANS)

Traditional industrial solvers rely on empirical eddy-viscosity models (Boussinesq approximations) that fail to capture Reynolds-stress anisotropy, particularly in adverse pressure gradients or separated flows.

### 3.1 Unsupervised RANS Closure via PINNs

- **Strategy:** Bypass turbulence modeling entirely. Use a PINN to solve the unclosed 2D incompressible RANS equations by treating the Reynolds stresses ($\overline{u'^2}, \overline{u'v'}, \overline{v'^2}$) as direct network outputs alongside $U, V,$ and $P$.
- **Integration:** Use Automatic Differentiation (`tf.GradientTape` or `torch.autograd`) to compute exact spatial derivatives ($U_{xx}, U_{yy}$). Apply a joint loss function balancing the unsupervised PDE residual ($\mathcal{L}_e$) and supervised Dirichlet boundary conditions ($\mathcal{L}_b$).
- **ROI:** Achieves mean-flow errors of $<2\%$ and Reynolds-stress errors of $<10\%$ on attached flows, drastically outperforming standard industrial RANS closures. Separated flows (e.g. periodic hill) are a harder regime — expect Reynolds-stress error in the 15–30% band, which is still favorable relative to industrial solvers on the same case but should not be compared against the attached-flow bar above.
- **[Added] Cost caveat — do not present this as a pure speed win:** PINNs are consistently reported as **at least an order of magnitude slower than a conventional CFD/RANS solver on an equivalent mesh.** The ROI case here is *closure-free accuracy* and tolerance of *coarser meshes* (automatic differentiation gives exact gradients, so resolution requirements relax) — not raw wall-clock speed. Do not deploy a PINN where a conventional solver already meets accuracy requirements; do not hybridize a PINN with a commercial solver expecting a speed multiplier — they solve the same equations by different, non-composable means.
- **[Added] Boundary-condition caveat:** the PDE/boundary loss weighting is not self-balancing — an over-weighted boundary term can converge to a low total loss with an inaccurate interior solution. Report $\mathcal{L}_e$ and $\mathcal{L}_b$ separately (see §3.2), and be aware PINNs can converge to a low-residual but **unphysical** solution in a way a classical solver cannot; there is no established mesh/collocation-point convergence study equivalent to a classical grid-convergence study.

### 3.2 Required Validation

- **Per-Equation Residuals:** The continuity, x-momentum, and y-momentum residuals must be evaluated and reported independently. A total loss score can hide a specific un-converged physical equation.
- **Threshold:** Any architectural change that increases the residual norm by $>5\%$ against the baseline is rejected.

## 4. Reduced-Order Models (ROMs) & Flow Control

For time-series forecasting and flow control policy generation, the network must capture the non-linear dynamics and phase-space geometry of the system.

### 4.1 Chaotic Attractor Forecasting

- **Strategy:** Use LSTMs (for filtered/narrowband inputs) or Transformers (for multi-scale turbulent inputs) to predict the temporal evolution of POD mode coefficients.
- **Explainability-Driven Control:** Run 3D U-Nets coupled with Kernel/Gradient SHAP on segmented Q-events. SHAP analysis reveals that **medium-size wall-attached ejections** yield the highest importance per unit volume—not the structures with the absolute highest Reynolds stress.
- **Integration:** Feed SHAP-identified target structures into Deep Reinforcement Learning (DRL) agents. The environment (simulation) rewards the agent for manipulating these specific high-impact structures, offering a more precise control strategy than blind drag-reduction optimization.
- **[Added] Prerequisite gate:** the SHAP analysis above is only meaningful once the underlying 3D U-Net surrogate is itself validated (reference baseline: ~2% mean relative error on next-step velocity prediction). SHAP values computed on an unvalidated surrogate are not trustworthy — validate the surrogate first, attribute importance second.

### 4.2 Required Validation

- **Dynamical Fidelity:** Because instantaneous autoregressive predictions will diverge exponentially due to chaos, instantaneous MSE is discarded for long-horizon validation.
- **Lyapunov Exponents:** The surrogate model's separation growth rate ($\lambda$) must match the true governing equations.
- **Poincaré Maps:** The network must correctly reproduce the joint PDF correlation (e.g., mean flow vs. streamwise-vortex amplitude) to verify it has learned the true physical attractor geometry.

## 5. MLOps, Scaling, and Deployment Standards

To transition these models from research scripts to production CFD environments, the following MLOps standards (per `#file:docs/copilot/mlops_scaling_rules.md`) are strictly enforced across the repository:

1. **Reproducibility & Tracking:** Every hyperparameter, Git commit, and framework seed (PyTorch/Numpy RNG) must be locked and logged via MLflow or Weights & Biases. Configuration must be handled via Hydra/YAML—no hardcoded variables in the execution scripts.
2. **Dataset Versioning:** All DNS/LES snapshot data and boundary condition arrays must be versioned via DVC. Physical normalization strategies (e.g., standardizing to $y^+$ inner units) must be explicitly recorded, as silent scaling changes will break downstream PINN differential physics losses.
3. **Distributed Scaling:** All models must clear a single-GPU correctness baseline and a 1-epoch CI smoke test before invoking `DistributedDataParallel`. Learning rates must scale proportionally with effective batch size when distributing across multi-node clusters.
4. **Mixed Precision Limits:** `torch.cuda.amp` (FP16) may only be enabled if it does not degrade the conservation residuals. (PINN PDE losses involving second-order gradients are highly sensitive to FP16 underflow).

---

## Verification Summary

| Claim checked | Status | Source |
|---|---|---|
| LSTM needs far more input steps than Transformer handles natively; MLP needs ~500 steps vs. LSTM's 10 | ✅ Confirmed | `01_temporal_predictions_and_chaos.md` §2 |
| Cross-$Re_\tau$ transfer learning → 75% data reduction at equal accuracy | ✅ Confirmed | `03_spatial_sensing_cnns_and_gans.md` §2.5(b) |
| Cross-wall-distance transfer learning (freeze first 3 layers) → ~4× training-time reduction | ✅ Confirmed, **was missing from original draft** | `03_spatial_sensing_cnns_and_gans.md` §2.5(a) |
| GAN reconstruction robust to $16^2$ downsampling | ✅ Confirmed | `03_spatial_sensing_cnns_and_gans.md` §2.6 |
| PINN mean-flow <2%, Reynolds-stress <10% on attached flows | ✅ Confirmed | `02_pinns_rans_and_measurement_piv.md` §2.1 |
| PINNs are ≥1 order of magnitude slower than CFD | ✅ Confirmed, **was missing from original draft** | `02_pinns_rans_and_measurement_piv.md` §3 |
| Per-equation PDE residual reporting requirement | ✅ Confirmed | `02_pinns_rans_and_measurement_piv.md` §4 |
| SHAP importance ≠ Reynolds-stress contribution; medium attached ejections highest per-volume importance | ✅ Confirmed | `04_explainable_ai_3d_turbulence.md` §3 |
| Lyapunov exponent / Poincaré map as required dynamical validation | ✅ Confirmed | `01_temporal_predictions_and_chaos.md` §4 |
| CNN/FCN architectures don't generalize across cases/geometries by design | ✅ Confirmed, **was missing from original draft** | `03_spatial_sensing_cnns_and_gans.md` §3 |
| MLOps rules (MLflow/W&B, Hydra, DVC, DDP smoke test, FP16 caveat) | ✅ Confirmed | `docs/copilot/mlops_scaling_rules.md` (repo standard, not lecture-derived) |
