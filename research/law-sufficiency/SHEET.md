# LAW-SUFFICIENCY-0: is the sealed law enough to run? An experiment sheet (2026-10-30)

**Status.** An experiment plan, nothing more. It is not an adopted ruling, and it authorizes no implementation: no
script it names is written until the owner accepts this sheet. It changes no released semantics and adds no
dependency. It is off the gate, and it does not touch version 1's critical path: draft 14, the version-1 reference,
the containment test, the CUT-0 pin, then 1a. It starts from commit `2e9805aaa1ceeae0beb443d527680796b66f39c7` (the
push of release 2, tree `2fbac135…`).

**The question.** The law seal is the sha256 of the law bytes (`src/orlog/front.py:27-28`), which `law_bytes(prog, an)`
writes (`src/orlog/sema.py:600`): `orlog-law 0`, the decimals line, then one `(clause id parent stmt)` line per clause.
But the reference runs the parsed program and its analysis, not those bytes: `Interp(prog, an, law_hex, text_hex)`
(`src/orlog/interp.py:85`). Does everything the run reads come from the sealed bytes? If it does, the law bytes can
be the boundary between the prose front end and any core, a Rust one included. If it does not, this sheet should
name exactly what is missing before anyone builds a second runtime on the wrong boundary.

## 1. Scope and starting point

- **What is tested.** Version 0's reference interpreter (`src/orlog/interp.py`) on version 0's law bytes.
- **What is not tested.** The generated backends (`lower.py`, `gen_py.py`, `gen_c.py` and the runtimes) also read
  `prog` and `an`. Their read sets are reported by test 1 but decide nothing here. Version 1's law forms (ports, the
  tick block) do not exist in the law bytes yet; §15 must define them before the pin, and this sheet does not.
- **What the code already shows (read here, DECLARED until test 1 traces it).** The run reads these, and none is
  written as such in the law bytes:

  | read by the run | made by the analysis | in the law bytes as |
  |---|---|---|
  | `s.elem` (a Change's numeric type, `interp.py:180`) | `sema.py:155` | not written; the variable's type and the index's presence would give it |
  | `c.cost_tracked` (a clause whose cost a claim reads, `interp.py:136`) | `sema.py:219` | not written; the claim's `(certificate N …)` names the clause |
  | `c.children` (a block's, an arm's or a procedure's clauses, `interp.py:145, 228, 238, 244`) | the parser | each clause's parent id |
  | `s.var.type` (a list's element type, for an event's encoding) | the analysis | not written; the `let` expression's types would give it |
  | `an.rules[name]` (a rule's clauses, `interp.py:425`) | `sema.py:75` | the `(define name …)` lines, in clause order |
  | `an.overrides[name]` (who beats whom, transitively closed, `interp.py:426`) | `sema.py:478-493` | each define's `(over id …)`; the closure is not written |
  | `an.claims` (the claim sites in order, `interp.py:130`) | `sema.py:212-213` | each `(claim id …)` |

  The text seal enters only the receipt's `text-seal` line (`interp.py:73-74, 128`). The trace head starts from the
  law seal (`interp.py:91`), and a `(seal)` expression reads the law seal's words (`interp.py:97`).

- **What the run produces.** The receipt (`interp.py:73-82`): `orlog-receipt 0`, `backend`, `law-seal`, `text-seal`,
  `status`, `output-bytes`, `output-sha256`, `events`, `trace-head`, `ops`, `claims`, one line per claim, `end`.

## 2. The three tests

**The projection, fixed before any comparison.** `P(receipt)` is the reference's receipt with two lines removed:
`backend` (which execution made it) and `text-seal` (which spelling it came from). Every other line is execution:
status, output length and sha256, event count, trace head (which commits to every event), operations, and each
claim's line. COMPAT-0's receipt core (`tests/compat.py:57`) drops `backend` only, so it is not this projection.
`P` is not widened or narrowed after a mismatch; a change to `P` is a new version of this sheet, made before its run.

**Runs are alike.** Every run uses the reference, the same budgets as COMPAT-0 (corpus 10,000,000 operations, the
rest 1,000,000), `PYTHONHASHSEED=0`, and no input: version 0 has none.

### Test 1: the read set against the sealed set

- **Method.** A recording wrapper over every node of `prog` and over `an` logs each attribute read, as (class,
  attribute). It logs two sets on every accepted text: `R_run`, what `Interp` reads, and `R_seal`, what
  `law_bytes(prog, an)` reads. Each pair in `R_run − R_seal` is a candidate, classified as one of:
  - **derivable**, with its derivation from sealed fields written out (for example, `elem` from the variable's type
    and whether an index is present);
  - **not derivable**: no function of the law bytes gives it.
  
  The static table in section 1 is checked against the trace: a pair it lists that the trace never sees, or a pair the
  trace sees that it does not list, is reported as such.
- **Sets.** The 300 frozen texts that have a law (13 corpus, 42 fixture, 158 mutant, 87 probe, from
  `tests/compat/baseline-v0.jsonl`), and `examples/`.
- **Falsifier.** A candidate that is not derivable, and whose perturbation, with the law bytes held fixed, changes
  `P(receipt)` on some text.

### Test 2: equal seal, equal behaviour

- **Method.** Group texts by law seal, run each, and compare `P(receipt)` within each group.
- **Sets.**
  - (a) The frozen texts: 173 distinct laws, of which 67 have two or more distinct texts, 184 texts in all (counted
    from the baseline, 2026-10-30).
  - (b) Generated variants of each of the 300 texts: each of the door's repairs applied (CR LF, a BOM, NBSP, curly
    quotes, ×, −, a non-NFC form) and a `Note:` line added. A variant is kept only if its law seal equals its
    source's; one whose seal moves is counted and reported, not compared.
  - (c) The three spellings in `examples/spellings/`.
- **Falsifier.** Two texts with one law seal and different `P(receipt)`.

### Test 3: an independent decoder

- **Method.** A decoder `D` reads the law bytes and nothing else, and builds the `prog′` and `an′` that `Interp`
  runs. It derives every field of section 1's table itself, from the bytes. It is written from the law grammar
  (`sema.py:513-597`, read as a specification) and must not call `parse_program`, `Analysis` or the `law_*`
  writers to build. It may construct `syntax.py`'s node classes, because `Interp` dispatches on them. That shared data
  type is a dependency the test does not attack, and it is said so.
- **Checks, on every accepted text.**
  - `P(Interp(prog′, an′))` equals `P(Interp(prog, an))`.
  - `law_bytes(prog′, an′)` equals the law bytes `D` read: the round trip, with the writer used only to check.
- **Sets.** As test 1.
- **Falsifier.** `D` cannot build a runnable law without information outside the bytes, or its run's `P` differs
  from the parsed run's.

## 3. Planted defects and falsifiers

Each test must refuse a defect planted in what it checks, or it shows nothing. Each plant is made in memory, never in
`src/`. Its expected verdict is written before it runs. A plant whose target the run does not reach on a given text
is an equivalent mutant there. It is measured and declared, never assumed.

| test | plant | expected |
|---|---|---|
| 1 | `Interp` made to read an unsealed field (a clause's source line) | the recorder lists it in `R_run − R_seal`, as not derivable |
| 1 | the recorder made to drop one class's reads | the static table's check reports the missing pair |
| 2 | `Interp` made to fold the text seal into its output | test 2 fails on the groups with two or more texts |
| 2 | `P` made to keep `text-seal` | test 2 fails on every group with two or more texts (shows `P` is the projection that matters) |
| 3 | an override edge removed from the parsed path's `an.overrides`, the law bytes fixed | the parsed `P` changes on a text whose rule the edge decides; the decoded `P` does not |
| 3 | a claim site dropped from the parsed path's `an.claims` | the parsed `P` changes (the claim lines); the decoded `P` does not |
| 3 | `cost_tracked` flipped on a certificate's clause in the parsed path | the parsed `P` changes (the claim's cost); the decoded `P` does not |
| 3 | a Change's `elem` changed from `int` to `fix` in the parsed path | the parsed `P` changes, or the run refuses; the decoded `P` does not |
| 3 | `an.rules[name]` reversed in the parsed path | measured: the rule's value is chosen after a conflict check, so this may be equivalent on every text; declared if so |
| 3 | `D` made to derive `elem` wrongly | test 3 fails |
| 3 | `D` made to read one field from the parsed path | the independence check (`D`'s imports and its inputs) fails |

## 4. Outcomes and what each means for the architecture

| outcome | what it means | what follows |
|---|---|---|
| all three hold | on these sets, the law bytes determine the reference's run, given `D`'s derivations (MEASURED, not ESTABLISHED: finite sets) | the law bytes are the candidate boundary for an independent core: a Rust core reads them, not prose and not Python's analysis. `D`'s derivations become part of the format's meaning, written as obligations. `D` is the machine-form half of Lauburu |
| test 1 finds derivable gaps only | the boundary holds, but the core must re-derive those fields | each derivation is stated, and the Rust core's cost includes it. The derivations are a second reading of `sema.py` and need their own plants |
| test 1 finds a gap that is not derivable | the seal does not determine the run | a new law-bytes version (`orlog-law 1`) by the owner's ruling, with COMPAT-0's consequences; no Rust core on the current bytes |
| test 2 fails | two texts with one seal run differently: the strongest falsifier | a finding for the owner: the law seal is not an execution identity, and COMPAT-0's frozen pairs are read again |
| test 3 diverges with no test-1 gap | a defect in `D`, or a dependency the recorder cannot see (clause order, ids) | investigate `D` before concluding anything |

**What a positive result does not show.** That a Rust core is correct. That Float is identical across hosts (HOST-0).
The prose-printer side of LAU-1. Version 1's law forms. That the backends read only sealed fields. Anything beyond the
texts run: a sufficiency result on finite sets is MEASURED, and its derivations are checked only by behaviour on those
sets.

**What it would cost.** Three scripts in `research/law-sufficiency/` (the recorder, the variant generator, the
decoder) with their plants. Evidence lands in `evidence/` as `law-sufficiency-*.txt`, each with its command and tree,
run twice. No file of `src/`, `tests/` or `vectors/` changes.
