---
layout: blog-post
categories: blog
excerpt_separator: <!--more-->
title: "Search and Metavariable Coupling"
author: Leni Aniva
date: 2024-11-15
---
**Search** is the underlying theme of many difficult computational tasks.
Search algorithms have achieved incredible success in the fields of board games,
planning, and SMT. Can we extend the same idea to proving mathematical theorems?
We'll use an example to motivate.

<!--more-->

This is the beginning of a series of expositions on the topic of
machine-assisted theorem proving. My goal is to write the expositions in an
entertaining and educational format so the layperson can understand the
motivation, difficulty, and possible solutions in the quest for what I call
*logical creativity*, which has been a very tough goal for artificial
intelligence systems.

## Search

Many tasks in everyday life involve search. Planning a schedule, playing a game
of Go, or packing a bag all boil down to finding an optimal configuration in the
current state. **Search** is a cycle with the following steps:
1. Find the possible actions on a state
2. Compute the result of this action
3. Return to step (1) with derived states from step (2)

### Picnic

Let's consider a planning question. Five friends want to have a picnic. Their
names are Letty, Chen, Alice, Merlin, and Yomu, and five dishes: fish, soup,
dessert, bread, and fruit.

There are some restrictions:
1. Each person can only cook one dish
2. Fruit grows in the forest. It must be brought to the picnic. Letty lives far
   away from the forest so she prefers not to do this unless necessary
   (*foreshadowing*). Yomu is afraid of the dark so she cannot go as well.

Each person can only prepare certain dishes:

| Person | Dish           |
|--------|----------------|
| Chen   | Bread, Fish, Fruit |
| Alice  | Fruit, Dessert, Fish |
| Letty  | Soup, Bread |
| Merlin | Fruit, Dessert |
| Yomu   | Dessert, Soup |

Given these restrictions, what should each person prepare for the picnic?

<img src="/assets/blog-images/2024-11-15-search-and-metavariable-coupling/picnic-graph.svg" width="100%" alt="Picnic setting graph" />

### Solution

A common solution for a problem of this scale is to enumerate every single
combination of person and dish. While it is a sensible method for smaller
problems, the number of possible combinations quickly explode in size as the
number of questions get large. In fact it grows as $O(n!)$ for combinatorial
problems of size $n$. For problems involving numbers, there may be infinite
combinations.

A brute force solution will not scale, so we turn to the next best method of
solving this problem: Try to solve it one small piece at a time.

We could start by assigning Merlin the task of cooking dessert. At this point,
we do not know if this assignment will be correct in the end, but we must make
*some* attempt to reach a fuller solution.

<img src="/assets/blog-images/2024-11-15-search-and-metavariable-coupling/picnic-search-step1.svg" width="40%" alt="Search Step 1"/>

Then we could try assigning Chen the task of bread.

<img src="/assets/blog-images/2024-11-15-search-and-metavariable-coupling/picnic-search-step2.svg" width="70%" alt="Search Step 2"/>

This leaves not many options for the remaining members. Letty then must be cooking soup.

<img src="/assets/blog-images/2024-11-15-search-and-metavariable-coupling/picnic-search-step3.svg" width="100%" alt="Search Step 3"/>

But this is a problem. There is no dish Yomu can cook now! If every person can
only cook one dish, Yomu must do *something*. Recall that our decisions about
what the tasks of Merlin and Chen were arbitrary, so we could retrace our step
back to Chen's decision. This is known as **backtracking**. Suppose Chen this
time cooks Fish.

<img src="/assets/blog-images/2024-11-15-search-and-metavariable-coupling/picnic-search-step4.svg" width="100%" alt="Search Step 4"/>

Learning from our mistakes (*foreshadowing*), we assign Letty to the task of
bread.

<img src="/assets/blog-images/2024-11-15-search-and-metavariable-coupling/picnic-search-step5.svg" width="100%" alt="Search Step 5"/>

At this stage, the tasks of Alice and Yomu have been narrowed down so they do
not affect each other. Thus we conclude the roles of each person are

<img src="/assets/blog-images/2024-11-15-search-and-metavariable-coupling/picnic-search-full.svg" width="100%" alt="Picnic Search Graph"/>


| Person | Dish           |
|--------|----------------|
| Chen   | Bread, **Fish**, Fruit |
| Alice  | **Fruit**, Dessert, Fish |
| Letty  | Soup, **Bread** |
| Merlin | Fruit, **Dessert** |
| Yomu   | Dessert, **Soup** |

## Formulation

The above search process can be rigorously formulated in a proof assistant. A
*proof assistant* is a computer program which automatically checks the
correctness of logic. Examples include Lean, Isabelle, Coq, and Aya. In Lean 4,
every statement, theorem, proof, or function is an *expression*. For example, we
can write a function that maps a natural number to another natural number:

```lean
λ (x: Nat) ⇒ 3 * x + 2
```

$\vdash$ is the **entailment operator**, indicating the *type* of the left side
is equal to the right side. Each valid expression has a property called **type**
that is another expression. This article will not go into exactly what is a
type. Readers who are interested should read [Calculus of Inductive
Constructions](https://coq.inria.fr/doc/V8.11.1/refman/language/cic.html) in
Coq's documentation. The type of this expression is

```lean
Nat → Nat
```

which is the type of all functions that maps a natural number to another natural
number.

To represent the picnic task, we could define a type that has just 5 values:

```lean
inductive PicnicTask where
  | fish
  | bread
  | dessert
  | fruit
  | soup
deriving instance DecidableEq for PicnicTask
```

The `DecidableEq` instance is a technicality in Lean which allows us to compare
two `PicnicTask`s.

For example, the statement "Cirno can cook all five dishes" can be written in Lean as

```lean
?Cirno : PicnicTask
```

This means the value of `?Cirno` can only be one of the five cases listed in `PicnicTask`.

and "Letty can cook soup or bread" is

```lean
?Letty : { t: PicnicTask // [.soup, .bread].contains t }
```

This is **subtyping**, a construction in Lean where the type of a variable is
restricted to the set of another type. `?Letty.val` is now restricted to either
`.soup` or `.bread`.

`?Letty` is a **unassigned metavariable** or a **goal**. Lean 4 uses
metavariables to drive the proof search process.  The user's task is to provide
a solution to every goal. In Lean, the user assigns values to goals by directly
writing out a proof expression or use commands called **tactics**. A tactic
generates an expression dependent on the current goal.

The picnic problem above can be written as a list of goals:

```lean
?Chen   : { t: PicnicTask // [.bread, .fish, .fruit].contains t }
?Alice  : { t: PicnicTask // [.fruit, .dessert, .fish].contains t }
?Letty  : { t: PicnicTask // [.soup, .bread].contains t }
?Merlin : { t: PicnicTask // [.fruit, .dessert].contains t }
?Yomu   : { t: PicnicTask // [.dessert, .soup].contains t }
?unique : ?Chen.val ≠ ?Alice.val ∧ ?Chen.val ≠ ?Letty.val ∧ ... ∧ ?Merlin.val ≠ ?Yomu.val
```

Or, written mathematically

$$\begin{aligned}
    ?\text{Chen} &\vdash \{\text{Bread}, \text{Fish}, \text{Fruit}\} \\
    ?\text{Alice} &\vdash \{\text{Fruit}, \text{Dessert}, \text{Fish}\} \\
    ?\text{Letty} &\vdash \{\text{Soup}, \text{Bread}\} \\
    ?\text{Merlin} &\vdash \{\text{Fruit}, \text{Dessert}\} \\
    ?\text{Yomu} &\vdash \{\text{Dessert}, \text{Soup}\} \\
    ?1 &\vdash
        \mathsf{unique}(?\text{Chen}, ?\text{Alice}, ?\text{Letty}, ?\text{Merlin}, ?\text{Yomu})
\end{aligned}$$
When we begun to search for the optimal picnic arrangement, we did not have a
fully clear picture of the solution, represented by the question marks.  Yet we
can still reference these indeterminant values in statements such as "whoever
makes the dessert cannot also make fruit".

In particular the assignments of metavariables affect each other. If
$?\text{Chen} := \text{Bread}$, then we cannot have $?\text{Letty} =
\text{Bread}$. What we observed above is a phenomenon called **Metavariable
Coupling** and the terminology was first introduced in
[Aesop](https://zenodo.org/records/7430233).

Metavariable coupling often arise in mathematical problems. A minimal
metavariable coupling example is the following. Consider proving $2 \leq 5$. Set
this to a goal $?1$ and suppose we use $\leq$'s transitivity to prove it. This
amounts to proving

$$\begin{aligned}
?1 &\vdash 2 \leq ?z \\
?2 &\vdash ?z \leq 5 \\
?z &\vdash \Nat
\end{aligned}$$

Not only do we have to exhibit some value $z$, we also need to prove that it is
between $2$ and $5$! In an example like this, it is straightforward to try a
value of $z$ such as $z := 3$. This **decouples** the two goals $?1$ and $?2$:

$$\begin{aligned}
?1 &\vdash 2 \leq 3 \\
?2 &\vdash 3 \leq 5 \\
\end{aligned}$$

so their solutions no longer affect each other.

## Solutions of Metavariable Coupling

Metavariable coupling arises when we try to use artificial intelligence to solve
mathematics. It does not appear often, and hence some research papers could get
away with not mentioning it, but it is a fundamental feature of the logic system
we use. Aesop is a Lean proof automation tool and it first provided a concrete
definition and solution to coupling. Aesop's solution to coupling is *copying*.
When a goal is solved via a tactic execution, all the goals that were coupled to
it are copied (called **resumption**) as children goals.

<img src="/assets/blog-images/2024-11-15-search-and-metavariable-coupling/metavariable-coupling-copying.svg" width="60%" alt="Copying as a solution to coupling"/>

In our tool [Pantograph](https://arxiv.org/abs/2410.16429), the user has the
choice on how to handle metavariable coupling. The user has the choice to decide
when to *resume* a goal and *continue* from an earlier proof state. This is
named **Continuation-Resumption Paradigm**. Customized handling makes it easier
to refute fruitless search branches on the spot.

#### [Leni Aniva](https://leni.sh) is a PhD student advised by Clark Barrett in the Stanford Center for Automated Reasoning ([Centaur](https://centaur.stanford.edu/)) Lab. Her PhD work is focused on applying a combination of machine learning and formal methods to the problem of mathematical theorem proving. She is the author of [PyPantograph](https://github.com/lenianiva/PyPantograph) which is a tool for training machine learning models for Lean 4.
