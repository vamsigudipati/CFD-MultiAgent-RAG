## New Journal of Physics

# **A low-dimensional model for turbulent shear flows**

**Jeff Moehlis**1**, Holger Faisst**$^{2}$ **and Bruno Eckhardt**$^{2}$

$^{1}$ Department of Mechanical and Environmental Engineering,

University of California, Santa Barbara, CA 93106, USA

$^{2}$ Fachbereich Physik, Philipps-Universität Marburg, D-35032 Marburg, Germany

E-mail: [bruno.eckhardt@physik.uni-marburg.de](mailto:bruno.eckhardt@physik.uni-marburg.de)

New Journal of Physics **6** (2004) 56

Received 27 January 2004

Published 27 May 2004

Online at <http://www.njp.org/>

DOI: 10.1088/1367-2630/6/1/056

**Abstract.** We analyse a low-dimensional model for turbulent shear flows. The model is based on Fourier modes and describes sinusoidal shear flow, in which the fluid between two free-slip walls experiences a sinusoidal body force. The model contains a total of nine modes, including modes describing the basic mean velocity profile and its modification, downstream vortices, streaks, and instabilities of streaks, with other modes being a consequence of the nonlinear interactions. The transition to turbulence for the model is subcritical and intermittent, and the distributions of turbulent lifetimes are exponential, in agreement with observations in many shear flows.

# **Contents**

| 1. Introduction                           | 2  |
|-------------------------------------------|----|
| 2. Sinusoidal shear flows                 | 3  |
| 3. A low-dimensional model                | 4  |
| 4. Dynamics of the model                  | 9  |
| 4.1. Domain with Lx = 1.75 π , Lz = 1.2 π | 10 |
| 4.2. Domain with Lx = 4 π , Lz = 2 π      | 11 |
| 5. Transition behaviour                   | 13 |
| 6. Conclusions                            | 14 |
| Acknowledgments                           | 16 |
| References                                | 17 |

### **1. Introduction**

The understanding of the transition to turbulence in many flows has benefited from the analysis of simplified models. Beginning with Lorenz's numerical simulations of a three-mode caricature of thermal convection [1\], various models for convection and centrifugally unstable systems have been derived and analysed. Such models highlight different kinds of bifurcations and a wide variety of dynamical behaviour in systems with a linear instability [2\]–[\5]. However, describing the transition to turbulence in shear flows such as plane Couette flow or pipe flow has proven much more difficult: there is no linear instability around which centre manifold and other reduction techniques can be applied; moreover, numerical simulations and experiments indicate that the dynamics are spatially and temporally complicated right above the onset of turbulence [\6]–[\10].

Although there is considerable complexity in the dynamics of shear flows, there is also some simplicity. Indeed, visual inspection of direct numerical simulations [\11] and experiments in the transition region [\10, 12], proper orthogonal decomposition of the flow field [\5, 13], and results from linear stability analysis \[7], [14], [15\] all suggest that downstream vortices should play a major role. These modes drive streaks, and, as discussed perhaps most strongly by Waleffe [14, 16], the unstable modes of these streaks are recycled as downstream vortices. This suggests that it should be possible to close the dynamics of shear flow turbulence with a few modes. What makes the development of such low-dimensional models complicated is the fact that the peculiar form of the non-linearity of the Navier–Stokes equations constrains the possible interactions among modes, so that a poor choice of modes in a model can lead to trivial dynamics.

There have been several previous attempts to derive low-dimensional models for shear flow turbulence. Because of their geometric simplicity, much of this effort has been in the modelling of plane Couette flow, in which fluid is sheared between two infinite parallel no-slip walls moving at the same speed but in opposite directions, and for sinusoidal shear flow, in which fluid between two free-slip walls experiences a sinusoidal body force which gives rise to a sinusoidal laminar profile. For example, building on his analysis of linear instabilities, Waleffe proposed an eight-mode model and a further reduction to a four-mode model for sinusoidal shear flow [16\]. The dynamics of the eight-mode model were not studied in detail. For the four-mode model, the 'turbulent state'is represented as a stationary point or a periodic solution [14, 16, 17]. On the other hand, analysis of a straightforward projection of the sinusoidal shear flow equations onto a set of 19 Fourier modes gives a fluctuating turbulent state [\18]. Eliminating a residual symmetry reduces the number of degrees of freedom to nine without a change in qualitative behaviour [\19]. Different kinds of dynamical behaviour, including heteroclinic cycles, have been observed in a model for plane Couette flow derived using modes extracted from a proper orthogonal decomposition [13\].We also note that for pipe flow, Brosa and Grossmann [\20] studied a model with 42 Galerkin modes selected from the couplings between the linear eigenmodes of the Stokes problem. Finally, phenomena not unlike those observed in shear flows have also been seen in models with couplings that maintain certain characteristics of the flow, but are not derived from the Navier–Stokes equations [21\]–[23\].

The model that we present below has nine degrees of freedom. All but one of the modes are already contained in the eight-mode model proposed by Waleffe [16\], although there are small but significant modifications to some modes. The essential elements are modes for the basic mean velocity profile, the downstream vortices, the streaks, the instabilities of the streaks, and several modes that result from the advection of the previous modes by the mean profile. The key improvement on Waleffe's eight-mode model [\16] is that we include a mode for the modification of the structure of the mean velocity profile: as is well known for turbulent shear flows, the fluctuations change the mean profile, and this is described to lowest order by the new mode. In addition, unlike the modes in [\16], the variation in the shear direction in some modes is not a simple sine or cosine function, thus introducing additional couplings between the modes. As a result, we are able to capture desired aspects of shear flow turbulence with a much lower dimensional model than the 17-dimensional extension suggested in [16\].

In the present paper we focus on the dynamics of the model. The dynamical system behaviour of the model, and the analysis of the stationary states and periodic solutions and their bifurcations, will be presented in a companion paper [\24]. The outline is as follows: after general remarks in section 2 we introduce the modes, their couplings, and the equations of motion in section 3. We analyse the dynamics in the minimal flow unit, then for a wider and longer domain in sections 4.1 and 4.2, respectively. The characteristics of the transition to turbulence are studied in section 5. We conclude with a few remarks in section 6.

### **2. Sinusoidal shear flows**

We use a coordinate system with *x* pointing downstream, *y* in the direction of the shear, and *z* in the spanwise direction. The characteristic velocity *U*$^{0}$ is taken to be the laminar velocity arising due to the forcing at a distance *d/*4 from the top wall, where *d* is the distance between the walls; see (5) and (6) below. Then, non-dimensionalizing the lengths in units of *d/*2, velocities in units of *$^{U}$*0, time in units of *(d/*2*)/U*0, and pressure in units of *$^{U}$*$^{2}$ $^{0}$*ρ*, where *ρ* is the fluid density, the evolution equations are

$$\frac{\partial \mathbf{u}}{\partial t} = -(\mathbf{u} \cdot \nabla)\mathbf{u} - \nabla p + \frac{1}{Re}\nabla^2\mathbf{u} + \mathbf{F}(y), \quad (1)$$

with Reynolds number defined to be

$$Re = \frac{U_0 d}{2\nu}, \quad (2)$$

where *ν* is the kinematic viscosity. The fluid is incompressible,

$$\nabla \cdot \mathbf{u} = 0, \quad (3)$$

and there are free-slip boundary conditions at the walls at *$^{y}$* =±1, i.e.,

$$u_y|_{y=\pm 1} = 0, \quad \frac{\partial u_x}{\partial y} \Big|_{y=\pm 1} = \frac{\partial u_z}{\partial y} \Big|_{y=\pm 1} = 0. \quad (4)$$

 Finally, the flow is assumed to be periodic in the streamwise and spanwise directions, with lengths*Lx* and*Lz*, respectively. FollowingWaleffe [16\], we take the non-dimensionalized volume force to be

$$F(y) = \frac{\sqrt{2}\pi^2}{4Re} \sin(\pi y/2) \hat{e}_x, \quad (5)$$

giving the laminar profile

$$U(y) = \sqrt{2} \sin(\pi y/2) \hat{e}_x. \quad (6)$$

The laminar profile is inflectional but remains stable for all Reynolds numbers *Re* [25\]. In the following, we let *$^{α}$* = $^{2}$*π/Lx*, *$^{β}$* = *π/*2, and *$^{γ}$* = $^{2}$*π/Lz*, and denote the domain 0 *$^{x}$ Lx*, −$^{1}$ *$^{y}$* 1, 0 *$^{z}$ Lz* by .

#### **3. A low-dimensional model**

Our model is a nine-mode generalization of the eight-mode model considered in Waleffe [16\]. The additional ninth mode describes a modification to the basic mean velocity profile by the turbulence. It has wave vector *$^{k}$* = *(*0*,* $^{3}$*π/*2*,* $^{0}$*)*, to be compared with the wave vector *$^{k}$* = *(*0*, π/*2*,* $^{0}$*)* of the basic profile (6). Since, in general, if two modes with wave vectors *$^{k}$*$^{1}$ and *$^{k}$*$^{2}$ enter into *($^{u}$* ·∇*)u*, a mode with wave vector *$^{k}$*$^{1}$ $^{+}$ *$^{k}$*$^{2}$ results, generation of such a modification of the basic profile requires modes with *y*-component of their wave vector equal to *π*. Allowing such modes is the second major difference from the model of Waleffe.

The modes and wave vectors that should be included appear rather naturally, as follows. A prominent feature of shear flows is the presence of streamwise vortices. Vortices that span the entire gap have a wave vector *$^{k}$* = *(*0*, π/*2*, γ)*, as for *$^{u}$*$^{3}$ (the complete modes are given below, equations (7)–(16)). A streak, *u*2, capturing spanwise variation of the streamwise velocity, results from the advection of the basic profile *u*$^{1}$ by the vortex, and hence has wave vectors *(*0*,* $^{0}$*, γ)* and *(*0*, π, γ)*. In fact, these Fourier modes are tied together through a cos2*(πy/*2*)* = *(*1 + cos*(πy))/*2 dependence. Then, advecting the streak by the vortex gives a mode including the wave vector *(*0*,* 3*π/*2*,* 0*)*, as in the new mode *u*9. In [16\], none of the modes, including the streak, have wave vectors with *y*-component equal to *π*, and hence that model cannot produce a modification of the shape of the basic profile.

The other modes in [\16] are associated with instabilities of the streak mode, with their specific forms determined by physical and symmetry considerations. For example, the streak can develop instabilities with a component representing vortices pointing in the wall-normal direction, described by wave vectors *(*±*α,* $^{0}$*,* ±*γ)*. Because our streak mode has an additional cos$^{2}$*(πy/*2*)* dependence with respect to Waleffe's streak mode, we modify the appropriate streak instability modes *u*$^{4}$ and *u*$^{6}$ to have the same dependence. The resulting modes then couple to other modes to generate the modification to the basic profile with wave vector *(*0*,* 3*π/*2*,* 0*)*.

Finally, as in [16\], we 'pin'the spanwise and streamwise locations of the modes, which gives only one real degree of freedom for each mode. Because of the translation symmetries in the downstream and spanwise directions, there is actually no preferred location for these structures; proper accounting for these symmetries would require two or more real (or one or more complex) degrees of freedom for each mode in our model, except for *u*$^{1}$ and *u*9, thereby greatly increasing the dimensionality of our model, cf [13,] [26\]. Consideration of such an extension of the present model is deferred to future work.

With the above considerations in mind, the modes for the model are: the basic profile

$$u_1 = \begin{pmatrix} \sqrt{2} \sin(\pi y/2) \\ 0 \\ 0 \end{pmatrix}, \quad (7)$$

the streak

$$\mathbf{u}_2 = \begin{pmatrix} \frac{4}{\sqrt{3}} \cos^2(\pi y/2) \cos(\gamma z) \\ 0 \\ 0 \end{pmatrix}, \quad (8)$$

the downstream vortex

$$\mathbf{u}_3 = \frac{2}{\sqrt{4\gamma^2 + \pi^2}} \begin{pmatrix} 0 \\ 2\gamma \cos(\pi y/2) \cos(\gamma z) \\ \pi \sin(\pi y/2) \sin(\gamma z) \end{pmatrix}, \quad (9)$$

and the spanwise flows

$$\mathbf{u}_4 = \begin{pmatrix} 0 \\ 0 \\ \frac{4}{\sqrt{3}} \cos(\alpha x) \cos^2(\pi y/2) \end{pmatrix} \quad (10)$$

and

$$\mathbf{u}_5 = \begin{pmatrix} 0 \\ 0 \\ 2 \sin(\alpha x) \sin(\pi y/2) \end{pmatrix}. \quad (11)$$

Furthermore, we have the normal vortex modes

$$\mathbf{u}_6 = \frac{4\sqrt{2}}{\sqrt{3(\alpha^2 + \gamma^2)}} \begin{pmatrix} -\gamma \cos(\alpha x) \cos^2(\pi y/2) \sin(\gamma z) \\ 0 \\ \alpha \sin(\alpha x) \cos^2(\pi y/2) \cos(\gamma z) \end{pmatrix} \quad (12)$$

and

$$\mathbf{u}_7 = \frac{2\sqrt{2}}{\sqrt{\alpha^2 + \gamma^2}} \begin{pmatrix} \gamma \sin(\alpha x) \sin(\pi y/2) \sin(\gamma z) \\ 0 \\ \alpha \cos(\alpha x) \sin(\pi y/2) \cos(\gamma z) \end{pmatrix}, \quad (13)$$

generated from the advection of  $\mathbf{u}_4$  and  $\mathbf{u}_5$  by both the streak  $\mathbf{u}_2$  and the vortex  $\mathbf{u}_3$ . These interactions also give rise to a fully three-dimensional mode,

$$\mathbf{u}_8 = N_8 \begin{pmatrix} \pi \alpha \sin(\alpha x) \sin(\pi y/2) \sin(\gamma z) \\ 2(\alpha^2 + \gamma^2) \cos(\alpha x) \cos(\pi y/2) \sin(\gamma z) \\ -\pi \gamma \cos(\alpha x) \sin(\pi y/2) \cos(\gamma z) \end{pmatrix}, \quad (14)$$

**Table 1.** Matrix of couplings between the modes: *(u$^{i}$* ·∇*)u$^{j}$* with indices *$^{i}$* from the row and *j* from the column contributes to mode *k*, with *k* the entry in the matrix. Dashes indicate couplings that vanish exactly. Boldface entries indicate couplings that are absent in Waleffe's model. All pairs except for the entry (3,1) and, of course, the dashed ones, couple to higher-order Fourier modes outside the set contained in our model. The lack of coupling within this set is indicated by ∗.

| i \ j | 1 | 2    | 3   | 4     | 5   | 6    | 7 | 8 | 9 |
|-------|---|------|-----|-------|-----|------|---|---|---|
| 1     | – | –    | –   | 5     | 4   | 7    | 6 | ∗ | – |
| 2     | – | –    | –   | 6     | 7,8 | 4    | 5 | 5 | – |
| 3     | 2 | 1, 9 | –   | 7 , 8 | 6   | 5    | 4 | 4 | 2 |
| 4     | – | 6    | 7,8 | –     | –   | 2    | 3 | 3 | – |
| 5     | – | 7,8  | 6   | –     | –   | 3    | 2 | 2 | – |
| 6     | – | ∗    | 5   | ∗     | 3   | ∗    | ∗ | ∗ | – |
| 7     | – | ∗    | 4   | 3     | ∗   | ∗    | ∗ | ∗ | – |
| 8     | 6 | ∗    | 4   | 3     | ∗   | 1, 9 | ∗ | ∗ | 6 |
| 9     | – | –    | –   | 5     | 4   | 7    | 6 | ∗ | – |

with normalization constant

$$N_8 = \frac{2\sqrt{2}}{\sqrt{(\alpha^2 + \gamma^2)(4\alpha^2 + 4\gamma^2 + \pi^2)}}. \quad (15)$$

Finally, we have the new mode mentioned earlier, the modification of the basic profile

$$\mathbf{u}_9 = \begin{pmatrix} \sqrt{2} \sin(3\pi y/2) \\ 0 \\ 0 \end{pmatrix}. \quad (16)$$

The modes are orthogonal, and normalized so that

$$\iint_{\Omega} u_n \cdot u_m \, d^3x = 2(2\pi/\alpha)(2\pi/\gamma)\delta_{nm}. \quad (17)$$

Each mode individually satisfies incompressibility and free-slip boundary conditions at the walls. Note that the modes with a cos2 *πy* dependence are not pure Fourier modes, but rather superpositions of two Fourier modes. Introducing independent amplitudes for the pure modes would increase the number of equations, but also raise the risk of causing a collapse in the dynamics if the non-linear couplings between the modes are not strong enough. This issue has not been explored further.

Table 1 shows how these modes couple through the advection term to generate other modes. In the *$^{i}$*th row and *$^{j}$*th column, a dash indicates that *(u$^{i}$* ·∇*)u$^{j}$* vanishes exactly, an entry *$^{k}$* indicates a contribution to mode *k* since

$$\iint_{\Omega} (\mathbf{u}_i \cdot \nabla) \mathbf{u}_j \cdot \mathbf{u}_k \, d^3x \neq 0, \quad (18)$$

and ∗ indicates that *(u$^{i}$* ·∇*)u$^{j}$* has only a non-trivial projection to modes outside the set contained in our model. Bold entries are couplings that are not contained in Waleffe's eightmode model [16\]. The asymmetry in the couplings indicates that sometimes one mode advects

another but not vice versa, i.e., *(u$^{i}$* ·∇*)u$^{j}$* can be different from *(u$^{j}$* ·∇*)ui*. Ordinary differential equations are obtained by Galerkin projection \[5], [16\], i.e. by plugging the ansatz

---

$$u(\mathbf{x}, t) = \sum_m a_m(t) \mathbf{u}_m(\mathbf{x}) \tag{19}$$

with real amplitudes *am* into (1), multiplying by *un(x)*, integrating over , and using (17). This gives

$$\begin{aligned} \left(\frac{8\pi^2}{\alpha\gamma}\right) \dot{a}_n &= -\sum_{m,l} a_m a_l \int \int \int_{\Omega} [(\mathbf{u}_m \cdot \nabla) \mathbf{u}_l] \cdot \mathbf{u}_n \, d^3x \\ &+ \frac{1}{Re} \sum_m a_m \int \int \int_{\Omega} (\nabla^2 \mathbf{u}_m) \cdot \mathbf{u}_n \, d^3x \\ &+ \int \int_{\Omega} \mathbf{F} \cdot \mathbf{u}_n \, d^3x. \end{aligned} \quad (20)$$

The pressure term makes no contribution here because the modes are divergence-free, their *y*-component vanishes at the walls, and they satisfy periodic boundary conditions in *x* and *z*, cf [\5]. For our choice of modes, we obtain the amplitude equations

$$\frac{da_1}{dt} = \frac{\beta^2}{Re} - \frac{\beta^2}{Re}a_1 - \sqrt{\frac{3}{2}} \frac{\beta\gamma}{\kappa_{\alpha\beta\gamma}}a_6a_8 + \sqrt{\frac{3}{2}} \frac{\beta\gamma}{\kappa_{\beta\gamma}}a_2a_3, \quad (21)$$

$$\frac{da_2}{dt} = - \left( \frac{4\beta^2}{3} + \gamma^2 \right) \frac{a_2}{Re} + \frac{5\sqrt{2}}{3\sqrt{3}} \frac{\gamma^2}{\kappa_{\alpha\gamma}} a_4 a_6 - \frac{\gamma^2}{\sqrt{6}\kappa_{\alpha\gamma}} a_5 a_7 \\ - \frac{\alpha\beta\gamma}{\sqrt{6}\kappa_{\alpha\gamma}\kappa_{\alpha\beta\gamma}} a_5 a_8 - \sqrt{\frac{3}{2}} \frac{\beta\gamma}{\kappa_{\beta\gamma}} a_1 a_3 - \sqrt{\frac{3}{2}} \frac{\beta\gamma}{\kappa_{\beta\gamma}} a_3 a_9, \quad (22)$$

$$\frac{da_3}{dt} = -\frac{\beta^2 + \gamma^2}{Re} a_3 + \frac{2}{\sqrt{6}} \frac{\alpha \beta \gamma}{\kappa_{\alpha \gamma} \kappa_{\beta \gamma}} (a_4 a_7 + a_5 a_6) + \frac{\beta^2 (3\alpha^2 + \gamma^2) - 3\gamma^2(\alpha^2 + \gamma^2)}{\sqrt{6} \kappa_{\alpha \gamma} \kappa_{\beta \gamma} \kappa_{\alpha \beta \gamma}} a_4 a_8, \quad (23)$$

$$\frac{da_4}{dt} = -\frac{3\alpha^2 + 4\beta^2}{3Re} a_4 - \frac{\alpha}{\sqrt{6}} a_1 a_5 - \frac{10}{3\sqrt{6}} \frac{\alpha^2}{\kappa_{\alpha\gamma}} a_2 a_6$$

$$-\sqrt{\frac{3}{2}} \frac{\alpha\beta\gamma}{\kappa_{\alpha\gamma}\kappa_{\beta\gamma}} a_3 a_7 - \sqrt{\frac{3}{2}} \frac{\alpha^2\beta^2}{\kappa_{\alpha\gamma}\kappa_{\beta\gamma}\kappa_{\alpha\beta\gamma}} a_3 a_8 - \frac{\alpha}{\sqrt{6}} a_5 a_9, \quad (24)$$

$$\frac{da_5}{dt} = -\frac{\alpha^2 + \beta^2}{Re} a_5 + \frac{\alpha}{\sqrt{6}} a_1 a_4 + \frac{\alpha^2}{\sqrt{6} \kappa_{\alpha\gamma}} a_2 a_7 - \frac{\alpha \beta \gamma}{\sqrt{6} \kappa_{\alpha\gamma} \kappa_{\alpha\beta\gamma}} a_2 a_8 + \frac{\alpha}{\sqrt{6}} a_4 a_9 + \frac{2}{\sqrt{6}} \frac{\alpha \beta \gamma}{\kappa_{\alpha\gamma} \kappa_{\beta\gamma}} a_3 a_6, \quad (25)$$

$$\begin{aligned} \frac{da_6}{dt} &= -\frac{3\alpha^2 + 4\beta^2 + 3\gamma^2}{3Re}a_6 + \frac{\alpha}{\sqrt{6}}a_1a_7 + \sqrt{\frac{3}{2}}\frac{\beta\gamma}{\kappa_{\alpha\beta\gamma}}a_1a_8 \\ &+ \frac{10}{3\sqrt{6}}\frac{\alpha^2 - \gamma^2}{\kappa_{\alpha\gamma}}a_2a_4 - 2\sqrt{\frac{2}{3}}\frac{\alpha\beta\gamma}{\kappa_{\alpha\gamma}\kappa_{\beta\gamma}}a_3a_5 + \frac{\alpha}{\sqrt{6}}a_7a_9 + \sqrt{\frac{3}{2}}\frac{\beta\gamma}{\kappa_{\alpha\beta\gamma}}a_8a_9, \end{aligned} \quad (26)$$

$$\frac{da_7}{dt} = -\frac{\alpha^2 + \beta^2 + \gamma^2}{Re} a_7 - \frac{\alpha}{\sqrt{6}} (a_1 a_6 + a_6 a_9) + \frac{1}{\sqrt{6}} \frac{\gamma^2 - \alpha^2}{k_{\alpha\gamma}} a_2 a_5 + \frac{1}{\sqrt{6}} \frac{\alpha \beta \gamma}{k_{\alpha\gamma} k_{\beta\gamma}} a_3 a_4, \quad (27)$$

$$\frac{da_8}{dt} = -\frac{\alpha^2 + \beta^2 + \gamma^2}{Re} a_8 + \frac{2}{\sqrt{6}} \frac{\alpha \beta \gamma}{\kappa_{\alpha\gamma} \kappa_{\alpha\beta\gamma}} a_2 a_5 + \frac{\gamma^2 (3\alpha^2 - \beta^2 + 3\gamma^2)}{\sqrt{6} \kappa_{\alpha\gamma} \kappa_{\beta\gamma} \kappa_{\alpha\beta\gamma}} a_3 a_4, \quad (28)$$

$$\frac{da_9}{dt} = -\frac{9\beta^2}{Re}a_9 + \sqrt{\frac{3}{2}}\frac{\beta\gamma}{\kappa_{\beta\gamma}}a_2a_3 - \sqrt{\frac{3}{2}}\frac{\beta\gamma}{\kappa_{\alpha\beta\gamma}}a_6a_8, \quad (29)$$

where

$$\kappa_{\alpha\gamma} = \sqrt{\alpha^2 + \gamma^2}, \quad (30)$$

$$\kappa_{\beta\gamma} = \sqrt{\beta^2 + \gamma^2}, \quad (31)$$

$$\kappa_{\alpha\beta\gamma} = \sqrt{\alpha^2 + \beta^2 + \gamma^2}. \quad (32)$$

These equations have a strong similarity to Waleffe's eight-mode model [16\], but because some modes differ there are different O*(*1*)* factors multiplying some terms, and several additional terms, including all terms that contain *$^{a}$*9. While the numerical factors can be expected to play a minor role for the qualitative behaviour, all couplings seem to be significant. For example, for Waleffe's eight-mode model we have been unable to locate any unstable, stationary finite amplitude coherent structures consisting of streamwise vortices and streaks, as have been found numerically for shear flows such as plane Couette flow \[27], [28\]. On the other hand, for our nine-mode model, with its additional couplings, we do find such solutions: see figure 1.

The laminar state corresponds to the fixed point with *$^{a}$*$^{1}$ = 1, and *$^{a}$*$^{2}$ =···= *$^{a}$*$^{9}$ = 0, which is linearly stable for all *Re*. In the next section, we will see that turbulence exists for the model despite the stability of the laminar state: the model thus captures the subcritical nature of the transition to turbulence.

![](_page_8_Figure_2.jpeg)

**Figure 1.** Unstable, stationary finite amplitude coherent structures at lowest *Re* for which they exist for domains of size *Lx* = $^{4}$*π*, *Lz* = $^{2}$*π*, for (a) full equations describing plane Couette flow (*Re* = 125), and (b) our model for sinusoidal shear flow (*Re* = 308). The three panels show the mean profile (left), the downstream vortices (upper right) and the flow in the midplane between the plates (lower right). For the vortices, the flow is averaged in the downstream direction. The velocity fields are represented by vectors for the components shown in the plane and by colours for the velocity perpendicular to the plane. The solid lines in the lower right panel indicate zero contours of the *x*-velocity. To aid in comparing these flows with different boundary conditions, in the upper right panel in (a) we subtract off the laminar profile, while in (b) we subtract off the component of the flow proportional to the laminar profile.

### **4. Dynamics of the model**

In [\11], plane Couette flow is considered for a minimal flow unit, the smallest domain which is numerically found to sustain turbulence. It elucidates a 'self-sustaining process' in which streamwise vortices cause streak formation, then the streaks break down to give

![](_page_9_Figure_2.jpeg)

**Figure 2.** Dynamics of the model with *Re* = 400 for *Lx* = $^{1}$*.*75*π, Lz* = $^{1}$*.*2*π*. The three panels are as for figure 1, except that in the upper right panel the colour indicates the full averaged downstream velocity, i.e., the component proportional to the laminar profile is included. The frame shown is from the accompanying [animation.](http://www.iop.org/EJ/mmedia/1367-2630/6/1/056/MFU.mpg)

*x*-dependent flow, then the streamwise vortices regenerate and the process repeats. It has been suggested that such a self-sustaining process is a universal characteristic of shear flow turbulence [11, 16, 29, 30]. In section 4.1, we analyse the model in the highly constrained geometry of a minimal flow unit.

On the other hand, the analysis of Nagata [27\] and Busse and Clever \[28\] for the optimal domain size for the formation of stationary coherent structures suggests considering a longer and wider domain. The dynamics for that domain are given in section 4.2.

#### 4.1. Domain with $$L_x = 1.75\pi$$ , $L_z = 1.2\pi$

We first consider a flow domain with *Lx* = $^{1}$*.*75*$^{π}$* and *Lz* = $^{1}$*.*2*π*. For plane Couette flow, this corresponds to the minimal flow unit, the smallest domain which is found numerically to sustain turbulence [\11]. Previous models for shear flows for this domain size include [26\] for plane Couette flow. See also [31\] for a discussion of models for minimal flow unit channel flow.

The dynamics for the model at *Re* = 400 are shown in figure 2. The movie clearly shows the following series of events: if we start with a vortex (indicated in the upper right panel by the arrows for the velocity field in the plane), the formation of a streak can be observed next (indicated by the colours for the downstream component). The streak then goes unstable by the sinusoidal mode that is the basic instability kept for the model \[16\]: it shows up prominently in the midplane cross section of the velocity field. The sinusoidal modulation grows, breaks up into patches and rearranges with the regions of vertical motions shifted by half a wave length: the consequences for the vortices are that they disappear and then reform with a reversed sense of rotation.

Figure 3 shows the timeseries for all nine amplitudes in the model for the solution shown in figure 2. The fluctuations are compatible with a non-periodic, irregular turbulent state. However,

![](_page_10_Figure_2.jpeg)

**Figure 3.** The amplitudes for a typical chaotic transient for the domain of size *Lx* = $^{1}$*.*75*$^{π}$* and *Lz* = $^{1}$*.*2*π*, and Reynolds number *Re* = 400. This corresponds to the solution shown in figure 2 and the associated movie.

the eventual decay to the laminar state shows it does not belong to a turbulent attractor but rather to a transient state on a chaotic saddle. Notice that the amplitude of *$^{a}$*$^{1}$ becomes large near *$^{t}$* ≈ 1600, indicating an attempt to leave the turbulent state and to relax to the laminar one. However, the conditions for relaxation to the laminar state are not only that *$^{a}$*$^{1}$ has to become large, but also that the other modes have to be small, which is not satisfied until *$^{t}$* ≈ 2600 when the trajectory finally escapes the turbulent region.

# *4.2. Domain with Lx* = *$^{4}$π, Lz* = *$^{2}$$^{π}$*

#### 4.2. Domain with $$L_x = 4\pi, L_z = 2\pi$$

The moderately longer and wider domain with *Lx* = $^{4}$*$^{π}$* and *Lz* = $^{2}$*$^{π}$* has been considered in many previous studies of shear flow turbulence, including plane Couette flow [13, 19, 27, 28] and sinusoidal shear flow [19\]. This corresponds to an optimal domain size for plane Couette flow in the sense that the steady finite amplitude solutions appear at the smallest value of *Re* [28,] [32\].

The dynamics in the wider domain is similar to that for the smaller one, but perhaps a bit more violent. The reversals of the vortices are still present, but the dynamics of the sinusoidal instability in the midplane representation is less regular. In a full numerical simulation, more modes would be present and the variations in space and time can be expected to be even more irregular.

The timeseries for all the nine amplitudes in the model for the solution shown in figure 4 are displayed in figure 5. As for the minimal flow unit domain, the fluctuations are compatible

![](_page_11_Figure_2.jpeg)

**Figure 4.** Dynamics of the model with *Re* = 400 for the aspect ratio *Lx* = $^{4}$*π*, *Lz* = $^{2}$*π*. The panels and the representation of the flow are the same as in figure 2. The frame shown is from the accompanying [animation.](http://www.iop.org/EJ/mmedia/1367-2630/6/1/056/NBC.mpg)

![](_page_11_Figure_4.jpeg)

**Figure 5.** The amplitudes for a typical chaotic transient for a domain of size *Lx* = $^{4}$*$^{π}$* and *Lz* = $^{2}$*π*, and Reynolds number *Re* = 400, and it corresponds to the solution shown in figure 4 and the associated movie.

with a non-periodic, irregular, transient turbulent state. Notice that the amplitude of *$^{a}$*$^{1}$ becomes large several times, indicating an attempt to leave the turbulent state and to relax to the laminar one, e.g. near the times *$^{t}$* = 800, 2700, 4500, 7800 and, most clearly, near *$^{t}$* = 6500, where it almost succeeds. Finally, near *$^{t}$* = 10 000 the flow laminarizes.

![](_page_12_Figure_2.jpeg)

**Figure 6.** Colour-coded lifetimes of perturbations in the minimal flow unit for different values of *Re* and the initial energy. Integrations were only carried out up to *$^{t}$* = 1000.

### **5. Transition behaviour**

The finite lifetime of the trajectories for our model shown in the previous section indicates that the turbulent state is not an attractor. Similar behaviour has been seen in the other shear flows without a linear instability, and it has been suggested that the turbulent state is a chaotic saddle [9, 18, 33]. The typical characteristic of a chaotic saddle is an exponential lifetime distribution [34\]–[36\] that has also been seen in experiments and simulations [9, 37].

For low values of the Reynolds number *Re*, the model shows an apparent fractal dependence of lifetimes on *Re* and on initial energy *E* of a perturbation (figure 6). Here initial conditions are chosen so that *$^{a}$*$^{2}$ $^{=}$ *$^{a}$*$^{3}$ $^{=}$ *$^{a}$*$^{4}$ $^{=}$ *$^{a}$*$^{5}$ $^{=}$ $^{√}$*$^{E}$* $^{−}$ $^{1}$*/*2, *$^{a}$*$^{1}$ $^{=}$ *$^{a}$*$^{6}$ $^{=}$ *$^{a}$*$^{7}$ $^{=}$ *$^{a}$*$^{8}$ $^{=}$ *$^{a}$*$^{9}$ $^{=}$ 0.

The strong variations of the lifetime with initial conditions suggests a probabilistic description, e.g. the study of the survival probability *P(t)* to be still turbulent after a time *t*. For the determination of *P(t)* for a set of Reynolds numbers we used ensembles of 1000 randomly selected initial conditions on an energy shell *$^{i}$ $^{a}$*$^{2}$ *$^{i}$* = $^{0}$*.*3 that were integrated for a maximum time of 10 000 units. The results in figure 7 support an exponential lifetime distribution, with a characteristic mean lifetime that increases rapidly with Reynolds number. However, for *Re >* 320 we have clear deviations from exponential decay. They appear first for long lifetimes, but set in earlier for increasing Reynolds number. The simplest explanation for this change is that a stable attractor appears and absorbs a finite fraction of initial conditions. Analysis of the periodic orbits in the system indeed shows this to be the case [24].

![](_page_13_Figure_2.jpeg)

**Figure 7.** Lifetime distributions for the model in the minimal flow unit and different values of *Re*. The red lines show exponential fits to the distributions.

The lifetime distributions for the longer and wider domain with *Lx* = $^{4}$*$^{π}$* and *Lz* = $^{2}$*$^{π}$* are shown in figure 8; initial conditions are specified as for figure 6. The cuts at fixed Reynolds number in figure 9 and the successive magnifications in figure 8 indicate how strongly the lifetimes vary under tiny variations in parameters and how sensitively the system responds to changes in initial conditions. Survival probabilities for the larger domain are shown in figure 10. An exponential form is a good representation of the data for all Reynolds numbers. There does not seem to be a co-existing non-trivial stable state, as there was for the minimal flow unit, cf [\24].

For both geometries, the median lifetimes increase rapidly with Reynolds number, perhaps exponentially, as indicated in figure 11. A rapid increase of lifetimes has also been observed in experiments [9,] [10\], numerical simulations [37,] [38\] and in other models for spatially extended systems [36,] [39\].

# **6. Conclusions**

The calculations and simulations show that nine judiciously chosen modes can capture the dynamics of vortices and streaks in turbulent shear flows. Interactions between the modes are sufficient to keep the dynamics alive and non-periodic, as expected for a turbulent flow. For a wide range of parameters, the turbulent states do not persist indefinitely, but decay after a while. The survival probability is exponential, as expected for a chaotic saddle. The appearance of an attracting state in the minimal flow unit for large Reynolds numbers shows that a transition to an attractor is possible, but this depends on the domain size and most likely also on the number of modes included.

The model captures the dynamics of vortices and shows characteristics of the self-sustaining process elucidated in [11,] [16\]. As suggested there, the cycle closes and the instability of the streaks drives modes that can be recycled to form vortices, thus completing the self-sustaining regeneration cycle.

![](_page_14_Figure_2.jpeg)

**Figure 8.** Lifetimes versus initial energy and Reynolds number for *Lx* = $^{4}$*π*, and *Lz* = $^{2}$*π*. Integrations were only carried out up to *$^{t}$* = 1500. The other frames show successive magnifications of the small domains indicated by rectangles.

![](_page_14_Figure_4.jpeg)

**Figure 9.** Lifetimes for *Lx* = $^{4}$*π, Lz* = $^{2}$*π*, for the three Reynolds numbers *Re* = 50, 80 and 100 and different initial energies, with initial conditions as described in the text.

![](_page_15_Figure_2.jpeg)

**Figure 10.** Lifetime distributions for our model with domain size *Lx* = $^{4}$*π*, *Lz* = $^{2}$*$^{π}$* and different values of *Re*. The red lines show exponential fits to the distributions.

![](_page_15_Figure_4.jpeg)

**Figure 11.** Median lifetime as a function of Reynolds number for the two domains studied here; ×, the larger domain; + , the minimal flow unit. Straight lines show exponential fits.

Even the Reynolds number at which long-lived turbulence is found to be present is not too different from that found in full numerical simulations. For the free-slip boundary conditions, a critical Reynolds number of about 130 has been found in [40\]. As can be expected for the more flexible free-slip boundary conditions, it is about 2/5 of the values for the transition in plane Couette flow [\19, 37]. That it is so close to the value we find here must be considered fortuitous, since experiments with other low-dimensional models show wide variations in behaviour under changes in the number and characteristics of modes kept.

### **Acknowledgments**

### **References**

[1] Lorenz E N 1963 *J. Atmos. Sci.* **20** 130 [2] Cross M C and Hohenberg P C 1993 *Rev. Mod. Phys.* **65** 851 [3] Guckenheimer J and Holmes P 1983 *Nonlinear Oscillations, Dynamical Systems, and Bifurcations of Vector Fields* (New York: Springer) [4] Golubitsky M, Stewart I and Schaeffer D G 1988 *Singularities and Groups in Bifurcation Theory* vol II (New York: Springer) [5] Holmes P, Lumley J L and Berkooz G 1996 *Turbulence, Coherent Structures, Dynamical Systems and Symmetry* (Cambridge: Cambridge University Press) [6] Grossmann S 2000 *Rev. Mod. Phys.* **72** 603 [7] Schmid P J and Henningson D S 1999 *Stability and Transition of Shear Flows* (New York: Springer) [8] Tillmark N and Alfredsson P H 1992 *J. Fluid Mech.* **235** 89 [9] Bottin S and Chat´e H 1998 *Eur. Phys. J.* B **6** 143 [10] Bottin S, Daviaud F, Manneville P and Dauchot O 1998 *Europhys. Lett.* **43** 171 [11] Hamilton J M, Kim J and Waleffe F 1995 *J. Fluid Mech.* **287** 317 [12] Dauchot O and Daviaud F 1995 *Phys. Fluids* **7** 335 [13] Moehlis J, Smith T R, Holmes P and Faisst H 2002 *Phys. Fluids* **14** 2493 [14] Waleffe F 1995 *Phys. Fluids* **7** 3060 [15] Chapman S J 2002 *J. Fluid Mech.* **451** 35 [16] Waleffe F 1997 *Phys. Fluids* **9** 883 [17] Dauchot O and Vioujard N 2000 *Eur. Phys. J.* B **14** 377 [18] Eckhardt B and Mersmann A 1999 *Phys. Rev.* E **60** 509 [19] Schmiegel A 1999 *PhD Thesis* Philipps-Universität Marburg [20] Brosa U and Grossmann S 1999 *Eur. Phys. J.* B **9** 343 [21] Trefethen L N, Trefethen A E, Reddy S C and Driscoll T A 1993 *Science* **261** 578 [22] Baggett J S and Trefethen L N 1997 *Phys. Fluids* **9** 1043 [23] Gebhardt T and Grossmann S 1994 *Phys. Rev.* E **50** 3705 [24] Moehlis J, Faisst H and Eckhardt B 2004 *SIAM J. Appl. Dyn. Syst.* submitted [25] Drazin P G and Reid W H 1981 *Hydrodynamic Stability* (Cambridge: Cambridge University Press) [26] Smith T R, Moehlis J and Holmes P 2004 submitted for publication [27] Nagata M 1990 *J. Fluid Mech.* **217** 519 [28] Clever R M and Busse F H 1997 *J. Fluid Mech.* **344** 137 [29] Reddy S C, Schmid P J, Baggett J S and Henningson D S 1998 *J. Fluid Mech.* **365** 269 [30] Jim´enez J and Pinelli A 1999 *J. Fluid Mech.* **389** 335 [31] Podvin B and Lumley J 1998 *J. Fluid Mech.* **362** 121 [32] Waleffe F 2003 *Phys. Fluids* **15** 1517 [33] Schmiegel A and Eckhardt B 1997 *Phys. Rev. Lett.* **79** 5250 [34] Grebogi C, Ott E and Yorke J A 1983 *Physica* D **7** 181 [35] Kantz H and Grassberger P 1985 *Physica* D **17** 75 [36] T´el T 1991 *Directions in Chaos* vol 3, ed H Bai-Lin, D H Feng and J M Yuan (Singapore: World Scientific) p 149 [37] Eckhardt B, Faisst H, Schmiegel A and Schumacher J 2002 *Advances in Turbulence IX* ed I P Castro, P E Hanock and T G Thomas (Barcelona: CIMNE) p 701 [38] Faisst H and Eckhardt B 2004 *J. Fluid Mech.* **504** 343 [39] Crutchfield J P and Kaneko K 1988 *Phys. Rev. Lett.* **60** 2715 [40] Schumacher J and Eckhardt B 2001 *Phys. Rev.* E **63** 046307