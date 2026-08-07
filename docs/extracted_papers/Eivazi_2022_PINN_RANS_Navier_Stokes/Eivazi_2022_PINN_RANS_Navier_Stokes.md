# PHYSICS-INFORMED NEURAL NETWORKS FOR SOLVING REYNOLDS-AVERAGED NAVIER–STOKES EQUATIONS

*Hamidreza Eivazi*1,$^{2}$ *, Mojtaba Tahani*$^{1}$ *, Philipp Schlatter*$^{2}$ *, Ricardo Vinuesa*$^{2}$

$^{1}$ *Faculty of New Sciences and Technologies, University of Tehran, Tehran, Iran* $^{2}$ *SimEx/FLOW, Engineering Mechanics, KTH Royal Institute of Technology, SE-100 44 Stockholm, Sweden* [hamidre@kth.se](mailto:hamidre@kth.se)

# Abstract

Physics-informed neural networks (PINNs) are successful machine-learning methods for the solution and identification of partial differential equations (PDEs). We employ PINNs for solving the Reynolds-averaged Navier–Stokes (RANS) equations for incompressible turbulent flows without any specific model or assumption for turbulence, and by taking only the data on the domain boundaries. We first show the applicability of PINNs for solving the Navier–Stokes equations for laminar flows by solving the Falkner–Skan boundary layer. We then apply PINNs for the simulation of four turbulent-flow cases, *i.e.*, zero-pressure-gradient boundary layer, adversepressure-gradient boundary layer, and turbulent flows over a NACA4412 airfoil and the periodic hill. Our results show the excellent applicability of PINNs for laminar flows with strong pressure gradients, where predictions with less than 1% error can be obtained. For turbulent flows, we also obtain very good accuracy on simulation results even for the Reynolds-stress components.

# 1 Introduction

In recent years, machine-learning (ML) methods have started to play a revolutionary role in many scientific disciplines (Vinuesa et al., 2020). Fluid mechanics has been one of the active research topics for development of innovative ML-based approaches (Kutz, 2017; Duraisamy et al., 2019; Brunton et al., 2020). The contribution of ML in turbulent-flow problems is mainly in the contexts of data-driven turbulence closure modeling (Ling et al., 2016; Jiang et al., 2021), prediction of temporal dynamics in turbulent flows (Srinivasan et al., 2019; Eivazi et al., 2021), nonlinear modal decomposition (Murata et al., 2020; Eivazi et al., 2020) extraction of turbulence theory form data (Jimenez, 2018), non-intrusive sensing in ´ turbulent flows (Guastoni et al., 2020; Guemes et al., ¨ 2021), and flow control (Tang et al., 2020). More recently, exploiting the universal-approximation property of neural networks for solving complex partial differential equation (PDE) systems has brought attention, aiming to provide efficient solvers that approximate the solution. Physics-informed neural networks (PINNs), introduced by Raissi et al. (2019a), have been shown to be well suited for the solution of forward and inverse problems related to several different types of PDEs. PINNs have been used to simulate vortex-induced vibrations (Raissi et al., 2019b) and to tackle ill-posed inverse fluid mechanics problems (Raissi et al., 2020). Moreover, PINNs have been employed for super-resolution and denoising of 4Dflow magnetic resonance imaging (MRI) (Fathi et al., 2020) and prediction of near-wall blood flow from sparse data (Arzani et al., 2021). Recently, Jin et al. (2021) showed the applicability of PINNs for the simulation of turbulence directly, where good agreement was obtained between the direct numerical simulation (DNS) results and the PINNs simulation results. A detailed discussion on the prevailing trends in embedding physics into ML algorithms and diverse applications of PINNs can be found in the work by Karniadakis et al. (2021).

In this study, we employ PINNs for solving the Reynolds-averaged Navier–Stokes (RANS) equations for incompressible turbulent flows without any specific model or assumption for turbulence. In the RANS equations, the loss of information in the averaging process leads to an underdetermined system of equations. Traditional solvers require the introduction of modeling assumptions to close the system. We introduced an alternative approach to tackle this problem by using the information from a few data examples and the underdetermined system of equations for the training of a neural network that solves the system of equations. In particular, we use the data on the domain boundaries (including Reynolds-stress components) along with the RANS equations that guide the learning process towards the solution. The spatial coordinates are the inputs of the model and the mean-flow quantities, *i.e.*, velocity components, pressure, and Reynolds-stress components, are the outputs. Automatic differentiation (AD) (Baydin et al., 2018) is applied to differentiate the outputs with respect to the inputs to construct the RANS equations. Only the data on the domain boundaries are considered as the training dataset for the supervised-learning part while a set of points inside the domain together with the points

![](_page_1_Diagram_0.jpeg)

Figure 1: A schematic of PINNs for solving the RANS equations for a general two-dimensional set-up. The left part of the model is a FNN, and the right part is the formulation of the RANS equations using AD.

on the boundaries are used to calculate the residual of the governing equations, which acts as the unsupervised loss. The Reynolds number is set through the governing equations. We take mean-flow quantities obtained from DNS or well-resolved large-eddy simulation (LES) of canonical turbulent flow cases as the reference.

# 2 Methodology

A schematic of PINNs for the RANS equations is depicted in Figure 1. In a general two-dimensional setup, the spatial coordinates (x and y) are the inputs of a fully-connected neural network (FNN), and the outputs are the mean streamwise and wall-normal components of velocity (U and V , respectively), pressure (P), and Reynolds-stress components (u $^{2}$, uv, and v $^{2}$). Automatic differentiation (Baydin et al., 2018) is applied to differentiate outputs with respect to the inputs and formulate the RANS equations (continuity and momentum equations). AD can be implemented directly from the deep learning framework as it is used to compute the gradients and update the network parameters, i.e. weights w and biases b, during the training. We use the open-source machine-learning software framework TensorFlow (Abadi et al., 2016) to develop our PINN models. TensorFlow provides the "tf.GradientTape" application programming interface (API) for AD by computing the gradient of a computation with respect to some inputs. Tensor-Flow "records" the computational operations executed inside the context of a tf.GradientTape onto a so-called "tape", and then uses that tape to compute the gradients of a recorded computation using reversemode differentiation.

In our setup, only the data on the domain boundaries are used as the training dataset for supervised learning. The total loss is the summation of the supervised loss and the residual of the governing equations as follows:

$$L = L_e + L_b, \quad (1a)$$

$$L_e = \frac{1}{N_e} \sum_{i=1}^3 \sum_{n=1}^{N_e} |\epsilon_i^n|^2, \quad (1b)$$

$$L_b = \frac{1}{N_b} \sum_{n=1}^{N_b} |\mathbf{U}_b^n - \tilde{\mathbf{U}}_b^n|^2, \quad (1c)$$

where L$^{e}$ and L$^{b}$ are the loss-function components corresponding to the residual of the RANS equations and the boundary conditions, respectively. Here N$^{e}$ represents the number of points for which the residual of the RANS equations is calculated, and N$^{b}$ is the number of training samples on the domain boundaries. We consider a set of points inside the domain and compute the residuals on these points together with the points on the domain boundaries. Here, U$^{n}$ $^{b}$ = [U n b , V $^{n}$ b , P $^{n}$ b , u 2 n b , uv$^{n}$ b , v 2 n b $^{T}$ represents the given data for point n on the boundaries. U˜ $^{n}$ b is the vector of PINN predictions at the corresponding point, and n i is the residual of the i th governing equation at point n. It is also possible to consider weighting coefficients to balance different terms of the loss function and accelerate convergence in the training process (Jin et al., 2021).

![](_page_1_Figure_6.jpeg)

Figure 2: Simulation results of the Falkner–Skan boundary layer with adverse pressure gradient using PINNs (left) in comparison with the reference data (right). (a, b, c) Contours of U, V , and P, respectively.

# 3 Results

We employ PINNs for solving the RANS equations for four turbulent flow cases, *i.e.*, zero-pressuregradient (ZPG) boundary layer (Eitel-Amor et al., 2014), adverse-pressure-gradient (APG) boundary layer (Bobke et al., 2017), and turbulent flows over a

![](_page_2_Figure_0.jpeg)

Figure 3: Simulation results of the ZPG turbulent boundary layer using PINNs in comparison with the reference data. (a) Contours of U (top), V (middle), and uv (bottom); (b) Shape factor H$^{12}$ (top) and skin-friction coefficient c$^{f}$ (bottom). (c) Inner-scaled mean streamwise velocity U $^{+}$(top) and Reynolds-stress uv$^{+}$ (bottom) profiles at $Re_\theta$ = 2500, 4000, and 5500. Dashed and solid lines represent, respectively, the PINN predictions and the reference data. Darker color shows higher Reθ.

NACA4412 airfoil (Vinuesa et al., 2018) and the periodic hill. We also show the applicability of PINNs for the simulation of laminar boundary flows. To evaluate the accuracy of the predictions, we consider the relative `2-norm of errors E$^{i}$ on all the computational points and for the i th variable as:

---

$$E_i = \frac{\|\mathbf{U}_i - \tilde{\mathbf{U}}_i\|_2}{\|\mathbf{U}_i\|_2} \times 100, \quad (2)$$

where || · ||$^{2}$ denotes `2-norm, and $^{U}$ and $^{U}$˜ indicate the vectors of reference data and PINN predictions, respectively. Results for E is reported in Table 1 for all the test cases. The dash symbol in this table denotes that the corresponding variable is not calculated in that test case. We discuss each test case in detail in the following.

Table 1: Relative `2-norm of errors, as defined in Eq. (2), in the PINNs predictions with respect to the reference data for all the test cases. The dash symbol in the table denotes that the corresponding variable is not calculated in that test case.

| Test FSBL ZPG | E U 0.07 1.02 | E V 0.12 4.25 | E P 0.001 – | E u 2 – – | E uv – 6.46 | E v 2 – – |
|---------------|---------------|---------------|-------------|-----------|-------------|-----------|
| APG           | 0.28          | 1.57          | 4.60        | –         | 7.96        | –         |
| NACA4412      | 1.56          | 2.17          | 7.30        | 9.43      | 11.36       | 4.69      |
| Periodic hill | 2.77          | 19.70         | 8.61        | 28.18     | 16.70       | 20.24     |

### Falkner–Skan boundary layer (FSBL)

As the first test case, we solve two-dimensional Navier–Stokes equations for the Falkner–Skan boundary layer at Re = 100 using PINNs to show the applicability of PINNs for the laminar boundary layer flows. We consider a boundary layer with adversepressure-gradient with $^{m}$ $^{=}$ −0.$^{08}$ leading to $^{β}$ FS $^{=}$ $^{2}$m/($^{m}$ + 1) = −0.$^{1739}$ where $^{β}$ FS $^{=}$ −0.$^{1988}$ corresponds to separation. The inputs of the PINN model are x and y and the outputs are the velocity components and the pressure. We only use the data on the domain boundaries for the velocity components for supervised learning. The reference data is obtained from the analytical solution. The FNN comprises 8 hidden layers, each containing 20 neurons with hyperbolic tangent function (tanh) as the activation function. We first use the Adam optimizer (Kingma and Ba, 2017) for the training of the model and then apply Broyden– Fletcher–Goldfarb–Shanno (BFGS) algorithm to obtain a more accurate solution. The optimization process of the BFGS algorithm is stopped automatically based on the increment tolerance. Similar model architecture and training procedures are implemented for the simulation of other test cases using PINNs.

Results are illustrated in Figure 2 as the contours of U, V , and P obtained from PINN predictions (left) and reference data (right). The relative `2-norm of errors are reported in Table 1. Our results suggest that excellent predictions can be obtained using PINNs for laminar boundary layer flows. It can be seen in Figure 2 that although we only use velocity components on the domain boundaries as the training data, the PINN model provides accurate predictions for the pressure.

## ZPG turbulent boundary layer

For the ZPG boundary layer we employ the simulation data of Eitel-Amor et al. (2014) for a domain range of 1, 000 < $Re_\theta$ < 7, 000, where $Re_\theta$ = θU∞/ν represents the Reynolds number based on the momentum thickness θ, the free-stream velocity U∞,

![](_page_3_Figure_0.jpeg)

Figure 4: Simulation results of the APG turbulent boundary layer using PINNs in comparison with the reference data. (a) Contours of U, V , uv, and P from top to bottom, respectively. (b) Shape factor H$^{12}$ (top) and skin-friction coefficient c$^{f}$ (bottom). (d) Inner-scaled mean streamwise velocity U $^{+}$(top) and Reynolds-stress uv$^{+}$ (bottom) profiles at $Re_\theta$ = 1623, 2138, and 2588. Dashed and solid lines represent, respectively, the PINN predictions and the reference data. Darker color shows higher Reθ.

and the kinematic viscosity ν. For this test case, we consider continuity and streamwise momentum equations as the governing equations and the mean streamwise U and wall-normal V velocity components and the shear Reynolds-stress uv as the outputs of the model.

Results of the PINN simulation are depicted in Figure 3(a ∼ c) in comparison with the reference data. Figure 3(a) shows contours of U, V , and uv. The relative `2-norm of errors for U, V , and uv are 1.02%, 4.25%, and 6.46%, respectively, as reported in Table 1. The characteristics of the boundary layer are also quantified in terms of the shape factor, defined as the ratio of displacement and momentum thickness, H$^{12}$ = δ $^{*}$/θ, and the skin-friction coefficient c$^{f}$ = 2($u_\tau$ /U∞) 2 , where $u_\tau$ = p τw/ρ represents the friction velocity ($\tau_w$ is the mean wall-shear stress and ρ is the fluid density). The relevant velocity and length scales close to the wall are given by $u_\tau$ and ` $^{*}$ = ν/$u_\tau$ . The inner-scaled quantities are thus written as, *e.g.*, U $^{+}$ = U/$u_\tau$ and $y^+$ = y/`$^{*}$ . Figure 3(b) shows the shape factor H$^{12}$ and the skin-friction coefficient cf obtained from PINN predictions against the reference data. Moreover, Figure 3(c) depicts inner-scaled mean streamwise velocity U $^{+}$ and Reynolds-stress uv$^{+}$ profiles at three streamwise locations ($Re_\theta$ = 2500, 4000, and 5500) indicated by white dashed lines in Figure 3(a) (top left). Our results show excellent accuracy of the PINN simulation.

### APG turbulent boundary layer

As the next test case, we simulate the APG turbulent boundary layer for a Reynolds number range of 910 < $Re_\theta$ < 3360 and at a constant Clauser pressure-gradient parameter β = δ $^{*}$/τwdP∞/dx ' 1 where P$^{∞}$ is the free stream pressure (Bobke et al., 2017). For this test case, we consider a PINN model with 8 hidden layers, each containing 20 neurons, and continuity and streamwise and wall-normal momentum equations as the governing equations. We observe that, even in the presence of adverse pressure gradient, excellent predictions can be obtained using PINNs as it is shown in Figure 4 where we compared the predictions with the reference data. It can be seen in Figure 4(a) that although we do not use any turbulence model, the predictions for the shear Reynolds stress uv coincide with the reference data. The relative `2-norm of errors are reported in Table 1 where the lowest and the highest errors are related to U and uv and are equal to 0.28% and 7.96%, respectively. Figure 4(b) shows the accuracy of the PINN predictions against the reference data in terms of boundary layer characteristics, i.e., H$^{12}$ (top) and c$^{f}$ (bottom). Moreover, Figure 4(c) depicts the inner-scaled streamwise velocity (top) and Reynolds-stress (bottom) obtained from the PINN predictions and the reference data at three different $Re_\theta$ of 1623, 2138, and 2588. Our results show that the PINN model can provide accurate predictions for the APG turbulent boundary layer.

#### NACA4412 airfoil

Next, we use PINNs for simulation of the turbulent boundary layer developing on the suction side of a NACA4412 airfoil at the Reynolds number based on U$^{∞}$ and chord length c of $Re_c$ = U∞c/ν = 200, 000. The data for the training and testing of the model is employed from the work by Vinuesa et al. (2018) where results were obtained based on well-resolved large-eddy simulations (LESs) using a spectral-element method. We consider a domain range of 0.5 < x/c < 1 and a PINN model with 8 hidden layers, each with 20 neurons. Two-dimensional RANS equations are considered as the governing equations. For this test case, we use the wall-normal based spatial coordinates x$^{n}$ and y$^{n}$ as the inputs of the FNN and U, V , P, u $^{2}$, uv, and v $^{2}$ as the outputs. Results are reported as the profiles of the inner-scaled streamwise velocity and Reynolds-stress components at x/c ' 0.625, 0.75, and 0.875 in Figure 5. Our results show an excellent agreement between the PINN predictions and the reference data both for velocity and Reynolds-stress components. Table 1 shows the relative `2-norm of errors in the PINN predictions. It can be seen that for mean-velocity components U and V , the error is less than 3%. The highest error is related to uv, and it is equal to 11.36%.

![](_page_4_Figure_2.jpeg)

Figure 5: Simulation results of turbulent boundary layer over the suction side of a NACA4412 airfoil at $Re_c$ = 200, 000 using PINNs in comparison with the reference data at x/c ' 0.625, 0.75, and 0.875. (a) Inner-scaled streamwise velocity profile U $^{+}$. (b, c, d) Profiles of the inner-scaled Reynoldsstress components uv$^{+}$, u$^{2}$ + , and v 2 + , respectively. Dashed and solid lines represent, respectively, the PINN predictions and the reference data. Darker color shows higher x/c.

#### Periodic hill

At last, we evaluate the performance of our proposed framework for solving RANS equations using PINNs in the simulation of the turbulent flow over a periodic hill at the Reynolds number Re$^{b}$ = 2, 800 based on the crest height H and the bulk velocity U$^{b}$ at the crest. The training and testing data are obtained from DNS simulation using a spectral-element method. For this test case, we consider a domain range of 1 < x/H < 5 as it is depicted in Figure 6 by the grey dashed lines. Similar to the previous test cases, the data on the domain boundaries are used for the training of a PINN model with 8 hidden layers, each containing 20 neurons where twodimensional RANS equations are considered as the

![](_page_4_Figure_0.jpeg)

Figure 6: Simulation results of the turbulent flow over a periodic hill at Re$^{b}$ = 2, 800 using PINNs in comparison with the reference data. (a) Contour of U and flow streamlines for the PINN simulation (left) and the reference data (right). (b) U profiles at five different streamwise locations.

governing equations. Figure 6(a) shows the streamwise velocity U contour and the flow streamlines for the PINN predictions (left) and the reference data (right). It can be observed that the PINN model is able to simulate the separated flow without a turbulence model and only by using the data on the domain boundaries and the RANS equations as the governing equations. It should be noted that the velocity and Reynolds-stress components on the top and bottom boundaries are equal to zero due to the no-slip condition. Therefore, we only need the data at the input and output boundaries and pressure on all the boundaries for the supervised learning. Figure 6(b) illustrates the streamwise velocity profiles at five different streamwise locations for the PINN predictions and the reference data. Our results show an excellent agreement between the PINN predictions and the reference data. It can be seen in Figure 6 that the extent of the separated region and the reattachment point are accurately predicted by the PINN model. The relative `2-norm of errors are reported in Table 1. The lowest error is related to U, and it is equal to 2.77%. The highest error is equal to 28.18% and is associated with u 2.

# 4 Conclusions

We introduced an alternative approach based on PINNs for solving the RANS equations. In contrast to traditional methods, we solve the RANS equations for incompressible turbulent flows without any specific model or assumption for turbulence and through

- the use of the data on the domain boundaries (including Reynolds-stress components) along with the governing equations that guide the learning process towards the solution. We simulate the Falkner–Skan boundary layer with adverse pressure gradient using PINNs to show the applicability of the model for laminar boundary layer flows. In this case, we only used the data on the boundaries for the velocity components as the training data. Our results suggest the applicability of PINNs for laminar boundary layer flows where excellent predictions can be obtained, even for the pressure. Moreover, we applied PINNs for the simulation of ZPG and APG turbulent boundary layers, and turbulent flows over the NACA4412 airfoil and the periodic hill. We only used the data on the domain boundaries, including Reynolds-stress components, for supervised learning while we considered the residual of the RANS equations as the loss for unsupervised learning. A set of points inside the domain and the points on the domain boundaries are employed to evaluate the residual of the governing equations. From these points we predict the mean-flow quantities. For the points on the boundaries we calculate the supervised loss by comparing the predictions with the training data while for all the points we compute the residuals by constructing the RANS equations using AD. For ZPG and APG boundary layers, we obtained excellent predictions using PINNs where the average relative `2-norm of errors are equal to 3.91% and 3.60%, respectively. Our results for the NACA4412 airfoil and the periodic hill show that PINNs can provide accurate predictions for the streamwise velocity with less than 3% error while leading to good accuracy even in the simulation of Reynolds-stress components. Acknowledgments RV acknowledges the Goran Gustafsson founda- ¨ tion for supporting this research. HE acknowledges the support of the University of Tehran. References
- R. Vinuesa, H. Azizpour, I. Leite, M. Balaam,
  - V. Dignum, S. Domisch, A. Fellander, S. D. Lang- ¨ hans, M. Tegmark, and F. Fuso Nerini, Nat. Commun. 11, 233 (2020).
- J. N. Kutz, J. Fluid Mech. 814, 1 (2017).
- K. Duraisamy, G. Iaccarino, and H. Xiao, Annu. Rev. Fluid Mech. 51, 357 (2019).
- S. L. Brunton, B. R. Noack, and P. Koumoutsakos, Annu. Rev. Fluid Mech. 52, 477 (2020).
- J. Ling, A. Kurzawski, and J. Templeton, J. Fluid Mech. 807, 155–166 (2016).
- C. Jiang, R. Vinuesa, R. Chen, J. Mi, S. Laima, and
  - H. Li, Phys. Fluids 33, 055133 (2021).
- P. A. Srinivasan, L. Guastoni, H. Azizpour, P. Schlatter, and R. Vinuesa, Phys. Rev. Fluids 4, 054603 (2019).
- H. Eivazi, L. Guastoni, P. Schlatter, H. Azizpour, and
- R. Vinuesa, Int. J. Heat Fluid Flow 90, 108816 (2021).
- T. Murata, K. Fukami, and K. Fukagata, J. Fluid Mech. 882, A13 (2020).
- H. Eivazi, H. Veisi, M. H. Naderi, and V. Esfahanian, Phys. Fluids 32, 105104 (2020).
- J. Jimenez, J. Fluid Mech. ´ 854, R1 (2018).
- L. Guastoni, A. Guemes, A. Ianiro, S. Discetti, ¨
  - P. Schlatter, H. Azizpour, and R. Vinuesa (2020), <arXiv:2006.12483>.
- A. Guemes, H. Tober, S. Discetti, A. Ianiro, B. Sir- ¨ macek, H. Azizpour, and R. Vinuesa, Phys. Fluids (2021), <arXiv:2103.07387>.
- H. Tang, J. Rabault, A. Kuhnle, Y. Wang, and T. Wang, Phys. Fluids 32, 053605 (2020).
- M. Raissi, P. Perdikaris, and G. Karniadakis, J. Comput. Phys. 378, 686 (2019a).
- M. Raissi, Z. Wang, M. S. Triantafyllou, and G. E. Karniadakis, J. Fluid Mech. 861, 119–137 (2019b).
- M. Raissi, A. Yazdani, and G. E. Karniadakis, Science 367, 1026 (2020).
- M. F. Fathi, I. Perez-Raya, A. Baghaie, P. Berg,
  - G. Janiga, A. Arzani, and R. M. D'Souza, Comput Methods Programs Biomed 197, 105729 (2020), ISSN 0169-2607.
- A. Arzani, J.-X. Wang, and R. M. D'Souza (2021), <arXiv:2104.08249>.
- X. Jin, S. Cai, H. Li, and G. E. Karniadakis, J. Comput. Phys. 426, 109951 (2021).
- G. E. Karniadakis, I. G. Kevrekidis, L. Lu,
  - P. Perdikaris, S. Wang, and L. Yang, Nat. Rev. Phys 3, 422 (2021), ISSN 2522-5820.
- A. G. Baydin, B. A. Pearlmutter, A. A. Radul, and
  - J. M. Siskind (2018), <arXiv:1502.05767>.
- M. Abadi et al., In Proc. 12th USENIX Symposium on Operating Systems Design and Implementation (OSDI '16) 16, 265 (2016).
- G. Eitel-Amor, R. Orl ¨ u, and P. Schlatter, Int. J. Heat ¨ Fluid Flow 47, 57 (2014).
- A. Bobke, R. Vinuesa, R. Orl ¨ u, and P. Schlatter, J. ¨ Fluid Mech. 820, 667–692 (2017).
- R. Vinuesa, P. Negi, M. Atzori, A. Hanifi, D. Henningson, and P. Schlatter, Int. J. Heat Fluid Flow 72, 86 (2018).
- D. P. Kingma and J. Ba (2017), <arXiv:1412.6980>.