---
layout: blog-post
categories: blog
excerpt_separator: <!--more-->
title: "Lean-auto: Connecting Lean 4 to Automated Theorem Provers"
author: Yicheng Qian
brief: "How Lean-auto translates Lean 4's rich type theory into logic that automated provers understand, from our CAV 2025 paper"
date: 2025-07-21
---
<!-- DRAFT: written from the CAV 2025 paper for the author to review and revise before publishing. -->

Anyone who has written proofs in Lean knows the feeling: you reach a step that is obvious on paper but tedious to justify formally. Other proof assistants have long had a powerful answer, called *hammers*, which hand such goals off to automated theorem provers. Isabelle's Sledgehammer is the best-known example. Lean 4 has not had one. In our CAV 2025 paper, *Lean-auto: An Interface Between Lean 4 and Automated Theorem Provers*, we tackle the hardest part of building a hammer for Lean: translating Lean's logic into something automated provers can work with.
<!--more-->

## What makes a hammer, and why Lean is hard

A hammer has three main parts:

1. **Premise selection:** choosing which existing theorems are likely to be useful.
2. **Translation:** turning the goal and the premises into the input language of an automated prover.
3. **Proof reconstruction:** turning the prover's answer back into a proof that the proof assistant's kernel can check.

Lean-auto focuses on translation, which is especially difficult for Lean. Automated provers work in relatively simple logics: first-order logic and, increasingly, higher-order logic. Lean 4 is built on *dependent type theory*, which is far more expressive, and everyday Lean code leans heavily on features such as typeclasses (used throughout Mathlib to overload operators and describe mathematical structures), universe polymorphism, inductive types, and definitional equality (terms that look different but are equal by computation). A translation has to bridge all of that without producing something unsound or impossibly large.

## How Lean-auto works

There are two broad ways to translate a rich logic into a simpler one. *Encoding-based* translation (used by CoqHammer) represents typing information explicitly with extra symbols. *Monomorphization* (used by Isabelle's Sledgehammer) instead instantiates polymorphic statements at the specific types where they are actually needed. In a small experiment on Mathlib, we found that encoding produced much larger problems, which tends to hurt prover performance, so Lean-auto uses monomorphization.

Sledgehammer's monomorphization was designed for a simpler logic than Lean's, so we redesigned it from the ground up for dependent type theory. Lean-auto translates a goal in stages:

- **Preprocessing** handles Lean-specific features. It partially unfolds definitions to deal with definitional equality, generates equations relating terms that are equal by definition, translates inductive types, and sets the goal up as a proof by contradiction.
- **Quantifier instantiation** runs a saturation loop that instantiates general (polymorphic) facts at the specific types that appear in the problem.
- **Abstraction** then turns the result into a higher-order logic problem, absorbing the parts that automated provers can't understand, including large typeclass arguments, into ordinary variables.
- **Universe lifting** finally removes Lean's universe levels.

The main translation is sound: if the automated prover proves the translated problem, the original Lean goal is true.

Lean-auto can send problems to three kinds of provers: Duper, a superposition prover written in Lean itself; Zipperposition, a higher-order prover; and the SMT solvers Z3 and cvc5. For Duper, Lean-auto reconstructs a full proof that Lean's kernel checks. For the external provers, it currently trusts their answers and issues a warning. Reconstructing proofs from SMT solvers is the job of our companion project, [Lean-SMT](/blog/2025/07/21/lean-smt.html).

## Results

We evaluated Lean-auto on about 149,000 theorems from Mathlib4. To isolate the quality of the translation, we gave each tool the premises used in the theorem's human-written proof, which simulates an ideal premise selector.

- **Lean-auto combined with Duper**, the configuration with full proof reconstruction, proved **36.6%** of the theorems. That is more than any existing Lean tool, and 5 percentage points better than the best previous one, the proof-search tactic Aesop.
- Lean-auto is **complementary** to existing tools: 14.8% of the theorems were proved only by Lean-auto.
- Running Lean-auto **together with existing tools** proved **more than half (53.2%)** of the theorems.

Lean-auto is currently slower than existing tactics on easy problems, but it solves more problems overall.

## What's next

Lean-auto is a key building block for a full hammer in Lean 4. Next steps include premise selection, broader proof reconstruction, handling more advanced uses of type quantifiers, and improving performance. Lean-auto is open source and [available on GitHub](https://github.com/leanprover-community/lean-auto).

For the full details, read [the paper](https://doi.org/10.1007/978-3-031-98682-6_10), which is open access.
