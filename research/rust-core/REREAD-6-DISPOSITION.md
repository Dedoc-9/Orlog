# REREAD-6: the dispositions of its findings (PROPOSED, 2026-10-30; adopted, below)

**Adopted (2026-10-30).** The owner adopted U1(a) and U2, the recurring-runner-fault rule included, and the remaining
minor dispositions *"as text, test, and evidence-record corrections, provided they preserve the existing language and
outcome semantics"* (recorded whole in [RULINGS.md](RULINGS.md)). His precisions:
- U1: *"a successful byte comparison alone does not prove that a writer ran"*. OUT comes from the writer, R7 gains the
  two writer plants, and the source review records OUT's provenance;
- U2: runner faults kept *"distinct from reference exceptions, core faults, and externally caused termination"*. The
  repeat rule is *"experimental procedure, not a new semantic outcome class"*.

They are applied in draft 7, the checker, the runner and SHEET.md's Amendment 6. The text below is kept as it was
proposed.

**Status.** Proposed, not adopted. These dispose of the 10 findings in [REREAD-6-REPORT.md](REREAD-6-REPORT.md), the
re-read of LAW-FORMAT-0 draft 6 (sha256 `c5435579…`), its checker (`3c3ad0b6…`), the reference runner (`33914074…`)
and its check (`e1edf642…`), and SHEET Amendment 5 (`fb505ccf…`). Nothing changes until the owner rules. He answers
ASK U1 and U2. Then:
- draft 7 applies every DRAFT item and his answers;
- the checker, `plant_reverts.py`, `ref_run.py` and `ref_run_paths.py` are amended to match;
- SHEET.md gains Amendment 6, and the records they fix are made again;
- a fresh independent re-read follows.

No core code is written before its findings are resolved. In his words: *"No Rust-core implementation,
production-source changes, gate or release changes, commit, or push is authorized. Phase 0 remains active."*

**What the re-read found holds** (MEASURED there; the claims below re-run here):
- **The gates' precedence (N1)** is stated unambiguously, is faithful to E1(b)'s adopted text and to his words, and is
  implemented exactly:
  - an independent phase 3, written from section 8's text, agrees with the checker on 80,000 fuzzed laws;
  - a control using draft 5's rule differs on 4,406 of 40,000, so the comparison has power;
  - the gates stay linear on 300,000-clause trees with several gates failing;
  - the plants pin N1 against draft 5's rule and all six sequential orders.
- **The write-back mode** is kept apart from output, receipts and traces, and runs nothing. Nothing reads it but R2,
  and R2 fails on a difference and on a load refusal.
- **N3's three readings** are stated, and consistent between the draft and the sheet. The narrow reading of a block
  is planted, and its plant bites. A result is defined for all ten classes, written back included. The six kinds are
  unchanged.
- **Every frozen file reproduces byte for byte,** a full 26-minute regeneration of `r6-reference-2.txt` included, and
  242 sampled mutants re-run twice through the runner give every row the same.
- **The budget positions hold:** 60 runs at every B, 0 mismatches.
- **Chains of 100,000 are accepted,** and appendix A reproduces through the reference.
- **Draft 6 broke none of the B1 requirements.**

**What it found wrong, by area:**

| | findings |
|---|---|
| R2's observation | **M1 (MAJOR)**: the write-back cannot tell a re-encoding from an echo of LAW, so the dropped-name gap N2 was meant to close is still unseen |
| the ruling's scope | **M2 (MAJOR)**: L2 and L3, both MAJOR, were applied under "the ten minor findings"; L3's and L5's runner faults change two adopted classifications; and treating a runner fault as an interrupt is the writer's extension, with no end for a fault that recurs |
| the checker | M3 (W5's naming of absorbed clauses inconsistent), M4 (N3's narrow reading pinned for blocks only), M10 (the 304 laws' write-back never compared, though printed) |
| the text | M5 (three write-back guesses), M6 (the adjudicator still lacks SPEC), M8 (the precedence's reason omits F1(b)'s text), M9 (records not kept current) |
| the runner's check | M7 (`ref_run_paths.py` holds the runner's endings, not its run conditions; decoder1 not held to its sha256) |

**The report's count is right:** 0 BLOCKER, 2 MAJOR (M1, M2), 8 MINOR (M3–M10), 10 in all. By re-read, the findings
have run 17 (F), 19 (G), 15 (H), 17 (J), 16 (K), 14 (L), 10 (M).

**Which findings are mine:**
- **M1:** I wrote the write-back as "the bytes it writes back from what it loaded" and did not say they may not come
  from the bytes read. For a canonical law, the two give the same OUT.
- **M2:**
  - I called "L2, L3 and L5–L14" the ten minor corrections, in RULINGS.md's introduction and in draft 6, lines 11,
    905 and 919. That is twelve items, and L2 and L3 are MAJOR.
  - The extension of his interrupt rule to runner faults is mine (RULINGS.md, "As kept").
- **M3, M4:** my structure gate registers a W4 chain's first arm, and a sound chain's not. And I planted the narrow
  reading for blocks only.
- **M5:** the write-back row's *"(or `stack`, if a stack the load uses fails)"* is my invention; no load stack is
  defined.
- **M10:** the checker has printed *"written back exactly"* since draft 0 without comparing `write()` with the bytes.
  W1–W3 imply it by construction, but the line claims a measurement it did not make. That is a fifth claim of mine
  refuted.
- **M6–M9:** wording and records of mine.

**How each finding was checked.** Each concrete claim was run again here, read-only (scratch `rr6_check.py`):
- through `format_check.read`;
- through the checker run whole with `write()` broken in memory;
- through two copies of the runner held outside the repository, each checked by `ref_run_paths.py`.

| | severity | finding | re-run here | disposition |
|---|---|---|---|---|
| M1 | MAJOR | R2 cannot tell a write-back from an echo of LAW | **CONFIRMED** by reasoning, NOT MEASURED (no core). Every law that passes section 8 is canonical, so a writer and an echo give the same OUT, and R2b's twins never reach OUT | **ASK U1** |
| M2 | MAJOR | L2 and L3 applied under "the ten minor findings"; L3 and L5 reclassify two cases; runner faults as interrupts is the writer's; a recurring fault has no end | **CONFIRMED.** REREAD-5-DISPOSITION.md marks L2 and L3 MAJOR. `ref_run_paths.py` classes a text the front end refuses and a budget of −1 RUNNER-FAULT, where Amendment 4's runner gave NO-REFERENCE-RESULT and RESULT | **ASK U2**. And **DRAFT**: the miscount is corrected in place in RULINGS.md, with a note, and in draft 7 |
| M3 | MINOR | W5's naming of absorbed clauses differs between a sound chain and a W4 chain | **CONFIRMED.** A first arm naming absorbed clause 2: sound chain W5 line 4 ("in no If chain"); with an else naming 99, W4 line 5 (the first arm counted) | **DRAFT:** the row's own words, *"named by exactly one arm or else of exactly one such If"*, read as written: every arm or else whose ⟨C⟩ is an absorbed clause names it, in a sound chain and in a W4 chain alike. A first arm that names one fails the chain's shape at the If's line. The checker made consistent; P1, P2 and the later-arm case planted; the R6 checker record made again (the report counts 61 verdicts moving, all swap mutants) |
| M4 | MINOR | N3's narrow reading pinned for blocks only | **CONFIRMED.** An inline if's else naming absorbed clause 2 gives W5 line 4 | **DRAFT:** planted, and undone in `plant_reverts.py` (inline ifs' arms and else allowed to name) |
| M5 | MINOR | three write-back guesses: the kind of a load failure, `--` positionals, the CORE-FAULT example | **CONFIRMED** by the text (draft 6 :684 against :738; :671 against :728; SHEET :202 against :580-581) | **DRAFT:** every allocation while reading or loading LAW reports `law`, in both modes (the invented `stack` removed). A positional beginning with `--` is a usage error in both modes, `--write-back` in first place excepted. Amendment 6 says a write-back run's files are judged against the written-back row, and that row's end is no CORE-FAULT |
| M6 | MINOR | the adjudicator lacks SPEC, on which W9, the promote rule and section 7's order rest | **CONFIRMED** by the text | **DRAFT** (Amendment 6): the adjudicator gets the core author's whole reading set, by sha256: the draft, SPEC.md, RUNTIME-SPEC.md and both vector files |
| M7 | MINOR | `ref_run_paths.py` holds the runner's endings, not its run conditions; decoder1 not held to its sha256 | **CONFIRMED.** With the ENV line removed, and with `sys.setrecursionlimit(100000)` added, the copies pass, 25 of 25. `ref_run.py` holds no sha256 of decoder1 | **DRAFT:** the runner holds decoder1.py to its pinned sha256 before importing it; a mismatch or an import failure is a RUNNER-FAULT. `ref_run_paths.py` requires the ENV line's fields: the recursion limit equal to a fresh interpreter's default, and `format_check not-imported`. It also checks one run's P against P computed in its own process, and scans the runner's source for no environment read, no recursion limit and no `format_check`. Each a case |
| M8 | MINOR | the precedence's reason omits F1(b)'s option text | **CONFIRMED** (REREAD-4-DISPOSITION.md:117: *"a third gate, after the depth gate and the chain gate"*) | **DRAFT:** the reason cites F1(b)'s text, his F1 words that left the order *"deliberately unsettled"*, and N1, which decided it. The rule is unchanged |
| M9 | MINOR | records not current | **CONFIRMED:** SHEET :525 (*"changes no class"*, no note); SHEET :476 names draft 5's R2b checker record; `r6-reference-2.txt`'s first line names Amendment 4; draft 6 :865 gives no draft-6 expectation; REREAD-5-DISPOSITION.md's L1 row promised draft 5 a correction that the keep-drafts rule forbids | **DRAFT:** an in-place note at SHEET :525. Amendment 6 names `evidence/rust-core-r2b-checker-6.txt`. The generator's header names Amendments 4 and 5, and the record is made again (rows unchanged: a prediction). Draft 7's line is corrected. REREAD-5-DISPOSITION.md gains a note: draft 5 stays as it was, and its correction is draft 6's section 8 |
| M10 | MINOR | "written back exactly: 304 of 304" counts passes, not write-backs | **CONFIRMED.** `main()` never calls `write()` on the 304 laws. With `write()` broken, it still prints *"written back exactly: 304 of 304"* | **DRAFT:** the checker compares `write(L)` with the bytes on every law, and its line counts that comparison. `plant_reverts.py` breaks `write()` and requires the count to fall |

## The questions for the owner

### ASK U1 (M1). How does R2 tell a re-encoding from an echo?

His N2 words: *"The core writes back the exact law bytes it successfully loaded."* Every byte string that passes
section 8 is canonical. So a core whose write-back copies the bytes it read gives the same OUT as one that writes them
from what it loaded. R2 then cannot see L4's case: a core that drops a part no run reads, a name say.

| | what it entails |
|---|---|
| **(a) OUT from the writer alone, and a writer plant to prove it** | Section 10 says OUT is produced only by the writer of sections 2–4, from the loaded structure, never from the bytes read. R7 gains two writer plants, each required to be caught by R2: the write-back omits a `let`'s name, and it reverses an `(over …)` list. A core that echoes its input lets both pass, so R7 itself exposes the echo. The independent source reading (section 0) also records where OUT's bytes come from. Two plants and a sentence; it makes R2 observe what N2 adopted it for |
| (b) the limit stated | R2's record says it shows that the loaded law writes back as read, and does not show that the core keeps every written part. L4's case stays unobserved |

Recommended: **(a)**. Without it, N2's write-back cannot fail a core for the very defect it was adopted to catch.

### ASK U2 (M2). Three points of the runner's faults, to confirm or reverse

He accepted *"the ten minor findings"* as mechanical corrections, *"provided they do not alter adopted semantics or
classifications"*. Draft 6 also applied L2's and L3's DRAFT rows, both MAJOR, and with L5 it changed two
classifications of Amendment 4's runner:
- a text the front end refuses was NO-REFERENCE-RESULT, and is now a runner fault;
- a budget of −1 was a RESULT (`RUN STOPPED ops 0`), and is now a runner fault.

| | as applied in draft 6 | the other way |
|---|---|---|
| (i) L2's and L3's DRAFT rows | applied: the adjudicator gets the whole draft; `classify` reads raw runs; a runner fault exits 3 and is never a class | not adopted: Amendment 4's runner and reading set stand, and draft 7 takes the rows out |
| (ii) a runner fault | handled as an interrupted experiment: discarded whole and repeated, its runs kept and counted, never toward acceptance | a runner fault stops the experiment and goes to him, with no repetition |
| (iii) a runner fault that recurs | (unsaid) | after one repetition that ends in a fault again, the experiment stops, and the fault goes to him. No third run |

Recommended: **confirm (i) and (ii) as applied, and add (iii)'s rule**. The two reclassified cases were defects: a text
the experiment holds as accepted cannot meaningfully be a reference crash, and a budget no core accepts cannot be a
result. A recurring fault is a defect of the setup, so it should go to him, not loop.

## What follows his answers

1. **LAW-FORMAT-0 draft 7:** every DRAFT item and his answers, each change marked with its finding. Drafts 0–6 and the
   seven re-read reports stay as they are.
2. **The checker, `plant_reverts.py`, `ref_run.py` and `ref_run_paths.py` amended to match**, each run twice. That
   covers:
   - M3's consistent W5 naming, and its three plants;
   - M4's plant;
   - M10's write-back comparison;
   - M7's runner checks;
   - under U1(a), the writer plants named for R7 (the core's, not the checker's).
3. **SHEET.md Amendment 6:** U1 and U2, M5's write-back rules, M6's reading set, M9's records. The records made again
   are `r6-reference` (rows unchanged: a prediction), and the checker's R6 and R2b verdicts, each made twice with
   identical bytes.
4. **A fresh independent re-read.**
5. **No core code** before its findings are resolved.
