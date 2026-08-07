# A transformer-based synthetic-inflow generator for spatially-developing turbulent boundary layers

Mustafa Z. Yousif$^{1}$ , Meng Zhang$^{1}$ , Linqi Yu$^{1}$ , Ricardo Vinuesa$^{2}$ and HeeChang Lim1,†

$^{1}$School of Mechanical Engineering, Pusan National University, 2, Busandaehak-ro 63beon-gil, Geumjeong-gu, Busan, 46241, Rep. of KOREA

$^{2}$FLOW, Engineering Mechanics, KTH Royal Institute of Technology, Stockholm, Sweden

(Received xx; revised xx; accepted xx)

This study proposes a newly-developed deep-learning-based method to generate turbulent inflow conditions for spatially-developing turbulent boundary layer (TBL) simulations. A combination of a transformer and a multiscale-enhanced super-resolution generative adversarial network is utilised to predict velocity fields of a spatially-developing TBL at various planes normal to the streamwise direction. Datasets of direct numerical simulation (DNS) of flat plate flow spanning a momentum thickness-based Reynolds number, $Re_\theta$ = 661.5 – 1502.0, are used to train and test the model. The model shows a remarkable ability to predict the instantaneous velocity fields with detailed fluctuations and reproduce the turbulence statistics as well as spatial and temporal spectra with commendable accuracy as compared with the DNS results. The proposed model also exhibits a reasonable accuracy for predicting velocity fields at Reynolds numbers that are not used in the training process. With the aid of transfer learning, the computational cost of the proposed model is considered to be effectively low. Furthermore, applying the generated turbulent inflow conditions to an inflow-outflow simulation reveals a negligible development distance for the TBL to reach the target statistics. The results demonstrate, for the first time that transformer-based models can be efficient in predicting the dynamics of turbulent flows. It also shows that combining these models with generative adversarial networks-based models can be useful in tackling various turbulence-related problems, including the development of efficient synthetic-turbulent inflow generators.

# 1. Introduction

The generation of turbulent inflow conditions is essential in simulating spatiallydeveloping turbulent boundary layers (TBLs), considering its effect on the accuracy of the simulations and computational cost. It is also a challenging topic due to the need for the time-dependent turbulent inflow data to be accurately described. The generated data should satisfy the momentum and continuity equations and consequently match the turbulent statistics and spectra of the flow. Several approaches have been proposed to generate turbulent inflow conditions with different levels of success (Wu 2017). Adding infinitesimal perturbations on the laminar mean velocity profile at the inlet section of the computational domain and allowing the transition of the boundary layer is a straightforward approach that guarantees a realistic spatially-developing TBL. However, the need for a development distance that is long enough for the flow to

reach the fully-turbulent state can result in a high computational cost, making this approach not applicable for most turbulence simulations, where fully-turbulent inflow conditions are required. The use of precursor (auxiliary) parallel flow (fully developed flow) simulations with periodic boundary conditions applied to the streamwise direction is another approach that can be used by extracting flow fields from a plane normal to the streamwise direction and applying the data as inflow conditions to the main simulations. Although this method can produce accurate turbulence statistics and spectra for fully developed flows, it requires a high computational cost. Additionally, the streamwise periodicity effect, caused by the recycling of the flow within a limited domain size, can lead to physically unrealistic streamwise-repetitive features in the flow fields (Wu 2017). Furthermore, using parallel flow data as inflow for a simulation of a spatially-developing TBL can result in a long development distance downstream of the domain inlet to produce the correct boundary layer characteristics (Lund 1993).

To address this issue, a recycling-rescaling method was introduced by Lund et al. (1998), which is a modified version of the method by Spalart (1988). Here the velocity fields in the auxiliary simulation are rescaled before being reintroduced at the inlet section. Another well-known approach for generating turbulent inflow conditions is adding random fluctuations based on known turbulence statistics. The methods that are based on this approach are usually called synthetic turbulent inflow generation methods. Several methods, such as the synthetic random Fourier method (Le et al. 1997), synthetic digital filtering method (Klein et al. 2003), synthetic coherent eddy method (Jarrin et al. 2006), synthetic vortex method (Sergent 2020; Mathey et al. 2006; Yousif & Lim 2021), synthetic volume-force method (Schlatter & Orl¨u ¨ 2012; Spille-Kohoff & Kaltenbach 2001) and numerical counterpart of the experimental tripping methods (Sanmiguel Vila et al. 2017) have been proposed to feature a fast generation of turbulence with various levels of precision. However, a long-distance downstream of the domain inlet is required to allow the boundary layer to recover from the unphysical random fluctuations of the generated velocity fields and produce the right flow characteristics, resulting in a high computational cost. Another approach based on proper orthogonal decomposition (POD) and Galerkin projection has been proposed to build a reduced-order flow model and generate turbulent inflow conditions by utilising the most energetic eddies (Johansson & Andersson 2004). A similar approach has been applied to experimental measurements (Druault et al. 2004; Perret et al. 2008) to reconstruct turbulent inflow velocity fields from hot-wire anemometry and particle image velocimetry using POD and linear stochastic estimation. This approach showed the possibility of utilising the experimental results as turbulent inflow conditions. However, the costly experimental setup makes this approach not applicable as a general method to generate turbulence.

The rapid development of deep learning algorithms and the increase in the graphic processing unit (GPU) capability, accompanied by the enormous amounts of high-fidelity data generated from experimental and numerical simulations, encourage exploring new data-driven approaches that can efficiently tackle various fluid-flow problems (Brunton et al. 2020; Kutz 2017; Vinuesa & Brunton 2021). Deep learning is a subset of machine learning, where deep neural networks are used for classification, prediction and feature extraction (LeCun et al. 2015). Recently, several models have shown great potential in solving different problems in the field of turbulence, such as turbulence modelling (Duraisamy et al. 2019; Wang et al. 2017), turbulent flow prediction (Lee & You 2019; Srinivasan et al. 2019), reduced-order modelling (Nakamura et al. 2021; Yousif & Lim 2022), flow control (Fan et al. 2020; Park & Choi 2020; Rabault et al. 2019; Vinuesa et al. 2022), non-intrusive sensing (Guastoni et al. 2021; G¨uemes et al. 2021) and turbulent flow reconstruction (Deng et al. 2019; Eivazi et al. 2022; Fukami et al. 2019a; Kim et al. 2021; Yousif et al. 2021, 2022b).

Furthermore, recent studies on the generation of turbulent inflow conditions using deep learning models (DLMs) have shown promising results. Fukami et al. (2019b) showed that convolutional neural networks (CNNs) could be used to generate turbulent inflow conditions by proposing a model based on a convolutional autoencoder (CAE) with a multilayer perceptron (MLP) to generate turbulent inflow conditions using turbulent channel flow data. Kim & Lee (2020) proposed a generative adversarial network (GAN) and a recurrent neural network (RNN)-based model as a representative of unsupervised deep learning to generate turbulent inflow conditions at various Reynolds numbers using data of turbulent channel flow at various friction Reynolds numbers. Recently, Yousif et al. (2022a) utilised a combination of a multiscale CAE with a subpixel convolution layer ( MSCSP-AE ) having a physical constrains-based loss function and a long shortterm memory (LSTM) model to generate turbulent inflow conditions from turbulent channel flow data.

In all the above models, the prediction of the turbulent inflow conditions is based on parallel flows, which, as mentioned before, is more suitable as inflow for fully developed TBLs. Therefore, it is necessary to develop a model that considers the spatial development of TBLs (Jim´enez et al. 2010). In this context, this paper proposes a deep learning method consisting of a transformer and a multiscale-enhanced super-resolution generative adversarial network (MS-ESRGAN) to generate turbulent inflow conditions for spatiallydeveloping TBL simulations.

The remainder of this paper is organised as follows. In Section 2, the methodology of generating the turbulent inflow data using the proposed DLM is explained. The datasets used for training and testing the model are described in Section 3. Section 4 presents the results obtained from testing the proposed model. Finally, Section 5 presents the conclusions.

### 2. Methodology

The proposed DLM is a combination of two architectures. The first one is the transformer (Vaswani et al. 2017) and the second one is the MS-ESRGAN (Yousif et al. 2021). The transformer is used to predict the temporal evolution of extremely coarse velocity fields obtained by selecting distributed points at various sections along the streamwise direction of a spatially-developing TBL flow, as shown in figure 1(a). Here the flow data are obtained through direct numerical simulation (DNS). Meanwhile, the MS-ESRGAN is used to perform a super-resolution reconstruction of the data for all the sections predicted by the transformer, leading to a final high-resolution (HR) data, i.e. velocity fields with the same resolution as the ground truth data, as shown in figure 1(b). In other words, the transformer is trained for the data at each section, whereas MS-ESRGAN is trained for all the sections used in the training process. Figure 1(c) shows the schematic representation of the proposed DLM for generating turbulent inflow conditions. As shown in the figure, the input to the DLM is represented by coarse velocity data obtained from a plane normal to the streamwise direction with time interval [t0, ..., tn], and the output is represented by predicted high-resolution velocity data at instants, tn+1, where n is set to 12 in this study.

In this study, the open-source library TensorFlow 2.4.0 (Abadi et al. 2016) is used for the implementation of the presented model. The source code of the model is available on the following web page:

![](_page_3_Diagram_0.jpeg)

Figure 1. Schematic of (a) training procedure for the transformer, (b) training procedure for the MS-ESRGAN and (c) turbulent inflow generation using the proposed DLM.

Click the link: <https://fluids.pusan.ac.kr/fluids/65416/subview.do>

#### 2.1. Transformer

LSTM (Hochreiter & Schmidhuber 1997) is an artificial neural network that can handle sequential data and time-series modelling. LSTM is a type of RNN (Rumelhart et al. 1986). It has also played an essential role in modelling the temporal evolution of turbulence in various problems (Eivazi et al. 2021; Kim & Lee 2020; Nakamura et al. 2021; Srinivasan et al. 2019; Yousif & Lim 2022). Although LSTM is designed to overcome most of the traditional RNN limitations, such as vanishing gradients and explosion of gradients (Graves 2012), it is usually slow in terms of training due to its architecture, which requires that the time-series data are introduced to the network sequentially. This prevents parallelisation of the training process, which is why GPU is used in deep learning calculations. Furthermore, LSTM has shown a limitation in dealing with long-range dependencies.

The transformer (Vaswani et al. 2017) was introduced to deal with these limitations by applying the self-attention concept to compute the representations of its input and output data without feeding the data sequentially. In this study, a transformer is used to model the temporal evolution of the velocity fields that represent the turbulent inflow data.

Figure 2 shows the transformer used in this study. Similar to the original transformer proposed by Vaswani et al. (2017), it has two main components: encoder and decoder. The inputs of both components are passed through a positional encoding using sine and cosine functions, which can encode the order information of the input data into a vector and add it directly to the input vector. The encoder consists of six stacked encoder layers. Each layer contains a multi-head self-attention sublayer and a feed-forward sublayer. The input of the multi-head self-attention sublayer consists of queries (Q), keys (K), and values (V ). Note that attention is a function that can map a query and set of keyvalue pairs to output, where the queries, keys, values and output are all vectors. The output can be calculated as the weighted sum of the values. The attention function is represented by scaled dot-product attention, which is an attention mechanism with the dot products are scaled down by √ dk, where d$^{k}$ is the dimension of Q, K and it is equal to the dimension of V , i.e. dv.

The scaled dot-product attention is calculated as follows:

| Attention( $Q, K, V$ ) = softmax $\left( \frac{QK^T}{\sqrt{d_k}} \right) V$ , | (2.1) |
|-------------------------------------------------------------------------------|-------|
|-------------------------------------------------------------------------------|-------|

where softmax is a function that takes an input vector and normalizes it to a probability distribution so that the output vector has values that sum to 1 (Goodfellow et al. 2014). In the multi-head self-attention sublayer, d$^{v}$ = dmodel/h, where dmodel and h are the dimension of the input data to the model and number of heads, respectively.

The multi-head attention allows the model to jointly attend to information from different representation subspaces at different positions such that

Multi – Head(
$$Q, K, V$$
) =  $Concat(head_1, ..., head_h) W^o$ , (2.2)

$$head_i = \text{Attention}\left(QW_i^Q, KW_i^K, VW_i^V\right), \quad (2.3)$$

where W Q i , W $^{K}$ i and W$^{V}$ i are the weights corresponding to Q, K, V at every head, respectively; W$^{o}$ represents the weights of the concatenated heads. W Q $^{i}$ ∈ $^{R}$ $^{d}$model×d$^{k}$ , W $^{K}$ $^{i}$ ∈ $^{R}$ $^{d}$model×d$^{k}$ , W$^{V}$ $^{i}$ ∈ $^{R}$ $^{d}$model×d$^{v}$ and W$^{o}$ ∈ $^{R}$ hdv×dmodel .

The multi-head self-attention sublayer contains six heads of scaled dot-product attention.

A residual connection (He et al. 2016) is applied around the multi-head attention, followed by layer normalisation (Ba et al. 2016).

The second part of the encoder layer, i.e. the feed-forward sublayer, contains two dense layers with linear and rectified linear unit (ReLU) activation functions. This layer projects the vector to a larger space, where it is easier to extract the required information and then projects it back to the original space. As in the multi-head self-attention sublayer, a residual connection is employed before applying layer normalisation.

Similar to the encoder, the decoder contains six decoder layers. In addition to the multihead self-attention and feed-forward sublayers, the decoder layer has a third sublayer that performs multi-head attention over the output of the encoder stack. Furthermore, the multi-head self-attention sublayer is changed to a masked multi-head self-attention sublayer, as shown in figure 2, which is similar to the multi-head self-attention sublayer with the difference that the scaled dot-product attention is changed to a masked scaled dot-product attention (Vaswani et al. 2017). The masking operation ensures that the prediction can only depend on the known outputs, a fact that prevents later information leakage. In this study, the dropout technique is applied to every sublayer before the residual connection and the rate of dropout is set to 0.1.

![](_page_5_Diagram_1.jpeg)

Figure 2. Architecture of the transformer. The dashed line box represents the scaled dot-product attention.

The square of the L$^{2}$ norm error is chosen as a loss function for the transformer such that

---

$$\mathcal{L}_{transformer} = \frac{1}{M} \sum_{m=1}^M \|Output_m - Target_m\|_2^2 \quad (2.4)$$

where Output and T arget represent the output from the transformer and ground truth data, respectively, at a specific time step, m. M represents the size of the training mini-batch, which is set to 64. The adaptive moment estimation (Adam) optimisation algorithm (Kingma & Ba 2017) is used to update the weights of the model.

#### 2.2. MS-ESRGAN

GANs (Goodfellow et al. 2014) have shown great success in image transformation and super-resolution problems (Ledig et al. 2017; Mirza & Osindero 2014; Wang et al. 2018; Zhu et al. 2017). GAN-based models have also shown promising results in reconstructing HR turbulent flow fields from coarse data (Fukami et al. 2021, 2019a; G¨uemes et al. 2021; Kim et al. 2021; Yousif et al. 2021, 2022b). In a GAN model that is used for image generation, two adversarial neural networks called the generator (G) and the discriminator (D) compete with each other. G tries to generate artificial images with the same statistical properties as those of the real ones, whereas D tries to distinguish the artificial images from the real ones. After successful training, G should be able to

![](_page_6_Diagram_1.jpeg)

Figure 3. Architecture of MS-ESRGAN. (a) The generator, where β is the residual scaling parameter which is set to 0.2 in this study, and (b) the discriminator.

generate artificial images that are difficult to distinguish by D. This process can be expressed as a min-max two-player game with a value function V (D, G) such that

$$Q_G^{min} \frac{m}{D} V(D, G) = \mathbb{E}_{x_r \sim P_{data}(x_r)} [\log D(x_r)] + \mathbb{E}_{\xi \sim P_{\xi}(\xi)} [\log(1 - D(G(\xi)))], \quad (2.5)$$

where x$^{r}$ is the image from the ground truth data (real image) and Pdata(xr) is the real image distribution. E represents the operation of calculating the average of all the data in the training mini-batch. In the second right term of equation 2.5, ξ is a random vector used as an input to G and D(xr) represents the probability that the image is real and not generated by the generator. The output from G, i.e. G(ξ), is expected to generate an image that is similar to the real one, such that the value of D(G(ξ)) is close to 1. Meanwhile, D(xr) returns a value close to 1, whereas D(G(ξ)) returns a value close to 0. Thus, in the training process, G is trained in a direction that minimises V (D, G), whereas D is trained in a direction that maximises V (D, G).

In this study, MS-ESRGAN (Yousif et al. 2021) is used to perform super-resolution reconstruction of the velocity fields predicted by the transformer. MS-ESRGAN is based on the enhanced super-resolution GAN (ESRGAN) (Wang et al. 2018). Figure 3 shows the architecture of MS-ESRGAN. As shown in figure 3(a), G consists of a deep CNN represented by residual in residual dense blocks (RRDBs) and multiscale parts (MSP). Note that the input to G is low-resolution data, which are first passed through a convolutional layer and then through a series of RRDBs. The MSP, consisting of three parallel convolutional sub-models with different kernel sizes, is applied to the data features extracted by RRDBs. More details for MSP can be found in Yousif et al. (2021, 2022b). The outputs of the three sub-models are summed and passed through a final convolutional layer to generate HR artificial data (xa). Figure 3(b) shows that the artificial and real data are fed to D and passed through a series of convolutional, batch normalisation and leaky ReLU layers. As a final step, the data are crossed over a convolutional layer. The non-transformed discriminator outputs using the real and artificial data, i.e. C(xr) and C(xa), are used to calculate the relativistic average discriminator value DRa (Jolicoeur-Martineau 2018):

$$D_{Ra}(x_r, x_a) = \sigma(C(x_r)) - \mathbb{E}_{x_a} [C(x_a)], \quad (2.6)$$

$$D_{Ra}(x_a, x_r) = \sigma(C(x_a)) - \mathbb{E}_{x_r} [C(x_r)], \quad (2.7)$$

where σ is the sigmoid function. In equations 2.6 and 2.7, DRa represents the probability that the output from D using the real image is relatively more realistic than the output using the artificial image.

Then, the discriminator loss function is defined as follows:

$$\ell_D^{\text{rea}} = -\mathbb{E}_{x_r} [\log(D_{Ra}(x_r, x_a))] - \mathbb{E}_{x_a} [\log(1 - D_{Ra}(x_a, x_r))]. \quad (2.8)$$

The adversarial loss function of the generator can be expressed in a symmetrical form as follows:

$$\mathcal{E}_G^{\text{ra}} = -\mathbb{E}_{x_r} [\log(1 - D_{Ra}(x_r, x_a))] - \mathbb{E}_{x_a} [\log(D_{Ra}(x_a, x_r))]. \quad (2.9)$$

The total loss function of the generator is defined as

$$\mathcal{L}_G = \ell_G^{Ra} + \beta \ell_{pixel} + \ell_{perceptual}, \quad (2.10)$$

where `pixel is the error calculated based on the pixel difference of the generated and ground truth data; `perceptual represents the difference between features that are extracted from the real and the artificial data. The pre-trained CNN VGG-19 (Simonyan & Zisserman 2015) is used to extract the features using the output of three different layers (Yousif et al. 2021). Here, β is a weight coefficient and its value is set to be 5000. The square of the L$^{2}$ norm error is used to calculate `pixel and `perceptual. The size of the mini-batch is set to 32. As in the transformer model, the Adam optimisation algorithm is used to update the weights of the model.

#### 3. Data description and pre-processing

The transitional boundary layer database (Lee & Zaki 2018) available at the Johns Hopkins turbulence databases (JHTDB) is considered in this study for the training and testing of the DLM. The database was obtained via DNS of incompressible flow over a flat plate with an elliptical leading edge. In the simulation, the half-thickness of the plate L and the free stream velocity U$^{∞}$ are used as a reference length and velocity. Additionally, x, y and z are defined as the streamwise, wall-normal and spanwise coordinates, respectively, with the corresponding velocity components u, v, and w. Note that the same definitions of the coordinates and velocity components are used in this study.

In the simulation, the length of the plate, L$^{x}$ = 1, 050L measured from the leading edge (x = 0), the domain height, L$^{y}$ = 40L and the width of the plate, L$^{z}$ = 240L. The stored database in JHTDB is in the range x ∈ [30.2185, 1000.065]L, y ∈ [0.0036, 26.488]L,

| Re θ | 661 5 | 905 7 | 1362 0 |
|------|-------|-------|--------|
| DNS  | 1 458 | 1 457 | 1 453  |
| DLM  | 1 415 | 1 423 | 1 429  |

Table 1. Shape factor values of the DNS and predicted planes by the DLM.

and z ∈ [0, 240]L. The corresponding number of grid points is N$^{x}$ × N$^{y}$ × N$^{z}$ = 3320 × 224 × 2048 ≈ 1.5 × 10$^{9}$ . The database time step is ∆t = 0.25L/U∞. The stored database spans the following range in momentum-thickness-based Reynolds number, $Re_\theta$ = U∞θ/ν ∈ [105.5, 1502.0], where θ represents the momentum thickness and ν is the kinematic viscosity. More details for the simulation and database can be found in Lee & Zaki (2018) and on the website of JHTDB.

In this study, the datasets within the range of $Re_\theta$ ∈ [661.5, 1502.0] are considered for training and testing the DLM. This range of $Re_\theta$ in the database represents the fullyturbulent part of the flow (Lee & Zaki 2018). Datasets of the velocity components are collected from various (y − z) planes along the streamwise direction, with the number of snapshots = 4700 for every plane. To reduce the computational cost, the original size of each plane, N$^{y}$ × N$^{z}$ = 224 × 2048 is reduced to 112 × 1024. Furthermore, to increase the amount of training and testing data, every selected plane is divided into four identical sections along the spanwise direction, resulting in N$^{y}$ × N$^{z}$ = 112 × 256 for each section. To obtain the coarse data, the size of the data is further reduced to N$^{y}$ × N$^{z}$ = 14 × 32, which is obtained by selecting distributed points in the fields. The distribution of the points is obtained in a stretching manner such that more points can be selected near the wall. A time series of 4000 snapshots for each section are used to train the DLM, resulting in a total number of training snapshots = 4000×4×3 = 48000. The fluctuations of the velocity fields are used in the training and prediction processes. The input data to the DLM are normalised using the min-max normalisation function to produce values between 0 and 1.

### 4. Results and discussion

# 4.1. Results from the DLM trained at various $Re_\theta$

This section examines the capability of the proposed DLM to generate turbulent inflow data at three different Reynolds numbers for which the network has already been trained, $Re_\theta$ = 661.5, 905.7, and 1362.0. Figures 4-6 show the instantaneous streamwise velocity (u $^{+}$) and vorticity (ω + x ) fields of the DNS and the predicted data for three different time steps, where the superscript '+' denotes normalisation by viscous inner scale; in the figures, δ represents the boundary layer thickness. The figures show that the instantaneous flow fields can be predicted using the model with a commendable agreement with the DNS data. Note that the model has shown a capacity to predict the instantaneous flow fields for a long period of time, more than the one required for the flow data to reach a statistically stationary state (reaching fixed first and second-order statistics over time), i.e. for a number of time steps = 10000.

The shape factor (ratio of displacement to momentum thickness) values of the DNS and predicted planes are shown in table 1. A slight under-prediction can be seen in all the predicted values with the highest deviation of 2.95% at $Re_\theta$ = 661.5.

Figure 7 shows the probability density functions (p.d.f.) of the velocity components

![](_page_9_Figure_1.jpeg)

Figure 4. Instantaneous (a) streamwise velocity and (b) vorticity fields at $Re_\theta$ = 661.5, for three different instants. Reference (DNS) and predicted (DLM) data are shown.

![](_page_9_Figure_3.jpeg)

Figure 5. Instantaneous (a) streamwise velocity and (b) vorticity fields at $Re_\theta$ = 905.7, for three different instants. Reference (DNS) and predicted (DLM) data are shown.

(u $^{+}$, v $^{+}$, and w $^{+}$) plotted against the wall-normal distance ($y^+$). The figure shows that the p.d.f. plots of the generated velocity components are generally consistent with the p.d.f. plots obtained from the DNS data, indicating the capability of the model in predicting the velocity fields with distributions of the velocity components that are consistent with those of the DNS data.

Figures 8-10 compare the turbulence statistics of the generated velocity fields with the turbulence statistics of the DNS data. As shown in the figures, the mean streamwise velocity profile (U $^{+}$) for all the three Reynolds numbers shows excellent agreement with the results obtained from the DNS. The comparison of root-mean-square profiles

![](_page_10_Figure_1.jpeg)

Figure 6. Instantaneous (a) streamwise velocity and (b) vorticity fields at $Re_\theta$ = 1362.0, for three different instants. Reference (DNS) and predicted (DLM) data are shown.

![](_page_10_Figure_3.jpeg)

Figure 7. Probability density functions of the velocity components as a function of the wall-normal distance. The shaded contours represent the results from the DNS data and the dashed ones represent the results from the predicted data. The contour levels are in the range of 20%-80% of the maximum p.d.f. with an increment of 20%. (a) $Re_\theta$ = 661.5, (b) $Re_\theta$ = 905.7, (c) $Re_\theta$ = 1362.0.

![](_page_11_Figure_0.jpeg)

Figure 8. Turbulence statistics of the flow at $Re_\theta$ = 661.5. (a) Mean streamwise velocity profile. (b) Root-mean-square profiles of the velocity components. (c) Reynolds shear stress profile.

![](_page_11_Figure_2.jpeg)

Figure 9. Turbulence statistics of the flow at $Re_\theta$ = 905.7. (a) Mean streamwise velocity profile. (b) Root-mean-square profiles of the velocity components. (c) Reynolds shear stress profile.

![](_page_11_Figure_4.jpeg)

Figure 10. Turbulence statistics of the flow at $Re_\theta$ = 1362.0. (a) Mean streamwise velocity profile. (b) Root-mean-square profiles of the velocity components. (c) Reynolds shear stress profile.

of the velocity components (u + rms, v + rms, and w + rms) reveals good agreement with the results obtained from the DNS. However, the profile of the Reynolds shear stress (u 0v 0 + ) shows a slight under-prediction in the region between near the wall and the maximum Reynolds shear stress and the profile values in this region improve as the Reynolds number increases. This might be attributed to the fact that with the increase in the boundarylayer thickness, the effect of zero padding in the convolution processes is decreased in MS-ESRGAN, resulting in a better prediction of the velocity fields in this region of the boundary layer. These results are consistent with the results from table 1.

The capability of the proposed DLM to produce realistic spatial spectra of the velocity fields is investigated by employing the premultiplied spanwise wavenumber spectra,

![](_page_12_Figure_1.jpeg)

Figure 11. Premultiplied spanwise wavenumber energy spectra of the velocity components as a function of the wall-normal distance and the spanwise wavelength. The shaded contours represent the results from the DNS data and the dashed ones represent the results from the predicted data. The contour levels are in the range of 10%–90% of the maximum k + $^{z}$ Φ + αα with an increment of 10%. (a) $Re_\theta$ = 661.5, (b) $Re_\theta$ = 905.7, (c) $Re_\theta$ = 1362.0.

kzΦαα, where Φαα represents the spanwise wavenumber spectra, α represents the velocity component and k$^{z}$ is the spanwise wavenumber. Figure 11 shows the contour plots of k + $^{z}$ Φ + αα as a function of $y^+$ and the spanwise wavelength, λ + z . The figure shows that the spectra of the velocity components are generally consistent with those obtained from the DNS data with a slight deviation at the high wavenumbers. This indicates that the two-point correlations of the generated velocity components are consistent with those obtained from the DNS data, further supporting the excellent performance of the proposed DLM to properly represent the spatial distribution of the velocity fields. It is worth noting that the ability of the model to reproduce accurate spectra is essential in generating the turbulent inflow conditions to guarantee that the turbulence will be sustained after introducing the synthetic-inflow; otherwise, the generated inflow would require very long distances to reach "well-behaved" turbulent conditions, and these fluctuations could also dissipate.

To evaluate the performance of the proposed DLM to generate the velocity fields with accurate dynamics, the frequency spectra, φ + αα, as a function of $y^+$ and the frequency, f + are represented in figure 12. Note that the spectra obtained from the generated velocity fields show a commendable agreement with those of the DNS data, indicating that the

![](_page_13_Figure_1.jpeg)

Figure 12. Frequency spectra of the velocity components as a function of the wall-normal distance and the frequency. The shaded contours represent the results from the DNS data and the dashed ones represent the results from the predicted data. The contour levels are in the range of 10%–90% of the maximum φ + αα with an increment of 10%. (a) $Re_\theta$ = 661.5, (b) $Re_\theta$ = 905.7, (c) $Re_\theta$ = 1362.0.

proposed DLM can produce turbulent inflow conditions with a temporal evolution of the velocity fields that is consistent with that of the DNS.

### 4.2. Interpolation and extrapolation capability of the DLM

This section investigates the performance of the proposed DLM to generate turbulent inflow conditions at Reynolds numbers that are not used in the training process. The velocity fields at $Re_\theta$ = 763.8 and 1155.1 are used as examples of the velocity fields that fall between the Reynolds numbers used in the training process, i.e. the interpolation ability of the model is investigated using the flow fields at these Reynolds numbers.

Figure 13 shows the instantaneous streamwise velocity and vorticity fields for the flow at $Re_\theta$ = 763.8. It is worth noting that the transformer trained for the flow at the nearest Reθ, i.e. $Re_\theta$ = 661.5 is used to predict the temporal evolution of the velocity fields. The figure shows that the main features of the flow fields can be obtained with relatively good precision; however, the details of the predicted velocity fluctuations are not clearly shown. Similar results can be observed in figure 14 for the predicted velocity fields at $Re_\theta$ = 1155.1. Here, the current transformers trained for the flow at $Re_\theta$ = 905.7 and 1362.0 are used to predict the temporal evolution of the velocity fields.

The turbulence statistics of the flow at $Re_\theta$ = 763.8 and 1155.1 are shown in figures 15

![](_page_14_Figure_1.jpeg)

Figure 13. Instantaneous (a) streamwise velocity and (b) vorticity fields at $Re_\theta$ = 763.8, for three different instants. Reference (DNS) and predicted (DLM) data are shown.

![](_page_14_Figure_3.jpeg)

Figure 14. Instantaneous (a) streamwise velocity and (b) vorticity fields at $Re_\theta$ = 1155.1, for three different instants. Cases 1 and 2 represent the prediction using the transformer that is trained for the flow at $Re_\theta$ = 905.7 and 1362.0, respectively.

![](_page_15_Figure_0.jpeg)

Figure 15. Turbulence statistics of the flow at $Re_\theta$ = 763.8. (a) Mean streamwise velocity profile. (b) Root-mean-square profiles of the velocity components. (c) Reynolds shear stress profile.

![](_page_15_Figure_2.jpeg)

Figure 16. Turbulence statistics of the flow at $Re_\theta$ = 1155.1. Cases 1 and 2 represent the prediction using the transformer model trained for the flow at $Re_\theta$ = 905.7 and 1362.0, respectively. (a) Mean streamwise velocity profile. (b) Root-mean-square profiles of the velocity components. (c) Reynolds shear stress profile.

and 16, respectively. Although the mean streamwise velocity and the root-mean-square profiles of the spanwise and wall-normal velocity components show an ability of the DLM to predict reasonably well, the root-mean-square profile of the streamwise velocity component and the Reynolds shear stress show an under-prediction due to the lack of detailed information on the velocity fluctuations.

The extrapolation ability of the DLM is evaluated using the flow fields at $Re_\theta$ = 1502.0, which is higher than the maximum $Re_\theta$ used to train the transformer and MS-ESRGAN, i.e. $Re_\theta$ = 1362.0. The transformer trained for the flow at $Re_\theta$ = 1362.0 is used to predict the dynamics of the velocity fields. Figure 17 shows that the generated instantaneous streamwise velocity and vorticity fields generally have similar accuracy to the interpolated flow fields. Meanwhile, the turbulence statistics show a deviation from the DNS statistics, as shown in figure 18. This can be attributed to the lack of details of the velocity fluctuations and the extrapolation process that relies on the flow information at one Reynolds number compared with the interpolation process where the flow falls within the range of the Reynolds numbers that the MS-ESRGAN is trained for.

Finally, the accuracy of the spectral content of the interpolated and extrapolated velocity components is examined in figure 19 by employing the premultiplied spanwise wavenumber spectra. These results indicate that the spectra are produced with relatively good accuracy for the low-moderate wavenumbers.

![](_page_16_Figure_1.jpeg)

Figure 17. Instantaneous (a) streamwise velocity and (b) vorticity fields at $Re_\theta$ = 1502.0 for three different instants. Reference (DNS) and predicted (DLM) data are shown.

![](_page_16_Figure_3.jpeg)

Figure 18. Turbulence statistics of the flow at $Re_\theta$ = 1502.0. (a) Mean streamwise velocity profile. (b) Root-mean-square profiles of the velocity components. (c) Reynolds shear stress profile.

#### 4.3. Error analysis, transfer learning and computational cost

The performance of the proposed DLM is further statistically investigated using the L$^{2}$ norm error of the predicted data for all the Reynolds numbers used in this study,

$$\varepsilon = \frac{1}{J} \sum_{j=1}^J \frac{\|\alpha_j^{\text{DNS}} - \alpha_j^{\text{LDM}}\|_2}{\|\alpha_j^{\text{DNS}}\|_2} \quad (4.1)$$

where α DNS j and α DLM j represent the ground truth (DNS) and the predicted velocity components using the DLM, respectively, and J represents the number of the test snapshots.

Figure 20 shows that as the Reynolds number increases, no significant differences can be seen in the error values of the predicted velocity fields. However, as expected, the error shows higher values for the interpolated and extrapolated velocity fields compared with the error of the predicted velocity fields at the Reynolds numbers that the DLM is trained for. Additionally, in contrast with the aforementioned statistical results, the error

![](_page_17_Figure_1.jpeg)

Figure 19. Premultiplied spanwise wavenumber energy spectra of the velocity components as a function of the wall distance and wavelength. The shaded contours represent the results from the DNS data; the dashed-black contours represent the results from the predicted velocity data at $Re_\theta$ = 763.8 and 1502.0; the dashed-brown and grey contours represent the results from the velocity data at $Re_\theta$ = 1155.1 predicted using the transformer model trained for the flow at $Re_\theta$ = 905.7 and 1362.0, respectively. The contour levels are in the range of 10%-90% of the maximum k + $^{z}$ Φ + αα with an increment of 10%. (a) $Re_\theta$ = 763.8. (b) $Re_\theta$ =1155.1. (c) $Re_\theta$ =1502.0.

values are relatively high for the wall-normal and spanwise velocity fields. This indicates that the DLM has learned to model the structure of the flow with generally accurate turbulence statistics and spatio-temporal correlations, rather than reproducing the time sequence of the flow data. This observation is consistent with the results obtained by Fukami et al. (2019b); Kim & Lee (2020); Yousif et al. (2022a). Furthermore, using very coarse input data (7 × 16) in the training of the DLM shows a slight reduction in the model performance, indicating the capability of the DLM to generate the turbulent inflow data even if it is trained with very coarse input data.

It is worth mentioning that the transfer learning (TL) technique is used in this study (Guastoni et al. 2021; Yousif et al. 2022a, 2021). The weights of the transformer are sequentially transferred for every training (y−z) plane in the flow. First, the transformer is trained for the flow at the lowest Reynolds number, i.e. $Re_\theta$ = 661.5. After that, the weights of the model are transferred for the training using the next $Re_\theta$ data and so on. The results from using TL in this study show that with the use of only 25% of the training data for the transformer model, the computational cost (represented by the training time) can be reduced by 52% without affecting the prediction accuracy. These

![](_page_18_Figure_1.jpeg)

Figure 20. L$^{2}$ norm error of the predicted velocity fields. (a) Streamwise velocity. (b) Wall-normal velocity. (c) Spanwise velocity. Cases 1 and 2 represent the results from the velocity data at $Re_\theta$ = 1155.1 predicted using the transformer model trained for the flow at $Re_\theta$ = 905.7 and 1362.0, respectively.

results are consistent with the results obtained by Guastoni et al. (2021); Yousif et al. (2022a, 2021).

The total number of trainable parameters of the DLM is 356.5 million (305.5 million for the transformer and 51 million for the MS-ESRGAN). The training of the transformer model for all the three Reynolds numbers used in this study using a single NVIDIA TITAN RTX GPU with the aid of TL requires approximately 23 hours. Meanwhile, the training of the MS-ESRGAN requires approximately 32 hours. Thus, the total training time of the DLM model is 55 hours, indicating that the computational cost of the model is relatively lower than the cost of the DNS that is required to generate the velocity fields. Furthermore, this computational cost is required only once, i.e. for the training of the model. Since the prediction process is computationally inexpensive and does not need any data for the prediction (except the initial instantaneous fields), the DLM can also be considered efficient in terms of storing the inflow data.

#### 4.4. Simulation of spatially developing TBL using the turbulent inflow data

In order to examine the feasibility of applying the DLM-based turbulent inflow conditions, the generated data are utilised to perform an inflow–outflow large eddy simulation (LES) of flat plate TBL spanning $Re_\theta$ = 1362-1820. The open-source computational fluid dynamics (CFD) finite-volume code OpenFOAM-5.0x is used to perform the simulation. The dimensions of the computational domain are 20δ0, 1.8δ0, and 4δ$^{0}$ in the streamwise, wall-normal and spanwise directions, respectively, where δ$^{0}$ represents the boundary layer thickness at the inlet section of the domain. The corresponding grid size = 320×90×150. The grid points have a uniform distribution in the streamwise and spanwise directions while local grid refinement is applied near the wall using the stretching grid technique in the wall-normal direction. The spatial spacing at the midpoint of the domain is ∆x$^{+}$ ≈ 15.4, $\Delta y^+$ wall ≈ $^{0}$.2 and ∆z$^{+}$ ≈ $^{6}$.5, where $^{y}$ + wall represents the spatial spacing in the wall-normal direction near the wall. A no-slip boundary condition is applied to the wall, while periodic boundary conditions are applied to the spanwise direction. A slip boundary condition is assigned to the top of the domain, whereas an advection boundary condition is applied to the outlet of the domain. The pressure implicit split operator (PISO) algorithm is employed to solve the coupled pressure momentum system. The dynamic Smagorinsky model (Germano et al. 1991) is applied for the subgridscale modelling. All the discretisation schemes used in the simulation have second-order accuracy. The generated inflow data are linearly interpolated in time to have a simulation time step ∆t = 0.0017δ0/U$^{∞}$ yielding a maximum Courant number of 0.8. The statistics from the simulation are accumulated over a period of 620 δ0/U$^{∞}$ after an initial run with a period of 60 δ0/U$^{∞}$ or 3 flow through.

The formation of the instantaneous vortical structures of the flow is visualised by utilising the Q − criterion vortex identification method (Hunt et al. 1988) in figure 21. Smooth development of the coherent structures represented by the hairpin-vortex-like structures (Adrian 2007) can be observed from the figure with no noticeable formation of artificial turbulence at the inlet section of the domain. This indicates that the inflow data obtained from the DLM could represent most of the flow physics at the inlet section, resulting in a negligible developing distance upstream of the domain.

A comparison of the mean streamwise velocity and Reynolds shear stress profiles at $Re_\theta$ = 1400 with the DNS results are provided in figure 22. The mean streamwise velocity profile is in excellent agreement with the DNS results. Furthermore, the Reynolds shear stress profile is consistent with the DNS results in most of the boundary layer regions.

To further evaluate the accuracy of the inflow conditions, statistics obtained from the simulation are compared with the inflow–outflow LES results of Lund et al. (1998) and DNS results of Spalart (1988). Figure 23 shows the profiles of the mean streamwise velocity and Reynolds shear stress profiles at $Re_\theta$ = 1530. An agreement can be observed with Lund et al. (1998) results of the modified Spalart (recycling-rescaling) method and the results of Spalart (1988) ($Re_\theta$ = 1410 ) in the inner region of the boundary layer, however, a deviation can be observed in the outer region. This might be attributed to the fact that the original DNS data that are used to train the DLM contain free-stream turbulence (Lee & Zaki 2018).

The evolution of the shape factor H is shown in figure 24(a). Here the result from the simulation is generally consistent with the DNS and Spalart (1988) results, and within 5% of the modified Spalart method from Lund et al. (1998). The result of the skin-friction coefficient in figure 24(b) shows an agreement with the results from Lund et al. (1998) and Spalart (1988) with an over-prediction of approximately 8% compared with the DNS results. The change in the shape factor slope and the over-prediction of the skin-friction coefficient compared with the DNS result can be attributed to the numerical setup of the inflow-outflow simulation. Note that in the work of Lund et al. (1998), the inflow data were generated from precursor simulations that have the same y − z plane size as the inlet section of the inflow-outflow simulations, and no spatial or time interpolation was applied to the inflow data.

The above results suggest that the turbulent inflow data that are generated by the proposed DLM can be practically used as inflow conditions for simulations that do not necessarily have the same spatial and time resolutions as the generated data, which is the case in the simulation described in this section.

# 5. Conclusions

This study proposed a deep-learning-based method to generate turbulent inflow conditions for spatially-developing TBL simulations. A combination of a transformer and MS-ESRGAN was used to build the inflow generator. The transformer was trained to model the temporal evolution of the velocity fields represented by various (y−z) planes of spatially limited data. Meanwhile, MS-ESRGAN was trained to perform super-resolution reconstruction of the predicted velocity fields.

![](_page_20_Figure_9.jpeg)

FIGURE 21. Iso-surfaces of instantaneous vortical structures ( $Q - \text{criterion} = 0.54U_\infty^2/\delta_0^2$ ) from the inflow–outflow simulation coloured by the streamwise velocity.

![](_page_20_Figure_11.jpeg)

FIGURE 22. Turbulence statistics from the inflow–outflow simulation at  $Re_\theta = 1400$  compared with the DNS results. (a) Mean streamwise velocity profile. (b) Reynolds shear stress profile.

![](_page_20_Figure_13.jpeg)

FIGURE 23. Turbulence statistics from the inflow–outflow simulation at  $Re_\theta = 1530$  compared with the results of [Lund et al. (1998)](#) and [Spalart (1988)](#). (a) Mean streamwise velocity profile. (b) Reynolds shear stress profile.

The generated instantaneous velocity fields showed an excellent agreement with the DNS results for the velocity fields at Reynolds numbers that the DLM was trained for. The model also successfully reproduced the turbulence statistics with commendable accuracy. Furthermore, the model reproduced the spectra of the velocity components with accurate precision, indicating accurate spatial and temporal correlations of the generated

![](_page_21_Figure_1.jpeg)

Figure 24. Evolution of the shape factor and skin-friction coefficient in the inflow–outflow simulation compared with the results of the DNS, Lund et al. (1998) and Spalart (1988). (a) Shape factor. (b) Skin-friction coefficient.

velocity components, which further supports the ability of the model to maintain the realistic behaviour of the velocity fields.

The performance of the proposed model was further examined using velocity fields at Reynolds numbers that were not used in the training process. The instantaneous and statistical results showed a reasonable accuracy for the interpolated and extrapolated velocity fields. The spectra of the velocity components revealed a relatively good agreement with the results from the actual velocity data, with a deviation that can be observed at high wavenumbers. These results suggest that the model can generate the turbulent inflow conditions for the flow at Reynolds numbers that are not necessarily used in the training of the model.

The results obtained from the error analysis showed that the increase in the Reynolds number has no significant effect on the error values of the predicted velocity fields, indicating that the model is robust to the increase of the Reynolds number. The use of TL in the training of the transformer revealed a noticeable reduction in the computational cost of the DLM without affecting the precision of the prediction.

The inflow-outflow simulation results showed the feasibility of applying the generated turbulent inflow conditions to turbulent flow simulations as a negligible developing distance upstream of the domain is required for the TBL to reach the target statistics.

This study showed for the first time that a transformer-based model could be effectively used for modelling the dynamics of turbulent flows with the ability to perform parallel computing during the training process, which is not possible in LSTM-based models. It also paved the way for utilising synthetic-inflow generators for large-scale turbulence simulations using deep learning, with significant promise in terms of computational savings.

# Acknowledgements

This work was supported by 'Human Resources Program in Energy Technology' of the Korea Institute of Energy Technology Evaluation and Planning (KETEP), granted financial resource from the Ministry of Trade, Industry & Energy, Republic of Korea (no. 20214000000140). In addition, this work was supported by the National Research Foundation of Korea (NRF) grant funded by the Korea government (MSIP) (no. 2019R1I1A3A01058576). This work was also supported by the National Supercomputing Center with supercomputing resources including technical support (KSC-2021-CRE- 0244). R.V. acknowledges the financial support from the ERC Grant No. "2021-CoG-101043998, DEEPCONTROL".

# Declaration of interests

The authors report no conflict of interest.

#### REFERENCES

Abadi, M., Agarwal, A., Barham, P., Brevdo, E., Chen, Z., Citro, C., Corrado, G. S., Davis, A., Dean, J., Devin, M., Ghemawat, S., Goodfellow, I., Harp, A., Irving, G., Isard, M., Jia, Y., Jozefowicz, R., Kaiser, L., Kudlur, M., Levenberg, J., Mane, D., Monga, R., Moore, S., Murray, D., Olah, C., Schuster, M., Shlens, J., Steiner, B., Sutskever, I., Talwar, K., Tucker, P., Vanhoucke, V., Vasudevan, V., Viegas, F., Vinyals, O., Warden, P., Wattenberg, M., Wicke, M., Yu, Y. & Zheng, X. 2016 Tensorflow: Large-scale machine learning on heterogeneous distributed systems. ArXiv:1603.04467. . Adrian, Ronald J. 2007 Hairpin vortex organization in wall turbulence. Physics of Fluids 19, 041301. Ba, J. L., Kiros, J. R. & Hinton, G. E. 2016 Layer normalization. ArXiv:1607.06450. . Brunton, S. L., Noack, B. R. & Koumoutsakos, P. 2020 Machine learning for fluid mechanics. Annual Review of Fluid Mechanics. 52(1), 477–508. Deng, Z., He, C., Liu, Y. & Kim, K. C. 2019 Super-resolution reconstruction of turbulent velocity fields using a generative adversarial network-based artificial intelligence framework. Physics of Fluids 31(12), 125111. Druault, P., Lardeau, S., Bonnet, J. P., Coiffet, F., Delville, J., Lamballais, E., Largeau, J. F. & Perret, L. 2004 Generation of three-dimensional turbulent inlet conditions for large-eddy simulation. AIAA Journal 42(3), 447–456. Duraisamy, K., Iaccarino, G. & Xiao, H. 2019 Turbulence modeling in the age of data. Annual Review of Fluid Mechanics 51(1), 357–377. Eivazi, H., Clainche, S. L., Hoyas, S. & Vinuesa, R. 2022 Towards extraction of orthogonal and parsimonious non-linear modes from turbulent flows. Expert Systems with Applications 202, 117038. Eivazi, H., Guastoni, L., Schlatter, P., Azizpour, H. & Vinuesa, R. 2021 Recurrent neural networks and koopman-based frameworks for temporal predictions in a low-order model of turbulence. International Journal of Heat and Fluid Flow 90, 108816. Fan, D., Yang, L., Wang, Z., Triantafyllou, M. S. & Karniadakis, G. E. 2020 Reinforcement learning for bluff body active flow control in experiments and simulations. Proceedings of the National Academy of Sciences 117(42), 26091–26098. Fukami, K., Fukagata, K. & Taira, K. 2019a Super-resolution reconstruction of turbulent flows with machine learning. Journal of Fluid Mechanics 870, 106–120. Fukami, K., Fukagata, K. & Taira, K. 2021 Machine-learning-based spatio-temporal super resolution reconstruction of turbulent flows. Journal of Fluid Mechanics 909. Fukami, K., Nabae, Y., Kawai, K. & Fukagata, K. 2019b Synthetic turbulent inflow generator using machine learning. Physical Review Fluids 4(6). Germano, M., Piomelli, U., p. Moin & Cabot, W. H. 1991 A dynamic subgrid-scale eddy viscosity model. Physics of Fluids A: Fluid Dynamics 3, 1760–1765. Goodfellow, I., Pouget-Abadie, J., Mirza, M., Xu, B., Warde-Farley, D., Ozair, S., Courville, A. & Bengio, Y. 2014 Generative adversarial nets. Advances in Neural Information Processing Systems 27. Graves, A. 2012 Long short-term memory. MIT Press pp. 37–45. Guastoni, L., Guemes, A., Ianiro, A., Discetti, S., Schlatter, P., Azizpour, H. & Vinuesa, R. 2021 Convolutional-network models to predict wall-bounded turbulence from wall quantities. Journal of Fluid Mechanics 928. Guemes, A., Discetti, S., Ianiro, A., Sirmacek, B., Azizpour, H. & Vinuesa, R. ¨ 2021

- From coarse wall measurements to turbulent velocity fields through deep learning. Physics of Fluids 33(7), 075121. He, K., Zhang, X., Ren, S. & Sun, J. 2016 Deep residual learning for image recognition. IEEE Conference on Computer Vision and Pattern Recognition (CVPR) pp. 770–778. Hochreiter, S. & Schmidhuber, J. 1997 Long short-term memory. Neural Computation 9(8), 1735–1780. Hunt, Julian Charles Roland, Wray, Alan A. & Moin, Parviz 1988 Eddies, streams, and convergence zones in turbulent flows. in Proceedings of the Summer Program (Center for Turbulence Research pp. 193–208. Jarrin, N., Benhamadouche, S., Laurence, D. & Prosser, R. 2006 A synthetic-eddymethod for generating inflow conditions for large-eddy simulations. International Journal of Heat and Fluid Flow 27(4), 585–593. Jimenez, J., Hoyas, S., Simens, M. P. & Mizuno, Y. ´ 2010 Turbulent boundary layers and channels at moderate reynolds numbers. Journal of Fluid Mechanics 657, 335–360. Johansson, P. S. & Andersson, H. I. 2004 Generation of inflow data for inhomogeneous turbulence. Theoretical and Computational Fluid Dynamics 18(5), 371–389. Jolicoeur-Martineau, A. 2018 The relativistic discriminator: A key element missing from standard gan. ArXiv:1807.00734 . Kim, H., Kim, J., Won, S. & Lee, C. 2021 Unsupervised deep learning for super-resolution reconstruction of turbulence. Journal of Fluid Mechanics 910. Kim, J. & Lee, C. 2020 Deep unsupervised learning of turbulence for inflow generation at various reynolds numbers. Journal of Computational Physics 406, 109216. Kingma, D. P. & Ba, J. 2017 Adam: A method for stochastic optimization. ArXiv:1412.6980 . Klein, M., Sadiki, A. & Janicka, J. 2003 A digital filter based generation of inflow data for spatially developing direct numerical or large eddy simulations. Journal of Computational Physics 186(2), 652–665. Kutz, J. N. 2017 Deep learning in fluid dynamics. Journal of Fluid Mechanics 814, 1–4. Le, H., Moin, P. & Kim, J. 1997 Direct numerical simulation of turbulent flow over a backwardfacing step. Journal of Fluid Mechanics 330, 349–374. LeCun, Y., Bengio, Y. & Hinton, G. 2015 Deep learning. Nature 521(7553), 436–444. Ledig, C., Theis, L., Huszar, F., Caballero, J., Cunningham, A., Acosta, A., Aitken, A., Tejani, A., Totz, J. & andW. Shi, Z. Wang 2017 Photo-realistic single image super-resolution using a generative adversarial network. ArXiv:1609.04802 . Lee, J. & Zaki, T. A. 2018 Detection algorithm for turbulent interfaces and large-scale structures in intermittent flows. Computers & Fluids 175, 142–158. Lee, S. & You, D. 2019 Data-driven prediction of unsteady flow over a circular cylinder using deep learning. Journal of Fluid Mechanics 879, 217–254. Lund, T., Wu, X. & K.Squires 1998 Generation of turbulent inflow data for spatiallydeveloping boundary layer simulations. Journal of Computational Physics 140(2), 233–
- 258. Lund, T. S. 1993 Large eddy simulation of a boundary layer with concave streamwise curvature. Center for Turbulence Research pp. 91–99. Mathey, F., Cokljat, D., Bertoglio, J. P. & Sergent, E. 2006 Assessment of the vortex method for large eddy simulation inlet conditions. Progress in Computational Fluid Dynamics, an International Journal 6(1–3), 58–67. Mirza, M. & Osindero, S. 2014 Conditional generative adversarial nets. arXiv:1411.1784v1 . Nakamura, T., Fukami, K., Hasegawa, K., Nabae, Y. & Fukagata, K. 2021 Convolutional neural network and long short-term memory based reduced order surrogate for minimal turbulent channel flow. Physics of Fluids 33(2), 025116. Park, J. & Choi, H. 2020 Machine-learning-based feedback control for drag reduction in a turbulent channel flow. Journal of Fluid Mechanics 904. Perret, L., Delville, J., Manceau, R. & Bonnet, J. P. 2008 Turbulent inflow conditions for large-eddy simulation based on low-order empirical model. Physics of Fluids 20(7), 075–107. Rabault, J., Kuchta, M., Jensen, A., Reglade, U. & Cerardi, N. 2019 Artificial neural

- networks trained through deep reinforcement learning discover control strategies for active flow control. Journal of Fluid Mechanics 865, 281–302. Rumelhart, D. E., Hinton, G. E. & Williams, R. J. 1986 Learning representations by back-propagating errors. Nature 323(6088), 533–536. Sanmiguel Vila, C., Vinuesa, R., Discetti, S., Ianiro, A., Schlatter, P. & Orlu, R. 2017 On the identification of well-behaved turbulent boundary layers. Journal of Fluid Mechanics 822, 109–138. Schlatter, P. & Orl ¨ u, R. ¨ 2012 Turbulent boundary layers at moderate reynolds numbers: Inflow length and tripping effects. Journal of Fluid Mechanics 710, 5–34. Sergent, E. 2020 Vers une m´ethodologie de couplage entre la simulation des grandes ´echelles et les mod`eles statistiques. Ecully, Ecole centrale de Lyon . Simonyan, K. & Zisserman, A. 2015 Very deep convolutional networks for large-scale image recognition. ArXiv:1409.1556 . Spalart, P. R. 1988 Direct simulation of a turbulent boundary layer up to re$^{\theta}$ = 1410. Journal of Fluid Mechanics 187, 61–98. Spille-Kohoff, A. & Kaltenbach, H. J. 2001 Generation of turbulent inflow data with a prescribed shear-stress profile. Technische univ Berlin (German) Hermann-Fottinger inst fur stromunsmechanik . Srinivasan, P. A., Guastoni, L., Azizpour, H., Schlatter, P. & Vinuesa, R. 2019 Predictions of turbulent shear flows using deep neural networks. Physical Review Fluids 4(5), 054603. Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser,
- L. & Polosukhin, I. 2017 Attention is all you need. Advances in Neural Information Processing Systems 30. Vinuesa, R. & Brunton, S. L. 2021 The potential of machine learning to enhance computational fluid dynamics. ArXiv:2110.02085 . Vinuesa, R., Lehmkuhl, O., Lozano-Duran, A. & Rabault, J. 2022 Flow control in wings and discovery of novel approaches via deep reinforcement learning. Fluids 7(2), 62. Wang, J.-X., Wu, J.-L. & Xiao, H. 2017 A physics informed machine learning approach for reconstructing reynolds stress modeling discrepancies based on dns data. Physical Review Fluids 2(3), 034603. Wang, X., Yu, K., Wu, S., Gu, J., Liu, Y., Dong, C., Loy, C. C., Qiao, Y. & Tang, X. 2018 Esrgan: Enhanced super-resolution generative adversarial networks. ArXiv:1809.00219 . Wu, X. 2017 Inflow turbulence generation methods. Annual Review of Fluid Mechanics 49(1), 23–49. Yousif, M. Z. & Lim, H. 2021 Improved delayed detached-eddy simulation and proper orthogonal decomposition analysis of turbulent wake behind a wall-mounted square cylinder. AIP Advances 11(045011). Yousif, M. Z. & Lim, H. 2022 Reduced-order modeling for turbulent wake of a finite wallmounted square cylinder based on artificial neural network. Physics of Fluids 34(1), 015116. Yousif, M. Z., Yu, L. & Lim, H. 2021 High-fidelity reconstruction of turbulent flow from spatially limited data using enhanced super-resolution generative adversarial network. Physics of Fluids 33(12), 125119. Yousif, M. Z., Yu, L. & Lim, H. 2022a Physics-guided deep learning for generating turbulent inflow conditions. Journal of Fluid Mechanics 936. Yousif, M. Z., Yu, L. & Lim, H. 2022b Super-resolution reconstruction of turbulent flow fields at various reynolds numbers based on generative adversarial networks. Physics of Fluids 34(1), 015130. Zhu, J.-Y., Park, T., Isola, P. & Efros, A. A. 2017 Unpaired image-to-image translation using cycle-consistent adversarial networks. 2017 IEEE International Conference on Computer Vision (ICCV) pp. 2242–2251.