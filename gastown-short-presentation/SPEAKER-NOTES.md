# Speaker Notes — Cookin w/ Gas Town (15 min)

5 min slides, 10 min live demo. Don't rush the slides to get to the demo — the concepts make the demo land.

---

## Pre-Talk Setup Checklist

- [ ] **Conclave rig running**: `gt rig status conclave` should show witness + refinery running. If not, start them: `gt rig start conclave/witness` and `gt rig start conclave/refinery`.
- [ ] **Clean mayor inbox**: `gt mail inbox` — read or archive old messages so the demo inbox isn't cluttered with stale mail. You want to show fresh flow, not yesterday's noise.
- [ ] **Showoff ready**: confirm `make demo` works from the presentation directory. Showoff depends on gum — run `which gum` and `which showoff` (or check that `../labs/showoff/bin/showoff` exists).
- [ ] **Reset demo state**: `make demo-reset` to clear any previous demo workspace.
- [ ] **No stale beads**: `bd list` — make sure there isn't already a bead called "Add liveness probe to the etherpad deployment" sitting around. If so, close it or pick a different task title.
- [ ] **Browser open** to `localhost:8000` with the presentation loaded (`make start` in another terminal).
- [ ] **Terminal ready**: big font, dark background, positioned next to or below the browser. The audience needs to read your terminal.
- [ ] **Two terminal tabs/panes**: one for showoff demo commands, one for ad-hoc checks if needed.

---

## Slide-by-Slide Guide

### Slide 0 — "Cookin w/ Gas Town" (title)
**Image**: busytown-gastown.png

- Introduce yourself. Name, Six Feet Up, what you do there.
- Frame the talk: Part 1 of a two-part series. Today is "how do you get multiple AI agents to do real work without everything falling apart?"
- Set expectations: 5 min of concepts, then a live demo against a real project.

**Timing**: ~30 seconds

**Transition**: "So what's the dilemma?"

---

### Slide 1 — "The Dilemma"
**Image**: future-is-legion.jpg

- Read the three lines on the slide — let them land. One agent is a conversation. Two is a negotiation. Three is a government.
- The point: once you have multiple agents, you need structure. You can't micromanage them and you can't let them free-range.
- This is the problem Gas Town was built to solve.

**Timing**: ~45 seconds

**Transition**: "So why orchestrate at all? Why not just let them talk to each other?"

---

### Slide 2 — "Why Orchestrate"
**Image**: kent-beck-genie.png

- This is the thesis slide. Read the quote: "Patterns for communication are patterns for parallelism."
- Explain: if you want agents working in parallel, you need communication patterns first. Not bureaucracy — infrastructure.
- Name-drop the lineage: CSP, actor models, message queues. Those solved concurrency for software. Roles and protocols solve it for agents.
- Every design choice in Gas Town (mail, hooks, beads, roles) exists so agents can work simultaneously without stepping on each other.

**Timing**: ~45 seconds

**Transition**: "Let me show you what Gas Town actually is."

---

### Slide 3 — "What is Gas Town"
**Image**: 4.png

- Gas Town is not a framework — it's an operating model. Built on Claude Code, git worktrees, and plain files.
- Walk the four bullets: roles (who), beads (what), rigs (where), comms (how).
- Emphasize: beads are lighter than tickets. Rigs give each agent their own worktree. Communication is async — mail and hooks, not shared context.

**Timing**: ~45 seconds

**Transition**: "Let's meet the cast."

---

### Slide 4 — "The Cast"
**Image**: busytown-joe.png

- Walk the table quickly. Mayor = tech lead. Witness = QA. Refinery = senior dev. Polecats = junior devs.
- Key insight: each role runs as a separate Claude Code session with its own context. They communicate through the mail system, not through shared memory.
- Mayor is the drive shaft. Witness catches mistakes before they land. Refinery does the heavy lifting. Polecats are fungible — spin up N of them.

**Timing**: ~30 seconds

**Transition**: "Here's how work actually flows through the system."

---

### Slide 5 — "The Engine"
**Image**: 6.png

- Walk the flow: user request -> mayor creates bead -> slings to rig -> agent picks up on hook -> work happens -> logged to ledger.
- The propulsion principle: when an agent finds work on their hook, they execute. No confirmation. No waiting. The hook IS your assignment.
- The failure mode is stopping to ask "should I do this?" — that kills throughput.

**Timing**: ~30 seconds

**Transition**: "Enough theory. Let's cook." (advance to demo slide)

---

### Slide 6 — "Let's Cook" (DEMO)
**Image**: agent-at-home-0.png

- Say: "We're going to do this live against conclave — a real incident response platform. Not a toy."
- Switch to terminal, run `make demo`.

**Timing**: This is the handoff — 5 seconds on the slide, then you're in the terminal for 10 minutes.

---

### Slide 7 — "What Makes It Work"
**Image**: busytown-gastown.png

- Come back to slides after demo.
- Three principles: constraint over control, protocol over micromanagement, visibility over trust.
- The mayor doesn't write code. The witness doesn't build. Constraint is what makes nondeterministic systems useful.

**Timing**: ~30 seconds

**Transition**: "Part 2 will cover the hard problems."

---

### Slide 8 — "Next Time + Talk To Me"
**Image**: 3.png

- Tease Part 2: failure modes, scaling polecats, cross-rig coordination.
- Thank you, questions welcome. "Gas Town is built on Claude Code — ask me how to get started."

**Timing**: ~15 seconds + Q&A

---

## Demo Walkthrough (10 minutes)

Start the demo from the presentation directory:

```sh
make demo
```

Showoff will walk you through `demo/steps/` one at a time. It presents each step file and gives you a workspace to run commands.

---

### Step 1 — See the Orchestra (~2 min)

**Commands:**
```sh
gt rig status conclave
```
then:
```sh
gt mail inbox
```

**What to say:**
- "This is the conclave rig. You can see the witness and refinery are running — each is a separate Claude Code session in its own git worktree."
- "The mayor's inbox is the coordination hub. You can see messages from previous agent work — this isn't a fresh setup, this is a live project."
- Point out the roles by name in the status output. If there are recent mail messages, read one briefly to show the format.

**If it fails:**
- `gt rig status` hangs: kill it, run again. Sometimes the first call after idle is slow.
- Witness/refinery not running: `gt rig start conclave/witness` and `gt rig start conclave/refinery` on the spot. Narrate it — "agents need to be running to pick up work, let me start them."

---

### Step 2 — Create Work (~1.5 min)

**Commands:**
```sh
bd create "Add liveness probe to the etherpad deployment"
```
then:
```sh
bd list
```

**What to say:**
- "A user request becomes a bead — that's our unit of work. Lighter than a ticket, heavier than a TODO."
- After create: "Note the bead ID — this is now a trackable, auditable work item." Write down or remember the bead ID for step 3.
- After list: "You can see it in the ledger alongside any other active beads."

**If it fails:**
- `bd create` errors: check you're in the right context (mayor role). Run `gt prime` if needed.
- Wrong bead title: doesn't matter, any title works. Pick something relevant to conclave.

---

### Step 3 — Sling to Refinery (~1.5 min)

**Commands:**
```sh
gt sling <bead-id> conclave/refinery
```
then:
```sh
gt hook conclave/refinery
```

**What to say:**
- "The mayor doesn't build — it delegates. We sling this bead to the conclave refinery."
- "The refinery will pick this up on its next hook check. No waiting, no confirmation. It works in its own git worktree — isolated from my context."
- After `gt hook`: "This is what the refinery's hook looks like — the bead is sitting there, waiting to be picked up."

**If it fails:**
- Sling fails with "unknown rig": make sure conclave rig exists — `gt rig list`.
- Wrong bead ID: use `bd list` to grab the right one.

---

### Step 4 — Watch it Flow (~3 min)

This is the money step. Give it time.

**Commands:**
```sh
gt mail inbox
```
then:
```sh
gt rig status conclave
```
then:
```sh
bd log
```

**What to say:**
- "Now we wait for the system to work. The refinery picks up the bead, does the work, and reports back. The witness reviews automatically."
- Check inbox repeatedly if needed — narrate what you see: "The refinery has picked up the bead... it's working on the implementation... now the witness is reviewing."
- Show `bd log` to display the trail of events on the bead.

**If the agent doesn't pick up:**
- Don't panic. The hook check interval may be longer than expected.
- You can force it: check `gt hook conclave/refinery` to confirm the bead is there, then explain "in production the agent picks this up on its next cycle — let me nudge it" and re-trigger if there's a way, or just narrate what would happen.
- Have a fallback: if it's been 60+ seconds, show the audience the hook contents and the mail system, and say "the agent is working in its own worktree — let me show you what that looks like" and `gt rig status conclave` to show it's active.

**If mail doesn't arrive:**
- Check `gt mail inbox` in a different role context if possible.
- Show the bead log instead: `bd log` will show state transitions even if mail is delayed.

---

### Step 5 — The Ledger (~2 min)

**Commands:**
```sh
bd show <bead-id>
```

**What to say:**
- "Every action is logged. The ledger is the audit trail."
- Point out: who did the work, who reviewed it, when each step completed.
- "This isn't a snapshot — it's trajectory. You can see the full lifecycle of this work item. This is your CI log for agent work."
- If the bead completed fully (refinery did work + witness reviewed): celebrate it. "That's a real PR, reviewed by an AI witness, on a real project, triggered by a single command."
- If it's still in progress: that's fine too. "The work is underway — you can see each state transition. The system is deterministic in structure even though the agents are nondeterministic."

**If it fails:**
- `bd show` with wrong ID: `bd list` to find it.
- Bead still in early state: narrate the states it has been through. Even a partially complete bead demonstrates the flow.

---

## Post-Talk Checklist

- [ ] Stop the presentation server (Ctrl-C the `make start` process)
- [ ] `make demo-reset` to clean up demo workspace
- [ ] Leave conclave rig running (or stop if done for the day: `gt rig stop conclave/witness`, `gt rig stop conclave/refinery`)
- [ ] Close/complete the demo bead if it finished: `bd close <bead-id>`
- [ ] If the refinery created a PR, decide whether to merge or close it
