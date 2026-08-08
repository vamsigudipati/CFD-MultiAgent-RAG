![](_page_0_Picture_0.jpeg)

**PAPER • OPEN ACCESS**

## Enhancement of PIV measurements via physicsinformed neural networks

To cite this article: Gazi Hasanuzzaman et al 2023 Meas. Sci. Technol. 34 044002

View the article online for updates and enhancements.

### You may also like

Stochastic particle advection velocimetry (SPAV): theory, simulations, and proof-ofconcept experiments Ke Zhou, Jiaqi Li, Jiarong Hong et al. -

Polynomial differentiation decreases the training time complexity of physicsinformed neural networks and strengthens their approximation power Juan-Esteban Suarez Cardona and Michael Hecht -

Spectrally adapted physics-informed neural networks for solving unbounded domain problems Mingtao Xia, Lucas Böttcher and Tom Chou -

# **Enhancement of PIV measurements via physics-informed neural networks**

**Gazi Hasanuzzaman**1,*∗* **, Hamidreza Eivazi**$^{2}$ **, Sebastian Merbold**$^{1}$ **, Christoph Egbers**$^{1}$ **and Ricardo Vinuesa**2,*∗*

$^{1}$ Department of Aerodynamics and Fluid Mechanics, Brandenburg University of Technology, Cottbus-Senftenberg, Germany

$^{2}$ FLOW, Engineering Mechanics, KTH Royal Institute of Technology, Stockholm, Sweden

E-mail: gazihasanuzzaman.me@live.com and rvinuesa@mech.kth.se

Received 2 June 2022, revised 24 November 2022

![](_page_1_Picture_11.jpeg)

Accepted for publication 8 December 2022

Published 3 January 2023

#### **Abstract**

Physics-informed neural networks (PINN) are machine-learning methods that have been proved to be very successful and effective for solving governing equations of fluid flow. In this work we develop a robust and efficient model within this framework and apply it to a series of two-dimensional three-component stereo particle-image velocimetry (PIV) datasets, to reconstruct the mean velocity field and correct measurements errors in the data. Within this framework, the PINNs-based model solves the Reynolds-averaged-Navier–Stokes equations for zero-pressure-gradient turbulent boundary layer (ZPGTBL) without a prior assumption and only taking the data at the PIV domain boundaries. The turbulent boundary layer (TBL) data has different flow conditions upstream of the measurement location due to the effect of an applied flow control via uniform blowing. The developed PINN model is very robust, adaptable and independent of the upstream flow conditions due to different rates of wall-normal blowing while predicting the mean velocity quantities simultaneously. Hence, this approach enables improving the mean-flow quantities by reducing errors in the PIV data. For comparison, a similar analysis has been applied to numerical data obtained from a spatially-developing ZPGTBL and an adverse-pressure-gradient TBL over a NACA4412 airfoil geometry. The PINNs-predicted results have less than 1% error in the streamwise velocity and are in excellent agreement with the reference data. This shows that PINNs has potential applicability to shear-driven turbulent flows with different flow histories, which includes experiments and numerical simulations for predicting high-fidelity data.

Keywords: deep learning, physics-informed neural networks, particle image velocimetry, turbulence, flow control

(Some figures may appear in colour only in the online journal)

Original Content from this work may be used under the terms of the Creative Commons Attribution 4.0 licence. Any further distribution of this work must maintain attribution to the author(s) and the title of the work, journal citation and DOI.

*$^{*}$* Authors to whom any correspondence should be addressed.

#### **1. Introduction**

Measurement of spatio-temporal velocity data is crucial for the study of fluid dynamics. Experimentally, this is commonly done with intrusive/non-intrusive measurements of flow quantities such as velocity and pressure. On the other hand, numerical simulations enables integrating the governing equations of the flow with appropriate initial and boundary conditions (BCs). Unfortunately, it is quite challenging to obtain measurements with very detailed spatio-temporal accuracy.

Particle-image-velocimetry (PIV) is a well-known measurement technique in the field of experimental fluid mechanics and aerodynamics [17]. This is a non-intrusive optical method that is used to obtain quantitative spatio-temporal flow velocity data. To this end, a laser-illuminated light sheet and one or more cameras are used for imaging, and the fluid is previously seeded. Different camera arrangements are applied to obtain various flow fields with limited/all velocity components such as 2D2C (classical PIV), 2D3C (stereo PIV) and 3D3C (volumetric/tomographic PIV) velocity components [30]. PIV offers technical flexibility that can be adapted to versatile fluidflow experiments and hence, accurate velocity data over a considerable large experimental domain can be achieved. In case of a complex geometry, where the gradient of the streamwise velocity is sufficiently large and the PIV application suffers from blind spots, Navier–Stokes simulations are also applied on the PIV data known as 'gappy PIV' [18].

Although PIV is widely used to measure shear-driven turbulent flows, the turbulent boundary layer (TBL) is a prominent case which can be quite challenging in terms of effective and optimized measurements. TBLs exhibit complex interactions of turbulent structures with different spatial scales ranging from the viscous length scale (*l* $^{+}$ = *ν/$u_\tau$* , where *ν* and *$u_\tau$* indicate kinematic viscosity and friction velocity respectively) to several boundary-layer thicknesses (*δ*). Considering the complex and three-dimensional nature of a TBL, appropriate measurement techniques such as PIV are very effective in order to resolve all scales. Note that here we will consider incompressible flow with Newtonian fluid.

The PIV peak-detection algorithm uses displacement of illuminated particles comparing image pairs separated by a certain time delay. Subsequently, the spatial displacement of the seeded particles is interpreted as the velocity vector map. Due to uniform time delay between image pairs, considerable spatial difference is observed for particle displacement from the near-wall region to the outer layer. This provides higher uncertainty for the near-wall data when the graduallydecreasing-interrogation-window feature is adopted within the image-processing algorithm. Considerable effort is dedicated to measuring the smallest scales together with the large ones within the same magnification.

Wall-shear stress plays an important role in the analysis of TBL data, not only when it comes to scaling the mean profile but also for quantify the role of skin friction in TBL-control experiments [9]. Traditionally, the determination of wall-shear stress through direct measurement was mostly based on direct

oil-film interferometry (OFI) [21], surface hot-film interferometry (SHFA) [31] or non-intrusive laser-doppler anemometry (LDA) [13]. Application of another measurement technique only to infer wall-shear data in conjunction with PIV is often not possible depending on the experimental setup. Note that despite the extensive experimental work on flow control of TBLs, a number of numerical studies have been recently published, with focus on flat-plate [14] and also wing TBLs [1, 2].

The non-intrusive, instantaneous/mean acquisition of wallshear stress (*τw*) was made possible with the advent of high-magnification PIV/profile PIV [28, 29]. Although this approach has the potential of accurately measuring the wallshear data but strongly depends on the high resolution of magnification within the viscous sub-layer and high seeding density. Often the wall BCs of the TBL are modified due to control experiments, which strongly influence the particle distribution in the viscous sub-layer. Eventually this problem limits the application of high-magnification PIV within the near-wall region. Under such circumstances, OFI or SHFA remain as the only choices to measure the wall-shear stress. If the measurement matrix has a large parameter space, measurement of the wall-shear stress becomes challenging. Moreover, it is a common practice to apply other measurement techniques for the near-wall region besides PIV in order to cover the entire TBL, thus increasing measurement costs and requiring tedious effort.

Note that accurately measuring the near-wall data is often not practical with classical PIV. This is due to spurious data from the near-wall region due to unavoidable laser reflection from the wall. A reduction of the boundary-layer thickness (*δ*) makes these near-wall measurements even more challenging a consequence of increased flow velocity [13]. Consequently, all these issues limit the capacity of classical PIV approaches such as 2D2C and 2D3C (to some extent all other PIV approaches) to accurately measure near-wall data.

Spatially-developing TBLs offer the possibility for control experiments at high Reynolds numbers, mostly intended to reduce friction drag. The upstream flow can be modified in order to influence the downstream flow. The effect of the modified BC on the friction parameters and TBL properties are studied through modification of turbulent structures and statistical quantities. Particularly, uniform blowing is an effective active-flow-control technique that extend its influence on the flow statistics far downstream. Due to its additional mass flux from a different source, seeding the near-wall region is often difficult for the purpose of PIV study. Moreover, spatiallydeveloping TBLs are intentionally set up in such a way that the boundary layer is thick and therefore, smallest scales are large enough to resolve while using PIV. Such thick boundary layers require large-field PIV measurements which employ multiple cameras overlapping in their field of view (FoV). During post processing of these overlapping double-frame images, the frames are reconstructed into a single vector field after arithmetic averaging, and hence, their difference due to varying projection angle of each cameras produces an error. Usually, this error is minimized through statistically analyzing a

![](_page_3_Figure_2.jpeg)

**Figure 1.** Convergence of the mean streamwise (*U*), wall-normal (*V*) velocity and the Reynolds shear stress *uv* as a function of the number of samples for the XYU10S case: *$^{U}$$^{∞}$* $^{=}$ $^{3}$ m s*−*$^{1}$ and *$Re_\theta$* $^{=}$ 7500, at streamwise location, *$^{x}$* $^{=}$ 19.063 m (*x/δ ≈* $^{79}$*.*13) and wall normal-location, *$^{y}$* $^{=}$ 0.0204 m (*y/δ ≈* $^{0}$*.*085).

large number of vector fields. Although large quantities such as the mean streamwise velocity component (*U*) reaches a good convergence after averaging large number of temporal vectors fields, smaller quantities such as the mean wall-normal velocity (*V*) and the mean spanwise velocity (*W*) suffer from considerable amount of convergence error. Note that the latter should be statistically zero in canonical ZPGTBLs. Moreover, acquisition and processing time overburden the experimental cost due to handling large number of temporal vector fields.

Hasanuzzaman *et al* [10] investigated uniform-blowing effects in ZPGTBL at moderately-high Reynolds numbers based on momentum thickness: *$Re_\theta$* $^{=}$ *$^{U}$∞θ/ν* $^{=}$ 7500– 19 763, where *$^{U}$∞* and *$^{\theta}$* represent free stream velocity and momentum thickness, respectively. Uniform blowing was applied at an upstream location and the measurement was conducted immediately after. PIV measurement was conducted using the stereo arrangement and each set of acquisition contains 10$^{4}$ vector fields in time for all quantities. Figure 1 presents the convergence of *U*, *V* and *uv* (which is the Reynolds shear stress) from stereo PIV measurements obtained for *Reθ,*SBL $^{=}$ 7500, *$^{U}$∞* $^{=}$ $^{3}$*.*$^{1}$ m s*−*$^{1}$ . This result was obtained from temporal-sliding averages of 10 000 streamwise, wallnormal velocity and Reynolds shear stress samples. In addition to the convergence problem and the large vector fields, resolving all scales simultaneously within one magnification was a challenging and time consuming task, both from imageprocessing and experimental-setup points of view.

Time-resolved PIV (TRPIV) measurements are typical for the study of coherent-structure dynamics, as presented e.g. in [11]. Their stereo PIV was applied to a vertical plane within a boundary layer with uniform blowing. To resolve all scales in a single magnification, high-resolution images at high acquisition rate (3200 images in 3.2 s) were acquired. This is a memory-intensive measurement procedure and the camera cache limits the total number of images during a single acquisition. Therefore, coarse measurements with less camera resolution can increase the total number of images. For high-speed flows, classical, low-speed PIV is still the only choice.

The discussion above on the common problems for PIV measurements can be summarized as: (a) PIV suffers from convergence of mean velocities even with high numbers of samples; (b) reaching the near-wall region (specifically the viscous sub-layer) with regular PIV is challenging due to reflections from the wall; (c) control experiments in TBL geometry suffers from insufficient seeding density near the wall; and finally (d) in order to resolve all scales of the flow field with TRPIV, the total number of images high resolution is needed.

On the other hand, artificial-intelligence/machine-learning (ML) methods are being widely used in a number of fluidmechanics areas [25], including numerical simulation, modeling of turbulence and measurement data assimilation (DA) [19]. With increased computational power, this has a great potential to enhance, denoise [16] or reconstruct PIV velocity data in terms of their resolution in time and space. In typical ML frameworks, for instance those relying on deep learning (DL), the quality of the data significantly determines the usability of the methods. Therefore, large datasets are required, which may not be available from experimental measurements. Note that it is generally not straightforward to combine available data with existing physical laws in DL models. However, integrating the governing equation and domain information into the model training is essential in order to improve its efficiency regarding the empirical, physical and mathematical perception of the flow. In recent years, MLbased algorithms have been progressively more widely used in a wide range of areas [23, 24], including for simulations of fluid mechanics [25]. In particular, a recent study by Guastoni *et al* [8], proposed two models based on convolutional neural networks (CNNs) to train and predict two-dimensional instantaneous velocity-fluctuation fields. They used channel-flow data, particularly wall-shear stress and wall pressure obtained through direct numerical simulations (DNSs) as an input to their models. Predictions from both models were very accurate compared to the reference DNS data, outperforming traditional linear methods. Along with successful application of numerical data, the success of their model within shear bounded flow indicate that non-intrusive sensing can also be benefited in terms of active control experiments with closedloop [26]. In addition to improving numerical data, CNN has also been effectively applied to improve synthetic PIV data [20].

In this study we explore the framework of physics-informed neural networks (PINNs) to address the problems arising from the application of PIV. Subsequently, PINNs were also applied to the data from numerical simulations. PINNs, according to [15], provide a framework that will integrate data and the physical laws into the learning process of a neural network, resulting in a robust model that can provide accurate and physicallyconsistent predictions despite having imperfect data. Note that the laws governing fluid-dynamics problems are non-linear partial differential equations (PDEs). Eivazi and Vinuesa [5] showed the potential of using PINNs to reconstruct experimental data with noise and other measurement errors, including vortical flows and wall-bounded turbulence. A similar study using PINNs for velocity-field reconstruction from sparse data can be found in [27]. Another application of PINNs was presented by Eivazi *et al* [3] and Eivazi *et al* [4, 5], who applied the PINN algorithm to solve the Reynolds-averaged-Navier–Stokes (RANS) for incompressible ZPGTBLs without any prior assumptions for turbulence. Along with supervised learning from the domain boundary, mean-flow quantities and their coordinates at the domain boundary were used as input data. This study reports very accurate prediction of the mean flow field, the skin-friction coefficient and the Reynolds stresses in complex flow cases involving pressure gradients and separation.

In the present work we will employ the PINN framework to augment the spatial resolution of the mean velocity fields. We will formulate a supervised-learning problem together with PINNs to solve the RANS equations for incompressible TBL flows, using mean data as the reference. The RANS equations are applied without any a-priori turbulence model or assumptions. Note that usually modelling assumptions are introduced to model the Reynolds stresses in the RANS equations. Within the scope of the present work, we will introduce a novel approach, where the data points at the mean field boundary will be used to train the neural network in order to solve the set of governing equations.

#### **2. Methodology**

PINNs are deep-learning-based frameworks for solution of PDEs. A PINN comprises two parts: a multilayer perceptron (MLP) and a so-called residual network, which calculates the residual of the governing equations. For a steady PDE, the spatial coordinates **x** are the inputs of the MLP and the solution vector of the PDE system **u** = *f*(**x**) is the output where the function *f* is parameterized by the MLP. Automatic differentiation (AD) is utilized to differentiate the outputs **u** with respect to the inputs **x** and formulate the governing equations. Note that AD can be implemented directly from the deep-learning framework since it is used to compute the gradients and update the network parameters, i.e. weights*w* and biases *b*, during the training. We consider the two-dimensional RANS equations for steady and incompressible flows as the governing PDE:

$$\frac{\partial U_i}{\partial x_i} = 0, \quad (1a)$$

$$U_j \frac{\partial U_i}{\partial x_j} = -\frac{1}{\rho} \frac{\partial P}{\partial x_i} - \frac{\partial u_i u_j}{\partial x_j} + \nu \frac{\partial^2 U_i}{\partial x_i \partial x_j}, \quad (1b)$$

where *U$^{i}$* denotes the *i*th component of mean velocity vector and *uiu$^{j}$* represents components of the Reynolds-stress tensor. Furthermore, *P* is the mean pressure, *ρ* is the density, *ν* is the kinematic viscosity and *i,j* = 1*,*2. Figure 2 depicts a schematic view of the PINN, which shows the neurons with non-linear activation functions, the implementation of AD for differentiating the outputs **u** with respect to the inputs **x** = (*x, y*) and the calculation of the residual of the RANS equations **e**.

The main objective of our PINNs framework is to enhance the available reference data by reducing the noise and the error in the measurements. In particular, we aim to obtain the mean wall-normal velocity by having a set of noisy measurements for the mean streamwise velocity and the mean Reynolds-stress components, through solving the RANS equations. Figures 3(b)–(f) shows the contours of the reference PIV data set 'mps3-SBL'. Note that ˆ*.* indicates that the flow quantities are averaged in time, and are extracted from a particular streamwise location (*x* = 19.2 m both for reference and predicted data), normalized with outer scale: *$^{U}$∞* and *$^{U}$* 2 *∞* respectively.

It can be seen that the obtained mean wall-normal velocity from the PIV measurements is very noisy. The comparison with the well-resolved large-eddy-simulation data from the work in [6] also indicates that the obtained mean wall-normal velocity from PIV measurements is not accurate. This is due to the fact that accurate measurement of the wall-normal velocity in boundary layers is very challenging, as discussed above. To reduce the error in the measurements, we consider the output of the MLP for the *i*th sample as **u** *$^{i}$* = [*U i ,uv$^{i}$ ,uu$^{i}$ , vv$^{i}$ ,V i* ], where for *V* we do not use the PIV data as the targets, rather we aim to obtain the correct *V $^{i}$* by imposing the residual of the RANS equations **e** *i* as an unsupervised loss.

We consider two sets of points for supervised and unsupervised learning. Supervised learning refers to the training process by computing a supervised loss for the data for which the targets are available, and unsupervised learning stands for utilizing the residual of the RANS equations for training. The total loss is the summation of the supervised loss and the residual of the governing equations as:

$$L = L_e + L_s, \quad (2a)$$

$$L_e = \frac{1}{N_e} \sum_{i=1}^3 \sum_{n=1}^{N_e} |e_i^n|^2, \quad (2b)$$

$$L_s = \frac{1}{N_s} \sum_{n=1}^{N_s} |\mathbf{u}_s^n - \tilde{\mathbf{u}}_s^n|^2, \quad (2c)$$

where *L$^{e}$* and *L$^{s}$* are the loss-function components corresponding to the residual of the RANS equations and the target data **u***$^{s}$* = [*U,uv,uu, vv*], respectively. Here *N$^{e}$* represents the number of points for which the residual of the RANS equations is calculated, i.e. the collocation points **x***e*, and *N$^{s}$* is the number of training samples with the targets, i.e. the training-data points **x***$^{s}$* . Figure 3(a) depicts **x***$^{e}$* and **x***$^{s}$* over the computational domain. We consider *N$^{e}$* = 3350 and *N$^{s}$* = 350, which are equally-spaced points in logarithmic space in the *y* direction.

The MLP comprises four hidden layers, each containing 20 neurons, with hyperbolic tangent as the activation function and we employ a full-batch training procedure. We initiate the

![](_page_5_Figure_2.jpeg)

![](_page_5_Diagram_3.jpeg)

**Figure 2.** A schematic view of PINNs. Green indicates the neurons with non-linear activation functions, blue represents the implementation of AD for differentiating the outputs **u** with respect to the inputs **x** = (*x, y*) and magenta refers to the calculation of the residual of the RANS equations **e**.

![](_page_5_Figure_5.jpeg)

**Figure 3.** Data set 'mps3–SBL': (a) Collocation **x***$^{e}$* (pink) and the training-data points **x***$^{s}$* (blue) within the computational domain. (b)–(f) Contours of the mean velocities and Reynolds-stress components.

training using the Adam optimizer for 20 000 epochs with an exponential decay of learning rate as:

$$\ell r = \ell r_0 \alpha_d^{(n_c/n_d)}, \quad (3)$$

where *ℓr*$^{0}$ = 0*.*01 is the initial learning rate, *α*$^{d}$ = 0*.*1 is the decay rate and *n*$^{d}$ = 5000 is the decay step to be considered with respect to the current step *n*c. The decay of the learning rate is applied according to equation (3) every *n*$^{d}$ epochs. Then we utilize the limited-memory Broyden–Fletcher–Goldfarb–Shanno (L-BFGS) algorithm as the optimizer to obtain the solution. The optimization process of the L-BFGS algorithm is stopped automatically based on the increment tolerance. Figure 4 represents the supervised *L$^{s}$* , unsupervised *L$^{e}$* and the total loss *L* during the training process for the 'mps3-SBL' data set.

#### **3. Results**

Mean velocity fields obtained from both numerical simulations and experiments were used as the reference data for PINNs analysis. The experimental data was obtained from a ZPGTBL, while the numerical databases correspond to a

![](_page_6_Figure_2.jpeg)

**Figure 4.** Supervised *Ls*, unsupervised *L$^{e}$* and the total loss *L* during the training process for the 'mps3–SBL' data set.

**Figure 5.** The selected computational domain based on *$Re_\theta$* corresponding to 400 *< $Re_\theta$ <* 500 for the test case with no control together with the collocation and training data points.

spatially-developing ZPGTBL and an airfoil. All the reference data studied active flow control of boundary layer using Wallnormal blowing to reduce friction drag, subsequently changing the turbulence and mean properties of the downstream flow field. This flow-control scheme provides an unique opportunity to prove the robustness of the PINNs algorithm independent of any assumptions. The details of the reference dataset from different sources will be discussed in the following sections.

#### *3.1. DNS of TBL with uniform blowing*

We employ a data set obtained from DNS of a spatiallydeveloping turbulent boundary layer with uniform blowing (UB) [14] for our first experiment. Four test cases are selected for this study with the magnitude of UB equal to 0% (no control), 0.1%, 0.5% and 1.0% of the free stream velocity. The computational domain is selected based on the momentumthickness Reynolds number 400 *< $Re_\theta$ <* 500 for the reference case without control. Figure 5 depicts the computational domain together with the collocation and training data points. We utilize *N$^{e}$* = 17 000 and *N$^{s}$* = 188 for all four experiments. The objective is to reconstruct the wall-normal velocity from the data on the domain boundaries for streamwise velocity and Reynolds stresses. It should be noted that we do not use any training sample for wall-normal velocity; we aim to reconstruct wall-normal velocity by solving an optimization problem, which is constrained by the governing RANS equations, using PINNs. To this end, we employ an MLP with four hidden layers and 20 neurons per hidden layer. The training procedure and model hyperparameters are described in section 2. The learning curves are reported in appendix for all the test cases.

Figure 6 illustrates the obtained profiles for the velocity and Reynolds-stress components at the middle of the region of interest (*x* = 17.20) for the uncontrolled test case (top) and the case with UB of 1% (bottom) in comparison with the reference DNS data. It can be seen that excellent reconstructions are obtained for *V*ˆ using PINNs for both cases. The advantage of such reconstruction is that it can be applied over a very small data set (only 188 sample points with labels), and no training data is required for wall-normal velocity. Moreover, we obtain excellent predictions for streamwise velocity and Reynolds-stress components inside the domain.

The velocity profiles for *U*ˆ and *V*ˆ at *x* = 17.20 are depicted in figure 7 for all the four cases with different magnitudes of UB. It can be seen that the PINN approach is able to reconstruct the wall-normal velocity accurately for all the cases and capture the increase of wall-normal velocity due to the increase of UB magnitude. Our results also show the excellent performance of PINNs in the prediction of *U*ˆ inside the domain for all the cases. To better represent the performance of PINNs in the prediction of boundary-layer parameters inside the domain we illustrate the contour of *V*ˆ in figure 9 and contours of *U*ˆ, *uv*ˆ , *uu*ˆ and *vv*ˆ in figure 8 for the test case with UB of 1%. Results are reported for PINNs predictions compared with the reference DNS data. We also report the relative errors in the figures. The relative error is defined as:

![](_page_6_Figure_7.jpeg)

$$\epsilon = \frac{|\text{Pred.} - \text{Ref.}|}{|\text{Ref.}|} \quad (4)$$

where (*·*) indicates the mean over the domain. The maximum relative error for wall-normal velocity *ϵV*$^{ˆ}$ is less than 5%, which shows the accurate performance of the PINN approach in the reconstructions.

Figure 8 presents the contours of *U*ˆ, *uv*ˆ , *uu*ˆ and *vv*ˆ along with their relative errors plotted beside each of these mean properties of the flow field. As it can be seen in figure 8, the maximum relative error for streamwise velocity is less than 1%. For the Reynolds-stress components the maximum relative errors are higher than those of the mean-velocity components, and are equal to 11%, 15% and 13% for *uv*ˆ , *uu*ˆ and *vv*ˆ , respectively. The mean of the relative error over the domain is less than 3% for all the Reynolds-stress components, again highlighting the very good performance of the PINNs-based methodology proposed here. Figure 9 presents the mean wall-normal velocity with the relative error, which is 4%. PINNs predicted fields (figures 8 and 9) indicate better convergence of the data.

Our results show that accurate reconstructions of wall-normal velocity can be obtained from a limited set of

![](_page_7_Figure_2.jpeg)

**Figure 6.** Profiles for the mean (a) streamwise velocity, (b) wall-normal velocity and (c) Reynolds-stress components at *x* = 17.20 for the SBL and same quantities in (d)–(f) for UB of 1%, PINNs prediction in comparison with the reference DNS data.

measurements for streamwise velocity and Reynolds-stress components in the turbulent boundary layer. It should be noted that the accuracy of the predictions may vary by changing the size of the domain, and for larger sizes of the computational domain more training data with labels may be required.

#### *3.2. Wing boundary layers with uniform blowing*

In this section PINNs-predicted results based on the data from Atzori *et al* [1, 2] will be presented. The authors performed high-fidelity simulations on a NACA4412 airfoil at a Reynolds number based on chord length *$Re_c$* $^{=}$ *$^{U}$∞C/ν* $^{=}$ 0.2 million, *$^{C}$* is the chord length. The suction side of the wing profile exhibits an adverse pressure gradient which rapidly increases in the streamwise direction, therefore; data from a specific section of the computational domain was used for PINNs prediction as indicated in figure 10.

In order to exhibit the statistical accuracy of the PINNs prediction, figure 11 plots the mean profiles at 0*.*75*C*, where, it shows that profiles of PINNs predicted data for mean velocity and Reynolds-stress components are in excellent agreement with the reference data.

#### *3.3. PINNs predictions of the PIV flow field*

The 2D3C stereo PIV measurements used for the present PINNs predictions are from [10, 12]. The measurements were taken at the boundary-layer wind-tunnel facility at Laboratoire de Mécanique des Fluides de Lille—Kampé de Fériet [7] in France, within the European High Performance Infrastructures in Turbulence (EuHIT) framework. The recirculating wind tunnel has a test section with a length of 20.6 m with a cross section of $^{2}$ *×* $^{1}$ $^{m}$$^{2}$ (width *×* height). Figure 12(a) presents the isometric projection of the flow field schematic where the reference in Cartesian coordinates is considered at the leading edge. Therefore, the streamwise, wall-normal and spanwise directions are indicated by the *x*, *y* and *z* coordinates respectively, where *x* = 0 at the leading edge center of the plate. Four cameras with Scheimpflug adapters according to stereo arrangement were used with the same magnification parameters. Here, the FoV was divided into two overlapping segments. The TBL at *$Re_\theta$* = 7495 was investigated along with an active flow control with uniform blowing. Wallnormal blowing was applied before the measurement plane as indicated with pink region in figure 12(a) (22 cm upstream from the beginning of the FoV). Wall-normal blowing was applied at a blowing ratio BR of 0%, 1%, 3% and 6% of *$^{U}$∞*

![](_page_8_Figure_2.jpeg)

**Figure 7.** Velocity profiles for (a) *$^{U}$*$^{ˆ}$ and (b) *$^{V}$*$^{ˆ}$ at *$^{x}$* $^{=}$ 17.20 for all the four cases with different magnitudes of UB: (■) no control, (♦) UB 0.1%, (*•*) UB 0.5% and (▼) UB 1%. Red dashed lines show PINN predictions and blue solid lines indicate DNS data.

![](_page_8_Figure_4.jpeg)

**Figure 8.** Contours of (a) *U*ˆ, (d) *uv*ˆ , (g) *uu*ˆ and (j) *vv*ˆ obtained from PINN in comparison with those of (b), (e), (h) and (k) which are from the reference high-fidelity database for the test case with UB of 1%, in (c), (f), (i) and (l) we show the relative errors in the field.

(note that BR $^{=}$ *$^{V}$w/U$^{∞}$ ×* 100, where *$^{V}$$^{w}$* is the wall-normal blowing velocity). Hence, the various cases will be denoted as: 'mps3-SBL', 'mps3-b0', 'mps3-b1', 'mps3-b3' and 'mps3 b6' respectively in the description of the results. Note that 'SBL' corresponds to a smooth wall, whereas 'b0' denotes a case with a perforated wall with no blowing; the effect of the roughness due to the holes is negligible in *U*, and very small in *V* as discussed below. During the experiment, the free

![](_page_9_Figure_2.jpeg)

**Figure 9.** Contour of *V*ˆ obtained from (a) PINN in comparison with (b) the reference high-fidelity data for the test case with UB of 1%, in (c) we show the relative error.

**Figure 10.** (a) Domain for the NACA4412 airfoil on the suction side. Black dashed line indicates the analyzed region of interest, which in (b) is shown in more detail. The lengths are scaled with the wing chord, and the colors indicate mean streamwise velocity.

stream velocity for each of these cases was fairly constant. On the other hand, blowing convects vertically the turbulent structures present in the near-wall region towards the outer region, resulting in an attenuated turbulence in the near wall region [22]. This leads to increased *V* and *δ*, and their increase depends on the magnitude of BR.

We have selected this data set to assess the robustness of the PINNs model, using only the data at the boundary and without a-priory assumptions. Each set of measurements contains 10$^{4}$ time steps at acquisition frequency of 4 Hz, where each time step contains $^{402}$ *×* $^{333}$ vectors for each flow quantity with an uniform interval of 6*.*5 $^{+}$ *∼* $^{18}$*.*$^{5}$ $^{+}$ depending on the flow Reynolds number. The accuracy on mean streamwise velocity was *±*1*.*5% of *$^{U}$$^{∞}$* with $^{95}$% confidence interval. In average, the random error for streamwise and wall-normal velocity components were less than $^{1}$% of corresponding *$^{U}$∞*. However, the spanwise velocity component exhibit maximum random error (1*.*1% of *$^{U}$∞*) compared to other velocity components. Note that this is the out-of-plane velocity component.

The first data point is obtained at a wall-normal distance of *y* $^{+}$ = 16. The streamwise length of the FoV was less than 1*δ*, and the variation of *δ* over the streamwise length was less than 1% for the standard ZPGTBL case. Interested readers are referred to [10] for a detailed overview of the TBL mean properties, error estimation and PIV properties of magnification and post processing algorithms. One common measurement error for all sets of measurements is the overestimation of *V*, this is due to the fact that the overall magnification uncertainty has the largest effect on the smallest flow quantities.

We applied the PINNs algorithm on a reference data set measured with PIV on a ZPGTBL [10] to predict the mean flow field. Only the two-dimensional (2D) Cartesian coordinates of the vector field and flow-field data averaged over time was used for the training of the supervised-learning process and therefore, the PINNs prediction improved the convergence of these mean fields and corrected the spurious data in terms of over/under estimation. Note that the predicted field has a size similar to that of the reference data field, therefore the current predictions are limited to length of the reference data field. We have predicted only the mean streamwise and wall-normal velocity fields and the 2D Reynolds stresses.

![](_page_9_Figure_5.jpeg)

Figures 13 and 14 present the comparison of turbulence statistics for the 'mps3-SBL' and 'mps3-b6' data sets., where only *U*ˆ, *uv*ˆ and *vv*ˆ are shown. These figures show that the reference PIV data exhibits a well-converged *U*ˆ field, while both *uv*ˆ and *vv*ˆ exhibit insufficient convergence. On the other hand, the *uv*ˆ and *vv*ˆ fields predicted via PINNs are very smooth and clearly show a well-converged statistical behavior. Note that this result is also observed for the case with BR = 6%, in which the flow is significantly modified upstream of the measurement location, and the PINNs framework was capable of successfully predicting the turbulence statistics even when significant flow-history effects were present. Also note that the results in figure 14 show the significant boundary-layer growth associated with the wall-normal convection introduced by the blowing, a phenomenon which is also well represented by the PINN framework. Note that the results corresponding to the intermediate cases 'mps3-b0', 'mps3-b1' and 'mps3-b3' are presented in the appendix.

Next, we will present the turbulence statistics for the reference data along with their corresponding PINNs prediction and a second reference data set from the well-resolved LES from [6]. Figure 15 shows the turbulence statistics at *x* = 12.9 m as a function of the outer-scaled wall-normal location *y/δ* for the SBL case. This figure shows that the mean velocity profile from the experiment is in very good agreement with that of the simulation, and also from the PINN prediction. When it comes to the Reynolds stresses, simulation and experiment are also in good agreement, although the experiment exhibits a moderate noise, more noticeable in the *uv*ˆ field. Interestingly, the PINN predictions significantly reduce this noise, leading to a better agreement with the reference numerical data. It is also important to note that the *V*ˆ profile from the experiment does not show good agreement with the simulation, due to the fact that this is a very small quantity which is generally challenging to accurately measure as discussed above. Interestingly, the PINN prediction of *V*ˆ is in very good agreement with the high-fidelity

![](_page_10_Figure_2.jpeg)

**Figure 11.** Profiles of (a) mean streamwise velocity, (b) wall-normal velocity and (c) the Reynolds-stress components along the outer-scaled wall-normal distance at 75% chord length.

![](_page_10_Figure_4.jpeg)

**Figure 12.** (a) Schematic representation of the flow field and the stereo PIV arrangement (all dimension in meter); (b) photograph of the wind-tunnel test section.

![](_page_10_Figure_6.jpeg)

**Figure 13.** Flow-field reconstruction with PINNs for data set 'mps3-SBL', in the top row (a), (c) and (e) are the reference data, (b), (d) and (f) are the PINNs prediction. Flow quantities are mentioned on top of each column.

numerical data, a fact that shows the great potential of this approach to correct experimental data. A similar comparison is presented in figure 16 for the 'mps3-b6' case, in which the numerical data is included only for reference, but no direct comparison is possible because the simulation does not involve blowing. The experimental data, in which a significant blowing ratio of 6% is introduced, shows the expected differences in the flow when comparing with the smooth-wall numerical case, i.e. more pronounced outer-layer fluctuations and Reynolds shear stress [1]. In this case, the mean flows

![](_page_11_Figure_2.jpeg)

**Figure 14.** Flow-field reconstruction with PINNs for data set 'mps3-b6', in the top row (a), (c) and (e) are the reference data, (b), (d) and (f) are the PINNs prediction. Flow quantities are mentioned on top of each column.

![](_page_11_Figure_4.jpeg)

**Figure 15.** Turbulence statistics at *x* = 12.9 m from experiment, simulation [6] and PINN prediction (see legend) for the 'mps3-SBL' case. We show (a) mean streamwise velocity *U*ˆ, (b) mean wall-normal velocity *V*ˆ and (c) the Reynolds stresses *uv*ˆ , *uu*ˆ and *vv*ˆ .

![](_page_11_Figure_6.jpeg)

**Figure 16.** Turbulence statistics at *x* = 19.2 m from experiment, simulation [6] and PINN prediction (see legend) for the 'mps3-b6' case. We show (a) mean streamwise velocity *U*ˆ, (b) mean wall-normal velocity *V*ˆ and (c) the Reynolds stresses *uv*ˆ , *uu*ˆ and *vv*ˆ .

![](_page_12_Figure_2.jpeg)

**Figure 17.** Comparison of PINNs-predicted profiles for the different cases under study (except 'mps3-SBL'), where the darker colors correspond to stronger BR. The dashed lines represent the canonical ZPG TBL numerical data from [6]. (a) Outer-scaled mean streamwise velocity (*U*ˆ) and (b) outer-scaled mean wall-normal velocity (*V*ˆ) profiles at *x* = 19.2 m.

from PIV and PINNs are in excellent agreement, and a significant reduction of the experimental noise is achieved in the Reynolds stresses. Regarding the *V*ˆ profile, it can be observed that the experimental measurement provided very noisy data and even negative velocities, which are not consistent with the behavior expected for this flow. On the other hand, the PINN prediction exhibits very smooth behavior, and the trend increases as the wall is approached, which is consistent with the strong *V$^{w}$* imposed right upstream of the measurement location. Consequently, the PINN framework not only improves the measurement of *V*ˆ but also enforces a physically-consistent behavior.

Finally, figure 17 compares all the PINNs-predicted outerscaled profiles of *U*ˆ and *V*ˆ for all the blowing cases (see the appendix for all the analysis of the intermediate control configurations). The streamwise-velocity profiles exhibit a trend consistent with that reported in the experimental work from [10], while the wall-normal-velocity profiles are very smooth and also show the expected increase with BR, both as the wake region and the wall are approached. It is interesting to note that the 'mps3-b0' case exhibits a *V*ˆ profile slightly below that of the canonical ZPG configuration (even with some values slightly below zero closer to the wall), which is a consequence of the perforated plate.

### **4. Conclusion**

We have employed the PINNs framework to make predictions on various datasets extracted from experiments and numerical simulations. Besides the regular smooth-wall TBLs, an active control through uniform blowing was also added upstream of the measurement location/simulated domain, which introduced several different flow conditions to the downstream flow field. The change of boundary conditions are the consequence of different blowing rations BR ranging from 0% to 6%. In contrast to traditional approaches to solve RANS equations, which require turbulence models, in the PINNs framework we solve the RANS for incompressible turbulent flow without any specific model/assumptions. Instead, only the mean velocities and the Reynolds-stresses components at the domain boundary are needed. The training process involves minimizing the residual of the RANS equations and also being able to match the implemented boundary conditions.

A logarithmic function was employed to choose data systematically at the domain boundaries in order to evaluate the residual of the governing equations. Then, selected data points were utilized to predict the subsequent flow quantities. The supervised loss is also calculated based on this selection criterion comparing the predicted and the input data.

The predicted flow quantities including the Reynolds stresses are in excellent agreement with reference data. Our results indicate that PINNs can provide accurate predictions for the mean-flow quantities and the Reynolds stresses. At the same time, good adaptability and robustness are exhibited by the PINNs algorithm, which is an additional advantage in order to apply these techniques to the numerical simulations and PIV measurements from incompressible turbulent flows, even with changing upstream flow conditions. The PINNs algorithm has the capability to reconstruct the flow-field quantities removing the noise present in the experimental data. Furthermore, our framework can correct the measurements of *V*, which is particularly challenging to measure in these types of turbulent flows. This constitutes an enormous advantage when enhancing experimental data.

A traditional PIV system is limited in its spatial resolution, especially the near-wall region is coarsely resolved. A further development of this work will be be made taking the near-wall region also into the PINN simulation to compute the viscous sub-layer and thus, predict the wall-shear stresses for given experimental setups. Here, we have shown the advantage of using PINNs framework to analyse the underlying flow behavior from experimental results. This leads to a new perspective for complex-flow situations, which are expensive to simulate and challenging to study with experimental methods.

### **Data availability statement**

The data that support the findings of this study are available upon reasonable request from the authors.

### **Acknowledgments**

We thank Marco Atzori, Yukinori Kametani, and Koji Fukagata for providing the numerical data. Christoph Egbers and team acknowledge the support from Vasyl Motuz from BTU Cottbus-Senftenberg, Jean-Marc Foucaut and Christophe Cuvier from Laboratoire de Mécanique des Fluides de Lille— Kampé de Fériet (LMFL), Lille, France. The financial support under EuHIT Grant Agreement Number 312778 within the FP7-INFRASTRUCTURES-2012-1 (European Union's research and innovation funding program) is also acknowledged. Ricardo Vinuesa and team acknowledge the financial support from the Göran Gustafsson foundation and from the ERC Grant No. '2021-CoG-101043998, DEEPCONTROL'. Part of the numerical results were obtained thanks to computer time provided by the Swedish National Allocation Committee (SNIC). The codes used to obtain the findings of this study are openly available on GitHub: https://github.com/KTH-FlowAI/ Enhancement-of-PIV-via-PINNs.

#### **Appendix**

In this appendix we show the experimental data and the PINNbased reconstructions from the intermediate cases not shown above. Figures 18–20 show the flow-field reconstruction of *U*, *uv* and *vv* for the 'mps3-b0', 'mps3-b1' and 'mps3-b3' cases, respectively. In these figures, the two-dimensional measurement area is shown, and data from PIV and PINN are presented. Furthermore, figures 21–23 show numerical, experimental and PINN prediction of the turbulence statistics at *x* = 12.9 m for the 'mps3-b0', 'mps3-b1' and 'mps3-b3' configurations, respectively.

![](_page_14_Figure_2.jpeg)

**Figure 18.** Flow-field reconstruction with PINNs for data set 'mps3-b0', in the top row (a), (c) and (e) are the reference data, (b), (d) and (f) are the PINNs prediction. Flow quantities are mentioned on top of each column.

![](_page_14_Figure_4.jpeg)

**Figure 19.** Flow-field reconstruction with PINNs for data set 'mps3-b1', in the top row (a), (c) and (e) are the reference data, (b), (d) and (f) are the PINNs prediction. Flow quantities are mentioned on top of each column.

![](_page_14_Figure_6.jpeg)

**Figure 20.** Flow-field reconstruction with PINNs for data set 'mps3-b3', in the top row (a), (c) and (e) are the reference data, (b), (d) and (f) are the PINNs prediction. Flow quantities are mentioned on top of each column.

![](_page_15_Figure_2.jpeg)

**Figure 21.** Turbulence statistics at *x* = 19.2 m from experiment, simulation [6] and PINN prediction (see legend) for the 'mps3-b0' case. We show (a) mean streamwise velocity *U*ˆ, (b) mean wall-normal velocity *V*ˆ and (c) the Reynolds stresses *uv*ˆ , *uu*ˆ and *vv*ˆ .

![](_page_15_Figure_4.jpeg)

**Figure 22.** Turbulence statistics at *x* = 19.2 m from experiment, simulation [6] and PINN prediction (see legend) for the 'mps3-b1' case. We show (a) mean streamwise velocity *U*ˆ, (b) mean wall-normal velocity *V*ˆ and (c) the Reynolds stresses *uv*ˆ , *uu*ˆ and *vv*ˆ .

![](_page_15_Figure_6.jpeg)

**Figure 23.** Turbulence statistics at *x* = 19.2 m from experiment, simulation [6] and PINN prediction (see legend) for the 'mps3-b3' case. We show (a) mean streamwise velocity *U*ˆ, (b) mean wall-normal velocity *V*ˆ and (c) the Reynolds stresses *uv*ˆ , *uu*ˆ and *vv*ˆ .

**ORCID iD** Ricardo Vinuesa https://orcid.org/0000-0001-6570-5499 **References** [1] Atzori M, Vinuesa R, Fahland G, Stroh A, Gatti D, Frohnapfel B and Schlatter P 2020 Aerodynamic effects of uniform blowing and suction on a NACA4412 airfoil *Flow Turbul. Combust.* **105** 735–59 [2] Atzori M, Vinuesa R, Stroh A, Gatti D, Frohnapfel B and Schlatter P 2021 Uniform blowing and suction applied to nonuniform adverse-pressure-gradient wing boundary layers *Phys. Rev. Fluids* **6** 113904 [3] Eivazi H, Tahani M, Schlatter P and Vinuesa R 2021 Physics-informed neural networks for solving Reynolds-averaged Navier–Stokes equations *Proc. 13th ERCOFTAC Symp. on Engineering Turbulence Modeling and Measurements (ETMM13) (Rhodes, Greece, 15–17 September 2021)* (arXiv:2107.10711) [4] Eivazi H, Tahani M, Schlatter P and Vinuesa R 2022 Physics-informed neural networks for solving Reynolds-averaged Navier–Stokes equations *Phys. Fluids* **34** 075117 [5] Eivazi H and Vinuesa R 2022 Physics-informed deep-learning applications to experimental fluid mechanics (arXiv:2203. 15402) [6] Eitel-Amor G, Örlü R and Schlatter P 2014 Simulation and validation of a spatially evolving turbulent boundary layer up to *$Re_\theta$* = 8300 *Int. J. Heat Fluid Flow* **47** 57–69 [7] Foucaut J-M, Carlier J and Stanislas M 2004 PIV optimization for the study of turbulent flow using spectral analysis *Meas. Sci. Technol.* **15** 1046–58 [8] Guastoni L, Güemes A, Ianiro A, Discetti S, Schlatter P, Azizpour H and Vinuesa R 2021 Convolutional-network models to predict wall-bounded turbulence from wall quantities *J. Fluid Mech.* **928** A27 [9] Hasanuzzaman G, Merbold S, Motuz V and Egbers C 2016 Experimental investigation of turbulent structures and their control in boundary layer flow *Experimentelle StröMungsmechanik, 24. Fachtagung (6–8 September 2016)* (Karlsruhe: German Association for Laser Anemometry GALA eV) p 27.1–6 [10] Hasanuzzaman G, Merbold S, Cuvier C, Motuz V, Foucaut J M and Egbers C 2020 Experimental investigation of turbulent boundary layers at high Reynolds number with uniform blowing part I: statistics *J. Turbul.* **21** 129–65 [11] Hasanuzzaman G, Merbold S, Cuvier C, Motuz V, Foucaut J-M and Egbers C 2018 Experimental investigation of active control inturbulent boundary layer using uniform blowing *5th Int. Conf. on Experimental Fluid Mechanics (ICEFM) (Munich, Germany, 2–4 July 2018)* pp 1–6 [12] Hasanuzzaman G 2021 *Experimental Investigation of Turbulent Boundary Layer With Uniform Blowing at Moderate and High Reynolds Numbers* 1st edn (Göttingen: Cuvillier Verlag) pp 1–152 [13] Hasanuzzaman G, Merbold S, Motuz V and Egbers C 2022 Enhanced outer peaks in turbulent boundary layer using uniform blowing at moderate Reynolds number *J. Turbul.* **23** 68–95 [14] Kametani Y and Fukagata K 2011 Direct numerical simulation of spatially developing turbulent boundary layers with uniform blowing or suction *J. Fluid Mech.* **681** 154–72 [15] Raissi M, Perdikaris P and Karniadakis G E 2017 Physics informed deep learning (part I): data-driven solutions of nonlinear partial differential equations pp 1–22 (arXiv:1711.10561) [16] Raissi M, Yazdani A and Karniadakis G E 2020 Hidden fluid mechanics: learning velocity and pressure fields from flow visualizations *Science* **367** 1026–30 [17] Schröder A and Willert C 2008 *Particle Image Velocimetry: New Developments and Recent Applications* (Berlin: Springer) pp 1–13 [18] Sciacchitano A, Dwight R P and Scarano F 2012 Navier–Stokes simulations in gappy PIV data *Exp. Fluids* **53** 1421–35 [19] Symon S, Dovetta N, McKeon B J, Sipp D and Schmid P J 2017 Data assimilation of mean velocity from 2D PIV measurements of flow over an idealized airfoil *Exp. Fluids* **58** 1–15 [20] Stulov N and Chertkov M 2021 Neural particle image velocimetry *Med. Phys.* 1–9 submitted [21] Vinuesa R, Bartrons E, Chiu D, Dressler K M, Rüedi J-D, Suzuki Y and Nagib H M 2014 New insight into flow development and two dimensionality of turbulent channel flows *Exp. Fluids* **55** 1–14 [22] Vinuesa R, Negi P S, Atzori M, Hanifi A, Henningson D S and Schlatter P 2018 Turbulent boundary layers around wing sections up to *$Re_c$* = 100000 *Int. J. Heat Fluid Flow* **72** 86–99 [23] Vinuesa R, Azizpour H, Leite I, Balaam M, Dignum V, Domisch S, Felländer A, Langhans S D, Tegmark M and Fuso-Nerini F 2020 The role of artificial intelligence in achieving the sustainable development goals *Nat. Commun.* **11** 233 [24] Vinuesa R, Theodorou A, Battaglini M and Dignum V 2020 A socio-technical framework for digital contact tracing *Results Eng.* **8** 100163 [25] Vinuesa R and Brunton S L 2022 Enhancing computational fluid dynamics with machine learning *Nat. Comput. Sci.* **2** 358–66 [26] Vinuesa R, Lehmkuhl O, Lozano-Durán A and Rabault J 2022 Flow control in wings and discovery of novel approaches via deep reinforcement learning *Fluids* **7** 62 [27] Wang H, Liu Y and Wang S 2022 Dense velocity reconstruction from particle image velocimetry/particle tracking velocimetry using a physics-informed neural network *Phys. Fluids* **34** 017116 [28] Willert C E *et al* 2018 Experimental evidence of near-wall reverse flow events in a zero pressure gradient turbulent boundary layer *Exp. Therm. Fluid Sci.* **91** 320–8 [29] Willert C E 2018 Profile PIV'—more than just an optical hotwire new potentials of PIV in boundary layer research *Proc. 18th Int. Symp. on Flow Visualization (Zurich, Switzerland, 26–29 June 2018)* pp 1–18 [30] Willert R M, Wereley C E and Kompenhans J 2013 *Particle Image Velocimetry: A Practical Guide* (Berlin: Springer) pp 1–448 [31] Zanoun E S, Jehring L and Egbers C 2014 Three measuring techniques for assessing the mean wall skin friction in wall-bounded flows *Thermophys. Aeromech.* **21** 179–90
