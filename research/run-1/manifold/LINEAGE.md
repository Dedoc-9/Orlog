# LINEAGE: the owner's earlier "manifold" designs, read from their code and weighed against CUT-0 (2026-10-26, research only)

The owner asked that his earlier manifold, topology, quotient and lattice designs, in his other repositories and in the
local folders, be found and weighed against CUT-0 (`research/run-1/CUT-0.md`, its probes
`research/run-1/probes/cut0_session.py` and `cut0_claims.py`). He then asked the converse: where could the designs
derived in Orlog apply in those repositories? This record answers both. It is the lineage researcher's, beside the
proponent's and the adversary's files in this folder, which it does not touch. Nothing here is ruled.

**What was read.** All 27 repositories of the owner's GitHub account, and 23 local folders, labelled
L1 to L23 here: their names and locations stay on the owner's machine, and the key is not published. Local folders were read first. Repositories without a local copy were shallow-cloned into `work/lineage/`, which
git ignores. Two clones (`dvsm-meta-kernel`, `DVSM-Protocol`) did not check out on Windows file names, so they were
read through `git show HEAD:path`. Nothing in any repository or folder was changed, and nothing was pushed.

**Grades.**
- **ESTABLISHED:** read in code, at the file and line given.
- **MEASURED:** run by this researcher (section 6 lists every run).
- **DECLARED:** the repository's own prose, unverified.

Paths are relative to the repository or to the local folder labelled.

**Who read what.** The reading was split. This researcher read `dvsm-meta-kernel`'s lockstep kernels,
`mcl-observer-runtime`, `DEEQN64` and `Q64-adaptive-dynamics`. Four delegated readers read the rest, each against the
same brief.
- **(re-read):** a citation this researcher opened again and found as cited. Every design that the synthesis (section 4)
  relies on was re-read.
- **Unmarked ESTABLISHED:** read in code by a delegated reader, and not re-read here.
- **Corrections:** two delegated statements were corrected on re-reading. They are noted where they occur (2.3, 2.4).

## 0. The answer in brief

- **"Manifold" in the owner's code almost never names a manifold of states or histories.** Read from the code, it names
  one of these:
  - an orthonormal frame kept near WᵀW = I (genuine geometry, a Stiefel set);
  - a low-rank principal subspace of a sliding window (a point on a Grassmannian);
  - a box, or a union of boxes, with a clamp;
  - a fixed-length float array;
  - a canonical graph;
  - a string label;
  - a hypothesis, tested and mostly refuted (Urðr's `voxmanifold`).

  No design builds the reviewer's stratified configuration space over discrete session or run states (section 1).
- **Problem 1, the fibers of the history-to-log projection.** Usable mechanisms exist, but they are discrete and none is
  geometric:
  - **Urðr's `inputset`:** nested projections, with a witness-pair search for "this quantity is constant on the
    projection's fibers".
  - **Verðandi's WORKSHOP-0 census** (local folder L18): every single edit is classified by which of
    authority and projection moved, under one-directional laws.
  - **The pair test in local folder L1's Firewall Spec** states the right well-definedness condition, but only as
    float drafts.
  - **Confirmations of CUT-0's own design:**
    - Semiotic core's quotient counting;
    - Urðr's `recirc` collision of an honest and a doctored set;
    - Urðr's `netcode/session`, the nearest working twin of the session.
- **Problem 2, claim-continuation soundness.** One design gives CUT-0 a real mechanism: Ursprung's PO-10 harness
  (`weltwerk/verify/abstraction_soundness.py`).
  - It checks that an abstraction over-approximates the existential image of an exact reachable graph, and that it never
    reports a false CLOSED. It has a plant that drops the bad block. Here 5 of 5 checks passed (MEASURED).
  - It is the exact template for CUT-0's statement: K over-approximates every resumed run's evaluations, and no claim is
    falsely held.
  - Urðr's segmentation law (cut after any step, snapshot, resume, compare) is the resumption pattern this folder's
    `resume_oracle.py` already follows.

  Every other "reach" in the lineage is either empty (a stub returning the empty set) or bounded below the truth.
- **The concrete comparison the brief asked for.** `dvsm-meta-kernel`'s "lockstep command buffering" is one `Vec` of
  commands, drained in push order at each tick. Its "S_ECHO hash finality" is a 64-bit FNV-1a over entity ids and
  positions, with no input in it.
  - Its consensus "rollback" restores the state the rejected tick just produced (MEASURED).
  - Its determinism smoke test passes because every tick is rejected. With peers that agree, it would report a
    deterministic kernel non-deterministic at the second tick (MEASURED).
  - It gives CUT-0 nothing. CUT-0's session would catch each of its defects (section 2.1, table).
- **Where Orlog's designs would bite hardest** (section 5):
  - **Range-before-grid (e)** at the silent Q32.32 and Q31.32 conversions. Two of them use Orlog's own scale of 2^32 in an
    i64: `dvsm-meta-kernel` `fx` (MEASURED: NaN becomes 0, out of range saturates, off grid truncates), and local folder
    L6's `to_q31_32`.
  - **The session's assign, drop and close rules (b)** at the lockstep buffers.
  - **The two-layer binding (d)** at every hash that binds state but not input, or binds a result but not the refusals.

## 1. What the words denote in code

| denotation, read from code | where | grade |
|---|---|---|
| an orthonormal frame W with Gram–Schmidt or QR retraction and a drift norm ‖WᵀW − I‖ (a Stiefel set; square W makes it O(r)) | `dvsm-meta-kernel` `Ultimate Stack/Cargo/src/manifold.rs` 42-148; `dvsm-pi-plus/Crates/dvsm core/src/manifold.rs` 5-25; `2-Layer_Reality_Core/Gated_Steifel_Refined.rs` 196-208, 347-388; Dentatus (local folder L7) `AetherManifold/riemann.py` 38-73 | ESTABLISHED |
| the top-k eigenspace of a sliding-window covariance; "manifold velocity" is sqrt(Σ(1−σᵢ²)) between successive subspaces, a chordal distance although the docstring says geodesic | `DEEQN64` `_runtime/q64_stratified_engine.py` 126-218, 352-371; the same file in `Q64-adaptive-dynamics` | ESTABLISHED |
| "stratified": a fixed split of a 64-vector into four index ranges | `DEEQN64` `src/engine.rs` 126-130 | ESTABLISHED |
| a box, or a union of boxes, on (x, v, a, j); "Π_M" is a per-coordinate clamp | `dvsm-meta-kernel` `Minimal_Core/Π_M_STRATIFIED_MANIFOLD_PROJECTION_CORE.rs` 248-356, 407-427 | ESTABLISHED |
| an active set {Interior, Upper, Lower} of an interval, with a contact log of each clip (the one genuine stratification) | `dvsm-meta-kernel` `Minimal_Core/RESEARCH_GRADE_CORE.rs` 414-453, 536-558 | ESTABLISHED (re-read) |
| the fiber of a hash of a trace over a finite universe; a one-swap order test | `dvsm-meta-kernel` `DVSM_ODCN_Obs.swift` 184-264 | ESTABLISHED (re-read) |
| a quotient by exact tuple equality of channel images | local folder L8 `genesis/gen008_constraints.py` 40-41 | ESTABLISHED (re-read) |
| a quotient by nested projections; and a lattice of input subsets, with its antichain of minimal determining sets | Urðr `tools/terrain/inputset.py` 110-125, 272-293; `tools/terrain/autoroute.py` 192-194, 476-487 | ESTABLISHED (re-read for inputset) |
| a Galois connection α/γ and its closure | Urðr `tools/terrain/recirc.py` 116-135 | ESTABLISHED (re-read) |
| a quotient of a reachable graph by a partition (the existential image) | Ursprung `weltwerk/verify/abstraction_soundness.py` 117-124 | ESTABLISHED (re-read) |
| a single-linkage partition at a threshold τ, with refinement and variation of information | `mcl-observer-runtime` `mcl_sdk/mcl_kernel.py` 31-83; local folder L12 `q64-adaptive-dynamics/MCL/mcl-ecr/meta/mcl_kernel.py`; local folder L4 `mcl_runtime/kernel.py` 17-62 | ESTABLISHED |
| a graph whose identity is the hash of a canonical edge set | Dentatus `manifold/manifold_core.py` 31-103; local folder L10 `manifold_core.py` 32-104 | ESTABLISHED |
| a fixed-length float array named "manifold" | `DVSM-Draco` `src/physics/dvsm_state.rs` 61; local folders L6 and L12, `dvsm_state.rs` (`z_manifold: [f32; 269]`) | ESTABLISHED |
| a hypothesis that certificate validity forms connected regions, scored and mostly refuted | Urðr `tools/terrain/voxmanifold.py` 15-33, 355-394, 440-457 | ESTABLISHED |
| persistent homology over F2, refusing at the i64 ceiling | Urðr `tools/homology/urdr_homology.py` 63, 77-87, 116 | ESTABLISHED |
| an EMA scalar, a constant, a threshold, the identity, or a label | `DVSM-Protocol`, `DVSM-Pulse`, `DUMEwow`, `3x-DVSM`, `SymFlow-DVSM-Lattice`, `DQSDv2GPU`, `AIS2`, L12's klein_glug and phase3 files (section 2.14) | ESTABLISHED |

## 2. The designs, repository by repository

### 2.1 dvsm-meta-kernel: lockstep command buffering and S_ECHO hash finality (2dca188, 2026-05-27)

**Files.** `dvsm_meta_kernel.rs` (the namesake; git blob `1e45824`, sha256 `998a2111…`), `Deterministic ECS Kernel`
(headed DVSM_REAL_CORE), `README`.

**1. Meaning.** Here "S_ECHO" is the state's identity.
- In `dvsm_meta_kernel.rs` it is a 64-bit FNV-1a fold over each alive entity's id, generation and three positions
  (115-139). Velocity, the tick, dead entities and every command are outside it. ESTABLISHED (re-read).
- In `Deterministic ECS Kernel` the fold is salted with the tick and covers ids and positions, still without velocity
  (200-218). ESTABLISHED (re-read).
- The README states the equivalence as a biconditional between equal S_ECHO and equal state (`README` 672 and 787), and
  calls S_ECHO "cryptographic" (646, 1022). DECLARED.
- The manifold language around S_ECHO (`README` 170-173, 386; the Genesis archive's HASH∘RENORMALIZE) is prose. No
  RENORMALIZE exists in code. DECLARED.

**2. Mechanism.** ESTABLISHED (re-read).
- `Server` holds `buffer: Vec<Command>` (148).
- `tick` drains the buffer in push order (176-192), then:
  - moves positions by velocity / 60 (197-205);
  - hashes (210);
  - pushes a snapshot into a 64-deep ring (215-223);
  - counts the peer hashes equal to its own (228).
- **Below the threshold of 2,** it assigns `self.rollback.back()`'s state (231-233). That is the snapshot it pushed four
  lines earlier. It then returns `None`.
- **`Deterministic ECS Kernel` encodes its network frame from `self.buffer` (298) after `mem::take` emptied it (234),**
  so the frame it builds never carries a command.
- Its client `reconcile` rolls back to the ring's newest snapshot (316). It panics on an empty ring (`unwrap`).

**3. Evidence.** MEASURED, rustc 1.96, the file as published, twice: it prints its PASS line both times. A probe built
from the file's lines 1-269 unchanged, with only its `main` replaced (appendix), measured these, byte-identical across
two runs:

| probe | result |
|---|---|
| P1, the smoke test's own loop (peers report 12345) | 128 ticks of 128 return `None`, so the test's comparison never runs: it cannot fail |
| P1b, the same loop with peers agreeing with each tick's hash | the comparison fails at the second tick, so with working consensus the test would call the kernel non-deterministic |
| P2, a tick rejected by its peers | the state after it equals the snapshot that same tick pushed; the tick counter advanced and the commands are consumed. The "rollback" restores nothing |
| P3, two worlds with equal positions and different velocities | equal S_ECHO before one step; unequal after it |
| P3b, one dead entity against an empty world | equal S_ECHO |
| P4, the Q32.32 door `fx(f64)` (39-41) | NaN becomes 0; +∞ and 1e30 become i64::MAX; −1e30 becomes i64::MIN; 1.5e-10 becomes 0; −0.7e-9 becomes −3 (truncated toward zero) |
| P5, the buffer | a SetVel for an unknown entity leaves no trace (hash unchanged, buffer empty); two SetVel for one entity in one tick keep the second; Spawn(3) twice makes two entities |

`Deterministic ECS Kernel`'s `test_determinism` (330-342) asserts nothing. ESTABLISHED (re-read).

**4. Against CUT-0, concretely.** The brief named this kernel as close to the session's arrival, assignment and close
model. Read from code, it shares only the tick. Each row is ESTABLISHED, and MEASURED where P-numbered.

| CUT-0's session (`cut0_session.py`) | `dvsm_meta_kernel.rs` / `Deterministic ECS Kernel` |
|---|---|
| `arrive(port, source, bytes)`: numbered, its source named (G5), judged at once by the door (range before grid) | no arrival: the caller pushes typed values into the buffer, and a `Command` names no sender (94-98), so two peers' identical commands are one (G5's defect); a decimal enters through `fx`, which repairs NaN, ∞, out-of-range and off-grid values silently (P4) |
| `assign(arrival, tick)`: one slot per (tick, port); SLOT-FILLED, ASSIGN-CLOSED, ASSIGN-AHEAD | implicit: whatever is buffered when `tick()` runs. Which tick a command lands in is a fact of call timing, recorded nowhere. A second write to one slot silently wins (P5): CUT-0's plant `overwrite` |
| `drop(arrival)`: an explicit, recorded event | a command naming an unknown entity is skipped with no record (181, 187; 246-262; P5) |
| `close()`: runs only if every each-tick port is filled, else NOT-RUN INPUT-MISSING | a tick runs on any buffer, empty included; a missing input is indistinguishable from "no change" |
| `end()`, END-PENDING, END-UNDISPOSED | none |
| the input log, the history's projection under a strict grammar | none kept: after the drain no command exists anywhere; `NetFrame::encode` writes an unframed byte string, and in DVSM_REAL_CORE writes it from the emptied buffer |
| the receipt core, a function of the input log | S_ECHO, a projection of the state that drops velocity, so its fibers hold states with different futures (P3). It is not a congruence of the step |
| the session record binding history, log and core | none |
| "finality" | a rejected tick keeps its state, its snapshot and its tick (P2) |

- **Problem 1:** S_ECHO is the counterexample. A digest whose fibers are not respected by the dynamics agrees on
  states that diverge one tick later.
  - CUT-0 avoids this by construction: the receipt core is a function of the input log, and so is execution.
  - The session probe checks that the execution is a function of the input log.
- **Problem 2:** nothing.
- **Reusable mechanism:** none. **Reusable lesson:** a determinism test must be able to fail (the plant discipline
  Orlog already keeps).

**5. Overclaims.** ESTABLISHED, or MEASURED as marked.
- "Rollback-free … deterministic replay" (`README` 685, 708-710) against no stored input. Nothing can be replayed.
- "Snapshot-based rollback" (`dvsm_meta_kernel.rs` 13) that restores the present (P2).
- "Cryptographic" for FNV-1a.
- The biconditional state ⇔ hash, refuted by P3 and P3b.
- "Anti-desync validation via hash finality" (`README` 729-730) for a test that never compares (P1).

**Lineage of the lockstep idea in the owner's own work.** All ESTABLISHED (re-read).
- **`dvsm-meta-kernel` (May 2026).**
- **Dentatus `lockstep/` (June 2026; local folder L7):**
  - integer state;
  - inputs kept per tick (`tick.py` 57, 68);
  - a truth hash of (tick, state) (35-37);
  - re-simulation from the inputs on a mispredict (`rollback.py` 61-82).
- **Urðr `tools/netcode/session.py` (September 2026):**
  - membership judged at the event's tick (132-138);
  - convergence over four delivery schedules to one chain equal to a batch oracle (401-412);
  - typed refusals kept outside the trace (382-383);
  - a segmentation law, snapshot and resume at every cut (495-512).
- **CUT-0 (October 2026)** adds what none of the three has: the door at arrival, explicit assign and drop, a close
  rule, an end rule, and a history seal beside the core.

### 2.2 dvsm-meta-kernel: the manifold family (same commit)

The repository holds 126 files that mention "manifold", mostly concatenated drafts. Many do not compile as laid out:
- duplicate types;
- a crate root with no `mod`;
- `i256` defined nowhere;
- JSON pasted into `.rs` files.

No file has a test that can fail on the geometry. ESTABLISHED. The designs nearest CUT-0:

- **The stratified jet projection** (`Minimal_Core/Π_M_STRATIFIED_MANIFOLD_PROJECTION_CORE.rs`). ESTABLISHED.
  - Strata are boxes; they may overlap, and ties go to box order.
  - Π_M clamps each coordinate (289-300, 407-427). The header itself names independent clamping as the wrong design
    (159-174).
  - A NaN state lies in no box and comes out non-finite.
  - Relation to CUT-0: naming only. It is the anti-pattern for problem 1: a many-to-one map that forgets how far outside
    the state was, and keeps no record of it.
- **The active-set contact log** (`Minimal_Core/RESEARCH_GRADE_CORE.rs`). ESTABLISHED (re-read).
  - `classify_active_set` (424-436) splits the x interval into its open interior and two faces.
  - Each x clip appends a `ContactEvent`: step, node, raw value, projected value, magnitude, face (443-453, 536-558).
  - This is the right architecture for problem 1: a projected core plus a side record of what the projection forgot.
  - The record is not injective on the fiber:
    - clips of v, a and j leave no event;
    - mode π+ zeroes v, a and j unrecorded;
    - `clip > 0.0` is false for NaN;
    - a value exactly on a bound is active and recorded nowhere.
  - The property to take is checkable: (core, side record) must be injective on each fiber. Plant one clip per
    coordinate, a NaN and an exact-bound value. This code fails all three.
- **Observational fibers** (`DVSM_ODCN_Obs.swift`). ESTABLISHED (re-read).
  - Ω is an order-sensitive hash of a witness-lifted trace (184-226).
  - `fiber` filters a finite universe by equal Ω (252-264).
  - `isChiral` compares Ω(a+b) with Ω(b+a) (234-245). It is the lineage's only minimal-pair code.
  - The file does not compile: redeclared types; an identifier with spaces at 388.
  - Usable for problem 1 only as a test pattern:
    - enumerate bounded histories;
    - group them by exact log bytes, never by a hash (a hash's fibers include collisions);
    - require the seal to separate exactly the differences declared to survive;
    - use one-event swaps, insertions and deletions as the generators.
- **The quotient-functor "lattice"** (`Minimal_Core/Minimal_Core.rs` 2700-2869). ESTABLISHED.
  - Maps from a trajectory to vectors, with a declared order (refines, join, meet) that nothing implements.
  - The declared "resolution" contradicts the maps: two maps inducing one partition are given resolutions `usize::MAX`
    and 1.
  - The lesson for CUT-0: refinement must be computed from the fibers, never declared.
- **The fracture flag** (`Minimal_Core/Minimal_Core.rs` 1515-1625). ESTABLISHED.
  - It is an absorbing exclusion: a fractured node is skipped forever.
  - Its frozen value is still read by its neighbour.
  - A NaN drift never fractures, so the rule fails open and is not monotone on NaN.

### 2.3 Urðr (local folder L23, ad6d55f, 2026-09-30, the same commit as GitHub)

**`inputset` and `autoroute`: which record determines a quantity (problem 1, directly).**
1. **Meaning.** ESTABLISHED (re-read).
   - `proj(level, s)` (`tools/terrain/inputset.py` 110-125) defines four nested projections:
     CERT ⊂ LATTICE ⊂ HISTORY ⊂ COHORT.
   - LATTICE there means the voxel occupancy.
   - `autoroute` has an order lattice of the 16 subsets of four input atoms, and returns its antichain of minimal
     determining sets (`tools/terrain/autoroute.py` 192-194, 476-487).
2. **Mechanism.** ESTABLISHED (re-read).
   - `determines` (272-279) searches a finite family of situations for two with equal projections and unequal values.
   - `tier_of` (282-293) returns the coarsest level that determines the quantity, with the refuting witness from the
     level below.
   - **Correction to the delegated reading:** the witness returned is the pair of differing values, not the pair of
     situations.
3. **Evidence.** ESTABLISHED.
   - Gate rows `verify.py` 17463-17577 and `tests/test_inputset.py`.
   - Plants: a vacuous self-comparison (`inputset.py` 360-372), a hand-typed table (343-357), autoroute's
     search-only over-skip (516-523).
4. **CUT-0, problem 1: usable now.**
   - Declare the levels the input log, then the history.
   - For each quantity the contract defines (the receipt core's fields, the court's reading, and anything said to depend
     on refusals), compute the coarsest level that determines it, over the session probe's exhaustive domain.
   - A quantity the log does not determine comes with two histories, one log and two values. It must read the history
     seal. That is the reviewer's "which differences must survive", decided and witnessed.
5. **Overclaims.** ESTABLISHED.
   - Positives are relative to the family; the module says so (50-53).
   - `autoroute`'s syntactic route is called "sound, universal" (511) and a sufficient condition for a universal positive
     (575-578). It has three limits (re-read):
     - it stops at depth 3, a bound its own docstring declares (524-528);
     - it follows only callables named as bare tokens in a function's globals, so a call through a module attribute is
       never followed (541-546);
     - it matches only the key as a quoted literal (583-584).

     Only the second and third are undeclared.
   - Stale counts appear in its prose (61-63 against 192, 439).

**`netcode/session`: the nearest working twin of CUT-0's session.** ESTABLISHED (re-read).
- Membership is a function of the event's tick and the calendar alone (132-138). The head-time variant differs by one
  expression (160-182) and is shown to fail convergence.
- `run` returns the trace and a separate tuple of typed refusals (382-383).
- The header records that two wrong designs produce the same chains with different refusal codes (34-43): the codes
  carry what the state does not. This is CUT-0's case X, from the other side.
- The segmentation law (495-512) cuts after every step, snapshots, resumes a fresh session and compares with the
  oracle. `RESUMABLE` is derived from the fields set in the constructors (178-181).
- **Gap.**
  - The header and docstrings say the four schedules carry "the identical eleven envelopes" (27, 294).
  - The schedules deliver envelopes 0 to 7 only (297-316).
  - The out-of-window envelopes are refused separately, at four fixed heads (`the_membership_refusals`).
  - So no convergence or segmentation sweep contains a refused arrival. CUT-0's session cases (a refusal then a retry, a
    retry after the close, a slot filled twice) are exactly what is missing there.

**`recirc`: a closure is blind to an omission.** ESTABLISHED (re-read).
- α/γ and the closure γ∘α (116-131).
- An honest capture and a doctored one with one obligation dropped have different raw sets and equal closures
  (`doctored_collides_with_honest`, 231-239).
- For problem 1 this is the owner's own measured argument for CUT-0's separate history seal: a coarse image cannot
  show an omission that only the raw history shows.
- Delegated reading, not re-read: the docstring's claim that the refinement step count carries information is false by
  `refine_to_fixed_point` (257-273), and the test bounding it (`tests/test_recirc.py` 72-79) cannot fail.

**Other Urðr designs.** ESTABLISHED.
- **`fibre.py`** groups recorded states by framebuffer digest (123-144), and tests whether forgetting a field keeps the
  map well defined (201-205). It states honestly that the converse direction is untested (193-198).
- **`snapshot.py`** refuses to save a MEASURED value (35-37). Its loader rebuilds a claim from the file's own maturity
  strings (68-69), so a hand-edited snapshot can import MEASURED (section 5).
- **`voxmanifold`** is a precedent for testing a manifold analogy instead of naming one. It was pre-registered, scored and
  mostly refuted.

### 2.4 Ursprung (clone dcdad67, 2026-07-05; local folder L22 holds one prose file)

**PO-10, `weltwerk/verify/abstraction_soundness.py`: the template for problem 2.**
1. **Meaning.** "Quotient" is a partition α of the exact reachable states. `lift` is the existential image of init,
   edges and bad states under α (117-124). ESTABLISHED (re-read).
2. **Mechanism.** ESTABLISHED (re-read).
   - `build_concrete` explores the real transition relation breadth-first to a bound of 6 (39-77) and records
     `frontier_open` when the bound was reached (77).
   - `admissible` requires a candidate abstraction's init, edges and bad set each to contain the lift (128-134).
   - `no_false_closed` checks the conclusion directly: never abstract CLOSED while the exact graph is VIOLATED
     (137-141).
3. **Evidence.** MEASURED here.
   - `test_abstraction_soundness.py` (pure standard library): 5 of 5 checks pass, among them the plant that drops the bad
     block and must be both inadmissible and a false CLOSED.
   - Both fixture worlds have `frontier_open` False (5 states, 15 edges; 4 states, 12 edges): their graphs are closed,
     so the verdicts compared are exact.
   - **Correction to the delegated reading:** the bounded-graph gap is real but latent. No verdict or test reads
     `frontier_open`, so a world truncated at the bound would be judged as if exact. The fixtures do not exercise it.
4. **CUT-0, problem 2: the mechanism CUT-0 lacks, as a harness.** The mapping is one to one:
   - the exact graph is the set of claims a resumed run evaluates after the cut, over every value the refusing
     operation could return;
   - the abstraction is K;
   - CLOSED is "held";
   - a false CLOSED is a claim held whose site some resumed run reaches.

   This folder's `resume_oracle.py` builds the exact side; PO-10 supplies the premise-and-conclusion shape and its plant.
   Under Orlog's discipline, a run the oracle cannot finish is LOG-OPEN, never exact. So a CUT-0 harness would have to
   read its own `frontier_open`, which PO-10 does not.
5. **Overclaims.** None in the harness. Its scope is stated: a theorem only under admissibility.

**`weltwerk/scale/reachability_algebra.py` and `teleport.py`.** ESTABLISHED (re-read for the first).
- The potential set is the reflexive ball (I∨A)^H (31-44). The walk of exactly H steps undercounts, being
  parity-restricted on a bipartite ring (47-56). Both are tested against brute force.
- Lesson for K: it must be a reflexive closure, never "exactly the next H steps".

**`experiments/live_world_kernel/claim_lattice.py`.** ESTABLISHED.
- A real order lattice of (maturity, evidence) claims: meet and join computed (129-138), no-strength-creation checked
  exhaustively (159-226).
- It has no withhold operator and no fixed-point argument, so Orlog's lemma (f) is not there.
- Three of its checks cannot fail (160, 208-209, 223).
- No test or gate references it.

### 2.5 A local Verðandi copy (local folder L18, a16d663, 2026-10-08)

**WORKSHOP-0, `workshop/edit.rs`.**
1. **Meaning.** The authority is the hashed level and tile files. The projection is three witnesses: strips, frame
   digest, pixels. "Outside-view" means the authority moved and no witness did: a member of the projection's fiber.
   ESTABLISHED (re-read).
2. **Mechanism.** ESTABLISHED (re-read).
   - `classify` (446-463) is an exhaustive match over what moved. Arms the kernel makes impossible return an error.
   - `consequence` (465-507) re-derives the result column by column, and refuses:
     - a digest that moved with no column;
     - pixels with no strip, index or material behind them.
3. **Evidence.** ESTABLISHED.
   - Gate rows `workshop-stale` and `workshop-projection` plant each defect (`verify/verify.py` 1116, 1127).
   - A census of 1,379 edits, 1,308 outside-view (`workshop/attest/census-witness.json`).
   - The header records the biconditional "authority moved ⇔ projection moved" as measured false (31-32).
4. **CUT-0, problem 1: usable now, as the census shape.**
   - Enumerate every single-event mutation of a history: an arrival added or removed, its source changed, an assign
     moved, a drop added, a close moved.
   - Classify each by which of the input log, the receipt core and the history seal moved.
   - Hold two laws: log unmoved ⇒ core unmoved, and history moved ⇒ seal moved. Refuse the impossible arms.
   - The session probe already mutates logs byte by byte and checks named history pairs. This census would mutate every
     history in its domain event by event and classify each mutation, which it does not yet do.
5. **Overclaims.** None found; code and header agree.

**SESSION-WALK, `workshop/sessionwalk.rs`.** ESTABLISHED (re-read).
- The head is a left fold over each event's tag and witness (431-439).
- Tick stamps are checked for form and never folded: "a tick is when, not what" (36-40).
- For CUT-0 this is the contrast case. The owner's own precedent puts timing outside a head, deliberately and in
  writing. In CUT-0, `assign(arrival, tick)` decides what a tick runs on, so it cannot be "when, not what"; the close
  event and the assignment belong in the history.

### 2.6 Semiotic core (local folder L8, 2026-06-12)

1. **Meaning.** `quotient(channels)` counts the distinct joint images of a tuple of functions on a 4-element space
   (`genesis/gen008_constraints.py` 40-41). ESTABLISHED (re-read).
2. **Mechanism.** ESTABLISHED (re-read). Four cases are computed:
   - one corrupted channel merges exactly two classes (C1);
   - channels supported on one region cannot see the other (C2);
   - a lossy post-map cannot be re-separated (C3, the data-processing inequality);
   - delivery time fixes what is distinguishable (C4).

   GEN-002b also injects ledger faults, and makes intra-tick order a declared, tested fiber (`gen002b_ledger_faults.py`
   87-88, 139). ESTABLISHED.
3. **Evidence.** Assertions that could come out otherwise, on one 4-element space. The result files call them theorems.
   DECLARED. GEN-004's tamper check K5 compares against the untampered original and is marked a placeholder (96-107), so
   it cannot fail. ESTABLISHED.
4. **CUT-0, problem 1.** A confirmation, not a new mechanism:
   - C3 is the reason the history seal must be computed from the history, never from the log;
   - C4 is the reason the close event must be in the history.
   - `quotient()` is an exact class counter usable over the session probe's domain.
5. **Overclaims.** "Theorem" from n = 4 instances.

### 2.7 dvsm, the Firewall Spec drafts (local folder L1, `Firewall Spec/`, 2026-05-12)

1. **Meaning.** Fiber, quotient and equivalence class mean the kernel of an observation map O. ESTABLISHED.
   - `Shared_State.rs`: `in_kernel` 188-192, `fiber` 213-219.
   - `compression_rust_intro.rs`: a lossy O at 192-204.
2. **Mechanism.** `preserves_equivalence` (`compression_rust_intro.rs` 424-436) is the pair test O(s1) = O(s2) ⇒
   O(F(s1,u)) = O(F(s2,u)). `check_commutativity` compares O∘F with f∘O through a representative (212-237). ESTABLISHED
   (re-read for the pair test).
3. **Evidence.** None. ESTABLISHED.
   - No test and no caller.
   - Float comparisons with ε = 1e-12.
   - `Shared_State.rs` defines `DVSMCore` three times.
   - `F_quotient` (442-454) applies the pair test to a state and its own successor, not to two members of one fiber, and
     on failure silently keeps the old state (re-read).
4. **CUT-0, problem 1: the criterion, stated.** A difference inside a log fiber must survive exactly when some
   continuation's observable separates it. The pair test finds such differences. CUT-0 meets the criterion by
   construction (execution is a function of the log). The test is the check that keeps it so.
5. **Overclaims.** The drafts define incompatible quotients: `v − floor v` against `fract()`, which is negative for
   negative v (`dvsm_bounded_fifo_dynamical_system.rs` 133-135). Refused inputs leave no trace and the runtime's time
   advances anyway (`Shared_State.rs` 289-291), so a refused input and an absent one share a fiber. That is CUT-0's
   "different refusals, one log" without the seal. ESTABLISHED.

### 2.8 Dentatus (local folder L7, b65b069, 2026-06-19)

- **`manifold/manifold_core.py`.** "Graph embedded in a manifold" (line 4) is a graph.
  - Its identity is sha256 of a canonical edge set and its Laplacian (31-53). Normalization silently drops self-loops and
    duplicate edges (33).
  - The exact gate is connectivity and bridges (56-103). The Fiedler value is captured, never hashed.
  - Naming only. ESTABLISHED.
- **`lockstep/`.** Read in 2.1. ESTABLISHED (re-read).
  - `kinematic_step` reads `int(inp.get("a", 0))` (`tick.py` 45): a missing input becomes 0, and a float input is
    truncated.
  - `reconcile` builds its corrected track from the authoritative prefix followed by the client's predicted inputs
    (`rollback.py` 71-72). Predictions are hashed into the "corrected" truth, although the docstring says they are never
    committed truth (10-12).
  - `last_valid_tick` returns 0 both when tick 0 is valid and when nothing is (52-58).
- **`consequence/propagation.py`.** ESTABLISHED (re-read).
  - Its "causal frontier" walks at most 6 layers (`depth=6`), with integer decay that drops flows truncated to 0
    (24-55).
  - The docstring calls the complement "provably-irrelevant", while also saying it is an allocation decision, never a
    truth decision.
  - Used as CUT-0's K, it would be an under-approximation and would hold claims wrongly. That is the cautionary case for
    problem 2.
- **`chronicle`, `airlock`, `quorum`.** ESTABLISHED.
  - `Recorder.record` raises and records nothing (`chronicle/core.py` 81-83), so refusals never reach the history.
  - Airlock rejections point at the commit head and are not chained to one another (`airlock/membrane.py` 64-68).
  - Quorum's `cert_hash` leaves out the rejected and the equivocating votes (`quorum/tally.py` 113-117, 159-160), so
    rounds differing in who was rejected share one certificate.
  - Each is a log without a history seal: problem 1's failure, three times.
- **`AetherManifold/riemann.py`** is a genuine Stiefel manifold in Q32: a tangent projection and an integer Gram–Schmidt
  retraction (38-73). It is a different subject. Its conversion `to_fp` rounds half away from zero with no refusal
  (`aether/fixedpoint.py` 17-27). ESTABLISHED.

### 2.9 mcl-observer-runtime (d8b1907, 2026-06-11), with local folder L12's MCL kernel and local folder L4

1. **Meaning.** The description's "quotient topologies" are single-linkage partitions of entity embeddings at a
   threshold τ, chosen at the largest gap of the merge heights, which are the H0 barcode (`mcl_sdk/mcl_kernel.py` 31-51,
   86-105; `mcl_sdk/sir_runtime.py` 104-110). "Persistence-indexed" is fair for that choice. ESTABLISHED.
2. **Mechanism.** ESTABLISHED.
   - `project` (54-58) restricts a partition.
   - `refines` (75-78) is exact.
   - `vi` (61-72) is the variation of information, with values below 1e-12 set to 0.
   - `analyze` partitions under each registered encoder, compares partitions by VI, and lists the pairs coincident in one
     encoder and distant in another (`sir_runtime.py` 171-184).
   - Its `chain_hash` (207-208) is a 16-hex sha256 of the result: no predecessor, so not a chain.
3. **Evidence.** MEASURED: `tests/test_sdk.py`, run directly, 8 of 8 pass.
   - The divergence test detects by unequal `chain_hash`, so it would detect any change at all.
   - `test_trajectory_drift_ticks` asserts only that the result is a list.
   - The kernel's header cites a firewall test, `test_sir_stack.py` (7-9), that this repository does not contain. Its
     rule is DECLARED here.
4. **CUT-0.** A different subject (metric clustering).
   - The generic part, exact `refines` and `project` over finite partitions, could check ker(log) ⊑ ker(core) on
     enumerated histories. So could L12's copy (`q64-adaptive-dynamics/MCL/mcl-ecr/meta/mcl_kernel.py` 52-81, with
     falsifiable unit checks in `test_sir_stack.py` 17-28 there).
   - Its documents say the quotient is non-invertible and that a lossy quotient must not certify (`docs/USAGE.md` 76,
     111, 145). That is CUT-0's rule that the log never becomes an authority on the history. DECLARED.
5. **Overclaims.** ESTABLISHED.
   - "Anisotropic perturbation spectra" in the description, against `perturb`, documented and coded isotropic (108-116).
   - "Provenance-chained" for an unchained digest.
   - "Certifying structural admissibility" for the constant string `"structural_admissibility_only"` (`sir_runtime.py`
     200-206).

### 2.10 DEEQN64 (f800fb2, 2026-06-03) and Q64-adaptive-dynamics (daacbfe, 2026-05-30)

The two share the description "Did the system stay within its own certified geometric manifold?". DECLARED.

1. **Meaning.** ESTABLISHED.
   - In the Python reference engine, "manifold" is the top-k eigenspace of a 20-frame window covariance, and
     "converged" is a conjunction of float predicates (`_runtime/q64_stratified_engine.py` 199-218):
     - a normalized PCA residual below ε;
     - the rank within ±1 of its median;
     - spectral energy stable;
     - an eigen-gap.
   - "Stratified" is a fixed split of the 64-vector into four index ranges (`src/engine.rs` 126-130).
2. **Mechanism.** In the Rust crate `DEEQN64` builds, `Q64DomainEngine::update` (`src/engine.rs` 60-77):
   - reads only the state's length;
   - sets `converged = frame_count > 100`, under a comment calling it a placeholder (67-68);
   - computes a rank from the frame count (69).

   The H1 gate (157-181) therefore passes once enough frames have passed, whatever the state, NaN included. ESTABLISHED.
3. **Evidence.**
   - The Rust tests check construction and a dimension error only (195-214).
   - The Python tests make statistical assertions on synthetic data that can fail (`Q64-adaptive-dynamics`
     `tests/test_integration.py`, for example 80, 151). They were not run: NOT_MEASURED.
   - `Q64-adaptive-dynamics`'s `Cargo.toml` names `src/lib.rs` and `src/bin/validator.rs`, which do not exist, and its
     `pyproject.toml` builds with maturin. ESTABLISHED.
4. **CUT-0.** A different subject: continuous statistics of telemetry. Neither problem.
5. **Overclaims.**
   - "Certified": nothing is certified, and the Rust gate certifies the frame count. ESTABLISHED.
   - "Geodesic distance on Grassmannian" (354) for a chordal formula (368).
   - L12's `Q64_Production` copy returns the maximum on error (`src/q64/stratified_engine.py` 370-371).

### 2.11 The fixed-point lineage: DVSM-Draco (335a175), local folder L6, local folder L12, local folder L17

Nothing here bears on problem 1 or 2. It is listed because it is where Orlog's range-before-grid (e) meets the most
code.

- **`DVSM-Draco` `src/physics/fixed_point.rs` 104-107.** `q31_encode` clamps, then truncates by cast. The file's own
  contract says no NaN case exists. ESTABLISHED (re-read).
- **Local folder L6 `src/math/quantize_q31_32.rs` 46-69.** Orlog's own scale, 2^32 in an i64.
  - It tests finiteness, then range, then truncates to the grid: Orlog's order, with each refusal replaced by a repair.
    Non-finite input returns 0 with a log line; overflow clamps with a log line.
  - Its round-trip check refuses an out-of-range value, and a test plants one and requires `Err` (262-267). That is the
    lineage's one falsifiable range plant.
  - ESTABLISHED (re-read).
- **Local folder L12 `src/molecular/torsion_injection.rs` 87-94.** `(value · 2^32) as i64`, followed by a clamp to the i64
  range that does nothing. NaN becomes 0. ESTABLISHED (re-read). The same folder's `src/compression/saec_math.rs` 34-38
  clamps silently to [−2, 2], and a test asserts the clamp (166-169). ESTABLISHED.
- **`dvsm-meta-kernel` `Research/MengerSponge/KERNEL.rs` 105-112, and local folder L17.** `quantize_q64`:
  - non-finite input becomes 0;
  - out-of-range values are clamped into [0, 1);
  - values are truncated through f64.

  The test named NaN rejection (`TEST_SUITE.rs` 79-91) asserts acceptance and zeroing. Local folder L17 is a
  superset of the repository's folder and is newer overall. ESTABLISHED.

### 2.12 Local folders L10 (2026-06-16) and L9 (2026-10-25)

- **L10's `manifold_core.py`.** A graph's identity is the hash of (n, normalized edges, integer Laplacian) (32-54,
  re-read): a quotient by edge order, orientation, duplicates and self-loops.
  - Nine tests can fail (`tests/test_manifold.py` 14-57).
  - Node ids are not range-checked: a negative id aliases through Python indexing.
  - Problem 1: partial. The capture seam is a working instance of (d): an exact core, with a soft observable beside it
    and outside the hash.
  - ESTABLISHED.
- **L9's `nearmiss/nearmiss/record.py`.** The `result` block is digested (66-114, 123); `diagnostics`, holding
  float residuals and the environment, is not (115-122). Both re-read. `nearmiss/nearmiss/digest.py` refuses NaN (12),
  and corruption tests require refusal (`nearmiss/tests/test_corruption.py` 41-85).
  - "Lattice" there is the Z² sum of an Epstein zeta function, a different subject.
  - Problem 1: the two-layer shape without its outer seal.
  - ESTABLISHED.

### 2.13 DVSM-Atmos-Kernel (0a019a2), SymFlow-DVSM-Lattice (2e18f7d), DVSM-Protocol (2b25d0c), DVSM-Pulse (87905b5)

None of these has a test. All findings are ESTABLISHED.

- **`DVSM-Atmos-Kernel` `README` 1263-1516 (Rust in prose): the "causal quotient".** The closest in intent to problem 1
  in the DVSM line, and broken:
  - payload bytes are never hashed (1479-1495);
  - layers are sorted by size before hashing (1466), so opposite causal orders give one signature;
  - events without edges vanish (1413-1416).
- **`DVSM-Atmos-Kernel` `DVSM_UNIFIED_CLOSED_SYSTEM.swift` 136-140.** `DVSMReachOperator.compute` returns the empty set
  (re-read). As a "can K reach the claim" operator, an empty reach would hold every claim. This is the anti-pattern a
  CUT-0 plant must catch.
- **`SymFlow-DVSM-Lattice`.** "Lattice" is rounding to a 0.125 grid that returns a residual, which is then discarded
  (`DVSMExecutionContract.swift` 57-76, 100). Ingest is "most recent wins", with overwritten arrivals only counted
  (`DVSM-SymFlowRuntime.swift` 40-99). That is the direct contrast to CUT-0's SLOT-FILLED and explicit drop.
- **`DVSM-Protocol` `DVSMGeometricManifoldKernel.swift`.** The DVSM line's one real Riemannian geometry: ψ on S¹⁵, a
  Rayleigh residual, an exponential map (73-79, 177-181). A different subject. Its "exact Hessenberg least-squares"
  solve divides by the diagonal (162-171).
- **`DVSM-Pulse`.** "Topology" is a shard registry. The snapshot hash is a per-process seeded `hashValue` (KERNEL
  SPECIFICATION LAYER 180-190).

### 2.14 Naming only, or nothing (one line each)

| repository or folder | read at | finding |
|---|---|---|
| `DUME.doc` | 30c5437, 2026-05-05 | prose; its "checksum" is the string id-count (`Engine/Engine/DataEngine` 157). ESTABLISHED |
| `DUME-DVSM` | f372a97, 2026-05-06 | comments only. DECLARED |
| `DUMEwow` | 6d0e383, 2026-05-07 | the "stratified lattice" is a 3-case enum; does not compile (an arity mismatch at `regime_governor.rs` 68). ESTABLISHED |
| `dume-hybrid-engine` | 94a7667, 2026-05-04 | "manifold" is a k-NN graph (`Sources/Manifold/GraphEvolution.swift` 101-247); Package.swift's target paths do not exist. ESTABLISHED |
| `DUME-Strick-Gov` | 9b92d01, 2026-05-05 | a placeholder graph layer; ReplayVM's "hash" is the sum of its inputs (`DVSMExternalSystemContract.swift` 184-190). ESTABLISHED |
| `3x-DVSM` | ad59e86, 2026-05-06 | ManifoldProjection is the identity, +0.001 or a random float. ESTABLISHED |
| `dvsm-v3`, `-dvsm-v3`, local folder L1's `dvsm-v3` (newest) | 7212621 / 786b30c, 2026-05-18 | keywords in prose only; the replay hash is an XOR fold, so frame order is lost and equal frames cancel (`src/lib.rs` 290-301). ESTABLISHED |
| `DQSDv2` | 1bcbeae, 2026-05-18 | the tree is empty: the description's Q16/Q31/Q64 backends do not exist at HEAD. ESTABLISHED |
| `DQSDv2GPU` | 1b67b5e, 2026-05-18 | "reset manifold" zeroes the vector above an energy bound (`README.rs` 133-150), a clamp. ESTABLISHED |
| `anamorph-chaos-sweep` | 504ac58, 2026-07-08 | "manifold" is an ODE state space (`Research/chaotic_coupling.rs` 50-54). ESTABLISHED |
| `AIS2` | 175eac8, 2026-06-09 | naming only; the folders its README describes are absent at HEAD. ESTABLISHED |
| `Q64_Production` | 182135b, 2026-06-05 | LICENSE only (the code is in local folder L12's `Q64_Production`, section 5). ESTABLISHED |
| `MCL-ECL-SDK` | — | an empty repository. ESTABLISHED |
| `deterministic-kernel`, local folder L3 | GitHub head holds only LICENSE; the local checkout a00b7a0 (2026-06-07) has the code, with uncommitted work | "topology" is a hash of (dimension, nonzero count, seed) (`src/lib.rs` 332 onward). ESTABLISHED |
| `executable-epistemics`, local folder L4 | ae1b38d, 2026-06-13 | "stratum" is a median split (`studies/exp003_moderator/analyze_exp003.py` 145-146); the quotient is single-linkage clustering. ESTABLISHED |
| local folder L5 | 2026-06-11 | prose; it says the quotient map is non-invertible (`MCL-ECR.txt` 116, 204). DECLARED |
| local folder L2 | 2026-05-19 | prose specifying a free-monoid trace space and fibers of a lossy Ω. DECLARED |
| local folders L11, L13, L14 | 2026-06-07, 2026-10-10, 2026-06-07 | data and prose; L11's forensic record reports event_count 0 with every check true, a vacuous pass. ESTABLISHED |
| local folder L16 | 2026-06-09 | `Notes.txt` defines history equivalence as "no intervention sequence can induce a divergence", a Nerode-style congruence; prose, PDFs skipped. DECLARED |
| local folders L20, L21, L19 | 2026-10-25, 2026-10-14 | ordinary uses of "projection"; nothing |
| local folder L15 | — | third-party open-source checkouts; the "manifold" hits are theirs (for example `sklearn/manifold`); no owner design |

## 3. The reviewer's four angles, against the lineage

| angle | nearest prior design | what it actually is | verdict for CUT-0 |
|---|---|---|---|
| a stratified state space | `RESEARCH_GRADE_CORE.rs`'s active set | an interval's interior and two faces over reals, with a non-injective contact log | the shape only; no lineage design stratifies discrete session states (which ports are filled, which frames are open) |
| the fibers of the history-to-log projection | Urðr `inputset`; Verðandi's WORKSHOP-0 census; Semiotic core's `quotient`; the Firewall Spec pair test; `DVSM_ODCN_Obs.swift`'s `fiber` | exact witness search over nested projections; an exhaustive single-edit census; exact class counting; a stated congruence test; hash fibers over a finite universe | usable as checks over the session probe's domain (section 4) |
| a dynamic configuration space for claims | Ursprung PO-10 | an existential-image abstraction of an exact reachable graph, with an admissibility check and a plant | the discrete form of the angle, and the template for problem 2 |
| operational singularities as minimal pairs | `isChiral`'s one swap; Urðr's head-time defect "differs by one expression"; CUT-0's own pairs C1 to C5′ | minimal pairs as test generators | CUT-0 already uses minimal pairs; the lineage adds event-level generators (swap, insert, delete one event) |

## 4. Synthesis

**What the prior designs give CUT-0 that it lacks.**
1. **A determination check for problem 1** (Urðr `inputset`, re-read).
   - Over the session probe's exhaustive domain, for each quantity the contract names, compute the coarsest record that
     determines it: input log, then history.
   - Where the log is not enough, the check prints two histories with one log and two values.
   - This decides the reviewer's "which differences must survive" quantity by quantity, instead of by argument.
2. **A history census for problem 1** (Verðandi's WORKSHOP-0, re-read).
   - Every single-event mutation of a history is classified by which of log, core and seal moved.
   - Two laws are held: log unmoved ⇒ core unmoved, and history moved ⇒ seal moved.
   - Impossible arms are refused.
   - The session probe mutates logs byte by byte and checks named history pairs (case X). The census would add the
     systematic form: every single-event mutation of every history in its domain, each classified.
3. **An admissibility harness for problem 2** (Ursprung PO-10, re-read and run).
   - The premise: K's claim set contains the image of every resumed run's evaluations.
   - The conclusion: no claim held that a resumed run evaluates.
   - The plant: drop a reachable claim from K. It must be found both inadmissible and a false hold.
   - This folder's `resume_oracle.py` is the exact side. PO-10 is the harness shape, with one repair: the oracle's own
     open frontier must make the verdict LOG-OPEN, which PO-10 never reads.
4. **Plants the lineage shows are needed for K**, each a design that would have passed without one:
   - an empty reach holds every claim (`DVSM-Atmos-Kernel` 136-140);
   - a bounded or decaying walk under-approximates (Dentatus `consequence/propagation.py`; Ursprung's exactly-H walk);
   - a syntactic reach with a depth cut-off and bare-name calls only (Urðr `autoroute` 524-546).

   CUT-0's existing plants in `cut0_claims.py` test K's construction rule by rule: returns, loop bits, open claims,
   arms, descriptors, and the entry check. None cuts K off at a depth or a pass count, the under-approximation the
   lineage shows twice, so that plant would be new.

**Confirmations, not additions.** Each is the owner's own earlier finding of a rule CUT-0 already has:
- Semiotic core's C3 (no function of the log re-separates a log fiber);
- Urðr `recirc`'s honest/doctored collision;
- Urðr `netcode/session`'s "the codes carry what the state does not";
- L9's digested result beside undigested diagnostics;
- L10's exact core beside a captured observable.

All of them argue for CUT-0's history seal beside the receipt core.

**Naming only.** Every use of manifold, topology, stratum, lattice or quotient in these is naming only for CUT-0:
- the DVSM and DUME lines;
- the Q64 line;
- `mcl-observer-runtime`;
- `dvsm-meta-kernel`'s lockstep kernels;
- the fixed-point kernels;
- AIS2, anamorph-chaos-sweep and the DQSD repositories.

Their mathematics is either:
- real but continuous: Stiefel frames, Grassmannian subspaces, Riemannian spheres, single-linkage clustering, ODE state
  spaces; or
- a name on a clamp, an array, a threshold or a stub.

None of it models discrete histories, logs or continuations.

## 5. Where Orlog's designs could apply

The designs are lettered as the owner listed them:
- **(a)** the causal cut and continuation;
- **(b)** the session as a transition system (arrive, assign, drop, close, end; END-PENDING, END-UNDISPOSED);
- **(c)** the input log under a strict canonical grammar, tested by every single-byte mutation;
- **(d)** the two-layer binding (receipt core over the input log; session record binding history, log and core);
- **(e)** range-before-grid refusal for fixed-point inputs;
- **(f)** the monotonicity lemma for rules that withhold.

ESTABLISHED means the code the design would meet was read at the lines given.

| where | what is there | design | what it would add or catch | grade |
|---|---|---|---|---|
| `dvsm-meta-kernel` `dvsm_meta_kernel.rs` 39-41 | `fx(f64)` to Q32.32: NaN becomes 0, ±∞ and out-of-range values saturate, off-grid values truncate toward zero | (e) | INPUT-RANGE for non-finite and out-of-range values, then INPUT-GRID for 1.5e-10 and −0.7e-9, at Orlog's own scale | MEASURED (P4) |
| same, 145-239 | one drained buffer: no slot, no drop, no close rule, no end | (b) | SLOT-FILLED for the second SetVel (P5); a recorded drop for a command naming an unknown entity (P5); NOT-RUN when a player's command is missing at the close; END-PENDING for commands buffered at shutdown | MEASURED (P5); ESTABLISHED |
| same, 115-139, 228-235 | S_ECHO over state only; a rejected tick keeps its state | (d) | a core computed from the input log (so velocity, and every input, is bound); a session record that would make the rejected tick a recorded event instead of a silent no-op | MEASURED (P2, P3) |
| `dvsm-meta-kernel` `Deterministic ECS Kernel` 111-146, 234, 298 | an unframed binary command frame, built from the emptied buffer | (c) | an encode-decode round trip under a strict grammar fails at once (the frame is empty); single-byte mutations would show there is no decoder at all | ESTABLISHED (re-read) |
| `dvsm-meta-kernel` `2-Layer_Reality_Core/DVSM_Gated_Steifel_Runtime.rs` 622-638, 1084-1145 | drop-oldest ingest when full, wall-clock pacing, a loop that never ends | (b), (d) | each drop a recorded event; a session record that shows which inputs were stepped; an end rule for the buffered remainder | ESTABLISHED |
| `dvsm-meta-kernel` `Research/MengerSponge/KERNEL.rs` 105-112, 130-147, 358, 369 | `quantize_q64` repairs silently; the frame hash binds only constants | (e), (c) | refusals in place of repairs; the first single-byte mutation of the sensor input leaves the hash unchanged, which exposes that the bound value is identically 0 | ESTABLISHED |
| `dvsm-meta-kernel` `Minimal_Core/Minimal_Core.rs` 1515-1625 | the fracture rule: NaN drift never fractures | (f) | stating the withholding rule as a lemma forces "non-finite ⇒ withhold" | ESTABLISHED |
| `DVSM-Draco` `src/physics/fixed_point.rs` 104-107 | `q31_encode` clamps, then truncates | (e) | refusals in place of the clamp and the cast | ESTABLISHED (re-read) |
| local folder L6 `src/math/quantize_q31_32.rs` 46-69 | finite, range and grid checked in Orlog's order, each repaired | (e) | turn the three repairs into the three refusals; keep its round-trip plant | ESTABLISHED (re-read) |
| local folder L12 `src/molecular/torsion_injection.rs` 87-94, 151-161, 175 | cast at 2^32, a clamp that does nothing, a non-fatal CRC mismatch, narrowing to f32 | (e), (d) | refusal at the door; a receipt that binds the bytes injected, not a value narrowed after the fact | ESTABLISHED (re-read for 87-94) |
| Dentatus `lockstep/tick.py` 45 | a missing input becomes 0; a float input is truncated | (b), (e) | NOT-RUN INPUT-MISSING for the absent input; INPUT-GRID for the float | ESTABLISHED (re-read) |
| Dentatus `lockstep/rollback.py` 71-72 | predicted inputs hashed into the corrected track | (d), (b) | the core binds only affirmed inputs; ticks past the affirmed prefix are LOG-OPEN, never sealed | ESTABLISHED (re-read) |
| Dentatus `chronicle/core.py` 81-83, `airlock/membrane.py` 64-68, `quorum/tally.py` 159-160 | refusals unrecorded or unchained; rejected votes outside the certificate | (d) | a history record of refusals, chained and bound beside the core | ESTABLISHED |
| Urðr `tools/netcode/session.py` 297-316 | swept schedules contain no refused arrival | (b) | CUT-0's session cases (a refusal then a retry, a retry after the close, a slot filled twice) inside the convergence and segmentation sweeps | ESTABLISHED (re-read) |
| Urðr `urdr/snapshot.py` 55, 68-69 (with `urdr/values.py` 75-83) | the loader rebuilds MEASURED from the file's strings; `int()` coerces | (f), (c) | a load rule that may only withhold (demote or refuse), never raise; a strict grammar for the snapshot file | ESTABLISHED |
| Urðr `urdr/parser.py` 519-521 to `urdr/values.py` 17-19 | an out-of-range integer literal wraps | (e) | INPUT-RANGE (there is no decimal input, so no grid refusal applies) | ESTABLISHED |
| Ursprung `weltwerk/verify/abstraction_soundness.py` 77, 137-141 | `frontier_open` computed and never read | (a) | the LOG-OPEN discipline: a truncated graph gives a BOUNDED verdict, never CLOSED | ESTABLISHED (re-read); fixtures closed, MEASURED |
| Ursprung `experiments/live_world_kernel/claim_lattice.py` 129-226 | a claim lattice with no withhold operator, and three checks that cannot fail | (f) | the lemma states what withholding does to fixed points; the plant discipline makes the checks able to fail | ESTABLISHED |
| `mcl-observer-runtime` `mcl_sdk/sir_runtime.py` 79-81, 207-208 | `json.load` with no grammar; an unchained `chain_hash` | (c), (d) | a canonical corpus grammar; a record binding the corpus digest, the kernel fingerprint and the result | ESTABLISHED |
| `DEEQN64` `src/engine.rs` 60-77 | `update` reads only the state's length | (e) | a door on the 64 values (NaN accepted today), though the gate itself does not read them | ESTABLISHED |
| local folder L12 `q64-public-repo/src/validity_core.py` 63-71, 89-98 | `meet` is a product; monotone degradation asserted at run time | (f) | a lattice-law check catches `meet`; the lemma replaces an assert that `python -O` removes | ESTABLISHED |
| local folder L12 `Q64_Production/tests/verification/runtime/lattice_algebra.py` 142-180 | a quotient-morphism test that passes on singleton classes | (c) | enumeration with mutations; a singleton class counted as untested, never as a pass | ESTABLISHED |
| local folder L8 `genesis/gen004_commitments.py` 88-107 | tamper checks that cannot fail | (c) | re-derivation plus every single-byte mutation of every stored record | ESTABLISHED |
| `DVSM-Atmos-Kernel` `DVSM_REAL_CORE` 806-828 | a Reject clears the whole command buffer | (b) | per-command drops and END-UNDISPOSED make each disposal explicit | ESTABLISHED |
| `DVSM-Atmos-Kernel` `README` 1479-1495 | a causal signature that never hashes payload bytes | (c) | the first single-byte mutation of any payload leaves the signature unchanged | ESTABLISHED |
| `SymFlow-DVSM-Lattice` `DVSM-SymFlowRuntime.swift` 40-99 | most-recent-wins ingest | (b) | SLOT-FILLED and explicit drops | ESTABLISHED |
| `DVSM-Protocol` (CONVERGENT, v21, `DVSMCore.swift` 18-20) | `Int64(v · 1e6)` traps on NaN, ∞ and out-of-range values, and truncates | (e) | the trap becomes a refusal; off-grid values are refused instead of truncated | ESTABLISHED |
| L9's `nearmiss/nearmiss/record.py` 115-123 | diagnostics outside every digest | (d) | an outer seal binding the result digest with a digest of the diagnostics | ESTABLISHED |
| local folder L10 `manifold_core.py` 32-47 | node ids not range-checked; self-loops dropped silently | (e) | a door refusing ids outside [0, n) and self-loops before canonicalizing | ESTABLISHED |
| `deterministic-kernel` (local) `src/lib.rs` 98-139 | saturating Q32.32 add and subtract; multiply truncates; divide at the wrong scale | (e) | refusals at the arithmetic's range | ESTABLISHED |

**The causal cut (a) has no other natural host in the lineage.** No repository has a structured interpreter whose
refusal could carry a frame stack. The nearest are:
- Dentatus's rollback, where "the last valid tick" is a cut over ticks, not frames;
- Urðr's segmentation law, which cuts sessions, not runs.

Applying (a) there would be a new design, not a repair. DECLARED.

## 6. What was run, and what this record does not show

**Run here.** PYTHONHASHSEED=0, PYTHONUTF8=1; rustc 1.96 and CPython 3.14.
- **`dvsm-meta-kernel` `dvsm_meta_kernel.rs`.**
  - The file as published, compiled with `rustc -O`, run twice: PASS both times.
  - The probe in the appendix: the file's lines 1-269 unchanged plus a new `main`. Run twice, byte-identical.
  - Both were built outside the repository from `git show HEAD:dvsm_meta_kernel.rs`. This is a self-contained,
    standard-library file whose `main` is its own smoke test.
- **`mcl-observer-runtime` `tests/test_sdk.py`.** Run directly with `-I -B`: 8 of 8. A self-contained standard-library
  test file.
- **Ursprung `weltwerk/verify/test_abstraction_soundness.py`.** Run with `-B` from the clone's root: 5 of 5. A
  self-contained standard-library test. Then `build_concrete` was read for the two fixture worlds (frontier closed in
  both) through a one-line import of the same module.

No other code from any repository was run. The two clones run in (`mcl-observer-runtime`, Ursprung) showed a clean
`git status` after each run. `dvsm_meta_kernel.rs` was built outside its clone, whose checkout had failed before any
run.

**Does not show.**
- That any lineage mechanism works on CUT-0's domain. Sections 4 and 5 propose; nothing was built.
- Whether the many drafts that do not compile would behave as read. Where a statement depends on a language or library
  rule that was not read here (Rust's float-to-int cast, nalgebra's `normalize`), the delegated readers marked it
  DECLARED.
- The Python Q64 tests, which need numpy and were not run (NOT_MEASURED).
- Every file of `dvsm-meta-kernel` (126 files with "manifold"), of Urðr (185 with the vocabulary), or of L15
  (about 53,000 files). The readings sampled each by keyword, then read the designs that compute something.
- Any claim about the owner's intent. The record reads what the code does.

## Appendix: the observation probe for `dvsm_meta_kernel.rs`

This `main` replaces only the repository's `main` (its lines 270-276). The repository's lines 1-269 precede it
unchanged.

```rust
fn main() {
    // P1: the smoke test's loop, each tick's return counted.
    let mut server = Server::new();
    let (mut some, mut none) = (0usize, 0usize);
    for _ in 0..128 {
        server.buffer.push(Command::Spawn(1));
        server.buffer.push(Command::SetVel(1, [fx(1.0), fx(0.0), fx(0.0)]));
        match server.tick(vec![12345, 12345]) { Some(_) => some += 1, None => none += 1 }
    }
    println!("P1 smoketest loop: ticks returning Some {} / None {}", some, none);
    // P1b: the same loop, with peers that agree with each tick's own hash (computed on a shadow server).
    let (mut shadow, mut agreed) = (Server::new(), Server::new());
    let (mut baseline, mut differs_at): (Option<u64>, Option<usize>) = (None, None);
    for k in 0..128 {
        for s in [&mut shadow, &mut agreed] {
            s.buffer.push(Command::Spawn(1));
            s.buffer.push(Command::SetVel(1, [fx(1.0), fx(0.0), fx(0.0)]));
        }
        let _ = shadow.tick(vec![]);
        let local = s_echo(&shadow.ecs);
        match (baseline, agreed.tick(vec![local, local])) {
            (None, Some(x)) => baseline = Some(x),
            (Some(b), Some(x)) if b != x && differs_at.is_none() => differs_at = Some(k),
            _ => {}
        }
    }
    println!("P1b smoketest's comparison with agreeing peers: first differing tick {:?}", differs_at);
    // P2: a rejected tick, P3/P3b: S_ECHO's fibers, P4: fx, P5: the buffer.
    let mut s = Server::new();
    s.buffer.push(Command::Spawn(7));
    s.buffer.push(Command::SetVel(7, [fx(2.0), fx(0.0), fx(0.0)]));
    let r = s.tick(vec![]);
    let after = s_echo(&s.ecs);
    println!("P2 rejected tick: returned {:?}; state equals the snapshot pushed this tick {}; depth {}; tick {}",
             r, after == s.rollback.back().unwrap().hash, s.rollback.len(), s.tick);
    let (mut a, mut b) = (ECS::new(), ECS::new());
    a.spawn(1); b.spawn(1);
    a.vel[0] = [fx(1.0), fx(0.0), fx(0.0)];
    let before = s_echo(&a) == s_echo(&b);
    for e in [&mut a, &mut b] { for j in 0..3 { e.pos[0][j].0 += e.vel[0][j].0 / 60; } }
    println!("P3 equal pos, different vel: equal before {}; equal after {}", before, s_echo(&a) == s_echo(&b));
    let mut c = ECS::new(); c.spawn(9); c.alive[0] = false;
    println!("P3b one dead entity vs empty world: equal {}", s_echo(&c) == s_echo(&ECS::new()));
    for (name, v) in [("NaN", f64::NAN), ("+inf", f64::INFINITY), ("1e30", 1e30), ("-1e30", -1e30),
                      ("1.5e-10", 1.5e-10), ("-0.7e-9", -0.7e-9)] {
        println!("P4 fx({}) = raw {}", name, fx(v).0);
    }
    let mut t = Server::new();
    t.buffer.push(Command::SetVel(42, [fx(5.0), fx(0.0), fx(0.0)]));
    let h0 = s_echo(&t.ecs);
    t.tick(vec![]);
    println!("P5 SetVel to unknown entity: hash unchanged {}; buffer left {}", s_echo(&t.ecs) == h0, t.buffer.len());
    let mut u = Server::new();
    u.buffer.push(Command::Spawn(3));
    u.buffer.push(Command::SetVel(3, [fx(1.0), fx(0.0), fx(0.0)]));
    u.buffer.push(Command::SetVel(3, [fx(4.0), fx(0.0), fx(0.0)]));
    u.tick(vec![]);
    println!("P5 two SetVel in one tick: vel x raw {} (fx(4.0) raw {})", u.ecs.vel[0][0].0, fx(4.0).0);
    let mut w = Server::new();
    w.buffer.push(Command::Spawn(3));
    w.buffer.push(Command::Spawn(3));
    w.tick(vec![]);
    println!("P5 Spawn(3) twice: entities {}", w.ecs.entities.len());
}
```

The output recorded here (both runs identical):

```
P1 smoketest loop: ticks returning Some 0 / None 128
P1b smoketest's comparison with agreeing peers: first differing tick Some(1)
P2 rejected tick: returned None; state hash after 5152288395182987663 equals the snapshot pushed this tick true; rollback depth 1; tick counter 1
P3 equal pos, different vel: s_echo equal before one step true; equal after false
P3b one dead entity vs empty world: s_echo equal true
P4 fx(NaN) = raw 0
P4 fx(+inf) = raw 9223372036854775807
P4 fx(1e30) = raw 9223372036854775807
P4 fx(-1e30) = raw -9223372036854775808
P4 fx(1.5e-10 (below 2^-32)) = raw 0
P4 fx(-0.7e-9 (off grid, negative)) = raw -3
P5 SetVel to an unknown entity: state hash unchanged true; buffer left 0
P5 two SetVel for one entity in one tick: vel x raw 17179869184 (fx(4.0) raw 17179869184)
P5 Spawn(3) twice: entities 2
```

The appendix's `main` is a condensed form of the one that was run: the same probes in the same order, with shorter
labels. The output above is the run's own. A rerun of this condensed `main` prints the same values under its own
labels.
