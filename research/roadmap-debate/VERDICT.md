# Verdict: the next steps, ranked by foundational value (2026-10-25)

The judge's verdict on the foundations review. It weighs the three reports saved verbatim beside it (ARCHITECT.md,
SKEPTIC.md, PROSECUTOR.md), the owner's two interventions of the same evening (on what agreement measures and where the
ground ends; on hardening that pays twice), and what was measured while the debate ran. It is model output, like the
reports, and decides nothing for the owner: every rung below waits for his word, and a rung that changes a contract
changes it under a new version.

**The question.** Rank the next steps by their foundational value for one system with many uses: a game or reality
engine, a language, an API, a user interface that accepts edits, and sockets and tools for testing. The owner's anchor
for such a system, which the skeptic read literally: "Exploration should be cheap. Recovery should be reliable.
Generation should be explainable. Admission should be earned."

The verdict is set out as an OODA loop: what was observed, how it orients the choice, the decision, and what was acted
on in this round.

## 1. Observe

**The architect read the code** (ARCHITECT.md, its probes OBSERVED once):
- A program is closed: no statement reads from outside, so a receipt is a function of the law alone, and there is no
  time.
- Each compiled run is its own process, with its state in statics; the reference alone is re-entrant.
- Identity is by place: inserting one Let after §1 of gcd_certificate.orl changes 23 of its 25 law lines, and a claim's
  seal includes the whole law seal, so rewording any clause ends every ratification.
- The ledger was not reliable: a torn last line raised a JSON error in every court reading.
- Cost: the reference walks 0.67–1.74 M counted operations a second; a four-way arbitration of a just-edited law takes
  5.6 s, 0.66 s warm.
- Grammar: new statement forms must be spelled where v0 raises SYNTAX at the statement, and no new word reserved.

**The skeptic measured runs** (SKEPTIC.md, MEASURED once on a busy desktop):
- Ticks are cheap: 28 µs a tick of fall.orl in the reference, 1.3 µs in C.
- Processes are not: 12.5 ms to start a native program, 107 ms for Python, about 300 ms for `orl.py` before any work.
- Every text change is a rebuild, 0.33–1.3 s, and the C build at -O2 grows faster than linearly in the law (336 s at
  10,000 clauses; 1.65 s at -O0).
- Two defects: two programs arbitrated at once in one work folder gave 16 agreements in 48, with 18 false
  BACKEND-DISSENT, 3 false REFERENCE-DISSENT and 11 tracebacks; and nothing bounded a run (a legal loop of 10^9 steps
  was killed by its watchdog after 20 s).

**The prosecutor audited the documents against the code** (PROSECUTOR.md): 57 findings, two of them high. chaos.orl
still carried the claim the court had found FATAL (L16), and a failed build was counted as a dissent. Their
dispositions are in §5.

**The owner added three things:**
- Four-way agreement measures what the executions do not share. He asked which it is, for each layer.
- The court's terminal ground is social, so its trustworthiness is not auditable by reading code. He ranked its limits.
- Five measures pay twice, for security and for reproducible simulation, and they reshuffle the ranking. HOST-0
  becomes the test that defines the numeric and ordering seals; the bounded-run defect jumps the queue; and snapshots
  and the ledger gain a second justification.

## 2. Orient

**Where the architect and the skeptic agree:**
1. **Inputs are the foundation.** The architect's RUN-1 is first after its gate; the skeptic's "inputs as data" is
   first after a ruling. Without inputs, every variation is a new law, every test case is a build, a note edit is a
   rebuild, and a game cannot start. None of the five uses is reachable from a closed program.
2. **Two speeds.** A preview runs the reference in one process (3.4 ms a case, against 531 ms through `orl.py`). The
   four executions and the court belong to admission (1.6–4.0 s cold).
3. **Purity and bounds before any client.** A socket in front of the arbiter as it stood would have delivered false
   dissents and unbounded runs (the skeptic's server-shell probe: killed).

**Where they part, and the verdict on each:**
1. **The gate.** The architect wants COMPAT-0 first: a frozen record of every existing text's law bytes and receipt.
   The skeptic wants an owner ruling first: is a world property part of the law, of its inputs, or a data section
   sealed apart? *Verdict:* both, in parallel. The ruling shapes RUN-1; COMPAT-0 protects every rung whatever the ruling
   is, and costs a day.
2. **Edits.** The architect proposes an edit language with exact inverses (EDIT-0). The skeptic measured that whole
   texts plus the content-addressed build cache already make undo exact and fast (85 ms, a cache hit), and that an edit
   language brings back the problem Verðandi's 0254 had to solve. *Verdict:* the skeptic's whole-text history first, an
   edit language only if the architect's own first deliverable, a churn measurement, shows whole texts do not suffice.
3. **Sockets.** The architect puts a JSON-RPC server after the session API, so that a protocol is versioned before its
   first client. The skeptic puts a resident worker early and a socket only when a remote client exists. *Verdict:* they
   agree in substance. The gain is being resident (a pipe round trip costs 0.053 ms, a process start 300 ms), not having
   a socket. The transport is JSON lines on stdin and stdout with byte-exact golden transcripts. A TCP listener waits
   for a remote client and the owner's word.
4. **A second host.** The architect runs HOST-0 "whenever it fits", the skeptic ranks it 11th. The owner moved it: it
   is the test that defines the numeric and ordering seals. *Verdict:* run v0's baseline now, before RUN-1 freezes
   receipt 1 and the input encodings, so that a difference between hosts changes a seal nothing yet rests on.

## 3. Decide: the ranking

Each step says what it entails, the theorem or design it rests on, the part of the anchor it serves, and the falsifier
that could fail it. Cost is the reports' estimate, not a measurement.

### Done in this round (the queue-jumpers)
Isolated arbitrations, bounded reference runs, honest failed builds, a ledger that fails closed, vectors checked by
something other than their generator, and the independence rows. §4 gives each with its evidence.

### 1. COMPAT-0: the conservative-extension gate
- **Entails:** `tests/compat.py` and a frozen baseline at a named commit, recording for every text either its refusal
  code and line or the sha256 of its law bytes and receipt core. The texts are the 11 corpus programs, the 291
  hand-worked probes, and diff_twin's mutant sets, stored as seeds and digests. A self-test row requires the compiler to
  reproduce every entry; a text v0 refused may later be accepted. `tests/corpus_seals.py`, written this round, is its
  first column.
- **Theorem:** conservative extension. Every text v0 accepts keeps its law bytes and its receipt. MEASURED on the
  samples, DECLARED in general, resting on the spelling rule: new forms only where v0 raises SYNTAX.
- **Anchor:** recovery. Every seal, ratification and admission record keeps its meaning.
- **Falsifier:** the plant `reserve-tick` (fall.orl uses `tick` as a name) must turn the row red, and so must a changed
  law-line spelling.
- **Cost:** about a day. **Not yet:** a fuzzing project; it reuses diff_twin's generators.
- *Built 2026-10-26, at the owner's word ("Start COMPAT-0, the conservative-extension gate, as the next rung"):*
  `tests/compat.py`, with v0 frozen at b4eaf11. It holds 3,361 texts (every version of every corpus program in the
  history, the 291 probes, 57 fixtures and 3,000 mutants) as stored texts rather than seeds, since the mutator's pool
  changes whenever a fixture is added. Its plants: reserve-tick, law-line-format, say-counts-twice (a change only the
  receipts see), frozen-text-altered. What it does not protect, at his request, is in `tests/compat/README.md`;
  evidence in `evidence/compat-check.txt`, `compat-history.txt` and `seal-audit.txt`.

### 2. HOST-0: v0's baseline, then a second host
- **Entails:** `tests/host_compare.py` and a baseline recorded here, holding for each corpus program the receipt core's
  sha256, the output's sha256 and the trace head, plus the vectors' sha256 and the self-test's summary. Predictions are
  frozen before the run, with the risks named: correctly rounded square root, contraction off, the NaN-fold hazard, and
  flush-to-zero, which no runtime checks (DOCTRINE T5). The owner runs it on Linux x86-64 and on ARM64.
- **Theorem:** an attempt to falsify T5 off this host, where it is NOT_MEASURED. Run before RUN-1, it decides the
  numeric and ordering seals rather than confirming them later (the owner's reshuffle).
- **Anchor:** recovery. A recording replays elsewhere, which lockstep play needs.
- **Falsifier:** any differing receipt core, output byte or vector. Control: on ARM, the FMA row's naive C loop must
  still diverge.
- **Cost:** hours, and a second machine (the owner's).

### 3. The owner's rulings for RUN-1 (no code)
- Is a world property part of the law, of its inputs, or a data section sealed apart? This is the skeptic's question.
- RUN-1's spellings and headers (`orlog-law 1`, `orlog-trace-1`, `orlog-receipt 1`).
- Inputs exact-or-refused (the conversion rule) or rounded-and-noted (the literal rule).
- A refusal ends a branch, so a refuted claim is never rolled back.
- A twin round before the backends follow.
- **The input log's channel.** Replayable observations are not admissible ones (DOCTRINE T12, limit 4). Is a log the
  testimony of whoever supplied it, ratifiable like any other channel and never grounding by itself?
- *Written up 2026-10-26, at the owner's word ("run-1 ruling sheet next"):* `research/run-1/RULINGS.md`, twelve
  rulings and ten defaults, each spelling measured against v0 and COMPAT-0's frozen texts
  (`research/run-1/probe-spellings.txt`).

### 4. RUN-1: the open run
- **Entails:**
  - Declared ports, read-only, and one tick block. Each tick is an event 'T', then one 'N' per port in declaration
    order, then the body.
  - An input log, `orlog-inputs 0`, of typed encodings only, written once by a Python input door, so no runtime ever
    parses decimal text.
  - Receipt 1 with ticks, the input log's sha256 and an output chained per tick.
  - A per-tick budget written in the law. An overrun is a refusal event in the trace, which the law said; the host's
    stop stays a separate, verdict-free outcome.
  - In two commits: 1a, the reference and the specification with COMPAT-0 green; 1b, the backends.
  - 1b also carries the skeptic's *build identity by the law*: the text seal is passed in at run time, so a note edit
    stops rebuilding. That folds two runtime-contract revisions into one.
- **Theorems:**
  - *Replay:* every outside value is an event before it is read, so a run is a function of the law and the log.
  - *Alignment:* inputs are addressed by (tick, port), never by the order a law pulls them, so an edited law re-runs
    over an old log tick for tick.
  - *Tick termination:* every loop is bounded and there is no recursion.
  - *Capability:* a law reads only the ports it declares.
- **Anchor:** all four, and all five uses.
- **Falsifier:**
  - COMPAT-0 stays green.
  - A recorded 1,000-tick log gives byte-identical receipt 1 on all four executions.
  - Each plant must be caught: a dropped 'N' event, a backend that parses decimal input, a misaligned log entry.
- **Cost:** the largest early step. **Not yet:** pull-style input, clock and file ports, modules.

### 5. LEDGER-1: the world's ledger, before the first real ratification
- **Entails:** `orlog-ledger 1`. Each line links to the previous line's sha256. One writer holds an OS lock, writes a
  whole line and then fsyncs. A torn last line is quarantined and recorded. The ledger lives in the world's folder.
  Only console acts write it.
- **Theorem:** tamper evidence by accident, not authentication (the same honest bound as the line check). After a
  crash the ledger is as it was, or has one more whole line. Its fail-closed reading was done in this round.
- **Anchor:** recovery and earned admission. It pays twice: an audit trail, and the spine of replay.
- **Falsifier:** a reordered line, a deleted middle line and a truncated last line each end in LEDGER-BROKEN or
  quarantine, never a traceback.
- **Cost:** low. Now is the right time: no ledger file exists yet, so the format can change at no migration cost.

### 6. SNAP-1: snapshot, restore and branches
- **Entails:** `orlog-snapshot 0`, canonical bytes at a tick boundary, with restore in the reference and all three
  runtimes. A session is an append-only tree, and a refused branch stays in it.
- **Theorem:** complete-state continuation. Restoring S_n and replaying from tick n+1 reproduces every later head. The
  lineage's F-SNAP failure (a snapshot that aliased live lists) makes snapshots bytes, never object graphs.
- **Anchor:** recovery and exploration. It pays twice: the owner's rollback netcode and desync search, and an audit.
- **Falsifier:** restore at every k-th tick gives identical heads four ways. Plants: a snapshot that forgets the claim
  accumulators, one that forgets the cost counters, one that aliases a list.

### 7. SESSION-0 with two speeds
- **Entails:** an in-process session API over the reference (`open`, `step`, `snapshot`, `restore`, `fork`, `view`,
  `explain`, `arbitrate`), with a budget of counted operations on every call. A preview holds nothing; admission is
  arbitrated. A reference-only mode on the command line is its first, smallest piece and can land at once: today
  `--backends reference` raises.
- **Design:** the de Bruijn criterion. The session is plumbing over the authority. A session gives the same receipt as
  a batch run, and two sessions share no state.
- **Anchor:** exploration, at milliseconds per step.
- **Falsifier:** two sessions interleaved tick by tick give each one's receipts alone; a module-level cache planted
  between them must be caught.

### 8. RPC-0: the test socket
- **Entails:** JSON-RPC 2.0 on stdin and stdout, one object per line. `initialize` returns a version and the method
  table, frozen per version. Laws travel as base64, so the door sees raw bytes; port values travel as strings. A
  refusal is a result, not a transport error. No method writes the ledger.
- **Design:** a deterministic server is a function from a request transcript to a response transcript, so golden
  transcripts are byte-exact conformance tests.
- **Anchor:** exploration, explainability and earned admission. It is the "sockets and tools for testing" in the
  question, and every agent that proposes edits speaks through it.
- **Falsifier:** each plant must be caught: a law decoded as text before the door, an i64 sent as a JSON number, a
  `ratify` method, a timestamp in a response, a refusal sent as an error.

### 9. EDIT-0a: whole-text history and base binding
- **Entails:** an append-only history of text seals with the texts they name. A submitted edit names its base text
  seal and is refused when the head has moved (compare-and-swap). Undo admits an earlier text.
- **Design:** exact by construction. The whole text is the state, and the content-addressed cache makes undo a hit.
  Verðandi's lesson stands: a stale head is refused, never merged.
- **Anchor:** recovery and earned admission.
- **Falsifier:** undo reproduces the earlier receipt byte for byte; an edit on a moved head is refused.
- **EDIT-0b**, an edit language with exact inverses, waits for a churn measurement over the corpus showing whole texts
  do not suffice. Its exact-inverse problem was expensive in Verðandi.

### 10. Effect isolation and total order, as rules
- **Entails:** a run writes only its declared channels. When modules arrive, a subsystem touches only its declared
  state regions. Every collection the language ever gains iterates in an order the law defines and shows.
- **Theorem:** isolated transitions are race-free, so disjoint bodies can step concurrently with identical results (the
  owner's argument). Today the only collection is the list, which is ordered, and the compiler's output is identical
  under two hash seeds.
- **Falsifier:** a row with every new collection, and a plant that iterates in hash order.

### 11–15. Later
- **11. PERF-0 and a build policy.** A faster checked path for the reference (the generated Python backend in process,
  or a closure compiler held as a fifth execution). Then c99 and Rust built in parallel, and an optimization level
  chosen for large laws, since -O2 is superlinear.
- **12. MODULES-0.** Imports pinned by the full seal, and parameters passed by value; still no recursion.
- **13. EMBED-1.** Re-entrant compiled runtimes, so that a native game host can embed a run. It reopens C memory
  safety.
- **14. NUMERIC-2,** reframed as the owner asked: a sealed numeric dialect first, with rounding, saturation and overflow
  specified and its vectors partly hand-written; big integers and rationals second.
- **15. A TCP adapter** over RPC-0, only for a remote client and with the owner's word. A listener reachable from
  another machine is distribution.

**Quick, blocking nothing:**
- the reference-only mode;
- probing the toolchains once per worker, not once per artifact (130 ms each time);
- the stale comment in `orlog_rt.h`, with the header's next change;
- the second-round court record;
- whether examples/fall.orl joins the twin's inputs.

**Not a rung: Ragnarök.** The counterworld search is an instrument for prosecutions, not a court or a language feature.
Its verdict is `research/ragnarok/VERDICT.md`.

## 4. Act: what this round did

Each item is MEASURED here, 2026-10-25, with its evidence:
- **The arbiter is pure of ambient files.** One run folder per arbitration, removed after it. 48 arbitrations of two
  programs at once in one folder, three times: all agreed, no folder left (`evidence/race-after.txt`). The self-test
  holds a race of 16 and a plant that shares the folder.
- **Runs are bounded.** The reference runs under a budget of counted operations: a loop of 10^9 is STOPPED-BY-HOST at
  operation 100,002 of a budget of 100,000, the same on both runs, with no receipt and no refusal. The backends run
  under a wall clock, labelled host-dependent.
- **Failure is deterministic.** A torn ledger reads LEDGER-BROKEN at its line (row and plant). A backend that did not
  build is counted neither agreeing nor dissenting, and every claim reads INCOMPLETE.
- **The arithmetic is checked beyond its generator.** `tests/vectors_independent.py` derives 20,006 of the 20,015
  vectors again without importing the reference: 0 differ. 113 hand-worked cases and two published digests agree, and
  five plants are caught, three of them mistakes the reference and its vectors would share
  (`evidence/vectors-independent.txt`). Its first run caught one plant by the derivation alone, because no hand case
  routed a non-canonical NaN through the canonicalization. Three cases were added.
- **Agreement is tested as a claim.** Rows for the lowering plant (REFERENCE-DISSENT, 41 operations more) and the
  front-end plant: a monitored negative, which passes while the defect slips past all four executions.
- **The documents** (§5), and **the self-test:** 161/161 twice, byte-identical, and 151/151 with Python alone.

These are the owner's "bounded execution" and the skeptic's "isolate runs" done now. His other three measures that pay
twice are SNAP-1, LEDGER-1 and EDIT-0 (event-sourced state), rule 10 (effect isolation, total order) and HOST-0 with
NUMERIC-2 (defined numerics).

## 5. The documentation prosecutor's findings: dispositions

Each finding was checked against the code before its document changed.

| finding | disposition |
|---|---|
| F1 | **Applied.** chaos.orl's notes corrected; the law seal is unchanged; the twin's inputs regenerated (chaos and leapfrog only) |
| F2 | **Applied, code.** A failed build or missing compiler is `build_failed`, outside dissent and agreement; INCOMPLETE; SPEC §12 notes the change |
| F3 | **Applied, code.** `orl.py court` takes `--backends`; README corrected |
| F4 | **Applied.** README and DOCTRINE: 221 seeds and 20,000 mutants; 47 of 48, the 48th a timeout identical without a limit |
| F5 | **Applied.** SPEC §14: seed 1 cannot be reproduced by today's tool. AGENTS: the signatures to expect (`evidence/difftwin-n3000-seed1.txt`: 10 disagreements, all three settled readings) |
| F6 | **Applied.** E18 (with a plant) and E22 rows; RECORD.md notes the finding, to be entered against ed2-IMPL in the second round's record |
| F7 | **Applied.** "Where a guard could pass by accident" in README and AGENTS |
| F8 | **Applied.** "Written from the specification, importing numeric_ref.py and seal.py" in DOCTRINE, SPEC §11, RECORD.md, ADMISSION.md and AGENTS |
| F9 | **Applied.** §14 in every precedence list |
| F10 | **Applied.** SPEC §14 item 7 defines the tree; `syntax.py` named as the implementation |
| F11 | **Applied.** RUNTIME-SPEC §4a, ownership |
| F12 | **Applied.** DOCTRINE: counts typed beside their evidence |
| F13 | **Applied.** DOCTRINE: "diverges", and 0 FMA for chaos.orl alone |
| F14 | **Applied.** README: measured on two programs; flat in general DECLARED |
| F15 | **Applied.** `tests/e21_list_leak.py` tracked; rt_c/NOTES.md corrected in place; `evidence/e21-lists-rerun.txt` |
| F16 | **Applied.** ADMISSION.md: the court's narrowed "not found" |
| F17 | **Applied.** The 24-deep four-way row; RECORD.md and DOCTRINE noted |
| F18 | **Applied.** DOCTRINE §9: fork 2 decided; §14's readings added to fork 7 |
| F19 | **Applied.** E1–E26; §10 a pointer |
| F20 | **Applied.** `evidence/rt_rs-vectors-O.txt`, `-O0.txt`; "separately written (one model family)" |
| F21 | **Applied.** `evidence/rt_c-vectors-O0.txt` |
| F22 | **Applied.** DOCTRINE and RECORD.md: L16's scripts are not in the repository |
| F23 | **Applied.** SPEC §14: §13's run OBSERVED in scratch, not reproducible |
| F24 | **Applied.** `evidence/doorfuzz-60000-5.txt` |
| F25 | **Applied.** `evidence/corpus-seals.txt`: 11 of 11 under 83eb044 and fc19339 |
| F26 | **Applied.** 155 marked OBSERVED; 124 recorded (`evidence/probes3-first-run.txt`) |
| F27 | **Applied.** SPEC §10 and canon.py: retraction DECLARED; the hyphen and apostrophe repairs listed |
| F28 | **Applied.** SPEC §13 and DOCTRINE: INTERNAL is a defect, not a verdict |
| F29–F32 | **Applied.** RUNTIME-SPEC: exit statuses, `<float.h>` first, `args_os`, four heads |
| F33–F36 | **Applied** as dated notes in rt_c/NOTES.md (the author's record is not rewritten); `x.sh` pointed at the repository |
| F37, F38 | **Applied.** AGENTS and README: separate authors of one model family; rt_rs/NOTES.md dated notes |
| F39–F41 | **Applied.** AGENTS: the evidence list, each round's `settled.json`, commands from the root with a chain folder, SPECULATIVE among the grades; README's grade line |
| F42 | **Open, for the owner.** 16 tracked files under `court/` embed the home folder's path: the logic prosecution's header and 15 captured observations. They are records kept as captured, and redacting them rewrites a record. No new file adds one: the debate records here give such paths relative to the repository. *Ruled 2026-10-26: his words, "Scrub the home paths from all 16 `court/` records in the held push, but preserve the evidence and provenance of F42." The current files hold `{session}` and `{python}` in place of the paths: 4,068 lines in the 16 files, nothing else changed. The paths remain in history through commit 95dac79, which is the finding's evidence. Whether to rewrite history is a separate decision, so F42 stays open for history.* |
| F43–F46 | **Applied.** AGENTS' door sentence narrowed; edition lines agree; STATUS rewritten for this round; the capture's CR LF stated |
| F47–F53 | **Applied.** README: receipts without their backend line, the twin's three rounds, the cycle named when the claim lies on one, "Ørlǫg does not solve the paradox", "parts of the specification", the lineage; ADMISSION's folders |
| F54 | **Applied.** leapfrog.orl's note: Newton's third law, not Noether; the law seal is unchanged |
| F55–F57 | **Applied.** The self-test's usage line, the one-backend witness and the FMA row's text |

The prosecutor's "known open items": DOCTRINE §5's twin line and defect table are updated; the court record's second
round stays open (STATUS.md).
