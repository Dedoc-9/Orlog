# The manifold debate: the adversary's record (2026-10-26, research only)

The adversary's side of the debate on an outside reviewer's suggestion to apply "manifold computing" to CUT-0. It
attacks three things: the framing, CUT-0's continuation K̂ (`research/run-1/probes/cut0_claims.py`), and the session
model (`research/run-1/probes/cut0_session.py`). Nothing here is ruled, built into `src/` or committed. No file outside
`research/run-1/manifold/adversary/` and this record was written. The proponent's record and scripts
(`PROPONENT.md`, `fibers.py`, `resume_oracle.py`) were not opened before this record was written. No `LINEAGE.md`
existed when it was finished, so the lineage researcher's claims are not attacked here (see §1.6).

The probes are read as they stand on 2026-10-26. `CUT-0.md` was revised while this work ran; the revision read last
defines K as "the set of claims the run could still have evaluated, had the refusing operation returned with any
value and every later value been anything" (`CUT-0.md` line 49), states the invariant K̂ ⊇ K (line 61), and owes "the
adversary's multi-byte and two-port attacks on the session model" (§4). This record answers both.

Grades: **MEASURED** (run here, command and output given), **EXHAUSTIVE** (every case of a declared finite domain),
**ESTABLISHED** (read in code or text, file and line given), **DECLARED** (argued). Sources outside the repository
are graded by how they were read: *abstract or search summary only*, or *from memory, not re-read here*.

## Count by severity

| severity | count | findings |
|---|---|---|
| unsound | 5 | F1 (the While fuel bit), F2 (the cut descriptor), G1 (no each-tick port), G5 (no source in the history), G6 (a dead record decides the tick bit; version 1, DECLARED) |
| imprecise | 5 | F3 (If arms already passed), F4 (the instrument under a host budget), G2 (the door and Python's `$`), G3 (INPUT-REFUSED under A2), G7 (a host's drop reads as the player's missing input) |
| framing only | 3 | F5 (the probe's acceptance rows refuse its own promised gain), G4 (rows that cannot turn red), M (the manifold framing) |

**The most serious counterexample (F1):** `§1 Let i be 0. §2 Let d be 0. §3 While i is less than 10, at most 3 times,
do the following. §3.1 Increase i by 1. §3.2 We claim that i is at most 3, by the owner. §3.3 If i equals 3, say 1
divided by d.` CUT-0 holds §3.2 (true in 3 of 3). With `d` = 1, one literal apart, it withholds it, and the pass past
the fuel check refutes it (i = 4). The input that causes a refusal raises the claim's standing.

## How to rerun

From the repository's root, with `PYTHONHASHSEED=0 PYTHONUTF8=1` and `python -B`. Each output file opens with its
command and date. Every script reads the probes through their own functions, never a copy.

| script | output | what |
|---|---|---|
| `adversary/cont_oracle.py` | (a module) | the dynamic continuation oracle, written apart from K̂ |
| `adversary/k_attacks.py` | `k_attacks.txt` | 31 hand-made laws through `judge()` and the oracle |
| `adversary/k_fuzz.py 20000 20261026` | `k_fuzz-20000.txt` | 20,000 random laws through `judge()` and the oracle |
| `adversary/k_monotone.py 20000 7` | `k_monotone-20000.txt` | cut monotonicity over 20,000 random laws |
| `adversary/k_repairs.py` | `k_repairs.txt` | the instrument under a budget; the repairs of F1 to F4, each against the probe as its plant |
| `adversary/k_criteria.py` | `k_criteria.txt` | the probe's acceptance arithmetic on F2's pair |
| `adversary/s_attacks.py` | `s_attacks.txt` | wider domains, no port, the door, multi-byte edits, the rows against the plants, the record |
| `adversary/s_drop.py` | `s_drop.txt` | the host's drop and INPUT-MISSING |

`k_attacks`, `k_criteria`, `s_drop` and `k_repairs` were each run twice; the second output was byte-identical to the
first, headers aside (MEASURED). The two 20,000-law runs and `s_attacks` were run once.

*Noted 2026-10-26, later, by the release check (`adversary/RERUN.md`): the outputs above record the attack on CUT-0's
first form, before the repairs it caused, and six of them no longer reproduce on the repaired tree. They are kept as
written. Their current-tree reruns stand beside them as `*-current.txt`, each change tied to its repair. Three scripts
(`k_monotone.py`, `k_repairs.py`, `s_attacks.py`) carry dated compatibility fixes.*

### The oracle (`cont_oracle.py`)

It does not compute K̂. It runs the reference interpreter to its first refusal and, instead of stopping, lets the
refusing operation return a substitute value (one of 0, 1, 2, 3, −1, 5 and 2^32: both arms of most conditions), then
runs on and records which claims complete an evaluation after the cut. Two readings of "what follows":
- **S1, one return:** any later refusal stops the run;
- **S2, every refusal returns:** the run continues past every later refusal, bounded by a step budget.

Each substitute gives one real continuation, so the oracle **under-approximates** K. A claim that CUT-0 holds and the
oracle sees evaluated again is a counterexample under that reading. A claim CUT-0 withholds that the oracle never
reaches is only a candidate imprecision.

## 1. The framing

### 1.1 What the object is

- **The claim side** is a deterministic, sequential interpreter with structured control, no recursion (sema refuses
  it, `src/orlog/sema.py` lines 200-205) and bounded loops (ESTABLISHED). The question CUT-0 asks at a cut, "can the
  continuation still evaluate claim c?", is forward may-reachability from a concrete call stack, with loop counters
  abstracted to a bit. That is abstract interpretation (Cousot and Cousot, 1977) over a pushdown control structure: a
  `post*` from one configuration in the sense of pushdown reachability (Bouajjani, Esparza and Maler, 1997). Both are
  *from memory, not re-read here*.
- **The session side** is a labelled transition system over the events arrive, assign, drop, close and end. The input
  log is its image under a projection π that **erases** events (refused arrivals, drops) and forgets the order of
  arrivals relative to one another (ESTABLISHED, `cut0_session.py` lines 189-206).

### 1.2 Directed algebraic topology and trace spaces

**What it is.** Fajstrup, Goubault, Haucourt, Mimram and Raussen, *Directed Algebraic Topology and Concurrency*
(Springer, 2016): *table of contents and search summary only*. "Trace Spaces: an efficient new technique for
state-space reduction" (ESOP 2012): *abstract only*. An n-cube is n independent actions run concurrently. Two
executions are equivalent when one deforms into the other through such cubes (dihomotopy). A trace space is the
space of directed paths modulo that equivalence.

**Here it is decoration (DECLARED from the definitions).**
- A sequential deterministic program has no independent actions. Its directed space is one-dimensional: a directed
  graph with no 2-cells.
- Dihomotopy is then equality of paths. A trace space between two states is a discrete set, and for a deterministic
  program it has exactly one point.
- The machinery returns path enumeration, which `judge()` and the oracle already do.

**The one place it touches something real** is the session with several ports. Arrivals from different sources are
concurrent in the world, and two histories that differ by swapping arrivals on different ports (arrival indices
renamed) project to one log. That is Mazurkiewicz independence. It is usable as partial-order reduction (Godefroid,
1996, *from memory*). Goubault, Heindel and Mimram, "A geometric view of partial order reduction" (ENTCS 298, 2013;
*abstract only*), show that the geometric reduction and persistent-set reduction use persistent transitions in
essentially the same way. So the geometry, applied here, would rebuild POR. Use POR directly.

**What trace theory does not cover either.** π also **erases** events. A fiber π⁻¹(log) holds histories with any
number of refused retries and drops, so it is infinite and is not a Mazurkiewicz trace class. The structure that
matters is the kernel of an erasing projection. That is automata and transducer theory, not topology.

### 1.3 Configuration spaces and state complexes

Abrams and Ghrist, "State complexes for metamorphic robots" (arXiv cs/0307004; *abstract and search summary only*).
It builds a cube complex from a transition graph, with a cube for each set of commuting moves, and uses non-positive
curvature to prove geodesic (time-optimal) paths. Applied here (DECLARED):
- on the claim side there are no commuting moves, so the complex is the graph itself;
- on the session side its cubes are the commuting arrival squares of §1.2, and its normal forms are the trace
  monoid's (Cartier-Foata, *from memory*).

The reviewer's preferred "discrete configuration complex" therefore says nothing beyond trace theory.

### 1.4 Persistent homology and manifold learning

- **Persistent homology** needs a point cloud in a metric space and a filtration. These states are symbolic
  configurations with no canonical metric. Any metric is the analyst's choice, and the barcode then describes that
  choice.
- A search found no application of persistent homology to program state spaces or to verification (*search summary
  only*). The nearest hit applies topological features to failure-count time series of evolving software (Pita Costa
  and Galinac Grbac, ICPE 2017 companion, *search summary only*). It is not about state spaces.
- **Manifold learning** assumes samples from a smooth low-dimensional manifold. Here the space is finite and discrete,
  and there is no tangent space to learn.
- Both are decoration (DECLARED).

### 1.5 "Singularities that flip an outcome"

In a discrete system, a flip is a pair of adjacent configurations whose outcomes differ. The search the reviewer
describes is exactly the probe's one-literal-apart pairs and this record's `k_monotone.py`. F1 is such a flip: on one
run, the cut moves one statement later, from the division on pass 3 to the fuel check, and the claim goes from held to
withheld. It was found with an operational oracle and a six-clause law. It is a single edge, with no homological
content.

Di Zhang, "The Singularity Theory of Concurrent Programs" (arXiv 2510.25112, October 2025; *abstract only*; the page
does not say whether it is refereed). It treats deadlocks as attractors and livelocks as non-contractible loops, and
it is about concurrent programs. Version 0 has neither: loops are bounded by fuel, and there is one thread.

Herlihy, Kozlov and Rajsbaum, *Distributed Computing Through Combinatorial Topology* (2013; *from memory*). Topology
decides wait-free solvability for asynchronous processes with failures. RUN-1's host serializes every arrival, so it is
one process, and its protocol complex is trivial. This becomes relevant only if several hosts must agree on a tick's
contents, which is consensus and is not proposed.

### 1.6 The lineage claims

The owner asked that his earlier manifold designs in other repositories be weighed, and a separate researcher is
writing `LINEAGE.md`. It did not exist when this record was finished, so none of its claims is attacked here. A test
for any of them, stated before it is read: a design is relevant to CUT-0 only if it names a property of K̂ or of the
session that it decides, and exhibits a counterexample, or a proof, that the operational oracle and the exhaustive
enumeration here do not already give. Anything else is decoration by the same argument as §1.2 to §1.4.

### 1.7 The reviewer's four win criteria

| criterion | result | by what |
|---|---|---|
| (a) a missed aliasing or premature-completion counterexample | **met, not by the framing**: F1 (premature completion of a While's claim), F2 (two claims aliased by one clause), G1, G3 | a dynamic oracle, a random generator, structured edits |
| (b) a smaller, demonstrably complete representation | **not met**: the representation CUT-0 offers (a clause, one bit per loop, `!`) is not complete (F2); a complete one adds the open claim's id, and, for precision, the arm (F3) | — |
| (c) a soundness argument for claim settlement | the argument that works is a simulation argument of abstract interpretation (§2.6). It holds for version 0 only after F1's repair, and nothing in it is topological | — |
| (d) lower analysis cost without fewer cases | available, and not from topology. 68,476 histories have 21 distinct logs (MEASURED, `s_attacks.txt` §4), so rows that read only the log can be checked once per fiber. Several ports take POR | a quotient by π |

**Verdict on the framing:** decoration for this system. The usable pieces are classical: abstract interpretation and
pushdown reachability for K̂, trace theory or POR and a quotient by the projection for the session. Each
counterexample below was found without geometry.

## 2. K̂, broken

All readings below are `judge()`'s (the probe's own). The oracle's columns are in `k_attacks.txt`.

### Coverage of the requested constructs (MEASURED, `k_attacks.txt`)

| construct | laws | result |
|---|---|---|
| rule uses (Define): undefined at a Say, in a claim, in a For bound, in a While condition | A01-A04 | right; A04 withholds a claim no one-return continuation reaches (the top-While rule, see F1) |
| Musts | A05-A07 | right |
| Otherwise, if chains | A08-A10 | A09: imprecise (F3) |
| inline Perform in an If arm, an inline otherwise arm, an Otherwise, if arm | A11-A13 | right |
| procedures from loops; nested procedures; a procedure in a While | A14-A16 | A16: F1 |
| For bounds that are expressions, refuse, or run empty | A17-A19 | right |
| an If condition refusing on a loop's last pass | A20, A21 | right |
| a refusal in a procedure performed from an Otherwise arm | A22 | right |
| claims sharing a clause | A23, A23' | F2 |
| a While whose condition refuses | A24, A25 | A25: as A04 |
| the fuel bit against the probe's C6 | C6, A26, A26', A27, A27' | F1 |

### F1 (unsound): a While frame's fuel bit below the top

- **Rule attacked:** K̂ adds a While's body below the top only "if fuel remains" (`cut0_claims.py` lines 166-168),
  while a While on top adds its body "whatever the bit says" (lines 152-155, the C6 repair).
- **Minimal counterexample (MEASURED, `k_attacks.txt`, A27 and A27′):**

  ```
  §1 Let i be 0.
  §2 Let d be 0.
  §3 While i is less than 10, at most 3 times, do the following.
  §3.1 Increase i by 1.
  §3.2 We claim that i is at most 3, by the owner.
  §3.3 If i equals 3, say 1 divided by d.
  ```

  - With `d` = 0, the run refuses DIVISION-BY-ZERO on pass 3, cut `[3. 3.3 3.3]`, and §3.2 is **held**, true in 3 of
    3.
  - With `d` = 1, it refuses FUEL-EXHAUSTED at the fourth check, cut `[3.]`, and §3.2 is **withheld**, true in 3 of 3.
  - The completed evaluations are identical, and the hostile literal raises the standing.
  - The every-return continuation of the `d` = 0 run evaluates §3.2 again, with i = 4, and refutes it.
- **Expected against actual.** E2 asks whether the run "could still have evaluated" the claim. That question has one
  answer for both runs, since both stand before the same fuel check:
  - read with refusals as stops, neither run can make a fourth evaluation, and both should be held (C6 is then
    imprecise);
  - read with refusals passable, both should be withheld, and the `d` = 0 run is unsound.

  CUT-0 answers differently only because a different operation refused. The revised definition, "every later value
  been anything" (`CUT-0.md` line 49), reads most naturally as the second reading, the one the C6 repair itself needs:
  a refused guard that "returns". On that reading **K̂ ⊉ K**, and the stated invariant fails.
- **Scale (MEASURED):**
  - `k_fuzz-20000.txt`: of 59,383 claims in 12,548 refusing random laws, 2,754 are held by the cut. The one-return
    oracle evaluates none of them again: 0 S1 counterexamples. The every-return oracle evaluates 26 of them again,
    each with a spent While bit in its cut. No other S2 counterexample appears, and the probe never raised.
  - `k_monotone-20000.txt`: cut monotonicity (K̂ at an earlier point of the same run must contain K̂ at the cut) fails
    at 578 of 125,063 earlier points. Every failure has a spent While bit, and the shortest is the pair above, made
    by the generator.
- **Falsifying test and plant:** A16, A26 and A27 must read withheld, and `k_monotone` must find no violation. The
  plant is the probe as it stands: it holds all three, and `k_monotone` finds 578 violations.
- **Repair, measured (`k_repairs.txt` §2):** a While frame below the top may always repeat. That is the probe's own
  plant `no-count`, restricted to While.
  - A16, A26 and A27 become withheld.
  - The probe's 13 cases read as the probe requires.
  - None of the corpus's 108 claims changes.
  - `k_monotone` finds 0 violations.

  The alternative is to revert the C6 repair, which makes C6, A26′ and A27′ held. It is consistent, but it holds a
  claim whose next pass would refute it.
- **The same lever in version 1 is G6.**

### F2 (unsound as specified): the cut descriptor names a clause, not a claim

- **Rule attacked:** "What the court needs, and no more: the cut's frames, a clause and one bit for each loop, plus the
  open-claim mark" (`CUT-0.md` line 129), and `descriptor()` (`cut0_claims.py` lines 175-186).
- **Minimal counterexample (MEASURED, `k_attacks.txt` A23/A23′, `k_repairs.txt` §3):** one law, one literal apart:

  ```
  §1 Let xs be a list of 2 copies of 1.
  §2 Let c be true.                       (A23′: false)
  §3 For each i from 1 to 3, do the following.
  §3.1 If (i equals 1) equals c, we claim that item i of xs equals 1; otherwise, we claim that item i of xs equals 1.
  ```

  - Both runs have the descriptor `[3. 3.1 3.1!]`, refuse at the same clause with the same code, and have the same
    claim lines (each claim 1 of 1).
  - The readings are opposite: (held, withheld) and (withheld, held).
  - `judge()` is right on both, and the oracle confirms it.
  - A court that has only the descriptor cannot be. Either it withholds both claims, which gives R8's "possible"
    back, or it holds the wrong one in one of the two runs.
- **Falsifying test and plant:** the two descriptors must differ. The plant is `descriptor()` as specified.
- **Repair (MEASURED):** the open mark carries the claim's id: `[3. 3.1 3.1!1]` against `[3. 3.1 3.1!0]`.

### F3 (imprecise): an If chain's arms whose conditions already read false

- **Counterexample (MEASURED, A09):** an Otherwise, if condition refuses on a loop's last pass. K̂ adds every arm,
  including the first, whose condition has just read false and cannot run. Its claim is withheld, and no continuation
  reaches it.
- **Repair (MEASURED, `k_repairs.txt` §5):** the If frame records which arm's condition refused, and K̂ takes that
  arm onward.
  - A09 is held.
  - The 13 cases are unchanged.
  - Over the corpus and these cases, one claim is gained and none lost, and the gained claim is checked by the
    oracle: 0 evaluated again.
- **Test:** A09 must read held. The plant is K̂ with every arm.

### F4 (imprecise: the instrument): the instrumented reference skips the budget check at For and While

- **Rule attacked:** "every receipt it writes is checked byte for byte" and "the same host stops as the reference on
  all 356 runnable texts" (`CUT-0.md` §2). `CutInterp.stmt` replaces the reference's For and While (`cut0_claims.py`
  lines 58-84) and so skips `Interp.stmt`'s check `ops > budget` at their entry (`src/orlog/interp.py` lines
  151-152).
- **Counterexample (MEASURED, `k_repairs.txt` §1):** `§1 Let x be 1. §2 For each i from 2 to 1, do the following.
  §2.1 Say i.` under budget 0.
  - The reference stops by the host after 1 operation.
  - `CutInterp` completes and writes a receipt.
  - The probe's own `equivalence()` reports the pair different, and the same holds for a For and a While with bodies.
  - Its corpus never exercises a host stop ("stopped by the host alike: 0").
- **Consequence:** `judge()` runs the plain reference first, so no reading here is wrong. The equivalence claim holds
  only on that corpus.
- **Repair (MEASURED, `k_repairs.txt` §4):** the check at For and While entry. The three laws then differ in 0 runs,
  and the corpus in 0 of 356.

### F5 (framing only): the probe's acceptance rows refuse CUT-0's own promised gain

- **Rule attacked:** `ok = ... gained == 0 and r8_cut == r8` (`cut0_claims.py` line 372). CUT-0.md says the frames
  make R8's "possible" exact, so CUT-0 must sometimes hold a claim that R8 withholds.
- **Counterexample (MEASURED, `k_criteria.txt`):** A23 holds one claim that R8 withholds as built. It reads gained 1,
  R8's class 2, withheld by the cut 1, so the probe would print FAILED on a corpus holding it, although its reading
  is right.
- **Repair:** every gain over the court as built must be put to an independent check (here, the oracle), instead of
  being forbidden.

### 2.6 The over-approximation argument, construct by construct (DECLARED, supported by MEASURED sampling)

The argument in `CUT-0.md` (the table after line 61) is a simulation argument: every step of a concrete continuation
lands in K̂.
- **The rest of a block, inline arms, rule uses, Must, Let, Set, Increase, Decrease, Say, Append, Remove, Decimals:**
  they hold. The table is right, and the cases are A01-A07 and A11-A12.
- **For:** holds. The bounds are fixed at entry, and the counter cannot be set (LOOP-VARIABLE, `sema.py` lines
  131-132 and 144-145).
- **An If on top:** holds, but it is imprecise (F3).
- **Perform:** holds. There is no recursion and procedures stand at top level only (`sema.py` lines 180-182 and
  200-205), so `Reach.proc`'s memo closes a DAG and the return goes only to the stack's caller.
- **Claim on top:** holds.
- **While: it misses.** The top row passes a refused fuel check, and the lower row honours a later one. The argument
  holds under S1 for the lower row and under S2 for the top row, and so under neither reading as a whole. With F1's
  repair it holds under S2 for every construct.
- **Sampled support:** 0 S1 counterexamples in 20,000 random laws, and every S2 counterexample is a spent While bit.
  The generator does not cover Append, Remove, item assignment, fixed or float numbers, text, or certificate and
  agreement oracles.
- **The cut's descriptor**, as opposed to K̂ itself, is not sufficient (F2).

## 3. The session model, broken

### Is one port at depth 6 too small?

- **Wider domains (EXHAUSTIVE over each, `s_attacks.txt` §1):**
  - two ports to depth 5 (37,505 histories);
  - two ports to depth 6 (102,383);
  - three ports to depth 5 (55,233);
  - one port to depth 8 (214,429).
- No row fails in any of them, and `history_bytes` has no collision.
- Depth is not the weakness; the rows are (G4). The real break needed **zero** ports, not more (G1).

### G1 (unsound): a law with no each-tick port

- **Counterexample (MEASURED, `s_attacks.txt` §2):** the history `[close]` with no each-tick port is legal.
  - Its projection writes the record `t 1 `, with a trailing space (`cut0_session.py` line 193).
  - The parser requires exactly 2 + 0 fields and refuses it, LOG-RECORD (lines 234-235). The row
    `projection-parses` fails.
  - `execute` would also index `vals[0]` (line 268).
- RULINGS R6 says "A tick block with no port still takes input" (`RULINGS.md` line 236), so such a law is in scope.
- **Test:** `check_run([("close",)], [])` passes. The plant is the probe.
- **Repair:** fix the empty record's one byte form (`t N`, with each value preceded by its space) in the grammar and
  in `serialize`, or refuse a tick block with no each-tick port. Either is a one-way format decision.

### G2 (imprecise): the door accepts a trailing LF

- **Counterexample (MEASURED, `s_attacks.txt` §3):** `door(b"1\n")` is accepted as 1. `FIXED` is matched with `$`
  (`cut0_session.py` lines 53 and 62), and Python's `$` also matches before a final newline.
- CONTRACT-DRAFT §1.3.1 requires the grammar "exactly" (line 31). Round D's Finding 16 left the trailing LF
  undecided, and the model decides it by accident.
- **Test:** `door(b"1\n")` reads INPUT-SYNTAX. The plant is the probe.
- **Repair:** `re.fullmatch`, or `\Z`.

### G3 (imprecise): the strict parser accepts a log no A2 history projects

- **Counterexample (MEASURED, `s_attacks.txt` §4):** multi-byte edits of the probe's 21 distinct logs: line swaps,
  deletions, duplications, substituted causes and the i64 bounds, 217 edits in all.
  - 152 are accepted, and every one is canonical.
  - 20 lie outside the image of A2's projection. The shortest is the header, then `end 0 not-run 1 INPUT-REFUSED a`.
  - Under A2, no history can put a refused arrival in a slot (`cut0_session.py` lines 101-103), so INPUT-REFUSED is
    A1's alone.
  - `parse_log` accepts it (`CAUSES`, line 49), and `execute` writes a core with status
    `NOT-RUN 1 INPUT-REFUSED a`.
  - The values at the i64 bounds are accepted and are in the image, as they should be.
- **Test:** the log above is refused under A2. The plant is the probe.
- **Repair:** the cause set follows the declared policy, or the log's header names the policy.

### G4 (framing only): most rows cannot turn red, and six plants pass the exhaustive domain

- **MEASURED (`s_attacks.txt` §5):** each of the probe's nine plants was run on the probe's own domain (one port,
  depth 6, 68,476 histories).
  - **11 of the 15 rows never turn red** under any plant:
    - projection-is-a-function, log-round-trips, door-replays and one-disposition-each;
    - execution-is-a-function, statuses-partition and T1-is-the-prefix;
    - T-differences-are-the-lines, ops-minus-last-T-is-tick-ops, no-T-ops-is-the-prefix and session-binds.
  - **Six of the nine plants turn no row red on the domain:** assign-refused, hold-previous, overwrite, lenient-hex,
    after-end and record-without-history. Each is caught only by its named case.
  - The execution side of the 68,476 histories sees 21 distinct logs.
- **ESTABLISHED by reading `check_run`** (lines 351-397). Five of the rows compare a function with itself:
  projection-is-a-function, door-replays, execution-is-a-function and session-binds, and one-disposition-each by
  construction. ops-minus-last-T-is-tick-ops compares `c - T[-1][1]` with the same expression (line 293).
- **No row states CONTRACT-DRAFT §1.5,** "No value is ever invented, held over from an earlier tick or defaulted".
- **Proposed row, MEASURED (§5b):** `no-value-invented` requires every tick record's value to be the door's value of
  the arrival the history assigned to that (tick, port).
  - As it stands, 0 of 68,476 histories fail it.
  - Under `hold-previous`, 1,062 of 68,917 fail it.

  So the exhaustive domain catches the plant that it now misses.
- **Repair:** replace the rows that cannot fail with ones that can, and give each a plant read on the exhaustive
  domain, not only on a named case.

### G5 (unsound against the record's own claim): the history holds no source

- **Rule attacked:** the session record attests "session provenance" (`CUT-0.md` line 173), and `drop` tells "its
  source" (line 153). CONTRACT-DRAFT §1.1 gives each arrival "the source's label" (line 23).
- **Counterexample (MEASURED, `s_attacks.txt` §6):** the model's event is `arrive(port, bytes)`.
  - Alice's `1` and Mallory's `1` give one history and one session record.
  - A result that must say who sent an input, or who sent the refused ones, cannot be read from it.
- **Test:** the two sessions' records differ. The plant is the probe.
- **Repair:** `arrive(port, source, bytes)`, with the source in `history_bytes`.

### G6 (unsound, DECLARED for version 1): a record the run never reads decides the tick bit

- **Rule attacked:** for REFUSED inside tick t, "the tick block's own frame says whether a later tick record exists"
  (`CUT-0.md` line 59). CONTRACT-DRAFT §4.4 says later records "are not read" (line 99).
- **The enabling fact (MEASURED, `s_attacks.txt` §7):** the model's δ ignores the run.
  - After tick 1 refuses (value 13), the host may still assign and close tick 2, then end.
  - The history is legal, the log holds 2 records against 1 tick run, and no row fails.
  - The probe's comment "the ticks that will run" (line 85) is false.
- **Consequence (DECLARED):** a claim evaluated in tick t before the refusal is held if the host ends at once, and
  withheld if the host appends a record the run never reads. The host chooses the standing with bytes outside the
  run. ROUNDS.md item 18 rejected a repair for exactly this property: it "lets whoever chooses the log choose the
  standing".
- **Repair:** as F1, the tick frame may always repeat after a refusal, as the NOT-RUN and LOG-OPEN rows already have
  it. Alternatively, δ ends the session at a refusing tick.

### G7 (imprecise): a host's drop reads as the player's missing input

- **Counterexample (MEASURED, `s_drop.txt`):** with ports a and b, compare "a sent nothing" with "a's valid `1`,
  dropped by the host".
  - Both are legal and pass every row.
  - Both give one input log and one receipt core, `NOT-RUN 1 INPUT-MISSING a`.
  - Only the session record differs.
- The receipt names the player's input as missing when the host declined it.
- **Repair:** a cause of its own (a dropped input), or a rule that a drop cannot leave its port's slot empty at the
  close.

### Already known, not counted

The port signature's unescaped name, which lets two port lists share one signature, is Round D's Finding 8. The model
writes the same form (`cut0_session.py` lines 180-182) and inherits it.

## 4. What neither probe can show

**The claims probe:**
- **Version 1:** ticks, ports, TICK-BUDGET and the tick frame's bit. G6 is DECLARED only.
- **The four executions.** CUT-0 puts the cut in the `'R'` event so that every backend agrees on it. Only the
  reference's frames exist. Nothing shows that the C, Rust and Python backends, which lower to three-address code,
  can produce the same frames, the same loop bits or the open claim's id (F2).
- **Proof.** The invariant K̂ ⊇ K is argued and sampled. The oracle under-approximates (seven substitutes, one
  generator grammar), and the absence of S1 counterexamples is not a proof.
- **The court's other rules.** Premises and support (R6's least fixed point), grounding (the PREFIX licence) and a
  certificate claim's cost reading when its certified clause lies in K̂ are not combined with the cut rule.
- **The meaning of E2 itself.** F1 shows CUT-0 cannot satisfy both readings of "could still have evaluated". Which
  one the owner means is a ruling, not a measurement.

**The session probe:**
- **Orlog's execution:** the stand-in law reads only the first port's value (line 268).
- **What the model leaves out:** read-once ports and their record (CONTRACT-DRAFT §2.1), port types other than
  fixed, the arrival log's own format (§1.1), the door's report, and the chained `in_t` (§2.3). The record hashes the
  whole log.
- **The source of an arrival (G5), and any time.**
- **The host's honesty and its fairness.**
  - A host may drop any valid input and close (G7).
  - Nothing says when a host must assign or close.
  - A lying host writes a consistent set of records.

  The record's integrity is not its truth.
- **Policy A1** over the exhaustive domain.

---
*The adversary, research/run-1/manifold/. Written before reading the proponent's record or scripts.*
