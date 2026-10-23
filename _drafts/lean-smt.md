---
layout: blog-post
categories: blog
excerpt_separator: <!--more-->
title: "Lean-SMT: Bringing SMT Solvers into Lean"
author: Abdalrhman Mohamed
brief: "A tactic that sends Lean goals to cvc5 and turns its proofs into native Lean proofs, from our CAV 2025 paper"
date: 2025-07-21
---
<!-- DRAFT: written from the CAV 2025 paper for the author to review and revise before publishing. -->

Lean has quickly become one of the most popular proof assistants, especially among mathematicians. But it still lacks some of the automation that users of older systems take for granted. In particular, Isabelle's Sledgehammer can send a goal to an SMT solver and turn the solver's proof back into a checked Isabelle proof. In our CAV 2025 paper, *Lean-SMT: An SMT Tactic for Discharging Proof Goals in Lean*, we bring this capability to Lean 4.
<!--more-->

## Why not just trust the solver?

Proof assistants are trustworthy because every proof is checked by a small, simple kernel. SMT solvers are powerful but large and complex, so their answers shouldn't be trusted blindly. The solution is to ask the solver for a *proof* and replay that proof inside Lean, so that Lean's kernel has the final say. That is exactly what Lean-SMT does, with the proof-producing SMT solver [cvc5](https://cvc5.github.io/).

## How it works

Lean-SMT runs a goal through a four-stage pipeline:

1. **Preprocessing.** Lean's dependent type theory is far more expressive than the first-order logic SMT solvers use. Lean-SMT first uses our companion tool [Lean-auto](/blog/2025/07/21/lean-auto.html) to reduce the goal to first-order logic, for example by replacing a typeclass like `Group` with explicit axioms about the group operations. It then rewrites Lean-specific types and constructs, such as `Nat`, `Prop`, and `↔`, into forms that SMT-LIB supports. Every step produces a proof, so soundness is guaranteed by Lean.
2. **Translation.** The simplified goal is translated into an SMT-LIB problem whose unsatisfiability means the goal is true. One subtlety is that SMT-LIB assumes every type is non-empty, while Lean allows empty types. Lean-SMT stays sound by checking for this during reconstruction.
3. **Solving.** cvc5 solves the problem and produces a proof in its Cooperating Proof Calculus. Lean-SMT talks to cvc5 directly through a new Lean API we added to the solver.
4. **Reconstruction.** Lean-SMT replays cvc5's proof step by step as a native Lean proof, which Lean's kernel then checks.

Reconstruction is where most of the work is. cvc5's proof format has hundreds of rules, and Lean-SMT currently supports about 200 of them, enough for the most common kinds of goals. It uses three techniques:

- **Theorems:** for 163 rules, we proved a matching Lean theorem that justifies each use of the rule.
- **Tactics:** for 37 more complex rules, we wrote custom tactics backed by a library of around 400 theorems.
- **Reflection:** for rules involving computation, such as normalizing polynomial arithmetic, we wrote decision procedures in Lean and formally verified them. Compiling these to machine code made them up to 25× faster on large arithmetic expressions.

If a step can't be reconstructed, Lean-SMT doesn't fail silently. It hands that step back to the user as a subgoal, so soundness is never compromised.

We chose to *replay* proofs rather than run a single formally verified checker (the approach taken by SMTCoq for the Rocq proof assistant). Replay is much easier to adapt as cvc5's proof format evolves, which has been crucial while cvc5's proof infrastructure is still under active development.

## Results

We evaluated Lean-SMT in two ways:

- **As a tactic**, on 5,000 benchmarks from Isabelle's Sledgehammer evaluations, Lean-SMT outperformed Sledgehammer's integration with the veriT solver, largely because cvc5 solves more of these problems. It replayed proofs in under a second for 98% of the benchmarks, and in under five seconds for the rest.
- **As a trustworthy proof checker for SMT**, on SMT-COMP 2024 benchmarks, Lean-SMT verified 71% of the proofs cvc5 produced while relying only on Lean's kernel for soundness. It was usually within an order of magnitude of Ethos, cvc5's dedicated (and less minimal) proof checker. Compared with SMTCoq, it covers a broader range of problems, thanks to the flexibility of proof replay.

## What's next

Lean-SMT is a big step toward a full Sledgehammer-style hammer for Lean, and other Lean projects are already using it. Next we plan to support more SMT theories (bit-vectors, floating-point numbers, datatypes, and strings), cover more of cvc5's proof rules, and integrate more deeply with Lean-auto. Lean-SMT is open source and [available on GitHub](https://github.com/ufmg-smite/lean-smt).

For the full details, read [the paper](https://doi.org/10.1007/978-3-031-98682-6_11), which is open access.
