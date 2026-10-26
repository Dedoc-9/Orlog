# Debate record: the foundations architect's report (2026-10-25)

A subagent's report, saved verbatim by the judge. It is model output, not the owner's words, and carries no
authority: the judge's verdict (VERDICT.md in this folder) weighs it against the use-case skeptic's report. Its scratch
probes were in `work/arch-review/` (ignored by git). Its numbers are OBSERVED once on one host.

---

# Ørlǫg: the next steps, ranked by foundational value

I read README, AGENTS, STATUS, DOCTRINE (§1, §8, §9), SPEC (body and §11–§14), RUNTIME-SPEC, ADMISSION and court/RECORD. I also read the whole of `src/orlog/`, plus the state, exit and argv code of the C, Rust and Python runtimes. I changed no tracked file. My seven scratch probes are in `work/arch-review/` (ignored by git). Every number below is OBSERVED once on this host: software timings, with a `perf_counter` step of 1e-7 s.

## What the code says, and why it sets the order

1. **A program is closed.** No statement reads anything from outside (SPEC.md:69-88), so a receipt is a function of the law alone. The court already lists "any input but this one" as unmeasured (court.py:284-285). There is no time: a simulation is a For loop with a literal count (examples/fall.orl:15).
2. **Each compiled run is its own process.** C keeps the run's state in statics (rt_c/orlog_rt.h:270-283), opens its files from argv (:1365-1381) and ends with `exit()` (:433-458). The C generator makes variables and text slots static (gen_c.py:291-297), and E21's memory bound relies on "no recursion, so one live instance" (gen_c.py:271, :292; DOCTRINE.md:392). Rust and the Python backend read argv and exit (rt_rs/orlog_rt.rs:883, :1384; rt_py.py:74-87, :119-126). The reference, by contrast, is already re-entrant: all its state is on `self`, a refusal is an exception, and output goes to a bytearray (interp.py:73-113).
3. **Identity is by place.** Clause ids are document positions (syntax.py:154, :226) and variable ids follow textual order (sema.py:97). The law is a list of `(clause id parent stmt)` lines (sema.py:600-608), and a claim's seal includes the whole law seal (court.py:141-144). OBSERVED with `edit_churn_probe.py`: rewording one Say changes the claim's seal, so a ratification would stop applying; inserting one Let after §1 of gcd_certificate.orl changes 23 of its 25 law lines.
4. **The ledger is not yet reliable.** It defaults to `ratified.jsonl` in the repository root (orl.py:23), which does not exist yet. An append calls fsync but takes no lock and does not link to the previous line (orl.py:118-122). `read_ledger` catches only FileNotFoundError (court.py:147-158): OBSERVED with `ledger_torn_probe.py`, a torn last line raises JSONDecodeError, so a crash mid-append breaks every court reading. The court artifact's `chain_hash` is a hash of the artifact itself, not a link to anything (court.py:289).
5. **What a check costs.** The reference walks 0.67–1.74 M counted operations per second on the corpus (leapfrog: 168,078 ops in 0.173 s). In cProfile, the isinstance dispatch in `eval` and `stmt` takes about 54% of the time, and the Fraction-based `x_mul` about 17% (numeric_ref.py:47-54, :117). The generated Python backend runs leapfrog in 0.081 s, but every process pays about 0.095 s of start-up. A four-way arbitration of a just-edited leapfrog takes 5.6 s, because C and Rust rebuild (builds are keyed by the source's sha, arbiter.py:112-141); warm, 0.66 s. So a preview must run in-process on the reference, and four-way arbitration belongs to admission.
6. **Grammar collisions are real** (`grammar_probe.py`). v0 accepts `Receive thrust as a fixed.` as a call when a procedure of that name exists, accepts `To move by d, do the following.` as a procedure named "move by d", and `tick` is an identifier in examples/fall.orl:15. v0 refuses with SYNTAX at the statement, whatever the rest of the text holds: `Let thrust be given each tick as a fixed.`, `Each tick, do the following.`, `Let physics be the law sealed <hex>.` and `To move, given d as a fixed, do the following.` Rule: spell every new form where v0 raises SYNTAX at the statement, and never reserve a new word.

## The ranked steps

### Step 0 (the gate, and step 1's first commit): COMPAT-0, the conservative-extension harness
- **Entails:** `tests/compat.py` and a frozen baseline of the current compiler's results (fc19339) over the 11 corpus programs and their spellings, the 291 hand-worked probes, and diff_twin's mutant sets from seeds 1 and 2 (seeds and digests stored, not texts). For each text: the refusal code and line, or the sha256 of its law bytes and of its receipt core. A self-test row requires the new compiler to reproduce every entry; the only exception is a text v0 refused, which a later version may accept. No contract changes.
- **Design:** conservative extension: every text v0 accepts keeps its law bytes and its receipt (MEASURED on samples; DECLARED in general, resting on the spelling rule above).
- **Anchor:** Recovery: every seal, ratification and admission record keeps its meaning.
- **Unblocks:** every language step (1, 9, 11), and protects every line of step 4's ledger.
- **Cost and risk:** low, about a day.
- **Falsifier:** plant `reserve-tick` (add `tick` to RESERVED, syntax.py:94-101): fall.orl is refused SYNTAX and the row must fail. Plant `law-line-format` (change one law-line spelling): every seal moves and the row must fail.
- **Not yet:** a fuzzing project; it reuses diff_twin's generators.

### Step 1: RUN-1, the open run (declared input ports, a tick block, inputs as events)
- **Entails:** a SPEC amendment §15, with spellings for the owner to rule: a port `Let X be given each tick as a T.` declares a read-only variable; one top-level `Each tick, do the following.` stands as the last top-level clause; new codes PORT-PLACE, TICK-PLACE, PORT-VARIABLE, with SPEC §13's phase table changed in the same commit. `orlog-law 1` only when a v1 form appears, adding `(port var "name" type)` and `(tick clause)` lines; v0 laws stay byte-identical. Each tick: event 'T' (u64 tick), then one 'N' per port in declaration order (u32 var plus the value encoding of RUNTIME-SPEC §5), then the body; binding a port counts 0 operations; a refusal ends the run. v1 traces start from `head0 = SHA-256("orlog-trace-1" || law_seal)`. `orlog-receipt 1` adds `ticks` and `input-log-sha256`, and replaces `output-sha256` with an `output-chain` (out_t = SHA-256(out_{t-1} || SHA-256(output of tick t))), so no snapshot needs a hash midstate (CPython's hashlib cannot export one); OUTPUT-TOO-LONG becomes per tick (SPEC.md:243's 2^30-byte total would end any long session). The input log, `orlog-inputs 0`, holds typed encodings only, written once by a Python input door (`src/orlog/door_input.py`: exact parsing, text through canon's literal policy); C and Rust never parse decimal text. Code: syntax.py, sema.py, interp.py (a `tick()`), lower.py, gen_py/gen_c/gen_rs, the three runtimes (log reader, 'T' and 'N', receipt 1), arbiter.py, court.py (evaluations over a log; the log's seal in provenance). A new `vectors/input-vectors.txt`; `runtime-vectors.txt` (841240b7…) untouched. Two commits: 1a the reference, the spec and COMPAT-0; until 1b brings the backends, the court reads REFERENCE-ONLY and holds no claim (court.py:200, :207).
- **Theorems:** *Replay*: a run has no source of nondeterminism but the log (no locale, clock, environment or randomness: RUNTIME-SPEC.md:25-27); every outside value is an event before it is read, so a run is a function of the law and the log, and the trace head commits to both (DECLARED; the arbiter MEASURES it per session). Prior art: deterministic lockstep (Bettner & Terrano 2001), rr (O'Callahan et al. 2017), event sourcing, Elm's update. *Alignment*: inputs are addressed by (tick, port), never by the order a law pulls them, so an edited law re-runs over an old log tick for tick (a pull statement would shift every later input after one extra read, which is why it is rejected). *Tick termination*: every loop is bounded and there is no recursion, so every tick terminates. *Capability*: a law reads only the ports it declares.
- **Anchor:** Recovery, Explainable, Exploration.
- **Unblocks:** all five use cases; steps 2–10 rest on it.
- **Cost and risk:** the largest early step; a v1 twin round is the owner's call; risks are grammar collisions, seal drift, and the court's meaning over many evaluations.
- **Falsifier:** COMPAT-0 green (all 11 corpus seals unchanged); a recorded 1,000-tick log for two or three open laws gives byte-identical receipt-1 on all four executions; plants `c99-drops-an-N-event` (localized at its first divergent event, arbiter.py:247-277), `backend-parses-decimal-input` (refused: the log holds only encodings), `misaligned-log-entry` (refused, not shifted).
- **Not yet:** a pull-style input statement; clock, random or file ports (randomness is a seeded port plus a PRNG written in the law); list or record ports; an end-of-session block; modules.

### Step 2: SNAP-1, snapshot, restore and branches
- **Entails:** `orlog-snapshot 0`, canonical bytes at a tick boundary: the law seal, the tick, ops, events, the trace head, the output-chain head, every top-level variable as (id, name, type, encoding), the claim accumulators (interp.py:82) and the cost counters (:83). The digest is SHA-256 of those bytes; it is not an event (when a host snapshots must not change the trace); the session record keeps each tick's trace head. `restore` in interp.py and in the three runtimes, so every continuation is held four ways. A session is an append-only tree: a refusal ends a branch, recovery forks from an earlier snapshot, and the refused branch stays in the record.
- **Theorem and design:** *complete-state continuation*: restoring S_n and replaying the inputs from tick n+1 reproduces every later head and the final receipt; completeness is what could fail, so one plant holds each component. Lineage: F-SNAP (STATE-TRANSACTION-0: a retained snapshot that aliased live lists was corrupted by later mutation, so snapshots are bytes, never object graphs); bench2 (journal rollback stayed flat in history length while replay grew, so keep both: snapshots to jump, replay to verify). A refusal is not rolled back: that would erase the refuted claim, and the court would only ever read "true in n of n" (a laundered verdict).
- **Anchor:** Recovery, Exploration, Explainable.
- **Unblocks:** save and load, rollback, crash recovery, preview from "now" (step 6), the session API's fork (step 3), native restore (step 10).
- **Cost and risk:** medium; the main risk is state completeness in C, because of the statics.
- **Falsifier:** restore at every k-th tick and continue: identical heads and receipt four ways. Plants, each caught: `snapshot-forgets-claim-accumulators` (claim lines differ), `snapshot-forgets-cost-counters` (ref-cost differs), `snapshot-aliases-a-list` (digest no longer matches), `snapshot-holds-a-midstate` (the reference cannot produce it).
- **Not yet:** state migration between two laws; delta snapshots; compacting the tree; replicas.

### Step 3: SESSION-0, an in-process session API, reference first
- **Entails:** `src/orlog/session.py`: `Session.open(raw bytes)`, `step(record)`, `snapshot()`, `restore()`, `fork()`, `view(name)` (no event), `trace(a, b)`, `receipt()`, `court(ledger)`, `arbitrate()` (writes the log, runs the backends as processes over it, extending arbiter.py:160-223) and `explain(tick)` (the refused clause, its code, that tick's inputs). A counted operation budget answers STOPPED-BY-HOST with no receipt (a host stop must never look like a law's refusal). `orl.py session` subcommands. Two tiers in the contract: a preview runs the reference in-process and holds nothing; admission is arbitrated.
- **Design:** the de Bruijn criterion (interp.py:3-4): the session is plumbing over the authority and needs no runtime change. Invariants: a session gives the same receipt, byte for byte, as a batch run of the same log; two sessions in one process share no mutable state.
- **Anchor:** Exploration (milliseconds per step), Explainable.
- **Unblocks:** steps 5 and 6, the UX and test harnesses; fixes the shape steps 8 and 10 implement.
- **Cost and risk:** low to medium.
- **Falsifier:** session, batch and arbitrated backends give the same receipts; two sessions interleaved tick by tick give the same receipts as each run alone (plant: a module-level cache shared between sessions); a budget stop written as a REFUSED receipt must be caught.
- **Not yet:** embedding the compiled backends; threads; a network; a GUI.

### Step 4: LEDGER-1, the world's ledger and the audit chain
- **Entails:** `src/orlog/ledger.py`, format `orlog-ledger 1`: each line JSON `{seq, prev: sha256 of the previous line's bytes, kind}`, kinds `ratify-claim`, `cite-theorem`, `admit-edit`, `undo-edit`. One writer under an exclusive OS lock (standard library), a whole line then fsync. On open, a torn last line is moved to quarantine and recorded, never dropped. The court refuses LEDGER-BROKEN instead of raising. The ledger lives in the world's folder, not the repository root. Court and witness artifacts record the ledger head and the input-log seal they read (court.py:274-290, arbiter.py:296-322). Only console person-acts write it: no language construct, no RPC method. After an edit, carry-forward is shown as information only; it grounds nothing (R5, court.py:41-42).
- **Theorem:** tamper-evidence by accident, not authentication: anyone can recompute the chain (the same honest bound the line check states, seal.py:12-13). After a crash the ledger is as it was, or has one more whole line.
- **Anchor:** Recovery, Admission earned, Explainable.
- **Why now:** no ledger file exists yet, so the format can change at no migration cost. The concrete proposal for DOCTRINE §9 fork 5.
- **Cost and risk:** low; the risk is lock semantics on Windows.
- **Falsifier:** plants (a reordered line, a deleted middle line, a truncated last line) each end in LEDGER-BROKEN or quarantine, never a traceback (today's reader fails the torn-line row); a `ratify` method added to the RPC table fails the structural row; a GROUNDED claim, after an admitted edit, reads UNGROUNDED with the carry-forward note.
- **Not yet:** signatures, keys, roles, quorum, replicas, a remote ledger (the owner's ruling: a second human, a second machine or distribution first).

### Step 5: RPC-0, the test socket
- **Entails:** `src/orlog/rpc.py` and `orl.py serve`: JSON-RPC 2.0, one JSON object per line on stdio (MCP's stdio framing), ASCII output, single-threaded, answered in order. `initialize` returns `{protocol: "orlog-rpc", version: 0, methods, law_versions, receipt_versions}`; changing any method's shape makes a new version. v0 methods: initialize, shutdown, check, run, arbitrate, court (reading the ledger only), session.open / step / snapshot / restore / fork / view / trace / receipt / explain / close; v1 adds edit.propose and edit.preview. Laws and snapshots travel as base64, never as JSON strings (the door must see the raw bytes). Port values travel as strings, never JSON numbers (an i64 above 2^53 does not survive a JavaScript client). A refusal of a text is a result (`status: REFUSED` with code and line); JSON-RPC errors only for transport faults. No clock, pid or absolute path in responses; a counted operation budget per request.
- **Design:** a deterministic server is a function from a request transcript to a response transcript, so golden transcripts are byte-exact conformance tests; the method table is frozen per version and held to the server, as SPEC §13's phase table is held to the source.
- **Tests:** `tests/rpc/v0/*.in.jsonl` → `*.out.jsonl`, their sha256 recorded, byte-identical on two runs. Plants, each caught: the law decoded as text before the door (its door events vanish); an i64 as a JSON number (the 2^63−1 round trip fails); a `ratify` method (the method-table row fails); a timestamp in a response (two runs differ); a refusal sent as a JSON-RPC error (the transcript differs).
- **Anchor:** Exploration, Explainable, Admission earned.
- **Unblocks:** agents, the UX as a separate process, later LSP (diagnostics) and MCP (tools/list from the method table) adapters.
- **Why above step 6:** every external client speaks through it, including the agents that will propose edits, and a protocol's versioning must exist before its first client.
- **Cost and risk:** low.
- **Not yet:** a TCP or WebSocket listener (reachable from another machine is distribution; even a localhost one needs the owner's word); authentication; adapters until v0 is frozen; notifications; any method that writes the ledger.

### Step 6: EDIT-0, propose, preview, admit and undo, with exact inverses
- **Entails:** `src/orlog/edit.py` and `world.py`. An edit is `{base: law seal and text seal; ops: insert-after L TEXT | replace L TEXT | delete L; intent: text (data, never instructions); proposer: a label}`. Applying it: the outline renumbered deterministically (syntax.py:162-171 forces it); reference tokens rewritten through the lexer, never inside a literal; each line keeps its label spelling; the candidate passes the door, each repair shown. It produces an id map (clauses, variables, claims), the exact inverse checked before anything is written (it must reproduce the base byte for byte, or the edit is refused), and a churn report. Preview writes nothing (in Verðandi every evaluation appends an `evaluate` event, the "no scratch tier" gap the owner named): it re-executes the world's log under the candidate (REPLAY-FROM-ORIGIN), or continues from the current snapshot when the state is compatible (FORWARD-FROM-SNAPSHOT), named apart because they answer different questions; it gives the first divergence through the id map and the court before and after. Admit is a person's act at the console: head equal to base or HEAD-MOVED and nothing written; four-way arbitration of the main branch's log must agree; then one ledger line with the inverse and the hashes of the witness and court artifacts. Undo admits the stored inverse, refused (never searched for) when the rows it names no longer stand. First deliverable: a churn measurement over the corpus before any stable-identity layer is decided (mirrors LOCALITY-1, admitted as "measurement and report only").
- **Theorems:** the exact inverse (Verðandi 0254); staleness by compare-and-swap on the head (LEDGER-SAFE-0); preview determinism (from step 1); computation never grounds (R2) and an edited claim has a new seal, so an agent's edit can be admitted by a person but never raises a standing above WELL-FOUNDED.
- **Anchor:** all four.
- **Unblocks:** the UX, agents proposing over RPC v1.
- **Cost and risk:** medium to high (absorbed Otherwise arms, EMPTY-BLOCK after a delete, certificate or notwithstanding targets).
- **Falsifier:** for every corpus program and every generated single-clause edit, undo restores the base's sha256. Plants, each caught: an inverse that normalizes `3.1.` to `§3.1`; a regex rewriter that touches "§3" inside a literal; a writer that skips the head check; a preview not byte-identical when run twice.
- **Not yet:** state migration; merging concurrent edits (a second human is a trigger); commuting or glueing edits (Verðandi's GLUE-0); slice-bound ratification (the owner's fork 4); automatic admission; a UI.

### Step 7: HOST-0, determinism on a second host, measured
- **Entails:** `tests/host_compare.py` and a baseline recorded here (each corpus program's receipt-core sha256, output sha256 and trace head; later each recorded session; the vectors' sha and the self-test summary). The owner runs it on Linux x86-64 (WSL2 or a container: another libc and linker) and on ARM64 (another FPU and default NaN), with clang as pinned, gcc as a probe, CPython 3.11 beside 3.14. Predictions frozen first, risks named: correctly rounded sqrt, contraction off, the NaN-fold hazard (RUNTIME-SPEC.md:64-70).
- **Design:** an attempt to falsify T5 off this host (README: NOT_MEASURED).
- **Anchor:** Recovery: a recording replays elsewhere.
- **Unblocks:** any claim that a session replays on another machine; lockstep multiplayer.
- **Cost and risk:** low, hours.
- **Falsifier:** any differing receipt core, output byte or vector; control: on ARM, the FMA row's naive C loop must still diverge.
- **When:** the v0 baseline now; again after step 2.
- **Not yet:** CI, automated cross-machine comparison, signatures over results (running Orlog there for others would be distribution).

### Step 8: PERF-0, the reference's speed, measured, then a held fast path
- **Entails:** a benchmark that prints and asserts nothing. Then either (A) the generated Python backend loaded in-process (`rt_py` writing to buffers and raising instead of exiting): already held four ways, about twice the reference's speed, no 0.095 s start-up; or (B) a closure-compiled engine (Feeley & Lapalme 1987) held to interp.py as a fifth execution. Integer fast paths in the fast engine, held by the vectors; numeric_ref stays the definition.
- **Design:** the authority stays small and judges recordings, not the live loop.
- **Anchor:** Exploration, Recovery.
- **Unblocks:** larger worlds, faster admission, long replays; decides what step 10 embeds.
- **Cost and risk:** low for (A), medium for (B).
- **Falsifier:** agreement on the corpus, probes, mutants and sessions; plant: a fast `x_mul` that floors must be caught.
- **Not yet:** a JIT, C extensions, parallel ticks, frame-rate claims.

### Step 9: MODULES-0, sealed imports and parameters
- **Entails:** imports pinned by the full 256-bit seal (the four words are a 64-bit check for people), spelled `Let physics be the law sealed <hex>.` (SYNTAX in v0); flattened into the importer's clause numbering, so the event format is unchanged. Parameters `To move, given d as a fixed, …` (SYNTAX in v0), by value. Still no recursion, so the C backend's static slots stay sound under E21. Modules declare no ports and receive values only through parameters (Dennis & Van Horn 1966; Miller 2006).
- **Design:** content addressing (Unison, Dhall) plus step 0's conservative extension.
- **Anchor:** Explainable, Exploration, Admission.
- **Unblocks:** "a language" at scale; libraries (a PRNG, vector math); later gluing.
- **Cost and risk:** high (a SPEC amendment, a twin round, three generators).
- **Falsifier:** COMPAT-0 green; IMPORT-SEAL refuses a mismatched pin; a pin by seal words is refused; plant: recursion through an import must be caught.
- **Not yet:** a registry or fetching (distribution), recursion, records (entity data lives in one list per field until then, as leapfrog.orl does).

### Step 10: EMBED-1, re-entrant compiled runtimes
- **Entails:** RUNTIME-SPEC v1 beside v0. All of a run's state in one struct (the C statics plus the generated g_v, g_ts, g_cost; Rust's `St` already is one, gen_rs.py:294-305). No exit and no argv; output and trace to buffers. A refusal unwinds to the step (every refusing call returns a status, or setjmp, which RUNTIME-SPEC.md:17-18's header list would have to admit). One E21 temp stack per session. A C ABI: orl_open, orl_step, orl_snapshot, orl_restore, orl_receipt, orl_close.
- **Anchor:** Exploration, Recovery at native speed.
- **Unblocks:** native game hosts.
- **Cost and risk:** high; reopens C memory safety.
- **Falsifier:** four-way agreement unchanged; interleaved sessions match sessions run alone; ASan clean. Plants, each caught: a leftover static; a refusal that skips the temp-stack release.
- **Not yet:** threads, host callbacks during a tick, WASM.

### Step 11: NUMERIC-2, big integers and rationals
- **Entails:** new types (Int stays i64); a size bound, canonical forms (rationals normalized), operation counts in proportion to limb work (so T3's counted reading is not weakened further, DOCTRINE.md:118-119); numeric_ref extended; a new vector file; std-only bignums in both runtimes.
- **Design:** exactness in Z and Q; canonical forms give byte-identical events.
- **Anchor:** Explainable: exact certificates (Freivalds, BLR).
- **Unblocks:** none of the five use cases first.
- **Cost and risk:** high.
- **Falsifier:** vectors pass in both runtimes; plants, each caught: an unnormalized 2/4 in an event; a cost model off by one limb.
- **Not yet:** big floats, transcendentals, implicit promotion.

## Dependency graph

```
COMPAT-0 ─► RUN-1 ─► SNAP-1 ─► SESSION-0 ─► RPC-0 ─────────────► RPC v1 (edit methods)
   │          │                   │  │                              ▲
   │          │                   │  └─► EDIT-0 ────────────────────┘
   │          │                   │        ▲
   │          │                   │     LEDGER-1 (no prerequisite; before the first real ratification)
   │          │                   └─► PERF-0 ─► EMBED-1 (also needs SNAP-1's format)
   │          └─► MODULES-0 (painless later if ports and state are keyed by name)
   ├─► MODULES-0
   └─► NUMERIC-2
HOST-0: the v0 corpus now; again on recorded sessions after SNAP-1
```

Build order: COMPAT-0 → RUN-1a → LEDGER-1 (small, in parallel) → RUN-1b → SNAP-1 → SESSION-0 → RPC-0 → EDIT-0 → RPC v1 → PERF-0 → MODULES-0 → EMBED-1 → NUMERIC-2, with HOST-0 whenever the second environment exists.

## Build first: RUN-1, with COMPAT-0 as its first commit

1. Every use case needs it: none of the five can be reached from a closed program.
2. It is the hardest retrofit: it fixes receipt 1, trace 1 with its 'T' and 'N' events, the court's scope over a log, and the shape of every later API. Building the session API, the socket or the edit protocol first would freeze them around one closed run.
3. Its long-tail choices are cheap only now: one input record per tick (re-execution under edits stays aligned); inputs as events (the trace explains what came from outside); parsing once at the door (no strtod divergence across hosts); output chained per tick (no hash midstate); a refusal ends a branch (no refuted claim laundered).
4. It is the doctrine's own next rung, "capability inputs" (DOCTRINE.md:427): not drift.
5. It can land reference-first: the court honestly reads REFERENCE-ONLY until the backends follow.

## Rulings needed from the owner

- For RUN-1: the spellings; inputs exact-or-refused (the conversion rule) or rounded-and-noted (the literal rule); a refusal ends the branch; new headers (orlog-law 1, orlog-trace-1, orlog-receipt 1); whether a v1 twin round comes before 1b; fork 3 (floats in identity), which float ports inherit; its admission record (fork 8).
- Fork 5: LEDGER-1, as the proposal for it.
- Fork 4: whether to bind a ratification to the claim's backward slice (Weiser 1981) rather than the whole law, so it survives unrelated edits. It weakens R5, so it is his ruling. Its falsifier: mutating anything outside the slice must leave the claim's evaluations unchanged, and a slicer planted to drop control dependence must be caught.
- Before the court becomes the audit trail, STATUS.md's second-round court record should be closed (hygiene, not a step).
