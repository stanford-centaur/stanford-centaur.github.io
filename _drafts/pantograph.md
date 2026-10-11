---
layout: blog-post
categories: blog
math: true
excerpt_separator: <!--more-->
title: "Pantograph: A Machine-to-Machine Interface for Lean 4"
author: Leni Aniva
brief: "An interface that lets machine learning agents search for proofs, sketch them, and extract data in Lean 4, from our TACAS 2025 paper"
date: 2025-05-03
---
<!-- DRAFT: written from the TACAS 2025 paper for the author to review and revise before publishing. -->

Proof assistants like Lean 4 give us the strongest guarantees we know how to get, for everything from verified operating systems to formalized mathematics. But writing formal proofs is slow and requires expertise, and machine learning is a promising way to automate more of it. To build AI agents that prove theorems, though, you first need a good way for a *machine* to talk to the proof assistant. That is what our TACAS 2025 paper, *Pantograph: A Machine-to-Machine Interaction Interface for Advanced Theorem Proving, High Level Reasoning, and Data Extraction in Lean 4*, provides.
<!--more-->

## Why a new interface?

The standard way to interact with Lean 4 is through its Language Server Protocol (LSP), the interface behind your editor. It is great for people, but awkward for programs. A machine using it has to track cursor positions in a text file, there is no easy way to extract training data, and there is no natural way to sketch a proof and let automation fill in the rest.

Pantograph is designed from the ground up for machine users. It is written entirely in Lean 4, with no external dependencies, and you can use it from Python (through PyPantograph), as a read-eval-print loop, or as a library. Its name comes from the drawing instrument that copies the movements of a pen, which is a fitting image for a tool that records a proof as it is being searched for.

## What Pantograph enables

**Real tree search.** When a proof has several open goals, Pantograph lets the agent decide which one to work on next. That makes it possible to use powerful search strategies like Monte Carlo Tree Search, the approach behind AlphaGo and AlphaZero, where an agent explores the most promising branches of a search tree. The complication is *metavariable coupling*: some tactics create goals that depend on each other, so solving one changes the others. Pantograph tells the agent exactly which goals are coupled and lets it decide how to handle them. (For a deeper dive into coupling, see our earlier post, [Search and Metavariable Coupling](/blog/2024/11/05/search-and-metavariable-coupling.html).)

**High-level reasoning steps.** Unlike earlier tools for Lean 4, Pantograph supports the tactics people rely on for structured reasoning: `have` and `let` for introducing intermediate claims, and `conv` and `calc` for step-by-step rewriting and chains of equalities. Pantograph can even run `conv` and `calc` partially and report the result, just as a human sees feedback at each step in the editor.

**Drafting.** Pantograph can take an incomplete proof and turn every `sorry` placeholder into a goal to be solved. That means an AI can write the outline of a proof and leave the details to other tools. For example, given the sketch

```lean
theorem double_le (n : Nat) (h : n ≤ 5) : 2 * n ≤ 10 := by
  have h1 : 2 * n ≤ 2 * 5 := sorry
  sorry
```

Pantograph produces two goals: proving the intermediate claim `h1`, and finishing the proof using `h1`. Each can then be handed to an automated tactic.

**Training data.** Pantograph can process whole Lean files, such as those in the Mathlib library, and extract every tactic step as a (goal before, tactic, goal after) triple, which is ready-made training data. It can also extract complete proofs along with their comments, which is useful for tasks like autoformalization, and can represent proofs as programs.

## Draft, sketch, prove, in Lean 4

To show what Pantograph makes possible, we used it to build the first implementation of the *Draft-Sketch-Prove* (DSP) approach in Lean 4. DSP was previously implemented in Isabelle. It works in three stages:

1. A language model writes an informal, natural-language proof (**draft**).
2. The same model turns that into a formal Lean 4 proof outline with `sorry` placeholders (**sketch**).
3. Pantograph turns the placeholders into goals, and standard automated tactics (`aesop`, `simp`, and `linarith`) try to close each one (**prove**).

We evaluated this on the MiniF2F benchmark of competition-style math problems, using off-the-shelf GPT-4o and o1-preview with no task-specific training. Our best configuration, GPT-4o generating three sketches per problem, proved **28%** of the test-set theorems. That isn't state of the art, but it is a solid baseline for an untrained system, and Pantograph's drafting support made it straightforward to build. Running three sketches instead of one barely increased run time, which suggests that model inference, not the proof search, is the main bottleneck.

The experiment also illustrates a broader point. Language models can hallucinate, but when their output is a formal proof sketch, the proof assistant and automation check every step. Pantograph is designed to make this kind of combination of generative AI and formal reasoning easy to build.

## Try it

Pantograph is open source: the core tool is [on GitHub](https://github.com/leanprover/Pantograph), and so is the Python interface, [PyPantograph](https://github.com/stanford-centaur/PyPantograph). Research groups in both academia and industry were already using it before the paper was published, and we hope you'll find interesting new ways to use it too.

For all the details, read [the paper](https://doi.org/10.1007/978-3-031-90643-5_6), which is open access.
