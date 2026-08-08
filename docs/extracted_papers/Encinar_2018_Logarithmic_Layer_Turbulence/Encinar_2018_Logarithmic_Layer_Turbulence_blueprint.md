## 1. Physical Problem Statement
- **Domain & Flow Regime**: Incompressible wall-bounded turbulent channel flow governed by the incompressible Navier-Stokes equations:
  $$\nabla \cdot \mathbf{u} = 0$$
  $$\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla)\mathbf{u} = -\nabla p + \frac{1}{Re_\tau} \nabla^2 \mathbf{u}$$
  Simulations span friction Reynolds numbers $Re_\tau = \frac{u_\tau h}{\nu} \in \{932, 2003, 5300\}$.
- **Geometry & Boundary Conditions**: 
  - Periodic boundary conditions in the streamwise ($x$) and spanwise ($z$) directions.
  - Domain dimensions $(L_x, L_z) = (2\pi h, \pi h)$ for small domain DNS (S1000, S2000) and $(8\pi h, 3\pi h)$ for large-box datasets (F2000, F5300).
  - No-slip and no-penetration boundary conditions at the solid walls ($y = 0, 2h$).
- **Flow Variables & Wall Observables**:
  - Target internal state: Fluctuation velocity components $\mathbf{u}' = (u, v, w)^T$ and kinematic pressure $p$ across the buffer layer ($y^+ < 20$) and logarithmic layer ($80\nu/u_\tau \le y \le 0.2h$).
  - Input wall sensors: Streamwise wall-shear stress $\tau_{x,w} = \mu \left.\frac{\partial u}{\partial y}\right|_w$, spanwise wall-shear stress $\tau_{z,w} = \mu \left.\frac{\partial w}{\partial y}\right|_w$, and wall pressure fluctuation $p_w = p(x, 0, z, t)$.
- **Nature of Paper**: Statistical fluid dynamics and Linear Stochastic Estimation (LSE) analysis using Direct Numerical Simulation (DNS) datasets. The study evaluates linear reconstructability and observability of logarithmic-layer turbulence from wall measurements; it does not implement a neural-network architecture.

## 2. Network Architectures
N/A — not a fluid-dynamics ML modeling paper (uses Linear Stochastic Estimation / linear statistical regression on DNS datasets; no artificial neural network topology, layers, or deep learning models are present).

## 3. Data Scaling & Normalization
- **Wall Units (Viscous Non-Dimensionalization)**:
  - Velocity scale: Friction velocity $u_\tau = \sqrt{\frac{\tau_w}{\rho}}$.
  - Length scale: Viscous length scale $\delta_\nu = \frac{\nu}{u_\tau}$.
  - Scaled coordinates and velocity fluctuations ($+$ superscript):
    $$x^+ = \frac{x u_\tau}{\nu}, \quad y^+ = \frac{y u_\tau}{\nu}, \quad z^+ = \frac{z u_\tau}{\nu}$$
    $$u^+ = \frac{u}{u_\tau}, \quad v^+ = \frac{v}{u_\tau}, \quad w^+ = \frac{w}{u_\tau}, \quad p^+ = \frac{p}{\rho u_\tau^2}$$
- **Outer Units**:
  - Length scaled by channel half-height $h$: $y/h, L_x/h, L_z/h$.
  - Integration time scaled by turnover units: $\frac{T u_\tau}{h}$.
- **Spectral Space Scaling**:
  - Wavelengths: Streamwise $\lambda_x = \frac{2\pi}{k_x}$ and spanwise $\lambda_z = \frac{2\pi}{k_z}$.

## 4. Required Physics Validation Gates
- **Turbulent Kinetic Energy & Reynolds Stresses**:
  - Reconstruction accuracy of the tangential Reynolds stress $\langle -u'v' \rangle$ up to $y/h \approx 0.2$.
  - Capture fraction of total kinetic energy for wall-attached structures in the logarithmic region ($\ge 50\%$).
- **Spectral Mass Distribution**:
  - Two-dimensional premultiplied energy spectra $k_x k_z E_{ii}(\lambda_x, \lambda_z, y)$ for velocity components $u, v, w$.
  - Accurate capture of spectral mass boundaries containing $50\%$, $70\%$, and $90\%$ of total variance at $y^+ = 5$.
- **Dissipation Profiling**:
  - Reproduction of integrated energy dissipation rate across $y^+ < 20$ (dominated by mean shear) and logarithmic interval $80\nu/u_\tau \le y \le 0.2h$ ($\approx 40\%$ of total fluctuation energy loss).

## 5. Architectural Innovations & Edge Cases
- **Observability Upper Bound**: Linear Stochastic Estimation (LSE) establishes the theoretical maximum bound of linear observability from wall measurements, showing that decorrelation occurs for scales detached from the wall beyond $y/h \approx 0.2$.
- **DNS Data Subsampling for Large Boxes**: For F2000 and F5300 datasets, spatial fields are stored at filtered LES-like resolutions ($\delta x^+ \approx 120$, $\delta z^+ \approx 90$) while preserving full DNS wall pressure spectrum physics computed prior to filtering.

## 6. Raw Data Corrections Log

| Raw Text / Fragment | Corrected Representation | Section | Page |
| :--- | :--- | :--- | :--- |
| `Javier Jim´enez` | `Javier Jiménez` | `Logarithmic-layer turbulence: a view from the wall` | UNAVAILABLE |
| `y/h . 0.2` | $y/h \lesssim 0.2$ | `Logarithmic-layer turbulence: a view from the wall` | UNAVAILABLE |
| `∆$^{x}$ $^{+}$ = 100` | $\Delta x^+ = 100$ | `Logarithmic-layer turbulence: a view from the wall > I. INTRODUCTION` | UNAVAILABLE |
| `D$^{y}$` | $D_y$ | `Logarithmic-layer turbulence: a view from the wall > I. INTRODUCTION > II. NUMERICAL EXPERIMENTS` | UNAVAILABLE |
| `N$^{f}$` | $N_f$ | `Logarithmic-layer turbulence: a view from the wall > I. INTRODUCTION > II. NUMERICAL EXPERIMENTS` | UNAVAILABLE |
| `108` (Table I, Case F5300, $N_z$ column) | `108` (Inferred truncation in raw extraction table; $N_z$ for F5300) | `Logarithmic-layer turbulence: a view from the wall > I. INTRODUCTION > II. NUMERICAL EXPERIMENTS` | UNAVAILABLE |