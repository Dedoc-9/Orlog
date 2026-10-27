# The held push: the decisions left, on one sheet (2026-10-27)

His word on the push: *"Wait for the amended set and R7. Do not push the four commits yet."* And under R7: *"no push
before the final gate, and no §15 clause built before the required review."* R7 is ruled. This sheet lists every
decision still between the five held commits and the gate, with a recommendation and what each choice costs. Nothing
here is ruled until he rules it, in his words.

## 1. The release's scope

*Ruled 2026-10-27 (`RULINGS.md`, "The release"): the narrow scope, N.*

The push holds research records, probes and evidence only. Nothing in `src/` or `tests/` changes, and nothing is
built. Two scopes are possible:

| scope | what is decided before the push | cost |
|---|---|---|
| **N, narrow (recommended)** | finding 6; each remaining row of the amended set given its disposition, most of them deferred to a ruling before 1a's build; finding 8 deferred with its packet, or ruled if he wants it now; the format freeze deferred to P6's trigger; the `.gitattributes` line | about three turns: rulings, one batched re-read, the gate |
| **F, full** | every row of the amended set and finding 8 ruled as written | each adopted row makes its clauses ruled, so the draft changes widely, with a re-read of each ruling's affected clauses: several more turns |

Why N is safe. R7 makes the re-reads a condition of building, not of pushing. Every open clause stays tagged open in
the pushed draft, and every deferral is recorded with the packet or row that will decide it. A deferred row decides
nothing by being deferred.

## 2. Finding 6: read-once ports

**Ruled 2026-10-27: A′, as RO′-1 to RO′-6, with six conditions (`RULINGS.md`, "Finding 6: read-once ports").** What follows is the record he ruled on.

The adversarial comparison he asked for is `packets/F-read-once-adversary.md`, saved unchanged except for two masked
paths. Its measured results were checked against its own outputs. Its verdict:

- **A fails R6's adopted sentence**, "a prefix claim's whole claim line is fixed by the law". Two logs of one law that
  both load give a licensed claim n of n evaluations, or 0 of 0 when the read-once value is missing. A stands only if
  R6's sentence is amended, or if A's NOT-RUN gives the court no claim line at all, which would be a new kind of
  outcome.
- **A′ survives the whole-log attack.** Checking the whole log first fixes when the log is checked, not which logs are
  well formed. A missing read-once record shows in the log's bytes, so the loader tells it from a malformed log before
  any statement runs. The report lists exactly which logs load.
- **CUT-0's row holds in computation**, MEASURED on version-0 stand-ins, with its plants caught. As first worded it was
  short of four things: a cut at a stop that is not a refusal; the open log with no read-once record (its N1); the old
  NOT-RUN and LOG-OPEN row limited to logs that have the record; and CUT-0's own reach following the tick block's
  body. Its wording RO′-6 holds all four.
- **A′ stops at the first read-once declaration**, even when the missing value is a later port's (its case 4b).

**Recommended: A′, in the report's wording RO′-1 to RO′-6** (§6), every byte form left open, with what it must not
decide. RO′-6 is a pinned change to CUT-0, possible while no digest is pinned.

**Left open beside it, for the amended set's A2 row** (deferred under scope N):
- N3: when the host runs the statements before the first read-once declaration. Two hosts that choose differently give
  one law and one set of arrivals two log hashes.
- N2: an `end()` before the read-once record closes.

**Passed to finding 8:** a form that loads for a header-only open log and for a log ending in a read-once NOT-RUN, with
packet D's LOG-END wording limited to tick NOT-RUNs. As worded today, no log ending in a read-once NOT-RUN loads in
either design (MEASURED in the session model).

**What A′ costs:** CUT-0 gains a cut at a stop that is not a refusal, and T10.1's argument reaches it only while binding
has no other effect (DECLARED until version 1 runs). Output may precede the read-once values: a host shows the scene
before its seed arrives.

## 3. Finding 8: load refusals

*Ruled 2026-10-27 (`RULINGS.md`, "The release"): deferred, under the narrow scope, with packet D and finding 6's condition 5.*

Packet D (`packets/D-LOG-refusals.md` §4) recommends:
1. load whole, after the law compiles and before any statement runs;
2. the nine LOG-* codes with the conditions worded there;
3. the model's order, sub-choices (a) to (e) open;
4. **(W)**: no receipt for a refused log, the witness records the code, line and message, exit 1, no court reading;
5. the end record's t = n+1 for each-tick ports only;
6. no read-once line when the law declares no read-once port.

Its parts on read-once ports depend on finding 6 (packet D §4, "Where read-once ports unavoidably touch the grammar").
One question rides on it: is the provenance line owed per court reading or per log offered (`packets/INTEGRATION.md`,
I-7)?

**Recommended for scope N:** defer finding 8 to the amended set's "identity and bytes" row, ruled before the build,
with packet D as its record. Ruling it now adds its own set of re-reads (§15.5 whole, §15.4, §15.7.5, §15.8, §15.11).

## 4. The amended set's remaining rows

*Ruled 2026-10-27 (`RULINGS.md`, "The release"): each row deferred as the table below gives it, under the narrow scope.*

Each row's proposal is in `ROUNDS.md`, "The amended set". The claims and PREFIX rows are ruled.

| row | kind | what it would fix | needed by this push? | recommended disposition |
|---|---|---|---|---|
| A2 | N | judge before assigning; every arrival in the history; a whole log checked before execution | no | defer to a ruling before the build; its read-once part follows finding 6 |
| budget | N | N = 0 or 1…2^62; the (N+1)-th operation counted, then refused | no | defer, with sheet R9 (a budget per tick), before 1b |
| port place | N | (b): ports at top level; a read outside the tick block refused at compile time | no | defer, with sheet R2 (the spellings) |
| session record | N | its own chained record; END-PENDING, END-UNDISPOSED, RUN-REFUSED | no | defer to a ruling before the build |
| binding | N | three records, three authorities | no | defer to a ruling before the build |
| identity and bytes | N | the port signature, the log's lines, `'T'`'s and `'N'`'s bytes, the statuses | no | defer, with finding 8 |
| counting | N | `'T'` cumulative; the tick block counts nothing | no | defer to a ruling before the build |
| H2 | N, then I | the door reads `Note:` and `Title:` at column one | no | defer: already "in a change of its own" |
| codes | I | the refusal-code registry and its row | no | defer: an implementation requirement for 1a |
| gate rows | I | the resumption oracle and the log congruence as 1a rows | no | defer: an implementation requirement for 1a |
| HOST-0 | N | its own rung, on a second machine | no | defer: HOST-0 is its own rung |
| F1–F9 | N | `FLOAT.md`'s float decisions | no | defer, with sheet R8 (float ports), before 1b |
| reporting | N | the authority rule; "grounded over claims" forbidden | no | defer to a ruling before the build |

## 5. The format freeze

*Ruled 2026-10-27 (`RULINGS.md`, "The release"): deferred to P6's trigger, under the narrow scope.*

Recommended since 2026-10-26 (`ROUNDS.md`, the held push): defer to `CUT-SCHEMA.md` P6's trigger, before the first
version-1 receipt is frozen anywhere. The version-1 frames are not yet derived, so a freeze now would fix a format not
yet written.

## 6. The seven first-form adversary outputs

*Ruled 2026-10-27 (`RULINGS.md`, "The release"): kept byte for byte as captured, by `-text` on their seven exact paths only; the current reruns stay normalized. Checked by staging into a temporary index: every byte kept, the reruns normalized, and the same bytes at a normalized path hash differently.*

`research/run-1/manifold/adversary/` holds seven outputs captured with mixed line ends (MEASURED by bytes,
`packets/INTEGRATION.md` §3). Under `* text=auto eol=lf`, git would store them with LF. **Recommended:** add one line to
`.gitattributes`, `research/run-1/manifold/adversary/*.txt -text`, in commit 2, so they are kept as captured, as the
file already keeps recorded runs. The six current reruns are LF either way.

## 7. The gate on the exact tree

Run after every decision and edit, on the tree that will be committed, with nothing edited after it starts:
1. **The tree's identity.** With a temporary index (`GIT_INDEX_FILE`), add every pending file and take `git write-tree`.
   His own index is untouched. After the five commits, `HEAD^{tree}` must equal it; the last commit message can carry
   it as a `Gated-Tree:` line.
2. **COMPAT-0:** `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B tests/compat.py check --jobs 8`. Expect `COMPAT-0 HELD`, same
   3361, 0 newly accepted, 0 settled, 0 skipped, 0 differ, 0 input changed.
3. **The self-test:** `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B tests/selftest.py`. Expect `ORLOG SELFTEST 210/210`.
4. **The probes:** each of `PROBES.md`'s eight, compared with its evidence file, headers aside, byte for byte.
5. **The adversary's current reruns:** the six `*-current.txt` and `s_drop`, compared the same way. The "seconds
   printed" are masked by one pattern, written before the run.
6. **The manifold:** `fibers.py` and `resume_oracle.py` compared; `fibers-timing.txt` and `resume_oracle-search.txt`
   are excluded and said so (a timing; a search run once). `make_laws.py` is run in a scratch copy, never over the
   committed `laws/`, and its output compared with them.
7. **The records' own tools:** `clause_diff.py` reproduces each `DRAFT-n-CHANGES.md`, and `ar_compute.py` (with no
   argument, 2 and 3) reproduces each `AR-*.md`.
8. **Privacy and size:** no private string in any pending file; the largest file under 50 MB.
9. **The record.** The gate's output stays outside the tree: in the session's scratch and in the last commit's
   message, never in a file of the gated tree.

Any difference stops the push until it is explained, and then either repaired with the gate run again or labelled.
