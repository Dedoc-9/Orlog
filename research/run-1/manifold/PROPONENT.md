# The manifold debate: the proponent's record (2026-10-26, research only)

An outside reviewer suggested reading CUT-0 (`research/run-1/CUT-0.md`) as "manifold computing": a model of the
execution's state space, not a replacement for the deterministic contract, preferring a discrete configuration complex
to any continuous geometry. The proponent's task was to find out by measurement whether that view yields a real win,
and to say so plainly if it does not. Nothing here is ruled, built into `src/`, or committed.

**Written here, and nothing else:** `research/run-1/manifold/`'s `fibers.py`, `resume_oracle.py`, `make_laws.py`,
`laws/` (15 version-0 laws), the outputs `fibers.txt`, `fibers-timing.txt`, `resume_oracle.txt`,
`resume_oracle-search.txt`, `make_laws.txt`, and this record. No file under `src/`, the probes, `CUT-0.md` or any other
document was edited. No git command that changes anything was run. (`git status` showed `research/run-1/CONTRACT-DEBATE.md`
and `DESIGN-BRIEF.md` modified when this was written; neither was touched by this work.)

**The probes moved while this work ran.** `cut0_claims.py` and `cut0_session.py` were revised several times on
2026-10-26, in answer to the adversary's findings (`ADVERSARY.md`: F1 to F4, G1 to G7). Both scripts here import the
probes' own functions, and their final outputs were made against these versions, whose sha256 each output prints:
- `research/run-1/probes/cut0_claims.py` sha256 `de5682e1473c231c6505a961630a81af021e0e8f20ff081f080880375d0fc300`
  (reading S2: K passes every later refusal);
- `research/run-1/probes/cut0_session.py` sha256 `e46ad6bb1693d9bcf333b502588bd910f293904c8ff1edce9a0cac5518adaa86`.

Earlier exploratory runs against earlier versions are cited only where marked *(first form)*, and only for a fact the
final runs reproduce or that the first form alone had. A rerun against later versions may differ, and should.

**Order of reading.** The probes, CUT-0.md and the contract draft first; the measurements next; `ADVERSARY.md` only
after this record's measurements had run once (section 7 says where the two meet); `LINEAGE.md` last, when it appeared
(section 6). The adversary's scripts under `adversary/` were not opened.

**Grades.** MEASURED (ran; command and output); EXHAUSTIVE (every case of a declared finite domain); ESTABLISHED (read
in code or specification, file and line); DECLARED (argued); CONJECTURED. A source outside the repository is graded by
how it was read: *full text, in part* (the text itself, read in the places cited), *abstract*, or *secondary* (a search
summary, a catalogue entry, another paper's description), or *from memory, not re-read here*.

## 0. The answer

| criterion | met? | the number that shows it |
|---|---|---|
| (a) a missed aliasing or premature-completion counterexample | no | 0 unsound runs of the probe's K, under R1 and Rinf, in 88,950 refused runs (61,879 EXHAUSTIVE, 27,071 MEASURED); 0 session records collapsing two histories in 106,588 |
| (b) a smaller, demonstrably complete representation | yes, for the session's law-facing rows; not by geometry | 352 congruence classes for 65,442 histories at 6 events; 6,705 for 2.1 × 10¹² at 14; 0 congruence failures; 0 row differences under 13 plants |
| (c) a soundness argument for claim settlement | yes, as a DECLARED argument; not by geometry | a frame-by-frame simulation argument; its one reading-dependent step (the While bit) isolated by measurement: 96 of 96 first-form failures through a spent fuel check, 0 otherwise |
| (d) lower cost without fewer cases | yes, for the session's law-facing rows; no for the claims | 0.06 to 0.11 s over the classes against 9.2 to 17.0 s over every history, for the same rows of D1 (one host under load, OBSERVED); 14 events in 3 to 5 s |

**Verdict.** The manifold view does not earn a place as a method for CUT-0. Its one testable geometric claim, that
quotienting the session's histories by commuting events (dihomotopy, Mazurkiewicz traces) gives a smaller
representation, was measured. The quotient equals the plain reachable-state set, EXHAUSTIVELY on two domains (22,021
traces for 22,021 states; 16,395 for 16,395): the complex's directed homotopy is trivial. The claim side has no squares
at all. Everything that worked is classical and non-geometric:
- a bisimulation and symmetry quotient of the session (b, d);
- a stack-machine simulation argument (c);
- a resumption oracle with plants, which found no counterexample against the probe as it stands (a).

The view earned a place only as a prompt: its questions (what do the projection's fibers depend on; what
configuration does a cut leave) led to the abstraction and the oracle. These two instruments are worth keeping off
the gate. The word "manifold" adds nothing to them.

## 1. The survey: what "manifold computing" can mean, and what applies here

The phrase has no settled meaning. A search found it used for spatial computing (a field of devices read as an
approximation of a continuous medium) and as the name of an old coordination language; neither is about state spaces
(*secondary*). Five readings are worth weighing.

| reading | sources (how read) | what it is | applies to a single-threaded deterministic run plus host-scheduled arrivals? |
|---|---|---|---|
| computation on a geometric manifold | Riemannian optimisation, geometric deep learning (*from memory*) | numbers living on a smooth manifold | no: every state here is a finite symbolic object |
| manifold learning | Tenenbaum, de Silva and Langford, Isomap, *Science* 290 (2000); Roweis and Saul, LLE, same issue (*abstract, secondary*) | low-dimensional smooth structure recovered from samples in a metric space | no: no metric, no samples from a smooth manifold, nothing to embed |
| directed algebraic topology: d-spaces, precubical sets, trace spaces, dihomotopy | Fajstrup, Goubault, Haucourt, Mimram and Raussen, "Trace spaces: an efficient new technique for state-space reduction", ESOP 2012, LNCS 7211, arXiv 1204.0414 (*abstract; full text, in part*: the language, the geometric semantics, the definition of dihomotopy, the index poset, the comparison with SPIN, the related-work paragraph); the same authors' book *Directed Algebraic Topology and Concurrency*, Springer 2016 (*secondary*); Grandis, *Directed Algebraic Topology*, CUP 2009 (*secondary*); Raussen, "Trace spaces in a pre-cubical complex", Aalborg R-2008-11 (*secondary*); Fajstrup, Goubault, Haucourt and Raussen, "Components of the fundamental category", *Appl. Categ. Struct.* 12 (2004) (*secondary*); Ziemiański, "Spaces of directed paths on pre-cubical sets", AAECC 2017, and part II, arXiv 1901.05206 (*secondary*); Goubault, "Geometry and concurrency: a user's guide", MSCS 10 (2000) (*secondary*: the issue's foreword only) | a program of n threads is a cube complex; its squares are pairs of actions that commute; two executions are dihomotopic when one deforms into the other across squares; a trace space is the space of executions modulo that | only where squares exist. The ESOP paper's programs are n threads with semaphores, and its reductions come from the holes mutual exclusion cuts in an n-cube. Its own related work reads persistent and stubborn sets as special cases of dihomotopy reduction, and the traces of trace theory as points of trace spaces. One thread gives a one-dimensional complex, and dihomotopy is equality of paths |
| higher-dimensional automata and asynchronous transition systems | Pratt, POPL 1991; van Glabbeek 2006, via Fahrenberg, Johansen, Trotter and Ziemiański, "Sculptures in concurrency", LMCS 2021 (*abstract, secondary*); Bednarczyk 1987, Shields 1985, Winskel and Nielsen, "Models for concurrency", 1995 (*secondary*) | the combinatorial form of the same object: states, transitions, and an independence relation whose squares commute | the session side only (section 2.3) |
| Mazurkiewicz traces and partial-order reduction | Diekert and Rozenberg (eds.), *The Book of Traces*, 1995, and Diekert and Métivier, "Partial commutation and traces", 1997 (*secondary*); Cartier and Foata 1969, the Foata normal form (*from memory*); Godefroid, *Partial-Order Methods for the Verification of Concurrent Systems*, LNCS 1032, 1996 (*secondary*: contents and descriptions); Flanagan and Godefroid, POPL 2005, and Abdulla, Aronis, Jonsson and Sagonas, POPL 2014 and J. ACM 64(4) 2017 (*abstract, secondary*) | words modulo commuting independent letters; one representative per class explored | the session side only, and section 2.3 measures that it buys nothing there |
| abstract interpretation of continuations | Cousot and Cousot, POPL 1977 (*from memory*); Van Horn and Might, "Abstracting abstract machines", ICFP 2010, arXiv 1007.4446 (*abstract*); Vardoulakis and Shivers, CFA2, LMCS 2011 (*abstract*); Reps, Horwitz and Sagiv, POPL 1995 (*abstract*); Bouajjani, Esparza and Maler, CONCUR 1997, pushdown reachability (*from memory*) | a continuation is a stack of frames; a sound analysis over-approximates what it can still do; "valid paths" return only to the actual caller | the claim side, directly: K is a forward reachability from one concrete stack, with exact call-return matching (the actual caller) and abstracted loop counters |

Also prior art for what sections 2 and 3 use, none re-read here: explicit-state model checking with a visited set
(Holzmann's SPIN); bisimulation minimisation (Park, Milner; Paige and Tarjan 1987); symmetry reduction (Ip and Dill
1996; Emerson and Sistla 1996); the Myhill–Nerode congruence; consistent cuts (Chandy and Lamport 1985, which CUT-0
cites); defunctionalised continuations and the CEK machine (Reynolds 1972; Felleisen and Friedman 1986).

**What applies, DECLARED from the definitions and supported by section 2's measurements.**
- **The claim side** is a deterministic, sequential interpreter with structured control and no recursion (ESTABLISHED:
  `src/orlog/sema.py` 182, 200-204; `src/orlog/syntax.py` 471-474, where an inline arm can be no If or loop). Given its
  inputs it has one execution. Its configuration complex has no squares, and the geometry reduces to the control
  structure. What remains is pushdown reachability from the cut's stack, which is what K is and what the oracle of
  section 3 tests.
- **The session side** has genuine squares: the host interleaves events that commute (an assignment and an unrelated
  arrival; two drops; assignments on two ports). It is the only place the directed-topology vocabulary has an object.
  Section 2.3 measures that its quotient by squares equals its quotient by end state: every two histories with one end
  state are one trace. In the vocabulary of the field, the trace space from the start to each state has one component.
  Dihomotopy then adds nothing to the reachable-state graph that explicit-state enumeration already gives.
- **"Singularities" (one step flipping an outcome)** are minimal pairs. CUT-0's probe already builds them by hand (a
  literal one apart); section 3 counts them over two families. No topology is needed to find or use them.

## 2. The session: fibers, quotients, and a smaller complete representation (`fibers.py`)

Every transition, projection, receipt core, session record and row below is `cut0_session.py`'s own function,
imported. The domains are declared finite (EXHAUSTIVE over each):
- **D0:** no each-tick port, every legal history to 5 events (11 histories; the adversary's G1, since repaired);
- **D1:** the probe's own, one port, arrivals among `1`, `1.1`, `4`, `13`, to 6 events (65,442 histories under the
  current δ, where after a refusing tick only the end may follow);
- **D2:** two ports, arrivals among `1` and `1.1`, to 6 events (41,135 histories).

Each arrival carries the probe's default source label, so the sources (the adversary's G5) are not varied here.

### 2.1 The fibers, and the records that must tell things apart (EXHAUSTIVE, `fibers.txt`)

| | D0 | D1 | D2 |
|---|---|---|---|
| histories | 11 | 65,442 | 41,135 |
| distinct input logs = distinct receipt cores | 11 | 13 | 7 |
| distinct session records | 11 | 65,442 | 41,135 |
| largest log fiber | 1 | 55,756 | 35,439 |
| core fibers holding two execution outcomes | 0 | 0 | 0 |
| session-record fibers holding two histories | 0 | 0 | 0 |
| log fibers holding two disposition vectors | 0 | 13 of 13 | 5 of 7 |
| NOT-RUN logs whose fiber mixes two reasons for the missing value | 0 | 2 of 2 | 2 of 3 |

- **No record collapses what it must separate.** The core is injective on logs, because it binds the log's sha256. The
  session record is injective on histories. No core fiber holds two execution outcomes (status, ticks, ops, executed,
  tick-ops, the `'T'` events, the tick lines).
- **What the log forgets is by design** (CUT-0 §3: a result that depends on a refusal reads the history). It forgets
  each arrival's disposition, the number of refusals, and why a NOT-RUN tick's port had no value. Classified per
  history, by priority:
  - **withheld:** an accepted arrival was never disposed;
  - **dropped:** the host dropped one;
  - **refused:** only refused arrivals since the last tick ran;
  - **none:** nothing arrived.

  | domain | NOT-RUN histories | withheld | dropped | refused | none |
  |---|---|---|---|---|---|
  | D1 | 4,386 | 4,113 | 252 | 10 | 11 |
  | D2 | 5,123 | 2,841 | 670 | 1,045 | 567 |

  All of them write the one cause `INPUT-MISSING`. Under A2 the cause field carries no information beyond tick and
  port: one value in every NOT-RUN log of both domains. Two of these collapses were known: Round D's headline (late,
  refused, host-withheld) and the adversary's G7 (a drop reads as a missing input). The counts are new. Each such
  history has a session record of its own, so the history tells all four apart, as CUT-0 intends.
- **No history-aliasing counterexample was found** (criterion (a), for the session): every pair of histories the
  contract must tell apart has two session records, and every pair with two execution outcomes has two cores.

**Which record determines which quantity** (the shape of Urðr's `inputset`, LINEAGE.md §2.3; EXHAUSTIVE over D1 and
D2):

| quantity | determined by the input log | by the session record |
|---|---|---|
| the receipt core, and every execution fact in it | yes (the core is a function of the log; 0 fibers with two) | yes |
| each arrival's disposition | no: 13 of 13 log fibers (D1), 5 of 7 (D2) hold two vectors | yes |
| the number of refused arrivals | no: 10 of 13 (D1), 5 of 7 (D2) hold two | yes |
| why a NOT-RUN port had no value | no: 2 of 2 (D1), 2 of 3 (D2) mix reasons | yes |
| the order of commuting events (section 2.3) | no | yes |

### 2.2 Logs the parser accepts that no history projects (EXHAUSTIVE within bounds, `fibers.txt`)

The strict parser's language, for logs of at most 2 ticks over the domain's accepted values, was compared with the
projection's image: every history up to 9 events (one port), 13 (two ports, A2) or 15 (two ports, A1). These bounds
reach every log of 2 ticks. The image is computed on section 2.5's abstraction, which is checked to be a congruence.
- **Under A2, the INPUT-REFUSED cause no longer appears.** It was accepted by the parser and was the projection of no
  A2 history (*first form*; the adversary's G3). It is now refused under A2, and this measurement finds it gone.
- **The G6 repair opened a new class.** δ now ends a session's ticks at a refusing tick. The parser does not run the
  law, so it still accepts logs that go on past one. Measured:
  - one port, A2: 21 logs accepted, 8 of them no history's projection, all of this kind;
  - two ports, A2: 84 accepted, 44 of this kind;
  - the smallest is `t 1 0000000400000000` then `t 2 0000000100000000` (tick 1 refuses TICK-BUDGET);
  - two ports, A2, with an end record: `t 1 0000000400000000 0000000100000000` then `end 1 not-run 2 INPUT-MISSING a`.

  Each executes, and a receipt core is written for it. CONTRACT-DRAFT §4.4 says later records "are not read", so its
  status is the refusing tick's, while its `input-log-sha256` differs from the reachable log's.
- **Minor finding, MEASURED: a receipt core is written over a log no session can write.** The core does not alias
  anything. Only `verify_session`, given a history, refuses the log. Either the contract accepts that a receipt
  attests a run and only a session record attests a session (CUT-0 §3 already says so), or the log grammar ends at a
  refusing record. The second requires the parser to run the law, so the first is the cheap reading. This is not
  claimed as a win: the adversary's G6 and the probe's revision produced the class, and this record measured it.
- **Under A1:** INPUT-REFUSED is reachable, and the only unreachable class is the same past-refusal class: 12 of 28
  logs (one port), 72 of 126 (two ports, every history to 15 events). At 13 events, four two-port logs ending in
  `not-run 3 INPUT-REFUSED b` were still unreached. A refused b on tick 3 needs 15 events, so the bound was raised and
  said (MEASURED, `fibers.txt`).

### 2.3 The two quotients the reviewer's view offers, and the one the contract needs (EXHAUSTIVE)

The configuration complex of the session has the states as vertices and the events as edges. Its squares come from a
static, symmetric, irreflexive independence relation on event letters (ESTABLISHED: `fibers.py` `independent`):
- assignments on two ports;
- drops of two arrivals;
- an assignment and an unrelated drop;
- an arrival and an assignment or drop of another arrival;
- an arrival or a drop with a close that ran its tick.

A close that ends the session or whose tick refused commutes with nothing. Every square was checked as a diamond:
both orders legal, one end state, the letters kept. Then three quotients of the histories were counted:

| | D1 | D2 |
|---|---|---|
| histories | 65,442 | 41,135 |
| squares checked as diamonds / failed | 99,642 / 0 | 55,448 / 0 |
| end states (the complex's vertices) | 22,021 | 16,395 |
| Mazurkiewicz traces (histories modulo squares; Foata normal form) | 22,021 | 16,395 |
| contract observations (arrivals with door results, dispositions, input log) | 22,021 | 16,395 |
| traces whose histories reach two end states / end states reached by two traces | 0 / 0 | 0 / 0 |

**The three quotients coincide, EXHAUSTIVELY on both domains.**
- Two histories are one trace exactly when they end in one state, and exactly when the contract observes the same
  thing of them.
- In the field's terms, the trace space from the start to each reachable state has one component: the directed
  homotopy of this complex is trivial.
- So dihomotopy, trace spaces and partial-order reduction add nothing here beyond the reachable-state graph, which
  explicit-state enumeration already gives.
- The squares are real (99,642 of them), but they do not cut the state space below the states. They only identify
  histories that already end in one state.

**What a trace quotient would cost the audit trail (MEASURED).** 12,525 traces in D1 (largest 20 histories) and 7,772
in D2 hold two or more histories, and each history has its own session record. The smallest pair, one trace and two
records:
- `arrive(a,1) assign(0,1) arrive(a,1)`
- `arrive(a,1) arrive(a,1) assign(0,1)`

Binding the trace instead of the history would forget the host's schedule: whether it assigned before or after an
unrelated arrival came, whether a close came before or after an arrival it did not consume. CUT-0 §3 records that
schedule on purpose ("a different schedule is a different history"). No disposition, no outcome and no log depends on
it (the table above), so the cost falls only on what the history attests about the host's timing.

### 2.4 Every row but the binding is a function of the end state (EXHAUSTIVE, under every plant)

For each history, the rows of `check_run` (the session binding aside) were compared with the rows of one
representative history of its end state. This was done unplanted and under each of the probe's 13 plants, on D1 to 6
events and D2 to 5 events: **0 histories differ** in all 28 comparisons.
- The plants that turn any row red on these domains are 4 of 13 on D1: `hold-previous` (354 histories, through
  `no-value-invented`), `budget-uncounted` (1,258), `end-anytime` (3,393) and `no-cause` (4,913).
- On D2 the count is 2 of 13: `end-anytime` (248) and `no-cause` (918).
- The others are caught only by the probe's named cases. The adversary's G4 reported the same for the probe's first
  nine.
- The session binding (`session-binds`) is the one row that reads the history itself. It failed on no history.

### 2.5 A smaller, demonstrably complete representation for the law-facing rows (criterion (b), MEASURED)

**The abstraction** (`fibers.py` `akey`) keeps only what the input log's future depends on:
- the open tick, the records, the outcome and the refusing tick;
- each filled slot's port and door result;
- the multiset of assignable arrivals' (port, door result).

It forgets arrival numbers, refused arrivals (under A2), disposed arrivals, sources and the order of every event.

**It is checked to be a congruence:** all states of one class have one input log and one multiset of (abstract event,
abstract successor). It was checked on every concrete state with fewer than 7 events unplanted (22,021 in D1, 16,395 in
D2); with fewer than 6 (D1) or 5 (D2) under each of the 13 plants; and with fewer than 5 under A1. There were 0
failures. That is the Myhill–Nerode condition for
the map history ↦ input log (prior art; and the owner's own prose note, section 6).

**Two consequences, each MEASURED:**
- **Completeness for the law-facing rows.** The 11 rows of `check_run` that read only the log (projection, round trip,
  execution, statuses, the `'T'` and tick-line identities, the budget, the counts) give each history exactly its class
  representative's failures: 0 differ, unplanted and under the 13 plants. The plants `budget-uncounted` and
  `no-cause` turn log rows red on 1,258 and 4,913 histories, and the classes report them exactly.
- **Counting without enumerating.** Each abstract edge carries its multiplicity, consistent within a class by the
  congruence. The number of histories is then a weighted path count on the classes: 65,442 for D1 at 6 events and
  41,135 for D2, each equal to the enumeration.

| domain, events | histories (counted) | concrete states | abstract classes | log rows failed |
|---|---|---|---|---|
| D1, 6 | 65,442 | 22,021 | 352 | none |
| D1, 7 | 507,430 | 110,566 | — | none (on the states) |
| D1, 8 | 4,090,552 | — | 918 | none |
| D1, 10 | 294,046,539 | — | 1,995 | none |
| D1, 12 | 23,760,658,653 | — | 3,826 | none |
| D1, 14 | 2,127,136,532,008 | — | 6,705 | none |
| D2, 6 | 41,135 | 16,395 | 111 | none |
| D2, 12 | 8,460,128,379 | — | 616 | none |

**Cost (OBSERVED on one host, a software timing with the machine under other load; stderr only, `fibers-timing.txt`).**
Running `check_run` once per history of D1 to 6 events took 9.2 s and 17.0 s in the two recorded runs. Once per
concrete state it took 3.3 s and 6.1 s, and once per abstract class 0.06 s and 0.11 s. The abstract graph to 14 events
took 3 to 5 s, while enumerating its 2.1 × 10¹² histories is out of reach. The ratio, roughly 150 to 1 between histories and
classes at 6 events and growing with depth, is the claim. No absolute time is.

**What it does not cover.** Only the 11 log rows are complete on the classes. The rows that read the history
(`door-replays`, `no-assignment-disappears`, `one-disposition-each`, `no-value-invented`, `session-binds`) need the
concrete states, which section 2.4 shows suffice for all but the binding. The binding needs the histories. The
congruence is EXHAUSTIVE to 7 events and ESTABLISHED beyond by reading `Session.step` and `legal_moves`
(`cut0_session.py` 92-167): they read only slots, the referenced arrival's port and door result, membership in
`disposed`, the tick, the records, the outcome and `refused`. Each of these is in the class key, or is erased by it
uniformly.

**Is it a win, and whose?** It meets (b) and (d) for the session's law-facing rows. It is bisimulation and symmetry
reduction (prior art: Paige–Tarjan, Ip–Dill, Emerson–Sistla; *from memory*), found by asking the reviewer's question
"what do the fibers of the projection depend on". It owes nothing to geometry. Section 2.3 is the geometric quotient,
and it is no smaller than the states.

## 3. The claims: a resumption oracle for K

### 3.1 The oracle, and why it models "the refusing operation returned" (`resume_oracle.py`)

**Construction (ESTABLISHED, `resume_oracle.py` class `Resumed`).** The probe's own `CutInterp` (the reference
interpreter with its frames recorded, itself checked against the reference by the probe) is subclassed once more. Its
first refusal records the cut exactly as `CutInterp` does and then, instead of raising, returns:
- an integer arithmetic refusal (`numeric_ref` raising inside `Interp.num`: DIVISION-BY-ZERO, INEXACT-DIVISION,
  OVERFLOW) returns a value v;
- INDEX-OUT-OF-RANGE in `item k of xs`, for a list of integers, returns v;
- CLAIM-REFUTED and MUST-FAILED return after their statement's evaluation, which had completed;
- FUEL-EXHAUSTED returns, and the reference's own While goes on to the pass the check guarded.

Any other refusal at the cut raises `Unmodelled` and the run is set aside and counted (none occurred in either family).
After the cut, nothing is simulated: the reference's own code runs on, with one value substituted. The claims evaluated
after the cut are read from the trace's `'C'` events emitted after it, so the completion of an evaluation open at the
cut counts as one.

**Three readings of what follows the cut.** The question is what a later refusal does in the hypothetical run.
- **R1:** a later refusal ends it. This was the probe's first form (reading S1).
- **Rnofuel:** every later refusal returns too, FUEL-EXHAUSTED excepted.
- **Rinf:** every later refusal returns, each value refusal with the same v. This is the probe's reading S2 since its
  revision of 2026-10-26 ("every later refusal also read as passable", `cut0_claims.py` docstring).

**Over which values (DECLARED, with a measured check).** "Returned with any value" is an unbounded set. The oracle
uses V = {−2, −1, 0, 1, 2, 3, 4, 9}, so it under-approximates the hypothetical continuation. A claim it finds after
the cut and outside K is a true counterexample; a claim it never finds proves nothing beyond V.
- In family E the returned value flows only into `y`, which E never reads. So one value is as good as all, and the
  measurement checks this: the R1 sets for v = 0 and v = 1 are equal on every cut of E.
- In family G, `y` is read only by the atoms `y is positive`, `y equals 1` and `For each … from 1 to y`. V meets every
  class those atoms cut the integers into: negative odd and even, 0, 1, 2, 3, and a value (9) that runs a For past every
  c the family uses.
- Values flowing on through `x` are not substituted, so V is complete for G's direct reads of `y` and no more.

**Termination.** A While whose fuel check returned can run without bound; every resumption has a host budget (5,000
counted operations). PO-10's lesson, from the lineage (section 6), is that a bounded exploration must say it is
bounded. So a resumption stopped by the budget is rerun at half the budget, and the record counts those whose claim
set still grew in the second half.

**Validity rows, on every run of both families (MEASURED, section 3.3):**
- `CutInterp` and the plain `Interp` agree on receipt, trace and host stop;
- on a completed run, the resumed interpreter writes the reference's receipt;
- before the cut, the resumed run's trace equals the plain reference's, event for event;
- its cut equals `CutInterp`'s, frame for frame: clause, kind, loop bit and arm;
- this script's copy of `continuation` equals `cut0_claims.continuation`, unplanted and under each of the probe's six
  plants that move K. The copy exists only to carry plants of its own.

**The oracle's own plants (each must fail a hand-worked case, MEASURED):**
- `no-resume`: the oracle stops at the cut;
- `one-value`: V = {1};
- `abandon-statement`: the refusing statement is skipped whole, a plausible wrong model of "returned".

**Hand-worked cases.** These carry, worked by hand before running, the claims some R1 and some Rinf resumption
evaluates after the cut:
- 18 of the probe's 19 cases: C1 to D11, F1, F1′, A23, A23′ and A09. L1, added to the probe for its `shallow-reach`
  plant after this table was written, is not among them;
- two of this record's own, VAL and FUELOUT.

### 3.2 The families

- **E, EXHAUSTIVE over a declared grammar.** Each law is `Let x be 0`, `Let y be 1`, `To p` with a body of one or two
  leaves, then two statements, each from a set S1 of 38.
  - The leaves are `Increase x by 1`, `Set y to (x minus c) divided by (x minus c)` (refusing when x = c) and
    `We claim that x is at least 0`.
  - S1 holds the leaves, a For of 2 passes over 1 or 2 leaves, a `While x is less than 3, at most 2 times` over 1 or 2
    leaves, an If and Otherwise of one leaf each, an inline If with an inline claim and an inline refusing Set, and
    `Perform p`.
  - That gives 17,328 laws, each run at c = 0 … 6: 121,296 runs, of which 61,879 refuse.
- **G, MEASURED.** 10,000 laws drawn with `random.Random(26102026)`, each at c = 0 … 6: 70,000 runs, of which 27,071
  refuse. They are size-bounded (at most 32 clauses) and hold:
  - procedures p, q and r, each performing those before it;
  - For loops with literal bounds, with the bound `y`, and with a refusing bound;
  - While loops with literal and refusing conditions and fuel 1, 2, 3 or 5;
  - If, Otherwise if and Otherwise chains, and inline If, inline Otherwise and Unless arms;
  - refusing conditions in any arm;
  - inline claims, open-able claims, refutable claims and Musts;
  - `item (x plus 1)` of a list of c ones.

  Refusals at the cut: DIVISION-BY-ZERO 11,701, FUEL-EXHAUSTED 9,351, INDEX-OUT-OF-RANGE 2,304, CLAIM-REFUTED 2,161,
  MUST-FAILED 1,554. None unmodelled, none stopped by the host.

### 3.3 Results (`resume_oracle.txt`; E EXHAUSTIVE, G MEASURED)

| | E | G |
|---|---|---|
| refused runs | 61,879 | 27,071 |
| validity: CutInterp ≠ plain reference; resumed receipt ≠ reference; trace before the cut ≠; cut ≠; copy of K ≠ probe's (and under its 6 plants) | 0; 0; 0; 0; 0 (0) | 0; 0; 0; 0; 0 (0) |
| R1 sets that depend on the returned value | 0 (y is never read) | 3,637 |
| resumptions stopped by the budget (under R1); of them still growing at half the budget | 148,344 (28,280); 0 | 42 (0); 0 |
| claims at the cuts | 110,476 | 82,373 |
| **K (reading S2): runs with a claim evaluated after the cut outside K, under R1 / Rinf** | **0 / 0** | **0 / 0** |
| **claims K holds that some resumption evaluates again, R1 / Rinf** | **0 / 0** | **0 / 0** |
| the first form: runs unsound under R1 / Rinf | 0 / 0 | 0 / 96, all 96 through FUEL-EXHAUSTED alone |
| claims the first form holds and K withholds (evaluated again under Rinf) | 0 | 226 (109) |
| claims K holds and the first form withholds (evaluated again under Rinf) | 0 | 2 (0) |
| held: by K / by the first form / by the oracle under R1 / under Rinf | 12,183 / 12,183 / 12,183 / 12,183 | 10,806 / 11,030 / 14,582 / 12,055 |
| claims K withholds (completed true, not open) that no Rinf resumption evaluates again | 0 | 1,249 |
| the same under R1 (of them reached only past a later refusal) | 0 | 3,776 (2,527) |
| cuts at a refuted claim (in K as open, harmless) | 0 | 2,161 |
| K a function of the descriptor within a law: classes holding two K, with the id / without it | 0 / 0 | 0 / 0 |
| one literal apart: claim pairs; K flips; the Rinf oracle flips; both; K alone; oracle alone | 87,665; 328; 328; 328; 0; 0 | 56,172; 2,231; 2,688; 2,148; 83; 540 |

**What this shows.**
- **K is sound on both families under both readings** (criterion (a) not met: no premature completion was found in K
  as it stands). The validity rows, the oracle's three plants and the ten unsound plants of K are what give the zero
  its meaning. Every unsound plant is caught on these families, in G by 96 to 9,967 runs each:

  | plant | runs caught, E | runs caught, G |
  |---|---|---|
  | `no-open` | 0 | 928 |
  | `header-bit` | 28,070 | 2,262 |
  | `while-bit` | 0 | 96 |
  | `top-after-missing` | 4,170 | 6,203 |
  | `outer-loop-never` | 1,310 | 1,506 |
  | `refused-arm-only` | 0 | 356 |
  | `proc-empty` | 283 | 3,703 |
  | `else-missing` | 1,266 | 2,314 |
  | `no-return` | 101 | 2,508 |
  | `depth-cut` | 6,178 | 9,967 |

  The three precision plants each enlarge |K − O(Rinf)|: in G, from 12,542 to 14,152 (`context-free`), 14,258
  (`no-count`) and 12,585 (`all-arms`).
- **The first form's one failure is F1**, which the adversary reported and the probe's revision repaired. An
  exploratory run of this oracle on the first form found the same class before `ADVERSARY.md` was read: 119 Rinf-only
  runs in an earlier draft of G, every one through a spent fuel check. That run's output is not part of this record,
  so it is OBSERVED. It classified the class as "beyond CUT-0's definition", which held then only under reading S1. It
  was not called unsoundness, so credit for the counterexample is the adversary's. Under R1 the first form is sound
  (0 runs on both families), and under Rinf it fails only through FUEL-EXHAUSTED: Rnofuel gives 0.
- **The price of reading S2, MEASURED.** In G, K withholds 226 claims the first form held. 109 of them are evaluated
  again under Rinf, which is the repair working. 117 are evaluated again by no Rinf resumption, which is the repair's
  cost. `laws/fuel-bit.orl` and `laws/s2-price.orl`, one literal apart, are the two kinds at five clauses. The arm
  refinement (F3) gains 2 claims, neither evaluated again.
- **K's precision is the gap to the oracle.** Under its own reading (Rinf), K withholds 1,249 claims in G that no
  resumption reaches: conditions after the cut, a While's condition, guards like D08. The oracle is the ground truth a
  value analysis would have to reach to recover them. CUT-0.md already declares this conservatism.
- **The descriptor is complete on these families.** Within each law, K is a function of the probe's descriptor, with
  or without the claim's id. F2's aliasing needs two open-able claims in one clause's two arms. G produces such
  clauses, but no c-sweep in G put two different open claims at one descriptor with different K. The hand-built pair
  `laws/desc-alias-0.orl` and `-2.orl` shows F2 directly (section 4). F2 is real and rare at random.
- **One literal apart** (the reviewer's "singularities"): of 56,172 claim pairs in G, K's verdict flips on 2,231. The
  oracle agrees on 2,148. K flips alone on 83 (its conservatism moving with the cut). The oracle flips alone on 540
  (genuine flips K is too coarse to see).

**Criterion (d) for the claims: not met.** The oracle costs more than K (|V| resumptions per cut, three readings). It
is a test instrument, not a cheaper analysis.

### 3.4 A soundness argument for K under version 0's control flow (DECLARED; criterion (c))

Let a run refuse with cut F = f₀ … f_m (outermost first), and let the refusing operation return. Every claim evaluation
the run then makes lies in one of five places, and K covers each.
1. **The rest of the top statement s_m.**
   - If s_m is a Claim, its evaluation completes. K adds the claim.
   - If s_m is an If whose condition refused (the frame records which arm's condition), that arm or a later one or the
     Otherwise may run. K adds `arms_from` that arm.
   - If s_m is a For or a While whose own clause refused (bounds, condition or fuel check), the next thing it guards is
     a pass. K adds the body.
   - A Perform's own operation cannot refuse in version 0. Every other statement holds no claim inside it:
     expressions and rules hold none (ESTABLISHED: `syntax.py` 675, `Define(name, e, proviso, overrides)`).
2. **The rest of each frame's block.** When f_i's statement completes, the next siblings of its clause run
   (`after(c_i)`, which skips absorbed Otherwise clauses: an If chain completes as one statement). A frame whose clause
   equals the frame below's is an inline arm statement, whose completion completes the If; K skips to that frame.
3. **Loop frames below the top.**
   - A For runs another pass exactly when its counter is below its bound. Both are fixed at entry, and the counter
     cannot be set (ESTABLISHED: `interp.py` 229-241; `sema.py` LOOP-VARIABLE). K's bit is exact.
   - Under S2 a While may always repeat. K adds its body whatever its bit says.
4. **Returns.** A procedure body that ends returns to the Perform on the stack, the actual caller, because there is
   no recursion (ESTABLISHED: `sema.py` 200-204). So a procedure instance is unique, and K adds `after` of that
   Perform's clause only.
5. **Procedures performed in the continuation.** `Reach.proc` follows every Perform. There is no recursion, so the
   memo's placeholder is never read before it is final.

Only one step depends on the reading: 3's While. Under R1 the lower While's bit is exact, because the next check
refuses FUEL-EXHAUSTED and R1 stops there. Under Rinf it is not exact, which is why the probe's revision dropped the
bit. Section 3.3 measures this dependence: the first form fails only under Rinf, and only through a spent fuel check.
The argument is a simulation argument over a stack machine. It is prior art in kind (pushdown reachability,
defunctionalised continuations), and nothing in it is geometric.

## 4. Every discrepancy, minimised into a version-0 law (`laws/`, written by `make_laws.py`)

No discrepancy against K as it stands was found, so nothing unsound needed minimising. The discrepancies there are:
- the first form's F1 class;
- K's precision gaps;
- the descriptor's F2;
- each unsound plant.

Each was minimised, by `resume_oracle.py search`'s delete-and-hoist minimiser on a family witness
(`resume_oracle-search.txt`) and then by hand. Each law below was worked by hand before it was run, and its reading is
frozen in `resume_oracle.py`'s `REGRESSION` table: K, the first form's K, O(R1), O(Rinf), the claims K holds, and the
plant it must catch. There are 15 laws and 15 checks, and all read as worked (MEASURED, `resume_oracle.txt`, "laws
15/15"). The files are UTF-8 with LF line ends, written in binary, with no CR byte. Each starts with a `Note:` line,
which version 0 skips.

| law (laws/) | the law, as a version-0 law of the requested kind | K / first form / O(R1) / O(Rinf) / held | it pins |
|---|---|---|---|
| `fuel-bit.orl` | §1 Let x be 0. §2 While x is less than 9, at most 2 times: §2.1 Increase x by 1. §2.2 We claim that x is positive. §2.3 Say 6 divided by (x minus 2). | {2.2} / ∅ / ∅ / {2.2} / ∅ | F1's class at five clauses: the first form held §2.2, and the probe now withholds it. It also catches the probe's own plant `while-bit` |
| `s2-price.orl` | `fuel-bit.orl` with its bound 9 changed to 2 | {2.2} / ∅ / ∅ / ∅ / ∅ | the price of reading S2, one literal from `fuel-bit.orl`. The first form holds §2.2 in both, and K withholds it in both. Only in `fuel-bit.orl` does any resumption evaluate it again, because here the next check reads 2 < 2 and leaves. Without the condition's value no rule over frames can tell the two apart |
| `later-refusal.orl` | §1 Let x be 0. §2 For each i from 1 to 2: §2.1 We claim that x is at least 0. §2.2 Say 1 divided by x. §2.3 Say 1 divided by x. | {2.1} / {2.1} / ∅ / {2.1} / ∅ | precision under R1: a certain later refusal stops every R1 resumption, and K ignores it (correct under S2) |
| `guard.orl` | §1 Let x be 0. §2 For each i from 1 to 3: §2.1 If i equals 1, we claim that x is at least 0. §2.2 Say 2 divided by (2 minus i). | {2.1} / {2.1} / ∅ / ∅ / ∅ | precision under both readings: the adversary's Round D D08, at four clauses |
| `refuted-open.orl` | §1 Let x be 0. §2 We claim that x is positive. | {2} / {2} / ∅ / ∅ / ∅ | K reads a refuted claim as open; harmless, since a refuted claim is never held |
| `desc-alias-0.orl`, `desc-alias-2.orl` | §1 Let x be 0 (or 2). §2 For each i from 1 to 3: §2.1 If i equals 1 plus x, we claim that 6 divided by (3 minus i) is positive; otherwise, we claim that 6 divided by (3 minus i) is positive. | K {#1} and {#0}; held {#0} and {#1}; descriptors `2. 2.1 2.1!` twice without the id, `…!1` and `…!0` with it | F2 in this record's vocabulary: one literal apart, opposite readings, one id-less descriptor |
| `plant-no-open.orl` | §1 Let x be 0. §2 We claim that (x minus 0) divided by (x minus 0) equals 1. | {2} / {2} / {2} / {2} / ∅ | the open evaluation completes (plant `no-open`) |
| `plant-header-bit.orl` | §1 Let x be 0. §2 While x is less than 3, at most 2 times: §2.1 We claim that x is at least 0. | {2.1} for all four | the fuel check returns into a pass (`header-bit`) |
| `plant-top-after-missing.orl` | §3 Set y to (x minus 0) divided by (x minus 0). §4 We claim that x is at least 0. (after Let x, Let y) | {4} for all four | the refusing clause's block goes on |
| `plant-outer-loop-never.orl` | §3 Increase x by 1. §4 For each i from 1 to 2: §4.1 We claim that x is at least 0. §4.2 Set y to (x minus 1) divided by (x minus 1). | {4.1} for all four | a For's remaining pass |
| `plant-if-first-arm.orl` | §2 If (x minus 0) divided by (x minus 0) equals 1: §2.1 Increase x by 1. §3 Otherwise: §3.1 We claim that x is less than 0. | {3.1} for all four | a refused condition may take a later arm (`refused-arm-only`) |
| `plant-proc-empty.orl` | §3 To p: §3.1 We claim that x is at least 0. §4 Set y to (x minus 0) divided by (x minus 0). §5 Perform p. | {3.1} for all four | a Perform in the continuation runs its body |
| `plant-else-missing.orl` | §2 While x is less than 3, at most 2 times: §2.1 Increase x by 1. §3 If x is even: §3.1 Increase x by 1. §4 Otherwise: §4.1 We claim that x is at least 0. | {4.1} for all four | the Otherwise arm after the cut |
| `plant-no-return.orl` | §3 To p: §3.1 Set y to (x minus 0) divided by (x minus 0). §4 Perform p. §5 We claim that x is at least 0. | {5} for all four | a procedure returns to its actual caller, which goes on |

"Worked by hand" means each column was derived from the reference's semantics before the law was run. For example,
for `fuel-bit.orl`:
- pass 2 refuses DIVISION-BY-ZERO at x = 2;
- under R1 the next check (x < 9, with the fuel of 2 spent) refuses FUEL-EXHAUSTED, so no pass follows;
- under Rinf that check returns, and pass 3 evaluates §2.2;
- the first form's lower While bit (fuel spent) excluded the body, so it held §2.2;
- reading S2 includes the body, so K withholds it.

The session side's minimal discrepancy is a log, not a law, and is given in section 2.2: `t 1 0000000400000000` then
`t 2 0000000100000000` under one port's signature.

## 5. The four criteria

| criterion | met? | the number that shows it | geometric? |
|---|---|---|---|
| (a) a previously missed history-aliasing or premature-completion counterexample | **no** | K: 0 unsound runs, under R1 and Rinf, in 88,950 refused runs (E 61,879 EXHAUSTIVE, G 27,071). The session: 0 record fibers with two histories, 0 core fibers with two outcomes, over 106,588 histories (D0 to D2). The first form's counterexample (F1) is the adversary's, and this record's oracle independently measures its class (96 runs in G, all through a spent fuel check). The one session discrepancy found (section 2.2, a receipt core over a log past a refusing tick) is non-surjectivity, not aliasing, and was created by the G6 repair | — |
| (b) a smaller, demonstrably complete representation | **yes, for the session's law-facing rows** | 352 abstract classes stand for 65,442 histories (D1, 6 events), and 6,705 for 2,127,136,532,008 histories (14 events). It is a congruence: 0 failures on every concrete state to 7 events. It is complete for the 11 log rows: 0 differences, unplanted and under 13 plants. Weighted path counts equal the enumeration | **no**: a bisimulation and symmetry quotient. The geometric quotient (traces) equals the states (22,021 = 22,021) and is not smaller |
| (c) a soundness argument for claim settlement under the allowed control flow | **yes, as an argument** (section 3.4, DECLARED), supported by the zero above and by 10 of 10 unsound plants caught | it rests on one reading-dependent step, the While bit, and the measurement isolates it: the first form fails only under Rinf and only through FUEL-EXHAUSTED (96 of 96) | **no**: a simulation argument over a stack machine |
| (d) lower analysis cost without reducing the explored cases | **yes, for the session's law-facing rows; no for the claims** | `check_run` on D1 to 6 events: 9.2 to 17.0 s over every history, 3.3 to 6.1 s over one representative per state, 0.06 to 0.11 s over one per class (one host under load, OBSERVED); 14 events in 3 to 5 s, against 2.1 × 10¹² histories that cannot be enumerated | **no**: the same quotient as (b) |

## 6. The lineage (`LINEAGE.md`, read when it appeared)

The judge asked whether the owner's earlier designs strengthen this case. They were not re-read here, so every
statement below is the lineage researcher's, graded *secondary* for this record.
- **The designs named by the owner do not strengthen it.** By LINEAGE.md's reading of their code (§1 and §2.9, 2.10,
  2.13, 2.14):
  - Q64 and DEEQN64's "certified geometric manifold" is a covariance eigenspace over telemetry, and the Rust gate
    certifies the frame count;
  - mcl-observer-runtime's "quotient topologies" are single-linkage partitions of embeddings;
  - the DUME line's "manifold" is a k-NN graph, an identity map or a placeholder;
  - dvsm-meta-kernel's lockstep is one drained buffer, and its S_ECHO binds state and no input;
  - SymFlow-DVSM-Lattice is rounding to a grid with most-recent-wins ingest;
  - DQSDv2's tree is empty.

  None models discrete histories, logs or continuations, so none bears on the four criteria.
- **What does bear, and is not geometric:**
  - **Ursprung's PO-10 harness** (LINEAGE.md §2.4) has the shape of section 3's oracle: an exact image under an
    abstraction, admissibility, no false CLOSED, and a plant that drops the bad block. Its unread `frontier_open` is why
    the oracle here counts resumptions stopped by the budget and checks whether their sets still grew. The result is in
    section 3.3.
  - **LINEAGE.md §4's suggested plant** (a reach cut off at a depth) is this oracle's `depth-cut`, caught. The probe
    has since added its own (`shallow-reach`).
  - **Urðr's `inputset`** (§2.3) decides "which record determines which quantity" by witness pairs. Section 2.1's
    determination table is that check, run on the session's domains.
  - **A prose note** in one of the owner's local folders (L16, LINEAGE.md §2.14, DECLARED there) defines history equivalence as
    "no intervention sequence can induce a divergence", a Nerode-style congruence. Section 2.5's abstraction is a
    measured instance of that congruence for the input log.

  Each strengthens a measured, non-geometric result. None strengthens the geometric reading.

## 7. Where this record meets the adversary's (`ADVERSARY.md`, read after this record's first measurements)

| the adversary's | this record | agreement |
|---|---|---|
| §1: the framing is decoration; the session's only geometric object is commuting arrivals, so the geometry would rebuild POR | section 2.3 measures it: the trace quotient equals the state quotient, EXHAUSTIVELY on D1 and D2, so even POR buys nothing below the states | agree, with a number |
| F1: the first form's lower While bit, unsound under S2 | its class measured here: 96 runs in G (119 in an exploratory earlier G, before reading F1, OBSERVED, classified as reading-dependent rather than unsound); sound under R1 and Rnofuel; repaired in the probe, 0 runs under the repaired K | agree on the fact; the counterexample and the repair are the adversary's |
| F2: the descriptor names a clause | rebuilt as `desc-alias-0/2`; rare at random (0 within-law collisions in G) | agree |
| F3: arms already read false | the revision's gain measured: 2 claims in G, neither evaluated again | agree |
| F4: the budget check at loop entry | the validity row compares CutInterp with the plain reference on every run: 0 differences in 191,296 runs | agree; repaired in the probe |
| G3: INPUT-REFUSED under A2 | repaired in the probe; section 2.2 measures that it is gone | agree |
| G6: a record the run never reads decides the tick bit | its repair (δ ends at a refusing tick) leaves logs past a refusing tick that the parser accepts and no session writes: 8 of 21 (one port) and 44 of 84 (two ports) | new, minor |
| G4: rows that cannot turn red | the same shape on the current probe: 4 of 13 plants turn a row red on D1, 2 of 13 on D2 | agree |
| G7: a drop reads as a missing input | counted: 252 of 4,386 NOT-RUN histories in D1, 670 of 5,123 in D2, are drops; all write INPUT-MISSING | agree, with counts |
| (b) not met; (d) available through a quotient by the projection | (b) and (d) met for the log rows, through a congruence finer than the projection's fibers (it must be, to step forward). This is not the 21 or 13 fibers of a fixed depth: the fibers are known only after enumerating every history, the classes before | the two records differ here, and the difference is the congruence |

## 8. How to rerun, and what was run twice

From the repository's root, each with `PYTHONHASHSEED=0 PYTHONUTF8=1` and `python -B`:

| command | output | time here | twice |
|---|---|---|---|
| `research/run-1/manifold/fibers.py` (stderr to `fibers-timing.txt`) | `fibers.txt` | about 5 minutes | stdout byte-identical (the timings differ, as timings do) |
| `research/run-1/manifold/resume_oracle.py` | `resume_oracle.txt`; exits 0 on its last line, `RESUMPTION ORACLE HELD` | about 7 minutes, 8 worker processes | byte-identical |
| `research/run-1/manifold/resume_oracle.py search` | `resume_oracle-search.txt` (the same check, then the minimised witnesses) | about 8 minutes | run once |
| `research/run-1/manifold/make_laws.py` | `make_laws.txt`, and `laws/` | a second | byte-identical; the laws' bytes unchanged by the second run |

- Each installed output opens with a header line giving its command and date. The captured stdout had CR LF line
  ends. The installed copies are normalised to LF; the byte-for-byte comparisons were made on the raw
  captures.
- Each script prints the sha256 of the probe it imports. The probe hashes above were read before and after each
  recorded pair, and were unchanged.
- Both scripts use the standard library only. `resume_oracle.py` uses `multiprocessing` and merges the chunks in
  order, so its output is the serial order's.
- **If the probes change again, a rerun will measure the new probes.** The validity rows (the copy of K against the
  probe's, under its plants) will say where a change moved K. Where the frames changed shape, `frames_key` and the
  plant hooks in `resume_oracle.py` may need the same change.

## 9. What this record does not show

- **Soundness of K beyond the families.** E is exhaustive over a small grammar; G is 10,000 sampled laws. The
  argument of section 3.4 is DECLARED, not checked by a proof assistant.
- **Coverage of the families.** Neither family uses texts, floats, fixed numbers, `Append`, `Remove`, item
  assignment, rules (`Define`), certificate or agreement oracles, or claims with premises. Their refusals at the cut
  would read as not modelled, and none occurred.
- **Completeness of the returned values.** They are under-approximated: V is complete for family G's direct reads of
  `y` only (section 3.1). A value flowing through `x` was never substituted.
- **Version 1.** NOT-RUN, LOG-OPEN and REFUSED inside a tick, where K is "the next tick", are DECLARED in CUT-0.md and
  untested here; version 0 has no tick block. The session model's execution is the probe's stand-in law.
- **The four executions.** Only the reference's frames exist. Whether the compiled backends can produce the same
  frames, bits, arms and ids is untested, as the adversary also says.
- **The session beyond its domains.** It was checked on one or two ports, two to four arrival values and one source
  label (G5's sources not varied), to 5 to 7 concrete events. The congruence beyond 7 events rests on the code reading
  of section 2.5. The parser-against-image comparison stops at 2 ticks.
- **Any timing as a measurement.** Every time here is OBSERVED on one host under other load.
- **The lineage's designs.** They were not re-read here; section 6 relies on LINEAGE.md's grading.
- **Novelty.** None is claimed. Every mechanism used is prior art named in section 1.
