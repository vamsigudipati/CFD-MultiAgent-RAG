# Discovering Symbolic Models from Deep Learning with Inductive Biases

Miles Cranmer$^{1}$ Alvaro Sanchez-Gonzalez$^{2}$ Peter Battaglia$^{2}$ Rui Xu$^{1}$

Kyle Cranmer$^{3}$ David Spergel$^{4}$,$^{1}$ Shirley Ho$^{4}$,3,1,$^{5}$

Princeton University, Princeton, USA $^{2}$ DeepMind, London, UK

$^{3}$ New York University, New York City, USA $^{4}$ Flatiron Institute, New York City, USA $^{5}$ Carnegie Mellon University, Pittsburgh, USA

### Abstract

We develop a general approach to distill symbolic representations of a learned deep model by introducing strong inductive biases. We focus on Graph Neural Networks (GNNs). The technique works as follows: we first encourage sparse latent representations when we train a GNN in a supervised setting, then we apply symbolic regression to components of the learned model to extract explicit physical relations. We find the correct known equations, including force laws and Hamiltonians, can be extracted from the neural network. We then apply our method to a non-trivial cosmology example—a detailed dark matter simulation—and discover a new analytic formula which can predict the concentration of dark matter from the mass distribution of nearby cosmic structures. The symbolic expressions extracted from the GNN using our technique also generalized to out-of-distributiondata better than the GNN itself. Our approach offers alternative directions for interpreting neural networks and discovering novel physical principles from the representations they learn.

## 1 Introduction

*The miracle of the appropriateness of the language of mathematics for the formulation of the laws of physics is a wonderful gift which we neither understand nor deserve. We should be grateful for it and hope that it will remain valid in future research and that it will extend, for better or for worse, to our pleasure, even though perhaps also to our bafflement, to wide branches of learning.*—Eugene Wigner "The Unreasonable Effectiveness of Mathematics in the Natural Sciences" \[1\].

For thousands of years, science has leveraged models made out of closed-form symbolic expressions, thanks to their many advantages: algebraic expressions are usually compact, present explicit interpretations, and generalize well. However, finding these algebraic expressions is difficult. Symbolic regression is one option: a supervised machine learning technique that assembles analytic functions to model a given dataset. However, typically one uses genetic algorithms—essentially a brute force procedure as in \[2\]—which scale exponentially with the number of input variables and operators. Many machine learning problems are thus intractable for traditional symbolic regression.

On the other hand, deep learning methods allow efficient training of complex models on highdimensional datasets. However, these learned models are black boxes, and difficult to interpret.

Code for our models and experiments can be found at [https://github.com/MilesCranmer/symbolic\\_](https://github.com/MilesCranmer/symbolic_deep_learning) [deep\\_learning](https://github.com/MilesCranmer/symbolic_deep_learning).

![](_page_1_Diagram_0.jpeg)

![Diagram illustrating the process of data simulation for a simple particle network. It shows a Dataset of simple particles, a Model with Graph Neural Network, and an Extract to Symbolic Equation. The process is divided into two parallel paths: 'Predict Dynamics' and 'Predict Properties'. The 'Predict Dynamics' path involves a simple particle network and an Encourage Low-Dimensionality Representation. The 'Predict Properties' path involves a Dark Matter Simulation network and an Unknown Dark Matter overdensity equation.]()Diagram illustrating the process of data simulation for a simple particle network. It shows a Dataset of simple particles, a Model with Graph Neural Network, and an Extract to Symbolic Equation. The process is divided into two parallel paths: 'Predict Dynamics' and 'Predict Properties'. The 'Predict Dynamics' path involves a simple particle network and an Encourage Low-Dimensionality Representation. The 'Predict Properties' path involves a Dark Matter Simulation network and an Unknown Dark Matter overdensity equation.

Dataset

Simple Particles

Predict Dynamics

Encourage Low-Dimensionality Representation

Extract to Symbolic Equation

 $\vec{a}_i = \frac{C}{M_i} \sum_{j \neq i} (1 - r_{ij}) \hat{r}_{ij}$ 

Known spring law

Dataset

Simple Particles

Predict Properties

Encourage Low-Dimensionality Representation

Extract to Symbolic Equation

 $\hat{a}_i = C_1 + \frac{1}{C_2 + C_3 M_i} \sum_{j \neq i} \frac{C_4 + M_j}{C_5 + C_6(r_{ij})^{C_7}}$ 

Unknown Dark Matter overdensity equation

Dark Matter Simulation

Predict Dynamics

Encourage Low-Dimensionality Representation

Extract to Symbolic Equation

 $\hat{a}_i = C_1 + \frac{1}{C_2 + C_3 M_i} \sum_{j \neq i} \frac{C_4 + M_j}{C_5 + C_6(r_{ij})^{C_7}}$ 

Known spring law

Unknown Dark Matter overdensity equation

Dark Matter Simulation

Predict Dynamics

Encourage Low-Dimensionality Representation

Extract to Symbolic Equation

 $\hat{a}_i = C_1 + \frac{1}{C_2 + C_3 M_i} \sum_{j \neq i} \frac{C_4 + M_j}{C_5 + C_6(r_{ij})^{C_7}}$ 

Known spring law

Unknown Dark Matter overdensity equation

Dark Matter Simulation

Predict Dynamics

Encourage Low-Dimensionali

Figure 1: A cartoon depicting how we extract physical equations from a dataset.

Furthermore, generalization is difficult without prior knowledge about the data imposed directly on the model. Even if we impose strong inductive biases on the models to improve generalization, the learned parts of networks typically are linear piece-wise approximations which extrapolate linearly (if using ReLU as activation \[3\]).

Here, we propose a general framework to leverage the advantages of both deep learning and symbolic regression. As an example, we study Graph Networks (GNs or GNNs) \[4\] as they have strong and well-motivated inductive biases that are very well suited to problems we are interested in. Then we apply symbolic regression to fit different internal parts of the learned model that operate on reduced size representations. The symbolic expressions can then be joined together, giving rise to an overall algebraic equation equivalent to the trained GN. Our work is a generalized and extended version of that in \[5\].

We apply our framework to three problems—rediscovering force laws, rediscovering Hamiltonians, and a real world astrophysical challenge—and demonstrate that we can drastically improve generalization, and distill plausible analytical expressions. We not only recover the injected closedform physical laws for Newtonian and Hamiltonian examples, we also derive a new interpretable closed-form analytical expression that can be useful in astrophysics.

## 2 Framework

Our framework can be summarized as follows. (1) Engineer a deep learning model with a separable internal structure that provides an inductive bias well matched to the nature of the data. Specifically, in the case of interacting particles, we use Graph Networks as the core inductive bias in our models. (2) Train the model end-to-end using available data. (3) Fit symbolic expressions to the distinct functions learned by the model internally. (4) Replace these functions in the deep model by the symbolic expressions. This procedure with the potential to discover new symbolic expressions for non-trivial datasets is illustrated in fig. 1.

Particle systems and Graph Networks. In this paper we focus on problems that can be well described as interacting particle systems. Nearly all of the physics we experience in our day-to-day life can be described in terms of interactions rules between particles or entities, so this is broadly relevant. Recent work has leveraged the inductive biases of Interaction Networks (INs) \[6\] in their generalized form, the *Graph Network*, a type of Graph Neural Network \[7,] [8,] [9\], to learn models of particle systems in many physical domains \[6,] [10,] [11,] [12,] [13,] [14,] [15,] [16\].

Therefore we use Graph Networks (GNs) at the core of our models, and incorporate into them physically motivated inductive biases appropriate for each of our case studies. Some other interesting approaches for learning low-dimensional general dynamical models include \[17,] [18,] [19\]. Other related work which studies the physical reasoning abilities of deep models include \[20,] [21,] [22,] [23\].

Internally, GNs are structured into three distinct components: an edge model, a node model, and a global model, which take on different but explicit roles in a regression problem. The edge model, or "message function," which we denote by φ e , maps from a pair of nodes (v$^{i}$ , $^{v}$$^{j}$ ∈ $^{R}$ $^{L}$$^{v}$ ) connected by an edge in a graph together with some vector information for the edge, to a message vector. These message vectors are summed element-wise for each receiving node over all of their sending nodes, and the summed vector is passed to the node model. The node model, φ v , takes the receiving node and the summed message vector, and computes an updated node: a vector representing some property or dynamical update. Finally, a global model φ u aggregates all messages and all updated nodes and computes a global property. φ e , φ v , φ u are usually approximated using multilayer-perceptrons, making them differentiable end-to-end. More details on GNs are given in the appendix. We illustrate the internal structure of a GN in fig. 2.

![](_page_2_Diagram_2.jpeg)

Figure 2: An illustration of the internal structure of the graph neural network we use in some of our experiments. Note that the comparison to Newtonian mechanics is purely for explanatory purposes, but is not explicit. Differences include: the "forces" (messages) are often high dimensional, the nodes need not be physical particles, φ e and φ v are arbitrary learned functions, and the output need not be an updated state. However, the rough equivalency between this architecture and physical frameworks allows us to interpret learned formulas in terms of existing physics.

GNs are the ideal candidate for our approach due to their inductive biases shared by many physics problems. (a) They are equivariant under particle permutations. (b) They are differentiable end-to-end and can be trained efficiently using gradient descent. (c) They make use of three separate and interpretable internal functions φ e , φ v , φ u , which are our targets for the symbolic regression. GNs can also be embedded with additional symmetries as in \[24,] [25\], but we do not implement these.

Symbolic regression. After training the Graph Networks, we use the symbolic regression package *eureqa* \[2\] to perform symbolic regression and fit compact closed-form analytical expressions to φ e , φ v , and φ u independently. *eureqa* works by using a genetic algorithm to combine algebraic expressions stochastically. The technique is similar to natural selection, where the "fitness" of each expression is defined in terms of simplicity and accuracy. The operators considered in the fitting process are $^{+}$, −, ×, /, >, <, ^, exp, log, IF(·, ·, ·) as well as real constants. After fitting expressions to each part of the graph network, we substitute the expressions into the model to create an alternative analytic model. We then refit any parameters in the symbolic model to the data a second time, to avoid the accumulated approximation error. Further details are given in the appendix.

This approach gives us an explicit way of interpreting the trained weights of a structured neural network. An alternative way of interpreting GNNs is given in \[26\]. This new technique also allows

us to extend symbolic regression to high-dimensional datasets, where it is otherwise intractable. As an example, consider attempting to discover the relationship between a scalar and a time series, given data {(z$^{i}$ , {$^{x}$i,1, $^{x}$i,2, . . . $^{x}$i,100}}, where $^{z}$$^{i}$ ∈ $^{R}$ and $^{x}$i,j ∈ $^{R}$ . Assume the true relationship as z$^{i}$ = y 2 i , for y$^{i}$ = P$^{100}$ $^{j}$=1 yi,j , yi,j = exp xi,j,$^{3}$ + cos 2xi,j,$^{1}$ . Now, in a learnable model, assume an inductive bias z$^{i}$ = f( P$^{100}$ $^{j}$=1 g(xi,j )) for scalar functions f and g. If we need to consider 10$^{9}$ equations for both f and g, then a standard symbolic regression search would need to consider their combination, leading to (10$^{9}$ ) $^{2}$ = 10$^{18}$ equations in total. But if we first fit a neural network for f and $^{g}$, and after training, fit an equation to $^{f}$ and $^{g}$ *separately*, we only need to consider $^{2}$×10$^{9}$ equations. In effect, we factorize high-dimensional datasets into smaller sub-problems that are tractable for symbolic regression.

We emphasize that this method is not a new symbolic regression technique by itself; rather, it is a way of extending any existing symbolic regression method to high-dimensional datasets by the use of a neural network with a well-motivated inductive bias. While we chose *eureqa* for our experiments based on its efficiency and ease-of-use, we could have chosen another low-dimensional symbolic regression package, such as our new high-performance package *PySR*$^{1}$ \[27\]. Other community packages such as \[28,] [29,] [30,] [31,] [32,] [33,] [34,] [35,] [36\], could likely also be used and achieve similar results (although \[32\] is unable to fit the constants required for the tasks here). Ref. \[29\] is an interesting approach that uses gradient descent on a pre-defined equation up to some depth, parametrized with a neural network, instead of genetic algorithms; \[35\] uses gradient descent on a latent embedding of an equation; and \[36\] demonstrates Monte Carlo Tree Search as a symbolic regression technique, using an asymptotic constraint as input to a neural network which guides the search. These could all be used as drop-in replacements for *eureqa* here to extend their algorithms to high-dimensional datasets.

We also note several exciting packages for symbolic regression of partial differential equations on gridded data: \[37,] [38,] [39,] [40,] [41,] [42\]. These either use sparse regression of coefficients over a library of PDE terms, or a genetic algorithm. While not applicable to our use-cases, these would be interesting to consider for future extensions to gridded PDE data.

Compact internal representations. While training, we encourage the model to use compact internal representations for latent hidden features (e.g., messages) by adding regularization terms to the loss (we investigate using L$^{1}$ and KL penalty terms with a fixed prior, see more details in the Appendix). One motivation for doing this is based on *Occam's Razor*: science always prefers the simpler model or representation of two which give similar accuracy. Another stronger motivation is that if there is a law that perfectly describes a system in terms of summed message vectors in a compact space (what we call a linear latent space), then we expect that a trained GN, with message vectors of the same dimension as that latent space, will be mathematical rotations of the true vectors. We give a mathematical explanation of this reasoning in the appendix, and emphasize that while it may seem obvious now, our work is the first to demonstrate it. More practically, by reducing the size of the latent representations, we can filter out all low-variance latent features without compromising the accuracy of the model, and vastly reducing the dimensionality of the hidden vectors. This makes the symbolic regression of the internal models more tractable.

Implementation details. We write our models with PyTorch \[43\] and PyTorch Geometric\[44\]. We train them with a decaying learning schedule using Adam \[45\]. The symbolic regression technique is described in section 4.1. More details are provided in the Appendix.

## 3 Case studies

In this section we present three specific case studies where we apply our proposed framework using additional inductive biases.

Newtonian dynamics. Newtonian dynamics describes the dynamics of particles according to Newton's law of motion: the motion of each particle is modeled using incident forces from nearby particles, which change its position, velocity and acceleration. Many important forces in physics (e.g., gravitational force − Gm1m$^{2}$ r $^{2}$ rˆ) are defined on pairs of particles, analogous to the message function φ $^{e}$ of our Graph Networks. The summation that aggregates messages is analogous to the

$^{1}$ <https://github.com/MilesCranmer/PySR>

calculation of the net force on a receiving particle. Finally, the node function, φ v , acts like Newton's law: acceleration equals the net force (the summed message) divided by the mass of the receiving particle.

To train a model on Newtonian dynamics data, we train the GN to predict the instantaneous acceleration of the particle against that calculated in the simulation. While Newtonian mechanics inspired the original development of INs, never before has an attempt to distill the relationship between the forces and the learned messages been successful. When applying the framework to this Newtonian dynamics problem (as illustrated in fig. 1), we expect the model trained with our framework to discover that the optimal dimensionality of messages should match the number of spatial dimensions. We also expect to recover algebraic formulas for pairwise interactions, and generalize better than purely learned models. We refer our readers to section 4.1 and the Appendix for more details.

Hamiltonian dynamics. Hamiltonian dynamics describes a system's total energy H(q, $^{p}$) as a function of its canonical coordinates q and momenta p—e.g., each particle's position and momentum. The dynamics of the system change perpendicularly to the gradient of H: dq $^{d}$$^{t}$ = ∂H ∂p , dp $^{d}$$^{t}$ $^{=}$ − dH dq .

Here, we will use a variant of a Hamiltonian Graph Network (HGN) \[46\] to learn H for the Newtonian dynamics data. This model is a combination of a Hamiltonian Neural Network \[47,] [48\] and GN. In this case, the global model φ $^{u}$ of the GN will output a single scalar value for the entire system representing the energy, and hence the GN will have the same functional form as a Hamiltonian. By then taking the partial derivatives of the GN-predicted H with respect to the position and momentum, q and p, respectively, of the input nodes, we will be able to calculate the updates to the momentum and position. We impose a modification to the HGN to facilitate its interpretability, and name this the "Flattened HGN" or FlatHGN: instead of summing high-dimensional encodings of nodes to calculate φ u , we instead set it to be a sum of scalar pairwise interaction terms, Hpair and a per-particle term, Hself. This is because many physical systems can be exactly described this way. This is a Hamiltonian version of the Lagrangian Graph Network in \[49\], and is similar to \[50\]. This is still general enough to express many physical systems, as nearly all of physics can be written as summed interaction energies, but could also be relaxed in the context of the framework.

Even though the model is trained end-to-end, we expect our framework to allow us to extract analytical expressions for both the per-particle kinetic energy, and the scalar pairwise potential energy. We refer our readers to our section 4.2 and the Appendix for more details.

Dark matter halos for cosmology. We also apply our framework to a dataset generated from stateof-the-art dark matter simulations \[51\]. We predict a property ("overdensity") of a dark matter blob (called a "halo") from the properties (positions, velocities, masses) of halos nearby. We would like to extract this relationship as an analytic expression so we may interpret it theoretically. This problem differs from the previous two use cases in many ways, including (1) it is a real-world problem where an exact analytical expression is unknown; (2) the problem does not involve dynamics, rather, it is a regression problem on a static dataset; and (3) the dataset is not made of particles, but rather a grid of density that has been grouped and reduced to handmade features. Similarly, we do not know the dimensionality of interactions, should a linear latent space exist. We rely on our inductive bias to find the optimal dimensional of the problem, and then yield an interpretable model that performs better than existing analytical approximations. We refer our readers to our section 4.3 and the Appendix for further details.

## 4 Experiments & results

### 4.1 Newtonian dynamics

We train our Newtonian dynamics GNs on data for simple N-body systems with known force laws. We then apply our technique to recover the known force laws via the representations learned by the message function φ e .

Data. The dataset consists of N-body particle simulations in two and three dimensions, under different interaction laws. We used the following forces: (a) $^{1}$/r orbital force: −$^{m}$1m2r/r $^{ˆ}$ ; (b) $^{1}$/r$^{2}$ orbital force −$^{m}$1m2r/r $^{ˆ}$ 2 ; (c) charged particles force q1q2r/r ˆ 2 ; (d) damped springs with |$^{r}$ − $^{1}$| 2

![](_page_5_Figure_0.jpeg)

![](_page_5_Diagram_1.jpeg)

Figure 3: A diagram showing how we implement and exploit our inductive bias on GNs. A video of this figure during training can be seen by going to the URL [https://github.com/MilesCranmer/](https://github.com/MilesCranmer/symbolic_deep_learning/blob/master/video_link.txt) [symbolic\\_deep\\_learning/blob/master/video\\_link.txt](https://github.com/MilesCranmer/symbolic_deep_learning/blob/master/video_link.txt).

potential and damping proportional and opposite to speed; (e) discontinuous forces, −{0, r$^{2}$}rˆ, switching to $^{0}$ force for r < $^{2}$; and (f) springs between all particles, a ($^{r}$ − 1)$^{2}$ potential. The simulations themselves contain masses and charges of 4 or 8 particles, with positions, velocities, and accelerations as a function of time. Further details of these systems are given in the appendix, with example trajectories shown in fig. 4.

Model training. The models are trained to predict instantaneous acceleration for every particle given the current state of the system. To investigate the importance of the size of the message representations for interpreting the messages as forces, we train our GN using 4 different strategies: 1. Standard, a GN with 100 message components; 2. Bottleneck, a GN with the number of message components matching the dimensionality of the problem (2 or 3); 3. L1, same as "Standard" but using a L$^{1}$ regularization loss term on the messages with a weight of 10$^{−}$$^{2}$ ; and 4. KL same as "Standard" but regularizing the messages using the Kullback-Leibler (KL) divergence with respect to Gaussian prior. Both the L$^{1}$ and KL strategies encourage the network to find compact representations for the message vectors, using different regularizations. We optimize the mean absolute loss between the predicted acceleration and the true acceleration of each node. Additional training details are given in the appendix and found in the codebase.

Performance comparison. To evaluate the learned models, we generate a new dataset from a different random seed. We find that the model with L$^{1}$ regularization has the greatest prediction performance in most cases (see table 3). It is worth noting that the bottleneck model, even though it has the correct dimensionalty, performs worse than the model using L$^{1}$ regularization under limited training time. We speculate that this may connect to the lottery ticket hypothesis \[52\].

Interpreting the message components. As a first attempt to interpret the information in the message components, we pick the D message features (where D is the dimensionality of the simulation) with the highest variance (or KL divergence), and fit each to a linear combination of the true force components. We find that while the GN trained in the Standard setting does not show strong correlations with force components (also seen in fig. 5), all other models for which the effective message size is constrained explicitly (bottleneck) or implicitly (KL or L1) to be low dimensional yield messages that are highly correlated with the true forces (see table 1 which indicates the fit errors with respect to the true forces), with the model trained with L$^{1}$ regularization showing the highest correlations. An explicit demonstration that the messages in a graph network learn forces has not been observed before our work.

The messages in these models are thus explicitly interpretable as forces. The video at [https://github.com/MilesCranmer/symbolic\\_deep\\_learning/blob/master/video\\_](https://github.com/MilesCranmer/symbolic_deep_learning/blob/master/video_link.txt) [link.txt](https://github.com/MilesCranmer/symbolic_deep_learning/blob/master/video_link.txt) (fig. 3) shows a fit of the message components over time during training, showing how the model discovers a message representation that is highly correlated with a rotation of the true force vector in an unsupervised way.

| Sim.     | Standard | Bottleneck | L 1   | KL    |
|----------|----------|------------|-------|-------|
| Charge-2 | 0.016    | 0.947      | 0.004 | 0.185 |
| Charge-3 | 0.013    | 0.980      | 0.002 | 0.425 |
| − 1 r    |          |            |       |       |
| -2       | 0.000    | 1.000      | 1.000 | 0.796 |
| − 1 r    |          |            |       |       |
| -3       | 0.000    | 1.000      | 1.000 | 0.332 |
| − 2 r    |          |            |       |       |
| -2       | 0.004    | 0.993      | 0.990 | 0.770 |
| − 2 r    |          |            |       |       |
| -3       | 0.002    | 0.994      | 0.977 | 0.214 |
| Spring-2 | 0.032    | 1.000      | 1.000 | 0.883 |
| Spring-3 | 0.036    | 0.995      | 1.000 | 0.214 |

Table 1: The R$^{2}$ value of a fit of a linear combination of true force components to the message components for a given model (see text). Numbers close to 1 indicate the messages and true force are strongly correlated. Successes/failures of force law symbolic regression are tabled in the appendix.

Symbolic regression on the internal functions. We now demonstrate symbolic regression to extract force laws from the messages, without using prior knowledge for each force's form. To do this, we record the most significant message component of φ e , which we refer to as φ e 1 , over random samples of the training dataset. The inputs to the regression are m1, m2, q1, q2, x1, x2, . . . (mass, charge, x-position of receiving and sending node) as well as simplified variables to help the symbolic regression: e.g., ∆x for x displacement, and r for distance.

We then use *eureqa* to fit the φ e to the inputs by minimizing the mean absolute error (MAE) over various analytic functions. Analogous to Occam's razor, we find the "best" algebraic model by asking *eureqa* to provide multiple candidate fits at different complexity levels (where complexity is scored as a function of the number and the type of operators, constants and input variables used), and select the fit that maximizes the fractional drop in mean absolute error (MAE) over the increase in complexity from the next best model: (−∆ log(MAEc)/∆c). From this, we recover many analytical expressions (this is tabled in the appendix) that are equivalent to the simulated force laws (a, b indicate learned constants):

• Spring, 2D, L$^{1}$ (expect φ e $^{1}$ ≈ ($^{a}$ · (∆x, $^{∆}$y))($^{r}$ − 1) + $^{b}$).

$$\phi_1^\varepsilon \approx 1.36\Delta y + 0.60\Delta x - \frac{0.60\Delta x + 1.37\Delta y}{r} - 0.0025$$

- 1/r$^{2}$ , 3D, Bottleneck (expect φ e 1 ≈ a·(∆x,∆y,∆z) r $^{3}$ + b).

$$\phi_1^\epsilon \approx \frac{0.021 \Delta x m_2 - 0.077 \Delta y m_2}{r^3}$$

- Discontinuous, 2D, L$^{1}$ (expect φ e $^{1}$ ≈ IF(r > $^{2}$,($^{a}$ · (∆x, $^{∆}$y, $^{∆}$z))r, 0) + $^{b}$).

$$\phi_1^\epsilon \approx \text{IF}(r > 2, 0.15r\Delta y + 0.19r\Delta x, 0) - 0.038$$

Note that reconstruction does not always succeed, especially for training strategies other than L$^{1}$ or bottleneck models that cannot successfully find compact representations of the right dimensionality (see some examples in Appendix).

### 4.2 Hamiltonian dynamics

Using the same datasets from the Newtonian dynamics case study, we also train our "FlatHGN," with the Hamiltonian inductive bias, and demonstrate that we can extract scalar potential energies, rather than forces, for all of our problems. For example, in the case of charged particles, with expected potential (Hpair ≈ aq1q$^{2}$ r ), symbolic regression applied to the learned message function yields$^{2}$ : Hpair ≈ 0.0019q1q$^{2}$ r .

It is also possible to fit the per-particle term Hself, however, in this case the same kinetic energy expression is recovered for all systems. In terms of performance results, the Hamiltonian models are comparable to that of the L$^{1}$ regularized model across all datasets (See Supplementary results table).

Note that in this case, by design, the "FlatHGN" has a message function with a dimensionality of 1 to match the output of the Hamiltonian function which is a scalar, so no regularization is needed, as the message size is directly constrained to the right dimension.

### 4.3 Dark matter halos for cosmology

Now, one may ask: "will this strategy also work for general regression problems, non-trivial datasets, complex interactions, and unknown laws?" Here we give an example that satisfies all four of these concerns, using data from a gravitational simulation of the Universe.

Cosmology studies the evolution of the Universe from the Big Bang to the complex galaxies and stars we see today \[53\]. The interactions of various types of matter and energy drive this evolution. Dark Matter alone consists of ≈ 85% of the total matter in the Universe \[54,] [55\], and therefore is extremely important for the development of galaxies. Dark matter particles clump together and act as gravitational basins called "halos" which pull regular baryonic matter together to produce stars, and form larger structures such as filaments and galaxies. It is an important question in cosmology to predict properties of dark matter halos based on their "environment," which consist of other nearby dark matter halos. Here we study the following problem: how can we predict the excess amount of matter (in comparison to its surroundings, δ = ρ−hρi hρi ) for a dark matter halo based on its properties and those of its neighboring dark matter halos?

A hand-designed estimator for the functional form of δ$^{i}$ for halo i might correlate δ with the mass of the same halo, M$^{i}$ , as well as the mass within 20 distance units (we decide to use 20 as the smoothing radius): $^{P}$|$^{r}$i−r$^{j}$ |<$^{20}$ $^{j}$6=$^{i}$ M$^{j}$ . The intuition behind this scaling is described in \[56\]. Can we find a better equation that we can fit better to the data, using our methodology?

Data, training and symbolic regression. We study this problem with the open sourced N-body dark matter simulations from \[51\]. We choose the zeroth simulation in this dataset, at the final time step (current day Universe), which contains 215,854 dark matter halos. Each halo has mass M$^{i}$ , position r$^{i}$ , and velocity v$^{i}$ . We also compute the smoothed overdensity δ$^{i}$ at the location of the center of each halo. We convert this set of halos into a graph by connecting halos within fifty distance units (each distance unit is approximately 3 million light years long) of each other. This results in 30,437,218 directional edges between halos, or 71 neighbors per halo on average. We then attempt to predict δ$^{i}$ for each halo with a GN. Training details are the same as for the Newtonian simulations, but we switch to 500 hidden units after hyperparameter tuning based on GN accuracy.

The GN trained with L$^{1}$ appears to have messages containing only 1 informative feature, so we extract message samples for this component of the messages over the training set for random pairs of halos, and node function samples for random receiving halos and their summed messages. The formula extracted by the algorithm is given in table 2 as "Best, with mass". The form of the formula is new and it captures a well-known relationship between halo mass and environment: bias-mass relationship. We refit the parameters in the formula on the original training data to avoid accumulated approximation error from the multiple levels of function fitting. We achieve a loss of 0.0882 where the hand-designed formula achieves a loss of 0.121. It is quite surprising that our formula extracted by our approach is able to achieve a better fit than the formula hand-designed by scientists.

$^{2}$We have removed constant terms that don't depend on the position or momentum as those are just arbitrary offsets in the Hamiltonian which don't have an impact on the dynamics. See Appendix for more details.

| Test               |       |       |     | Formula             |     |     | Summed Component             |     | D           |
|--------------------|-------|-------|-----|---------------------|-----|-----|------------------------------|-----|-------------|
|                    |       |       |     |                     |     |     |                              |     | δ i − δ ˆ i |
| Constant           |       |       |     | ˆ δ i = C 1         |     |     | N/A                          |     | 0.421       |
| Simple             | ˆ δ i | =     | C 1 | + ( C 2 + M i C 3 ) | e i | e i | =                            |     |             |
|                    |       |       |     |                     |     |     | P   r i − r j   < 20         |     |             |
|                    |       |       |     |                     |     |     | j 6 = i M j                  |     | 0.121       |
| Best, without mass |       | ˆ δ i | =   | C 1 +               |     |     |                              |     |             |
|                    |       |       |     | e i                 |     |     |                              |     |             |
|                    |       |       |     | C 2 + C 3 e i   v i |     |     |                              |     |             |
|                    |       |       |     |                     | e i | =   |                              |     |             |
|                    |       |       |     |                     |     |     | j 6 = i                      |     |             |
|                    |       |       |     |                     |     |     | C 4 +   v i − v j            |     |             |
|                    |       |       |     |                     |     |     | C 5 +( C 6   r i − r j   ) C | 7   |             |
| Best, with mass    |       | ˆ δ i | =   | C 1 +               |     |     |                              |     |             |
|                    |       |       |     | e i                 |     |     |                              |     |             |
|                    |       |       |     | C 2 + C 3 M i       |     |     |                              |     |             |
|                    |       |       |     |                     | e i | =   |                              |     |             |
|                    |       |       |     |                     |     |     | j 6 = i                      |     |             |
|                    |       |       |     |                     |     |     | C 4 + M j                    |     |             |
|                    |       |       |     |                     |     |     | C 5 +( C 6   r i − r j   )   | C 7 |             |

Table 2: A comparison of both known and discovered formulas for dark matter overdensity. C$^{i}$ indicates fitted parameters, which are given in the appendix.

The formula makes physical sense. Halos closer to the dark matter halo of interest should influence its properties more, and thus the summed function scales inversely with distance. Similar to the hand-designed formula, the overdensity should scale with the total matter density nearby, and we see this in that we are summing over mass of neighbors. The other differences are very interesting, and less clear; we plan to do detailed interpretation of these results in a future astrophysics study.

As a followup, we also calculated if we could predict the halo overdensity from only velocity and position information. This is useful because the most direct observational information available is in terms of halo velocities. We perform an identical analysis without mass information, and find a curiously similar formula. The relative speed between two neighbors can be seen as a proxy for mass, which is seen in table 2. This makes sense as a more massive object will have more gravity, accelerating falling particles near it to faster speeds. This formula is also new to cosmologists, and can in principle help push forward cosmological analysis.

Symbolic generalization. As we know that our physical world is well described by mathematics, we can use it as a powerful prior for creating new models of our world. Therefore, if we distill a neural network into a simple algebra, will the algebra generalize better to unseen data? Neural nets excel at learning in high-dimensional spaces, so perhaps, by combining both of these types of models, one can leverage the unique advantages of each. Such an idea is discussed in detail in \[57\].

Here we study this on the cosmology example by masking 20% of the data: halos which have δ$^{i}$ > 1. We then proceed through the same training procedure as before, learning a GN to predict δ with L$^{1}$ regularization, and then extracting messages for examples in the training set. Remarkably, we obtain a functionally identical expression when extracting the formula from the graph network on this subset of the data. We fit these constants to the same masked portion of data on which the graph network was trained. The graph network itself obtains an average error h$^{|}$δ$^{i}$ $^{−}$ $^{δ}$ˆi$^{|}$i = 0.$^{0634}$ on the training set, and 0.142 on the out-of-distribution data. Meanwhile, the symbolic expression achieves 0.0811 on the training set, but 0.0892 on the out-of-distribution data. Therefore, for this problem, it seems a symbolic expression generalizes much better than the very graph neural network it was extracted from. This alludes back to Eugene Wigner's article: the language of simple, symbolic models is remarkably effective in describing the universe.

### 5 Conclusion

We have demonstrated a general approach for imposing physically motivated inductive biases on GNs and Hamiltonian GNs to learn interpretable representations, and potentially improved zero-shot generalization. Through experiment, we have shown that GN models which implement a bottleneck or L$^{1}$ regularization in the message passing layer, or a Hamiltonian GN flattened to pairwise and self-terms, can learn message representations equivalent to linear transformations of the true force vector or energy. We have also demonstrated a generic technique for finding an unknown force law from these models: symbolic regression is capable of fitting explicit equations to our trained model's message function. We repeated this for energies instead of forces via introduction of the "Flattened Hamiltonian Graph Network." Because GNs have more explicit substructure than their more homogeneous deep learning relatives (e.g., plain MLPs, convolutional networks), we can draw more fine-grained interpretations of their learned representations and computations. Finally, we have demonstrated our algorithm on a non-trivial dataset, and discovered a new law for cosmological dark matter.

## Acknowledgments and Disclosure of Funding

Miles Cranmer would like to thank Christina Kreisch and Francisco Villaescusa-Navarro for assistance with the cosmology dataset; and Christina Kreisch, Oliver Philcox, and Edgar Minasyan for comments on a draft of the paper. The authors would like to thank the reviewers for insightful feedback that improved this paper. Shirley Ho and David Spergel's work is supported by the Simons Foundation.

Our code made use of the following Python packages: numpy, scipy, sklearn, jupyter, matplotlib, pandas, torch, tensorflow, jax, and torch\_geometric \[58,] [59,] [60,] [61,] [62,] [63,] [43,] [64,] [65,] [44\].

## References

[1] Eugene P. Wigner. The unreasonable effectiveness of mathematics in the natural sciences. *Communications on Pure and Applied Mathematics*, 13(1):1–14, 1960. doi: 10. 1002/cpa.3160130102. URL [https://onlinelibrary.wiley.com/doi/abs/10.1002/](https://onlinelibrary.wiley.com/doi/abs/10.1002/cpa.3160130102) [cpa.3160130102](https://onlinelibrary.wiley.com/doi/abs/10.1002/cpa.3160130102). [2] Michael Schmidt and Hod Lipson. Distilling free-form natural laws from experimental data. *science*, 324(5923):81–85, 2009. [3] Guido F Montufar, Razvan Pascanu, Kyunghyun Cho, and Yoshua Bengio. On the number of linear regions of deep neural networks. In *Advances in neural information processing systems*, pages 2924–2932, 2014. [4] Peter W Battaglia, Jessica B Hamrick, Victor Bapst, Alvaro Sanchez-Gonzalez, Vinicius Zambaldi, Mateusz Malinowski, Andrea Tacchetti, David Raposo, Adam Santoro, Ryan Faulkner, et al. Relational inductive biases, deep learning, and graph networks. *arXiv preprint arXiv:1806.01261*, 2018. [5] Miles D Cranmer, Rui Xu, Peter Battaglia, and Shirley Ho. Learning Symbolic Physics with Graph Networks. *arXiv preprint arXiv:1909.05862*, 2019. [6] Peter Battaglia, Razvan Pascanu, Matthew Lai, Danilo Jimenez Rezende, et al. Interaction networks for learning about objects, relations and physics. In *Advances in neural information processing systems*, pages 4502–4510, 2016. [7] Franco Scarselli, Marco Gori, Ah Chung Tsoi, Markus Hagenbuchner, and Gabriele Monfardini. The graph neural network model. *IEEE Transactions on Neural Networks*, 20(1):61–80, 2009. [8] Michael M Bronstein, Joan Bruna, Yann LeCun, Arthur Szlam, and Pierre Vandergheynst. Geometric deep learning: going beyond euclidean data. *IEEE Signal Processing Magazine*, 34 (4):18–42, 2017. [9] Justin Gilmer, Samuel S Schoenholz, Patrick F Riley, Oriol Vinyals, and George E Dahl. Neural message passing for quantum chemistry. In *Proceedings of the 34th International Conference on Machine Learning-Volume 70*, pages 1263–1272. JMLR. org, 2017. [10] Michael B Chang, Tomer Ullman, Antonio Torralba, and Joshua B Tenenbaum. A compositional object-based approach to learning physical dynamics. *arXiv preprint arXiv:1612.00341*, 2016. [11] Alvaro Sanchez-Gonzalez, Nicolas Heess, Jost Tobias Springenberg, Josh Merel, Martin Riedmiller, Raia Hadsell, and Peter Battaglia. Graph networks as learnable physics engines for inference and control. *arXiv preprint arXiv:1806.01242*, 2018. [12] Damian Mrowca, Chengxu Zhuang, Elias Wang, Nick Haber, Li F Fei-Fei, Josh Tenenbaum, and Daniel L Yamins. Flexible neural representation for physics prediction. In *Advances in Neural Information Processing Systems*, pages 8799–8810, 2018. [13] Yunzhu Li, Jiajun Wu, Russ Tedrake, Joshua B Tenenbaum, and Antonio Torralba. Learning particle dynamics for manipulating rigid bodies, deformable objects, and fluids. *arXiv preprint arXiv:1810.01566*, 2018.

[14] Thomas Kipf, Ethan Fetaya, Kuan-Chieh Wang, Max Welling, and Richard Zemel. Neural relational inference for interacting systems. *arXiv preprint arXiv:1802.04687*, 2018. [15] Victor Bapst, Thomas Keck, A Grabska-Barwinska, Craig Donner, Ekin Dogus Cubuk, ´ SS Schoenholz, Annette Obika, AWR Nelson, Trevor Back, Demis Hassabis, et al. Unveiling the predictive power of static structure in glassy systems. *Nature Physics*, 16(4):448–454, 2020. [16] Alvaro Sanchez-Gonzalez, Jonathan Godwin, Tobias Pfaff, Rex Ying, Jure Leskovec, and Peter W Battaglia. Learning to simulate complex physics with graph networks. *arXiv preprint arXiv:2002.09405*, 2020. [17] Norman H Packard, James P Crutchfield, J Doyne Farmer, and Robert S Shaw. Geometry from a time series. *Physical review letters*, 45(9):712, 1980. [18] Bryan C. Daniels and Ilya Nemenman. Automated adaptive inference of phenomenological dynamical models. *Nature Communications*, 6(1):1–8, August 2015. ISSN 2041-1723. [19] Miguel Jaques, Michael Burke, and Timothy Hospedales. Physics-as-Inverse-Graphics: Joint Unsupervised Learning of Objects and Physics from Video. *arXiv:1905.11169 [cs]*, May 2019. [20] Michael Janner, Sergey Levine, William T. Freeman, Joshua B. Tenenbaum, Chelsea Finn, and Jiajun Wu. Reasoning About Physical Interactions with Object-Centric Models. In *International Conference on Learning Representations*, 2019. URL [https://openreview.net/forum?](https://openreview.net/forum?id=HJx9EhC9tQ) [id=HJx9EhC9tQ](https://openreview.net/forum?id=HJx9EhC9tQ). [21] Anton Bakhtin, Laurens van der Maaten, Justin Johnson, Laura Gustafson, and Ross Girshick. PHYRE: A New Benchmark for Physical Reasoning. In H. Wallach, H. Larochelle, A. Beygelzimer, F. d'Alché-Buc, E. Fox, and R. Garnett, editors, *Advances in Neural Information Processing Systems 32*, pages 5082–5093. Curran Associates, Inc., 2019. URL [http://papers.nips.](http://papers.nips.cc/paper/8752-phyre-a-new-benchmark-for-physical-reasoning.pdf) [cc/paper/8752-phyre-a-new-benchmark-for-physical-reasoning.pdf](http://papers.nips.cc/paper/8752-phyre-a-new-benchmark-for-physical-reasoning.pdf). [22] Keyulu Xu, Jingling Li, Mozhi Zhang, Simon S. Du, Ken ichi Kawarabayashi, and Stefanie Jegelka. What Can Neural Networks Reason About? In *International Conference on Learning Representations*, 2020. URL <https://openreview.net/forum?id=rJxbJeHFPS>. [23] Samuel S Schoenholz, Ekin D Cubuk, Daniel M Sussman, Efthimios Kaxiras, and Andrea J Liu. A structural approach to relaxation in glassy liquids. *Nature Physics*, 12(5):469–471, 2016. [24] Erik J Bekkers. B-Spline CNNs on Lie Groups. 2019. [25] Marc Finzi, Samuel Stanton, Pavel Izmailov, and Andrew Gordon Wilson. Generalizing Convolutional Neural Networks for Equivariance to Lie Groups on Arbitrary Continuous Data. 2020. [26] Rex Ying, Dylan Bourgeois, Jiaxuan You, Marinka Zitnik, and Jure Leskovec. GNN Explainer: A tool for post-hoc explanation of graph neural networks. *arXiv preprint arXiv:1903.03894*, 2019. [27] Miles Cranmer. PySR: Fast & Parallelized Symbolic Regression in Python/Julia, September 2020. URL <https://doi.org/10.5281/zenodo.4052869>. [28] Dario Izzo and Francesco Biscani. dcgp: Differentiable Cartesian Genetic Programming made easy., May 2020. URL <https://doi.org/10.5281/zenodo.3802555>. [29] Subham Sahoo, Christoph Lampert, and Georg Martius. Learning Equations for Extrapolation and Control. volume 80 of *Proceedings of Machine Learning Research*, pages 4442–4450, Stockholmsmässan, Stockholm Sweden, 10–15 Jul 2018. PMLR. URL [http://proceedings.](http://proceedings.mlr.press/v80/sahoo18a.html) [mlr.press/v80/sahoo18a.html](http://proceedings.mlr.press/v80/sahoo18a.html). [30] Georg Martius and Christoph H. Lampert. Extrapolation and learning equations, 2016. [31] Félix-Antoine Fortin, François-Michel De Rainville, Marc-André Gardner, Marc Parizeau, and Christian Gagné. DEAP: Evolutionary algorithms made easy. *Journal of Machine Learning Research*, 13(70):2171–2175, 2012.

[32] Silviu-Marian Udrescu and Max Tegmark. AI Feynman: A physics-inspired method for symbolic regression. *Science Advances*, 6(16):eaay2631, 2020. [33] Tony Worm and Kenneth Chiu. Prioritized Grammar Enumeration: Symbolic Regression by Dynamic Programming. In *Proceedings of the 15th Annual Conference on Genetic and Evolutionary Computation*, GECCO '13, page 1021–1028, New York, NY, USA, 2013. Association for Computing Machinery. ISBN 9781450319638. doi: 10.1145/2463372.2463486. URL <https://doi.org/10.1145/2463372.2463486>. [34] Roger Guimerà, Ignasi Reichardt, Antoni Aguilar-Mogas, Francesco A. Massucci, Manuel Miranda, Jordi Pallarès, and Marta Sales-Pardo. A Bayesian machine scientist to aid in the solution of challenging scientific problems. *Science Advances*, 6(5), 2020. doi: 10.1126/sciadv. aav6971. URL <https://advances.sciencemag.org/content/6/5/eaav6971>. [35] Matt J. Kusner, Brooks Paige, and José Miguel Hernández-Lobato. Grammar Variational Autoencoder, 2017. [36] Li Li, Minjie Fan, Rishabh Singh, and Patrick Riley. Neural-guided symbolic regression with asymptotic constraints. *arXiv preprint arXiv:1901.07714*, 2019. [37] Gert-Jan Both, Subham Choudhury, Pierre Sens, and Remy Kusters. DeepMoD: Deep learning for Model Discovery in noisy data, 2019. [38] Steven L Brunton, Joshua L Proctor, and J Nathan Kutz. Discovering governing equations from data by sparse identification of nonlinear dynamical systems. *Proceedings of the national academy of sciences*, 113(15):3932–3937, 2016. [39] Steven Atkinson, Waad Subber, Liping Wang, Genghis Khan, Philippe Hawi, and Roger Ghanem. Data-driven discovery of free-form governing differential equations. *arXiv preprint arXiv:1910.05117*, 2019. [40] Christopher Rackauckas, Yingbo Ma, Julius Martensen, Collin Warner, Kirill Zubov, Rohit Supekar, Dominic Skinner, and Ali Ramadhan. Universal differential equations for scientific machine learning. *arXiv preprint arXiv:2001.04385*, 2020. [41] Zhao Chen, Yang Liu, and Hao Sun. Deep learning of physical laws from scarce data, 2020. [42] Harsha Vaddireddy, Adil Rasheed, Anne E. Staples, and Omer San. Feature engineering and symbolic regression methods for detecting hidden physics from sparse sensor observation data. *Physics of Fluids*, 32(1):015113, 2020. doi: 10.1063/1.5136351. URL [https://doi.org/10.](https://doi.org/10.1063/1.5136351) [1063/1.5136351](https://doi.org/10.1063/1.5136351). [43] Adam Paszke, Sam Gross, Francisco Massa, Adam Lerer, James Bradbury, Gregory Chanan, Trevor Killeen, Zeming Lin, Natalia Gimelshein, Luca Antiga, Alban Desmaison, Andreas Kopf, Edward Yang, Zachary DeVito, Martin Raison, Alykhan Tejani, Sasank Chilamkurthy, Benoit Steiner, Lu Fang, Junjie Bai, and Soumith Chintala. PyTorch: An Imperative Style, High-Performance Deep Learning Library. In H. Wallach, H. Larochelle, A. Beygelzimer, F. d'Alché-Buc, E. Fox, and R. Garnett, editors, *Advances in Neural Information Processing Systems 32*, pages 8024–8035. Curran Associates, Inc., 2019. URL [http://papers.neurips.cc/paper/](http://papers.neurips.cc/paper/9015-pytorch-an-imperative-style-high-performance-deep-learning-library.pdf) [9015-pytorch-an-imperative-style-high-performance-deep-learning-library.](http://papers.neurips.cc/paper/9015-pytorch-an-imperative-style-high-performance-deep-learning-library.pdf) [pdf](http://papers.neurips.cc/paper/9015-pytorch-an-imperative-style-high-performance-deep-learning-library.pdf). [44] Matthias Fey and Jan E. Lenssen. Fast Graph Representation Learning with PyTorch Geometric. In *ICLR Workshop on Representation Learning on Graphs and Manifolds*, 2019. [45] Diederik P Kingma and J Adam Ba. A method for stochastic optimization. *arXiv preprint arXiv:1412.6980*, 2014. [46] Alvaro Sanchez-Gonzalez, Victor Bapst, Kyle Cranmer, and Peter Battaglia. Hamiltonian graph networks with ode integrators. *arXiv preprint arXiv:1909.12790*, 2019. [47] Samuel Greydanus, Misko Dzamba, and Jason Yosinski. Hamiltonian neural networks. In *Advances in Neural Information Processing Systems*, pages 15353–15363, 2019.

- [48] Peter Toth, Danilo Jimenez Rezende, Andrew Jaegle, Sébastien Racanière, Aleksandar Botev, and Irina Higgins. Hamiltonian generative networks. *arXiv preprint arXiv:1909.13789*, 2019. [49] Miles Cranmer, Sam Greydanus, Stephan Hoyer, Peter Battaglia, David Spergel, and Shirley Ho. Lagrangian Neural Networks. In *ICLR 2020 Workshop on Integration of Deep Neural Models and Differential Equations*, 2020. [50] Jiang Wang, Simon Olsson, Christoph Wehmeyer, Adrià Pérez, Nicholas E Charron, Gianni De Fabritiis, Frank Noé, and Cecilia Clementi. Machine learning of coarse-grained molecular dynamics force fields. *ACS central science*, 5(5):755–767, 2019. [51] Francisco Villaescusa-Navarro, ChangHoon Hahn, Elena Massara, Arka Banerjee, Ana Maria Delgado, Doogesh Kodi Ramanah, Tom Charnock, Elena Giusarma, Yin Li, Erwan Allys, et al. The Quijote simulations. *arXiv preprint arXiv:1909.05273*, 2019. [52] Jonathan Frankle and Michael Carbin. The lottery ticket hypothesis: Finding sparse, trainable neural networks. In *International Conference on Learning Representations*, 2018. [53] Scott Dodelson. *Modern cosmology*. 2003. [54] David N Spergel, Licia Verde, Hiranya V Peiris, E Komatsu, MR Nolta, CL Bennett, M Halpern, G Hinshaw, N Jarosik, A Kogut, et al. First-year Wilkinson Microwave Anisotropy Probe (WMAP)\* observations: determination of cosmological parameters. *The Astrophysical Journal Supplement Series*, 148(1):175, 2003. [55] Planck Collaboration. Planck 2018 results. VI. Cosmological parameters. *arXiv e-prints*, art. arXiv:1807.06209, July 2018. [56] Carlos S. Frenk, Simon D. M. White, Marc Davis, and George Efstathiou. The Formation of Dark Halos in a Universe Dominated by Cold Dark Matter. *Astrophysical Journal*, 327:507, April 1988. doi: 10.1086/166213. [57] Gary Marcus. The next decade in AI: four steps towards robust artificial intelligence. *arXiv preprint arXiv:2002.06177*, 2020. [58] S. van der Walt, S. C. Colbert, and G. Varoquaux. The NumPy Array: A Structure for Efficient Numerical Computation. *Computing in Science Engineering*, 13(2):22–30, 2011. [59] Pauli Virtanen, Ralf Gommers, Travis E. Oliphant, Matt Haberland, Tyler Reddy, David Cournapeau, Evgeni Burovski, Pearu Peterson, Warren Weckesser, Jonathan Bright, Stéfan J. van der Walt, Matthew Brett, Joshua Wilson, K. Jarrod Millman, Nikolay Mayorov, Andrew
  - R. J. Nelson, Eric Jones, Robert Kern, Eric Larson, CJ Carey, ˙Ilhan Polat, Yu Feng, Eric W. Moore, Jake Vand erPlas, Denis Laxalde, Josef Perktold, Robert Cimrman, Ian Henriksen,
- E. A. Quintero, Charles R Harris, Anne M. Archibald, Antônio H. Ribeiro, Fabian Pedregosa, Paul van Mulbregt, and SciPy 1. 0 Contributors. SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python. *Nature Methods*, 17:261–272, 2020. doi: https://doi.org/10. 1038/s41592-019-0686-2. [60] Fabian Pedregosa, Gaël Varoquaux, Alexandre Gramfort, Vincent Michel, Bertrand Thirion, Olivier Grisel, Mathieu Blondel, Peter Prettenhofer, Ron Weiss, Vincent Dubourg, Jake Vanderplas, Alexandre Passos, David Cournapeau, Matthieu Brucher, Matthieu Perrot, and Édouard Duchesnay. Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*, 12(85):2825–2830, 2011. URL <http://jmlr.org/papers/v12/pedregosa11a.html>. [61] Thomas Kluyver, Benjamin Ragan-Kelley, Fernando Pérez, Brian Granger, Matthias Bussonnier, Jonathan Frederic, Kyle Kelley, Jessica Hamrick, Jason Grout, Sylvain Corlay, Paul Ivanov, Damián Avila, Safia Abdalla, and Carol Willing. Jupyter Notebooks – a publishing format for reproducible computational workflows. In F. Loizides and B. Schmidt, editors, *Positioning and Power in Academic Publishing: Players, Agents and Agendas*, pages 87 – 90. IOS Press, 2016. [62] J. D. Hunter. Matplotlib: A 2D Graphics Environment. *Computing in Science & Engineering*, 9 (3):90–95, 2007.

[63] Wes McKinney. Data Structures for Statistical Computing in Python. In Stéfan van der Walt and Jarrod Millman, editors, *Proceedings of the 9th Python in Science Conference*, pages 56 – 61, 2010. doi: 10.25080/Majora-92bf1922-00a. [64] Martín Abadi, Paul Barham, Jianmin Chen, Zhifeng Chen, Andy Davis, Jeffrey Dean, Matthieu Devin, Sanjay Ghemawat, Geoffrey Irving, Michael Isard, et al. Tensorflow: A system for large-scale machine learning. In *12th* {*USENIX*} *Symposium on Operating Systems Design and Implementation (*{*OSDI*} *16)*, pages 265–283, 2016. [65] James Bradbury, Roy Frostig, Peter Hawkins, Matthew James Johnson, Chris Leary, Dougal Maclaurin, and Skye Wanderman-Milne. JAX: composable transformations of Python+NumPy programs, 2018. URL <http://github.com/google/jax>.

# Supplementary

## A Model Implementation Details

Code for our implementation can be found at [https://github.com/MilesCranmer/symbolic\\_](https://github.com/MilesCranmer/symbolic_deep_learning) [deep\\_learning](https://github.com/MilesCranmer/symbolic_deep_learning). Here we describe how one can implement our model from scratch in a deep learning framework. The main argument in this paper is that one can apply strong inductive biases to a deep learning model to simplify the extraction of a symbolic representation of the learned model. While we emphasize that this idea is general, in this section we focus on the specific Graph Neural Networks we have used as an example throughout the paper.

### A.1 Basic Graph Representation

We would like to use the graph G = (V, E) to predict an updated graph G$^{0}$ = (V 0 , E). Our input dataset is a graph G = (V, E) consisting of N$^{v}$ nodes with L v features each: $^{V}$ $^{=}$ {$^{v}$i}i=1:N$^{v}$ , with each $^{v}$$^{i}$ ∈ $^{R}$ L v . The nodes are connected by N$^{e}$ edges: $^{E}$ $^{=}$ {(rk, sk)}k=1:N$^{e}$ , where $^{r}$k, s$^{k}$ ∈ {$^{1}$ : $^{N}$$^{v}$} are the indices for the receiving and sending nodes, respectively. We would like to use this graph to predict another graph V $^{0}$ $^{=}$ {$^{v}$ 0 i }i=1:N$^{v}$ , where each $^{v}$ 0 $^{i}$ ∈ $^{R}$ L v0 is the node corresponding to v$^{i}$ . The number of features in these predicted nodes, L v0 , need not necessarily be the same as for the input nodes (L v ), though this could be the case for dynamical models where one is predicting updated states of particles. For more general regression problems, the number of output features is arbitrary.

Edge model. The prediction is done in two parts. We create the first neural network, the edge model (or "message function"), to compute messages from one node to another: φ e : $^{R}$ L × R L $^{v}$ → $^{R}$ L 0 . Here, L e is the number of message features. In the bottleneck model, one sets L e equal to the known dimension of the force, which is 2 or 3 for us. In our models, we set L e = 100 for the standard and L$^{1}$ models, and 200 for the KL model (which is described separately later on). We create φ e as a multi-layer perceptron with ReLU activations and two hidden layers, each with 300 hidden nodes. The mapping is e 0 $^{k}$ = φ e (v$^{r}$$^{k}$ , v$^{s}$$^{k}$ ) for all edges indexed by k (i.e., we concatenate the receiving and sending node features).

Aggregation. These messages are then pooled via element-wise summation for each receiving node i into the summed message, e¯ 0 $^{i}$ ∈ $^{R}$ L e . This can be written as e¯ 0 $^{i}$ = P k∈{1:N$^{e}$|rk=i} e 0 k .

Node model. We create a second neural network to predict the output nodes, v 0 i , for each i from the corresponding summed message and input node. This net can be written as φ v : $^{R}$ L v ×R L e → $^{R}$ L v0 , and has the mapping: vˆ 0 $^{i}$ = φ v (v$^{i}$ , e¯ 0 i ), where vˆ 0 i is the prediction for v 0 i . We also create φ v as a

multi-layer perceptron with ReLU activations and two hidden layers, each with 300 hidden nodes. This model is then trained with the loss function as described later in this section.

Summary. We can write out our forward model for the bottleneck, standard, and L$^{1}$ models as:

Input graph 
$$G = (V, E)$$
 with

nodes (e.g., positions of particles) $^{V}$ $^{=}$ {$^{v}$i}i=1:N$^{v}$ ; $^{v}$$^{i}$ ∈ $^{R}$

L v , and

edges (indices of connected nodes) $^{E}$ $^{=}$ {(rk, sk)}k=1:N$^{e}$ ; $^{r}$k, s$^{k}$ ∈ {$^{1}$ : $^{N}$

v }.

Compute messages for each edge: e

0 $^{k}$ = φ e (v$^{r}$$^{k}$ , v$^{s}$$^{k}$ ),

$$\mathbf{e}'_k \in \mathbb{R}^{L^{e'}}$$
, then

sum for each receiving node i : e¯

0 $^{i}$ =

X k∈{1:N$^{e}$|rk=i} e 0 k ,

$$\bar{\mathbf{e}}'_i \in \mathbb{R}^{L^{e'}}$$
.

Compute output node prediction: vˆ

0 $^{i}$ = φ v (v$^{i}$ , e¯ 0 i )

vˆ 0 $^{i}$ ∈ $^{R}$ L v0 .

Loss. We jointly optimize the parameters in φ v and φ $^{e}$ via mini-batch gradient descent with Adam as the optimizer. Our total loss function for optimizing is:

$$\begin{aligned} \mathcal{L} &= \mathcal{L}_v + \alpha_1 \mathcal{L}_e + \alpha_2 \mathcal{L}_n, \text{ where} \\ \text{the prediction loss is } \mathcal{L}_v &= \frac{1}{N^v} \sum_{i \in \{1:N^v\}} |\mathbf{v}'_i - \hat{\mathbf{v}}'_i|, \\ \text{the message regularization is } \mathcal{L}_e &= \frac{1}{N^e} \begin{cases} \sum_{k \in \{1:N^e\}} |\mathbf{e}'_k|, & \mathbf{L}_1 \\ 0, & \text{Standard} \\ 0, & \text{Bottleneck} \end{cases}, \\ \text{with the regularization constant } \alpha_1 &= 10^{-2}, \text{ and the} \\ \text{regularization for the network weights is } \mathcal{L}_n &= \sum_{l \in \{1:N^l\}} |w_l|^2, \\ \text{with } \alpha_2 &= 10^{-8}, \end{aligned}$$

where v 0 i is the true value for the predicted node i. w$^{l}$ is the l-th network parameter out of N$^{l}$ total parameters. This implementation can be visualized during training in the video [https://github.com/MilesCranmer/symbolic\\_deep\\_learning](https://github.com/MilesCranmer/symbolic_deep_learning). During training, we also apply a random translation augmentation to all the particle positions to artificially generate more training data.

Next, we describe the KL variant of this model. Note that for the cosmology example in section 4.3, we use the L$^{1}$ model described above with 500 hidden nodes (found with coarse hyperparameter tuning to optimize accuracy) instead of 300, but other parameters are set the same.

### A.2 KL Model

The KL model is a variational version of the GN implementation above, which models the messages as distributions. We choose a normal distribution for each message component with a prior of µ = 0, σ = 1. More specifically, the output of φ e should now map to twice as many features as it is predicting a mean and variance, hence we set L e = 200. The first half of the outputs of φ $^{e}$ now represent the means, and the second half of the outputs represent the log variance of a particular message component. In other words,

$$\begin{aligned} \mu_k' &= \phi_{1:100}^e(\mathbf{v}_{r_k}, \mathbf{v}_{s_k}), \\ \sigma_k'^2 &= \exp(\phi_{101:200}^e(\mathbf{v}_{r_k}, \mathbf{v}_{s_k})), \\ \mathbf{e}_k' &\sim \mathcal{N}(\mu_k', \text{diag}(\sigma_k'^2)), \\ \bar{\mathbf{e}}_i' &= \sum_{k \in \{1: N^e | r_k = i\}} \mathbf{e}_k', \\ \hat{\mathbf{v}}_i' &= \phi^v(\mathbf{v}_i, \bar{\mathbf{e}}_i'), \end{aligned}$$

where N is a multinomial Gaussian distribution. Every time the graph network is run, we calculate the mean and log variance of messages, sample each message once to calculate e 0 k , and pass those samples through a sum to compute a sample of e¯ 0 i and then pass that value through the edge function to compute a sample of vˆ 0 i . The loss is calculated normally, except for Le, which becomes the KL divergence with respect to our Gaussian prior of µ = 0, σ = 1:

$$\mathcal{L}_e = \frac{1}{N^e} \sum_{k=1:N^e} \sum_{j=\{1:L^e'\}/2} \frac{1}{2} \left( \mu_{k,j}^2 + \sigma_{k,j}^2 - \log(\sigma_{k,j}^2) \right),$$

with α$^{1}$ = 1 (equivalent to β = 1 for the loss of a β-Variational Autoencoder; simply the standard VAE). The KL-divergence loss also encourages sparsity in the messages e 0 k similar to the L$^{1}$ loss. The difference is that here, an uninformative message component will have µ = 0, σ = 1 (a KL of 0) rather than a small absolute value. We train the networks with a decaying learning schedule as given in the example code.

#### A.3 Constraining Information in the Messages

The hypothesis which motivated our graph network inductive bias is that if one minimizes the dimension of the vector space used by messages in a GN, the components of message vectors will learn to be linear combinations of the true forces (or equivalent underlying summed function) for the system being learned. The key observation is that e 0 k could learn to correspond to the true force vector imposed on the rk-th body due to its interaction with the sk-th body.

Here, we sketch a rough mathematical explanation of our hypothesis that we will reconstruct the true force in the graph network given our inductive biases. Newtonian mechanics prescribes that force vectors, $^{f}$$^{k}$ ∈ F, can be summed to produce a net force, $^{P}$ k $^{f}$$^{k}$ $^{=}$ ¯f ∈ F, which can then be used to update the dynamics of a body. Our model uses the i-th body's pooled messages, ¯e$^{0}$ i to update the body's state via v 0 $^{i}$ = φ v (v$^{i}$ ,¯e$^{0}$ i ). If we assume our GN is trained to predict accelerations perfectly for any number of bodies, this means (ignoring mass) that ¯f$^{i}$ = P rk=i f$^{k}$ = φ v (v$^{i}$ , P rk=i e 0 k ) = φ v (v$^{i}$ ,¯e$^{0}$ i ). Since this is true for any number of bodies, we also have the result for a single interaction: ¯f$^{i}$ = $^{f}$k,rk=$^{i}$ = φ v (v$^{i}$ , e 0 k,rk=i ) = φ v (v$^{i}$ ,¯e$^{0}$ i ). Thus, we can substitute this expression into the multi-interaction case: P rk=i φ v (v$^{i}$ , e 0 k ) = φ v (v$^{i}$ ,¯e$^{0}$ i ) = φ v (v$^{i}$ , P rk=i e 0 k ). From this relation, we see that φ $^{v}$ has to be a linear transformation conditioned on v$^{i}$ . Therefore, for cases where φ v (v$^{i}$ ,¯e$^{0}$ i ) is invertible in ¯e$^{0}$ i (which becomes true when ¯e$^{0}$ i is the same dimension as the output of φ v ), we can write e 0 $^{k}$ = (φ v (v$^{i}$ , ·))$^{−}$$^{1}$ (fk), which is also a linear transform, meaning that the message vectors are linear transformations of the true forces when L e is equal to the dimension of the forces.

If the dimension of the force vectors (or what the minimum dimension of the message vectors "should" be) is unknown, one can encourage the messages to be sparse by applying L$^{1}$ or Kullback-Leibler regularizations to the messages in the GN. The aim is for the messages to learn the minimal vector space required for the computation automatically. This is a more mathematical explanation of why the message features are linear combinations of the force vectors, when our inductive bias of a bottleneck or sparse regularization is applied. We emphasize that this is a new contribution: never before has previous work explicitly identified the forces in a graph network.

General Graph Neural Networks. In all of our models here, we assume the dataset does not have edge-specific features, such as a different coupling constants between different particles, but these could be added by concatenating edge features to the receiving and sending node input to φ e . We also assume there are no global properties. The graph neural network is described in general form in \[4\]. All of our techniques are applicable to the general form: one would approximate φ $^{e}$ with a symbolic model with included input edge parameters, and also fit the global model, denoted φ u .

#### A.4 Flattened Hamiltonian Graph Network.

As part of this study, we also consider an alternate dynamical model that is described by a linear latent space other than force vectors. In the Hamiltonian formalism of classical mechanics, energies of pairwise interactions and kinetic and potential energies of particles are pooled into a global energy value, H, which is a scalar. We label pairwise interaction energy Hpair and the energy of individual particles as Hself. Thus, using our previous graph notation, we can write the total energy of a system as:

$$\mathcal{H} = \sum_{i=1:N^v} \mathcal{H}_{\text{self}}(\mathbf{v}_i) + \sum_{k \in \{1:N^e\}} \mathcal{H}_{\text{pair}}(\mathbf{v}_{r_k}, \mathbf{v}_{s_k}). \quad (1)$$

For particles interacting via gravity, this would be

$$\mathcal{H} = \sum_i \frac{p_i^2}{2m_i} - \frac{1}{2} \sum_{i \neq j} \frac{m_i m_j}{|\mathbf{r}_i - \mathbf{r}_j|}, \quad (2)$$

where p$^{i}$ , m$^{i}$ , r$^{i}$ indicates the momentum, mass, and position of particle i, respectively, and we have set the gravitational constant to $^{1}$. Following \[47,] [46\], we could model H as a neural network, and apply Hamilton's equations to create a dynamical model. More specifically, as in \[46\], we can predict H as the global property of a GN (this is called a Hamiltonian Graph Network or HGN). However, energy, like forces in Cartesian coordinates, is a summed quantity. In other words, energy is another "linear latent space" that describes the dynamics.

Therefore, we argue that an HGN will be more interpretable if we explicitly sum up energies over the system, rather than compute H as a global property of a GN. Here, we introduce the "Flattened Hamiltonian Graph Network," or "FlatHGN", which uses eq. (1) to construct a model that works on a graph. We set up two Multi-Layer Perceptrons (MLPs), one for each node:

$$\mathcal{H}_{\text{self}} : \mathbb{R}^{L^v} \rightarrow \mathbb{R}, \quad (3)$$

and one for each edge:

$$\mathcal{H}_{\text{pair}} : \mathbb{R}^{L^v} \times \mathbb{R}^{L^v} \rightarrow \mathbb{R}. \quad (4)$$

Note that the derivatives of H now propagate through the pool, e.g.,

$$\frac{\partial \mathcal{H}(V)}{\partial \mathbf{v}_i} = \frac{\partial \mathcal{H}_{\text{self}}(\mathbf{v}_i)}{\partial \mathbf{v}_i} + \sum_{r_k=i} \frac{\partial \mathcal{H}_{\text{pair}}(\mathbf{e}_k, \mathbf{v}_{r_k}, \mathbf{v}_{s_k})}{\partial \mathbf{v}_i} + \sum_{s_k=i} \frac{\partial \mathcal{H}_{\text{pair}}(\mathbf{e}_k, \mathbf{v}_{r_k}, \mathbf{v}_{s_k})}{\partial \mathbf{v}_i}. \quad (5)$$

This model is similar to the Lagrangian Graph Network proposed in \[49\]. Now, should this FlatHGN learn energy functions such that we can successfully model the dynamics of the system with Hamilton's equations, we would expect that Hself and Hpair should be analytically similar to parts of the true Hamiltonian. Since we have broken the traditional HGN into a FlatHGN, we now have pairwise and self energies, rather than a single global energy, and these are simpler to extract and interpret. This is a similar inductive bias to the GN we introduced previously. To train a FlatHGN, one can follow our strategy above, with the output predictions made using Hamilton's equations applied to our H. One difference is that we also regularize Hpair, since it is degenerate with Hself in that it can pick up self energy terms.

## B Simulations

Our simulations for sections 4.1 and 4.2 were written using the JAX library ([https://github.](https://github.com/google/jax) [com/google/jax](https://github.com/google/jax)) so that we could easily vectorize computations over the entire dataset of 10,000 simulations. Example "long exposures" for each simulation in 2D are shown in fig. 4. To create each simulation, we set up the following potentials between two particles, 1 (receiving) and 2 (sending). Here, r 0 $^{12}$ is the distance between two particles plus 0.01 to prevent singularities. For particle i, m$^{i}$ is the mass, q$^{i}$ is the charge, n is the number of particles in the simulation, r$^{i}$ is the position of a

![](_page_18_Figure_0.jpeg)

Figure 4: Examples of a selection of simulations, for 4 nodes and two dimensions. Decreasing transparency shows increasing time, and size of points shows mass.

particle, and r˙ $^{i}$ is the velocity of a particle.

|                | $1/r^2 : U_{12} = -m_1 m_2 / r'_{12}$                                                      |
|----------------|--------------------------------------------------------------------------------------------|
|                | $1/r : U_{12} = m_1 m_2 \log(r'_{12})$                                                     |
|                | Spring : $U_{12} = (r'_{12} - 1)^2$                                                        |
|                | Damped : $U_{12} = (r'_{12} - 1)^2 + \mathbf{r}_1 \cdot \dot{\mathbf{r}}_1 / n$            |
|                | Charge : $U_{12} = q_1 q_2 / r'_{12}$                                                      |
| Dicontinuous : | $U_{12} = \begin{cases} 0, & r'_{12} < 2 \\ (r'_{12} - 1)^2, & r'_{12} \geq 2 \end{cases}$ |

All variables lack units. Here, m$^{i}$ is sampled from a log-normal distribution with µ = 0, σ = 1. Each component of r$^{i}$ and r˙ $^{i}$ is randomly sampled from a normal distribution with µ = 0, σ = 1. q$^{i}$ is randomly drawn from a set of two elements: {−1, $^{1}$}, representing charge. The acceleration of a given particle is then

$$\ddot{\mathbf{r}}_i = -\frac{1}{m_i} \sum_j \nabla_{\mathbf{r}_i} U_{ij}. \quad (6)$$

This is integrated over 1000 time steps of a fixed step size for a given random initial configuration using an adaptive RK4 integrator. The step size varies for each simulation due to the differences in scale. It is: 0.005 for 1/r, 0.001 for 1/r$^{2}$ , 0.01 for Spring, 0.02 for Damped, 0.001 for Charge, and 0.01 for Discontinuous. Each simulation is performed in two and three dimensions, for 4 and 8 bodies. We store these simulations on disk. For training, the simulations for the particular problem being studied are loaded, and each instantaneous snapshot of each simulation is converted to a fully connected graph, with the predicted property (nodes of V 0 , see appendix A) being the acceleration of the particles at that snapshot.

The test loss of each model trained on each simulation set is given in table 3.

As described in the text (and visualized in the drive video), we can fit linear combinations of the true force components to each of the significant features of a message vector. This fit is summarized by table 1, and the fit itself is visualized in fig. 5 for various models on the 2D spring simulation.

| Sim.     | Standard | Bottleneck | L 1   | KL  | FlatHGN |
|----------|----------|------------|-------|-----|---------|
| Charge-2 | 49       | 50         | 52    | 60  | 55      |
| Charge-3 | 1.2      | 0.99       | 0.94  | 4.2 | 3.5     |
| Damped-2 | 0.30     | 0.33       | 0.30  | 1.5 | 0.35    |
| Damped-3 | 0.41     | 0.45       | 0.40  | 3.3 | 0.47    |
| Disc.-2  | 0.064    | 0.074      | 0.044 | 1.8 | 0.075   |
| Disc.-3  | 0.20     | 0.18       | 0.13  | 4.2 | 0.14    |
| − 1 r    |          |            |       |     |         |
| -2       | 0.077    | 0.069      | 0.079 | 3.5 | 0.05    |
| − 1 r    |          |            |       |     |         |
| -3       | 0.051    | 0.050      | 0.055 | 3.5 | 0.017   |
| − 2 r    |          |            |       |     |         |
| -2       | 1.6      | 1.6        | 1.2   | 9.3 | 1.3     |
| − 2 r    |          |            |       |     |         |
| -3       | 4.0      | 3.6        | 3.4   | 9.8 | 2.5     |
| Spring-2 | 0.047    | 0.046      | 0.045 | 1.7 | 0.016   |
| Spring-3 | 0.11     | 0.11       | 0.090 | 3.8 | 0.010   |

Table 3: Test prediction losses for each model on each dataset in two and three dimensions. The training was done with the same batch size, schedule, and number of epochs.

![](_page_19_Figure_2.jpeg)

Figure 5: The most significant message components of each model compared with a linear combination of the force components: this example, the spring simulation in 2D with eight nodes for training. These plots demonstrate that the GN's messages have learned to be linear transformations of the vector components of the true force, in this case a springlike force, after applying an inductive bias to the messages.

### C Symbolic Regression Details

After training a model on each simulation, we convert a deep learning model to a symbolic expression by approximating subcomponents of the model with symbolic regression, over observed inputs and outputs. For our aforementioned GNN implementation, we can record the outputs of φ e and φ v for various data points in the training set.

For models other than the bottleneck and Hamiltonian model (where we explicitly limit the features) we calculate the most significant output features of φ e (we also refer to the output features as "message components"). For the L$^{1}$ and standard model, this is done by sorting the message components with the largest standard deviation; the most significant feature is the one with the largest standard deviation, which are the features we study. For the KL model, we consider the feature with the largest KL-divergence: µ $^{2}$ + σ $^{2}$ − log σ 2 . These features are the ones we consider to be containing information used by the GN, so are the ones we fit symbolic expressions to.

As an example, here we fit the most significant feature, which we refer to as φ e 1 , over random examples of the training dataset. We do this for the particle simulations in section 4.1. The inputs to the actual φ e $^{1}$ neural network are: m1, m2, q1, q2, x1, x2, . . . (mass, charge, and Cartesian positions of receiving and sending node), leaving us with many examples of (m1, m2, q1, q2, x1, x2, . . . , φ$^{e}$ ). We would like to fit a symbolic expression to map (m1, m2, q1, q2, x1, x2, . . .) → $^{φ}$ e 1 . To simplify things for this symbolic model, we convert the input position variables to a more interpretable format: $^{∆}$$^{x}$ $^{=}$ $^{x}$2−$^{x}$$^{1}$ for x displacement, likewise for y (and z, if it is a 3D simulation), and r = p ∆x $^{2}$ + ∆y $^{2}$ (+∆z 2) for distance.

We then pass these (m1, m2, q1, q2, ∆x, ∆y,(∆z,)r, φ$^{e}$ 1 ) examples (we take 5000 examples for each of our tests) to *eureqa*, and ask it to fit φ e 1 as a function of the others by minimizing the mean absolute error (MAE). We allow it to use the operators $^{+}$, −, ×, /, >, <, ^, exp, log, IF(·, ·, ·) as well as real constants in its solutions. We score complexity by counting the number of occurrences of each operator, constant, and input variable. We weight ^, exp, log, IF(·, ·, ·) as three times the other operators, since these are more complex operations. *eureqa* outputs the best equation at each complexity level, denoted by c. Example outputs are shown in table 4 for the 1/r and 1/r$^{2}$ simulations. We select a formula from this list by taking the one that maximizes the fractional drop in mean absolute error (MAE) over an increase in complexity from the next best model. This is analogous to Occam's Razor: we jointly optimize for simplicity and accuracy of the model. The objective itself can be written as maximizing (−∆ log(MAEc)/∆c) over the best model at each maximum complexity level, and is schematically illustrated in fig. 6. We find experimentally that this score produces the best-recovered solutions in a variety of tests on different generating equations.

Following the process of fitting analytic equations to the messages, we fit a single analytic expression to model φ e as a function of the simplified input variables. We recover many analytical expressions that were used to generate the data, examples of which are listed below (a, b indicate learned constants):

- Spring, 2D, L$^{1}$ (expect φ e $^{1}$ ≈ ($^{a}$ · (∆x, $^{∆}$y))($^{r}$ − 1) + $^{b}$).

$$\phi_1^\epsilon \approx 1.36\Delta y + 0.60\Delta x - \frac{0.60\Delta x + 1.37\Delta y}{r} - 0.0025$$

• 1/r$^{2}$

, 3D, Bottleneck (expect φ

e

$$\text{exct } \phi_1^e \approx \frac{\mathbf{a} \cdot (\Delta x, \Delta y, \Delta z)}{r^3} + b).$$

a·(∆x,∆y,∆z)

$^{3}$ + b).

- Discontinuous, 2D, L$^{1}$ (expect φ e $^{1}$ ≈ IF(r > $^{2}$,($^{a}$ · (∆x, $^{∆}$y, $^{∆}$z))r, 0) + $^{b}$).

$$\phi_1^\epsilon \approx \text{IF}(r > 2, 0.15r\Delta y + 0.19r\Delta x, 0) - 0.038$$

Examples of failed reconstructions. Note that reconstruction does not always succeed, especially for training strategies other than L$^{1}$ or bottleneck models that cannot successfully find compact representations of the right dimensionality. We demonstrate some failed examples below:

- Spring, 3D, KL (expect φ e $^{1}$ ≈ ($^{a}$ · (∆x, $^{∆}$y, $^{∆}$z))($^{r}$ − 1) + $^{b}$).

$$\phi_1^\epsilon \approx 0.57\Delta y + 0.32\Delta z$$

- 1/r, 3D, Standard (expect φ e 1 ≈ a·(∆x,∆y,∆z) r $^{2}$ + b).

$$\phi_1^\epsilon \approx \frac{0.041 + m_2 \text{IF}(\Delta z > 0, 0.021, 0.067)}{r}$$

We do not attempt to make any general statements about when symbolic regression applied to the message components will fail or succeed in extracting the true law. Simply, we show that it is possible, for a variety of physical systems, and argue that reconstruction is more likely by the inclusion of a strong inductive bias in the network.

A full table of successes and failures in reconstructing the force law over the different n-body experiments is given in table 5. While the equations given throughout the paper were generated with *eureqa*, to create this table in particular, we switched from *eureqa* to *PySR*. This is because *PySR* allows us to configure a controlled experiment with fixed hyperparameters and total mutation steps for each force law, whereas Eureqa makes these controls inaccessible. However, given enough training time, we found *eureqa* and *PySR* produced equivalent results for equations at this simplicity level.

| e 1 φ e 1 φ e 1 φ e 1 φ e 1 φ | = = = = = Solutions 0 | (6 (3 (31 (2 | 162 07 61 6∆ 78 | extracted for the 2D 1 /r 2 + (5 62 + 20 3 m 2 ∆ x − + 19 9 m 2 ∆ x − 154 m 2 ∆ + 20 9∆ x − 154 m 2 ∆ y ) x − 152 m 2 ∆ y ) /r 3 − 152 m 2 ∆ y ) /r 3 | Simulation MAE 153 m 2 ∆ y ) /r 3 17.954713 y ) /r 3 18.400224 /r 3 42.323236 69.447467 131.42547 | Complexity 22 20 18 16 14 |
|-------------------------------|-----------------------|--------------|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|---------------------------|
| 1                             | = −                   | 142          | m               | 2 ∆ y/r 3                                                                                                                                             | 160.31243                                                                                         | 12                        |
| 1                             | = −                   | 184∆         |                 | y/r 2                                                                                                                                                 | 913.83751                                                                                         | 8                         |
| 1                             | = −                   | 7            | 32∆             | y/r                                                                                                                                                   | 1520.9493                                                                                         | 6                         |
| 1                             | = −                   | 0            | 282             | m 2 ∆ y                                                                                                                                               | 1551.3437                                                                                         | 5                         |
| 1                             | = −                   | 0            | 474∆            | y                                                                                                                                                     | 1558.9756                                                                                         | 3                         |
| 1                             | = 0                   | 0148         |                 |                                                                                                                                                       | 1570.0905                                                                                         | 1                         |
| Solutions                     |                       |              | extracted       | for the 2D 1 /r Simulation                                                                                                                            | MAE                                                                                               | Complexity                |
| 1                             | = (4                  |              | 53 m            | 2 ∆ y − 1 53∆ x − 15 0 m                                                                                                                              | 2 ∆ x ) /r 2 − 0 209 0.37839388                                                                   | 22                        |
| 1                             | = (4                  |              | 58 m            | 2 ∆ y − ∆ x − 15 2 m 2 ∆ x                                                                                                                            | ) /r 2 − 0 227 0.38                                                                               | 20                        |
| 1                             | = (4                  |              | 55 m            | 2 ∆ y − 15 5 m 2 ∆ x ) /r 2 −                                                                                                                         | 0 238 0.42                                                                                        | 18                        |
| 1                             | = (4                  |              | 59 m            | 2 ∆ y − 15 5 m 2 ∆ x ) /r 2                                                                                                                           | 0.46575519                                                                                        | 16                        |
| 1                             | = (10                 |              | 7∆              | y − 15 5 m 2 ∆ x ) /r 2                                                                                                                               | 2.48                                                                                              | 14                        |
| 1                             | = (∆                  |              | y −             | 15 6 m 2 ∆ x ) /r 2                                                                                                                                   | 6.96                                                                                              | 12                        |
| 1                             | = −                   | 15           | 6 m             | 2 ∆ x/r 2                                                                                                                                             | 7.93                                                                                              | 10                        |
| 1                             | = −                   | 34           | 8∆              | x/r 2                                                                                                                                                 | 31.17                                                                                             | 8                         |
| 1                             | = −                   | 8            | 71∆             | x/r                                                                                                                                                   | 68.345174                                                                                         | 6                         |
| 1                             | = −                   | 0            | 360             | m 2 ∆ x                                                                                                                                               | 85.743106                                                                                         | 5                         |
| 1                             | = −                   | 0            | 632∆            | x                                                                                                                                                     | 93.052677                                                                                         | 3                         |
| 1                             | = −                   | ∆            | x               |                                                                                                                                                       | 96.708906                                                                                         | 2                         |
| 1                             | = −                   | 0            | 303             |                                                                                                                                                       | 103.29053                                                                                         | 1                         |

Table 4: Results of using symbolic regression to fit equations to the most significant (see text) feature of φ e , denoted φ e 1 , for the 1/r$^{2}$ (top) and 1/r (bottom) force laws, extracted from the bottleneck model. We expect to see φ e 1 ≈ a·(∆x,∆y,∆z) $^{r}$$^{α}$ + b, for arbitrary a and b, and α = 2 for the 1/r simulation and α = 3 for the 1/r$^{2}$ simulation, which is approximately what we recover. The row with a gray background has the largest fractional drop in mean absolute error in their tables, which according to our parametrization of Occam's razor, represents the best model. This demonstrates a technique for learning an unknown "force law" with a constrained graph neural network.

Pure *eureqa* experiment To demonstrate that *eureqa* by itself is not capable of finding many of the equations considered from the raw high-dimensional dataset, we ran it on the simulation data without our GN's factorization of the problem, giving it the features of every particle. As expected, even after convergence, it cannot find meaningful equations; all of the solutions it provides for the n-body system are very poor fits. One such example of an equation, for the acceleration of particle 2 along the x direction in a 6-body system under a 1/r$^{2}$ force law, is:

| $\ddot{x}_2 = \frac{0.426}{367y_4 - 1470} + \frac{2.88 \times 10^5 x_1}{2.08 \times 10^3 y_4 + 446y_4^2} - 5.98 \times 10^{-5} x_6 - 109x_1,$ |
|-----------------------------------------------------------------------------------------------------------------------------------------------|
|-----------------------------------------------------------------------------------------------------------------------------------------------|

where the indices refer to particle number. Despite *eureqa* converging, this equation is evidently meaningless and achieves a poor fit to the data. Thus, we argue that raw symbolic regression is intractable for the problems we consider, and only after factorization with a neural network do these problems become feasible for symbolic regression.

Discovering potentials using FlatHGN. Lastly, we also show an example of a successful reconstruction of a pairwise Hamiltonian from data. We treat the Hpair just as we would $^{φ}$ e 1 , and fit it to data. The one difference here is that there are potential Hpair values offset by a constant function of the non-dynamical parameters (fixed properties like mass) which still produce the correct dynamics, since only the derivatives of Hpair are used. Thus, we cannot simply fit a linear transformation of the true Hpair to data to verify it has learned our generating equation: we must rely on symbolic regression

![](_page_22_Figure_0.jpeg)

Figure 6: A plot of the data for the 1/r simulation in table 4, indicating mean absolute error versus complexity in the top plot and fractional drop in mean absolute error over the next-best model in the bottom plot. As indicated, we take the largest drop in log-loss over a single increase in complexity as the chosen model—it is our parametrization of Occam's Razor.

| Sim.     | Standard Bottleneck | L 1 KL |
|----------|---------------------|--------|
| Charge-2 | ✗ ✓                 | ✗ ✗    |
| Charge-3 | ✗ ✓                 | ✗ ✗    |
| − 1      |                     |        |
| -2       | ✗ ✓                 | ✓ ✓    |
| − 1      |                     |        |
| -3       | ✗ ✓                 | ✓ ✓    |
| − 2      |                     |        |
| -2       | ✗ ✓                 | ✓ ✗    |
| − 2      |                     |        |
| -3       | ✗ ✓                 | ✓ ✗    |
| Spring-2 | ✗ ✓                 | ✓ ✓    |
| Spring-3 | ✗ ✓                 | ✓ ✓    |

Table 5: Success/failure of a reconstruction of the force law by symbolic regression, corresponding to the values in table 1.

to extract the full functional form. We follow the same procedure as before, and successfully extract the potential for a charge simulation:

$$\mathcal{H}_{\text{pair}} \approx \frac{0.0019q_1q_2}{r} - 0.0112 - 0.00143q_1 - 0.00112q_1q_2,$$

where we expect Hpair ≈ $^{a}$ q1q$^{2}$ $^{r}$ + f(q1, q2, m1, m2), for constant a and arbitrary function f, which shows that the neural network has learned the correct form of the Hamiltonian.

Hyperparameters. Since the hyperparameters used internally by *eureqa* are opaque and not tunable, here we discuss the parameters used in *PySR* \[27\], which are common among many symbolic regression tools. At a given step of the training, there is a set of active equations in the "population". The number of active equations is a tunable hyperparameter, and is related to the diversity of the discovered equations, as well as the number of compute cores being used. The max size of equations controls the maximum complexity considered, and can be controlled to prevent the algorithm from wasting cycles on over-complicated equations. The operators used in the equations depends on the specific problem considered, and is another hyperparameter specified by the user. Next, there is a set of tunable probabilities associated with each mutation: how frequently to mutate an operator into a different operator, add an operator with arguments, replace an operator and its arguments with a constant, and so on. In some approaches such as with *PySR*, the best equations found over the course of training are randomly reintroduced back into the population. The frequency at which this occurs is controlled by another hyperparameter.

## D Video Demonstration and Code

We include a video demonstration of the central ideas of our paper at [https://github.com/](https://github.com/MilesCranmer/symbolic_deep_learning) [MilesCranmer/symbolic\\_deep\\_learning](https://github.com/MilesCranmer/symbolic_deep_learning). It shows the message components of a graph network converging to be equal to a linear combination of the force components when L$^{1}$ regularization is applied. Time in each clip of the video is correlated with training epoch. In this video, the top left corner of the fully revealed plot corresponds to a single test simulation that is 300 time steps long. Four particles of different masses are initiated with random positions and velocities, and evolved according to the potential of a spring with an equilibrium position of $^{1}$: ($^{r}$ − 1)$^{2}$ , where r is the distance between two particles. The evaluation trajectories are shown on the right, with the gray particles indicating the true locations. The 15 largest message components in terms of standard deviation over a test set are represented in a sorted list below the graph network in gray, where darker color corresponds to a larger standard deviation. Since we apply L$^{1}$ regularization to the messages, we expect this list to grow sparser over time, which it does. Of these messages, the two largest components are extracted, and each is fit to a separate linear combination of the true force components (bottom left). A better fit to the true force components — indicating that the messages represent the force — are indicated by dots (each dot is a single message) that lie closer along the y = x line in the bottom middle two scatter plots.

As can be seen in the video, as the messages grow increasingly sparse, the messages eventually converge to be almost exactly linear combinations of the true forces. Finally, once the loss is converged, we also fit symbolic regression to the largest message component. The video was created using the same training procedure as used in the rest of the paper. The dataset that the L$^{1}$ model was trained on is the 4-node Spring-2. Finally, we include the full code required to generate the animated clips in the above figure. This code contains all of the models and simulators used in the paper, along with the default training parameters. This code can also be accessed in the drive.

## E Cosmological Experiments

For the cosmological data graph network, we do a coarse hyperparameter tuning based on predictions of δ$^{i}$ and select a GN with 500 hidden units, two hidden layers per node function and message function. We choose 100 message dimensions as before. We keep other hyperparameters the same as before: L$^{1}$ regularization with a regularization scale of 10$^{−}$$^{2}$ .

Remarkably, the vector space discovered by this graph network is 1 dimensional. This is indicated by the fact that only one message component has standard deviation of about 10$^{−}$$^{2}$ and all other 99 components have a standard deviation of under 10$^{−}$$^{8}$ . This suggests that the δ$^{i}$ prediction is a sum over some function of the center halo and each neighboring halo. Thus, we can rewrite our model as a sum over a function φ e $^{1}$ which takes the central halo and each neighboring halo, and passes it to φ v which predicts δ$^{i}$ given the central halo properties.

Best-fit parameters. We list best-fit parameters for the discovered models in the paper in table 6. The functional forms were extracted from the GN by approximating both φ e 1 and φ $^{v}$ over training data with a symbolic regression and then analytically composing the expressions. Although the symbolic regression fits constants itself, this accumulates error from the two levels of approximation (graph net

| Test ˆ δ i = Old ˆ δ i = C 1 + ( C 2 Best, mass ˆ δ i = C 1 + New C Best, with mass ˆ δ i = C 1 + Test Best, mass | C + 2 C 2 C | 1 + C + 1 C | M i e i 3 e e i C 3 = 1 | C 3 i   v i M i − 0 = | ) e   − | i 0376 0 |   | e e i , C 199 | i = = C 1 2 , C | e i = = 2 | = P P 0 = | j j 0 | P 6 = i 6 = i 0529 1 | r j 6 = C C 415 31 N/A i − r i C 5 +( 5 +( , C , C | j   4 + C C C 3 3 | <   6   4 6   = = 20 v i r + r i | − i − M − 0 0 | M j v j r j   j r j 027   ) C 7   ) C , | D E   δ i − δ ˆ i   7 |
|-------------------------------------------------------------------------------------------------------------------|-------------|-------------|-------------------------|-----------------------|---------|----------|---|---------------|-----------------|-----------|-----------|-------|----------------------|----------------------------------------------------|-------------------|----------------------------------|---------------|-----------------------------------------|-----------------------|
| C 4                                                                                                               | =           | 1           | 54                      | , C                   | 5       | =        |   | 50            | 165             |           | , C       |       | 6                    | = 18                                               | 94                | , C                              | 7             | = 13                                    | 21                    |
| Best, with mass                                                                                                   |             | C           | 1 =                     | −                     | 0       | 156      |   | ,             | C 2             | =         |           | 3     | 80                   | , C 3                                              | =                 | 0                                | 0809          | ,                                       |                       |
| C                                                                                                                 | 4           | =           | 0                       | 438                   | ,       | C        | 5 | =             | 7               | 06        | ,         | C     | 6                    | = 15                                               | 5                 | , C                              | 7             | = 20                                    | 3                     |
| Best, with mass and cutoff ∗                                                                                      |             | C           | 1 =                     | −                     | 0       | 149      |   | ,             | C 2             | =         |           | 3     | 77                   | , C 3                                              | =                 | 0                                | 0789          | ,                                       |                       |
| C                                                                                                                 | 4           | =           | 0                       | 442                   | ,       | C        | 5 | =             | 7               | 09        | ,         | C     | 6                    | = 15                                               | 5                 | , C                              | 7             | = 21                                    | 3                     |

Table 6: Best-fit parameters for the functional forms used to estimate the overdensity of dark matter halos. The functional forms are given in the upper table for reference. $^{*}$Here we use the same formula as "Best, with mass," since we found an equivalent formula by only looking at the 80% chunk of the data. The constants in that functional form are also fit by only training on that fraction of the data.

to data, symbolic regression to graph net). Thus, we take out the functional forms as given in table 6, and refit the parameters directly to the training data. This results in the parameters given, which are used to calculate accuracy of the symbolic models.