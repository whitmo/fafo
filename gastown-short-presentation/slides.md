---
title-prefix: Six Feet Up
pagetitle: "Cookin w/ Gas Town"
author: Whit Morriss, Six Feet Up
author-meta:
    - Whit Morriss
date: 2026
date-meta: 2026
keywords:
    - Agents
    - AI
    - Orchestration
    - Gas Town
---

<!-- slide: 0 -->
# Cookin w/ Gas Town {data-background="images/1.png"}

## Pt1 of a Conductor's Dilemma {.r-fit-text}
#### Whit Morriss
#### Six Feet Up

::: notes
- Intro: who you are, what you do at Six Feet Up
- This is part 1 — the conductor's dilemma is: how do you get
  multiple AI agents to do real work without everything falling apart?
- Today we're going to cook with Gas Town, a system we built to answer that question
:::

<!-- slide: 1 -->
# The Dilemma {data-background="images/2.png"}

One agent is a conversation.

Two agents is a negotiation.

Three agents is a _government_.

::: notes
- Single agent: you prompt, it responds. Easy.
- Two agents: now they need to agree on something. Handoff, context, who does what.
- Three+: you need structure. Roles, protocols, visibility.
- The conductor's dilemma: you can't micromanage agents and you can't
  let them free-range. You need a system that lets them self-organize
  around real constraints.
- This is the problem Gas Town solves.
:::

<!-- slide: 2 -->
# What is Gas Town {data-background="images/3.png"}

A multi-agent orchestration system for software teams.

- **Roles**: mayor, witness, refinery, polecats
- **Work units**: beads (trackable, auditable)
- **Projects**: rigs (worktrees with shared state)
- **Comms**: hooks, mail, handoffs

::: notes
- Gas Town is not a framework — it's an operating model
- Built on Claude Code, git worktrees, and plain files
- Each role has a specific job: mayor coordinates, witness reviews,
  refinery builds, polecats handle parallel tasks
- Beads are the unit of work — like tickets but lighter, tracked in the ledger
- Rigs are project containers — each agent gets their own worktree
- Communication is async: mail for messages, hooks for assignments
:::

<!-- slide: 3 -->
# The Cast {data-background="images/4.png"}

| Role | Job | Think of it as... |
|------|-----|-------------------|
| **Mayor** | Coordinate, delegate, decide | Tech lead |
| **Witness** | Review, verify, approve | QA / code review |
| **Refinery** | Build, implement, merge | Senior dev |
| **Polecats** | Parallel tasks, scouting | Junior devs |

::: notes
- Mayor is the drive shaft — checks hook, executes, delegates
- Witness watches for quality, catches mistakes before they land
- Refinery does the heavy lifting — implementation, merges, PRs
- Polecats are fungible — spin up N of them for parallel work
- Each role runs as a separate Claude Code session with its own context
- They communicate through the mail system, not through shared context
:::

<!-- slide: 4 -->
# The Engine {data-background="images/5.png"}

```
User request
  → Mayor creates bead
    → Mayor slings bead to rig
      → Agent picks up on hook
        → Work happens
          → Completion logged to ledger
```

::: notes
- This is the propulsion principle: when an agent finds work on their
  hook, they execute. No confirmation. No waiting.
- The hook IS your assignment
- Beads flow through the system like work orders
- Every completion is recorded — the ledger is the audit trail
- If an agent gets stuck, it hands off. Context is preserved in the bead.
- The failure mode is stopping to ask "should I do this?" — that's
  what kills throughput
:::

<!-- slide: 5 -->
# Why Not Just... {data-background="images/6.png"}

"Why not one big agent with a huge context?"

- Context is finite (~200k tokens)
- Attention degrades with length
- One agent = one thread of execution
- No parallelism, no specialization, no review

::: notes
- The tragedy of the context: every tool call, every search result
  eats tokens and pushes signal away from attention
- A single agent can't review its own work effectively
- With Gas Town, the witness reviews the refinery's work with fresh eyes
- Parallel polecats can scout 5 things at once
- Separation of concerns isn't just for code — it's for agents too
:::

<!-- slide: 6 -->
# Let's Cook {data-background="images/1.png"}

<DEMO>

::: notes
Demo target: conclave — a real incident response platform built with Gas Town.
Not a toy. Agents have been shipping real PRs on this rig.

Demo sequence (showoff steps):
1. gt rig status conclave — show who's running
2. bd create — make a real bead for conclave
3. gt sling — send it to the refinery
4. Watch the refinery pick it up, do the work
5. Witness reviews, mail flows
6. bd show — the ledger entry
:::

<!-- slide: 7 -->
# What We Just Saw {data-background="images/2.png"}

- Work flowed without human intervention
- Each agent did _one job well_
- Context stayed clean — no single agent held everything
- The ledger recorded what happened, not what was claimed

::: notes
- The refinery didn't need the full conversation history
- The witness reviewed with fresh context — adversarial by design
- Mail preserved the handoff context without polluting working memory
- The ledger is append-only — agents can't cover their tracks
- This is the conductor's insight: you don't play every instrument,
  you create the conditions for the orchestra to play itself
:::

<!-- slide: 8 -->
# The Conductor's Insight {data-background="images/3.png"}

You don't play every instrument.

You create conditions for the orchestra to play itself.

- **Constraint** over control
- **Protocol** over micromanagement
- **Visibility** over trust

::: notes
- Gas Town works because agents have clear roles and clear protocols
- The mayor doesn't write code — it creates beads and slings them
- The witness doesn't build — it reviews
- Constraint is what makes nondeterministic systems useful
- Same principle as the AllThings AI talk: determinism from
  nondeterministic systems through structure
:::

<!-- slide: 9 -->
# Next Time: Pt2 {data-background="images/4.png"}

The conductor's dilemma deepens:

- Failure modes and recovery
- Scaling polecats
- Cross-rig coordination
- When agents disagree

::: notes
- Part 2 will cover the hard problems: what happens when an agent
  fails mid-task, how do you scale beyond one rig, what happens
  when the witness and refinery disagree
- These are the real orchestration problems — the ones that make
  you want to go back to doing everything yourself
- But the ledger keeps you honest and the system keeps you sane
:::

<!-- slide: 10 -->
# Talk To Me {data-background="images/5.png"}

Whit Morriss

Six Feet Up

::: notes
- Thank you
- Questions welcome
- If you want to try Gas Town, it's built on Claude Code — ask me how to get started
:::
