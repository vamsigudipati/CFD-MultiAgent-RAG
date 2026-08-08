## 1. Physical Problem Statement
* **Flow Regime & System Dynamics**: Incompressible Newtonian flows (2D and 3D) subject to passive scalar transport in arbitrary/complex domains (e.g., bluff body external flows, cardiovascular internal flows like arteries/brain aneurysms).
* **Governing Equations**: Passive scalar advection-diffusion equation combined with incompressible Navier-Stokes mass and momentum conservation laws:
  $$\rho(\partial_t c + \mathbf{u} \cdot \nabla c) = \kappa \nabla^2 c$$
  where $c$ is the scalar concentration (e.g., dye or smoke), $\mathbf{u}$ is the flow velocity field, $\rho$ is fluid density, and $\kappa$ is molecular diffusivity.
* **Target Quantities**: Infer latent velocity field $\mathbf{u}(\mathbf{x}, t)$ and pressure field $p(\mathbf{x}, t)$ directly from spatio-temporal visualizations/data of passive scalar field $c(\mathbf{x}, t)$.
* **Boundary & Initial Conditions**: Agnostic to specific initial and boundary conditions or complex domain geometries.
* *Traceability*: `HEADER: Abstract` (Page: UNAVAILABLE), `HEADER: 1. Introduction` (Page: UNAVAILABLE).

## 2. Network Architectures
* **Topology**: Deep Neural Networks (Physics-Informed Deep Learning / Deep Hidden Physics Models).
* **Specific Hyperparameters**: Specific layer counts, neuron counts, activation functions, and optimizer settings are not specified in the provided context chunk.
* *Traceability*: `HEADER: 1. Introduction` (Page: UNAVAILABLE).

## 3. Data Scaling & Normalization
* **Scaling Rules**: Unspecified in the provided text context.
* *Traceability*: `HEADER: 1. Introduction` (Page: UNAVAILABLE).

## 4. Required Physics Validation Gates
* **Validation Metrics**: Reconstruction accuracy of velocity $\mathbf{u}$ and pressure $p$ fields.
* **Derived Physical Quantities**:
  * Lift and drag forces in external flow past bluff bodies.
  * Wall shear stresses (WSS) in vascular networks/arteries.
* **Conservation Constraints**: Adherence to passive scalar transport equation and underlying Navier-Stokes conservation laws.
* *Traceability*: `HEADER: Abstract` (Page: UNAVAILABLE), `HEADER: 1. Introduction` (Page: UNAVAILABLE).

## 5. Architectural Innovations & Edge Cases
* **Key Innovations**:
  * Physics-Informed regularization embedding partial differential equations (Navier-Stokes and scalar transport) directly into neural network loss formulation.
  * Geometry-agnostic and boundary-condition-free data assimilation from flow visualization (passive scalar time-series).
* **Edge Cases**: Quantification of internal biomedical flows where direct velocity/pressure sensor placement is impractical.
* *Traceability*: `HEADER: Abstract` (Page: UNAVAILABLE), `HEADER: 1. Introduction` (Page: UNAVAILABLE).

## 6. Raw Data Corrections Log
* In `HEADER: 1. Introduction`, citation brackets were fragmented during extraction (e.g., `\[4,] [5\]`, `\[9,] [10\]`, `\[15,] [16\]`, `\[17][–23\]`).
* In `HEADER: 1. Introduction`, line wrap fragmented sentence clause across line break (`conservation of mass, momentum \n and energy`).