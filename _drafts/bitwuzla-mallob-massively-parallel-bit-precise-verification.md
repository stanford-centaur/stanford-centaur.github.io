---
layout: blog-post
categories: blog
excerpt_separator: <!--more-->
title: "Massively Parallel Bit-Precise Verification with Bitwuzla and Mallob"
author: Aina Niemetz and Mathias Preiner
brief: "How plugging Bitwuzla into the distributed SAT platform Mallob lets one SMT query use hundreds of cores"
date: 2026-04-11
---
<!-- DRAFT: written from the TACAS 2026 paper for the authors to review and revise before publishing. -->

Our TACAS 2026 paper, *Massively Parallel Bit-Precise Verification with Bitwuzla and Mallob*, received three awards at ETAPS 2026: the ETAPS Best Tool Paper Award, the TACAS Distinguished Paper Award, and the TACAS Distinguished Artifact Award. In this post we explain the idea behind the system, which we call Bitwuzllob, and why it scales so well.
<!--more-->

## Why parallelize at the SAT level?

Bit-precise reasoning, that is, reasoning about fixed-size machine integers, is at the heart of many hardware and software verification tools. The dominant way SMT solvers handle bit-vectors is *bit-blasting*: after aggressive simplification, bit-vector constraints are translated into a propositional formula and handed to a SAT solver. This works remarkably well in practice, because modern SAT solvers can handle formulas with millions of variables. It also means that the SAT solver is usually where most of the time goes.

[Bitwuzla](https://bitwuzla.github.io/) is our SMT solver for bit-precise reasoning. It supports bit-vectors and floating-point arithmetic, combined with arrays and uninterpreted functions, with and without quantifiers. Its architecture follows the *lemmas on demand* paradigm: rather than tightly interleaving SAT search and theory reasoning (as in classic CDCL(T)), Bitwuzla maintains a bit-vector abstraction of the problem, bit-blasts it, asks a SAT solver whether it is satisfiable, and refines the abstraction with lemmas when the theory solvers find the SAT solver's model inconsistent. The upshot is that almost all of Bitwuzla's non-trivial reasoning happens inside plain *incremental* SAT calls, which are far easier to parallelize than the fine-grained back-and-forth of CDCL(T).

Meanwhile, distributed SAT solving has made huge strides. [Mallob](https://github.com/domschrei/mallob) is a distributed platform for scheduling and solving many SAT tasks at once, growing and shrinking the resources given to each task on demand. Its SAT engine, MallobSat, runs a solver thread on every core and has them share learned clauses, which lets it solve hard problems hundreds of times faster than a sequential solver. Mallob also supports incremental SAT solving at a distributed scale. Before this work, though, none of that power had been put to use for SMT.

## Putting the two together

Bitwuzllob integrates Bitwuzla into Mallob as a new application engine. From the outside it behaves like an ordinary SMT solver: it reads SMT-LIB and produces the usual answers and models. Inside, each SAT solver instance that Bitwuzla creates is replaced by an adapter object in Mallob, which sends Bitwuzla's SAT calls to a distributed incremental SAT task.

Because the parallelism lives entirely in the SAT back end, the approach is theory-agnostic. Every theory and combination that Bitwuzla supports benefits automatically, including quantified logics, floating-point arithmetic, and incremental (push/pop) problems.

Making this work well took more than wiring the two systems together. Three engineering ideas turned out to matter most:

- **Hiding latency.** Bitwuzla often issues thousands of SAT calls on one problem, most of them trivial. Even a few milliseconds of distributed overhead per call adds up. So each adapter also runs a local sequential SAT solver alongside the distributed one, and whichever finishes first wins. The distributed task is only launched once a call comes along that the local solver can't dispatch within a few milliseconds. If a problem consists of thousands of easy calls followed by one hard one, the cluster only ever sees the hard one.
- **Efficient communication.** To keep up with that volume of incremental updates, we reworked how Mallob passes formula data between processes, replacing many shared-memory segments with a single double-buffered channel.
- **Bounding concurrent tasks.** Quantified problems make Bitwuzla spawn nested sub-solvers, each with its own SAT solver. Since every suspended distributed task occupies a process, we cap the number of distributed tasks per SMT problem. When the cap is reached, we evict an inactive task (the one with the least accumulated runtime) and redeploy it later if it's needed again.

## Results

We evaluated Bitwuzllob on a representative sample of SMT-LIB benchmarks from every logic Bitwuzla supports: 1,098 non-incremental and 288 incremental instances. We ran it on up to 16 nodes (768 cores) of the SuperMUC-NG supercomputer. We compared against sequential Bitwuzla and against the strongest entries in the parallel track of SMT-COMP 2025: Bitwuzla with the parallel SAT solver Gimsatul as its back end, the partitioning-based solver STP-Parti-Bitwuzla, and a parallel portfolio of Yices2.

On a single 48-core node, Bitwuzllob clearly outperformed all of these. On non-incremental bit-vector (QF_BV) problems, it matched the Gimsatul-based configuration on easy instances and pulled well ahead on harder ones. Across all logics, the difference was even starker. Gimsatul doesn't support incremental solving, so Bitwuzla has to recreate it for every SAT call, and that configuration ended up *slower* than plain sequential Bitwuzla. Bitwuzllob, by contrast, beat sequential Bitwuzla by a wide margin.

Bitwuzllob also keeps scaling. Even on 4 cores it beats sequential Bitwuzla, and it continues to improve all the way up to 768 cores, with diminishing returns beyond about four nodes. Speedups grow with problem difficulty. On instances that take sequential Bitwuzla at least 300 seconds, the mean speedup is 9.9× on one node, 12.5× on four, and 15.6× on sixteen. Latency hiding pays off especially for incremental logics that issue more than a thousand SAT calls per instance, with mean speedups between 60% and 590%.

## What's next

Bitwuzllob gives us a solid foundation for further work on scalable bit-precise reasoning. Directions we're excited about include letting Bitwuzla issue asynchronous SAT calls so that several SAT tasks can run truly in parallel, combining SAT-level parallelism with theory-specific parallelization, and exploring several satisfying assignments from the distributed solver at once. That last idea is motivated by our observation that Bitwuzla's search can be quite sensitive to which model the SAT solver returns.

For all the details, see [the paper](https://doi.org/10.1007/978-3-032-22752-2_9). The artifact is [available on Zenodo](https://zenodo.org/records/17478480).
