---
layout: blog-post
categories: blog
math: true
excerpt_separator: <!--more-->
title: "Towards Efficient Verification of Quantized Neural Networks"
author: Pei Huang
brief: "Towards Efficient Verification of Quantized Neural Networks by Pei Huang"
date: 2024-05-15
---

Deep neural networks (DNNs) have demonstrated striking and steadily improving capabilities across a wide range of tasks. Ongoing improvements to neural networks are typically achieved through a significant expansion in their scale. This escalation, however, frequently leads to substantial increases in computational cost, memory bandwidth requirements, and energy consumption, which make DNNs difficult to deploy on embedded systems with limited hardware resources. A promising approach for mitigating this difficulty is neural network quantization. 
<!--more-->
This technique replaces floating point arithmetic with integer arithmetic in deep models, enabling more efficient inference on devices with reduced power and memory requirements. As quantization has been employed in safety-critical scenarios, for example, in Tesla's FSD-chip, it is urgent to develop efficient and effective analysis methods that provide rigorous guarantees.


Therefore, we propose a method for formally verifying properties of quantized neural networks. This method has three components, offering different trade-offs between scalability and precision. More details can be found in [the paper that we recently published at AAAI 2024](https://ojs.aaai.org/index.php/AAAI/article/view/30108).

<div style="margin-top: 70px;"></div>

| ![](/assets/blog-images/2024-5-15-towards-efficient-verification-of-quantized-neural-networks/fig1.png) | 
|:--:| 
| *Figure 1: Main Framework* |

The baseline approach models neural networks and formal properties as integer linear programming (ILP) problems. ILP is an exact method in the sense that it guarantees both soundness (if it reports the system is safe, then it really is safe) and completeness (if the system really is safe, then it will report that it is safe).

<div style="margin-top: 70px;"></div>

| ![](/assets/blog-images/2024-5-15-towards-efficient-verification-of-quantized-neural-networks/fig2.png) | 
|:--:| 
| *Figure 2: An example of QNN workflow. The constant \\(s\\) (for “scale”) is an arbitrary real number. The constant \\(z\\) (for “zero point”) is an integer. The quantization operation is a mapping from a real number \\(\gamma\\) to an integer \\(q\\) of the form Quant: \\(q=Round(\frac{\gamma}{s}+z)\\), De-quant: \\(\gamma=s(q-z)\\). A number in the form of “I(F)” means that “I” is its integer representation and “F” is its corresponding fixed-point representation.* |

However, a precise method may encounter scalability issues on larger QNNs. To address this, we also design a gradient-based method for finding counterexamples. We use a rewriting trick for the non-differentiable round operation, which enables the backward process to cross through the round operation and gives us the desired gradient information. If this method finds a counterexample, then we immediately know that the property does not hold, without having to invoke the ILP solver.
 
Another component of the framework lies in between the first two. It relies on abstract interpretation-based reasoning to do an incomplete but formal analysis of the network.  We extend existing abstract interpretation-based interval analysis methods to support the semantics of "round" and "clip" operations in quantized neural networks. In particular, for the clip operation, we reduce it to a gadget built from two ReLU units. If the abstract interpretation approach succeeds, we know the property holds. Otherwise, the result of the analysis can be used to reduce the runtime of the ILP-based complete method.

<div style="margin-top: 70px;"></div>

| ![](/assets/blog-images/2024-5-15-towards-efficient-verification-of-quantized-neural-networks/fig3.png) | 
|:--:| 
| *Figure 3: Using two ReLUs to simulate Clip.* |

In summary, we propose an efficient verification framework for QNNs that offers different trade-offs between scalability and precision. Our verification tool EQV is the first formal verification tool that precisely captures the quantization scheme used in popular deep learning frameworks. Although we focus on verifying adversarial robustness, our method could be generalized to verify other properties of QNNs. Experimental results show that EQV is more efficient and scalable than previously existing approaches.


Pei Huang is a Postdoctoral Researcher advised by Clark Barrett in the Stanford Center for Automated Reasoning (Centaur) Lab and AI safety His work is focused on trustworthy AI.

#### [Pei Huang](https://profiles.stanford.edu/pei-huang) is a Postdoctoral Researcher advised by Clark Barrett in the Stanford Center for Automated Reasoning ([Centaur](https://centaur.stanford.edu/)) Lab and the [Stanford Center for AI Safety](https://aisafety.stanford.edu/). His work is focused on trustworthy AI.
