#### UNIVERSITY OF CALIFORNIA SANTA BARBARA

#### Transient Growth for a Sinusoidal Shear Flow Model

by

Lina Kim

A thesis submitted in partial satisfaction of the requirements for the degree of Master of Science

in

Mechanical Engineering

Committee in charge: Professor Jeffrey Moehlis, Chair Professor George Homsy Professor Bassam Bamieh

September 2005

The Thesis of Lina Kim is approved:

Professor George Homsy

Professor Bassam Bamieh

Professor Jeffrey Moehlis, Chair

August 2005

#### Transient Growth for a Sinusoidal Shear Flow Model

Copyright 2005

by

Lina Kim

#### Abstract

#### Transient Growth for a Sinusoidal Shear Flow Model

by

Lina Kim

Turbulence is widely recognized as one of the most important unsolved problems in classical physics. The special case of shear flow turbulence, to be considered in this thesis, has the interesting property that turbulence is found both experimentally and in numerical simulations for values of the Reynolds number well below the value at which the laminar state loses stability. Turbulent shear flows are of great particular interest; indeed, the ability to understand and control these flows will lead to dramatic improvements in the efficiency and performance of many technological devices. A growing body of literature has suggested that the phenomenon of transient energy growth provides the key to understanding properties of shear flow turbulence.

This thesis contributes to the study of properties of shear flow turbulence by investigating transient energy growth due to the linear interaction between streaks and streamwise vortices for a nine-dimensional ordinary differential equation model. The model is based on Fourier modes for sinusoidal shear flow, in which fluid between two free-slip walls experiences a time-independent streamwise body force which varies sinusoidally in the wall-normal direction. In particular, an analysis of how transient energy growth due to linear effects depends on initial conditions and parameters such as Reynolds number and aspect ratio will be conducted. Additionally, the importance of transient energy growth for triggering nonlinear effects which can lead to sustained turbulence will be explored.

For this research, the initial perturbations which give optimal initial and total energy growth are obtained and a neutral transient growth curve, below which no initial condition gives transient energy growth, is defined. These results are compared to those obtained using pseudospectra analysis. Furthermore, the sensitivity of the perturbations to the laminar state is examined. These results represent a powerful generalization of standard hydrodynamic stability analysis to systems which lack a linear instability. The standard analysis only captures asymptotic behavior since it is limited to just calculating eigenvalues and the analysis in this thesis overcomes these limitations by usefully capturing the transient behavior and the importance of different initial distributions of energy.

To my parents and family.

### Contents

| List | of            | Figures          |                |            |          |            |                          | ix             |
|------|---------------|------------------|----------------|------------|----------|------------|--------------------------|----------------|
| 1    | Introduction  |                  |                |            |          |            |                          | 1              |
| 1.1  |               | Fundamental      | Fluid          |            | Dynamics |            | Equations                | 3              |
| 1.2  | A             | Nine-Dimensional |                |            | Model    | for        | Sinusoidal Shear Flow    | 6              |
|      | 1.2.1         |                  | Formulation    | of         | Modes    |            |                          | 7              |
|      | 1.2.2         | Galerkin         |                | Projection |          |            |                          | 9              |
| 2    | Transient     | Growth           | for            |            | the      |            | Streak-Streamwise Vortex | Interaction 12 |
| 2.1  |               | Geometric        | Interpretation |            | of       |            | Transient Energy Growth  | 14             |
| 2.2  |               | Optimal          | Transient      |            | Energy   | Growth     |                          | 15             |
| 2.3  |               | Application      | to Model       |            |          |            |                          | 17             |
|      | 2.3.1         | General          |                | Results    |          |            |                          | 17             |
|      | 2.3.2         | Neutral          |                | Transient  |          | Growth     |                          | 21             |
|      | 2.3.3         | Results          | for            | L z        | = 1 2    | π          |                          | 24             |
|      | 2.3.4         | Results          | for            | L z        | = 2 π    |            |                          | 30             |
| 3    | Pseudospectra |                  | Analysis       |            |          |            |                          | 35             |
| 3.1  |               | Results for L    | z = 1          | 2 π        |          |            |                          | 37             |
| 3.2  |               | Results for L    | z = 2 π        |            |          |            |                          | 38             |
| 4    | Transient     | Growth           | and            |            | the      | Transition | to Turbulence            | 42             |
| 4.1  | A             | Four-Mode        | Subspace       |            |          |            |                          | 43             |
|      | 4.1.1         | Optimal          |                | Growth     | of       | the        | Nonlinear Term N 23      | 44             |
|      | 4.1.2         | Results          | for            | L z        | = 1 2    | π          |                          | 46             |
|      | 4.1.3         | Results          | for            | L z        | = 2 π    |            |                          | 47             |
|      | 4.1.4         | Time             | Evolution      |            | due      | to         | Nonlinear Interactions   | 47             |
| 4.2  | The           | Full             | Nine-Mode      |            | Model    |            |                          | 57             |
| 5    | Conclusion    |                  |                |            |          |            |                          | 63             |
|      | Bibliography  |                  |                |            |          |            |                          | 66             |

A Finding a Lower Bound for Transient Energy Growth Using Kreiss' Theorem 71 B Proof that Streamwise Invariance Leads to Decay 74

### List of Figures

| 1.1  | Geometry        | for            | sinusoidal     |             | shear     | flow         |             |          |                        | 5              |
|------|-----------------|----------------|----------------|-------------|-----------|--------------|-------------|----------|------------------------|----------------|
| 2.1  | Geometrical     | interpretation |                |             |           | of transient |             | growth   |                        | 15             |
| 2.2  | Dependence      | of             | E              |             |           |              |             |          |                        |                |
|      |                 |                | (0)            | max         | on        | Re           | and γ       |          |                        | 18             |
| 2.3  | Dependence      | of             | E              |             |           |              |             |          |                        |                |
|      |                 |                | (0)            | max         | on        | γ for        | various     |          | Re                     | 19             |
| 2.4  | Neutral         | transient      | growth         |             | curve     |              |             |          |                        | 23             |
| 2.5  | Velocity        | field          | for            | the initial |           | condition    |             | which    | maximizes              | E              |
|      |                 |                |                |             |           |              |             |          |                        | (0), for       |
|      | L z = 1         | 2 π and        | Re             | = 400.      |           |              |             |          |                        | 25             |
| 2.6  | Time            | evolutions     | for            | amplitudes  |           |              | a 2 ( t )   | and      | a 3 ( t ) and E ( t    | ), for L z =   |
|      | 1 2 π and       | Re =           | 400.           |             |           |              |             |          |                        | 26             |
| 2.7  | Velocity        | field          | for            | the initial |           | condition    |             | which    | minimizes              | E              |
|      |                 |                |                |             |           |              |             |          |                        | (0), for       |
|      | L z = 1         | 2 π and        | Re             | = 400.      |           |              |             |          |                        | 26             |
| 2.8  | Velocity        | field for      | the            | initial     | condition |              | which       |          | gives E max , for      | L z = 1 2 π    |
|      | and Re          | = 400.         |                |             |           |              |             |          |                        | 27             |
| 2.9  | Dependence      | of             | initial        | rate        | of        | energy       | growth      |          | and maximum            | attainable     |
|      | energy          | on Re          | and            | θ , for     | L z       | = 1          | 2 π         |          |                        | 28             |
| 2.10 | Boundaries      | of             | qualitatively  |             |           | different    | E           | ( t ),   | for L z = 1 2 π        | 29             |
| 2.11 | Time            | evolution      | of             | energy      | for       | L            | z = 1       | 2 π      | , Re = 10, E (0)       | = 1 and        |
|      | various         | initial        | conditions.    |             |           |              |             |          |                        | 29             |
| 2.12 | Time evolutions |                | for            | amplitudes  |           | a            | 2 ( t ) and |          | a 3 ( t ) and E ( t ), | for L z = 2 π  |
|      | and Re          | = 400.         |                |             |           |              |             |          |                        | 31             |
| 2.13 | Dependence      | of             | initial        | rate        | of        | energy       | growth      |          | and maximum            | attainable     |
|      | energy          | on Re          | and            | θ , for     | L z       | = 2 π        |             |          |                        | 32             |
| 2.14 | Boundaries      | of             | qualitatively  |             |           | different    | E           | ( t ),   | for L z = 2 π          | 34             |
| 2.15 | Time evolution  |                | of energy      |             | for       | L z =        | 2 π , Re    |          | = 10, E (0) = 1        | and various    |
|      | initial         | conditions.    |                |             |           |              |             |          |                        | 34             |
| 3.1  | Boundaries      | for            | pseudospectra, |             |           | for          | L z =       | 1        | 2 π                    | 38             |
| 3.2  | Lower           | bound          | of E max       | using       |           | Kreiss’      | theorem,    |          | for L z = 1 2          | π 39           |
| 3.3  | Boundaries      | for            | pseudospectra, |             |           | for          | L z =       | 2        | π                      | 40             |
| 3.4  | Lower           | bound          | of E max       | using       |           | Kreiss’      | theorem,    |          | for L z = 2 π          | 40             |
| 3.5  | Comparison      | of             | E max          | to          | lower     | bound        | for         | variable | Re and                 | L z = 1 2 π 41 |

| 3.6  |           | Comparison    | of E max        | to          | lower         | bound       | for           | variable Re  | and        | L z        | = 2 π 41   |
|------|-----------|---------------|-----------------|-------------|---------------|-------------|---------------|--------------|------------|------------|------------|
| 4.1  |           | Dependence    | of   N 0        |             |               |             |               |              |            |            |            |
|      |           |               | 23              | (0)   and   | N 23          | max         | on Re         | and θ ,      | for L      | z =        | 1 2 π 48   |
| 4.2  | Time      | evolution     | of   N          | 23   ,      | for L z       | = 1 2       | π             |              |            |            | 48         |
| 4.3  |           | Dependence    | of   N 0        |             |               |             |               |              |            |            |            |
|      |           |               | 23              | (0)   and   | N 23          | max         | on Re         | and θ ,      | for L      | z =        | 2 π 49     |
| 4.4  | Time      | evolution     | of   N          | 23   ,      | for L z       | = 2 π       |               |              |            |            | 49         |
| 4.5  | Pictorial |               | representation  | of          | the           | effect of   | nonlinear     | terms        | on         | the        | modal      |
|      |           | amplitudes    |                 |             |               |             |               |              |            |            | 50         |
| 4.6  | Time      | evolutions    | for a           | 1 ( t ) ,   | a 2 ( t ) , a | 3 ( t ) ,   | a 9 ( t ) , E | ( t ) , N 23 | ( t ) for  |            | small per |
|      |           | turbations to | the             | laminar     | state         |             |               |              |            |            | 53         |
| 4.7  | Time      | evolutions    | for             | a 1 ( t )   | , a 2 ( t )   | , a 3 ( t ) | , a 9 ( t ) , | E ( t ) , N  | 23 ( t )   | for        | a large    |
|      |           | perturbation  | to the          | laminar     | state         |             |               |              |            |            | 55         |
| 4.8  | Velocity  |               | reconstructions |             | showing       | the         |               | advection of |            | streaks    | by the     |
|      |           | streamwise    | vortices        |             |               |             |               |              |            |            | 56         |
| 4.9  |           | Amplification | of E ( t        | ) for       | two-mode      |             | linear        | problem,     |            | four-mode  | and        |
|      |           | nine-mode     | models          |             |               |             |               |              |            |            | 58         |
| 4.10 |           | Boundary      | which shows     | the         |               | possibility | of            | turbulence   | for        | variable   | a 40       |
|      | and       | µ             |                 |             |               |             |               |              |            |            | 58         |
| 4.11 | Values    | of a 40       | for which       | the         | solution      |             | converges     | to the       | stable     |            | periodic   |
|      | orbit     | (sustained    |                 | turbulence) |               |             |               |              |            |            | 60         |
| 4.12 | Time      | evolution     | of              | the nine    | modes         | for         | two           | initial      | conditions |            | which      |
|      | either    | asymptotes    | on              | the         | stable        | periodic    | orbit         | or           | stable     | fixed      | point 61   |
| 4.13 | Time      | evolution     | of              | the         | nine          | modes       | for the       | initial      |            | conditions | from       |
|      | Figure    | 4.12,         | zoomed          | in          |               |             |               |              |            |            | 62         |

#### Acknowledgments

First and foremost I would like to extend my sincerest gratitude to Professor Jeff Moehlis, the best advisor and teacher I could have asked for. His patience, effort, enthusiasm, and knowledge of this research have inspired me to complete this thesis, and become a better researcher.

I would like to thank my committee members, Professor Homsy and Professor Bamieh, for their kindness, for taking time to read my thesis thoroughly and giving me great advise.

To my family and friends, mere words are not enough to thank them for their constant support and guidance. They have been there for me through thick and thin, my life would certainly not be the same without them.

Lastly, and most importantly, I would like to thank my parents, for loving and believing in me, and for sacrificing so much to give me, and my siblings, the opportunity to pursue our dreams of a better life.

### Chapter 1

## Introduction

Shear flows are fluid flows which are non-homogeneous with a mean shear. Turbulent shear flows are of great fundamental physical and mathematical interest because [4]: (i) Turbulence is found both experimentally and in numerical simulations for values of the Reynolds number well below the value at which the laminar state loses stability [7]. This is in contrast to other flows in which turbulence arises from laminar flow through a sequence of transitions to more and more complicated behavior as some parameter increases, such as for Rayleigh-B´enard convection. (ii) The governing partial differential equations possess numerous branches of (unstable) steady or traveling states consisting of wavy streamwise vortices and streaks that arise in saddle-node bifurcations [24, 6, 31, 9]. Such solutions have recently been detected experimentally [11, 4]. In [31] it was suggested that shear flow turbulence might be a "chaotic repellor," i.e., a repelling, transiently chaotic set in phase space, formed from heteroclinic connections among such finite amplitude solutions. Despite preliminary results exploring this suggestion (e.g. [22]), it has not been definitively proven to be relevant or not.

It has been suggested that transient energy growth provides a good basis for understanding these properties of shear flow turbulence (e.g. [35]). Such transient growth can significantly amplify small perturbations to the laminar state which can then trigger nonlinear effects that lead to turbulence.

An investigation of transient growth for a low-dimensional model for sinusoidal shear flow, recently introduced in [20], will be conducted in this thesis in order to better understand shear flow turbulence. The dependence of such transient energy growth on the initial conditions and parameters such as Reynolds number and aspect ratio (the length over which periodicity is imposed, normalized by d/2) will be analyzed. Furthermore, the importance of transient energy growth for triggering nonlinear effects which can lead to sustained turbulence will be explored.

The flow of interest and formulation of the model are introduced in the remainder of §1. In §2, $^{a}$ geometrical interpretation of transient growth is given. Then, the details of how such transient growth depends on initial conditions, Reynolds number, and aspect ratio are explored. Furthermore, the neutral transient growth curve, below which no initial condition gives transient energy growth, is investigated. In §3, the transient energy growth is interpreted using pseudospectra analysis, where $^{a}$ lower bound for the maximum attainable energy is obtained using Kreiss' Theorem. In §4, the importance of such transient growth for triggering nonlinear effects that might sustain turbulence is explored. Lastly, the conclusions are given in §5, with the appendices giving proofs of relevant mathematical results.

#### 1.1 Fundamental Fluid Dynamics Equations

In fluid dynamics, the Navier-Stokes equations are used to describe the flow of a fluid that is a continuum, that is, a fluid which satisfies the assumption that density and velocity fields may be defined at every point in space [26]. In the following, consider a Newtonian fluid for which shear stress is proportional to the velocity gradient [26]. These conservation equations are often written using the differential operator

$$\frac{D}{Dt}(\cdot) = \frac{\partial(\cdot)}{\partial t} + \mathbf{u} \cdot \nabla(\cdot), \quad (1.1)$$

which is defined as the time derivative as seen by an observer moving with the fluid and is often referred to as the material or substantial derivative. Conservation of mass states that

$$\frac{D\rho}{Dt} = -\rho \nabla \cdot \mathbf{u}, \quad (1.2)$$

where ρ is the density and u is the fluid velocity. The expression above is referred to as the continuity equation under the continuum assumption. Similarly, conservation of momentum states that

$$\frac{D\mathbf{u}}{Dt} = -\frac{1}{\rho}\nabla p + \nu\nabla^2\mathbf{u} + \mathbf{F}, \quad (1.3)$$

where p is the pressure, ν is the kinematic viscosity, and F is the body force acting on the fluid.

The present work considers sinusoidal shear flow, in which incompressible fluid between two free-slip walls experiences a time-independent streamwise sinusoidal body force which varies sinusoidally in the wall normal direction, and which gives rise to a sinusoidal laminar profile. The free-slip boundary conditions

| $u_y = 0,$ | $\frac{\partial u_x}{\partial y} = \frac{\partial u_z}{\partial y} = 0$ | (1.4) |
|------------|-------------------------------------------------------------------------|-------|
|------------|-------------------------------------------------------------------------|-------|

are imposed at $^{y}$ $^{=}$ ±1, and the flow is assumed periodic in the streamwise (x) and spanwise (z) directions, with lengths L$^{x}$ and Lz, respectively; see Figure 1.1. The characteristic velocity U$^{0}$ is taken to be the laminar velocity arising due to the forcing at a distance d/4 from the top wall [20]. Then, the lengths are nondimensionalized by d/2, velocities by U0, time by (d/2)/U0, and pressure by ρU$^{2}$ 0 . Keeping these non-dimensional considerations in mind, the continuity equation for incompressible flow simplifies to

$$\nabla \cdot \mathbf{u} = 0. \tag{1.5}$$

The corresponding non-dimensionalized conservation of momentum equation for this flow gives

$$\frac{\partial \mathbf{u}}{\partial t} = -(\mathbf{u} \cdot \nabla) \mathbf{u} - \nabla p + \frac{1}{Re} \nabla^2 \mathbf{u} + \mathbf{F}(y), \quad (1.6)$$

where the Reynolds number is defined as

| $Re = \frac{U_0 d}{2\nu}$ | (1.7) |
|---------------------------|-------|
|---------------------------|-------|

and the body force is

$$\mathbf{F}(y) = \frac{\sqrt{2}\pi^2}{4Re} \sin(\pi y/2) \hat{\mathbf{e}}_x. \quad (1.8)$$

![](_page_15_Diagram_0.jpeg)

Figure 1.1: Geometry for sinusoidal shear flow.

The steady laminar, rectilinear profile for sinusoidal shear flow,

$$\mathbf{U}(y) = \sqrt{2} \sin(\pi y/2) \hat{\mathbf{e}}_t \quad (1.9)$$

is linearly stable for all Re [7]. Note that this does not violate Rayleigh's theorem that a necessary condition for instability of a rectilinear, steady shear flow is that the shear profile has an inflection point; rather, it is a counter-example showing that this is not a sufficient condition [7]. Although difficult to obtain experimentally, sinusoidal shear flow represents a nontrivial shear flow which is amenable to analytical treatment; it is hoped that the knowledge gained from the study of sinusoidal shear flow is relevant to other shear flows such as plane Couette flow, boundary layer flow, plane Poiseuille flow, pipe flow, wakes, jets and mixing layers.

# 1.2 A Nine-Dimensional Model for Sinusoidal Shear Flow

There have been many attempts to gain insight into shear flow turbulence by studying reduced-order, low-dimensional ordinary differential equation models, which provide simplified dynamical descriptions for such complicated systems. As a result of their geometric simplicity, such models have typically been used to model plane Couette flow, in which fluid is sheared between two infinite parallel no-slip walls moving at the same speed but in opposite directions, and sinusoidal shear flow. See [2] for a review of models emphasizing transient growth arising from non-normality, [36, 37, 38, 8, 31, 20, 21] for models derived from Galerkin projection onto Fourier modes for sinusoidal shear flow, [22, 33] for models for plane Couette flow derived using the proper orthogonal decomposition, and [19, 18] for Swift-Hohenberg-like partial differential equation models. Proper orthogonal decomposition is a technique which captures dominant components, such as energy, of a complex system from data obtained from numerical simulations or experiments. Models derived using proper orthogonal decomposition have also been studied for turbulent boundary layers [1], channel flow [27], and transitional shear-layer flows [25]; see also the references in [29]. Several of these models show characteristics of the self-sustaining process elucidated in [37] and [38], in which streamwise vortices cause streak formation, then streaks break down to give streamwise-dependent flow, then streamwise vortices regenerate and the process repeats. It has been argued

that this self-sustaining process is a universal characteristic of shear flow turbulence [10, 38], cf. [28, 13, 17].

#### 1.2.1 Formulation of Modes

For sinusoidal shear flow, Fourier modes can be chosen to satisfy incompressibility and the free-slip boundary conditions. Such modes correspond naturally to streamwise vortices, streaks, and instability of streaks [20, 38]. A nine-dimensional model, introduced in [20] and obtained by projecting onto such Fourier modes will be considered for this thesis. For convenience, similar details from [20] are shown for the derivation of the model. The aspect ratios for this model are defined as α = 2π/Lx, β = π/2, and γ = 2π/Lz. This nine-dimensional model generalizes the eight-mode model of [38]. The main improvement for the nine-mode model is the inclusion of a mode which represents the lowest order modification of the mean profile (1.9); other modes from the eight-mode model are modified slightly so that they can couple to this new mode. Following [38], the modes for this model are normalized so that the following condition is satisfied

---

$$\iint_{\Omega} \mathbf{u}_n(x) \cdot \mathbf{u}_j(x) \, d^3\mathbf{x} = 2 \left( \frac{2\pi}{\alpha} \right) \left( \frac{2\pi}{\gamma} \right) \delta_{nj}. \quad (1.10)$$

The modes for this model are: the basic profile

$$\mathbf{u}_1 = \begin{pmatrix} \sqrt{2} \sin(\pi y/2) \\ 0 \\ 0 \end{pmatrix}, \quad (1.11)$$

representing a streamwise flow with the shape of the laminar profile,

$$\mathbf{u}_2 = \begin{pmatrix} \frac{4}{\sqrt{3}} \cos^2(\pi y/2) \cos(\gamma z) \\ 0 \\ 0 \end{pmatrix}, \quad (1.12)$$

which represents streaks, that is, spanwise variations in the streamwise velocity, and

$$\mathbf{u}_3 = \frac{2}{\sqrt{4\gamma^2 + \pi^2}} \begin{pmatrix} 0 \\ 2\gamma \cos(\pi y/2) \cos(\gamma z) \\ \pi \sin(\pi y/2) \sin(\gamma z) \end{pmatrix}, \quad (1.13)$$

which represents a pair of streamwise vortices. The spanwise flow is represented by the following two modes

$$\mathbf{u}_4 = \begin{pmatrix} 0 \\ 0 \\ \frac{4}{\sqrt{3}} \cos(\alpha x) \cos^2(\pi y/2) \end{pmatrix}, \quad (1.14)$$

$$\mathbf{u}_5 = \begin{pmatrix} 0 \\ 0 \\ 2 \sin(\alpha x) \sin(\pi y/2) \end{pmatrix}. \quad (1.15)$$

There are also two normal vortex modes;

$$\mathbf{u}_6 = \frac{4\sqrt{2}}{\sqrt{3(\alpha^2 + \gamma^2)}} \begin{pmatrix} -\gamma \cos(\alpha x) \cos^2(\pi y/2) \sin(\gamma z) \\ 0 \\ \alpha \sin(\alpha x) \cos^2(\pi y/2) \cos(\gamma z) \end{pmatrix}, \quad (1.16)$$

$$\mathbf{u}_7 = \frac{2\sqrt{2}}{\sqrt{\alpha^2 + \gamma^2}} \begin{pmatrix} \gamma \sin(\alpha x) \sin(\pi y/2) \sin(\gamma z) \\ 0 \\ \alpha \cos(\alpha x) \sin(\pi y/2) \cos(\gamma z) \end{pmatrix}, \quad (1.17)$$

and a fully-three dimensional mode

$$\mathbf{u}_8 = N_8 \begin{pmatrix} \pi \alpha \sin(\alpha x) \sin(\pi y/2) \sin(\gamma z) \\ 2(\alpha^2 + \gamma^2) \cos(\alpha x) \cos(\pi y/2) \sin(\gamma z) \\ -\pi \gamma \cos(\alpha x) \sin(\pi y/2) \cos(\gamma z) \end{pmatrix}, \quad (1.18)$$

where

$$N_8 = \frac{2\sqrt{2}}{\sqrt{(\alpha^2 + \gamma^2)(4\alpha^2 + 4\gamma^2 + \pi^2)}}.$$

The modification to the laminar mean flow profile is represented by

$$\mathbf{u}_9 = \begin{pmatrix} \sqrt{2} \sin(3\pi y/2) \\ 0 \\ 0 \end{pmatrix}. \quad (1.19)$$

#### 1.2.2 Galerkin Projection

The nine-mode model for sinusoidal shear flow is obtained by Galerkin projection of (1.6) onto important flow structures; namely the $^{u}$$^{1}$ − $^{u}$$^{9}$ modes given in (1.11-1.19). Galerkin projection is a technique in which the study of the dynamics of a system is replaced by the study of the dynamics of a subspace of that system. A useful Galerkin projection gives a good approximation of the full system

$$\frac{\partial \mathbf{u}}{\partial t} = \mathbf{F}(\mathbf{u}), \quad (1.20)$$

where F is an operator which can include differentiation, with a lower dimensional model. For the present problem, the velocity is expanded as

$$\mathbf{u}(\mathbf{x}, t) = \sum_{j=1}^9 a_j(t) \mathbf{u}_j(\mathbf{x}). \quad (1.21)$$

Substituting (1.21) into (1.20) and taking the inner product with u$^{j}$ (x) gives a set of nine coupled, nonlinear ordinary differential equations of the form

$$\dot{a}_n(t) = \left( \mathbf{F} \left( \sum_{j=1}^9 a_j(t) \mathbf{u}_j(\mathbf{x}) \right), \mathbf{u}_n(\mathbf{x}) \right), \quad (1.22)$$

where the amplitudes a$^{j}$ are real, and the modes u$^{j}$ are orthogonal under the standard inner product given by

---

$$(\mathbf{u}_n(x), \mathbf{u}_j(x)) = \iint_{\Omega} \mathbf{u}_n(x) \cdot \mathbf{u}_j(x) \, d^3\mathbf{x}. \quad (1.23)$$

Inserting the modes obtained in §1.2.1 into (1.22) gives

$$\frac{da_1}{dt} = \frac{\beta^2}{Re} - \frac{\beta^2}{Re}a_1 - \sqrt{\frac{3}{2}} \frac{\beta\gamma}{\kappa_{\alpha\beta\gamma}}a_6a_8 + \sqrt{\frac{3}{2}} \frac{\beta\gamma}{\kappa_{\beta\gamma}}a_2a_3, \quad (1.24)$$

$$\frac{da_2}{dt} = -\left(\frac{4\beta^2}{3} + \gamma^2\right) \frac{a_2}{Re} + \frac{5\sqrt{2}}{3\sqrt{3}} \frac{\gamma^2}{\kappa_{\alpha\gamma}} a_4 a_6 - \frac{\gamma^2}{\sqrt{6}\kappa_{\alpha\gamma}} a_5 a_7 - \frac{\alpha\beta\gamma}{\sqrt{6}\kappa_{\alpha\gamma}\kappa_{\alpha\beta\gamma}} a_5 a_8 - \sqrt{\frac{3}{2}} \frac{\beta\gamma}{\kappa_{\beta\gamma}} (a_1 a_3 + a_3 a_9), \quad (1.25)$$

$$\frac{da_3}{dt} = -\frac{\beta^2 + \gamma^2}{Re} a_3 + \frac{2}{\sqrt{6}} \frac{\alpha \beta \gamma}{\kappa_{\alpha\gamma} \kappa_{\beta\gamma}} (a_4 a_7 + a_5 a_6) + \frac{\beta^2 (3\alpha^2 + \gamma^2) - 3\gamma^2 (\alpha^2 + \gamma^2)}{\sqrt{6} \kappa_{\alpha\gamma} \kappa_{\beta\gamma} \kappa_{\alpha\beta\gamma}} a_4 a_8, \quad (1.26)$$

$$\frac{da_4}{dt} = -\frac{3\alpha^2 + 4\beta^2}{3Re}a_4 - \frac{\alpha}{\sqrt{6}}(a_1a_5 + a_5a_9) - \frac{10}{3\sqrt{6}}\frac{\alpha^2}{\kappa_{\alpha\gamma}}a_2a_6 - \sqrt{\frac{3}{2}} \frac{\alpha\beta\gamma}{\kappa_{\alpha\gamma}\kappa_{\beta\gamma}}a_3a_7 - \sqrt{\frac{3}{2}} \frac{\alpha^2\beta^2}{\kappa_{\alpha\gamma}\kappa_{\beta\gamma}\kappa_{\alpha\beta\gamma}}a_3a_8, \quad (1.27)$$

$$\frac{da_5}{dt} = -\frac{\alpha^2 + \beta^2}{Re} a_5 + \frac{\alpha}{\sqrt{6}}(a_1 a_4 + a_4 a_9) + \frac{\alpha^2}{\sqrt{6} \kappa_{\alpha\gamma}} a_2 a_7 - \frac{\alpha \beta \gamma}{\sqrt{6} \kappa_{\alpha\gamma} \kappa_{\alpha\beta\gamma}} a_2 a_8 + \frac{2}{\sqrt{6}} \frac{\alpha \beta \gamma}{\kappa_{\alpha\gamma} \kappa_{\beta\gamma}} a_3 a_6, \quad (1.28)$$

$$\begin{aligned} \frac{da_6}{dt} = & -\frac{3\alpha^2 + 4\beta^2 + 3\gamma^2}{3Re} a_6 + \frac{\alpha}{\sqrt{6}}(a_1a_7 + a_7a_9) + \frac{10}{3\sqrt{6}} \frac{\alpha^2 - \gamma^2}{\kappa_{\alpha\gamma}} a_2a_4 \\ & - 2\sqrt{\frac{2}{3}} \frac{\alpha\beta\gamma}{\kappa_{\alpha\gamma}\kappa_{\beta\gamma}} a_3a_5 + \sqrt{\frac{2}{3}} \frac{\beta\gamma}{\kappa_{\alpha\beta\gamma}} (a_1a_8 + a_8a_9), \end{aligned} \quad (1.29)$$

$$\frac{da_7}{dt} = -\frac{\alpha^2 + \beta^2 + \gamma^2}{Re} a_7 - \frac{\alpha}{\sqrt{6}}(a_1 a_6 + a_6 a_9) + \frac{1}{\sqrt{6}} \frac{\gamma^2 - \alpha^2}{\kappa_{\alpha\gamma}} a_2 a_5 + \frac{1}{\sqrt{6}} \frac{\alpha \beta \gamma}{\kappa_{\alpha\gamma} \kappa_{\beta\gamma}} a_3 a_4, \quad (1.30)$$

$$\begin{aligned} \frac{da_8}{dt} = & -\frac{\alpha^2 + \beta^2 + \gamma^2}{Re} a_8 + \frac{\gamma^2(3\alpha^2 - \beta^2 + 3\gamma^2)}{\sqrt{6}\kappa_{\alpha\gamma}\kappa_{\beta\gamma}\kappa_{\alpha\beta\gamma}} a_3 a_4 \\ & + \frac{2}{\sqrt{6}} \frac{\alpha\beta\gamma}{\kappa_{\alpha\gamma}\kappa_{\alpha\beta\gamma}} a_2 a_5, \end{aligned} \quad (1.31)$$

$$\frac{da_9}{dt} = -\frac{9\beta^2}{Re}a_9 - \sqrt{\frac{3}{2}} \frac{\beta\gamma}{\kappa_{\alpha\beta\gamma}}a_6a_8 + \sqrt{\frac{3}{2}} \frac{\beta\gamma}{\kappa_{\beta\gamma}}a_2a_3, \quad (1.32)$$

where

| $\kappa_{\alpha\gamma} = \sqrt{\alpha^2 + \gamma^2},$ | $\kappa_{\beta\gamma} = \sqrt{\beta^2 + \gamma^2},$ | $\kappa_{\alpha\beta\gamma} = \sqrt{\alpha^2 + \beta^2 + \gamma^2}.$ | (1.33) |
|-------------------------------------------------------|-----------------------------------------------------|----------------------------------------------------------------------|--------|
|-------------------------------------------------------|-----------------------------------------------------|----------------------------------------------------------------------|--------|

The transition to turbulence for this nine-mode model is subcritical, i.e., it is possible to get stable turbulence at values of Re for which the laminar state is stable. The distributions of turbulent lifetimes, i.e., the duration of turbulence before decaying to the laminar state, are exponential, in agreement with observations in many shear flows [20]. The laminar state for this model corresponds to a fixed point at a$^{1}$ = 1, a$^{2}$ = ... = a$^{9}$ = 0.

### Chapter 2

## Transient Growth for the

# Streak-Streamwise Vortex

## Interaction

The matrix $^{M}$ arising from the linearization of the nine-mode model from §1.2 about the laminar state is non-normal, i.e., MM$^{T}$ 6$^{=}$ $^{M}$$^{T}$M. This suggests that even though its eigenvalues are all strictly negative for all Re, corresponding to linear stability of the laminar state, it might be possible to have transient growth of energy which could trigger nonlinear effects that sustain turbulence [35]. In this chapter, a detailed analysis is conducted for the transient growth which occurs for the $^{2}$ × $^{2}$ block of $^{M}$ that corresponds to the linear evolution of the amplitudes $^{a}$$^{2}$ and a3. Much effort is devoted to this interaction because it gives the strongest transient energy growth compared to the other interactions of the linearized ninedimensional model. Also, streaks and streamwise vortices are dominant structures in numerical simulations and are found as unstable steady solutions of the Navier-Stokes equations [6, 22, 24, 31]. Furthermore, they are the most energetically excited structures of the linearized Navier-Stokes equations with forced input and can be explained as input-output resonances of frequency responses [16].

The dynamics associated with this block are given by the linear system

$$\begin{pmatrix} \dot{a}_2 \\ \dot{a}_3 \end{pmatrix} = \underbrace{\begin{pmatrix} b & c \\ 0 & d \end{pmatrix}}_{M_{23}} \begin{pmatrix} a_2 \\ a_3 \end{pmatrix}, \quad (2.1)$$

$$b = -\frac{\frac{4\beta^2}{3} + \gamma^2}{Re}, \quad c = -\frac{\sqrt{3/2} \beta \gamma}{\sqrt{\beta^2 + \gamma^2}}, \quad d = -\frac{\beta^2 + \gamma^2}{Re}.$$

The laminar state corresponds to a$^{2}$ = a$^{3}$ = 0; the stability of the laminar state with respect to streak and streamwise vortex perturbations follows from the fact that the eigenvalues b and d of M$^{23}$ must be negative. The exact solution to (2.1) is readily shown to be

| $a_2(t) = a_{20}e^{bt} + \frac{c}{d-b}a_{30}(e^{dt} - e^{bt}),$ | (2.2) |
|-----------------------------------------------------------------|-------|
|-----------------------------------------------------------------|-------|

| $a_3(t)$ | $= a_{30}e^{dt}$ | (2.3) |
|----------|------------------|-------|
|----------|------------------|-------|

For this linear system, the energy is defined to be

$$E(t) = (a_2(t))^2 + (a_3(t))^2. \quad (2.4)$$

# 2.1 Geometric Interpretation of Transient Energy Growth

The solution (2.2,2.3) can be rewritten in a form which allows an instructive geometric interpretation of transient energy growth, namely

$$\mathbf{a}(t) = (a_2(t), a_3(t)) = \underbrace{\mathbf{v}_1 b_{10} e^{bt}}_{\mathbf{s}_1(t)} + \underbrace{\mathbf{v}_2 b_{20} e^{dt}}_{\mathbf{s}_2(t)}, \quad (2.5)$$

where formulas for b$^{10}$ and b$^{20}$ in terms of a$^{20}$ and a$^{30}$ are readily obtained, and

$$\mathbf{v}_1 = \begin{pmatrix} 1 \\ 0 \end{pmatrix}, \quad \mathbf{v}_2 = \frac{|d-b|}{\sqrt{c^2 + (d-b)^2}} \begin{pmatrix} \frac{c}{d-b} \\ 1 \end{pmatrix} \quad (2.6)$$

are the normalized eigenvectors for M23. Since M$^{23}$ is non-normal, v$^{1}$ and v$^{2}$ are non-orthogonal; for example, for typical values L$^{x}$ = 1.75π, L$^{z}$ = 1.2π and Re = 400, they are almost anti-parallel. For the related system of plane Couette flow, these parameters correspond to the minimal flow unit, the smallest domain which is found numerically to sustain turbulence [10]. A small-amplitude initial condition is thus the superposition of two very large-amplitude components; i.e., |$^{s}$1(0)| and |$^{s}$2(0)| are large, as sketched in the left panels of Figure 2.1. For the linear system, b < d < 0, so the length of s1(t) decays more quickly than the length of s2(t). This leads to an $^{a}$(t) with larger length (and hence larger energy) than $^{a}$(0), as sketched in the right panel of Figure 2.1(a); thus, transient growth has occurred. For longer times, the length of s2(t) also decreases substantially, and the system asymptotically approaches the laminar state with a$^{2}$ = a$^{3}$ = 0.

![](_page_25_Diagram_0.jpeg)

![](_page_25_Picture_1.jpeg)

Figure 2.1: Geometrical interpretation of transient growth. The circles represent constant energy equal to the initial energy. Because $^{v}$$^{1}$ and $^{v}$$^{2}$ are nearly anti-parallel, the initial condition is $^{a}$$^{0}$ $^{=}$ $^{s}$1(0) $^{+}$ $^{s}$2(0) with large |$^{s}$1(0)| and |$^{s}$2(0)|, as shown in the left panels of (a) and (b). Because of different decay rates, in the right panels |$^{s}$1(t)| $^{&}$lt; |$^{s}$2(t)| ≈ |$^{s}$2(0)|. In (a), |a(t)| $^{&}$gt; |$^{a}$0| for short times, so that transient growth occurs. In (b), |a(t)| $^{&}$lt; |$^{a}$0|, so that transient growth does not occur, at least for short times. For clarity, the difference in decay rates is assumed to be large for this figure.

For other initial conditions, transient energy growth might not occur: see Figure 2.1(b). Clearly, the energy initially decreases with time. Depending on the rate of decay of the length of s2(t), the energy might always remain below its initial value, or might eventually grow above its initial value. Such considerations motivate the following exploration of how transient energy growth depends on initial conditions.

#### 2.2 Optimal Transient Energy Growth

A general linear equation $^{a}$˙ = A$^{a}$ has the exact solution

$$a(t) = e^{tA}a_0, \quad (2.7)$$

where $^{a}$$^{0}$ = $^{a}$(0). The energy of a solution is given by

---

$$E(t) = |\mathbf{a}(t)|^2 = \sum a_i^2, \quad (2.8)$$

where the sum is over the components of $^{a}$. It is found that

$$E'(0) = \frac{d}{dt} \bigg|_{t=0} |e^{tA} \mathbf{a}_0|^2 = 2\mathbf{a}_0 \cdot A\mathbf{a}_0 \equiv f(\mathbf{a}_0). \quad (2.9)$$

¯ To find the (normalized) initial condition which gives the maximum initial energy growth, f($^{a}$0) is maximized subject to the constraint

$$g(\mathbf{a}_0) \equiv |\mathbf{a}_0|^2 = 1. \tag{2.10}$$

Using Lagrange multipliers to impose this constraint, this leads to the linear set of equations

$$\frac{\partial f}{\partial a_{i0}} = \lambda \frac{\partial g}{\partial a_{i0}}, \quad (2.11)$$

where ai$^{0}$ is the i th component of $^{a}$0. Explicit computation shows that this is equivalent to the equation

$$(A + A^T)a_0 = \lambda a_0. \quad (2.12)$$

Thus the eigenvalues and eigenvectors of A+A$^{T}$ need to be found. It is also readily shown that

$$a_0 \cdot Aa_0 = a_0 \cdot A^T a_0, \quad (2.13)$$

which gives

$$E'(0) = \mathbf{a}_0 \cdot (A + A^T) \mathbf{a}_0 = \lambda |\mathbf{a}_0|^2. \quad (2.14)$$

Therefore, the largest (resp., smallest) value that E 0 (0) can obtain, when E(0) = |a0| $^{2}$ = 1, is equal to the largest (resp., smallest) eigenvalue of the matrix A + A$^{T}$ . The initial condition that maximizes (resp., minimizes) the initial energy growth is the corresponding eigenvector of this matrix (cf. [2]).

#### 2.3 Application to Model

#### 2.3.1 General Results

For the present problem, take A = M23. The maximum value that E 0 (0) can take is the larger eigenvalue of M$^{23}$ + M$^{T}$ 23:

$$[E'(0)]_{max} = b + d + \sqrt{b^2 + c^2 - 2bd + d^2} \quad (2.15)$$

$$= \frac{1}{6Re} \left( -14\beta^2 - 12\gamma^2 + \sqrt{\frac{4\beta^6 + 4\beta^4\gamma^2 + 54\beta^2\gamma^2Re^2}{\beta^2 + \gamma^2}} \right). \quad (2.16)$$

The corresponding (unnormalized) eigenvector is

$$(a_{20}, a_{30}) = \left( \frac{d - b - \sqrt{b^2 + c^2 - 2bd + d^2}}{c}, -1 \right) \quad (2.17)$$

$$= \left( \frac{\sqrt{4\beta^6 + 4\beta^4\gamma^2 + 54\beta^2\gamma^2 Re^2} - 2\beta^2\sqrt{\beta^2 + \gamma^2}}{3\sqrt{6}\beta\gamma Re}, -1 \right). \quad (2.18)$$

A surface plot showing how [E 0 (0)]max depends on Re and γ is displayed in Figure 2.2. Taking a cut at a small fixed Re, Figure 2.3(a) shows that [E 0 (0)]max reaches a local maximum for a particular γ value; for Re = 10, this corresponds to L$^{z}$ = 1.0396π. For large Re it is found that

$$[E'(0)]_{max} \approx |c| = \frac{\sqrt{3/2}\beta\gamma}{\sqrt{\beta^2 + \gamma^2}}. \quad (2.19)$$

This is a monotonically increasing function in γ, and for large values it asymptotically approaches p 3/2β = 1.9238; see Figure 2.3(b). Since γ = 2π/Lz, for large

![](_page_28_Figure_0.jpeg)

Figure 2.2: Dependence of [E$^{0}$ (0)]max on Reynolds number Re and spanwise wavenumber γ. See Figure 2.3 for two cuts at constant Re.

Re the maximum initial energy growth is larger for smaller spanwise aspect ratios. The corresponding (normalized) eigenvector which maximizes E 0 (0) in the limit of large Re is readily shown to be

| $(a_{20}, a_{30}) = (1/\sqrt{2}, -1/\sqrt{2}).$ | (2.20) |
|-------------------------------------------------|--------|
|-------------------------------------------------|--------|

This corresponds to the initial energy being equally distributed between the streaks and the streamwise vortices; as will be shown below, the phases between these modes are such that the advection of fluid by the streamwise vortices reinforces the streaks.

The minimum value that E 0 (0) can take is given by the remaining eigenvalue of M$^{23}$ + M$^{T}$ 23:

$$[E'(0)]_{min} = b + d - \sqrt{b^2 + c^2 - 2bd + d^2} \quad (2.21)$$

$$= -\frac{1}{6Re} \left( 14\beta^2 + 12\gamma^2 + \sqrt{\frac{4\beta^6 + 4\beta^4\gamma^2 + 54\beta^2\gamma^2Re^2}{\beta^2 + \gamma^2}} \right). \quad (2.22)$$

![](_page_29_Figure_0.jpeg)

Figure 2.3: Dependence of [E$^{0}$ (0)]max on spanwise wavenumber γ for (a) Re = 10 and (b) Re = $^{1}$ $^{×}$ $^{10}$$^{10}$ where the dotted lined corresponds to p 3/2β = 1.9238.

The corresponding (unnormalized) eigenvector is

$$(a_{20}, a_{30}) = \left( \frac{d - b + \sqrt{b^2 + c^2 - 2bd + d^2}}{c}, -1 \right) \quad (2.23)$$

$$= \left( \frac{-\sqrt{4\beta^6 + 4\beta^4\gamma^2 + 54\beta^2\gamma^2Re^2} - 2\beta^2\sqrt{\beta^2 + \gamma^2}}{3\sqrt{6}\beta\gamma Re}, -1 \right). \quad (2.24)$$

For large Re,

$$[E'(0)]_{min} \approx -|c| = -\frac{\sqrt{3/2}\beta\gamma}{\sqrt{\beta^2 + \gamma^2}} \quad (2.25)$$

with corresponding (normalized) eigenvector

| $(a_{20}, a_{30}) \approx (-1/\sqrt{2}, -1/\sqrt{2}).$ | (2.26) |
|--------------------------------------------------------|--------|
|--------------------------------------------------------|--------|

This also corresponds to the initial energy being equally distributed between the streaks and the streamwise vortices, but as will be shown below, the streaks are shifted by half of a spanwise wavelength with respect to the initial condition which maximizes the initial energy growth. The streamwise vortices advect the fluid so as to weaken the streaks.

The initial rate of energy growth E 0 (0) clearly depends on the initial distribution of energy between the streamwise vortices and the streaks. Let E(0) = a 2 $^{20}$+a 2 $^{30}$ = 1, and θ = tan−$^{1}$ (a30/a20). Thus, for example, θ = 0 corresponds to the initial energy being entirely in the streaks. Differentiating E = a 2 $^{2}$ + a 2 3 and using (2.1) gives

| $E'(0) = 2ba_{20}^2 + 2ca_{20}a_{30} + 2da_{30}^2$                                          |
|---------------------------------------------------------------------------------------------|
|                                                                                             |
|                                                                                             |
| $= 2b \cos^2 \theta + c \sin 2\theta + 2d \sin^2 \theta$                                    |
|                                                                                             |
|                                                                                             |
| $= b + d + (b - d) \cos 2\theta + c \sin 2\theta.$ (2.2) |

This is periodic with period π because rotation of θ by π corresponds to multiplication of $^{a}$$^{20}$ and $^{a}$$^{30}$ by −1, which has only $^{a}$ trivial effect for $^{a}$ linear problem. As expected from the discussion above, for systems with large Re (for which $^{b}$ → $^{0}$ and $^{d}$ → 0),

$$E'(0) \approx c \sin 2\theta.$$
 (2.28)

E 0 (0) reaches its maximum value of |c| for $^{\theta}$ ≈ $^{3}$π/$^{4}$ and $^{\theta}$ ≈ $^{7}$π/4, and its minimum value of −|c| for $^{\theta}$ ≈ π/$^{4}$ and $^{\theta}$ ≈ $^{5}$π/$^{4}$ (recall that $^{c}$ $^{&}$lt; 0). These results demonstrate how different initial distributions of energy affect the transient dynamics of the system, something which is not captured by standard eigenvalue analysis, which only gives asymptotic behavior.

Progress can also be made in understanding how the maximum value that E(t) reaches under the linear evolution depends on the initial distribution of energy between streamwise vortices and streaks, as captured by θ. In the limit of large Re, $^{b}$ → $^{0}$ and $^{d}$ → 0, so, for $^{E}$(0) $^{=}$ $^{a}$ 2 $^{20}$ + a 2 $^{30}$ = 1,

---

$$E(t) = [a_2(t)]^2 + [a_3(t)]^2 \approx \left(\frac{c}{d-b}\right)^2 (e^{dt} - e^{bt})^2 \sin^2 \theta. \quad (2.29)$$

(2.2) has a small magnitude relative to the second term. By solving E 0 (t) = 0 for t using (2.29), E(t) reaches its maximum at

$$t_{maxE} \approx \frac{\log(d/b)}{b-d} = \frac{3Re}{\beta^2} \log\left(\frac{4\beta^2/3 + \gamma^2}{\beta^2 + \gamma^2}\right), \quad (2.30)$$

with

$$\begin{aligned} E_{max} &\approx E(t_{max}E) \\ &\approx \left( \frac{c}{d-b} \right)^2 (b^{b/(d-b)} d^{b/(b-d)} - b^{d/(d-b)} d^{d(b-d)})^2 \sin^2 \theta \\ &= \frac{3}{2} \beta^2 \gamma^2 R e^2 \sin^2 \theta \frac{(\beta^2 + \gamma^2)^{5+6\gamma^2/\beta^2}}{(4\beta^2/3 + \gamma^2)^{8+6\gamma^2/\beta^2}}. \end{aligned} \quad (2.31)$$

The absolute maximum energy that can occur for the linear dynamics of the modes for streaks and streamwise vortices, for large fixed Re, thus occurs for $^{\theta}$ ≈ π/$^{2}$ and $^{\theta}$ ≈ $^{3}$π/2. This corresponds to the initial energy being entirely in the streamwise vortices. Note that the initial conditions which maximize E 0 (0) give sin$^{2}$ θ = 1/2, so that for large Re the absolute maximum energy is double the maximum energy obtained for the initial condition which maximizes initial energy growth. Furthermore, note that when θ is sufficiently close to 0 or π, the approximations (2.29) and (2.31) are not valid, and Emax = E(0). For example, θ = 0 implies that a$^{30}$ = 0, and that E(t) = a 2 $^{20}$e $^{2}$bt is monotonically decreasing.

#### 2.3.2 Neutral Transient Growth

As just shown, initial conditions have a dramatic effect on transient energy growth due to linear effects. A neutral transient growth curve, below which no initial condition gives transient energy growth, can be found by solving [E 0 (0)]max for Re using (2.16). The result yields the curve

$$Re^*(\gamma) = \frac{2\sqrt{2(\beta^2 + \gamma^2)^2(4\beta^2 + 3\gamma^2)}}{3\beta\gamma}; \quad (2.32)$$

see Figure 2.4. For a given aspect ratio γ, for Re > Re ∗ (γ) it is possible to find an initial condition with initial transient energy growth, while for Re < Re ∗ (γ) there are no such initial conditions. It was found that Re ∗ (γ) reaches a minimum at γ ∗ = 1.1634 with Re ∗ (γ ∗ ) = 7.3573. For Re < Re ∗ (γ ∗ ), there are no possible initial conditions for which E 0 (0) > 0. For Re > Re ∗ (γ ∗ ), there will be a band of θ values for which E 0 (0) > 0.

There is a larger band of initial θ values for which E(t) > E(0) for some t > 0, that is, for which the energy eventually exceeds its initial value. This includes the band of θ values for which E 0 (0) > 0; however, it is also possible to choose θ so that E 0 (0) is negative but after some initial decay the energy grows above E(0) before finally decaying to zero. To find this boundary, let t$^{1}$ > 0 be the time at which E(t1) = 1. At this time, the trajectory lies on the unit circle in the (a2, a3) phase space; for definiteness, let its location be (a21, $^{a}$31) ≡ (a2(t1), $^{a}$3(t1)), with angle θ$^{1}$ = tan−$^{1}$ (a31/a21). Furthermore, E 0 (t1) = 0. Thus (similar to (2.27)),

---

$$E'(t_1) = b + d + (b - d) \cos 2\theta_1 + c \sin 2\theta_1 = 0, \quad (2.33)$$

---

which can be solved for θ1. Now, from (2.3), a$^{31}$ = a30e dt$^{1}$ , that is,

$$\sin \theta_1 = \sin \theta e^{dt_1}$$
. (2.34)

This can be rearranged to give

$$t_1 = \frac{1}{d} \log \left( \frac{\sin \theta_1}{\sin \theta} \right). \quad (2.35)$$

![](_page_33_Figure_0.jpeg)

Figure 2.4: Neutral transient growth curve Re (γ). Above this curve, E$^{0}$ (0) > 0 for some initial distribution of energy as captured by θ. Below this curve, there are no such θ values. As discussed in the text, above this curve it is possible to find an initial condition for which E(t) > E(0) for some t > 0, while below this curve there is no such initial condition.

Finally, from (2.2),

| $a_{21} = a_{20}e^{bt_1} + \frac{c}{d-b}a_{30}(e^{dt_1} - e^{bt_1}), \quad (2.36)$ |
|------------------------------------------------------------------------------------|
|------------------------------------------------------------------------------------|

that is,

---

$$\cos \theta_1 = \cos \theta e^{bt_1} + \frac{c}{d-b} \sin \theta (e^{dt_1} - e^{bt_1}). \quad (2.37)$$

Plugging in (2.35) and for a given γ and Re, this is an equation which can be solved (numerically) for θ. These solutions lie on the boundary of the band of θ values for which E(t) > E(0) for some t > 0.

Interestingly, the curve for Re ∗ (γ) given by (2.32) coincides with the curve above which it is possible to find an initial condition for which E(t) > E(0) for some t > 0, and below which there is no such initial condition. Without loss of generality, take E(0) = 1. Certainly this new curve cannot lie above the curve for Re ∗ (γ), because E 0 (0) > 0 for some θ guarantees that E(t) > E(0) for some t > 0 for that initial condition. Instead, suppose that one chooses Re < Re ∗ (γ ∗ ), so that for all θ values E 0 (0) < 0. If there is a t$^{1}$ such that E(t1) = E(0) = 1 and E 0 (t1) > 0, then E(t) > E(0) for some t > t$^{1}$ > 0. Now, at time t$^{1}$ the solution has unit energy, and corresponds to some value for θ. If the initial θ value was taken to be this, then it would result in E 0 (0) > 0. This contradicts the assumption that E 0 (0) < 0 for all θ values. Therefore, the new curve cannot lie below the curve for Re ∗ (γ), so they must coincide.

For a very large aspect ratio system, the curve Re ∗ (γ) is defined to be the neutral transient growth curve, much in the spirit of neutral stability curves for standard hydrodynamic stability analysis: for fixed aspect ratio, it defines the value of Re at which transient growth is possible, while for fixed Re it defines the range of wavenumbers γ for which transient growth is possible. These results are viewed as a powerful generalization of standard hydrodynamic stability analysis to systems which lack a linear instability. The standard analysis is limited to calculating eigenvalues, and hence only captures asymptotic behavior. Furthermore, the standard analysis would not identify key differences in the situation, for example, in which there is an equal initial distribution of energy between streaks and rolls, or when the energy is all initially in the streamwise vortices. The analysis in this section overcomes these limitations by usefully capturing the transient behavior and the importance of different initial distributions of energy.

#### 2.3.3 Results for L$^{z}$ = 1.2π

As a representative example, consider the aspect ratio L$^{z}$ = 1.2π. (The results are independent of $^{L}$$^{x}$ ∼ $^{1}$/α because the streak and streamwise vortex modes have

![](_page_35_Figure_0.jpeg)

Figure 2.5: Velocity fields for (top) the initial condition which maximizes E$^{0}$ (0), and (bottom) the state for this initial condition when E is maximized, both for L$^{z}$ = 1.2π and Re = 400. The velocity fields are represented by vectors for the components shown in the plane and by grayscale for the velocity perpendicular to the plane. The vectors are identically scaled, so the shorter arrows in the bottom plot indicate weaker vortices. The laminar profile has been included in these plots.

no streamwise variation.) For these parameters, $^{b}$ $^{=}$ −6.0677/Re, $^{c}$ $^{=}$ −1.4000, and $^{d}$ $^{=}$ −5.2452/Re.

For Re = 400, it was found that the unit energy initial condition (a2(0), a3(0)) = (0.7066, −0.7076) (cf. (2.20)), with velocity reconstruction shown in the top panel of Figure 2.5, gives [E 0 (0)]max = 1.3717; the large Re prediction from (2.19) is 1.4000. Figure 2.6 shows a2(t), a3(t), and E(t) for this initial condition due to the linear evolution; the maximum value E = 678.07 occurs at tmax = 70.12, with (a2(tmax), $^{a}$3(tmax)) $^{=}$ (26.0382, −0.2821) and velocity reconstruction shown in the bottom panel of Figure 2.5. The large Re predictions from (2.30) and (2.31) (with

![](_page_36_Figure_0.jpeg)

Figure 2.6: Solution for (2.1) with L$^{z}$ = 1.2π, and Re = 400 for the initial condition which gives the maximum initial energy growth E$^{0}$ max(0) (solid lines) and the initial condition which gives the absolute maximum energy Emax which can occur (dashed lines).

![](_page_36_Figure_2.jpeg)

Figure 2.7: Velocity field for the initial condition which minimizes E$^{0}$ (0) for L$^{z}$ = 1.2π and Re = 400. Conventions are as in Figure 2.5.

![](_page_37_Figure_0.jpeg)

Figure 2.8: Velocity fields for (top) the initial condition which gives Emax, the absolute maximum of E, and (bottom) the state for this initial condition when this Emax is obtained, both for L$^{z}$ = 1.2π and Re = 400. Conventions are as in Figure 2.5.

Re = 400 and θ = 3π/4) are tmaxE = 70.84 and Emax = 664.44. Since the energy in the streamwise vortices decays monotonically, the bulk of the energy when it reaches its peak is in the streaks.

The minimal initial energy growth [E 0 (0)]min is obtained for the unit energy initial condition (a2(0), $^{a}$3(0)) $^{=}$ (−0.7076, −0.7066) (cf. (2.24)), with velocity reconstruction shown in Figure 2.7. Comparing this with the top panel of Figure 2.5, the streaks are shifted by roughly half of a spanwise wavelength with respect to the initial condition which maximizes the initial energy growth. Here the streamwise vortices advect the fluid in such a way as to weaken the streaks.

Still keeping L$^{z}$ = 1.2π and Re = 400, the absolute maximum energy which

![](_page_38_Figure_0.jpeg)

Figure 2.9: Results for L$^{z}$ = 1.2π, showing (a) E$^{0}$ (0) vs θ for Re = 10 (solid), Re = 400 (dashed), and the large Re limit given by (2.28) (dot-dashed, nearly coincident with dashed line), with dotted lines at θ = π/4, 3π/4, 5π/4, and 7π/4; (b) Emax vs. θ for Re = 400 (solid) and for the large Re limit given by (2.31) (dashed, nearly coincident with solid line); and (c) Emax vs. θ for Re = 1000 (solid) and for the large Re limit given by (2.31) (dashed, indistinguishable from solid line). In (b) and (c), the dotted lines are at θ = π/2, π, and 3π/2.

can occur for the linear dynamics with unit energy initial condition, is Emax = $^{1329}$.03. This occurs for (a2(0), $^{a}$3(0)) ≈ (0, −1) at time $^{t}$maxE $^{=}$ $^{70}$.83, with (a2(tmaxE), $^{a}$3(tmaxE)) $^{=}$ (36.4537, −0.3950); see Figure 2.6 for the solutions, and Figure 2.8 for velocity reconstructions. This compares favorably with the large Re predictions from (2.30) and (2.31) (with Re = 400 and θ = 3π/2) of tmaxE = 70.84 and Emax = 1328.87. Here again, the bulk of the energy when it reaches its peak is in the streaks.

Figure 2.9(a) plots (2.27) for this aspect ratio, showing how the initial rate of energy growth depends on Re and on the initial distribution of energy between

![](_page_39_Figure_0.jpeg)

Figure 2.10: Boundaries of qualitatively different E(t) for L$^{z}$ = 1.2π. The θ values inside the solid curve correspond to initial conditions for which E$^{0}$ (0) > 0. The θ values to the right of the dashed curve and to the left of the right branch of the solid curve correspond to initial conditions for which E(t) > E(0) for some t > 0. The dot-dashed line shows the initial condition giving [E$^{0}$ (0)]max. These results are for L$^{z}$ = 1.2π.

![](_page_39_Figure_2.jpeg)

Figure 2.11: Time evolution of energy for L$^{z}$ = 1.2π, Re = 10 and E(0) = 1 for (a) θ = 2.64302 (solid) corresponding to right solid boundary of Figure 2.10, θ = 2.01069 (dashed) corresponding to left solid boundary of Figure 2.10, and θ = 1.54592 (dot-dashed) corresponding to dashed boundary of Figure 2.10. (b) Energy time series for θ = 2.8 (solid), θ = 2.3 (dotted), θ = 1.7 (dashed), and θ = 1.4 (dot-dashed).

streamwise vortices and streaks, as captured by θ. Figure 2.9(b) shows the analogous plot for the maximum attainable energy, found by numerically maximizing E(t) using the exact results (2.2-2.3). In the limit of large Re, it was confirmed that (2.28) and (2.31) are good approximations. Clearly, it is possible to get substantial transient energy growth for this system before it decays to the laminar state (E = 0).

Next, consider boundaries of qualitatively different E(t). The boundary for which E 0 (0) > 0 is obtained by solving E(0) = 0 for θ from (2.27), see the solid line in Figure 2.10. A plot of E(t) for the two θ values on the boundary of this band for these parameters are shown in Figure 2.11(a) as solid and dashed lines. The boundary showing [E 0 (0)]max is found by studying the time series for the energy for an initial condition (θ = 1.54592) on the boundary; see the dot-dashed line in Figure 2.10. The last boundary, in dashed lines of Figure 2.10, corresponds to the band of θ values for which E(t) > E(0) for some t > 0 and is found by solving (2.37) for θ. Figure 2.11(b) shows the time series E(t) with initial conditions in the different regions of Figure 2.10 for Re = 10.

#### 2.3.4 Results for L$^{z}$ = 2π

As a second example, the aspect ratio L$^{z}$ = 2π will now be considered. For this and L$^{x}$ = 4π in the related system of plane Couette flow, this corresponds to the domain size where the steady finite amplitude solutions appear at the smallest value of Re [6, 39]. For these parameters, $^{b}$ $^{=}$ −4.2899/Re, $^{c}$ $^{=}$ −1.0332, and

![](_page_41_Figure_0.jpeg)

Figure 2.12: Solution for (2.1) with L$^{z}$ = 2π, and Re = 400 for the initial condition which gives the maximum initial energy growth E$^{0}$ max(0) (solid lines) and the initial condition which gives the absolute maximum energy Emax which can occur (dashed lines).

$^{d}$ $^{=}$ −3.4674/Re.

For Re = 400, Figure 2.12 shows a2(t), a3(t), and E(t) for the unit energy initial condition (a2(0), $^{a}$3(0)) $^{=}$ (0.7064, −0.7078) (cf. (2.20)) corresponding to maximum initial energy growth. From these values, an [E 0 (0)]max of 1.0137 was obtained and compares favorably well with the large Re prediction from (2.19) of 1.0332. Furthermore, the maximum energy was found at tmax = 102.55 with a corresponding value of $^{E}$max $^{=}$ $^{785}$.77, with (a2(tmax), $^{a}$3(tmax)) $^{=}$ (28.0300, −0.2910). These values are very close to Emax = 771.09 and tmax = 103.52, which were calculated for the large Re predictions from (2.30) and (2.31) with Re = 400 and θ = 3π/4. Like the results in §2.3.3, most of the energy is in the streaks when it reaches its peak since the energy in the streamwise vortices decays monotonically.

![](_page_42_Figure_0.jpeg)

Figure 2.13: Results for L$^{z}$ = 2π, showing (a) E$^{0}$ (0) vs θ for Re = 10 (solid), Re = 400 (dashed), and the large Re limit given by (2.28) (dot-dashed, nearly coincident with dashed line), with dotted lines at θ = π/4, 3π/4, 5π/4, and 7π/4; (b) Emax vs. θ for Re = 400 (solid) and for the large Re limit given by (2.31) (dashed, nearly coincident with solid line);and (c) Emax vs. θ for Re = 1000 (solid) and for the large Re limit given by (2.31) (dashed, indistinguishable from solid line). In (b) and (c), the dotted lines are at θ = π/2, π, and 3π/2.

The absolute maximum energy that can occur for the linear dynamics can be studied using the unit energy initial condition (a2(0), $^{a}$3(0)) $^{=}$ (0, −1). For Re = 400, the maximum value Emax = 1542.30 occurs at time tmax = 103.52, with (a2(tmax), $^{a}$3(tmax)) $^{=}$ (39.2705, −0.4077). Once again, these values compare well with the predictions of large Re from (2.30) and (2.31) of Emax = 1542.17 and tmax = 103.52 for Re = 400 and θ = 3π/2. Further analysis allows for the comparison of the initial rate of the energy growth as a function of initial conditions for various Re values; see Figure 2.13(a). In the limit of large Re, Figures 2.13(b) and (c) shows how the maximum attainable energy depends on initial conditions and confirms that (2.28) and (2.31) make valid approximations.

boundaries for E 0 (0) > 0, E(t) > E(0) and [E 0 (0)]max are similar to those found in §2.3.3 and meet at Re $^{=}$ $^{7}$.466. Figure 2.15 shows the time evolution of energy for Re = 10 and E(0) = 1 where θ = 1.3972 corresponds to the initial condition that allows energy to grow above E(0) after an initial decay before decaying to zero.

A detailed analysis was conducted for the transient growth which occurs for the linear interaction between the streaks and streamwise vortices of the ninemode model in §1.2. For this linear system, it was shown that it is possible to get substantial transient growth before the system decays to the laminar state and that the magnitude of growth depends on initial conditions, Re, and aspect ratios. For large Re, it was found that the maximum energy obtained for the initial condition which maximizes initial energy growth, which corresponds to an equal initial energy distribution between the streaks and streamwise vortices, is half the absolute maximum energy where the initial energy is entirely in the streamwise vortices. Furthermore, a neutral transient growth curve, below which no initial condition gives transient growth was found. Finally, boundaries for qualitatively different E(t) were found to capture the transient behavior and the importance of initial distributions of energy of the system.

![](_page_44_Figure_0.jpeg)

Figure 2.14: Boundaries of qualitatively different E(t) for L$^{z}$ = 2π. The θ values inside the solid curve correspond to initial conditions for which E$^{0}$ (0) > 0. The θ values to the right of the dashed curve and to the left of the right branch of the solid curve correspond to initial conditions for which E(t) > E(0) for some t > 0. The dot-dashed line shows the initial condition giving [E$^{0}$ (0)]max.

![](_page_44_Figure_2.jpeg)

Figure 2.15: Time evolution of energy for L$^{z}$ = 2π, Re = 10 and E(0) = 1 for (a) θ = 2.67898 (solid) corresponding to right solid boundary of Figure 2.14, θ = 1.95411 (dashed) corresponding to left solid boundary of Figure 2.14, and θ = 1.3972 (dot-dashed) corresponding to dashed boundary of Figure 2.14. (b) Energy time series for θ = 2.8 (solid), θ = 2.3 (dotted), θ = 1.7 (dashed), and θ = 1.2 (dot-dashed)

### Chapter 3

### Pseudospectra Analysis

An alternative method of analyzing a non-normal matrix is to calculate its pseudospectrum [34, 30]. This represents a generalization of eigenvalue analysis and as shown below, gives information about the physical behavior of a system. For ² > 0, the ²-pseudospectrum of a matrix A is defined as

---

$$\Lambda_\epsilon(A) = \{z \in \mathbb{C} : \|(zI - A)^{-1}\|_2 \geq \epsilon^{-1}\}, \quad (3.1)$$

with || · ||$^{2}$ representing the 2-norm. When $^{z}$ is an eigenvalue of $^{A}$, it is useful to take the convention that ||(zI − $^{A}$) −1 ||$^{2}$ is infinite. Thus, the eigenvalues are given by $^{Λ}$0(A). The $^{²}$-pseudospectra are closed, and if $^{²}$$^{1}$ $^{&}$lt; $^{²}$2, then $^{Λ}$$^{²}$$^{1}$ ⊂ $^{Λ}$$^{²}$$^{2}$ .

An equivalent definition of the pseudospectrum is that Λ²(A) is the set of all complex numbers $^{z}$ for which the smallest singular value of $^{L}$ ≡ zI − $^{A}$ is less than or equal to ². This follows from the above definition and the fact that the 2-norm of (zI − $^{A}$) −1 equals the smallest singular value of zI − $^{A}$ $^{=}$ $^{L}$. The boundary of the ²-pseudospectrum Λ²(A) is then found by setting the smallest singular value

of L equal to ². Recall that the singular values of L are the square roots of the eigenvalues of LL† , with the 2-norm of L being equal to its largest singular value.

For the present problem let A = M23, and therefore the ²-pseudospectra can be found exactly from the definition

$$\begin{aligned} L &= zI - M_{23} \\ &= \begin{pmatrix} z - b & -c \\ 0 & z - d \end{pmatrix} \\ &= \begin{pmatrix} X + iY - b & -c \\ 0 & X + iY - d \end{pmatrix}, \end{aligned} \quad (3.2)$$

where z = X + iY . Furthermore,

$$LL^\dagger = \begin{pmatrix} b^2 + c^2 - 2bX + X^2 + Y^2 & c(d - X + iY) \\ c(d - X - iY) & d^2 - 2dX + X^2 + Y^2 \end{pmatrix}. \quad (3.3)$$

The boundary of Λ²(A) is found by setting the square root of the smallest eigenvalue of (3.3) equal to ², giving

| $\epsilon = \frac{1}{\sqrt{2}}(b^2 + c^2 + d^2 - 2bX - 2dX + 2X^2 + 2Y^2 - (b^4 + c^4 + d^2(d - 2X))^2$ $-4b^3X - 4b(c^2 - d(d - 2X))X + 2b^2(c^2 - d^2 + 2dX + 2X^2)$ $+2c^2(d^2 - 2dX + 2(X^2 + Y^2)))^{1/2})^{1/2}.$ |  |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|

Kreiss' theorem uses pseudospectra to obtain a lower bound for the maximum attainable energy [30]. Specifically,

$$\max_{t>0} \|e^{At}\|_2^2 \geq \left\lceil \sup_{\epsilon>0} \frac{\delta(\epsilon)}{\epsilon} \right\rceil^2, \quad (3.5)$$

where the left hand side is the maximum attainable energy given a unit energy initial condition, and

$$\delta(\epsilon) = \sup_{\substack{\mathbb{R}(z) > 0 \\ z \in \Lambda_\epsilon(A)}} (\mathbb{R}(z)), \quad (3.6)$$

that is, δ(²) is the largest distance from the imaginary axis to a point in the unstable half-plane lying within the ²-pseudospectrum contour, see Appendix A for a detailed derivation.

#### 3.1 Results for L$^{z}$ $^{=}$ $^{1}$.2π

For $^{L}$$^{z}$ $^{=}$ $^{1}$.2π, Re $^{=}$ 10, the eigenvalues of $^{M}$$^{23}$ are $^{b}$ $^{=}$ −0.$^{6068}$ and $^{d}$ $^{=}$ −0.5245. For small values of $^{²}$, the boundary of $^{Λ}$²(M23) is disconnected, with separate components surrounding each eigenvalue individually; for larger values of ², the boundary encloses both eigenvalues; see Figure 3.1(a). To find a lower bound for Emax, the ratio of δ(²) to ² was calculated as a function of ²; see Figure 3.2(a). This ratio was maximized for ² = 2.6, yielding a lower bound of 1.0471, which compares reasonably well with the numerically-obtained absolute maximum energy of Emax = 1.19.

Keeping L$^{z}$ = 1.2π but for Re = 400, the eigenvalues are much closer to one another, with $^{b}$ $^{=}$ −0.0152, and $^{d}$ $^{=}$ −0.0131. This means that extremely small $^{²}$ values, on the order of 10−$^{8}$ , are needed to give boundaries which surround each eigenvalue individually; see Figure 3.1(b). As above, a lower bound for Emax can be calculated. Figure 3.2(b) shows that the ratio δ(²)/² peaks at 24.774 with $^{²}$ $^{=}$ $^{5}$.$^{8}$ × $^{10}$−$^{4}$ . Therefore the lower bound for the maximum attainable energy is

![](_page_48_Figure_0.jpeg)

Figure 3.1: Boundaries for pseudospectra for L$^{z}$ = 1.2π with (a) Re = 10 and (b) Re = 400, with ² values as labeled.

613.70, approximately half the numerically-obtained value of Emax = 1328.87 from §2.3.3.

#### 3.2 Results for L$^{z}$ $^{=}$ $^{2}$π

The results for this aspect ratio are very similar to the results in §3.1. For Re $^{=}$ 10, the eigenvalues of $^{M}$$^{23}$ are $^{b}$ $^{=}$ −0.$^{4290}$ and $^{d}$ $^{=}$ −0.3467. Here, it will require larger ² values to enclose each of the small eigenvalues individually and as a result, the ² contours for this aspect ratio are less round and slightly peanut shaped compared to those for L$^{z}$ = 1.2π; see Figure 3.3(a). A lower bound was found at ² = 1.3, where the ratio δ(²)/² reaches a maximum at 1.0426, therefore giving a lower bound of 1.0871 which is reasonably close to the numerically-obtained absolute energy of Emax = 1.3121; see Figure 3.4(a).

![](_page_49_Figure_0.jpeg)

Figure 3.2: Data for determining lower bound of Emax using Kreiss' theorem, for L$^{z}$ = 1.2π and (a) Re = 10, (b) Re = 400.

$^{d}$ $^{=}$ −8.$^{669}$ × $^{10}$−$^{3}$ , and as expected from the results in §3.1 the contours surround both of the eigenvalues for the ² values used. Smaller ² values would be required to enclose each of the eigenvalues individually due to their closeness, as shown in Figure 3.3(b). A lower bound for the maximum attainable energy was calculated to be 714.0386, where the maximum ratio δ(²)/² = 26.7215 corresponds to ² = $^{3}$.$^{6}$ × $^{10}$−$^{4}$ ; see Figure 3.4(b). Similar to the results for L$^{z}$ = 1.2π and Re = 400, Emax = 1542.30 is approximately twice the value of the lower bound obtained from pseudospectra analysis. Note that the lower bound calculation is slightly more accurate for L$^{z}$ = 1.2π than for L$^{z}$ = 2π.

Figures 3.5 and 3.6 show that relationship between Emax and the lower bound obtained using Kreiss' theorem as a function of Re for L$^{z}$ = 1.2π and L$^{z}$ = 2π, respectively. The lower bound becomes less sharp as Re increases, but both the absolute maximum attainable energy and the lower bound scale as Re 2 , the former being expected from (2.31); see Figures 3.5(b) and 3.6(b). These results strengthen

![](_page_50_Figure_0.jpeg)

Figure 3.3: Boundaries for pseudospectra for L$^{z}$ = 2π with (a) Re = 10 and (b) Re = 400, with ² values as labeled.

![](_page_50_Figure_2.jpeg)

Figure 3.4: Data for determining lower bound of Emax using Kreiss' theorem, for L$^{z}$ = 2π and (a) Re = 10, (b) Re = 400.

![](_page_51_Figure_0.jpeg)

Figure 3.5: (a) Comparison of Emax (solid) to lower bound (dashed) for variable Re values and L$^{z}$ = 1.2π. (b) shows the same results as (a) but using logarithmic axes. The dotted line in (b) has slope equal to 2.

![](_page_51_Figure_2.jpeg)

Figure 3.6: a) Comparison of Emax (solid) to lower bound (dashed) for variable Re values and L$^{z}$ = 2π. (b) shows the same results as (a) but using logarithmic axes. The dotted line in (b) has slope equal to 2.

the validity of the analysis conducted in § 2.3 and suggests that although pseudospectra is an important tool for studying non-normal matrices, it may not provide the best results.

## Chapter 4

# Transient Growth and the

# Transition to Turbulence

The importance of transient energy growth for turning on nonlinear effects which can lead to sustained turbulence will be studied in this chapter. This will be achieved by carefully investigating the four-mode subspace that arises from the nonlinear coupling of the streaks and the streamwise vortices, and the full ninemode model which becomes engaged by activating one of the dormant modes in this four-mode model. That is, it will be determined how the dynamics of the linear model are carried through to the nonlinear four-mode model and subsequently the full nine-mode model.

#### 4.1 A Four-Mode Subspace

The interaction between streaks and streamwise vortices gives rise to the nonlinear term $^{N}$$^{23}$ ≡ $^{a}$2a3, which is present in the full nine-mode model of §1.2 in the equations for the amplitudes a$^{1}$ and a9. Indeed, the full nonlinear equations for the interactions of the a1, a2, a3, a$^{9}$ amplitudes are

$$\frac{da_1}{dt} = \frac{\beta^2}{Re} - \frac{\beta^2}{Re} a_1 + \sqrt{\frac{3}{2}} \frac{\beta\gamma}{\kappa_{\beta\gamma}} a_2 a_3, \quad (4.1)$$

$$\frac{da_2}{dt} = -\left(\frac{4\beta^2}{3} + \gamma^2\right) \frac{a_2}{Re} - \sqrt{\frac{3}{2}} \frac{\beta\gamma}{\kappa_{\beta\gamma}} a_1 a_3 - \sqrt{\frac{3}{2}} \frac{\beta\gamma}{\kappa_{\beta\gamma}} a_3 a_9, \quad (4.2)$$

$$\frac{da_3}{dt} = -\frac{\beta^2 + \gamma^2}{Re} a_3, \quad (4.3)$$

$$\frac{da_9}{dt} = -\frac{9\beta^2}{Re}a_9 + \sqrt{\frac{3}{2}}\frac{\beta\gamma}{\kappa_{\beta\gamma}}a_2a_3. \quad (4.4)$$

These equations form an invariant subspace for the full nine-mode model of §1.2. Here, the streamwise vortices pull up negative fluid and pull down positive fluid causing the streaks to strengthen, which leads to the modification of the basic profile. This modification to the mean profile then leads to the weakening of the streaks. The interaction between the streamwise vortices, streaks, and basic profile in this subspace essentially captures the re-distribution of energy in the system. The laminar state corresponds to a fixed point at (a1, a2, a3, a9) = (1, 0, 0, 0) and the energy about this state is defined as

$$E_4(t) = (a_1(t) - 1)^2 + (a_2(t))^2 + (a_3(t))^2 + (a_9(t))^2.$$
 (4.5)

#### 4.1.1 Optimal Growth of the Nonlinear Term N$^{23}$

The initial growth rate for N$^{23}$ is given by

$$\begin{aligned} N_{2,3}(0) &= a_2(0)a_3(0) + a_2(0)a_3'(0) \\ &= (b+d)a_{20}a_{30} + ca_{30}^2. \end{aligned} \quad (4.6)$$

Similar to §2.2, finding the extrema of this subject to the constraint

| $a_{20}^2 + a_{30}^2 = 1$ | $(4.7)$ |
|---------------------------|---------|
|---------------------------|---------|

leads to an eigenvalue problem, here

$$\begin{pmatrix} 0 & (b+d)/2 \\ (b+d)/2 & c \end{pmatrix} \begin{pmatrix} a_{20} \\ a_{30} \end{pmatrix} = \lambda \begin{pmatrix} a_{20} \\ a_{30} \end{pmatrix}. \quad (4.8)$$

The eigenvalues are

$$\begin{aligned} \lambda_{\pm} &= c \pm \sqrt{b^2 + c^2 + 2bd + d^2} & (4.9) \\ &= \frac{-3\sqrt{3}\beta\gamma Re \pm \sqrt{98\beta^6 + 266\beta^4 + 72\gamma^6 + 3\beta^2(80\gamma^4 + 9\gamma^2 Re^2)}}{3\sqrt{2(\beta^2 + \gamma^2)}Re} & (4.10) \end{aligned}$$

with (unnormalized) eigenvectors

$$\begin{aligned} \mathbf{e}_{\pm} &= \left( \frac{-c \pm \sqrt{b^2 + c^2 + 2bd + d^2}}{b + d}, 1 \right) \\ &= \left( \frac{-3\sqrt{3}\beta\gamma Re \mp \sqrt{98\beta^6 + 266\beta^4 + 72\gamma^6 + 3\beta^2(80\gamma^4 + 9\gamma^2 Re^2)}}{\sqrt{2(\beta^2 + \gamma^2)}(7\beta^2 + 6\gamma^2)}, 1 \right). \end{aligned} \quad (4.11)$$

respectively. The large Re limit is most easily captured by considering (4.8) with $^{b}$ → $^{0}$ and $^{d}$ → 0. This gives

| $\lambda_+ \approx 0,$ | $\mathbf{e}_+ \approx (1, 0),$ | (4.13) |
|------------------------|--------------------------------|--------|
|------------------------|--------------------------------|--------|

$$\lambda_- \approx c = -\frac{\sqrt{3/2}\beta\gamma}{\sqrt{\beta^2 + \gamma^2}}, \quad \mathbf{e}_- \approx (0, 1), \quad (4.14)$$

where the eigenvectors have been normalized.

Letting E(0) = a 2 $^{20}$ + a 2 $^{30}$ = 1 and θ = tan−$^{1}$ (a30/a20), (4.6) is rewritten as

| $N'_{23}(0) = (b+d) \cos \theta \sin \theta + c \sin^2 \theta$ | (4.15) |
|----------------------------------------------------------------|--------|
|----------------------------------------------------------------|--------|

$$= \frac{b+d}{2} \sin 2\theta + \frac{c}{2}(1 - \cos 2\theta). \quad (4.16)$$

This is periodic in θ with period π. For systems with large Re,

$$N'_{23}(0) \approx \frac{c}{2}(1 - \cos 2\theta). \quad (4.17)$$

In this limit, N0 $^{23}$(0) must always be less than or equal to zero, since c < 0. Furthermore, in this limit |N$^{0}$ $^{23}$(0)| reaches its maximum value of |c| for $^{\theta}$ ≈ π/$^{2}$ and $^{\theta}$ ≈ $^{3}$π/2, and its minimum value of $^{0}$ for $^{\theta}$ ≈ $^{0}$ and $^{\theta}$ ≈ $^{π}$, results consistent with (4.13) and (4.14).

As in §2.3, progress can be made in understanding how the maximum value that |$^{N}$23(t)| reaches under the linear evolution depends on the initial distribution of energy between streamwise vortices and streaks, as captured by θ. The value of this analysis is limited as perturbations to the laminar state grow, since the linear dynamics becomes less relevant as nonlinear interactions increase. Nevertheless, it is hoped that useful information will be extracted from this investigation. Using (2.2) and (2.3) for unit initial energy and taking the limit of large Re for which $^{b}$ → $^{0}$ and $^{d}$ → 0, the following is obtained

---

$$N_{23}(t) \approx \frac{c}{d-b} e^{dt} (e^{dt} - e^{bt}) \sin^2 \theta. \quad (4.18)$$

This also requires that θ is not too close to 0 or π so that the other term can be dropped. Since d > b and c < 0, N$^{23}$ is expected to be negative for all times. Solving N0 $^{23}$(t) $^{=}$ $^{0}$ for $^{t}$ using (4.18), it is found that |$^{N}$23| reaches its maximum value at

$$t_{max N_{23}} \approx \frac{\log(2d/(b+d))}{b-d} = \frac{3Re}{\beta^2} \log\left(\frac{7\beta^2 + 6\gamma^2}{6(\beta^2 + \gamma^2)}\right). \quad (4.19)$$

with

$$|N_{23}|_{max} \approx |N_{23}(t_{max}N_{23})| \approx \frac{(2(\beta^2 + \gamma^2))^{11/2+6\gamma^2/\beta^2} 3^{15/2+6\gamma^2/\beta^2} \beta \gamma}{(7\beta^2 + 6\gamma^2)^{7+6\gamma^2/\beta^2}} Re \sin^2 \theta. \quad (4.20)$$

Thus, |$^{N}$23|max reaches its absolute maximum value for $^{\theta}$ ≈ π/$^{2}$ and $^{\theta}$ ≈ $^{3}$π/2, the same $^{\theta}$ values for which |N$^{0}$ (0)| is maximized.

#### 4.1.2 Results for L$^{z}$ = 1.2π

As an example, consider the aspect ratio L$^{z}$ = 1.2π. Figure 4.1(a) and (b) respectively show how N0 $^{23}$(0) and the maximum value of |$^{N}$23| due to the linear evolution depend on the initial distribution of energy between the streamwise vortices and the streaks, as captured by θ and Re. The initial condition (a20, a30) = (0.0101, $^{0}$.9999) maximizes |N$^{0}$ $^{23}$(0)| with the approximate value |c| $^{=}$ $^{1}$.4, and the linear evolution gives the maximum value |$^{N}$23| $^{=}$ $^{18}$.$^{90}$ reached at $^{t}$ $^{=}$ $^{36}$.$^{71}$ with (a2, $^{a}$3) $^{=}$ (30.5805, −0.6179). Note that the large Re predictions from (4.19) and (4.20) (with $^{\theta}$ $^{=}$ π/$^{2}$ and Re $^{=}$ 400) are $^{t}$maxN$^{23}$ $^{=}$ $^{36}$.$^{71}$ and |$^{N}$23|max $^{=}$ $^{18}$.90, which are identical to this precision with the results for the above initial condition.

For comparison, for the initial condition (a20, $^{a}$30) $^{=}$ (0.7066, −0.7076) which maximizes E 0 (0), the linear evolution gives the maximum value |$^{N}$23| $^{=}$ $^{9}$.$^{6438}$ reached at $^{t}$ $^{=}$ $^{36}$ with (a2, $^{a}$3) $^{=}$ (21.8505, −0.4414); see Figure 4.2.

#### 4.1.3 Results for L$^{z}$ = 2π

The results for the aspect ratio $^{L}$$^{z}$ $^{=}$ $^{2}$$^{π}$ are very similar to those in §4.1.2. Figure 4.3(a) and (b) respectively show N0 $^{23}$(0) and the maximum value of |$^{N}$23| due to the linear evolution as a function of the initial distribution of energy between the streamwise vortices and the streaks, as captured by θ, and on Re. The initial condition (a20, $^{a}$30) $^{=}$ (0.0101, $^{0}$.9999) maximizes |N$^{0}$ $^{23}$(0)| with the approximate value |c| $^{=}$ $^{1}$.033, and the linear evolution reached $^{a}$ maximum value at $^{t}$ $^{=}$ $^{54}$.$^{52}$ of |$^{N}$23| $^{=}$ $^{20}$.70, with (a2, $^{a}$3) $^{=}$ (33.2075, −0.6233). The large Re predictions from (4.19) and (4.20) for θ = π/2 and Re = 400 are tmaxN$^{23}$ = 54.51 and |$^{N}$23|max $^{=}$ $^{20}$.71. Again, for comparison, the linear evolution gives the maximum value |$^{N}$23| $^{=}$ $^{10}$.$^{5488}$ reached at $^{t}$ $^{=}$ $^{53}$.$^{54}$ with (a2, $^{a}$3) $^{=}$ (23.71, −0.4450) for the initial condition (a20, $^{a}$30) $^{=}$ (0.7066, −0.7076) which maximizes $^{E}$ 0 (0); see Figure 4.4.

#### 4.1.4 Time Evolution due to Nonlinear Interactions

Thus far, only the dynamics associated with the linearization about the laminar state have been considered. Here, the effects of the nonlinear terms on the dynamics of (4.1-4.4) are explored, with an emphasis on the role of transient growth. To do

![](_page_58_Figure_0.jpeg)

Figure 4.1: Results for $^{L}$$^{z}$ $^{=}$ $^{1}$.2π, showing (a) |N$^{0}$ $^{23}$(0)| vs. $^{\theta}$ for Re $^{=}$ $^{10}$ (solid), Re $^{=}$ $^{400}$ (dashed), and the large Re limit given by (4.17) (dot-dashed, nearly coincident with dashed line); (b) |$^{N}$23|max vs. $^{\theta}$ for Re $^{=}$ $^{400}$ (solid) and the large Re limit given by (4.20) (dashed, nearly coincident with solid line); and (c) |$^{N}$23|max vs. $^{\theta}$ for Re $^{=}$ $^{1000}$ (solid) and the large Re limit given by (4.20) (dashed, indistinguishable from solid line). The dotted lines are at θ = π/2, π, and 3π/2.

![](_page_58_Figure_2.jpeg)

Figure 4.2: Time evolution of |$^{N}$23| for (solid) initial condition which maximizes $^{E}$$^{0}$ (0) and (dashed) initial condition which maximizes |N$^{0}$ $^{23}$(0)| at $^{t}$ $^{=}$ 0.

![](_page_59_Figure_0.jpeg)

Figure 4.3: Results for $^{L}$$^{z}$ $^{=}$ $^{2}$π, showing (a) |N$^{0}$ $^{23}$(0)| vs. $^{\theta}$ for Re $^{=}$ $^{10}$ (solid), Re $^{=}$ $^{400}$ (dashed), and the large Re limit given by (4.17) (dot-dashed, nearly coincident with dashed line); (b) |$^{N}$23|max vs. $^{\theta}$ for Re $^{=}$ $^{400}$ (solid) and the large Re limit given by (4.20) (dashed, nearly coincident with solid line); and (c) |$^{N}$23|max vs. $^{\theta}$ for Re $^{=}$ $^{1000}$ (solid) and the large Re limit given by (4.20) (dashed, indistinguishable from solid line). The dotted lines are at θ = π/2, π, and 3π/2.

![](_page_59_Figure_2.jpeg)

Figure 4.4: Time evolution of |$^{N}$23| for $^{L}$$^{z}$ $^{=}$ $^{2}$$^{π}$ for (solid) initial condition which maximizes E$^{0}$ (0) and (dashed) initial condition which maximizes |N$^{0}$ $^{23}$(0)| at $^{t}$ $^{=}$ 0.

![](_page_60_Diagram_0.jpeg)

Figure 4.5: Pictorial representation of the effect of nonlinear terms on the modal amplitudes. The interaction between modes 2 and 3 gives the nonlinear term N$^{23}$ = a2a3, which affects the dynamics of modes a$^{1}$ and a9. Modes 1 and 3 interact to give the nonlinear term a1a3, which affects the dynamics of mode 2. Modes 3 and 9 interact to give the term a3a9, which affects the dynamics of mode 2.

this, it is important to understand the energy flow for this problem. The constant term in (4.1) is due to the sinusoidal body force, and is the only source of energy. The linear terms in (4.1-4.4) are due to viscous dissipation, and extract energy from the system. The nonlinear terms in (4.1-4.4) are energy conserving, merely transferring energy from one mode to another, e.g., [22]: see Figure 4.5. Since the modes u1, u2, u3, u$^{9}$ are all streamwise invariant, general arguments imply that all disturbances to the laminar state must eventually decay [23, 22]; see Appendix B. However, the transient behavior leading to this decay can be nontrivial, as will be seen in the following.

#### • $^{A}$ Small Perturbation to the Laminar State

Now consider the initial condition

| $(a_{10}, a_{20}, a_{30}, a_{90}) = (1, 0.07066, -0.07076, 0),$ | (4.21) |
|-----------------------------------------------------------------|--------|
|-----------------------------------------------------------------|--------|

corresponding to a small perturbation to the laminar state in the direction of fastest initial transient energy growth. The initial energy is E(0) = a 2 $^{20}$ + a 2 $^{30}$ = 0.1.

The initial dynamics are dominated by the transient growth due to the interaction of the streaks and streamwise vortices. This causes the nonlinear term N$^{23}$ to become more negative, making a$^{1}$ and a$^{9}$ decrease. Physically, the streamwise vortices pull up negative velocity fluid at z = Lz/2 and pull down positive velocity fluid at z = 0. When this is averaged across the z-direction, the amount of energy in the mean flow modes 1 and 9 is diminished. Since a$^{1}$ started at 1, it is expected to remain positive, at least for small times. Since a$^{3}$ is negative, the term proportional to −$^{a}$1a$^{3}$ in (4.2) is positive: physically, the streamwise vortices strengthen the streaks. On the other hand, a$^{9}$ starts at zero and becomes negative for small times. Thus, the term proportional to −$^{a}$3a$^{9}$ in (4.2) is negative. Physically, this comes from the fact that the mean flow modification associated with a$^{9}$ is positive just below the midplane and negative just above the midplane. Advection of this modification to the mean profile by the streamwise vortices leads to a weakening of the streaks.

As time progresses, the linear and nonlinear terms conspire to cause a$^{2}$ to start to decrease at an earlier time and smaller magnitude than one would expect from the linear dynamics. Indeed, instead of the energy peaking at E = a 2 $^{2}$ +a 2 $^{3}$ = 6.7807 with (a2, $^{a}$3) $^{=}$ (2.60382, −0.02821) at $^{t}$ $^{=}$ $^{70}$.12, as would be expected due to linear transient growth (see §2.3.3), it only reaches $^{E}$$^{4}$ $^{=}$ (a$^{1}$ − 1)$^{2}$ $^{+}$ $^{a}$ 2 $^{2}$ + a 2 $^{3}$ + a 2 $^{9}$ = 1.3222 for the four-mode subspace and E = a 2 $^{2}$ + a 2 $^{3}$ = 0.4636 for the streak-streamwise vortex interaction with (a2, $^{a}$3) $^{=}$ (0.6782, −0.0607) at $^{t}$ $^{=}$ $^{11}$.69. Next, $^{a}$$^{2}$ reaches a local minimum at t = 44.09 before growing to a local maximum at t = 108.7 and then decaying monotonically to zero; see Figure 4.6. This differs from the linear dynamics, in which a$^{2}$ monotonically decreases after reaching its first peak; see Figure 2.6. Such "ringing" behavior is due to the nonlinear interactions, and will be more prominent for larger initial perturbations. Note that a$^{3}$ monotonically increases toward zero as time progresses. Physically the decay of streamwise vortices is due to dissipation; there are no interactions for the set of modes in (4.1-4.4) which excite this mode.

Next, consider the initial condition

| $(a_{10}, a_{20}, a_{30}, a_{90}) = (1, 0, -0.1, 0)$ , | (4.22) |
|--------------------------------------------------------|--------|
|--------------------------------------------------------|--------|

corresponding to a small perturbation to the laminar state in the direction of maximum transient energy growth for the linear problem, with same energy as the initial condition just considered. Instead of the energy peaking at E = 13.2903 with (a2, $^{a}$3) $^{=}$ (3.64537, −0.03950) at time $^{t}$ $^{=}$ $^{70}$.83, as would be expected due to linear transient growth (see §2.3.3), it only reaches $^{E}$$^{4}$ $^{=}$ $^{1}$.$^{4693}$ and $^{E}$ $^{=}$ $^{0}$.$^{4781}$ with (a2, $^{a}$3) $^{=}$ (0.6856, −0.0894) at $^{t}$ $^{=}$ $^{8}$.57; see Figure 4.6. For both initial conditions, the nonlinearities greatly restrict the magnitude of the transient growth.

![](_page_63_Figure_3.jpeg)

Figure 4.6: Time evolutions for  $a_1(t), a_2(t), a_3(t), a_9(t), E(t), N_{23}(t)$  for the initial conditions  $(a_1, a_2, a_3, a_9) = (1, 0.07066, -0.07076, 0)$  and  $(1, 0, -0.1, 0)$  shown in solid and dashed lines, respectively.

### • $^{A}$ Larger Perturbation to the Laminar State

Consider the initial condition

| $(a_{10}, a_{20}, a_{30}, a_{90}) = (1, 0.7066, -0.7076, 0)$ , | (4.23) |
|----------------------------------------------------------------|--------|
|----------------------------------------------------------------|--------|

corresponding to a larger perturbation to the laminar state in the direction of fastest initial transient energy growth. (The values a$^{20}$ and a$^{30}$ are a factor of ten higher than those just considered, giving E(0) = a 2 $^{20}$ + a 2 $^{30}$ = 1.) As above, the nonlinear terms prevent a$^{2}$ from reaching its maximum found by just considering linear dynamics. Indeed, here the energy peaks at E$^{4}$ = 3.2411 and $^{E}$ $^{=}$ $^{1}$.$^{4816}$ with (a2, $^{a}$3) $^{=}$ (0.9941, −0.7024) at time $^{t}$ $^{=}$ $^{0}$.56, whereas in §2.3.3 it was found that this initial condition would lead to an energy E = 664.44 with (a2, $^{a}$3) $^{=}$ (26.0382, −0.2821) at time $^{t}$ $^{=}$ $^{70}$.$^{12}$ under linear dynamics. The same physical processes as described above occur here. However, there is much more prominent ringing behavior, in which a$^{2}$ undergoes decaying oscillations on its way to zero; see Figure 4.7. The ringing is associated with the streaks being pulled apart and advecting around the streamwise vortices, returning for another lap; see Figure 4.8. The timescale of the oscillations is approximately one characteristic turnover time as estimated from the velocity reconstruction for this particular perturbation to the laminar state. The size of such oscillations decreases with time (not surprisingly, since the system must approach the laminar state for large times) and their frequency decreases (as a$^{3}$ decays away, the characteristic turnover time gets longer and longer).

![](_page_65_Figure_3.jpeg)

Figure 4.7: Time evolutions for  $a_1(t), a_2(t), a_3(t), a_9(t), E(t), N_{23}$  for the initial condition  $(a_1, a_2, a_3, a_9) = (1, 0.7066, -0.7076, 0)$ .

![](_page_66_Figure_0.jpeg)

Figure 4.8: Velocity reconstructions showing the advection of streaks by the streamwise vortices for the initial conditions (a1, $^{a}$2, $^{a}$3, $^{a}$9) $^{=}$ (1, $^{0}$.7066, −0.7076, 0) at (a) $^{t}$ $^{=}$ 0, (b) $^{t}$ $^{=}$ $^{0}$.56, (c) t = 1.32, (d) t = 2.08, (e) t = 2.85, and (f) t = 5.22.

Finally, consider the initial condition

(a10, $^{a}$20, $^{a}$30, $^{a}$90) $^{=}$ (1, $^{0}$, −1, 0), (4.24)

corresponding to a larger perturbation to the laminar state in the direction of maximum transient energy growth for the linear problem, with same energy as the initial condition just considered. Here the energy peaks at E$^{4}$ = 2.8889 and $^{E}$ $^{=}$ $^{1}$.$^{477}$ with (a2, $^{a}$3) $^{=}$ (0.7051, −0.9897) at time $^{t}$ $^{=}$ $^{0}$.79, whereas in §2.3.3 it was found that this initial condition would lead to an energy E = 1329.03 with (a2, $^{a}$3) $^{=}$ (36.4537, −0.3950) at time $^{t}$ $^{=}$ $^{70}$.$^{83}$ under linear dynamics.

#### 4.2 The Full Nine-Mode Model

By perturbing one of the other amplitudes, say a4, away from zero, nonlinear interactions cause all of the modes in the nine-mode model of §1.2 to become active. If the perturbation away from the four-mode subspace is sufficiently small, the dynamics described above are expected to be present, at least for short times. However, the dynamics for longer times are very sensitive to the initial conditions. To further emphasize this argument, the relevance of the two-mode linear model to the four-mode model is shown by perturbing a$^{20}$ and a$^{30}$ by a small factor µ as

$$(a_{20}, a_{30}) = \mu(0.7066, -0.7076). \quad (4.25)$$

In Figure 4.9, it is shown that as E(0) or µ decreases, linear analysis becomes important for the four-mode model and as expected, small perturbations from the laminar state minimize the effects of nonlinearities on the magnitude of the transient growth. Furthermore, perturbing a$^{4}$ from the laminar state allows to investigate the importance of transient growth to the full nine-mode model. For very small a40, the dynamics of the four-mode model are carried through the nine-mode model. As µ increases, linear analysis and the four-mode model are less valid. The possibility of turbulence in the nine-mode model in terms of the amount of perturbation on a2, a$^{3}$ and a$^{4}$ can also be determined; see Figure 4.10. All disturbances below the curve will eventually decay back to the laminar state whereas disturbances above the curve might trigger turbulence.

This is illustrated by considering the parameter values L$^{z}$ = 1.2π, Re = 400,

![](_page_68_Figure_0.jpeg)

Figure 4.9: Amplification of E(t) for two-mode linear problem (dashed), four-mode (solid) and nine-mode (dotted) models represented by different a$^{40}$ initial conditions, as shown. The fourmode model matches the two-mode model for smaller perturbations to the laminar state. When all nine modes are included, the nonlinear terms are turned on more readily causing the dynamics of the full nine-mode model to behave less like that of the four-mode model as perturbations grow.

![](_page_68_Figure_2.jpeg)

Figure 4.10: Boundary which shows the possibility of turbulence for variable a$^{40}$ and µ. All perturbations below the curve decay to the laminar state whereas perturbations above might drive the system to sustained turbulence.

for which it has been shown that a stable periodic orbit coexists with the stable laminar state [20, 21]. The stable periodic orbit may be interpreted as a sustained turbulent state. Consider initial conditions

$$(a_{10}, a_{20}, a_{30}, a_{50}, a_{60}, a_{70}, a_{80}, a_{90}) = (1, 0.07066, -0.07076, 0, 0, 0, 0, 0), \quad (4.26)$$

with various values for a40. Figure 4.11 shows that it is very difficult to predict which values of a$^{40}$ lead to sustained turbulence or decay to the laminar state. Indeed, this is reminiscent of the fractal lifetime properties of [20] in which it was demonstrated that the length of time for which turbulence persists is very sensitive to initial conditions at any resolution. This sensitivity to initial conditions is further illustrated in Figures 4.12 and 4.13, which compare the dynamics for a$^{40}$ values equal to 0.06 and 0.059975. Initially, the trajectories for the two initial conditions are very close, and (moderate) transient growth is evidently present for a short time until it is damped by the nonlinear effects due to the coupling of the modes. The two solutions later diverge to either the laminar state (stable fixed point) or the sustained turbulent state (stable periodic orbit), with changes in $^{a}$$^{40}$ of $^{2}$.$^{5}$ × $^{10}$−$^{6}$ or less leading to different outcomes.

![](_page_70_Figure_0.jpeg)

Figure 4.11: For initial conditions given by (4.26), the dots represent the values of a$^{40}$ for which the solution converges to the stable periodic orbit, which is interpreted as sustained turbulence. Other initial a$^{40}$ values lead to a trajectory which decays to the stable fixed point corresponding to the laminar state.

![](_page_71_Figure_0.jpeg)

Figure 4.12: Time evolution of the nine modes for the initial conditions (a1, $^{a}$2, $^{a}$3, $^{a}$4, $^{a}$5, $^{a}$6, $^{a}$7, $^{a}$8, $^{a}$9) $^{=}$ (1, $^{0}$.07066, −0.07076, $^{0}$.06, $^{0}$, $^{0}$, $^{0}$, $^{0}$, 0) and (1, $^{0}$.07066, −0.07076, $^{0}$.059975, $^{0}$, $^{0}$, $^{0}$, $^{0}$, 0) shown in solid and dashed lines, respectively. The first initial condition gives a trajectory which asymptotes on the stable periodic orbit, while the latter gives a trajectory which decays to the laminar state.

![](_page_72_Figure_3.jpeg)

Figure 4.13: Time evolution of the nine modes for the initial conditions from Figure 4.12, zoomed in to show the behavior for short times.

### Chapter 5

# Conclusion

Transient growth due to the linear interaction between streaks and streamwise vortices for a nine-dimensional model for sinusoidal shear flow was investigated in this thesis. Initial perturbations which give optimal initial and total energy growth were obtained along with the neutral transient growth curve, below which no initial condition gives transient energy growth. The dependence of the dynamics on the initial distribution of perturbation energy between streaks and streamwise vortices was characterized. An alternative interpretation of transient growth was given using pseudospectra, which leads to a lower bound for the maximum attainable energy. Finally, the importance of such transient growth for triggering nonlinear effects that might sustain turbulence was considered by studying the dynamics of the four-mode subspace, resulting from the nonlinear coupling of the streaks and the streamwise vortices, and the full nine-mode model.

These results represent a powerful generalization of standard hydrodynamic sta-

bility analysis to systems which lack a linear instability. The standard analysis just calculates eigenvalues, and hence only captures asymptotic behavior. Furthermore, the standard analysis would not identify any difference in the situation, for example, in which there is an equal initial distribution of energy between streaks and rolls, or when the energy is all initially in the streamwise vortices. The analysis in this thesis overcomes these limitations by usefully capturing the transient behavior and the importance of different initial distributions of energy.

The results show that the linear dynamics of the streaks and streamwise vortices can lead to substantial transient growth and are consistent with previous results for the plane Couette flow [5] and Taylor-Couette flow in the plane Couette flow limit [12]. The approach presented in this thesis has the advantage of exploring how the results depend on the aspect ratio, Reynolds number, and initial conditions. For example, the results were obtained for two distinct domains. For the related system of plane Couette flow, the first is L$^{x}$ = 1.75π and L$^{z}$ = 1.2π, which corresponds to the minimal flow unit, the smallest domain which is found numerically to sustain turbulence [10]. The second is L$^{x}$ = 4π and L$^{z}$ = 2π, larger than the previous, it corresponds to the domain size where the steady finite amplitude solutions appear at the smallest value of the Reynolds number [6, 39]. For both domains, it was found that in the limit of large Reynolds number, the initial conditions which maximizes initial energy growth involved an equal distribution of energy between the streaks and streamwise vortices, with the vortices advecting the fluid in such a way as to strengthen the streaks. On the other hand, in this limit the initial condition which

gives the absolute maximum value of energy has all of the energy in the streamwise vortices; this is also the initial condition which initially turns on nonlinear terms in an optimal fashion.

Overall, it was found that the transient growth due to the linear interaction between the streaks and the streamwise vortices is severely limited by nonlinear effects. The four-mode subspace, containing the nonlinear coupling between the streaks and streamwise vortices, was initially dominated by transient growth and exhibited a "ringing" behavior before decaying to the laminar state. Indeed, for the full nonlinear problem, transient growth mechanisms are apparently only important for initial conditions very close to the laminar state, and for short times. The system was found to be very sensitive to small perturbations to the laminar state, and exhibited the fractal lifetime properties of [20]. Nevertheless, the analysis of transient growth mechanisms helps to clarify the transition to and nature of shear flow turbulence.

In the simulation of the full nine-mode model, transient growth is greatly restricted by the nonlinearities of the system suggesting that it is not the main force which drives the system to a state of turbulence. Therefore, future research will involve investigating the mechanisms which determine the transition to turbulence for the nine-dimensional model. Specifically, a distinction between solutions which give transient and sustained turbulence will be made. Furthermore, the mechanisms responsible for driving the solutions to either the laminar, transient turbulence, or sustained turbulence state will be explored.

# Bibliography

[1] N. Aubry, P. Holmes, J. L. Lumley, and E. Stone. The dynamics of coherent structures in the wall region of the turbulent boundary layer. J. Fluid Mech., 192:115–73, 1988. [2] J. S. Baggett and L. N. Trefethen. Low-dimensional models of subcritical transition to turbulence. Phys. Fluids, 9:1043–53, 1997. [3] K. M. Bobba, B. Bamieh, J. C. Doyle, and Antonis Papachristodoulou. Global stability and transient growth of stream-wise constant perturbations in parallel flows. 2005. In Preparation. [4] F. H. Busse. Visualizing the dynamics of the onset of turbulence. Science, 305:1574–1575, 2004. [5] K. M. Butler and B. F. Farrell. Three-dimensional optimal perturbations in viscous shear flow. Phys. Fluids A, 4:1637–1650, 1992. [6] R. M. Clever and F. H. Busse. Three-dimensional convection in a horizontal fluid layer subjected to a constant shear. J. Fluid Mech, 234:511–27, 1992.

- [7] P. G. Drazin and W. H. Reid. Hydrodynamic Stability. Cambridge University Press, Cambridge, UK, 1981. [8] B. Eckhardt and A. Mersmann. Transition to turbulence in a shear flow. Phys. Rev. E, 60:509–17, 1999. [9] H. Faisst. Turbulence transition in pipe flow. PhD thesis, Universit¨at Marburg, 2003. [10] J. Hamilton, J. Kim, and F. Waleffe. Regeneration mechanisms of near-wall turbulence structures. J. Fluid Mech., 287:317–48, 1995. [11] B. Hof, C. W. H. van Doorne, J. Westerweel, F. T. M. Nieuwstadt, H. Faisst,
- B. Eckhardt, H. Wedin, R. R. Kerswell, and F. Waleffe. Experimental observation of nonlinear traveling waves in turbulent pipe flow. Science, 305:1594– 1598, 2004. [12] H. Hristova, S. Roch, P. J. Schmid, and L. S. Tuckerman. Transient growth in Taylor-Couette flow. Phys. Fluids, 14:3475–3484, 2002. [13] J. Jim´enez and A. Pinelli. The autonomous cycle of near-wall turbulence. J. Fluid Mech., 389:335–359, 1999. [14] D. D. Joseph and W. Hung. Contributions to the nonlinear theory of stability of viscous flow in pipes and between rotating cylinders. Arch. Rational Mech. Anal., 44:1–22, 1971.

- [15] D. D. Joseph and L. N. Tao. Transverse velocity components in fully developed unsteady flows. J. Appl. Mech., 30:147–148, 1963. [16] M. R. Jovanovi´c and B. Bamieh. Componentwise energy amplification in channel flows. J. Fluid Mech., 543:145–183, 2005. [17] G. Kawahara and S. Kida. Periodic motion embedded in plane Couette turbulence: regeneration cycle and burst. J. Fluid Mech., 449:291–300, 2001. [18] P. Manneville. Spots and turbulent domains in a model of transitional plane Couette flow. Theor. Comp. Fluid Dyn., 18:169–181, 2004. [19] P. Manneville and F. Locher. A model for transitional plane Couette flow. C.
- R. Acad. Sci. II B, 328:159–164, 2000. [20] J. Moehlis, H. Faisst, and B. Eckhardt. A low-dimensional model for turbulent shear flows. New J. Phys., 6, 2004. Article 56. [21] J. Moehlis, H. Faisst, and B. Eckhardt. Periodic orbits and chaotic sets in a low-dimensional model for shear flows. SIAM J. Appl. Dyn. Syst., 4:352–376, 2005. [22] J. Moehlis, T. R. Smith, P. Holmes, and H. Faisst. Models for turbulent plane Couette flow using the proper orthogonal decomposition. Phys. Fluids, 14(7):2493–507, 2002. [23] H. K. Moffatt. Fixed points of turbulent dynamical systems and suppression

of nonlinearity. In J. L. Lumley, editor, Whither Turbulence? Turbulence at the Crossroads, pages 250–57. Springer-Verlag, New York, 1990. [24] M. Nagata. Three-dimensional finite-amplitude solutions in plane Couette flow: bifurcation from infinity. J. Fluid Mech., 217:519–27, 1990. [25] B. R. Noack, P. Papas, and P. A. Monkewitz. The need for a pressure-term representation in empirical Galerkin models of incompressible shear-flows. J. Fluid Mech., 523:339–365, 2005. [26] R. L. Panton. Incompressible Flow. Wiley-Interscience, New York, 1996. [27] B. Podvin and J. Lumley. A low-dimensional approach for the minimal flow unit. J. Fluid Mech., 362:121–55, 1998. [28] S. C. Reddy, P. J. Schmid, J. S. Baggett, and D. S. Henningson. On stability of streamwise streaks and transition thresholds in plane channel flows. J. Fluid Mech., 365:269–303, 1998. [29] D. Rempfer. Low-dimensional modeling and numerical simulation of transition in simple shear flows. Annu. Rev. Fluid. Mech., 35:229–265, 2003. [30] P. J. Schmid and D. S. Henningson. Stability and Transition in Shear Flows. Springer-Verlag, New York, NY, 2000. [31] A. Schmiegel. Transition to turbulence in linearly stable shear flows. PhD thesis, Universit¨at Marburg, 1999.

[32] T. R. Smith, J. Moehlis, and P. Holmes. Low-dimensional modelling of turbulence using the proper orthogonal decomposition: a tutorial. Nonlinear Dynamics, 41:275–307, 2005. [33] T. R. Smith, J. Moehlis, and P. Holmes. Low-dimensional models for turbulent plane Couette flow in a minimal flow unit. J. Fluid Mech., 538:71–110, 2005. [34] L. N. Trefethen. Pseudospectra of matrices. In D. F. Griffiths and G. A. Watson, editors, Numerical Analysis 1991, pages 234–266. Longman Sci. Tech, Harlow, Essex, UK, 1992. [35] L. N. Trefethen, A. E. Trefethen, S.C. Reddy, and T.A. Driscoll. Hydrodynamic stability without eigenvalues. Science, 261:578–84, 1993. [36] F. Waleffe. Hydrodynamic stability and turbulence: beyond transients to a self-sustaining process. Stud. Appl. Math., 95:319–43, 1995. [37] F. Waleffe. Transition in shear flows. Nonlinear normality versus non-normal linearity. Phys. Fluids, 7(12):3060–6, 1995. [38] F. Waleffe. On a self-sustaining process in shear flows. Phys. Fluids, 9:883–900, 1997. [39] F. Waleffe. Homotopy of exact coherent structures in plane shear flows. Phys. Fluids, 15(6):1517–34, 2003.

## Appendix A

# Finding a Lower Bound for

# Transient Energy Growth Using

# Kreiss' Theorem

A lower bound for transient energy growth can be obtained for a matrix exponential using Kreiss' theorem [30]. For a general linear equation $^{a}$˙ = Aa, which has the exact solution

$$a(t) = e^{tA} a_0, \quad (A.1)$$

the lower bound is calculated by defining the Laplace transform

$$\mathcal{L}(\mathbf{a}) = \tilde{\mathbf{a}} = \int_0^\infty e^{-st} \mathbf{a} dt. \quad (\text{A.2})$$

Since L (e At) $^{=}$ (sI − $^{A}$) −1 , (A.2) can be expressed as

---

$$\tilde{\mathbf{a}} = (sI - A)^{-1}\mathbf{a}_0 = \int_0^\infty e^{-st} e^{At}\mathbf{a}_0 dt. \quad (\text{A.3})$$

To find the bound, (sI − $^{A}$) −$^{1}$ must be estimated from (A.3) as follows

$$\begin{aligned} \|(sI - A)^{-1}\|_2 &\leq \int_0^\infty |e^{-st}| \|e^{At}\|_2 dt \\ &\leq \max_{t>0} \|e^{At}\|_2 \int_0^\infty e^{-\mathbb{R}(s)t} dt. \end{aligned} \quad (\text{A.4})$$

Since

$$\int_0^\infty e^{-\mathbb{R}(s)t} dt = \left[ -\frac{1}{\mathbb{R}(s)} e^{-\mathbb{R}(s)t} \right]_0^\infty = \frac{1}{\mathbb{R}(s)}, \quad (\text{A.5})$$

then

$$\|(sI - A)^{-1}\|_2 \leq \frac{1}{\mathbb{R}(s)} \max_{t>0} \|e^{At}\|_2. \quad (\text{A.6})$$

Rearranging (A.6) gives

$$\max_{t>0} \|e^{At}\|_2 \geq \mathbb{R}(s) \|(sI - A)^{-1}\|_2 \geq \max_{\mathbb{R}(s)>0} \mathbb{R}(s) \|(sI - A)^{-1}\|_2. \quad (\text{A.7})$$

Now, recall the definition of pseudospectra,

---

$$\Lambda_\epsilon(A) = \{z \in \mathbb{C} : ||(zI - A)^{-1}||_2 \geq \epsilon^{-1}\}, \qquad (A.8)$$

and choose some ² > 0 so that

| $  (sI - A)^{-1}  _2 \geq \epsilon^{-1}$ | $\forall z \in \Lambda_\epsilon(A).$ | $(A.9)$ |
|------------------------------------------|--------------------------------------|---------|
|------------------------------------------|--------------------------------------|---------|

Let $^{s}$ → $^{z}$, giving

$$\max_{t>0} \|e^{At}\|_2 \geq \max_{\substack{\mathbb{R}(z)>0 \\ z \in \Lambda_e(A)}} \left( \frac{\mathbb{R}(z)}{\epsilon} \right). \quad (\text{A.10})$$

Eqn (A.10) is true for any ² > 0, therefore taking the supremum over all ² gives Kreiss' theorem:

$$\max_{t>0} \|e^{At}\|_2 \geq \sup_{\epsilon>0} \sup_{\substack{\mathbb{R}(z)>0 \\ z \in \Lambda_\epsilon(A)}} \left( \frac{\mathbb{R}(z)}{\epsilon} \right) \equiv \Gamma. \quad (\text{A.11})$$

Squaring (A.11) gives the maximum attainable energy for all times. Therefore a lower bound for the maximum attainable energy is

$$\max_{t>0} \|e^{At}\|_2^2 = \Gamma^2 \geq \left[ \sup_{\epsilon>0} \frac{\delta(\epsilon)}{\epsilon} \right]^2, \quad (\text{A.12})$$

where δ(²) is the largest distance from the imaginary axis to a point in the unstable half-plane lying within the ²-pseudospectrum contour.

## Appendix B

### Proof that Streamwise Invariance

# Leads to Decay

It can be shown that all disturbances decay to the laminar state for flows with streamwise invariance using fundamental fluid dynamics concepts; here, the discussion in [23] is followed. The material derivative, from (1.1), for streamwise invariant flows reduces to

$$\frac{D}{Dt} = \frac{\partial}{\partial t} + v \frac{\partial}{\partial y} + w \frac{\partial}{\partial z}, \quad (\text{B.1})$$

the Navier-Stokes and vorticity equations in the streamwise direction are

$$\frac{\partial u}{\partial t} + v \frac{\partial u}{\partial y} + w \frac{\partial u}{\partial z} + v \frac{\partial U}{\partial y} = \nu \left( \frac{\partial^2 u}{\partial y^2} + \frac{\partial^2 u}{\partial z^2} \right) \quad (\text{B.2})$$

$$\frac{D\omega_x}{Dt} = \nu \left( \frac{\partial^2}{\partial y^2} + \frac{\partial^2}{\partial z^2} \right) \omega_x \quad (\text{B.3})$$

where u, v, w are the velocities in their respective x, y, z directions, U is the steady laminar profile for sinusoidal shear flow and ω$^{x}$ is the vorticity, both in the streamwise direction. It is useful to note that the flow in the cross-stream direction has

decoupled from the mean flow as shown in (B.3). The continuity equation, for incompressible flows, states that the divergence in the fluctuations is zero and is given by

$$\nabla \cdot \mathbf{u} = 0.$$
 (B.4)

The energy in the cross-stream direction is defined as

$$\frac{d}{dt} \iint (v^2 + w^2) dy \, dz = 2 \iint \left( v \frac{\partial v}{\partial t} + w \frac{\partial w}{\partial t} \right) dy \, dz. \quad (\text{B.5})$$

From the Navier-Stokes equations in the y and z directions

$$\frac{\partial v}{\partial t} = \nu \left( v \frac{\partial v}{\partial t} + w \frac{\partial w}{\partial t} \right) - \frac{1}{\rho} \frac{\partial p}{\partial y}, \quad (\text{B.6})$$

$$\frac{\partial w}{\partial t} = \nu \left( v \frac{\partial v}{\partial t} + w \frac{\partial w}{\partial t} \right) - \frac{1}{\rho} \frac{\partial p}{\partial z},$$

equation (B.5) reduces to

$$\frac{d}{dt} \iint (v^2 + w^2) dy dz = 2\nu \iint v \left( \frac{\partial^2}{\partial y^2} + \frac{\partial^2}{\partial z^2} \right) v dy dz + 2\nu \iint w \left( \frac{\partial^2}{\partial y^2} + \frac{\partial^2}{\partial z^2} \right) w dy dz. \quad (\text{B.7})$$

Furthermore, suppose that

$$\int v \frac{\partial^2 v}{\partial y^2} dy = \left[ v \frac{\partial v}{\partial y} \right]_0^\infty - \int \left( \frac{\partial v}{\partial y} \right)^2 dy \quad (\text{B.8})$$

where the first term of (B.8) goes to zero, then

$$\iint v \left( \frac{\partial^2}{\partial y^2} + \frac{\partial^2}{\partial z^2} \right) v \, dy \, dz = - \iint \left[ \left( \frac{\partial v}{\partial y} \right)^2 + \left( \frac{\partial v}{\partial z} \right)^2 \right] dy \, dz. \quad (\text{B.9})$$

Applying (B.9), Eqn (B.7) may now be written as

$$\frac{d}{dt} \iint (v^2 + w^2) dy \, dz = -2\nu \iint \left[ \left( \frac{\partial v}{\partial y} \right)^2 + \left( \frac{\partial v}{\partial z} \right)^2 + \left( \frac{\partial w}{\partial y} \right)^2 + \left( \frac{\partial w}{\partial z} \right)^2 \right] dy \, dz. \quad (\text{B.10})$$

Rearranging the right-hand side in terms of vorticity, which is equivalent to the curl of the velocity, i.e.

$$\boldsymbol{\omega} = \nabla \times \mathbf{u}, \quad (\text{B.11})$$

the x-component of the vorticity is defined as

$$\omega_x = \frac{\partial w}{\partial y} - \frac{\partial v}{\partial z}. \quad (\text{B.12})$$

By squaring (B.12) and using the definition of continuity where ∂v ∂y $^{=}$ − ∂w ∂z , Eqn. (B.10) can be re-written as

$$\frac{d}{dt} \iint (v^2 + w^2) dy \, dz = -2\nu \iint \omega_x^2 dy \, dz. \quad (\text{B.13})$$

From the above, the energy in the cross-steam direction accordingly decays to zero, therefore $^{v}$ → $^{0}$ and $^{w}$ → $^{0}$ as $^{t}$ → ∞.

It can be shown that for a streamwise invariant flow, the streamwise velocity u cannot become infinite in finite time [3]. Suppose that enough time has passed so that v and w are very small; a similar argument can be made to show that u must also decay to zero, as follows. For v = w = 0, (B.2) reduces to a two-dimensional diffusion equation for u:

$$\frac{\partial u}{\partial t} = \nu \left( \frac{\partial^2 u}{\partial y^2} + \frac{\partial^2 u}{\partial z^2} \right). \quad (\text{B.14})$$

By forming the dot product of u with (B.14) and integrating, it is found that the energy in the streamwise direction is

$$\frac{d}{dt} \iint u^2 dy \, dz = 2\nu \iint \left( u \frac{\partial^2 u}{\partial y^2} + u \frac{\partial^2 u}{\partial z^2} \right) dy \, dz. \quad (\text{B.15})$$

Using (B.8) to evaluate the right-hand side, (B.15) is rearranged to

$$\frac{d}{dt} \iint u^2 dy \, dz = -2\nu \iint \left[ \left( \frac{\partial u}{\partial y} \right)^2 + \left( \frac{\partial u}{\partial z} \right)^2 \right] dy \, dz. \quad (\text{B.16})$$

Since the right hand side of (B.16) is negative provided $^{u}$ 6$^{=}$ 0, the energy in the streamwise direction monotonically decays to zero, hence $^{u}$ → $^{0}$ as $^{t}$ → ∞. Therefore, although the velocity in the streamwise direction may encounter some transient growth, it must eventually decay to zero. An analogous proof of decay, following transient energy growth, for flows with streamwise invariance is given in [14, 15].