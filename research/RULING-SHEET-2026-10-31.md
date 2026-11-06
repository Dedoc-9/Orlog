# Ruling sheet, 2026-10-31 (PROPOSED; ruled the same day, below)

**Ruled (2026-10-31).** He ruled it (recorded whole in `rust-core/RULINGS.md`): A, B and D adopted; C adopted with an
explicit limitation; option (c) for the six files adopted on condition that it proves exact reversibility; the
corrections adopted where they implement adopted rulings, ZA7 withheld, ZA9 adopted as a test-scope constraint; the
debate's dispositions retained; REREAD-9 not yet authorized. His qualification: *"The final sheet must preserve these
dispositions without silently broadening them."* The text below is kept as it was proposed.


Every decision still open after his rulings G to L on REREAD-8, and after the ISPT-0 debate he asked for. Each item
has a recommended disposition with its reason; none is adopted until he rules it. The sections are kept apart, as his
consolidated draft asked: the debate's decisions (I), one Verðandi experiment (II), LAW-FORMAT-0 Phase 0 (III), and
what stays deferred (IV). In his words (the message that pasted the proposed sheet, kept in
`rust-core/messages/2026-10-31-his-consolidated-sheet.md`; corrected 2026-10-31, REREAD-9's NC14, his D7: this said
"his draft's words", and no record held them), this is *"a consolidated proposed ruling sheet, not a record of
decisions already made."*

## I. The ISPT-0 debate

The debate: a builder, an adversary, one answer each, then a judge who re-ran both sides' probes and its own check
(each twice, byte-identical). Its verdict is saved word for word outside the repository.

| item | recommended | what it means, and why |
|---|---|---|
| **I.1 ISPT-0** | **reject** | Archive it with its reductions. Its three obligations collapse to one commuting square (Hoare's 1972 data refinement; exact lumpability with probabilities); its physics names check nothing; Facultative Mutualism and Adventitious Symbiosis are assume–guarantee, conservative extension and gluing. Its object is not in Ørlǫg. No quantum or thermodynamic runtime, no ISPT gate |
| **I.2 glue verdicts on admission** | **adopt as a rule, non-decisional** | A glue verdict never decides an admission. That is Verðandi's present rule made standing (AGENTS.md: never let admission decide by a glue verdict "until the owner rules it"). Showing the verdict on the card is separate studio work in Verðandi, with its own checks; this ruling does not authorize it unless he says so |
| **I.3 one Verðandi scratch experiment** | **authorize, narrowly** | Section II. It is the one question in the debate the literature cannot answer for his mechanics |
| **I.4 DOCTRINE fork 9** (a rule that licenses derivations) | **defer** | Behind typed terminals and RUST-CORE-0. As proposed it would let computed footprints confer grounded standing, the shape of the defect T2 repaired |
| **I.5 a compositional identity** | **defer** | Only once a composition construct exists, and then as a manifest of component seals and the interface's seal, above the law seal. SPEC §9's law seal and COMPAT-0 untouched |

**What survived the debate** (the judge's form, MEASURED on one probe only; not shown to work generally):
1. **The envelope:** a component checked with every slot it reads but does not write left free over that slot's
   declared domain. With every write checked inside its domain each tick, any composition's traces, projected onto the
   component's slots, are traces of its envelope.
2. **May and must:** an envelope's alarm is a possible hazard; a gain stands only with a closed, replayable witness
   from inputs enumerated whole. On the probe, 49 of 50 envelope alarms and 10 of 13 proposed gains were spurious.
3. **Invariants owned by the interface:** an invariant inductive for the interface with every proposal left free holds
   for any set of components that use it. On the probe it held for the claim interface; the naive one broke it at 34
   steps.

**Dropped:** the physics names; ISPT's obligations as separate obligations; FM, AS and "Capability ≥" (a scalar
scorecard); the semilattice laws as a certificate; the fairness and cross-platform promises; any novelty claim for the
composition lattice; "pairwise checks are blind to order 3" (an artifact of the closed convention, MEASURED).

## II. Verðandi: one experiment

**Recommended: authorize** one isolated scratch experiment in Verðandi's graybox, testing the envelope check and
interface-owned invariants together. The one question: does the method find real composition hazards and certify useful
invariants in his own mechanics, without false claims of gain?

Conditions:
- **A written sheet first,** with the mechanics, their slots, declared domains and combining rules, and a falsifier
  for each guarantee. Candidates: rules 2's movers and rules 3's walls, targets and push, which already have twin
  implementations (`graybox/web/sim.js`, `graybox/tick_ref.py`), read-only.
- **Hand predictions before any run,** among them at least one predicted hazard (its tick, cell and objects).
- **Plants:** a writer outside its declared domain, refused by the per-tick check; the naive interface's breaking
  steps shown; the claim keys reversed (its certificate may say "order-free", never "the right mover won", as Urðr's
  voxtie showed).
- **Spurious alarms recorded apart from realized hazards;** a gain only with a closed, replayable witness.
- **Nothing in any tree:** no file, no gate row, no change to GLUE-0, CERT-0, STRICT-0, or any world. If the tick cannot
  play a scratch fixture without writing to the tree, the experiment stops and comes back.

## III. LAW-FORMAT-0 Phase 0

REREAD-9 is not authorized. His prior rulings stand: W14(c) is 91, the candidate limit, and REREAD-9 must try to write a
deeper valid line.

### III.1 W9's four open questions, with their exact text and witnesses

Each witness below is a whole law (the two header lines `orlog-law 0` and `(decimals fixed)`, then the clauses shown),
run through the checker here. Draft 9 (section 8) states each question; the independent verification
(`rust-core/W9-VERIFICATION-REPORT.md`) found (C) and (D).

**(A) `neg`, `abs`, `sqrt`.** The words: "a numeric operand of ⟨type⟩". They state two parts, both needing the operand.
Is "⟨type⟩ is numeric" also a part, made from the form alone?

| witness | the checker now (the part made) | the other reading (only the stated parts) |
|---|---|---|
| `(clause 1 0 (say (neg bool (rule "r"))))` | W9 at line 3 | W10 at line 3 |

Moves nothing: no plant, no corpus law, no verdict on R6's 10,000 mutants (MEASURED). **Recommended: only the stated
parts.** His principle under G: *"the checker must implement the adopted wording, not a more permissive interpretation
that happens to pass the existing corpus."* The words state two parts; the third is the checker's inference. The checker
then drops it, the witness is planted (W10 at line 3), and its undoing is shown to bite.

**(B) the comparisons, `==` and `!=`.** The words: "after promotion, one numeric type" (or "one type that is numeric,
bool or text"). Is an operand's own kind a part made when the other operand is underived, or is the kind checked with
the equality, once both are derived?

| witness | the checker now (per operand) | the other reading (with the equality) |
|---|---|---|
| `(clause 1 0 (say (< bool (lit bool 1) (rule "r"))))` | W9 at line 3 | W10 at line 3 |
| `(clause 1 0 (let 0 "x" (list-of (lit int 1) (lit int 2))))`, `(clause 2 0 (say (== bool (var 0) (rule "r"))))` | W9 at line 4 | W10 at line 4 |

Moves nothing (MEASURED). **Recommended: with the equality.** "One numeric type" is a property of the pair; nothing in
the words gives it to one operand alone. (For `+ - * / max min` the words go on, "which is ⟨type⟩", which gives each
operand its own part; the comparisons have no such clause.) Same principle as (A), and the same plant and undoing.

**(C) the type of a variable read in a rule's first define.** The underived list makes "an undeclared variable's type"
underived and does not say what undeclared means: (i) no clause declares the id; (ii) the variable is not in scope at
the define; (iii) the walk has not met its declaration by the define's clause. It shows only at a rule used on a line
before its first define.

| witness | (i) | (ii) | (iii), the checker now |
|---|---|---|---|
| V1: `(clause 1 0 (say (neg fix (rule "q"))))`, `(clause 2 0 (define "q" (var 0) - (over )))`, `(clause 3 0 (let 0 "y" (lit int 1)))` | W9 at line 3 | W10 at line 3 | W10 at line 3 |
| V2: `(clause 1 0 (say (neg fix (rule "q"))))`, `(clause 2 0 (if (arm 2 (lit bool 1) (let 0 "y" (lit int 1))) -))`, `(clause 3 0 (define "q" (var 0) - (over )))` | W9 at line 3 | W10 at line 3 | W9 at line 3 |

(The witnesses' (iii) and (i) columns were run here; (ii) is the verifier's.) What each costs:
- **(i)** is the words taken literally, and makes a variable's type order-free, as E2 made a rule's. But it needs a
  fixed point of its own: a variable's type can flow through rules back into itself. A first attempt here, taking an
  unmet variable's type from the last walk, never settles on 83 of R6's 10,000 mutants (the types cycle, and the
  checker's guard raises), where the checker settles on all (MEASURED). So (i) needs its least fixed point defined
  before its effect can be measured.
- **(iii)** is what the checker does, and it settles. It matches how variables are numbered and scoped: by the walk
  (E1, W8). But it is typing as met, which E2 rejected for rules.
- **(ii)** reads "undeclared" as W8's UNDECLARED. Not measured beyond the witnesses.

**Recommended: (iii), stated in the underived list,** because variables, unlike rules, are numbered and scoped by the
walk, and it is the one reading here measured to settle. If he prefers (i), order-free like rules, its fixed point is
defined and measured first, and the 83 mutants are the test. Either way V1 and V2 become plants.

**(D) which declaration types an id declared twice.** W8 refuses the second declaration, but a use on an earlier line is
reported first, and it may read the variable through a rule.

| witness | the checker now (the first declaration met) | the last declaration |
|---|---|---|
| V3: the use `(neg fix (rule "q"))` on line 3, `let 0` int, `let 0` fix, then `(define "q" (var 0))` | W9 at line 3 | W10 at line 3 |
| V4: the same with fix first, then int | W10 at line 3 | W9 at line 3 |

(The first column was run here; the last-declaration column is reasoned from the type each law would give q.)
**Recommended: the first declaration met,** stated in derivation 8. E1 already says the i-th declaration met has id i;
the first met is the one that holds the id. The checker does not change; V3 and V4 become plants.

### III.2 The six files that hold the home path

The four attempts' `runs.jsonl` (37–38 MB each) and the trial's two outputs are not kept yet. MEASURED: each
`runs.jsonl` holds the repository's absolute path 91,204 times and a path under `AppData\Local` 10 to 12 times, in
JSON-escaped form; each trial output holds one `AppData\Local` path, in its short 8.3 form. Both name his account. His
I asks for lossless retention; his standing rule keeps his home path out of the repository.

| option | what it does | cost |
|---|---|---|
| (a) keep them as they are, in the tracked tree | lossless; the account's name goes into the repository | needs his word that these files may carry it |
| (b) keep them outside the tracked tree | lossless; the manifest in the tree names each by length and sha256, and where he keeps it | a clone cannot check them without his copy |
| **(c) keep them in the tree, the account's prefix replaced by a token** | each spelling of the prefix (escaped, plain, 8.3) has its own token; the manifest records the original's sha256 and each token's count; `check` restores with the prefix it is given and requires the original's sha256 | lossless given the prefix, which is his to give; to be built and plant-tested before use |
| (d) keep only their sha256 | nothing kept | against his I |

**Recommended: (c).** It keeps the evidence in the tree, recoverable byte for byte, with no home path in it. Without
the prefix the check fails rather than passing. (b) is the simpler fallback.

### III.3 The disposition's items outside G to L

His scope sentence covered G to L only. Already done under a ruling: ZA1–ZA4 and ZA8 (G, H, L3), ZC2's wording (H),
ZB4 and ZC3's notes (L2), ZC10's quotation (L1), ZC1, ZC11 and ZB9 (I), ZB2, ZC4 and ZB11 documented (J), ZB10 and ZC9
(K). The rest, each with a recommendation:

| item | what it is | recommended |
|---|---|---|
| ZA5 | six plants: E1 for musts and claims; W9 whole-or-nothing in a binary, a unary, `item`, `list-of` | **apply**: plants and undoings only; they move nothing (reader 1, MEASURED) |
| ZA6 | E1's wording reads as one counter for three kinds | **apply**: "each kind numbered on its own" |
| ZA7 | E4's unbounded count overrides SPEC's `u64` unsaid; the other counters unstated | **apply** for the operation count, which E4 rules; **his** whether to extend it to the cost counters, claims' costs and evaluations, and the stop's printed count |
| ZA9 | W3's row has no pointer to section 10; where a writer plant goes | **apply** the pointer; **his** whether R7's writer plants go only in the writer's named code |
| ZB1 | Amendment 7 says `attempt.json` comes before any child process; the generator starts one first | **apply** an in-place note; the generator stays (pinned); the next generator fixes it |
| ZB3 | the runner's check misses the ENV line's completeness, the bytecode folders, the implementation and version | **apply** to the check alone (the runner is pinned); evidence made again |
| ZB5 | the variants make four of REREAD-6's five changes | **apply**: the fifth added, the record 15 of 16 |
| ZB6, AR-1, AR-2 | the start-failure count stops at one; a harness exception kept by type alone; `PYTHONUTF8` unrecorded | **record** as requirements of the next generator, under ATTEMPT-RECORD-0 |
| ZB7 | one of R2's 11 fixtures is neither out of order nor repeated | **apply**: "10 of the 11"; the pinned docstring noted, not changed |
| ZB8 | Amendment 7's "about four seconds" | **apply**: corrected in place; neither figure is a measurement |
| ZB12 | the failed attempt's two generations kept unevenly | **apply** wording ("generation 1 of `r6-reference-4`"), the two named side by side; no file moved |
| ZC5 | three of Y10's five in-place notes missing | **apply** the three notes |
| ZC6 | the Y9 note misstates its history | **apply** a further note |
| ZC12 | stale and colliding names in pinned code | **apply** a note in the sheet; the pinned files unchanged |
| W9 verification D5 | the element-type parts on a non-list variable | **apply** a wording clarification; no verdict depends on it |

### III.4 Before REREAD-9

| prerequisite | status |
|---|---|
| the checker follows E2 literally | built (G): six plants, four undoings, no R6 or R2b verdict moved |
| W9's parts explicit | enumerated and independently verified; waits on (A) to (D), then the checker made to follow the rulings, planted, and the evidence made again |
| section 7 complete | done (I, Amendment 8) |
| the 91 challenge prepared | drafted: search for a deeper line before reading the argument for 91, then try to break the argument |
| the six files | waits on III.2 |
| the items outside G to L | waits on III.3 |
| REREAD-9's briefs | `git status` only for named paths, with `GIT_OPTIONAL_LOCKS=0` (REREAD-8's disclosure) |

## IV. Deferred: not in this sheet's scope

- Rust-core implementation and production integration remain unauthorized; Python remains the reference authority.
- No gate or release change, commit or push.
- DOCTRINE fork 9 stays behind typed terminals and RUST-CORE-0; a compositional identity waits for a composition
  construct.

## V. The order

1. I.1 to I.5.
2. II, the experiment, if he authorizes it.
3. III.1, (A) to (D); then the checker made to follow them, planted, and evidenced twice.
4. III.2, the six files.
5. III.3, the items outside G to L.
6. III.4 checked whole; only then REREAD-9.
