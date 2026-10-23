---
layout: blog-post
categories: blog
math: true
excerpt_separator: <!--more-->
title: "Pono 2.0: A Versatile SMT-Based Model Checker for Safety and Liveness"
author: Áron Ricardo Perez-Lopez
brief: "What's new in Pono 2.0, winner of the FM 2026 Best Tool Paper Award"
date: 2026-05-18
---
<!-- DRAFT: written from the FM 2026 paper for the author to review and revise before publishing. -->

[Pono](https://github.com/stanford-centaur/pono) is our open-source, SMT-based model checker. The paper describing its new major release, *Pono 2.0: A Versatile SMT-Based Model Checker for Safety and Liveness*, received the Best Tool Paper Award at the 27th International Symposium on Formal Methods (FM 2026) in Tokyo. In this post we give an overview of Pono and the major new features in version 2.0.
<!--more-->

## What Pono does

Model checking automatically determines whether a system, typically a hardware design or a piece of software, satisfies a temporal property. Early symbolic model checkers used binary decision diagrams; later, SAT-based methods took over thanks to their robustness and scalability. SMT solvers take this a step further. They let a model checker reason about systems at the *word level*, treating a 32-bit register as a single bit-vector instead of 32 separate bits, or a memory as an array of bit-vectors instead of individual wires, and they can also handle infinite-state systems over integers and reals.

Pono takes as input a transition system, given by a set of state variables, a formula describing the initial states, and a formula relating each state to its successor. It then checks either a *safety* property (every reachable state is good) or, new in version 2.0, a *liveness* property, i.e., something good eventually happens. (The name "Pono" is Hawaiian for proper, correct, or goodness.)

Pono is solver-agnostic. It talks to SMT solvers through [Smt-Switch](https://github.com/stanford-centaur/smt-switch), our uniform API for SMT solving. By default it uses Bitwuzla for solving and interpolation over bit-vectors and arrays and cvc5 for other theories. It can be used as a command-line tool or as a C++ library. Pono also provides Python bindings, including a [pySMT](https://github.com/pysmt/pysmt) front-end.

Pono is designed for three kinds of uses:

- **Push-button verification.** Several verification frameworks and industrial tool suites call Pono as a back-end model checker with no human involvement.
- **Expert verification.** Advanced users can use Pono's highly configurable command-line interface as well as its C++ and Python APIs to build and instrument transition systems and to control the verification process in fine detail.
- **Model-checking research.** Pono's modular architecture makes it a convenient platform for implementing and comparing new algorithms and solver configurations.

## What's new in 2.0

Since the original release in 2021, Pono has grown considerably. The highlights:

- **Liveness checking.** To our knowledge, Pono 2.0 is the first tool to verify liveness properties for systems in the BTOR2 format. It implements two standard reductions from liveness to safety. *Liveness-to-safety* (L2S) looks for a "lasso", a path that revisits a state, while *k-liveness* counts how often a fairness signal can fire. Pono extends k-liveness so that it can find counterexamples as well as proofs.
- **New interpolation-based engines.** Pono 2.0 adds *interpolation-sequence-based model checking* (ISMC) and *dual approximated reachability* (DAR), which complement the original interpolation-based algorithm (IMC). The IMC engine itself is improved too: it is now able to derive interpolants backward, which works better with incremental solving and tends to converge faster, and it keeps only the most recent interpolant when computing the next one.
- **Better bounded model checking and k-induction**, with options to control the step size, grow the bound exponentially, and pick the starting point of the unrolling. These options proved very useful for finding bugs.
- **More abstraction-refinement options.** Pono 2.0 integrates counterexample-guided abstraction refinement (CEGAR) with many more engines, and it can abstract expensive arithmetic operations using free variables as well as uninterpreted functions. Its counterexample-guided prophecy technique for arrays now also supports bit-vector indices, which are ubiquitous in hardware.
- **Witnesses from every engine.** Counterexample traces can now be exported from all engines, including the IC3-based and CEGAR-based ones.
- **A new VMT-LIB front end** in addition to BTOR2 and SMV, **data-driven parallel portfolios**, and updated solver back ends: cvc5 replaces CVC4, Bitwuzla (now with interpolation support) replaces Boolector as the default, and MathSAT5 supports incremental interpolation.

## How well does it work?

At the 2025 Hardware Model Checking Competition (HWMCC'25), Pono 2.0 won first place in the word-level array track. In that track it found the most counterexamples, proved the most instances that no other tool proved, and had 100% of its counterexample witnesses confirmed.

In the paper we also compare Pono 2.0 with its predecessor and with the state-of-the-art model checkers nuXmv, AVR, and rIC3:

- **Integer arithmetic:** On 796 VMT-LIB tasks, Pono 2.0 solved 783, ahead of both AVR and nuXmv, and it was the fastest tool on 551 of them.
- **Real arithmetic:** Pono 2.0's results were comparable to nuXmv's.
- **Bit-vectors:** Pono 2.0 solved far more tasks than Pono 1.0. On the SV-COMP-derived set it tied rIC3 for the most tasks solved and was the fastest tool on more tasks than any other.
- **Bit-vector arrays:** On HWMCC tasks, Pono 2.0 closely matched AVR. On the SV-COMP-derived set it beat both AVR and Pono 1.0, which it outperformed by a wide margin (132 tasks solved vs. 54).
- **Liveness:** On termination tasks from SV-COMP, Pono 2.0 outperformed AVR and Pono 1.0 on bit-vectors (behind only rIC3) and beat both of them on bit-vector arrays.

## Try it

Pono and Smt-Switch are released as open source software under the BSD 3-Clause license. You can [get Pono on GitHub](https://github.com/stanford-centaur/pono) or run the pre-built container image without compiling anything. Next on our roadmap are support for SystemVerilog designs, the MOXI input language, exporting correctness proofs as witness circuits, and newer liveness algorithms.

For the full story, read [the paper](https://doi.org/10.1007/978-3-032-26220-2_1).
