# Information-theoretic formulation of dynamical systems: causality, modeling, and control

Adri´an Lozano-Dur´an and Gonzalo Arranz

Department of Aeronautics and Astronautics, Massachusetts Institute of Technology, Cambridge, MA 02139, USA (Dated: June 1, 2022)

The problems of causality, modeling, and control for chaotic, high-dimensional dynamical systems are formulated in the language of information theory. The central quantity of interest is the Shannon entropy, which measures the amount of information in the states of the system. Within this framework, causality is quantified by the information flux among the variables of interest in the dynamical system. Reduced-order modeling is posed as a problem related to the conservation of information in which models aim at preserving the maximum amount of relevant information from the original system. Similarly, control theory is cast in information-theoretic terms by envisioning the tandem sensor-actuator as a device reducing the unknown information of the state to be controlled. The new formulation is used to address three problems about the causality, modeling, and control of turbulence, which stands as a primary example of a chaotic, high-dimensional dynamical system. The applications include the causality of the energy transfer in the turbulent cascade, subgrid-scale modeling for large-eddy simulation, and flow control for drag reduction in wall-bounded turbulence.

# I. INTRODUCTION

Information theory is the science about the laws governing information or, in other words, the mathematics of message communication. A message can be thought of as the bits (ones and zeros) of an image transfer via the Internet, but also as the cascade of energy in a turbulent flow or the drag reduction in an airfoil when applying a particular control strategy. Information theory is one of the few scientific fields fortunate enough to have an identifiable beginning: Shannon \[1\], who ushered us into the Information Age with a quantitative theory of communication. Since then, a field that started as a branch of mathematics dealing with messages, ultimately matured into a much broader discipline applicable to engineering, biology, medical science, sociology, psychology. . . e.g., [2\]. The success of information theory relies on the notion of information as a fundamental property of physical systems, closely tied to the restrictions and possibilities of the laws of physics \[3\]. The fundamental nature of information provides the foundations for the principles of conservation of information and maximum entropy highly regarded within the physics community \[4–][6\]. Interestingly, despite the accomplishments of information theory in many scientific disciplines, applications to some branches of physics are remarkably limited. The goal of the present work is to advance our physical understanding of chaotic, high-dimensional dynamical systems by looking at the problems of causality, reduced-order modeling, and control through the lens of information theory.

The grounds for causality as information are rooted in the intimate connection between information flux and the arrow of time: the laws of physics are time-symmetric at the microscopic level, and it is only from the macroscopic viewpoint that time-asymmetries arise in the system \[7\]. Such asymmetries determine the direction of time, that can be leveraged to measure the causality of events using information-theoretic metrics based on the Shannon entropy. Modeling can be posed as a problem of conservation of information: reduced-order models contain a smaller number of degrees of freedom than the original system, which in turn entails a loss of information. Thus, the goal of a model is to guarantee as much as possible the conservation of relevant information from the original system. Similarly, control theory for dynamical systems can be cast in information-theoretic terms if we envision the tandem sensor-actuator as a device aimed at reducing the unknown information associated with the state of the system to be controlled. In all of the cases above, the underlying idea advanced is that the evolution of the information content in a chaotic system greatly aids the understanding and manipulation of the quantities of interest.

In the present work, i) a new definition of causality is proposed based on the information required to attain total knowledge of a variable in the future, ii) the conditions for maximum information-preserving models are derived and leveraged to prove that accurate models maximize the information shared between the model state and the true state, and iii) new definitions of open/closed-loop control, observability, controllability, and optimal control are introduced in terms of the information shared among the variable to control and/or the sensors and actuators. The informationtheoretic formulation of causality, reduced-order modeling and control is introduced in §IV, §V, and §VI, respectively. The sections are self-contained and follow a consistent notation. Each section provides a brief introduction of the topic and closes with the application of the theory to tackle a problem in turbulent flows. Nonetheless, the theory is broadly applicable to any chaotic dynamical system. Given our emphasis on turbulent flows, we provide next a summary of current approaches for turbulence research. The reader interested in the formulation of the theory is directly referred to §II.

# A. Abridged summary of modeling, control, and causality in turbulence research

Turbulence, i.e., the multiscale motion of fluids, stands as a primary example of a chaotic, high-dimensional phenomenon. Broadly speaking, efforts in turbulence research can be subdivided into physical insight, modeling, and control. The three branches are intimately intertwined, yet they provide a conceptual partition of the field which is useful in terms of goals and methods. Even a brief survey of the methods for modeling, control, and causality would entail a monumental task that will not be attempted here. Instead, common pathways to tackle these problems are discussed along with the some pitfalls and limitations.

In the context of modeling, the field of fluid mechanics is in the enviable position of owning a set of equations that describes the motion of a fluid to near-perfect accuracy: the Navier-Stokes equations. Thus, significant ongoing efforts are devoted to capturing the essential flow physics in the form of reduced-order models. Prominent techniques include proper orthogonal decomposition and Galerkin projection \[8\], balanced truncation and dynamic mode decomposition \[9\], or extensions by Koopman theory \[10\]. Machine learning also provides a modular and agile framework that can be tailored to address reduced-order modeling \[11,] [12\]. Linear theories are still instrumental for devising reduced-order models, while other approaches rely on phenomenological arguments. The modeling application of this work is centered on large-eddy simulation (LES), in which the large eddies in the flow are resolved and the effect of the small scales is modeled through a subgrid-scale model (SGS). Most SGS models are derived from a combination of theory and physical intuition. \[13–][15\]. In addition, Galilean invariance, along with the principles of mass, momentum, and energy conservation, are invoked to constrain the admissible models e.g., [16,] [17\]. However, although we do possess a crude practical understanding of turbulence, flow predictions from the state-of-the-art models are still unable to comply with the stringent accuracy requirements and computational efficiency demanded by the industry \[18\].

Control, the ability to alter flows to achieve the desired outcome, is a matter of tremendous consequence in engineering. In system control, sensors measure the state of the flow, while actuators create the flow disturbances to prevent or trigger a targeted condition (e.g., drag reduction, mixing enhancement, etc.). Recent decades have seen a flourishing of activity in various techniques for control of turbulent flows –active, passive, open-loop, closed-loop \[12,] [19–][23\]. A common family of methods originates from linear theories, which constitutes the foundation of many control strategies \[10,] [24][–28\]. However, linear methods have sparked criticism as turbulence is a highly nonlinear phenomenon, and universal control strategies cannot be anticipated from a single set of linearized equations. Nonlinear control strategies are less common, but they have also been available for years e.g., [29–][31\]. They are, nonetheless, accompanied by a considerable penalty in the computational cost, which renders nonlinear control impractical in many real-world applications.

Causality is the mechanism by which one event contributes to the genesis of another \[32\]. Whereas control and modeling are well-established cornerstones of turbulence research, the same cannot be said about the elusive concept of causality, which has been overlooked within the fluids community except for a handful of works \[33–][36\]. In the case of turbulence research, causal inference is usually simplified in terms of the cross-time correlation between pairs of time signals representing the events of interest (e.g., kinetic energy, dissipation, etc.). The correlation method dates back to the work of the mathematician A.-M. Legendre in the 1800s, and undoubtedly constitutes an outdated legacy tool. Efforts to infer causality using time-correlation include the investigations of the turbulent kinetic energy \[37,] [38\] and the space-time signature of spectral quantities e.g., [39–][44\], to name a few. However, it is universally accepted that correlation does not imply causation \[45\], as the former lacks the directionality and asymmetry required to quantify causal interactions. Despite this limitation, the correlation between time signals stands as the state-of-the-art tool for (non-intrusive) causality quantification in fluid mechanics.

The goal of the present work is to further advance the field of turbulence research by introducing a new informationtheoretic formalism for causality, modeling, and control. To date, the use of information-theoretic tools in the fluid mechanics community is still in its infancy. Betchov \[46\] was one of first authors to propose an information-theoretic metrics to quantify the intricacy of turbulence. Cerbus and Goldburg \[47\] applied the concept of conditional Shannon entropy to analyze the energy cascade in 2-D turbulence. The work by Cerbus \[48\] also contains additional discussions on the use of established tools in information theory for fluid dynamics. Materassi et al. \[49\] used normalized transfer entropy to study the cascading process in synthetic turbulence generated via the shell model. In a series of works, Granero-Belinch´on et al. \[50\], Granero-Belinch´on et al. \[51\], Granero-Belinchon \[52\], Granero-Belinch´on et al. \[53\] investigated the information content, intermittency, and stationarity characteristics of isotropic turbulence using information-theoretic tools applied to experimental velocity signals. Liang and Lozano-Dur´an \[34\] and Lozano-Dur´an et al. \[35\] applied information-theoretic definitions of causality to unveil the dynamics of energy-containing eddies in wall-bounded turbulence. A similar approach was followed by Wang et al. \[54\] to study cause-and-effect interactions in turbulent flows over porous media. Lozano-Dur´an et al. \[35\] also discussed the use of information transfer among variables to inform the design of reduced-order models. Shavit and Falkovich \[55\] used singular measures and information capacity to study the turbulent cascade and explore the connection between information and modeling. More recently, Lee \[56\] leveraged the principle of maximum-entropy to analyze the turbulence energy

spectra. The aforementioned studies have offered a new perspective of turbulence using established tools in information theory. In the following, we further develop the theory of information for dynamical systems with the aim of advancing the field of turbulence research.

#### II. BASICS OF INFORMATION THEORY

Let us introduce the concepts of information theory required to formulate the problems of causality, modeling, and control. The first question that must be addressed is the meaning of information, as it departs from the intuitive definition used in our everyday life. Let us consider the discrete random variable X taking values equal to x with probability mass function p(x) = Pr{X = x} over the finite set of outcomes of X. The information of observing the event X = x is defined as \[1\]:

$$ \mathcal{I}(x) = -\log_2[p(x)]. \quad (1) $$

The units of I(x) are set by the base chosen, in this case 'bits' for base 2. The base of the logarithm is arbitrary and can be changed using the identity log$^{a}$ p = log$^{a}$ b log$^{b}$ p. For example, consider tossing a fair coin with X ∈ {heads,tails} such that p(heads) = p(tails) = 0.5. The information of getting heads after flipping the coin once is I(heads) = − log$^{2}$ (0.5) = 1 bit, i.e., observing the outcome of flipping a fair coin provides one bit of information. If the coin is completely biased towards heads, p(heads) = 1, then I(heads) = − log$^{2}$ (1) = 0 bits (where 0 log 0 = 0), i.e., no information is gained as the outcome was already known before flipping the coin. This simple but revealing example illustrates the meaning of information in the present work: information is the statistical notion of how unlikely it is to observe an event. Low probability events provide more information than high probability events. Thus, within the framework of information theory, the statement "tomorrow the sun will rise in the west" contains more information than "tomorrow the sun will rise in the east", simply because the former is extremely unlikely. The information can also be interpreted in terms of uncertainty: I(x) is the number of bits required to unambiguously determine the state x. The latter interpretation will be frequently evoked in this work.

The reader might ask why not choosing information to be directly proportional to p(x) rather than to − log$^{2}$ [p(x)]. However, the logarithm function is the most natural choice for a measure of information that is additive in the number of states of the system considered. This might be illustrated by tossing a fair coin n times. The information gathered for a particular sequence of events is

$$ \mathcal{I}(\text{heads, heads, tails, } \dots) = -\log_2(0.5^n) = n \text{ bits.} \quad (2) $$

In general, when two systems with N different states are combined, the resulting system contains N$^{2}$ states (i.e., Cartesian product of the states of both systems), but the amount of information is 2N \[57\] as illustrated in the example above. Another viewpoint of Eq. (2) is that the probability of observing a sequence of events is a multiplicative process given by p(x1)p(x2)...p(x$^{N}$ ), whereas it would be preferable to work with an additive process. The latter is attained by taking the logarithms of the probabilities, − log$^{2}$ [p(x1)] − log$^{2}$ [p(x2)] − ... − log$^{2}$ [p(x$^{N}$ )], where the minus sign is introduced for convenience to obtain an outcome that is equal or larger than zero.

Equations (1) and (2) provide the information gained observing one particular event or a sequence of events, respectively. Usually, we are interested in the average information in X given by the expectation $\langle \cdot \rangle$ over all the possible outcomes

---

$$H(X) = \langle \mathcal{I}(x) \rangle = \sum_x -p(x) \log_2[p(x)] \geq 0, \tag{3}$$

which is referred to as the Shannon entropy and represents the generalization to arbitrary variables of the well-known thermodynamic entropy \[58,] [59\]. Following the example above, the entropy of the system "flipping a fair coin n times" is H = − P0.5 $^{n}$ log$^{2}$ (0.5 $^{n}$) = n bits, where the sum is performed over all the possible outcomes of flipping a coin n times (namely, 2$^{n}$). As expected, flipping n times a biased coin with p(heads) = 1 provides no information (H = 0). Shannon \[1\] showed that Eq. (3) corresponds to the minimum average number of bits needed to encode a source of n states with probability distribution p. As measure of uncertainty, H is maximum when all the possible outcomes are equiprobable (large uncertainty in the state of the system) and zero when the process is completely deterministic (no uncertainty in the outcome).

The Shannon entropy can be generalized to m random variables X = [X1, X2, ..., Xm] as

$$H(\mathbf{X}) = \langle \mathcal{I}(\mathbf{x}) \rangle = \sum_{x_1, \dots, x_m} -p(x_1, x_2, \dots, x_m) \log_2[p(x_1, x_2, \dots, x_m)] \quad (4a)$$

$^{H}$(X|$^{Y}$ ) $^{I}$(X; $^{Y}$ ) $^{H}$($^{Y}$ |X)

H(X) H(Y )

(a)

H(X, Y )

(b)

FIG. 1: Venn diagrams of (a) the conditional entropy and mutual information between two random variables X and Y , and (b) total entropy in two random variables.

where p(x1, x2, ..., xm) is the joint probability mass function Pr{X$^{1}$ = x1, X$^{2}$ = x2, ..., X$^{m}$ = xm}. Similarly, given the random variables $^{X}$ and $^{Y}$ and the conditional distribution $^{p}$(x|y) = $^{p}$(x, y)/p(y) with $^{p}$(y) = P x p(x, y) as the marginal probability distribution of Y , the entropy of X conditioned on Y is defined as \[60\]

---

$$H(X|Y) = \sum_{x,y} -p(x,y) \log_2[p(x|y)]. \tag{5}$$

It is useful to interpret H(X|Y ) as the uncertainty in the state X after conducting the 'measurement' of the state Y . This interpretation is alluded to in the following sections. If X and Y are independent random variables, then H(X|Y ) = H(X), i.e., knowing the state Y does not reduce the uncertainty in X. Conversely, H(X|Y ) = 0 if knowing Y implies that X is completed determined. Finally, the mutual information between the random variables X and Y is

$$I(X;Y) = H(X) - H(X|Y) = H(Y) - H(Y|X), \quad (6)$$

which is a symmetric metric I(X; Y ) = I(Y ; X) representing the information shared among the state variables X and Y . The mutual information between variables will be also central to the formalism presented below. Figure 1 depicts the relationship between the entropy, conditional entropy, and mutual information.

The concepts above provide the foundations to the information-theoretic formulation of causality, modeling, and control detailed in the following sections. First, we introduce the formalism of information in dynamical systems. Several studies have already discussed this topic, mostly in the context of predictability and chaos e.g. [61–][65\]. The exposition here is extended and tailored to our particular interests.

## III. INFORMATION IN DYNAMICAL SYSTEMS

Let us consider the continuous deterministic dynamical system with state variable q = q(x, t), where x is the vector of spatial coordinates, and t is time. The dynamics of q are governed by the partial differential equation

$$\frac{\partial \mathbf{q}}{\partial t} = \mathbf{F}(\mathbf{q}), \quad (7)$$

that might represent, for example, the equations of conservation of mass, momentum, and energy. Equation (7) can be integrated in time from t$^{n}$ to tn+1 to yield

---

$$\mathbf{q}(\mathbf{x}, t_{n+1}) = \mathbf{q}(\mathbf{x}, t_n) + \int_{t_n}^{t_{n+1}} F(\mathbf{q}) \mathrm{d}t, \quad (8)$$

where tn+1 − t$^{n}$ is an arbitrary time span. We consider a spatially coarse-grained version of q at time t$^{n}$ denoted by q $^{n}$ = [q n 1 , ...., q$^{n}$ $^{N}$ ], where N is the number of degrees of freedom of the system. We assume that the dimensionality of q $^{n}$ is large enough to capture all the relevant dynamics of Eq. (8). In the context of fluid dynamics q $^{n}$ might represent, for example, the three velocities components and pressure at discrete spatial locations, the Fourier coefficients of the velocity, the coefficients from the Karhunen-Lo`eve decomposition of the flow \[8\], or in general, any spatially-finite representation of the continuous system.

We treat q $^{n}$ as a random variable, indicated by Q $^{n}$ = [Q$^{n}$ 1 , . . . , Q$^{n}$ $^{N}$ ], and consider a finite partition of the phase space D = {D1, D2, . . . , DN$^{q}$ }, where N$^{q}$ is the number of partitions, such that D = ∪ N$^{q}$ $^{i}$=1D$^{i}$ and D$^{i}$ ∩ D$^{j}$ = ∅ for all i 6= j. The system is said to be in the state D$^{i}$ if q $^{n}$ ∈ D$^{i}$ . The probability of finding the system at state D$^{i}$ at time t$^{n}$ is p q $^{i}$ = Pr{Q $^{n}$ ∈ $^{D}$i}. For simplicity, we refer to the latter probability simply as $^{p}$($^{q}$ $^{n}$). The dynamics of Q n , are determined by

$$Q^{n+1} = f(Q^n), \quad (9)$$

where the map f is derived from Eq. (8). Note that the system considered in Eq. (9) is closed in the sense that no external stochastic forcing is applied.

The information contained in the system at time t$^{n}$ is given by the entropy of Q n , namely, H(Q n ). As the system evolves in time according to Eq. (9), its information content is bounded by

$$H(\mathbf{Q}^{n+1}) = H(\mathbf{f}(\mathbf{Q}^n)) \leq H(\mathbf{Q}^n), \quad (10)$$

which is the result of the entropy of transformed random variables \[2\]. A consequence of Eq. (10) is that the dynamical system in Eq. (9) either conserves or destroys information, but never creates information. Another interpretation of Eq. (10) is that, for deterministic systems, the information of future states is completely determined by the initial condition, whereas the converse is not always true. For example, dissipative systems cannot be integrated backwards in time to univocally recover its initial state.

The entropy of the system at t$^{n}$ can be related to the entropy at tn+1 through the Perron-Frobenious operator $^{P}$[·] \[66\] which advances the probability distribution of the system

$$p(\mathbf{q}^{n+1}) = \mathbb{P}[p(\mathbf{q}^n)]. \quad (11)$$

By construction of the system in Eq. (9), we can derive the zero conditional-entropy condition

$$H(Q^{n+1}|Q^n) = \sum -p(q^{n+1}, q^n) \log[p(q^{n+1}|q^n)] = (12a)$$

$$= \sum -\mathbb{P}[p(q^n|q^n)|p(q^n) \log\{\mathbb{P}[p(q^n|q^n)]\}] = 0, \quad (12b)$$

$$= \sum -\mathbb{P}[p(q^n|q^n)p(q^n) \log\{\mathbb{P}[p(q^n|q^n)]\}] = 0, \quad (12b)$$

which shows that there is no uncertainty in the future state Q $^{n}$+1 given the past state Q n . Equation (12) merely echoes the deterministic nature of the governing equations, and will be instrumental in the formulation of the principles for causality, modeling, and control. Additionally, if the map f is reversible, namely, Q $^{n}$ = f −1 (Q $^{n}$+1), then we obtain the conservation of information for dynamical systems

$$H(Q^{n+1}) = H(Q^n), \quad (13)$$

which can be regarded as a fundamental principle underlying the rest of conservation laws.

The condition in Eq. (12) may be generalized by adding the noise, W$^{n}$ , which accounts for uncertainties in the system state Q n , numerical errors, unknown physics in the map f, etc. The new governing equation is then Q $^{n}$+1 = f(Q n ,W$^{n}$ ) which implies that H(Q $^{n}$+1|Q n ) ≥ 0 (information can be created) unless the effect of noise is taken into consideration, i.e. H(Q $^{n}$+1|Q n ,W$^{n}$ ) = 0. A consequence of the latter is that for long integration times in chaotic systems, a small amount of noise will also result in H(Q $^{n}$+1|Q n ) ≥ 0. Hereafter, we center our attention on fully deterministic systems and assume that the impact of the noise on Q $^{n}$+1 is negligible (W$^{n}$ = 0) for the problems of causality and modeling. The effect of the noise will be introduced in the formulation of control.

# IV. INFORMATION FLUX AS CAUSALITY

One of the most intuitive definitions of causality relies on the concept of interventions: manipulation of the causing variable leads to changes in the effect \[32,] [67\]. Interventions provide a pathway to evaluate the causal effect that a process $^{A}$ exerts on another process $^{B}$ by setting $^{A}$ to a modified value $^{A}$e and observing the post-intervention consequences on B. Despite the intuitiveness of interventions as a measure of causality, the approach is not free of shortcomings. Causality with interventions is intrusive (i.e., it requires modification of the system) and costly (the simulations need to be recomputed if numerical experiments are used). When the data are collected from physical experiments, the causality with interventions might be even more challenging or directly impossible to practice (for instance, we cannot use interventions to assess the causality of the prices in the stock market in 2008). Causality with interventions also poses the question of what type of intervention must be introduced in A and whether that would affect the outcome of the exercise as a consequence of forcing the system out of its natural attractor. The framework of information theory provides an alternative, non-intrusive definition of causality as the information transferred from the variable A to the variable B. The idea can be traced back to the work of Wiener \[68\] and was first quantified by Granger \[69\] using signal forecasting via linear autoregressive models. In the context of information theory, the definition was formalized by Massey \[70\] and Kramer \[71\] through the use of conditional entropies with the so-called directed information. Schreiber \[72\] introduced an heuristic definition of causality inspired by the direction of information in Markov chains. Liang and Kleeman \[73\] and later Sinha and Vaidya \[74\] proposed to infer causality by measuring the information changes in the disturbed dynamical system. The new formulation of causality proposed here is motivated by the information required to attain total knowledge of a future state. Similar to previous works, the definition relies on conditional entropies. However, our information-theoretic quantification of causality is directly grounded on the zero conditional-entropy condition for deterministic systems (i.e., Eq. 12) and generalizes previous definitions of causality to multivariate systems. We also introduce the concept of information leak as the amount of information unaccounted for by the observable variables.

#### A. Formulation

# 1. Information flux

The goal of this section is to leverage the information flux from present states of the system to future states as a proxy for causal inference. Without loss of generality, let us derive the information transferred from Q n to Q n+1 j . The dynamics of Q n+1 j is governed by the j-th component of Eq. (9),

$$Q_j^{n+1} = f_j(Q^n). \quad (14)$$

From Eq. (14) and the propagation of information in deterministic systems (Eq. (12)), it follows that

$$H(Q_j^{n+1}|\mathbf{Q}^n) = 0, \quad (15)$$

which shows that all the information contained in Q n+1 j originates from Q n . Let us define the subset of variables Q n ¯$^{ı}$ = [Q n ¯ı1 , ..., Q n ¯ı$^{M}$ ], where ¯ı = [¯ı1, ...,¯ıM] is a vector of indices with M ≤ N, and the vector of remaining variables Q n ✄ ¯ı , such that Q $^{n}$ = [Q n ✄ ¯ı , Q n ¯ı ]. If only the information from Q n ✄ ¯ı is accessible, then the uncertainty in the future state Q n+1 j can be non-zero,

$$H(Q_j^{n+1}|\mathbf{Q}_t^n) \geq 0. \quad (16)$$

Equation (16) quantifies the average number of bits required to completely determined the state of Q n+1 $^{j}$ when Q n ¯ı is unknown, or in other words, the information in Q n ¯ı contributing to the dynamics of Q n+1 j . The interpretation of Eq. (16) as the information flux from Q n ¯ı to Q n+1 $^{j}$ motivates our definition of causality. The information-theoretic causality from Q n ¯ı to Q n+1 j , denoted by $^{T}$¯ı→$^{j}$ , is defined as the information flux from $^{Q}$ n ¯ı to Q n+1 j ,

$$T_{\bar{\mathbf{z}} \rightarrow j} = \sum_{k=0}^{M-1} \sum_{\bar{\mathbf{z}}(k) \in \mathcal{C}_k} (-1)^k H(Q_j^{n+1} | \mathbf{Q}_{\frac{1}{k}(k)}^n), \quad (17)$$

where ¯ı(k) is equal to ¯ı removing k-components and C$^{k}$ is the group of all the combinations of ¯ı(k). Equation (17) represents how much the past information in Q n ¯ı improves our knowledge of the future state Q n+1 j , which is consistent with the intuition of causality \[68\]. Note that the information flux from $^{T}$¯ı→$^{j}$ does not overlap with the information flux from T¯$^{ı}$ $^{0}$→$^{j}$ for ¯$^{ı}$ different from ¯$^{ı}$ 0 even if ¯ı ∩ ¯ı $^{0}$ $^{6}$$^{=}$ $^{∅}$. For example, the information flux from $^{T}$[1,2]→$^{j}$ does not overlap with $^{T}$1→$^{j}$ . This implies that $^{T}$¯ı→$^{j}$ only accounts for the information flux exclusively due to the joint effect of all the variables in Q n ¯ı . Figure 2a illustrates the Venn diagram of entropies and information fluxes for a system with three variables. The information flux can be cast in compact form using the generalized conditional mutual information,

$$\mathbf{z}_{i \rightarrow j} = I(Q_j^{n+1}; Q_{i1}^n; Q_{i2}^n; \dots; Q_{iM}^n | \mathbf{Q}_f^n), \quad (18)$$

where I(·; ·; ·; ...|·) is the conditional co-information \[75,] [76\] recursively defined by

$$(Q_j^{n+1}; Q_{i1}^n; \dots; Q_{iM-1}^n; Q_{iM}^n | Q_j^n) = (19a)$$

$$(Q_j^{n+1}; Q_{i_1}^n; \dots; Q_{i_{M-1}}^n | \mathbf{Q}_j^n) - I(Q_j^{n+1}; Q_{i_1}^n; \dots; Q_{i_{M-1}}^n | [Q_{i_M}^n | \mathbf{Q}_j^n]). \quad (19b)$$

![](_page_6_Picture_1.jpeg)

FIG. 2: (a) Schematic of the entropies at time t$^{n}$ for a system with three variables [Q$^{n}$ 1 , Q$^{n}$ 2 , Q$^{n}$ 3 ] and their relation to the entropy of the future variable Q n+1 2 . Note that the entropy of Q n+1 $^{2}$ must be contained within the entropy of H(Q$^{n}$ 1 , Q$^{n}$ 2 , Q$^{n}$ 3 ) for consistency with Eq. (15). (b) Similar to (a), but for a system of observables states (Eq. (22)). In this case, the entropy of Y n+1 2 in not contained within H(Y n 1 , Y $^{n}$ 2 , Y $^{n}$ 3 ), leading to T Y leak,j = H(Y n+1 2 |Y n 1 , Y $^{n}$ 2 , Y $^{n}$ 3 ) > 0.

The recursion in Eq. (19) is repeated until obtaining the pairwise definition of conditional mutual information I(X; Y |Z) = H(X|Z) − H(X|[Y, Z]).

By construction of Eq. (17), it is satisfied that the amount of information in the state Q n+1 j is equal to the sum of all the information fluxes from Q n ¯$^{ı}$ and Q$^{n}$ ✄ ¯ı to Q n+1 j ,

$$H(Q_j^{n+1}) = \sum_{\vec{v}' \in \mathcal{C}} T_{\vec{v}' \rightarrow j}, \quad (20)$$

where C is the group of all combinations of vectors ¯ı 0 of length 1 to N with components taken from ¯ı ∪ ¯✄ ı. Another important property of the information flux is that $^{T}$¯ı→$^{j}$ = 0 if the dynamics of $^{Q}$ n+1 j does not depend explicitly on the states Q n ¯ı , namely,

$$Q_j^{n+1} = f_j(Q_j^n) \Rightarrow T_{\overline{t}_{i \rightarrow j}} = 0. \quad (21)$$

The zero-information-flux condition above is again consistent with the intuition that no direct causality should emerge from Q n ¯ı to Q n+1 j unless the latter depends on the former. Additionally, the information flux is based on probability distributions and, as such, is invariant under shifting, rescaling and, in general, nonlinear C 1 -diffeomorphism transformations of the signals \[77\]. One more attractive feature of the information flux is that $^{T}$¯ı→$^{j}$ accounts for direct causality excluding intermediate variables. For example, if the causality flow is Q$^{i}$ → Q$^{j}$ → Q$^{k}$ , then there is no causality from Q$^{i}$ to Q$^{k}$ (i.e., $^{T}$i→$^{k}$ = 0) provided that the three components $^{Q}$$^{i}$ , Q$^{j}$ , and Q$^{k}$ are contained in Q.

The definition from Eq. (17) is trivially generalized to quantify the information flux from Q n ¯ı to a set of variables with indices ¯ = [¯1,¯2, ...] by replacing Q n+1 j by Q n+1 ¯ . It can be shown that given two arbitrary sets of variables with index vectors ¯$^{ı}$ and ¯, in general, it is satisfied that $^{T}$¯ı→¯ $^{6}$$^{=}$ $^{T}$¯→¯ı, and thus the information flux is asymmetric.

# 2. Information flux of observable states

In many occasions, we are interested in, or only have accessed to, an observable state

$$Y^n = h(Q^n), \quad (22)$$

$$H(\mathbf{Y}^n) = H(\mathbf{h}(\mathbf{Q}^n)) \leq H(\mathbf{Q}^n), \quad (23)$$

such that complete knowledge of Y n does not necessarily imply that the future state Y $^{n}$+1 is known. This is revealed by the inequality H(Y $^{n}$+1|Y n ) ≥ H(Y $^{n}$+1|Q n ) = 0, that particularized for the j-component of Y n results in

$$H(Y_j^{n+1}|\mathbf{Y}^n) \geq 0. \quad (24)$$

In light of Eq. (24), the definition of information flux from Eq. (17) should be modified to account for the lack of knowledge from unobserved states. The information flux from an observable state Y n ¯ı to a future observable state Y n+1 j is defined as

$$T_{\bar{\mathbf{z}} \rightarrow j}^Y = \left[ \sum_{k=0}^{M-1} \sum_{\bar{\mathbf{z}}(k) \in \mathcal{P}_k} (-1)^k H(Y_j^{n+1} | \mathbf{Y}_{\frac{1}{k}(k)}^n) \right] + (-1)^M H(Y_j^{n+1} | \mathbf{Y}^n), \quad (25)$$

where ¯ı is again a vector of indices, ¯ı = [¯ı1, ...,¯ıM], now with M ≤ N$^{Y}$ . The term H(Y n+1 j |Y n ) in Eq. (25) quantifies the information loss from unobserved states and is naturally absorbed into the summation as

$$T_{\bar{\mathbf{z}} \rightarrow j}^Y = \sum_{k=0}^M \sum_{\bar{\mathbf{z}}(k) \in \mathcal{P}_k} (-1)^k H(Y_j^{n+1} | \mathbf{Y}_{\frac{1}{k}(k)}^n). \quad (26)$$

The definition above can be written in compact form using again the conditional co-information as

$$Y_{i \rightarrow j}^T = I(Y_j^{n+1}; Y_{i1}^n; Y_{i2}^n; \dots; Y_{iM}^n | \mathbf{Y}_j^n). \quad (27)$$

When Y $^{n}$ = Q n , then H(Y n+1 j |Y n ) = 0 and Eq. (17) is recovered. Moreover, for ¯ı = [i], the information flux for observable states is

$$T_{i \rightarrow j} = H(Y_j^{n+1}|Y_j^n) - H(Y_j^{n+1}|Y^n), \quad (28)$$

that is the multivariate generalization of the transfer entropy proposed by Schreiber \[72\]. Another difference from Schreiber \[72\] is that the new definition of causality accounts for the information flux due to the joint effect of variables when ¯ı has more than one component. We will show in the example below that the joint information flux might be of the same order as the information flux from individual variables.

We have shown in Eq. (20) that the total information in a future state is determined by the sum of all information fluxes. However, limiting the knowledge of the system to a reduced set of observable variables Y n entails a leak of information towards future state Y n+1 j such that now

$$H(Y_j^{n+1}) = \sum_{\bar{v} \in \mathcal{P}} T_{\bar{v} \rightarrow j}^Y + T_{\text{leak},j}^Y, \quad (29)$$

where T Y leak,j is the information leak or amount of information in Y n+1 j that cannot be explained by Y n j , and it is given by

$$T_{\text{leak},j}^Y = H(Y_j^{n+1} | Y^n). \quad (30)$$

The information flux in Eq. (17) and Eq. (26) has units of bits. It is then natural to introduce the normalized information flux as

$$TN_{i \rightarrow j}^Y = \frac{T_{i \rightarrow j}^Y}{H(Y_{n+1}^j)}, \quad (31a)$$

$$TN_{\text{leak},j}^Y = \frac{T_{\text{leak},j}^Y}{H(Y_{n+1}^j)}, \quad (31b)$$

which satisfies

$$\sum_{\bar{\mathbf{z}} \in \mathcal{P}} TN_{\bar{\mathbf{z}} \rightarrow j}^Y + TN_{\text{leak},j}^Y = 1. \quad (32)$$

A similar normalization was proposed by Materassi et al. \[49\] in the context of delayed mutual information. Other normalizations are discussed in Duan et al. \[78\].

As an example, we elaborate on the information flux formulas for Y n+1 2 in a system with three observable variables (N$^{Y}$ = 3), as depicted in Fig. 2b. For ¯ı = [1] and j = 2, we get

$$T_{1\rightarrow 2} = H(Y_2^{n+1}|Y_2^n, Y_3^n) - H(Y_2^{n+1}|Y_1^n, Y_2^n, Y_3^n), \quad (33)$$

for ¯ı = [1, 3] and j = 2,

$$T_{[1,3] \rightarrow 2}^Y = H(Y_2^{n+1}|Y_2^n) - H(Y_2^{n+1}|Y_1^n, Y_2^n) - H(Y_2^{n+1}|Y_2^n, Y_3^n) + \\ + H(Y_2^{n+1}|Y_1^n, Y_2^n, Y_3^n), \quad (34)$$

and for ¯ı = [1, 2, 3] and j = 2, we have

$$\begin{aligned} T_{[1,2,3] \rightarrow 2}^Y &= H(Y_2^{n+1}) - \\ &- H(Y_2^{n+1}|Y_1^n) - H(Y_2^{n+1}|Y_2^n) - H(Y_2^{n+1}|Y_3^n) + \\ &+ H(Y_2^{n+1}|Y_1^n, Y_2^n) + H(Y_2^{n+1}|Y_1^n, Y_3^n) + H(Y_2^{n+1}|Y_2^n, Y_3^n) - \\ &- H(Y_2^{n+1}|Y_1^n, Y_2^n, Y_3^n). \end{aligned} \tag{35}$$

In the three examples above, T Y $^{1}$→$^{2}$ , T Y [1,3]→$^{2}$ and T Y [1,2,3]→$^{2}$ contain non-overlapping information similar to the sketch shown in figure 2a. The total information in Y n+1 2 is given by

| $H(Y_2^{n+1}) = T_{1 \rightarrow 2}^Y + T_{2 \rightarrow 2}^Y + T_{3 \rightarrow 2}^Y +$ $T_{[1,2] \rightarrow 2}^Y + T_{[1,3] \rightarrow 2}^Y + T_{[2,3] \rightarrow 2}^Y + T_{[1,2,3] \rightarrow 2}^Y + T_{\text{leak},j}^Y, \quad (36)$ |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

where T Y leak,j = H(Y n+1 2 |Y n 1 , Y $^{n}$ 2 , Y $^{n}$ 3 ).

We close this section by noting that T Y ¯ı→$^{j}$ (similarly for $^{T}$¯ı→$^{j}$ ) is not constrained to be larger or equal to zero when the number of variables considered is odd. This might not be obvious from figure 2b, as conditional entropies do not obey the conservation of areas depicted by the Venn diagram shown in the plot. However, the possibility of negative values of the co-information is a known property often discussed in the literature see, for instance, [76\]. In general, negative information flux will occur when there is backpropagation of information from the future to the past, i.e, the knowledge of an event in the future would provide information about an event in the past, but not the other way around. The reader is referred to James et al. \[79\] for a deeper discussion on the topic.

#### 3. Optimal observable states and phase-space partition for information flux

The analysis of information fluxes is considerably simplified when the mutual information between pairs of components in Y n is zero,

$$I(Y_i^n; Y_j^n) = 0, i \neq j. \quad (37)$$

In that case, we can focus on the information flux from one single variable to the future state as shown in Eq. (28). Given an observable state Y n , we define the optimal observable representation for information flux as Y $^{n}$∗ = $^{w}$∗ (Y n ), where w∗ is the reversible transformation satisfying

$$\mathbf{w}^* = \arg \min_{\mathbf{w}(\mathbf{Y}^n)} \left( \sum_{i,j, i \neq j} I(Y_i^n, Y_j^n) \right), \text{ s.t. } H(\mathbf{Y}^{n*}) = H(\mathbf{Y}^n). \quad (38)$$

The new observable state Y n∗ has the advantage of minimizing the causal links due to the joint effect of two or more variables acting together, which might ease the identification of key physical processes and facilitate the reduced-order modeling of the system. A similar argument can be applied to the phase-space partition D = {D1, D2, ..., DN$^{q}$ } to define the optimal D∗ for causal inference as

$$D^* = \arg \min_D \left( \sum_{i,j, i \neq j} I(Q_i^n; Q_j^n) \right) \text{ s.t. } D_i \cap D_j = \emptyset \quad \forall i \neq j. \quad (39)$$

![](_page_9_Diagram_1.jpeg)

FIG. 3: Schematic of the Richardson's turbulent energy cascade \[80\] in which energy is transferred sequentially between eddies of decreasing size. The kinetic energy flows from the largest flow motions, characterized by the integral length-scale Lε, to the Kolmogorov length-scale η, where it is finally dissipated.

# B. Application: Causality of the energy cascade in isotropic turbulence

The cascade of energy in turbulent flows, i.e., the transfer of kinetic energy from large to small flow scales or vice versa (backward cascade), is the cornerstone of most theories and models of turbulence since the 1940s \[80–][86\]. Yet, understanding the dynamics of the kinetic energy transfer across scales remains an outstanding challenge in fluid mechanics. Given the ubiquity of turbulence, a deeper understanding of the energy transfer among the flow scales would enable significant progress across various fields ranging from combustion \[87\], meteorology \[88\], and astrophysics \[89\] to engineering applications of aero/hydro-dynamics \[90–][94\]. In spite of the substantial advances in the last decades, the causal interactions of energy among scales in the turbulent cascade remain uncharted. Here, we use the formalism introduced in §IV A to investigate the information flux of the turbulent kinetic energy across different scales. Our goal is to assess the local-in-scale cascade in which the kinetic energy is transferred sequentially from one scale to the next smaller scale as sketched in figure 3.

The case selected to study the energy cascade is isotropic turbulence in a triply periodic box with side L. The data were obtained from the DNS of Cardesa et al. \[38\], which is publicly available in Torroja \[95\]. The conservation of mass and momentum equations of an incompressible fluid are given by

$$\frac{\partial u_i}{\partial t} + \frac{\partial u_i u_j}{\partial x_j} = -\frac{1}{\rho} \frac{\partial \Pi}{\partial x_i} + \nu \frac{\partial^2 u_i}{\partial x_j \partial x_j} + f_i, \quad \frac{\partial u_i}{\partial x_i} = 0, \quad (40)$$

where repeated indices imply summation, x = [x1, x2, x3] are the spatial coordinates, u$^{i}$ for i = 1, 2, 3 are the velocities components, Π is the pressure, ρ is the flow density, ν is the kinematic viscosity, and f$^{i}$ is a linear forcing sustaining the turbulent flow \[96\]. The flow setup is characterized by one nondimensional parameter, the Reynolds number, which quantifies the separation of length-scales in the flow. The Reynolds number based on the Taylor microscale \[97\] is Re$^{λ}$ ≈ 380. The simulation was conducted by solving Eq. (40) with 1024$^{3}$ spatial Fourier modes, which is enough to accurately resolve all the relevant length-scales of the flow. The system is multiscale and highly chaotic, with roughly 10$^{9}$ degrees of freedom.

In the following, we summarize the main parameters of the simulation. The reader is referred to Cardesa et al. \[38\] for more details about the flow set-up. The spatial- and time- average of the turbulent kinetic energy (K = uiui/2) and dissipation (ε = 2νSijSij ) are denoted by Kavg and εavg, respectively, where Sij = (∂ui/∂x$^{j}$ + ∂uj/∂xi)/2 is the rate-of-strain tensor. The ratio between the largest and smallest length-scales of the problem can be quantified by Lε/η = 1800, where L$^{ε}$ = K 3/2 avg /εavg is the integral length-scale, and η = (ν $^{3}$/εavg) 1/4 is the Kolmogorov length-scale. The data generated is also time-resolved, with flow fields stored every ∆t = 0.0076Tε, where T$^{ε}$ = Kavg/εavg, and was purposely run for long times to enable the reliable computation of conditional entropies. The total time simulated

![](_page_10_Figure_1.jpeg)

FIG. 4: Isosurfaces of the instantaneous kinetic energy transfer Σ$^{i}$ for filter sizes (a) ∆ = ¯ ∆¯ $^{1}$ = 163η (denoted by Σ1) and (b) ∆ = ¯ ∆¯ $^{4}$ = 21η (denoted by Σ4) at the same time.

after transients was equal to 165Tε.

The next step is to quantify the kinetic energy carried by the energy-containing eddies at various length-scales as a function of time. To that end, the i-th component of the instantaneous flow velocity ui(x, t) is decomposed into large- and small- components according to ui(x, t) = ¯ui(x, t) + u 0 i (x, t), where ¯(·) denotes the low-pass Gaussian filter operator,

$$\bar{u}_i(\mathbf{x}, t) = \int_V \frac{\sqrt{\pi}}{\Delta} \exp \left[ -\pi^2 (\mathbf{x} - \mathbf{x}')^2 / \Delta^2 \right] u_i(\mathbf{x}') d\mathbf{x}', \quad (41)$$

and ∆ is the filter width. The kinetic energy of the large-scale field evolves as ¯

$$\left(\frac{\partial}{\partial t} + \bar{u}_j \frac{\partial}{\partial x_j}\right) \frac{1}{2} \bar{u}_i \bar{u}_i = -\frac{\partial}{\partial x_j} (\bar{u}_j \bar{\Pi} + \bar{u}_i \tau_{ij}^{\text{SGS}} - 2\nu \bar{u}_i \bar{S}_{ij}) + \Sigma - 2\nu \bar{S}_{ij} \bar{S}_{ij} + \bar{u}_i \bar{f}_i, \quad (42)$$

where τ SGS ij = (uiu$^{j}$ − u¯iu¯$^{j}$ ) is the subgrid-scale stress tensor, which represents the effect of the (filtered) small-scale eddies on the (resolved) large-scale eddies. The interscale energy transfer between the filtered and unfiltered scales is given by Σ = τ SGS ij $^{S}$¯ ij , which is the present quantity of interest.

The velocity field is low-pass filtered at four filter widths: ∆¯ $^{1}$ = 163η, ∆¯ $^{2}$ = 81η, ∆¯ $^{3}$ = 42η, and ∆¯ $^{4}$ = 21η. The filter widths selected lay in the inertial range of the simulation within the integral and Kolmogorov length-scales: $^{L}$$^{ε}$ $^{&}$gt; ∆¯ $^{i}$ > η, for i = 1, 2, 3 and 4. The resulting velocity fields are used to compute the interscale energy transfer at scale ∆¯ i , which is denoted by Σi(x, t). Examples of three-dimensional isosurfaces of Σ$^{1}$ and Σ$^{4}$ are featured in figure 4 to provide a visual reference of the spatial organization of the interscale energy transfer. We use the volumeaveraged value of Σ$^{i}$ over the whole domain, denoted by hΣii, as a marker for the time-evolution of the interscale energy transfer. Note that hΣii is only a function of time. Figure 5 contains a fragment of the time-history of hΣii for i = 1, 2, 3 and 4.

We can now relate the current formulation with the notation introduced in §IV A. The full system state Q n is given by the velocity components u$^{i}$ and pressure Π for the 1024$^{3}$ Fourier modes. The map Q $^{n}$+1 = f(Q n ) is obtained from the spatio-temporal discretization of the Navier–Stokes equations in Eq. (40). The observable states Y n are represented by the interscale turbulent kinetic energy transfer Y $^{n}$ = [hΣ1i,hΣ2i,hΣ3i,hΣ4i], and the mapping for the observable states Y $^{n}$ = h(Q n ) is derived from the definition of Σ$^{i}$ in conjunction with the discrete version of Eq. (40).

![](_page_11_Figure_1.jpeg)

FIG. 5: An extract of the time-history of hΣ1i, hΣ2i, hΣ3i, and hΣ4i (from black to red). Although not shown, the whole time-span of the signals is 165Tε.

![](_page_11_Figure_3.jpeg)

FIG. 6: (a) Information flux T Σ $^{i}$→$^{j}$ among interscale energy-transfer signals at different scales. (b) Correlation map $^{C}$i→$^{j}$ between interscale energy-transfer signals as defined by Eq. (44). For simplicity, the labels in the axes are Σ$^{i}$ , although they actually signify hΣii. The self-induced intrascale information fluxes T Σ $^{i}$→$^{i}$ in are masked in light red.

We examine the propagation of information among hΣii by evaluating the information flux defined in Eq. (26). We focus first on the information flux from one single energy transfer hΣii at time t to the energy transfer hΣ$^{j}$ i at time t + ∆t, termed as T Σ $^{i}$→$^{j}$ . The time-delay selected is ∆t = 0.046Tε, which is consistent with the time-lag for energy transfer reported in the literature \[38\]. It was tested that the conclusions drawn below are not affected when the value of ∆$^{t}$ was halved and doubled. It was also assessed that P$^{T}$ Σ ¯ı→$^{j}$ $^{+}$$^{T}$ Σ leak,j is equal to H(hΣ$^{j}$ i) to within machine precision. The information fluxes T Σ $^{i}$→$^{j}$ are normalized by H(hΣ$^{j}$ i) and organized into the causality map shown in figure 6(a). Our principal interest is in the interscale propagation of information (T Σ $^{i}$→$^{j}$ with $^{i}$ $^{6}$$^{=}$ $^{j}$). Consequently, the self-induced intrascale information fluxes (T Σ $^{i}$→$^{i}$ ) in figure 6(a) are masked in light red, as they tend to dominate (i.e., variables are mostly causal to themselves). The information fluxes in figure 6(a) vividly capture the forward energy cascade of information toward smaller scales, which is inferred from strongest information fluxes:

$$T_{1 \rightarrow 2}^\Sigma \rightarrow T_{2 \rightarrow 3}^\Sigma \rightarrow T_{3 \rightarrow 4}^\Sigma. \quad (43)$$

Backward transfer of information from smaller to larger scales is also possible, but considerably feeble compared to the forward information flux. Hence, the present analysis provides the first evidence of the forward, sequential-in-scale turbulent energy cascade from the information-theoretic viewpoint for the full Navier–Stokes equations. Our results are consistent with previous studies on the forward the energy cascade using correlation-based methods \[38,] [86\] and information-theoretic tools applied to the Gledzer–Ohkitana–Yamada shell model \[49\].

It is also revealing to compare the results in figure 6(a) with an equivalent time-cross correlation, as the latter is routinely employed for causal inference by the fluid mechanics community. The time-cross-correlation 'causality' from

![](_page_12_Figure_1.jpeg)

FIG. 7: Information flux among energy-transfer signals at different scales for (a) T Σ [i,k]→$^{j}$ and (b) T Σ [i,k,l]→$^{j}$ . The intrascale information fluxes T Σ [i,k]→$^{i}$ and T Σ [i,k,l]→$^{i}$ are masked with light red color. For simplicity, the labels in the axes are Σ$^{i}$ , although they actually signify hΣii.

hΣii to hΣ$^{j}$ i is defined as

$$C_{i \rightarrow j} = \frac{\sum_{n=1}^{N_t} \langle \Sigma_i \rangle (t_n) \langle \Sigma_j \rangle (t_n + \Delta t)}{\left( \sum_{n=1}^{N_t} \langle \Sigma_i \rangle^2 (t_n) \right)^{1/2} \left( \sum_{n=1}^{N_t} \langle \Sigma_j \rangle^2 (t_n) \right)^{1/2}}, \quad (44)$$

where hΣii(tn) signifies hΣii at time tn, and N$^{t}$ is the total number of times stored of the simulation. The values of Eq. (44) are bounded between 0 and 1. The correlation map, $^{C}$i→$^{j}$ , is shown in figure 6(b). The process portrayed by $^{C}$i→$^{j}$ is far more intertwined than its information-flux counterpart offered in figure 6(a). Similarly to $^{T}$ Σ $^{i}$→$^{j}$ , the correlation map also reveals the prevailing nature of the forward energy cascade (Ci→$^{j}$ larger for j > i). However, $^{C}$i→$^{j}$ is always above 0.8, implying that all the interscale energy transfers are tightly coupled. This is inconsistent with the information flux in figure 6(a) and is probably due to the inability of $^{C}$i→$^{j}$ to compensate for the effect of intermediate variables (e.g., a cascading process of the form Σ$^{1}$ → Σ$^{2}$ → Σ$^{3}$ would result in non-zero correlation between Σ$^{1}$ and Σ$^{3}$ via the intermediate variable Σ2). As a consequence, $^{C}$i→$^{j}$ also fails at shedding light on whether the energy is cascading sequentially from the large scales to the small scales (i.e. hΣ1i → hΣ2i → hΣ3i → Σ4), or on the other hand, the energy is transferred between non-contiguous scales (e.g. hΣ1i → hΣ3i without passing through hΣ2i). We have seen that the information flux in figure 6(a) supports the former: the energy is predominantly transfer sequentially according to relation in Eq. (43). Overall, the inference of causality based on the time-cross correlation is obscured by the often mild asymmetries in $^{C}$i→$^{j}$ and the failure of $^{C}$i→$^{j}$ to account for the effects of a third variable. In contrast, the causal map in figure 6(a) conveys a more intelligible picture of the influence among energy transfers at different scales.

For completeness, figure 7 includes the information flux due to the joint effect of two and three variables, where the values of T Σ [i,j]→$^{j}$ and T Σ [i,j,k]→$^{j}$ have also been masked for clarity. The largest information fluxes are

$$ T_{[1,2] \rightarrow 3}^\Sigma, T_{[2,3] \rightarrow 4}^\Sigma , and T_{[1,2,3] \rightarrow 4}^\Sigma \quad (45) $$

which are found to be of the same order of magnitude as T Σ $^{i}$→$^{j}$ . The result is again consistent with the prevailing downscale propagation of information of the energy cascade.

Finally, we calculate the information leak (T Σ leak,j ) from Eq. (30) to quantify the amount of information unaccounted for by the observable variables. The ratios T Σ leak,j/H(hΣ$^{j}$ i) are found to be 0.35, 0.24, 0.18, and 0.13 for j = 1, 2, 3 and 4, respectively. Therefore, the information from unobserved states diminishes towards the smallest scales. The largest leak occurs for hΣ1i, where ∼35% of the information comes from variables not considered within the set [hΣ1i, hΣ2i, hΣ3i, hΣ4i].

#### V. MODELING

A crucial step in reduced-order modeling of physical system consists of the identification of transformations enabling parsimonious, yet informative representations of the full system. While in some cases transformations can be carried out on the basis of intuition and experience, straightforward discrimination of the most relevant degrees of freedom is challenging for complex problems, most notably for chaotic, high-dimensional physical systems. In this context, information theory has emerged as a valuable framework for model selection and multimodel inference. Particularly noteworthy is the work by Akaike \[98][–100\], where models are selected on the basis of the relative amount of information from observations they are capable of accounting for. The approach, which shares similarities with Bayesian inference, offers an elegant generalization of the maximum likelihood criterion via entropy maximization \[100\]. Akaike's ideas have also bridged the use of the Kullback's information for parameter estimation and model identification techniques \[101\]. Other relevant studies have leveraged information-theoretic tools for coarse-graining of dynamical systems assisted by Monte-Carlo methods, renormalization group, or mapping-entropy techniques e.g. [102–][104\]. A detailed survey of information-theoretic model selection and inference can be found in Burnham and Anderson \[105\] and Anderson \[106\]. In the last decade, information theory has also become instrumental in machine learning, mostly within the subfield of deep reinforcement learning \[107\]. Examples of the latter are neural network training via the cross-entropy cost functional and estimation of confidence bounds for value functions and agent policies e.g. [108–][113\]. In this section, we formulate the problem of reduced-order modeling for chaotic, high-dimensional dynamical systems within the framework of information theory. We derived the equation that relates model accuracy with the amount of information preserved from the original system. The conditions for maximum information-preserving models are also formulated in terms of the mutual information and Kullback-Leibler divergence of the quantities of interest. The theory is applied to devise a subgrid-scale model for large-eddy simulation of isotropic turbulence.

#### A. Formulation

Let us denote the state of the system to be modeled at time t$^{n}$ by Q $^{n}$ = [Q$^{n}$ 1 , ..., Q$^{n}$ $^{N}$ ], where N is the total number of degrees of freedom. The dynamics of the full system are completely determined by

$$Q^{n+1} = f(Q^n), \quad (46)$$

where the map f advances the state of the system to an arbitrary time in the future. It was shown in §III that by construction of Eq. (46), it holds that

$$H(Q^{n+1}|Q^n) = 0, \quad (47)$$

i.e., there is no uncertainty in the future state Q $^{n}$+1 given the past state Q n .

We aim at modeling a subset of the phase-space of the full system denoted by $^{Q}$e $^{n}$ = [Q$^{n}$ 1 , ..., Q$^{n}$ N˜ ] with N < N ˜ , where N˜ are the degrees of freedom of the model. Accordingly, the state vector of the full system is decomposed as

$$Q^n = [\tilde{Q}^n, Q'^n], \quad (48)$$

n = Qe n where $^{Q}$e $^{n}$ is the state to be modeled (e.g., the information accessible to the model) and $^{Q}$ 0$^{n}$ are the inaccessible degrees of freedom that the model must account for. The exact dynamics of the modeled state is governed by

$^{Q}$e $^{n}$+1 $^{=}$ $^{f}$˜(Qe $^{n}$ where $^{f}$˜ are the components of $^{f}$ corresponding to the states $^{Q}$e $^{n}$. It can be readily shown from Eq. [(49)] that disposing of Q 0$^{n}$ may result in an increase of uncertainty in the future states quantified by

$$\bar{Q}^{n+1} = \tilde{f}(\bar{Q}^n, Q'^n), \quad (49)$$

$^{H}$(Qe $^{n}$+1|Qe $^{n}$ ) = $^{I}$(Qe $^{n}$+1; $^{Q}$ |Qe n ) $^{≥}$ $^{H}$(Qe $^{n}$+1|Qe $^{n}$ Equation [(50)] represents the fundamental loss of information for truncated systems: given the initial truncated state $^{Q}$e $^{n}$, the uncertainty in the future state $^{Q}$e $^{n}$+1 is equal to the information shared between $^{Q}$ $^{0}$$^{n}$ and $^{Q}$e $^{n}$+1 that cannot be accounted for by $^{Q}$e $^{n}$. Figure [$^{8}$] provides a visual representation of Eq. [(50)]. If the system is reversible, then Eq. [(50)] reduces to

$$H(\tilde{Q}^{n+1}|\tilde{Q}^n) = H(\tilde{Q}^{n+1}, Q'^n|\tilde{Q}^n) \geq H(\tilde{Q}^{n+1}|\tilde{Q}^n, Q'^n) = 0. \quad (50)$$

$^{H}$(Qe $^{n}$+1|Qe $^{n}$ |Qe n and the uncertainty in the future truncated state $^{Q}$e $^{n}$+1 is equal to the amount of information in $^{Q}$ 0$^{n}$ that cannot be recovered from $^{Q}$e $^{n}$.

$$H(\tilde{Q}^{n+1}|\tilde{Q}^n) = H(Q'^n|\tilde{Q}^n), \quad (51)$$

![](_page_14_Picture_1.jpeg)

FIG. 8: Schematic of the relationship among the entropies of the modeled (accessible) state $^{Q}$e n , the future modeled state Qe n+1 , and the inaccessible degrees of freedom Q0$^{n}$ .

#### 1. Information-theoretic bounds to model error

Let us consider a model with access to the information contained in $^{Q}$e $^{n}$ (i.e., the exact initial condition for the truncated state) but not to the information in Q 0$^{n}$ (i.e., inaccessible degrees of freedom). The governing equation for the model is denoted by

$^{Q}$b $^{n}$+1 $^{=}$ $^{f}$b(Qe $^{n}$ where $^{Q}$b $^{n}$+1 is the model prediction, which does not need to coincide with the exact solution $^{Q}$e $^{n}$+1 obtained from Eq. [(49)] using the exact map $^{f}$e. We aim at finding a model map $^{f}$b that predicts the future state to within the error $^{ε}$,

$$\widehat{Q}^{n+1} = \widehat{f}(\widehat{Q}^n), \quad (52)$$

$$\|\hat{Q}^{n+1} - \tilde{Q}^{n+1}\| \leq \varepsilon, \quad (53)$$

where || · || is the L$^{1}$ norm. In particular, we are interested in the bounds for the error expectation

$$ \mathbb{E}[\ \hat{Q}^{n+1} - \hat{Q}^{n+1}\ ]. \quad (54) $$
| uncertainty in the exact solution is quantified by |      |

Given the model prediction from Eq. [(52)], the uncertainty in the exact solution is quantified by

$$H(\tilde{Q}^{n+1}|\hat{Q}^{n+1}), \quad (55)$$

$^{H}$(Qe $^{n}$+1|Qb $^{n}$+1), (55) that we seek to relate to the model error ε. In general, nothing can be said about the relationship between $^{H}$(Qe $^{n}$+1|Qb $^{n}$+1) and the loss of information of the truncated system $^{H}$(Qe $^{n}$+1|Qe $^{n}$). Thus, the latter might be smaller,

equal, or larger than $^{H}$(Qe $^{n}$+1|Qb $^{n}$+1) contingent on $^{f}$b. Let us denote by P$^{e}$ the probability of obtaining a modeling error above the prescribed tolerance ε,

---

$$P_e = \text{Pr}(\|\hat{\mathbf{Q}}^{n+1} - \tilde{\mathbf{Q}}^{n+1}\| > \varepsilon).$$
 (56)

---

the uncertainty in Eq. (55) via a generalized Fano's inequality as

---

The error from Eq. [(53)] can be related to the uncertainty in Eq. [(55)] via a generalized Fano's inequality as

$$P_e \geq \frac{H(\tilde{\mathbf{Q}}^{n+1}|\hat{\mathbf{Q}}^{n+1}) - \log_2(\varepsilon/\Delta_Q) - 1}{\log_2(\tilde{N}) - \log_2(\varepsilon/\Delta_Q)}, \quad (57)$$

where ∆$^{Q}$ is a measure of the size of the phase-space partition D$^{i}$ introduced in §[III.] Equation [(57)] reveals that, given a model $^{f}$b, the probability of incurring an error larger than $^{ε}$ is lower bounded by the information loss of the model. It is convenient to rewrite Eq. [(57)] as

$$P_e \geq \frac{H(\tilde{\mathbf{Q}}^{n+1}) - I(\tilde{\mathbf{Q}}^{n+1}; \tilde{\mathbf{Q}}^{n+1}) - \log_2(\varepsilon/\Delta_Q) - 1}{\log_2(\tilde{N}) - \log_2(\varepsilon/\Delta_Q)}, \quad (58)$$

where $^{I}$(Qe $^{n}$+1; $^{Q}$b $^{n}$+1) is the mutual information between the 'true' state and the model prediction. A lower bound for the expected error is found by applying the Markov's inequality to Eq. [(58)],

$$\mathbb{E}[\|\hat{\mathbf{Q}}^{n+1} - \tilde{\mathbf{Q}}^{n+1}\|] \geq \varepsilon \frac{H(\hat{\mathbf{Q}}^{n+1}) - I(\hat{\mathbf{Q}}^{n+1}; \hat{\mathbf{Q}}^{n+1}) - \log_2(\varepsilon/\Delta_Q) - 1}{\log_2(\tilde{N}) - \log_2(\varepsilon/\Delta_Q)}. \quad (59)$$

Note that  $H(\tilde{Q}^{n+1})$  in Eq. (59) is just the information content of the true state, which is unaffected by the model. Therefore, the potential predictive capabilities of a model are attained by maximizing the mutual information between  $\tilde{Q}^{n+1}$  and  $\hat{Q}^{n+1}$ . Equation (59) echoes the intuition that the performance of a reduced-order model improves with the amount of information preserved from the system to be modeled. Another advantage of formulating the modeling problem in terms of mutual information  $I(\tilde{Q}^{n+1}, \hat{Q}^{n+1})$  is that the latter is a concave function of its arguments, which facilitates the optimization of Eq. (59).

A second model condition can be derived by relaxing the error constraint in Eq. (53) to

$$\|p(\hat{\mathbf{q}}^{n+1}) - p(\tilde{\mathbf{q}}^{n+1})\| \leq \varepsilon'. \quad (60)$$

where  $p(\tilde{\mathbf{q}}^{n+1})$  is the true probability distribution of the system state and  $p(\hat{\mathbf{q}}^{n+1})$  is the probability distribution of the model state. The error constraint in Eq. (60) is weaker than the constraint in Eq. (53), as evidenced by the fact that  $\|\tilde{Q}^{n+1} - \tilde{Q}^{n+1}\| \geq 0$  even if  $p(\tilde{\mathbf{q}}^{n+1}) = p(\hat{\mathbf{q}}^{n+1})$ . Hence, a model can flawlessly replicate the probability distribution (i.e., the statistics) of the actual state, yet the sequential samples drawn from the model (i.e., the dynamics) might not coincide with the ground truth owing to the lack of mutual information between  $\hat{Q}^{n+1}$  and  $\tilde{Q}^{n+1}$ .

The error defined by Eq. (60) allow us to estimate an upper bound for the expectation of the modeling error of probabilities. First, let us introduce the Kullback-Leibler (KL) divergence between  $p(\tilde{\mathbf{q}}^{n+1})$  and  $p(\hat{\mathbf{q}}^{n+1})$ ,

$$\text{KL}(\tilde{Q}^{n+1}, \hat{Q}^{n+1}) = \sum p(\tilde{\mathbf{q}}^{n+1}) \log[p(\tilde{\mathbf{q}}^{n+1})/p(\hat{\mathbf{q}}^{n+1})], \quad (61)$$

which is a measure of the average number of bits required to recover  $p(\tilde{\mathbf{q}}^{n+1})$  using the information in  $p(\hat{\mathbf{q}}^{n+1})$ . From a Bayesian inference viewpoint,  $\text{KL}(\tilde{Q}^{n+1}, \hat{Q}^{n+1})$  represents the information lost when  $p(\tilde{\mathbf{q}}^{n+1})$  is used to approximate  $p(\tilde{\mathbf{q}}^{n+1})$ . Equation (61) is an extension of Shannon's concept of information and is sometimes referred to as relative entropy [114, 115]. It can be shown via the Pinsker's inequality [116] that

$$\text{KL}(\tilde{Q}^{n+1}, \hat{Q}^{n+1}) \geq \frac{1}{2 \ln 2} \|p(\hat{\mathbf{q}}^{n+1}) - p(\tilde{\mathbf{q}}^{n+1})\|^2, \quad (62)$$

with  $\text{KL}(\tilde{Q}^{n+1}, \hat{Q}^{n+1}) = 0$  if and only if the model predictions are statistically identical to those from the original system. Equation (62) provides a connection between information loss and probabilistic model performance. Desirable maps  $\hat{\mathbf{f}}$  are those minimizing Eq. (61), which results in models containing the coherent information in the data, while leaving out the incoherent noise. Similarly to the mutual information, the KL divergence has the advantage of being convex with respect to the input arguments, which facilitates the search of the minimum.

Equation (61) can be written as

$$\text{KL}(\tilde{Q}^{n+1}, \hat{Q}^{n+1}) = \sum -p(\tilde{\mathbf{q}}^{n+1}) \log[p(\hat{\mathbf{q}}^{n+1})] - H(\tilde{Q}^{n+1}) \quad (63)$$

where the first term in the right-hand side of Eq. (63) is referred to as the cross entropy between  $\tilde{Q}^{n+1}$  and  $\hat{Q}^{n+1}$ . Taking into account that  $H(\tilde{Q}^{n+1})$  is fixed and the cross entropy is equal or larger than zero, minimizing  $\text{KL}(\tilde{Q}^{n+1}, \hat{Q}^{n+1})$  also implies minimizing the cross entropy, resulting in the minimum cross-entropy principle [59, 117]. Additionally, if  $p(\tilde{\mathbf{q}}^{n+1})$  is taken to be the uniform distribution, then

$$\text{KL}(\tilde{Q}^{n+1}, \hat{Q}^{n+1}) = \sum -\frac{1}{\tilde{N}} \log[p(\hat{\mathbf{q}}^{n+1})] - \log(\tilde{N}), \quad (64)$$

and minimizing Eq. (64) is equivalent to maximizing  $\sum \log[p(\hat{\mathbf{q}}^{n+1})]$ . The latter is the well-known maximum likelihood principle, which surfaces as a particular case of the KL-divergence minimization proposed here.

## 2. Conditions for maximum information-preserving models

The error bounds presented above provide the information-theoretic foundations for model discovery. The discussion has been centered on  $\tilde{Q}^{n+1}$ ; however, in most occasions, we are not interested in the prediction of the full truncated state, but rather in some quantity of interest

$$\tilde{\mathbf{Y}}^{n+1} = \mathbf{h}(\tilde{Q}^{n+1}), \quad (65)$$

such that the dimensionality of $^{Y}$e $^{n}$+1, denoted by $^{N}$$^{Y}$ , is much smaller than the dimensionality of $^{Q}$e $^{n}$+1, i.e., $^{N}$$^{Y}$ $^{N}$˜. One example is the aerodynamic modeling of an airfoil: the modeled state $^{Q}$e $^{n}$+1 is the flow around the airfoil, which could contain millions of degrees of freedom, whereas $^{Y}$e $^{n}$+1 may be the surface forces, which contain a few degrees of freedom. Most of the discussion in §[V A 1] is applicable to the modeling of $^{Y}$e $^{n}$+1. Given the quantity of interest predicted by the model

$$\hat{Y}^{n+1} = h(\hat{Q}^{n+1}), \quad (66)$$

the bounds for the modeling error are

$$\begin{aligned} \mathbb{E}[\|\tilde{\mathbf{Y}}^{n+1} - \tilde{\mathbf{Y}}^{n+1}\|] &\geq \varepsilon_Y \frac{H(\mathbf{Q}^{n+1}) - I(\tilde{\mathbf{Y}}^{n+1}, \tilde{\mathbf{Y}}^{n+1}) - \log_2(\varepsilon_Y/\Delta_Y) - 1}{\log_2(N_Y) - \log_2(\varepsilon_Y/\Delta_Y)}, & (67a) \\ \|p(\tilde{\mathbf{y}}^{n+1}) - p(\tilde{\mathbf{y}}^{n+1})\| &< (2 \ln 2 \text{ KL}(\tilde{\mathbf{Y}}^{n+1}, \tilde{\mathbf{Y}}^{n+1}))^{1/2}, & (67b) \end{aligned}$$

||p(yb where ∆$^{Y}$ is the partition size for the state $^{Y}$e $^{n}$+1. In summary, Eq. [(67)] establishes that a faithful model must i) maximize the mutual information between the model state and the true state, and ii) minimize the KL divergence between their probabilities. The mutual information assist the model to reproduce the dynamics of the original system, while the KL divergence enables the accurate prediction of the statistical quantities of interest. Whether we choose to optimize the mutual information, the KL divergence, or a combination of both depends on the scope of the model. We close this section by remarking that Eq. [(67)] is a necessary condition for the discovery of accurate models, but it is not sufficient. Eq. [(67)] does not provide the information of what physical quantities should be preserved by the model, nor the modeling assumptions to undertake. Those will rely on physical insight of the system to model and clear understanding of the relevant characteristic scales (length, time, velocities,...) involved in the problem.

$$\|p(\hat{\boldsymbol{y}}^{n+1}) - p(\hat{\boldsymbol{y}}^{n+1})\| \leq \left(2 \ln 2 \operatorname{KL}(\tilde{\boldsymbol{Y}}^{n+1}, \hat{\boldsymbol{Y}}^{n+1})\right)^{1/2}, \quad (67b)$$

### B. Application: Maximum information-preserving subgrid-scale model for LES

Most turbulent flows of engineering significance cannot be simulated by solving all the fluid motions of the Navier-Stokes equations because the range scales involved is so large that the computational cost becomes prohibitive. In LES, only the large eddies are resolved, and the effect of the small scales on the larger eddies is modeled through an SGS model [\[118\] as illustrated in figure 9. The approach enables a reduction of the computational cost by several orders of magnitude while still capturing the statistical quantities of interest. In the present section, we demonstrate the principle of maximum conservation of information discussed in §V by devising an SGS model for LES.

The governing equations for LES are formally derived by applying a spatial filter to Eq. (40),

$$\frac{\partial \bar{u}_i}{\partial t} + \frac{\partial \bar{u}_i \bar{u}_j}{\partial x_j} + \frac{\partial \tau_{ij}^{\text{SGS}}}{\partial x_j} = -\frac{1}{\rho} \frac{\partial \bar{\Pi}}{\partial x_i} + \nu \frac{\partial^2 \bar{u}_i}{\partial x_j \partial x_j}, \quad \frac{\partial \bar{u}_i}{\partial x_i} = 0, \quad (68)$$

where ¯(·) denotes spatially filtered quantity, and $^{\tau}$ SGS ij is the effect of the subgrid scales on the resolved eddies, which has to be modeled. The filter operator on a variable φ is defined as

$$\bar{\phi}(\mathbf{x}, t) \equiv \int_V G(\mathbf{x} - \mathbf{x}'; \bar{\Delta}) \phi(\mathbf{x}', t) d\mathbf{x}', \quad (69)$$

where G is the filter kernel with filter size ∆, and ¯ V is the domain of integration. The system in Eq. (68) is assumed to be severely truncated in the number of the degrees of freedom with respect to Eq. (40). The objective of LES is to model the SGS tensor as function of known filtered quantities,

$$\tau_{ij}^{\text{SGS}} = \tau_{ij}^{\text{SGS}}(\bar{S}_{ij}, \bar{\Omega}_{ij}, \bar{\Delta}; \boldsymbol{\theta}), \quad (70a)$$

where S¯ ij = (∂u¯i/∂x$^{j}$ + ∂u¯j/∂xi)/2, and Ω¯ ij = (∂u¯i/∂x$^{j}$ − ∂u¯j/∂xi)/2 are the filtered rate-of-strain and rate-ofrotation tensors, respectively, and θ are model parameters.

In the present formulation, the map f in Eq. (46) corresponds to a discrete version of Eq. (40), in which all the space and time scales are accurately resolved. The state vector Q n is given by the discretization of u$^{i}$ and Π in a grid fine enough to capture all the relevant scales of motion. The map for the model, $^{f}$b, is derived from the discretization

of Eq. (40), and the model state $^{Q}$b $^{n}$ corresponds to the filtered velocities and pressure, ¯u$^{i}$ and Π. ¯ A common misconception in LES modeling is that the closure problem of determining τ SGS ij arises from introducing the filter operator. Interestingly, this is not entirely accurate. Instead, the formalism introduced in §V shows that the

![](_page_17_Diagram_1.jpeg)

FIG. 9: Schematic of an LES grid and the turbulent eddies of different sizes. Only the large eddies are resolved by the grid, whereas the information from the small-scale eddies is lost.

closure problem is a consequence of the loss of information introduced by the filter rather than the action of filtering itself. This is easy to demonstrate by noting that the analytic form of τ SGS ij is completely determined when the filter is reversible, i.e., the information is conserved \[119–][122\]. One example of reversible filter is given by the differential filter \[123\]

$$G(\mathbf{x} - \mathbf{x}'; \bar{\Delta}) = \frac{1}{4\pi\bar{\Delta}^2} \frac{\exp(-|\mathbf{x} - \mathbf{x}'|/\bar{\Delta})}{|\mathbf{x} - \mathbf{x}'|}, \quad (71)$$

such that the analytic form of the τ SGS ij is exactly given by

$$\tau_{ij}^{\text{SGS}} = \overline{\bar{u}_i \bar{u}_j} - \bar{\Delta}^2 \bar{u}_j \frac{\partial \bar{u}_i}{\partial x_k \partial x_k} - \bar{\Delta}^2 \bar{u}_i \frac{\partial \bar{u}_j}{\partial x_k \partial x_k} + \bar{\Delta}^4 \frac{\partial \bar{u}_i}{\partial x_k \partial x_k} \frac{\partial \bar{u}_j}{\partial x_k \partial x_k} - \bar{u}_i \bar{u}_j. \quad (72)$$

Equation (72) is a function of the filtered velocities ¯u$^{i}$ , which are accessible to the model, and does not pose any closure problem. The actual closure problem emerges from the application of irreversible filters and/or the coarse discretization of the governing equations, which entail a truncation of the number of degrees of freedom in the system. In those situations, the LES grid resolution is unable to represent the small scales (i.e., subgrid scales), which in turn entails a loss of information. Hence, the paradigm of conservation of information discussed in §V A arises naturally as a fundamental aspect of LES modeling.

We leverage Eq. (67b) to construct an SGS model for turbulent flows. The flow considered is similar to that presented in §IV B: forced isotropic turbulence \[124\] in a triply periodic, cubic domain with size equal to L as shown in figure 10. The exact solution is obtained from a DNS using 512$^{3}$ dealiased Fourier modes for the spatial discretization and a fourth-order Runge-Kutta time stepping method. The turbulence is sustained by adding a linear forcing to the right-hand side of Eq. (40) equal to f$^{i}$ = Au$^{i}$ , where A was adjusted to maintain on average Re$^{λ}$ ≈ 260. The simulation was run for 50 integral times after initial transients. Figure 10 features a visualization of the energy field and dissipation field from the DNS, highlighting the separation of scales in the system. The functional form considered for the SGS stress tensor is

$$\tau_{ij}^{\text{SGS}} - \frac{1}{3}\tau_{kk}^{\text{SGS}}\delta_{ij} = \theta_1\bar{\Delta}^2\bar{S}_{ij}\sqrt{\bar{S}_{nm}\bar{S}_{nm}} + \theta_2\bar{\Delta}^2(\bar{S}_{ik}\bar{\Omega}_{kj} - \bar{\Omega}_{ik}\bar{S}_{kj}), \quad (73)$$

where δij is the Kronecker delta, and θ$^{1}$ and θ$^{2}$ are modeling parameters to be determined. Equation (73) is derived by retaining the two leading terms from the general expansion of the SGS tensor in terms of S¯ ij and Ω¯ ij proposed by Lund and Novikov \[125\].

![](_page_18_Figure_1.jpeg)

FIG. 10: Visualization of (a) the instantaneous turbulent kinetic energy uiui/2 and (b) enstrophy ωiω$^{i}$ , where ω$^{i}$ is the vorticity. The colormap ranges from 0 (dark) to 0.8 of the maximum value (light) of turbulent kinetic energy and enstrophy, respectively.

Let us introduce the interscale energy transfer and viscous dissipation at the filter cut-off ∆ given by ¯

$$\bar{\Gamma} = (\bar{u}_i \bar{u}_j - \bar{u}_i \bar{u}_j) \bar{S}_{ij} - 2\nu \bar{S}_{ij} \bar{S}_{ij}. \quad (74)$$

The modeling assumption proposed here is that the information content of p(Γ¯ $^{1}$) must be equal to the information content of p(Γ¯ $^{2}$γ), where Γ¯ $^{1}$ and Γ¯ $^{2}$ are Γ at two different scales ∆¯ $^{1}$ and ∆¯ $^{2}$, respectively, and $^{γ}$ = (∆¯ $^{1}$/∆¯ 2) 2/3 is a scaling factor. This self-similarity in the information implies that the energy transfer at two different scales should satisfy

$$p(\bar{\Gamma}_1) \approx p(\bar{\Gamma}_{2\gamma})/\gamma. \quad (75)$$

The hypothesis in Eq. (75) is corroborated in figure 11 using DNS data. Figure 11(a) shows p(Γ¯ $^{i}$) for three different values of the filter widths: ∆¯ $^{1}$ = L/32, ∆¯ $^{2}$ = L/16, and ∆¯ $^{3}$ = L/8. The scaling condition from Eq. (75) is tested in figure 11(b), which reveals the improved collapse using the factor γ. A similar scaling result was observed by Aoyama et al. \[84\].

In the case of LES, the interscale energy transfer and dissipation also depends on the contribution of the SGS model as

$$\bar{\Gamma} = (\bar{u}\bar{u}_j - \bar{u}\bar{u}_j)\bar{S}_{ij} - 2\nu\bar{S}_{ij}\bar{S}_{ij} + \tau_{ij}^{\text{SG}}\bar{S}_{ij}. \quad (76)$$

Hence, the model proposed aims at minimizing the information lost when p(Γ¯ $^{1}$) is used to approximate $^{p}$(Γ¯ $^{2}$γ) in the LES solution with ∆¯ $^{1}$ = 2∆ and ¯ ∆¯ $^{2}$ = 2∆¯ $^{1}$. The model is formulated using the KL divergence, which ensures that the average information required for reconstructing p(Γ¯ $^{2}$γ) is minimum given the information in $^{p}$(Γ¯ $^{1}$),

$$\theta = \arg \min_{\theta'} \text{KL} \left( \bar{\Gamma}_{2\gamma}, \bar{\Gamma}_1 \right), \quad (77)$$

![](_page_19_Figure_1.jpeg)

FIG. 11: (a) Probability mass distributions of the interscale energy transfer and viscous dissipation, Γ¯ $^{1}$, Γ¯ $^{2}$, and Γ¯ 3, at filter cut-offs ∆¯ $^{1}$ = L/32, ∆¯ $^{2}$ = L/16, and ∆¯ $^{3}$ = L/8, respectively. The results are for DNS using sharp Fourier filter and are normalized by the standard deviation of p(Γ¯ $^{1}$), denoted by σ1. (b) Probability mass distributions of the rescaled interscale energy transfer and viscous dissipation, Γ¯ $^{1}$, Γ¯ $^{2}$γ2, Γ¯ $^{3}$γ$^{3}$ with $^{γ}$$^{2}$ = (∆¯ $^{2}$/∆¯ 1) $^{2}$/$^{3}$ and $^{γ}$$^{3}$ = (∆¯ $^{3}$/∆¯ 1) 2/3 .

where θ = (θ1, θ2) from Eq. (73). We will refer to the model as Information-Preserving SGS model, or as IP-SGS model for short. Note that the IP-SGS model only relies on the physical assumption that the information content of p(Γ¯ $^{1}$) is equal to the information content of $^{p}$(Γ¯ $^{2}$γ), and does not require any DNS data to be trained.

To validate the model, an LES is conducted using 64$^{3}$ Fourier modes. The turbulence is driven by a linear forcing with the same A value obtained for the DNS. The kernel selected is the sharp Fourier filter. The LES entails a severe truncation of the number of degrees of freedom of the original system: the DNS contains more than 130 million degrees of freedom, whereas in the LES system the number of degrees of freedom is reduced to only 0.3 million. The IP-SGS model is implemented as follows: during the LES runtime, statistics are collected on-the-fly to reconstruct the probability distributions of Γ¯ $^{2}$$^{γ}$ and Γ¯ $^{1}$. Every 100 time steps, the model parameters θ$^{1}$ and θ$^{2}$ are computed from Eq. (77) using a gradient descent method that minimizes the KL divergence.

The performance of the SGS model is evaluated in figure 12 after initial transients in the system. We use as figure of merit the kinetic energy spectrum E(κ), where κ is the wavenumber. The predictions are compared against a case without SGS model and the optimal model. The latter is defined as the SGS model of the form dictated by Eq. (73) with the values of θ$^{1}$ and θ$^{2}$ that yield the best prediction of E(κ) in the L2-norm sense. The optimal values of θ$^{1}$ and θ$^{2}$ were obtained by a parametric sweep. The results in figure 12 show that the IP-SGS model offers an accuracy comparable to the optimal model, while providing a non-trivial improvement with respect to the case without SGS model. This modeling exercise demonstrates the viability of the information-theoretic formulation presented in §V as an effective framework for reduced-order modeling of highly chaotic systems with large number of degrees of freedom.

## VI. CONTROL

The first entropic analysis of feedback control for dynamical systems was proposed by Weidemann \[126\], who envisioned the sensor/actuator device as an information transformation of the data collected. The optimal control of time-continuous systems was later attempted by Saridis \[127\], and further extended to discrete systems by Tsai et al. \[128\]. Tatikonda and Mitter \[129\] investigated the lower bounds of controllability, observability, and stability of linear systems under communication constraints between the sensor and the actuator. Touchette and Lloyd \[130\] substantially advanced the information-theoretic formulation of the control problem by redefining the concepts of controllability and observability using conditional entropies. They posed the problem of control as a task of entropyreduction, and proved that the maximum reduction of entropy achievable in a system after a one-step actuation is

![](_page_20_Figure_1.jpeg)

FIG. 12: (a) Visualization of the instantaneous turbulent kinetic energy uiui/2. The colormap ranges from 0 (dark) to 0.8 of the maximum value (light) of turbulent kinetic energy. (b) The kinetic energy spectra as a function of the wavenumber for the 'exact' DNS solution, LES with IP-SGS model, LES with optimal SGS model, and LES without SGS model. The energy spectra are normalized by u 2 ref/2L, where u 2 ref/2 is the mean kinetic energy of the DNS solution.

bounded by the mutual information between the control parameters and the current state of the system. The analysis by Touchette and Lloyd \[130\] was broaden by Delvenne and Sandberg \[131\] to more general, convex, cost functions. In the same vein, Bania \[132\] recently developed an information-aided control approach which provides results akin to those from dynamic programming but at a more affordable computational cost. A review on the thermodynamics of information and its connection with feedback control can be found in Parrondo et al. \[133\]. Despite the merits of the previous works, a notable caveat is their limited applicability to stochastic control of problems with a low number of degrees of freedom see the examples in [134\].

In this section, we provide an information-theoretic formulation of the problem of optimal control for chaotic, high-dimensional dynamical systems. New definitions of open/closed-loop control, observability, and controllability are introduced in terms of the mutual information between different states of the system. The task of optimal control is posed as the reduction in uncertainty of the controlled state given the information collected by the sensors and the action performed by the actuators. In contrast to the traditional formulation of control, which emphasizes the differential equations of the dynamical system, our formulation is centered in the probability distribution of the states. The theory is applied to achieve optimal drag reduction in a wall-bounded turbulent flow using opposition control at the wall.

#### A. Formulation

Let us denote the state of the system to be controlled at time t$^{n}$ by Q $^{n}$ = [Q$^{n}$ 1 , ..., Q$^{n}$ $^{N}$ ], where N are the total number of degrees of freedom. The state of the uncontrolled system is denoted by Q n u (with subscript u) and its dynamics is completely determined by

$$Q_u^{n+1} = f(Q_u^n), \quad (78)$$

where f is the map function introduced in §III. The system is controlled to a new state Q $^{n}$+1 (without subscript u) by means of a sensor and an actuator that together constitute the controller. The state of the sensor and actuator are denoted by S and A, respectively, and both are considered random variables. The properties of the controller are parametrized by the vector θ (e.g., actuator/sensor locations, actuator intensity and frequency, etc.). In general, the full state Q n is inaccessible and only a subset of the phase-space is observable by the sensor,

$$S^n = h(Q^n, W^n; \theta), \quad (79)$$

![](_page_21_Picture_1.jpeg)

FIG. 13: Schematic of the entropies of the system in Eq. (81). (a) Entropy of the new controlled state, Q $^{n}$+1, which is bounded by the entropies of Q n and A n , as inferred from Eq. (81). (b) Relationship among the entropies of the current state, the sensor, and the actuator.

where W$^{n}$ represents random noise in the measurements. We will consider that W$^{n}$ is uncorrelated with Q n . The noise W$^{n}$ introduces additional information into the system that can be labeled as spurious, since it masks the actual information from the state Q n . The actuator gathers the information from the sensor and acts according to the control law

$$ A^n = g(S^n, V^n; \theta) \quad (80) $$

where V n is an auxiliary random variable which provides additional stochasticity (hence, information) to the actuator and is independent of Q n . Then, the controlled system is governed by

$$ Q^{n+1} = f(Q^n, A^n) \quad (81) $$

In the case of high-dimensional, chaotic systems, control of the full state constitutes an impractical task and hence is not the main concern here. Instead, our goal is to control a few degrees of freedom which are the most impactful on reducing or enhancing a quantity of interest. The sub-state to be controlled is denoted by J n , and is also assumed to be a random variable derived from Q n ,

$$J^n = l(Q^n). \quad (82)$$

In many situations, we are interested in the controlled state once the system has reached the statistically steady state. In those cases, the time step n + 1 represents the state of the system after initial transients. As an example (in line with the application in §VI B), we can consider the reduction of drag in an airfoil by blowing and suction of air over its surface. In this case, Q n is a (high-dimensional) discrete representation of the velocity and pressure fields in all the domain surrounding the airfoil, S n are pressure probes at the airfoil surface, A n is a flow jet at the wall which modifies the air velocity around the airfoil, and J $^{n}$+1 represents the controlled (low-dimensional) drag state after transients. The goal of the control law is then to alter the probability distribution of the drag to reduce i) its mean value and ii) its standard deviation to mitigate extreme drag events.

# 1. Open-loop and closed-loop control

The information in the controlled system flows from the system state Q n to the sensor S n , and from the sensor to the actuator A n . In the general scenario, the sensor shares the information with the actuator via a communication channel. The capacity of the communication channel between S n and A n is defined as

$$ \text{Ca} = \max_{p(\mathbf{S}^n)} I(\mathbf{S}^n; \mathbf{A}^n) \quad (83) $$

where the maximum is taken over all possible input distributions p(s $^{n}$). By virtue of the noisy-channel coding theorem \[1\], the capacity in Eq. (83) provides the highest information rate (i.e., bits per second) that can be achieved with an arbitrarily small error probability between the sensor and actuator.

The mutual information between the sensor and actuator from Eq. (83) provides the grounds for the definition of open-loop and closed-loop controllers. A control is said to be open-loop if

$$ I(A^n; Q^n) = 0 \quad (84) $$

i.e., there is no shared information between the actuator and the state of the system at tn. Note that an open-loop control can still modify the information content of future states because I(Q n+1 ; A n ) ≥ 0 by means of the auxiliary random variable V n . Conversely, a control is closed-loop if

$$ I(A^n; Q^n) > 0 \quad (85) $$

namely, the current state and the actuator share an amount of information greater than zero. From Eq. (79) and (80) it can be shown that

$$I(\mathbf{A}^n; \mathbf{Q}^n) \leq I(\mathbf{S}^n; \mathbf{Q}^n). \quad (86)$$

Thus, a sufficient condition for open-loop control is I(S n ; Q n ) = 0, whereas I(S n ; Q n ) > 0 and I(A n ;S n ) > 0 are necessary conditions for closed-loop control. A constraint from Eq. (80) is that, if there is no auxiliary random noise (V n ), the actuator cannot contain more information than the sensor, H(A n ) ≤ H(S n ). The relationships among Q n , S n and A n are illustrated in Figure 13b.

It is also interesting to establish the information loss across the controller. Let us assume an sparse sensor with N$^{s}$ degrees of freedom such that $^{N}$$^{s}$ $^{N}$. The information content of the noise scales as $^{H}$(W$^{n}$ ) ∼ log Ns, while the information of the system generally follows H(Q n ) ∼ log N. It is then reasonable to assume that H(W$^{n}$ ) H(S n ) will hold in most practical situations where N$^{s}$ N. If we further assume that all the information in the actuator is obtained from the sensor S n , then the hierarchy of information loss across the controlled system is given by

$$H(\mathbf{Q}^n) \gg H(\mathbf{S}^n) \geq H(\mathbf{A}^n). \quad (87)$$

Equation (87) shows that, when the measurements are sparse, the state of the system contains more information than the sensor, which in turn contains similar or less information than the actuator. The first inequality in Eq. (87) might not hold for systems with a few degrees of freedom or a large number of sensors. In those situations, the noise could increase the (spurious) information content of the sensor to yield H(Q n ) < H(S n ). Nonetheless, here we are interested in high-dimensional systems controlled using a few measurements such that Eq. (87) is likely to hold.

#### 2. Observability and controllability

Observability (how much we can know about the system) and controllability (how much we can modify the system) represent two major pillars of modern control system theory. Here, we formulate the information-theoretic counterparts of observability and controllability. Our definitions are motivated by the no-uncertainty conditions of deterministic systems given by

$$H(\mathbf{J}^n|\mathbf{Q}^n) = 0, \quad (88a)$$

| $H(J^{n+1} Q^n, A^n) = 0.$ | (88b) |
|----------------------------|-------|
|----------------------------|-------|

Equation (88a) is a statement about the observability of J n : there is no uncertainty in J $^{n}$ when the full state of the system in known. However, uncertainties might arise when the information available is only limited to the state of the sensor. Similarly, Eq. (88b) relates to the concept of controllability: given the system state Q n and the actuator action A n , there is no uncertainty in the future state J n+1 .

Consistently with the remarks above, observability of the state J $^{n}$ with respect to the sensor S n is defined as

$$O_J \equiv \frac{I(\mathbf{J}^n; \mathbf{S}^n)}{H(\mathbf{J}^n)}, \quad (89)$$

which represents the uncertainty in J n given the information from the sensor normalized by the total information in J n such that 0 ≤ O$^{J}$ ≤ 1. The normalization by H(J n ) in Eq. (89) is introduced to provide a relative measure of the observability with respect to the total information in J n . The observability can also be expressed as a function of H(J n |S n ) by

$$O_J = 1 - \frac{H(\mathbf{J}^n|\mathbf{S}^n)}{H(\mathbf{J}^n)}, \quad (90)$$

which shows that the smaller the value of H(J n |S n ) (i.e., the uncertainty in the state J n ), the larger the value of O$^{J}$ , in line with the intuition of observability argued in Eq. (88a). We say that a system with targeted variable J n is perfectly observable with respect to the sensor S n if and only if there is no uncertainty in the state of the system conditioned to knowing the state of the sensor, namely,

$$ H(J^n S^n) = 0 \quad (91) $$

which corresponds to O$^{J}$ = 1. Conversely, O$^{J}$ = 0 if none of the information in J n is accessible to the sensor. It can be shown that in the presence of noise in the sensor, the upper bound for observability is reduced as

$$0 \leq O_J \leq 1 - \frac{I(\mathbf{W}^n; \mathbf{S}^n)}{H(\mathbf{J}^n)}. \quad (92)$$

Thus, the observability of the controller degrades proportionally to the noise contamination of the sensor as quantified by I(W$^{n}$ ;S n ), and perfect observability is unattainable when I(W$^{n}$ ;S n ) > 0.

Controllability of the future state J $^{n}$+1 with respect to the action A n is defined by

$$C_J \equiv \frac{I(\mathbf{J}^{n+1}; \mathbf{A}^n)}{H(\mathbf{J}^{n+1})}, \quad (93)$$

provided that for all future states j $^{n}$+1 and initial condition q $^{n}$ there exist a control a $^{n}$ such that p(j $^{n}$+1|q $^{n}$, a $^{n}$) 6= 0. Equation (93) quantifies the uncertainty in the targeted state J $^{n}$+1 knowing the present information from the control. Similar to the observability, C$^{J}$ is bounded by 0 ≤ C$^{J}$ ≤ 1 and can also be cast as

$$C_J = 1 - \frac{H(\mathbf{J}^{n+1}|\mathbf{A}^n)}{H(\mathbf{J}^{n+1})}, \quad (94)$$

The smaller the value of H(J $^{n}$+1|A n ) the larger the controllability of the system (i.e., less uncertainty in the future outcome). A system is perfectly controllable at state J $^{n}$+1 if and only if the uncertainty associated with the latter upon application of the control action A n is zero, i.e., there exists a non-empty set of control values such that

$$ H(J^{n+1} A^n) = 0 \quad (95) $$

which corresponds to C$^{J}$ = 1. Note that observability depends on the targeted state at a given time (J n ), whereas controllability relates the future targeted state (J $^{n}$+1) with the knowledge of the system in the state at time $^{t}$n. Overall, the highest observability and controllability are attained by maximizing the mutual information between the target state and the control, which will be leveraged in §VI A 3 when seeking optimal control strategies.

It is insightful to interpret the definitions in Eq. (89) and Eq. (93) as the answer to the question: how much additional information is needed to completely determine the state J n at time t$^{n}$ (observability) and at future times tn+1 (controllability) considering that the state of the control is known at time tn. The aforementioned statement can literally be translated as the number of bits (for example, the size of a digital file) that are required on average to obtain perfect observability and controllability of the system. The amount of missing information (MI) to achieve perfect observability of the state J n is given by

$$ \text{MI}_O = (1 - O_J)H(\mathbf{J}^n) \quad (96) $$

Analogously, the amount of missing information for perfect controllability of the state J $^{n}$+1 is

$$ \text{MI}_C = (1 - C_J)H(\mathbf{J}^{n+1}) \quad (97) $$

For example, if the observability of the control is O$^{J}$ = 0.8 and the state J n has 120 megabytes of information, then the control requires 24 megabytes of additional information to unambiguously determine J n . A similar example applies to controllability. Another perspective on MI$^{O}$ and MI$^{C}$ is that they signify the minimum number of yes and no questions about the state J n that must be asked on average in order to attain perfect observability and controllability of the system, respectively.

# 3. Optimal control

Let us consider the quantity of interest J $^{n}$+1 with mean vector and covariance matrix given by

$$\mathbb{E}[J^{n+1}] = \mu, \quad (98a)$$

$$\text{var}[J^{n+1}] = \mathbb{E}[(J^{n+1} - \mathbb{E}[J^{n+1}])(J^{n+1} - \mathbb{E}[J^{n+1}])^T] = \Xi, \quad (98b)$$

![](_page_24_Figure_1.jpeg)

FIG. 14: Sketch of the of the probability mass functions illustrating the effect of the transformation in Eq. (99b) and the relaxation factors, α$^{µ}$ and αξ.

where $^{E}$[·] is the expectation operator and superindex T means transpose. The system is controlled by the tandem sensor–actuator (S n ,A n ) characterized by the parametrization θ. Let us define the control task as the modification of the moments of J $^{n}$+1 in Eq. (98) and denote by $^{µ}$$^{ˆ}$ and $^{Ξ}$b the targeted (i.e., desired) mean and variance for $^{J}$ n+1 , respectively. The goal of the control is to drive the system to the optimal state J ∗ , with mean µ ∗ and variance Ξ ∗ , as close as possible to $^{µ}$$^{ˆ}$ and $^{Ξ}$b, respectively, using the controller with optimal parameters $^{\theta}$ ∗ . The search for the optimal control parameters can be posed as the reduction in uncertainty of the controlled state given the information collected by the sensors and the action performed by the actuators. The latter is formulated as the minimization of Kullback-Leibler divergence between J $^{n}$+1 and an auxiliary state, $^{J}$b, constructed by shifting the mean of $^{J}$ $^{n}$+1 to µˆ and scaling its variance to $^{Ξ}$b. Then, the optimal information-theoretic controller is attained for

$$\theta^* = \arg \min_{\theta} \text{KL}(\mathcal{J}^{n+1}, \mathcal{J}), \quad (99a)$$

$$\begin{aligned} & \arg \min_{\theta} \text{KL}(\mathbf{J}^{n+1}, \hat{\mathbf{J}}), & (99a) \\ \hat{\mathbf{J}} &= \mathbf{a}\mathbf{J}^{n+1} + \mathbf{b}, & (99b) \end{aligned}$$

with

$$a_{ij}^2 = \frac{\widehat{\Xi}_{ij}}{\mathbb{E}[(J_i^{n+1} - \mu_i)(J_j^{n+1} - \mu_j)]}, \quad \mathbf{b} = \hat{\mu} - a\boldsymbol{\mu}.$$

The role of the matrix a and the vector b is to transform the probability distribution of J $^{n}$+1 into the distribution $^{J}$b

such that $^{E}$[Jb] = $^{µ}$$^{ˆ}$ and var[Jb] = $^{Ξ}$b. The optimization method posed in Eq. (99) can be simplified by decomposing the controller parameters space into three independent sets θ = [θ$^{s}$ θ$^{p}$ θa], where θ$^{s}$ are the sensor parameters (mainly, the sensor locations), θ$^{p}$ are the passive actuator parameters (i.e., those that do not directly modify the state of the system, such as the actuator locations), and θ$^{a}$ are the active actuator parameters (that act on the state of the system, such as the actuator amplitude, frequency, etc.). The parameters θ$^{s}$ and θ$^{p}$ can be optimized to enhance observability and controllability, respectively. It was shown in §VI A 2 that observability and controllability improve with the mutual information shared among the state variable J n and the controller state. With this insight, the optimization problem can be simplified as the following iterative process:

- 1. For a given iteration, i, assume θ$^{a}$ fixed and solve for θ$^{s}$ and θp,

$$\theta_s \leftarrow \arg \max_{\theta} I(\mathbf{J}^n; \mathbf{S}^n), \quad (100a)$$

$$\theta_p \leftarrow \arg \max_{\theta_p} I(\mathbf{J}^n; \mathbf{A}^n). \quad (100b)$$

The initial guess for θ$^{s}$ and θ$^{p}$ can be obtained from the uncontrolled system, θ$^{a}$ = 0.

- 2. Using the values of θ$^{s}$ and θ$^{p}$ from the previous optimization, solve for θ$^{a}$ as

$$\theta_a \leftarrow \arg \min_{\theta_a} \text{KL}(\mathbf{J}^{n+1}, \hat{\mathbf{J}}), \quad (101)$$

- 3. Repeat steps 1 and 2 while KL$^{i}$ < KL$^{i}$−$^{1}$ , being KL$^{i}$ = KL(J n+1 , $^{J}$b) computed at iteration $^{i}$.

To further facilitate the optimization, step 3 can be aided by introducing relaxation factors such that,

$$\mathbb{E}[\hat{J}] = (1 - \alpha_\mu)\hat{\mu} + \alpha_\mu\mu, \quad \text{var}[\hat{J}] = (1 - \alpha_\xi)\hat{\Xi} + \alpha_\xi\Xi. \quad (102)$$

$^{E}$[Jb] = (1 $^{−}$ $^{α}$µ)µ$^{ˆ}$ $^{+}$ $^{α}$µµ, var[Jb] = (1 $^{−}$ $^{α}$ξ)Ξb $^{+}$ $^{α}$ξΞ. (102) within each iteration. These relaxation factors are within the range 0 < αµ, α$^{ξ}$ ≤ 1 during the optimization, taking the limits α$^{µ}$ → 0 and α$^{ξ}$ → 0 as the iterations advance. The optimization procedure outlined above is algorithmically appealing, as it can be performed using gradient ascent/descent methods such as in reinforcement learning. One application of Eqs. (100) and (101) is discussed in §VI B for optimal control for drag reduction in wall turbulence.

Other variants of the optimization problem can be formulated to accommodate different cost functionals. For example, we might be interested in completely specifying a targeted probability distribution for J $^{n}$+1 (i.e., control acting over all the moments of J $^{n}$+1). In that case, the rescaling described in Eq. (99b) is not needed and the optimization problem is posed as

$$ \theta^* = \arg \min_{\theta} K(\mathbf{J}^{n+1}, \mathbf{J}_{\text{ref}}) \quad (103) $$

where Jref is the prescribed (and thus known) probability distribution that we aim to attain for the state J $^{n}$+1. The optimization in Eq. (103) provides the control parameters that minimize the error between the probability distribution of J $^{n}$+1 and $^{J}$ref in terms of the L$^{1}$ norm.

#### B. Application: Opposition control for drag reduction in turbulent channel flows

The enhanced transport of mass, momentum, and heat by turbulent flows has a significant impact on the design and performance of thermofluid systems. As such, the need of efficient control strategies to manipulate turbulent flows remains an ubiquitous task in numerous engineering applications. Examples of turbulent flow control can be found in drag reduction for airfoils and pipelines, and enhanced mixing for combustor chambers and heat exchangers, to name a few examples. Given its technological importance, flow control remains a field of active research, and many control strategies have been devised with different degree of success \[135\]. In the present section, we consider an application of opposition control for drag reduction in a turbulent channel flow, where flow is actively modified at the wall to attenuate turbulence and reduce drag \[136,] [137\]. The optimal control strategy is found using the information-theoretic tools described in §VI A 3.

The flow configuration considered is an incompressible turbulent channel flow see section 7.1 in [97\] comprising the flow confined between two parallel walls separated by a distance 2δ as shown in figure 15a. The streamwise, wall-normal, and spanwise directions are denoted by x, y, and z, respectively, and the corresponding velocities are u, v, and w. The flow is driven by imposing a constant mass flux in the streamwise direction which is identical for both the uncontrolled and controlled cases. The bottom and top walls are located at y = 0δ and y = 2δ, respectively. The size of the computational domain is πδ × 2δ × πδ/2, in the streamwise, wall-normal, and spanwise directions, respectively. The Reynolds number is Re = Ubulkδ/ν ≈ 3200, where ν is the kinematic viscosity and Ubulk is the mean streamwise velocity. The flow is calculated by direct numerical simulation of the incompressible Navier-Stokes equations in which all the scales of the flow are resolved. The code employed to perform the simulations was presented and validated in previous studies \[36,] [138][–140\]. In all the simulations, the domain is discretized into 64 × 90 × 64 grid points in the x, y, and z directions, respectively, which yields a total number of 368,640 degrees of freedom. The time step of the simulation is fixed to ∆t $^{+}$ ≈ 5 × 10−$^{3}$ , where + denotes non-dimensionalization by ν and the friction velocity uτ,u = p ν∂hui/∂y|$^{w}$ for the uncontrolled case. The operator $\langle \cdot \rangle$ signifies average in x, z, and time, and the subscript w denotes quantities evaluated at the wall.

Opposition control is a drag reduction technique based on blowing and sucking fluid at the wall with a velocity opposed to the velocity measured at some distance from the wall. In the case of a channel flow, the measured velocity is located in a wall-parallel plane at a distance y$^{s}$ from the wall referred to as the sensing plane. Figure 15b provides an schematic of the problem setup for opposition control in a turbulent channel flow. The optimization problem consists of finding the wall-normal distance of the sensing plane and the blowing/suction velocity of the actuator. We consider a prescribed law for the actuator such that the blowing/suction velocity at the wall is proportional to the measured velocity in the sensing plane. The instantaneous wall-normal velocity at the wall in the controlled case is given by

$$v(x, 0, z) = -\beta v(x, y_s, z), \quad (104)$$

where β is the blowing intensity. The controller parameter vector is θ = [θs, θa] = [ys, β], and Eqs. (79) and (80) take the form of S $^{k}$ = v(x, ys, z) and A$^{k}$ = −βS$^{k}$ , respectively, at times t$^{k}$ = t$^{n}$ and t$^{k}$ = tn+1. A control law equivalent to Eq. (104) is applied at the top wall.

![](_page_26_Figure_1.jpeg)

FIG. 15: (a) Sketch of a channel flow. The mean velocity is in the streamwise (x) direction. (b) Schematic of the opposition control technique. The contour corresponds to the instantaneous vertical velocity on a z-plane. Colormap ranges from (red) v $^{+}$ = −3.6 to (blue) 3.6.

The quantity to be controlled is the mean wall shear stress (i.e., the drag) in the statistically steady state of the controlled channel flow, denoted by J $^{n}$+1 = τw. The analysis is conducted considering two states: the state with no actuation, J $^{n}$, and the final statistically steady state, J $^{n}$+1, after actuation has been applied for a period of time equal to ∆t $^{+}$ = 60. The targeted mean and standard deviation of J $^{n}$+1 in the controlled state are set to ˆµ $^{+}$ = 0 and $^{Ξ}$b1/$^{2}$ $^{≈}$ $^{0}$.1hτw,ui, where $^{h}$τw,u$^{i}$ is the mean wall-shear stress of the uncontrolled case. The auxiliary probability

distribution $^{J}$bn+1 is defined as in Eq. (99b) using ˆ$^{µ}$ and Ξ. b Several methods are available for the optimization problem posed in §VI A 3. In our case, a simply gradient descent algorithm was sufficient to find the optimal state. The optimum parameters in Eq. (100a) and Eq. (101) are respectively computed iteratively as

$$\begin{aligned} \theta_s &\leftarrow \theta_s + \gamma \nabla I(S^{n+1}; J^{n+1}), \\ \theta_a &\leftarrow \theta_a - \gamma \nabla \text{KL}(J^{n+1}; \hat{J}), \end{aligned}$$

n+1; Jb), where here n + 1 represents successive controlled states, γ is the step size computed as in Barzilai and Borwein \[141\], and the gradient is numerically computed using forward finite differences. The parametric space is bounded by θ$^{s}$ ≡ y + $^{s}$ ∈ [0, 180] (for the bottom wall) and θ$^{a}$ ≡ β ∈ [−0.1, 1.1]. Values of β larger than 1 were found to be unstable, consistently with the findings in Chung and Talha \[142\]. The iteration process is started by finding the optimal sensor in the uncontrolled state and setting β = 0. The best location of the sensing plane before actuation is found to be y + $^{s}$ $^{≈}$ 9.65. The iterative process is then continued following the steps in §VI A 3. To aid the optimization, $^{α}$$^{µ}$ and α$^{ξ}$ in Eq. (102) are initially set to 0.6 and gradually decreased within each iteration. The optimal control is found at y +∗ $^{s}$ ≈ 13.9 and β ∗ = 1. Remarkably, our optimal control coincides with the global optimum reported by Chung and Talha \[142\], who performed a parametric study varying y$^{s}$ and β in a flow setup identical to the one presented here.

In terms of drag, the optimal control provides ≈ 26% reduction with respect to the uncontrolled state. A similar value was reported by other authors \[136,] [137,] [142\], which is expected since our control parameters are similar. However, it is important to remark that the methodology adopted here radically differs from the approach followed in the aforementioned references: instead of conducting simulations using a trial and error approach to find the optimal parameters, here we rely on the information-theoretic principles introduced in §VI.

For a more quantitative perspective, Figure 16a displays the probability mass distribution of the wall shear-stress for the uncontrolled state and optimally controlled state. It can be readily seen that both the mean and the standard deviation are smaller for the case with the optimal control. Similarly, figure 16b (left) shows that the Kullback-Leibler divergence is lower for the controlled case with optimal parameters than for the uncontrolled case. Figure 16b (right) depicts the mutual information between the wall shear stress and the wall-normal velocity at the sensing plane for the optimal sensor location, y ∗,k s for the uncontrolled state (k = n) and controlled state (k = n + 1). Interestingly, the mutual information is larger for the actuated state, arguably because the wall shear stress in the actuated case is more correlated with the imposed velocity at the wall.

![](_page_27_Figure_1.jpeg)

FIG. 16: (a) Probability mass distributions of the wall shear stress for the ( ) uncontrolled state (k = n) and the ( ) controlled state (k = n + 1). The line styles are ( ) for actual wall shear stress distribution (J k ) and ( ) for the auxiliary state (Jb$^{k}$ ). (b) KL divergence between the final state and the auxiliary state (left); and Mutual information between the sensor location and the state (right), normalized with the entropy of the uncontrolled state.

![](_page_27_Figure_3.jpeg)

FIG. 17: Instantaneous tangential Reynolds stress u 0v 0 at $y^+$ ≈ 10 for (a) uncontrolled state and (b) optimally controlled state. The colormap ranges from u 0v 0/u$^{2}$ τ,u = −6.8 (blue) to 6.8 (red).

Finally, to provide additional insight into the effect of the actuation on the flow, figure 17 shows the tangential Reynolds stresses u 0v 0 (where prime denotes fluctuations about the mean value) at y + $^{s}$ ≈ 10 for the uncontrolled and controlled states. It can be appreciated that the intensity of the tangential Reynolds stresses is lower for the case with optimal control, indicating a suppression of vortical structures near the wall.

# VII. CONCLUSIONS

The problems of causality, reduced-order modeling, and control for chaotic, high-dimensional dynamical systems have been formulated within the framework of information theory. In the proposed formalism, the state of the dynamical system is considered a random variable in which its information (i.e., Shannon entropy) quantifies the average number of bits to univocally determinate its value. A key quantity for the formalization of the theory is the conditional information, which measures the uncertainty in the state of the system given the partial knowledge of other states. In contrast to the equation-centered formulation of dynamical systems, where individual trajectories are the object of analysis, information theory offers a more natural approach to the investigation of chaotic systems from the viewpoint of the probability distributions of the states.

We have argued that statistical asymmetries in the information flux within the states of the system can be leveraged to measure causality among variables. As such, the information-theoretic causality from one variable to another is quantified as the information flux from the former to the latter. Our definition of causality is motivated by the information required to attain total knowledge of a future state and can be interpreted as how much the past information of the system improves our knowledge of the future state. The formulation of causality proposed here is grounded on the zero conditional-entropy condition for deterministic systems and generalizes to multiple variables the definition of causality by Schreiber \[72\]. The quantification of causality proposed also accounts for the information flux due to the joint effect of variables, which was absent in previous formulations. We have also introduced the information leak as the amount of information unaccounted for by the observable variables.

Reduced-order modeling of chaotic systems has been posed as a problem of conservation of information: modeled systems contain a smaller number of degrees of freedom than the original system, which in turn entails a loss of information. Thus, the primary goal of modeling is to preserve the maximum amount of useful information from the original system. We have derived the conditions for maximum information-preserving models and shown that accurate models must maximize the mutual information between the model state and the true state, and minimize the Kullback-Leibler divergence between their probabilities. The mutual information assists the model to reproduce the dynamics of the original system, while the Kullback-Leibler divergence enables the accurate prediction of the statistical quantities of interest.

Lastly, control theory has been cast in information-theoretic terms by envisioning the controller as a device aimed at reducing the uncertainty in the future state of the system to be controlled given the information collected by the sensors and the action performed by the actuators. We have reformulated the concepts of controllability and observability using mutual information between the present and future states. The definitions of open- and closedloop control have also been introduced based on the information shared between the actuator and the system state. The optimization problem was posed as the minimization of the Kullback-Leibler divergence between the probability distribution of the controlled state and a targeted state derived from the latter.

We have applied our information-theoretic framework to advance three outstanding problems in the causality, modeling, and control of turbulent flows. Information-theoretic causal inference was used to measure the information flux of the turbulent energy cascade in isotropic turbulence. The principle of maximum conservation of information was leveraged to devise a subgrid-scale model for large-eddy simulation of isotropic turbulence. Finally, informationtheoretic control was utilized to achieve optimal drag reduction in wall-bounded turbulence using opposition control at the wall. Overall, information theory offers an elegant formalization of the problems of causality, modeling, and control for chaotic, high-dimensional systems, aiding physical interpretation and easing the tasks of modeling and control all within one unified framework.

# VIII. ACKNOWLEDGMENTS

This work was supported by the National Science Foundation under Grant No. 032707-00001. G. A. was partially supported by STTR with Cascade Technologies, Inc. and the Naval Air Systems Command. The authors acknowledge the MIT SuperCloud and Lincoln Laboratory Supercomputing Center for providing HPC resources that have contributed to the research results reported within this paper.

[1] C. E. Shannon, [Bell Syst. Tech. J](https://doi.org/10.1002/j.1538-7305.1948.tb01338.x) 27, 379 (1948). [2] T. M. Cover and J. A. Thomas, Elements of Information Theory (Wiley-Interscience, USA, 2006). [3] R. Landauer, [Phys. Lett. A](https://doi.org/10.1016/0375-9601(96)00453-7) 217, 188 (1996). [4] R. Landauer, Physics Today 44, 23 (1991). [5] L. Brillouin, Science and information theory (Courier Corporation, 2013). [6] L. Susskind, The theoretical minimum: what you need to know to start doing physics, 1st ed. (Basic Books, New York, 2014). [7] A. S. Eddington, The nature of the physical world, 1st ed. (Cambridge University Press, 1929). [8] G. Berkooz, P. Holmes, and J. L. Lumley, [Annu. Rev. Fluid Mech.](https://doi.org/10.1146/annurev.fl.25.010193.002543) 25, 539 (1993). [9] P. J. Schmid, [Annu. Rev. Fluid Mech.](https://doi.org/10.1146/annurev.fluid.38.050304.092139) 39, 129 (2007). [10] C. W. Rowley and S. T. M. Dawson, [Annu. Rev. Fluid Mech.](https://doi.org/10.1146/annurev-fluid-010816-060042) 49, 387 (2017). [11] K. Duraisamy, G. Iaccarino, and H. Xiao, [Ann. Rev. Fluid Mech.](https://doi.org/10.1146/annurev-fluid-010518-040547) 51, 357 (2019). [12] S. L. Brunton, B. R. Noack, and P. Koumoutsakos, [Ann. Rev. Fluid Mech.](https://doi.org/10.1146/annurev-fluid-010719-060214) 52, 477 (2020). [13] C. Meneveau and J. Katz, [Annu. Rev. Fluid Mech.](https://doi.org/10.1146/annurev.fluid.32.1.1) 32, 1 (2000). [14] U. Piomelli and E. Balaras, [Annu. Rev. Fluid Mech.](https://doi.org/10.1146/annurev.fluid.34.082901.144919) 34, 349 (2002).

[15] S. T. Bose and G. I. Park, [Annu. Rev. Fluid Mech.](https://doi.org/10.1146/annurev-fluid-122316-045241) 50, 535 (2018). [16] C. G. Speziale, Annu. Rev. Fluid Mech. 23, 107 (1991). [17] M. H. Silvis, R. A. Remmerswaal, and R. Verstappen, Phys. Fluids 29, 015105 (2017). [18] J. Slotnick, A. Khodadoust, J. Alonso, D. Darmofal, W. Gropp, E. Lurie, and D. Mavriplis, Cfd vision 2030 study: a path to revolutionary computational aerosciences (2014). [19] M. Gad-el-Hak, [Flow Control: Passive, Active, and Reactive Flow Management](https://doi.org/10.1017/CBO9780511529535) (Cambridge University Press, 2000). [20] T. R. Bewley, P. Moin, and R. Temam, [J. Fluid Mech.](https://doi.org/10.1017/S0022112001005821) 447, 179 (2001). [21] M. D. Gunzburger, Perspectives in Flow Control and Optimization (Society for Industrial and Applied Mathematics, 2002). [22] J. Kim, Phys. Fluids 15, 1093 (2003). [23] S. S. Collis, R. D. Joslin, A. Seifert, and V. Theofilis, [Prog. Aerosp. Sci.](https://doi.org/10.1016/j.paerosci.2004.06.001) 40, 237 (2004). [24] J. Kim and T. R. Bewley, [Annu. Rev. Fluid Mech.](https://doi.org/10.1146/annurev.fluid.39.050905.110153) 39, 383 (2007). [25] P. J. Schmid and D. S. Henningson, Stability and Transition in Shear Flows (Springer New York, 2012). [26] B. J. McKeon, [J. Fluid Mech.](https://doi.org/10.1017/jfm.2017.115) 817, P1 (2017). [27] A. Zare, T. T. Georgiou, and M. Jovanovi´c, [Annu. Rev. Control Robot. Auton. Syst.](https://doi.org/10.1146/annurev-control-053018-023843) 3, 195 (2020). [28] M. R. Jovanovi´c, Annu. Rev. Fluid Mech. 53, 311 (2021). [29] R. King, M. Seibold, O. Lehmann, B. R. Noack, M. Morzy´nski, and G. Tadmor, in Control and Observer Design for Nonlinear Finite and Infinite Dimensional Systems, edited by T. Meurer, K. Graichen, and E. D. Gilles (Springer, Berlin, Heidelberg, 2005) pp. 369–386. [30] D. M. Luchtenburg, K. Aleksi´c, M. Schlegel, B. R. Noack, R. King, G. Tadmor, B. G¨unther, and F. Thiele, in Active Flow Control II, edited by R. King (Springer, Berlin, Heidelberg, 2010) pp. 341–356. [31] K. Aleksic, M. Luchtenburg, R. King, B. Noack, and J. Pfeifer, in [5th Flow Control Conference](https://doi.org/10.2514/6.2010-4833) (American Institute of Aeronautics and Astronautics, 2010). [32] J. Pearl, Causality: Models, Reasoning and Inference, 2nd ed. (Cambridge University Press, New York, NY, USA, 2009). [33] G. Tissot, A. Lozano-Dur´an, J. Jim´enez, L. Cordier, and B. R. Noack, [J. Phys. Conf. Ser](https://doi.org/10.1088/1742-6596/506/1/012006) 506, 012006 (2014). [34] X. S. Liang and A. Lozano-Dur´an, CTR - Proc. Summer Prog. , 233 (2016). [35] A. Lozano-Dur´an, H. J. Bae, and M. P. Encinar, [J. Fluid Mech.](https://doi.org/10.1017/jfm.2019.801) 882, A2 (2019). [36] A. Lozano-Dur´an, N. C. Constantinou, M.-A. Nikolaidis, and M. Karp, [J. Fluid Mech.](https://doi.org/10.1017/jfm.2020.902) 914, A8 (2021). [37] J. Jim´enez, [J. Fluid Mech.](https://doi.org/10.1017/jfm.2018.144) 842, P1 (2018). [38] J. I. Cardesa, A. Vela-Mart´ın, S. Dong, and J. Jim´enez, Phys. Fluids 27[, 111702 (2015).](https://doi.org/10.1063/1.4935812) [39] H. Choi and P. Moin, Phys. Fluids 2[, 1450 (1990).](https://doi.org/10.1063/1.857593) [40] J. M. Wallace, [Theor. Appl. Mech. Lett.](https://doi.org/https://doi.org/10.1063/2.1402203) 4, 022003 (2014). [41] M. Wilczek, R. J. Stevens, and C. Meneveau, J. Fluid Mech. 769 (2015). [42] R. de Kat and B. Ganapathisubramani, [J. Fluid Mech.](https://doi.org/10.1017/jfm.2015.558) 783, 166 (2015). [43] G. He, G. Jin, and Y. Yang, Annu. Rev. Fluid Mech. 49, 51 (2017). [44] H.-N. Wang, W.-X. Huang, and C.-X. Xu, Phys. Fluids 32[, 125103 (2020).](https://doi.org/10.1063/5.0028956) [45] H. Beebee, C. Hitchcock, and P. Menzies, The Oxford Handbook of Causation (OUP Oxford, 2012). [46] R. Betchov, Phys. Fluids 7[, 1160 (1964).](https://doi.org/10.1063/1.1711356) [47] R. T. Cerbus and W. I. Goldburg, Phys. Rev. E 88[, 053012 (2013).](https://doi.org/10.1103/PhysRevE.88.053012) [48] R. T. Cerbus, Information perspective on turbulence, Ph.D. thesis, University of Pittsburgh (2014). [49] M. Materassi, G. Consolini, N. Smith, and R. De Marco, Entropy 16[, 1272 (2014).](https://doi.org/10.3390/e16031272) [50] C. Granero-Belinch´on, S. G. Roux, and N. B. Garnier, [EPL (Europhysics Letters)](https://doi.org/10.1209/0295-5075/115/58003) 115, 58003 (2016). [51] C. Granero-Belinch´on, S. G. Roux, and N. B. Garnier, Phys. Rev. E 97[, 013107 (2018).](https://doi.org/10.1103/PhysRevE.97.013107) [52] C. Granero-Belinchon, Multiscale Information Transfer in Turbulence, Theses, Universit´e de Lyon (2018). [53] C. Granero-Belinch´on, S. G. Roux, and N. B. Garnier, Entropy 23[, 1609 (2021).](https://doi.org/10.3390/e23121609) [54] W. Wang, X. Chu, A. Lozano-Dur´an, R. Helmig, and B. Weigand, [J. Fluid Mech.](https://doi.org/10.1017/jfm.2021.445) 920, A21 (2021). [55] M. Shavit and G. Falkovich, Phys. Rev. Lett. 125[, 104501 (2020).](https://doi.org/10.1103/PhysRevLett.125.104501) [56] T.-W. Lee, [Eur. J. Mech. B Fluids](https://doi.org/10.1016/j.euromechflu.2021.01.011) 87, 128 (2021). [57] D. J. C. MacKay, Information Theory, Inference & Learning Algorithms (Cambridge University Press, USA, 2002). [58] L. Boltzmann, Mathematisch-Naturwissen Classe. Abt. II, LXXVI 76, 373 (1877). [59] E. T. Jaynes, Phys. Rev. 106, 620 (1957). [60] J. V. Stone, Information Theory: A Tutorial Introduction (2013). [61] R. Shaw, [Zeitschrift f¨ur Naturforschung A](https://doi.org/10.1515/zna-1981-0115) 36, 80 (1981). [62] T. DelSole, J. Atmos. Sci. 61, 2425 (2004). [63] P. Garbaczewski, J. Stat. Phys. 123, 315 (2006). [64] X. S. Liang and R. Kleeman, Phys. Rev. Lett. 95, 244101 (2005). [65] R. Kleeman, Entropy 13, 612 (2011). [66] C. Beck and F. Sch¨ogl, Thermodynamics of chaotic systems: an introduction, 4 (1995). [67] M. Eichler, Philos. Trans. R. Soc. A-Math. Phys. Eng. Sci. 371, 20110613 (2013). [68] N. Wiener, The theory of prediction, modern mathematics for engineers (McGraw-Hill, 1956). [69] C. W. J. Granger, Econometrica , 424 (1969). [70] J. Massey, in Proc. Int. Symp. Inf. Theory Applic.(ISITA-90) (Citeseer, 1990) pp. 303–305. [71] G. Kramer, Directed information for channels with feedback, Ph.D. thesis, ETH Z¨urich (1998). [72] T. Schreiber, Phys. Rev. Lett. 85, 461 (2000).

[73] X. S. Liang and R. Kleeman, Phys. Rev. Lett. 95[, 244101 (2006).](https://doi.org/10.1103/PhysRevLett.95.244101) [74] S. Sinha and U. Vaidya, in [IEEE 55th Conference on Decision and Control (CDC)](https://doi.org/10.1109/CDC.2016.7799401) (2016) pp. 7329–7334. [75] R. W. Yeung, IEEE Trans. Inf. Theory 37, 466 (1991). [76] A. J. Bell, in Proceedings of the Fifth International Workshop on Independent Component Analysis and Blind Signal Separation: ICA (Citeseer, 2003). [77] A. Kaiser and T. Schreiber, Physica D 166[, 43 (2002).](https://doi.org/https://doi.org/10.1016/S0167-2789(02)00432-3) [78] P. Duan, F. Yang, T. Chen, and S. L. Shah, [IEEE Trans. Control Syst. Technol.](https://doi.org/10.1109/TCST.2012.2233476) 21, 2052 (2013). [79] R. G. James, N. Barnett, and J. P. Crutchfield, Phys. Rev. Lett. 116, 238701 (2016). [80] L. F. Richardson, Weather Prediction by Numerical Process (Cambridge University Press, 1922). [81] A. M. Obukhov, Izv. Akad. Nauk USSR, Ser. Geogr. Geofiz. 5, 453 (1941). [82] A. N. Kolmogorov, in Dokl. Akad. Nauk SSSR, Vol. 30 (1941) pp. 301–305. [83] A. N. Kolmogorov, [J. Fluid Mech.](https://doi.org/10.1017/S0022112062000518) 13, 82 (1962). [84] T. Aoyama, T. Ishihara, Y. Kaneda, M. Yokokawa, K. Itakura, and A. Uno, J. Phys. Soc. Jpn. 74, 3202 (2005). [85] G. Falkovich, J. Phys. A 42[, 123001 (2009).](https://doi.org/10.1088/1751-8113/42/12/123001) [86] J. I. Cardesa, A. Vela-Mart´ın, and J. Jim´enez, Science 357, 782 (2017). [87] D. Veynante and L. Vervisch, Prog. Energy Combust. Sci. 28, 193 (2002). [88] E. Bodenschatz, Science 350[, 40 (2015).](https://doi.org/10.1126/science.aad1386) [89] R. M. B. Young and P. L. Read, Nat. Phys. 13, 1135 (2017). [90] L. Sirovich and S. Karlsson, Nature 388, 753 (1997). [91] B. Hof, A. De Lozar, M. Avila, X. Tu, and T. M. Schneider, Science 327[, 1491 (2010).](https://doi.org/10.1126/science.1186091) [92] I. Marusic, R. Mathis, and N. Hutchins, Science 329[, 193 (2010).](https://doi.org/10.1126/science.1188765) [93] J. K¨uhnen, B. Song, D. Scarselli, N. B. Budanur, M. Riedl, A. P. Willis, M. Avila, and B. Hof, Nat. Phys. 14[, 386 (2018).](https://doi.org/10.1038/s41567-017-0018-3) [94] J. G. Ballouz and N. T. Ouellette, J. Fluid Mech. 835[, 1048 (2018).](https://doi.org/10.1017/jfm.2017.802) [95] Torroja, Turbulent flow databases, <https://torroja.dmt.upm.es/turbdata/> (2021), [Online; accessed April-2021]. [96] C. Rosales and C. Meneveau, Phys. Fluids 17, 095106 (2005). [97] S. B. Pope, Turbulent Flows (Cambridge University Press, 2000). [98] H. Akaike, IEEE Trans. Autom. Control 19, 716 (1974). [99] H. Akaike, in Applications of statistics, edited by P. R. Krishnaiah (1977). [100] H. Akaike, in Selected papers of Hirotugu Akaike (Springer, 1998) pp. 199–213. [101] S. Kullback and R. A. Leibler, Ann. Math. Stat. 22, 79 (1951). [102] Y. Baram and N. Sandell, IEEE Trans. Autom. Control 23, 61 (1978). [103] P. M. Lenggenhager, D. E. G¨okmen, Z. Ringel, S. D. Huber, and M. Koch-Janusz, Phys. Rev. X 10, 011037 (2020). [104] M. Giulini, R. Menichetti, M. S. Shell, and R. Potestio, J. Chem. Theory Comput. 16, 6795 (2020). [105] K. P. Burnham and D. R. Anderson, Model selection and multimodel inference: A practical information-theoretic approach, 2nd ed. (Springer, 2002). [106] D. R. Anderson, Model based inference in the life sciences: a primer on evidence (Springer, 2008). [107] R. S. Sutton and A. G. Barto, Reinforcement learning: An introduction (MIT press, 2018). [108] S. Still, EPL (Europhysics Letters) 85, 28005 (2009). [109] P. A. Ortega and D. A. Braun, [P. R. Soc. A-Math. Phys. Eng. Sci.](https://doi.org/10.1098/rspa.2012.0683) 469, 20120683 (2013). [110] D. Russo and B. Van Roy, J. Mach. Learn. Res. 17, 2442 (2016). [111] F. Leibfried, J. Grau-Moya, and H. Bou-Ammar, arXiv preprint arXiv:1708.01867 (2017). [112] M. Koch-Janusz and Z. Ringel, Nat. Phys. 14, 578 (2018). [113] X. Lu and B. Van Roy, arXiv preprint arXiv:1911.09724 (2019). [114] A. Hobson and B.-K. Cheng, J. Stat. Phys. 7, 301 (1973). [115] E. S. Soofi, [J. Am. Stat. Assoc.](https://doi.org/10.1080/01621459.1994.10476865) 89, 1243 (1994). [116] T. Weissman, E. Ordentlich, G. Seroussi, S. Verdu, and M. J. Weinberger, Inequalities for the L$^{1}$ deviation of the empirical distribution, Tech. Rep. HPL-2003-97R1 (Hewlett-Packard Labs, Tech. Rep, 2003). [117] A. E. Abbas, A. H Cadenbach, and E. Salimi, Entropy 19, 232 (2017). [118] P. Sagaut and C. Meneveau, Large Eddy Simulation for Incompressible Flows: An Introduction (Springer, 2006). [119] W. K. Yeo, A generalized high pass/low pass averaging procedure for deriving and solving turbulent flow equations, Ph.D. thesis, The Ohio State University (1987). [120] D. Carati, G. S. Winckelmans, and H. Jeanmart, J. Fluid Mech. 441, 119 (2001). [121] H. J. Bae and A. Lozano-Dur´an, Center for Turbulence Research, Annual Research Briefs 2017, 207 (2017). [122] H. J. Bae and A. Lozano-Dur´an, Center for Turbulence Research, Annual Research Briefs 2018, 197 (2018). [123] M. Germano, Phys. Fluids 29[, 1755 (1986).](https://doi.org/10.1063/1.865649) [124] M. Lesieur, Turbulence in Fluids (Springer, 2008). [125] T. S. Lund and E. A. Novikov, Center for Turbulence Research, Annual Research Briefs 1992, 27 (1992). [126] H. L. Weidemann, in [Advances in Control Systems](https://doi.org/10.1016/B978-1-4831-6713-8.50011-7), Advances in Control Systems, Vol. 7, edited by C. T. Leondes (1969) pp. 225–255. [127] G. N. Saridis, [IEEE Trans. Autom. Control](https://doi.org/10.1109/9.1287) 33, 713 (1988). [128] Y. A. Tsai, F. A. Casiello, and K. A. Loparo, [IEEE Trans. Autom. Control](https://doi.org/10.1109/9.148379) 37, 1083 (1992). [129] S. Tatikonda and S. Mitter, [IEEE Trans. Autom. Control](https://doi.org/10.1109/TAC.2004.831187) 49, 1056 (2004). [130] H. Touchette and S. Lloyd, Physica A 331[, 140 (2004).](https://doi.org/10.1016/j.physa.2003.09.007) [131] J.-C. Delvenne and H. Sandberg, in [52nd IEEE Conference on Decision and Control](https://doi.org/10.1109/CDC.2013.6760357) (2013) pp. 3109–3114.

[132] P. Bania, [Int. J. Appl. Math. Comput. Sci.](https://doi.org/doi:10.34768/amcs-2020-0002) 30, 23 (2020). [133] J. M. R. Parrondo, J. M. Horowitz, and T. Sagawa, Nat. Phys 11[, 131 (2015).](https://doi.org/10.1038/nphys3230) [134] J. Chen, S. Fang, and H. Ishii, [Annu. Rev. Control](https://doi.org/10.1016/j.arcontrol.2019.03.011) 47, 155 (2019). [135] L. N. Cattafesta and M. Sheplak, Annu. Rev. Fluid Mech. 43, 247 (2011). [136] H. Choi, P. Moin, and J. Kim, [J. Fluid Mech.](https://doi.org/10.1017/S0022112094000431) 262, 75 (1994). [137] E. P. Hammond, T. R. Bewley, and P. Moin, Phys. Fluids 10[, 2421 (1998).](https://doi.org/10.1063/1.869759) [138] A. Lozano-Dur´an and H. J. Bae, Center for Turbulence Research, Annual Research Briefs , 97 (2016). [139] H. J. Bae, A. Lozano-Dur´an, S. T. Bose, and P. Moin, [Phys. Rev. Fluids](https://doi.org/10.1103/PhysRevFluids.3.014610) 3, 014610 (2018). [140] H. J. Bae, A. Lozano-Dur´an, S. T. Bose, and P. Moin, J. Fluid Mech. 859[, 400–432 (2019).](https://doi.org/10.1017/jfm.2018.838) [141] J. Barzilai and J. M. Borwein, [IMA J. Numer. Anal.](https://doi.org/10.1093/imanum/8.1.141) 8, 141 (1988). [142] Y. M. Chung and T. Talha, Phys. Fluids 23[, 025102 (2011).](https://doi.org/10.1063/1.3553278)