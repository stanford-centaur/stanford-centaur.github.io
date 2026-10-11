---
layout: blog-post
categories: blog
math: true
excerpt_separator: <!--more-->
title: "Satisfiability Modulo Theories: A Beginner's Tutorial"
author: Clark Barrett
brief: "A hands-on introduction to SMT solvers, recognized with the FM 2024 Distinguished Tutorial Paper Award"
date: 2024-09-09
---

SMT solvers power a huge range of verification and analysis tools, but getting started with one can feel daunting. To help, we wrote *Satisfiability Modulo Theories: A Beginner's Tutorial*, which received the Distinguished Tutorial Paper Award at the 26th International Symposium on Formal Methods (FM 2024) in Milan. In this post we give a taste of what the tutorial covers and how to work through it yourself.
<!--more-->

## Why SMT?

People have long dreamed of machines that can reason deductively: given some assumptions, decide whether a conclusion follows. In 1928 David Hilbert posed this as a grand challenge, the *Entscheidungsproblem*. A few years later, Church and Turing showed that it is impossible in general. Automated reasoning researchers didn't give up. Instead, they looked for special cases that *are* decidable and for heuristics that work well in practice.

Satisfiability modulo theories (SMT) hits a sweet spot in that search. It builds on a rich collection of decidable *theories*, such as arithmetic, bit-vectors, arrays, and strings, that give users a lot of expressive power without giving up decidability. It also handles some undecidable problems, such as many with quantifiers, using heuristics that often work well.

## A solver is a very smart calculator

At an intuitive level, an SMT solver is like a calculator: you describe a problem and it computes an answer. But it works *symbolically*, like grade-school algebra. You state constraints, and the solver either finds a solution satisfying all of them or reports that none exists. The tutorial starts with a classic word problem:

> In 10 years, Alice will be twice as old as Bob is now, but in 22 years, Bob will be twice as old as Alice is now. How old are Alice and Bob?

Using [cvc5](https://cvc5.github.io/)'s Python API (which is designed as a drop-in replacement for Z3's), this takes just a few lines:

```python
from cvc5.pythonic import *

a, b = Ints('a b')
solve(a + 10 == 2 * b, b + 22 == 2 * a)
```

The answer is `[a = 18, b = 14]`. The same problem can also be written in SMT-LIB, the standard input language that SMT solvers share:

```
(set-logic QF_LIA)
(set-option :produce-models true)
(declare-const a Int)
(declare-const b Int)
(assert (= (+ a 10) (* 2 b)))
(assert (= (+ b 22) (* 2 a)))
(check-sat)
(get-model)
```

The solver replies `sat` (short for *satisfiable*) and then prints a model assigning 18 to `a` and 14 to `b`. If the constraints have no solution, it replies `unsat` instead.

That one capability turns out to answer several kinds of questions:

- **Is something possible?** Assert your assumptions together with the hypothetical situation and ask whether the result is satisfiable. For example, the tutorial asks whether the product of two 32-bit machine integers can equal 1 when one of them is even. The answer is no: in arithmetic modulo a power of 2, even numbers have no multiplicative inverse.
- **Does something follow?** To check whether a conclusion follows from some assumptions, assert the assumptions together with the *negation* of the conclusion. If that is unsatisfiable, the conclusion must hold. The tutorial illustrates this with the classic syllogism: all humans are mortal, Socrates is human, so Socrates is mortal.

## What's in the tutorial

The tutorial is organized as a guided tour, with examples and exercises throughout:

- **Formal foundations:** the syntax and semantics of the many-sorted first-order logic underlying SMT, and what it means to reason "modulo a theory".
- **A catalog of SMT theories**, each with examples showing how to use it: uninterpreted functions, integer and real arithmetic, arrays, bit-vectors, algebraic datatypes, floating-point arithmetic, strings, and quantifiers. It also covers some non-standard theories, such as finite fields, and how theories combine.
- **Solver outputs:** what you can learn beyond `sat` and `unsat`. That includes models and the values of specific terms for satisfiable problems; *unsat cores* (subsets of the assertions that are already contradictory) and full *proofs* for unsatisfiable ones; and what it means when a solver answers `unknown`.

## Try it yourself

Every example and exercise works with either cvc5 or Z3, using either Python or SMT-LIB. You can install a solver's Python package, download a binary, or simply use [cvc5 in your browser](https://cvc5.github.io/app/) with nothing to install. The [online version of the tutorial](https://cvc5.github.io/tutorials/beginners/) on the cvc5 website includes all the examples, including SMT-LIB versions that didn't fit in the paper, along with solutions to the exercises.

You can read the full paper [on Springer](https://doi.org/10.1007/978-3-031-71177-0_31), where it is open access. An artifact with all the examples and tools is [available on Zenodo](https://doi.org/10.5281/zenodo.12763927).
