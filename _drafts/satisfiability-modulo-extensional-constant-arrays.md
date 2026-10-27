---
layout: blog-post
categories: blog
excerpt_separator: <!--more-->
title: "Satisfiability Modulo Extensional Constant Arrays"
author: Mathias Preiner and Aina Niemetz
brief: "A decision procedure for constant arrays over finite index domains, winner of a CAV 2026 Distinguished Paper Award"
date: 2026-07-26
---

Our paper **Satisfiability Modulo Extensional Constant Arrays** received a
Distinguished Paper Award at **CAV 2026** in Lisbon. It closes a long-standing gap
in SMT solving: deciding problems with *constant arrays*, arrays that hold the
same value at every index, when the index domain is finite, as it always is for
machine integers. In this post we explain why that case is tricky and what our
new procedure does about it.

<!--more-->

## Arrays, and arrays with a default value

Arrays are the natural model for memory in hardware and for array data
structures in software and therefore ubiquitous in hardware and software
verification. The SMT-LIB standard defines a theory of arrays with two
operations: *select* reads the element at an index, and *store* writes an
element at an index to produce a new array. The theory is *extensional*,
meaning that two arrays are equal exactly when they agree at every index.

What the standard theory cannot express succinctly is an array initialized with
a default value, for example, a zero-initialized block of memory.
Without a dedicated construct, this is usually encoded by writing the default
value explicitly to every relevant index with a long chain of stores.
However, that is both imprecise (only the indices you explicitly wrote are
covered) and inefficient (the store chains can get very deep).

Extending the standard theory with *constant arrays* closes this gap.
A constant array \\(\langle v \rangle\\) stores the value \\(v\\) at every
index, so reading it anywhere gives \\(v\\).
SMT solvers that support this extension accept the constant array construct
written as `((as const (Array I E)) v)` in SMT-LIB.

## Why finite index domains are hard

Previous decision procedures for extensional constant arrays all assume that the index domain is *infinite*, for example the mathematical integers. That assumption makes life much easier. Two infinite constant arrays with different default values can never be made equal, because you'd need infinitely many stores to change every index. So equalities between constant arrays reduce to equalities between their default values.

With a *finite* index domain, such as the 8-bit bit-vectors, this reasoning breaks down. Two constant arrays with different defaults *can* become equal if enough stores overwrite every index. For example, with only two possible indices, the formula

\\[ \langle v \rangle\langle i \triangleleft w \rangle\langle j \triangleleft w \rangle \approx \langle w \rangle \wedge v \not\approx w \\]

is satisfiable: just choose \\(i\\) and \\(j\\) to be the two different indices. In general, a solver has to reason about whether the stores on both sides together cover the *entire* index domain. That is a counting argument, and it doesn't fit naturally into existing array procedures.

This isn't just a theoretical gap. Among the solvers we tested, cvc5 and the previous version of Bitwuzla reject these problems outright. Z3 and MathSAT5 accept them, but on our crafted benchmarks they returned wrong answers on dozens of instances, all involving extensionality over finite constant arrays.

## Our approach

We first generalize the lemmas-on-demand procedure for extensional arrays from earlier work, which was specific to bit-vectors, to arbitrary index and element sorts. We present it as an abstract calculus that is independent of any particular solver architecture. The only requirement is a procedure that can supply a candidate model for the abstraction. We then extend this calculus with rules for constant arrays, including the finite case, and prove that the resulting calculus, CAEXT, is both refutationally and satisfiability sound.

The key ingredient for the finite case is a cardinality-style constraint. When the procedure detects a conflict between two constant arrays with different default values, it generates a lemma requiring that the indices written on the two sides cover at least as many distinct values as the index domain contains. We encode this with a new operator, \\(\mathit{distinct}_N(n, t_1, \ldots, t_k)\\), which holds when at least \\(n\\) of the terms \\(t_1, \ldots, t_k\\) take pairwise different values. This avoids quantifiers in the lemmas, which keeps them cheap for the underlying solver.

We implemented the procedure in the SMT solver [Bitwuzla](https://bitwuzla.github.io/), replacing its previous array solver. The calculus itself also covers infinite index domains, and we plan to bring it to [cvc5](https://cvc5.github.io/) as well.

## Results

Constant arrays aren't in the SMT-LIB benchmark library yet, so we evaluated the new procedure on several sources of problems:

- **Quantified SMT-LIB benchmarks** (5,112 instances). These don't mention constant arrays explicitly, but Bitwuzla's quantifier engine (model-based quantifier instantiation) represents array model values as stores on top of a constant array, so it constantly produces internal queries involving extensional constant arrays. With the new procedure, Bitwuzla solved **3,545** of these benchmarks, compared with 717 for the previous version: a 5× increase. On the benchmarks both versions solved, it was 27× faster. It also solved far more than Z3 (846) and cvc5 (276).
- **The quantifier engine's internal queries** (4,147). The new version solved all of them, compared with only 4 for the previous version. On the queries both it and Z3 solved, it was 140× faster than Z3.
- **Hardware model checking** (2,838 incremental queries from the Pono model checker's k-induction engine on HWMCC benchmarks). The new procedure solved every query, compared with 372 for the previous version and 2,142 for Z3, the next best.
- **Ethereum smart contracts** (benchmarks from the hevm symbolic execution engine). All solvers handled these well. The new procedure was the fastest.
- **Crafted benchmarks** that stress equalities between finite constant arrays. The new procedure solved the most, and it is the only solver that fully supports this case correctly.

For the full calculus, proofs, and experiments, see [the paper](https://doi.org/10.1007/978-3-032-32526-6_2) or [the extended version on arXiv](https://arxiv.org/abs/2605.16820). The artifact is [available on Zenodo](https://zenodo.org/records/19713260).
