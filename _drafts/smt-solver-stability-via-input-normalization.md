---
layout: blog-post
categories: blog
excerpt_separator: <!--more-->
title: "Towards SMT Solver Stability via Input Normalization"
author: Daneshvar Amrollahi
brief: "Making SMT solvers less sensitive to harmless changes in their input, from our FMCAD 2025 paper"
date: 2025-10-06
---
<!-- DRAFT: written from the FMCAD 2025 paper for the author to review and revise before publishing. -->

If you use SMT solvers regularly, you have probably run into this: a query that solved in a second yesterday takes a minute today, or times out altogether, even though you only renamed a variable or moved a function. This is the *stability* problem. In our FMCAD 2025 paper, *Towards SMT Solver Stability via Input Normalization*, we show how to reduce it by putting every input into a canonical form before the solver sees it.
<!--more-->

## Why stability matters

SMT solvers increasingly run inside workflows that send them the same or nearly the same queries over and over. Think of a software verification tool that reruns its regression suite every night. When performance swings wildly from one run to the next, it is frustrating and expensive.

This isn't a niche complaint. As part of an NSF-supported project, we interviewed a large number of SMT users and catalogued more than 100 issues they raised. Instability ranked second, behind only requests for better diagnostics when the solver fails. Engineers at Amazon Web Services, which runs SMT solvers at enormous scale, have named it as a top priority too.

Two points are worth making up front. First, stability is not the same as speed. Our goal is to make solving times *consistent*, and many users told us they would accept some slowdown in exchange. Second, some instability is inherent. SMT is NP-hard (or worse), so solvers rely on heuristics to guide an exponential search, and a tiny change in the input can send that search down a very different path, much like the butterfly effect.

## Where the variation comes from

Modern solvers already use deterministic data structures and algorithms. In a sequential setting, the main remaining source of variation is their search heuristics, which typically break ties according to *the order in which declarations and assertions appear in the input*. So two inputs that differ only in harmless ways can lead to completely different searches.

We consider four kinds of harmless, meaning semantics-preserving, changes, which we call *mutations*:

1. reordering assertions;
2. swapping the operands of commutative operators, such as `(+ x y)` versus `(+ y x)`;
3. renaming and reordering declarations; and
4. flipping a comparison, such as rewriting `(< a b)` as `(> b a)`.

These mirror what happens in practice. For example, moving or renaming a function in a program being verified can reorder and rename the declarations and assertions in the resulting query. Here is a tiny example of two inputs that differ only by renaming and reordering:

```
(declare-const x Int)          (declare-const b Int)
(declare-const y Int)          (declare-const a Int)
(assert (< (+ x y) 10))        (assert (> b 3))
(assert (> x 3))               (assert (< (+ b a) 10))
```

A solver may handle these very differently, even though they are the same problem.

## Normalization

Our idea is simple: before calling the solver, map every input to a *normal form*, so that all mutated versions of a problem become the same input. If that worked perfectly, the solver would see an identical query every time, and instability with respect to these mutations would disappear.

We first ask whether such a perfect normalizer exists. It does: one can define a canonical choice among all the equivalent versions of an input. But computing it is expensive. We show that perfect normalization, even just for reordering and renaming, is at least as hard as *graph isomorphism*, a famous problem for which no polynomial-time algorithm is known.

So we designed an efficient approximation that handles reordering and renaming:

1. **Sort the assertions by their shape.** We compare assertions by their *pattern*: the formula with each user-defined name replaced by a placeholder according to the order of first appearance. This makes the ordering independent of what anything is called.
2. **Break ties with "super-patterns".** Assertions with the same pattern are ordered by looking at how each symbol is used across the whole problem: in which groups of assertions it appears, and in what position.
3. **Rename everything canonically**, then sort once more.

The approximation isn't guaranteed to find a unique normal form, since highly symmetric problems can defeat the tie-breaking. But it is fast. With some engineering, such as sharing common subterms and indexing which assertions mention each symbol, it scales to benchmarks that are hundreds of megabytes in size.

## Results

We evaluated the normalizer on about 41,000 benchmarks sampled from SMT-LIB and on 16,600 program-verification benchmarks from the Mariposa project, which first measured instability in tools like Dafny and F\*. We created 10 randomly mutated versions of each benchmark.

- **Normal forms.** Without normalization, the 10 versions of a benchmark are almost always all different. After normalization, many SMT-LIB benchmarks collapse to one or two versions. On a sample, our normalizer produced a unique normal form 87% of the time, compared with 12% for an earlier normalizer designed for a narrower purpose. Even when it doesn't reach a unique form, the normalized versions become much more alike.
- **Stability.** We measured how much total solving time varies across the 10 versions, using both cvc5 and Z3. Normalization reduced the variation in *every* category, sometimes by more than an order of magnitude. For example, in one category of benchmarks for cvc5, the variation dropped from 286 to 4. Stability improved even on benchmarks where normalization didn't produce a single normal form, which suggests that making inputs *more similar* already helps.
- **Cost.** Normalization took less than 0.8% of total run time overall, and average solving performance was essentially unchanged.

The normalizer works with any SMT solver. Next, we plan to handle the remaining mutation types (commutative operands and flipped comparisons), explore further normalization techniques, and use normal forms to improve caching of solver results.

For the details, see [the paper](https://doi.org/10.34727/2025/isbn.978-3-85448-084-6_14). The artifact is [available on Zenodo](https://doi.org/10.5281/zenodo.16929484).
