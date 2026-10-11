---
layout: blog-post
categories: blog
math: true
excerpt_separator: <!--more-->
title: "Certificates in AI: Learn but Verify"
author: Clark Barrett
brief: "Why AI should be asked for evidence along with its answers, from our article in Communications of the ACM"
date: 2025-12-01
---

Self-driving cars should not crash. Credit scores should not discriminate. Chatbots should not hallucinate. Much of what AI produces is expected to meet objective requirements, but how can we trust that it does? In our article *Certificates in AI: Learn but Verify*, published in the December 2025 issue of *Communications of the ACM*, we argue for a simple rule we call the principle of **certifiable machine learning** (CML).
<!--more-->

## The principle

CML says: don't ask an AI for just the artifact you want. Ask for two things together, **the result** and **evidence that the result meets its specification**.

When that evidence can be checked independently, by someone who doesn't know or trust how the result was produced, we call it a **certificate**. Certificates come in many shapes:

- A fact can come with a **citation**, which anyone can look up.
- A theorem can come with a **proof**.
- Code can come with **loop invariants** (for safety) and **ranking functions** (for termination).
- A controller can come with a **barrier function** (for safety) or a **Lyapunov function** (for stability).

Asking for certificates pays off in several ways. Even if no one checks the evidence, the AI tends to do better simply because the request spells out what a good answer looks like. More importantly, the certificate can be handed to an independent checker, which opens the door to genuine guarantees.

## Learner and verifier

CML divides the work between two independent agents:

- The **learner** is powerful and efficient but not trusted. It might be a large language model or a neural network trainer, and it should benefit from every advance in AI. Its job is to propose both a result and a certificate.
- The **verifier** is trusted but may be slow or limited. It comes from the world of formal methods, and its only job is to *check* the certificate, not to find one.

This asymmetry is the heart of the idea. The hardest part of most proofs is coming up with an object that has some property: an invariant, a ranking function, a witness. That is where human ingenuity usually comes in, and where automated provers fall back on guessing or expensive search. In CML, the verifier never guesses. Whenever it needs such an object, it asks the learner.

Take termination. Showing directly that a program always terminates is hard. But if the learner also supplies a ranking function, a quantity that is never negative and goes down with every step, then checking that function is much easier than inventing it. And if the ranking function takes real values rather than integers, the learner can also supply the minimum amount by which it must decrease at each step.

The two agents work in a loop. If a check fails, the verifier sends feedback, such as a concrete counterexample or a hint, and the learner tries again. The learner can adjust the result, the certificate, or both. That flexibility matters: generating a result first and only then looking for a justification can fail because no suitable certificate exists for that particular result. Learning the two together avoids the problem.

As long as the verifier is sound, any result it accepts is guaranteed to meet its specification. When a formal check isn't possible, for example when the specification is in natural language, an informal, best-effort verifier can still catch problems and give feedback, though without a guarantee.

CML builds on a long line of work, most notably counterexample-guided inductive synthesis (CEGIS), which paired a learner that generates candidates with a verifier that checks them. CML goes a step further by asking the learner to do most of the work of producing certificates as well. It also differs from explainable AI: explanations aim to help *humans* understand a result, while certificates are meant to be checked by *machines*.

## CML in action

The article describes three applications:

- **Code from natural language.** Instead of asking an LLM only for code, ask it for code plus formal annotations: preconditions, postconditions, and loop invariants. A deductive verifier, such as Dafny, Verus, or CBMC, can then check that the code satisfies its annotations. The annotations also pin down exactly how the model interpreted an ambiguous natural-language request, so a human, or another LLM acting as an informal verifier, can confirm that the interpretation is right.
- **Verified code transpilation.** Translating programs into domain-specific languages such as Spark or NumPy by hand is tedious and error-prone. In LLMLift, an LLM proposes both the translated program and the loop invariants needed to prove it equivalent to the original, and an SMT-based verifier checks the proof.
- **Neural certificates for control.** For robots and other physical systems, a learner can train a neural controller together with a neural certificate, such as a barrier function showing that the system stays safe with a desired probability. The verifier checks the certificate's conditions and returns counterexamples when they fail. The learner can even help the verifier, for example by learning how to divide the state space into pieces that are easy to check.

## Looking ahead

Generative AI's potential seems nearly unlimited, but large neural networks are hard to explain and hard to verify. CML offers a practical path forward: whenever a task comes with a specification, ask the AI for a certificate along with its answer, and check it independently. This sets out a research agenda in which formal methods help make AI-generated artifacts safe and trustworthy.

You can read the full article [in Communications of the ACM](https://dl.acm.org/doi/full/10.1145/3737447).
