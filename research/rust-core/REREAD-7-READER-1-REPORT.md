> **A tokened copy, not the original hand-back** (2026-10-31, his ruling on the ten older reports, by REREAD-9's ASK 9-2 procedure): each spelling of the home folder's path is replaced by a token, `⟦HOME⟧` or `⟦HOME83⟧`; the original is kept outside the repository and named in `kept/TOKENED.txt` by its length and sha256, and `kept_tokens.py restore` gives it back exactly with the prefixes. After this line and the blank line below it, the file is the kept tokened bytes exactly, so its line numbers are the original's plus two.

# REREAD-7, reader 1 of 3: the format and the checker, its report word for word (2026-10-30)

Saved as returned by the reader, a fresh general-purpose agent with no part in writing anything it read. REREAD-7 ran
as three readers working at the same time, by the owner's approval (to be recorded in RULINGS.md once the readers have
finished, since reader 3 read that file under a pinned sha256): reader 1 the format and the checker, reader 2 the
protocol and evidence, reader 3 the rulings and cross-document consistency. Each started fresh, had its own scratch
folder and its own letter for findings (V, X, Y), and saw nothing of the others' work. Each was briefed:
- to read draft 7 (sha256 `05010e01…`), SHEET.md (`4d2dca8c…`, Amendment 6 holding the two placeholders of the record
  being remade) and RULINGS.md (`2cb28949…`) as its part required, with the code, the records and the specifications;
- never to open, read, list or grep anything under `research/law-sufficiency/`;
- to write only under its own scratch folder in the system's temp directory, and change nothing in the repository.

Its report follows, unedited, taken from its own transcript rather than retyped.

---

# REREAD-7, reader 1: LAW-FORMAT-0 draft 7's format rules and its checker

## What I read and ran

**Read in full:** `LAW-FORMAT-0-DRAFT-7.md` (sha256 `05010e01…` confirmed), including appendix A, and its diff against draft 6. `format_check.py` (`5103fd39…`), `plant_reverts.py` (`23f9cccd…`), `run_format.py`, `ref_run.py`, and RULINGS.md from B1 to the end. SHEET.md Amendments 5 and 6. SPEC §1–§9, RUNTIME-SPEC §4–§9, and `src/orlog/interp.py` and `sema.py` in full.

**Ran:** everything from the repository root with `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B`, at Python's default recursion limit (1000), which I never raised.
- Both evidence records reproduce. After stripping CR, my output matches `evidence/rust-core-format-7.txt` and `-7-reverts.txt` exactly.
- I wrote the following scratch scripts:
  - odd-law probes (`probe1.py`, `probe2.py`);
  - an independent reading of phase 3, written from the text and fuzzed against the checker (`fuzz_gates.py`);
  - a budget-position predictor written from section 5 and SPEC §7, compared with the reference in fresh processes (`budget_positions.py`);
  - long chains (`chains.py`);
  - alternative readings applied to an in-memory copy of the checker and run against the whole check (`undo.py`), then against R6's 10,000 mutants (`r6_readings.py`);
  - two toy cores built from the checker, one writing OUT and one echoing LAW, with R7's two writer plants (`echo_core.py`);
  - a mutation fuzz with the reference behind it (`mutate.py`).
- HEAD stayed `2e9805a`. `src/`, `tests/` and `vectors/` are clean, and no repository file was written.
- No process I started failed with WinError 1450 or any other process-creation error, so nothing was re-run for capacity.

**What I could not check:**
- No core exists, so nothing about a core was run.
- decoder1 was only executed, never read (it is under the forbidden folder).
- I have no independent re-implementation of phase 4. Phase 4 was checked by targeted probes and alternative readings, not by a second implementation.
- The H9 derivation of the 130 bound (W14(c)) was only read, not measured.

**One note:** a grep for the SHEET's placeholders also matched one line of `research/rust-core/REREAD-7-READER-3-REPORT.md`. That file was not in my first listing of the folder, so it appeared during my run. I did not open it.

## Verdict

The checker implements phases 1–3 as written, and its gates' precedence too:
- 400,000 random structural laws: my independent reading of the text agrees with the checker on all of them. No crash, and the coverage assertion never fired.
- All 88 plants and all 304 laws pass, with exact write-back.
- About 34,000 corpus mutants: no checker crash. Every mutant it accepted (12,893) decoder1 also accepted, and none raised an exception in the reference under a budget of 10,000.

The B1 obligations hold as written:
- **Termination:** the argument checks out by reasoning.
- **Budget positions:** 134 of 134 runs agree with the reference, every budget from 0 to total ops + 1 on four laws.
- **Explicit stacks:** the checker accepts perform and rule chains of 100,000 and writes them back exactly.

Draft 7 is not yet a text a clean-room author can follow without guessing. Three findings are MAJOR:
- **V1:** R7's writer plants cannot tell an echoing core from a writing one when W3 is judged by writing back, a design the format itself describes. SHEET Amendment 6's wording then either fails a compliant core or passes an echoing one.
- **V2 and V3:** two parts of phase 4's error recovery (numbering after a repeated id, and what counts as underived) are left undetermined. The checker departs from the most literal reading in both, and no plant pins either.

None of the three moves any of R6's 10,000 frozen verdicts (MEASURED). Nothing I found is a BLOCKER.

## Answers

**Q1: does the checker implement sections 2–4 and 8 as written?**
- **Phases 1–3: yes (MEASURED).**
  - Depth gate first, with no W4–W13 check when it fails: code lines 586–587, plants N1 and L6.
  - Then the least (line, W) among chain and structure failures.
  - W5's naming: a first arm names an absorbed clause too, in a sound chain (lines 685–691) and in a W4 chain (line 677).
  - The narrow reading: an inline `if` names nothing, through its blocks, its arms or its else. Only clause-statement Ifs feed `blocks` and `chain_of`.
  - The coverage assertion is at line 1065.
  - The write-back is compared on every law at line 1594.
  - The 400,000-law fuzz agreed on all of them.
- **Phase 4: no, in two places (V2, V3).** Three readings, each on its own, change only my probe laws and nothing else in the whole check or among R6's mutants (V4): numbering after a repeated id (V2); a rule's type, and the parts of a check, treated statically (V3); and W14(b) without its reset at a procedure (V4).

**Q2: do the plants test what their findings say, and do they bite?**
- Each undoing reproduces the alternative it claims. I checked the draft 4, draft 5, sequential-order, M3 and M4 undoings against section 11's stated outcomes.
- Readings that no plant pins (MEASURED): V2, V3, and V4's two (no reset at a procedure; only a block naming its own clause names it).
- J9's "only by a crash" is overstated (V5). A fixed-width reader bites three of J9's four plants without a crash. The clause-number plant cannot bite under that reader at all.
- M10's plant bites only a comparison that W3 already implies (V7).

**Q3: section 10's write-back mode, for a clean-room author.**
- Usage errors, outcomes, files and the exhaustion kind (`law` only) are specified.
- Two things are left to guess:
  - how R7's plants count as caught when the writer is also the W3 judge (V1);
  - how fine "never copied from the input bytes" is (V8).

**Q4: the B1 requirements.**
- **Termination:** sound as stated.
- **Budget:** the check positions match the reference exactly (MEASURED).
- **Explicit stacks:** the checker passes 100,000-long chains, while the reference crashes with a RecursionError at 1,000 (its known limit).
- **Detected exhaustion against external termination:** consistent through sections 0 and 10.
- One theoretical gap: the operation count can pass 2^64−1 (V9).

**Q5: what a clean-room author would still guess.** V2, V3, V6, V8, V9, and V1's catching rule.

## Findings

### V1 — MAJOR. R7's writer plants do not make an echoing core fail when W3 is judged by its writer, and "through the byte mismatch" would fail a compliant core
- **Where:** `LAW-FORMAT-0-DRAFT-7.md:514` (W3): *"Once W2 holds, writing back gives the rest exactly if and only if W3 holds"*. `:731–735`. SHEET.md:668–676: *"R2 must catch each through the byte mismatch it causes"* and *"A core whose write-back copies its input would let both pass, so R7 fails it."*
- **Evidence (MEASURED, `echo_core.py`):** two toy cores built from the checker, whose W3 is a write-back comparison. On the 298 laws:
  - **As built:** both write back 298 of 298 equal.
  - **"Drops a name":** the writer core and the echo core both give 154 LOAD-REFUSED, 0 byte mismatches.
  - **"Reverses over":** both give 3 LOAD-REFUSED, 0 byte mismatches.
- **What follows:**
  - The plants cannot tell echoing from writing for this design, which the format invites and the checker itself uses.
  - If only a byte mismatch counts as caught, a compliant writer core fails R7.
  - If any failure of R2 counts, an echoing core passes R7.
  - Either way the claim that the plants catch an echoing core holds only for cores whose loading never runs their writer.
- **Proposal (needs his ruling, since it touches U1's wording):** say that R2 catches a writer plant through a byte mismatch *or* through a load refusal of an accepted law. Withdraw the claim that the plants detect echoing, and leave OUT's provenance to section 0's source reading alone. Or, alternatively, require W3 to be judged lexically, independent of the writer.

### V2 — MAJOR. W8's numbering after a repeated or misnumbered id is undetermined, and the checker departs from section 7's literal reading
- **Where:** draft `:459`: *"Variables, claims and musts get ids 0, 1, … in the order the walk meets their declarations"*. `:519` (W8): *"each declared once"*. `format_check.py:906–913` (a repeated id is not counted), `:993–995` and `:999–1001` (musts and claims are counted by distinct id).
- **Evidence (MEASURED, `probe1.py`):**
  - **T1a:** block children declare id 0 at line 4 and id 0 again at line 5; the inline else on line 3 declares id 1. The checker says **W8 line 5**. Under the literal reading the third declaration met should be id 2, so **W8 line 3**.
  - **T1b:** the same law with the else declaring id 2 flips both verdicts.
  - **T1c:** the same with claims behaves as T1a.
  - **Pinning:** the ordinal reading changes nothing in the whole check (88 plants, 304 laws) and none of R6's 10,000 verdicts (`undo.py`, `r6_readings.py`).
- **Why it matters:** the line is part of a load refusal's result, so two cores that read this differently disagree (section 10). R6's adjudicator cannot decide such a case against section 8.
- **Proposal:** state the recovery rule for variables, claims and musts alike, either "the i-th declaration met has id i" or "the next id is the count of distinct ids declared so far". Make the checker agree, and add a plant whose line depends on the choice (T1a).

### V3 — MAJOR. "Underived" is broader in the checker than in section 8, which moves W9 to W10 on the same line
- **Where:** draft `:630–632` lists what an earlier failure leaves underived: *"a missing clause (…), an undeclared variable's type, a rule with no define"*. Derivation 17 (`:434`): *"the type of its first `define`'s value"*. W9 (`:544–545`): *"With one: an int index, a list variable, and the element type."*
- **What the checker does:**
  - It types a rule incrementally during the walk (`format_check.py:812`), so a use walked before the first define has no type.
  - It skips a whole compound check when any operand is underived: lines 941, 861–862, 873 and 832.
- **Evidence (MEASURED):**
  - **T2a,** `(say (+ int (rule "r") (lit bool 1)))` with r defined later as an int: checker **W10 line 3**; by the text **W9 line 3**.
  - **T2c,** the same use placed after r's first define: the checker gives **W9**. So its verdict depends on walk order, which derivation 17 does not.
  - **T3a/b/c/e** (`set` or `item` with an index on a non-list variable where the index is a rule with no define; `list-of` with a text value; `change` on a bool): checker W10. The list-variable part needs no index type, so the text gives W9.
  - **T7,** `(define "r" (rule "r") …)`: derivation 17 is circular for a first define that uses its own rule. Nothing says such a type is underived.
  - **Pinning:** no plant pins either point, and no R6 verdict moves (`undo.py`, `r6_readings.py`).
- **Proposal:** make the underived list exhaustive and say that derivation 17 applies wherever a use stands. Name each W9 condition as a separate check, made whenever its own inputs are derived. Correct the checker, and plant T2a and T3a.

### V4 — MINOR. Two readings that agree with the text are unpinned
- **W14(b)'s reset at a procedure** (`:574–575`, `format_check.py:583`): a non-top-level procedure inside 10 loops, with 10 more inside it. Built: W6 line 13. Without the reset: W14 line 20.
- **"Named by a block"**, which includes a block naming another clause (W5 row; line 716): with only a block that names its own clause counting, the verdict moves from W5 line 5 to W5 line 3.
- Neither changes any plant, corpus law or R6 verdict (MEASURED).
- **Proposal:** add the two probes as plants.

### V5 — MINOR. J9 "only by a crash" understates
- **Where:** draft `:883–884`: *"Six change only by a crash of the undone checker: … J9's four"*. The undoing is `plant_reverts.py:182`.
- **Evidence (MEASURED, `undo.py`):** a fixed-width reader is one that refuses an ⟨n⟩ above 2^64−1 as W2, and a prefix number that does not fit as W1. Under it:
  - the Int literal gives W2 line 3, not W13;
  - the perform target gives W2 line 3, not W4;
  - the label part gives W2 line 4, not W4;
  - the checker run ends FAILED, 85 of 88;
  - the clause number gives W1 line 3 either way.
- **Proposal:** add the non-crashing undoing to `plant_reverts.py`. Record the clause-number plant as one that pins only "no crash".

### V6 — MINOR. W8's row names only variables
- **Where:** `:519`, "**variables** (UNDECLARED, LOOP-VARIABLE)". The checker files claim and must misnumbering under W8 (T4a and T4b, both W8 line 3).
- A reader could file claim ids under W12, "claims".
- **Proposal:** say "ids of variables, claims and musts".

### V7 — MINOR. M10's measurement is implied by W3
- **Where:** `:813`, `:816–818`, `:880–881`. Code: `format_check.py:526` compares `w_stmt` with the rest of the line, and `write()` concatenates those same `w_stmt` outputs.
- So `write(L) == law` holds for every law that passes W1–W3. The draft admits this ("which W1–W3 imply by construction").
- The plant (`plant_reverts.py:146`, a byte appended in `write()`) bites only the count line. A real writer defect in `w_stmt` shows up as W3 refusals instead.
- **Proposal:** say the count cannot fail independently of W3, and describe the plant as testing that the comparison exists.

### V8 — MINOR. How fine "never copied from the input bytes" is, is not defined
- **Where:** `:104–105`, `:732–733`. Section 3 (`:187–190`) forbids parsing an ⟨n⟩ into a fixed width before the checks, which invites keeping digit strings as slices of the input.
- Whether writing kept slices back (digits, a name's escaped form) counts as copying is left to the source reader.
- **Proposal:** state that every atom is decoded to its value, and the writer re-encodes each by section 3, with no slice of the input reaching OUT.

### V9 — MINOR (reasoned). The operation count can pass 2^64−1, and nothing says what then
- **Where:** SPEC §7 (SPEC.md:209): "`ops` (u64…)". Draft `:308–309`: a `for` may run 2^64 times. B can be up to 2^64−1 (`:675`).
- What happens when the count overflows, both for counting and for the check "ops > B", is not stated. It is unreachable in practice, but it is a guess for a literal author.
- **Proposal:** one sentence fixing it, either "ops is unbounded" or "saturates".

### V10 — MINOR, outside my part, noted for the other readers
- **(a)** `ref_run.py:165` and `:171` hash and write the trace as `"\n".join(...)`, without the final LF that RUNTIME-SPEC §5 (`:145`) requires. MEASURED: `runs/b1-None/reference.trace` has 17 lines and 16 LFs. R4 compares traces line by line, so this matters only if a harness compares by sha.
- **(b)** SHEET.md:733 and `:744` still hold the placeholders `<R6REF7_SHA>` and `<R6REF7_NOTE>`, and `research/rust-core/r6-reference-3.txt` does not exist.
- **(c)** RULINGS.md:495–497 says M3 changes *"the checker's verdict, not the format's text"*, but draft 7 added text to W5's row (the diff at row W5).

## Files created (all under `⟦HOME⟧\AppData\Local\Temp\reread7-1\`)
- **Scripts:** `probe1.py`, `probe2.py`, `fuzz_gates.py`, `budget_positions.py`, `chains.py`, `undo.py`, `echo_core.py`, `mutate.py`, `r6_readings.py`.
- **Outputs:** `fc_run.txt`, `pr_run.txt`, `echo_core_out.txt`, `fc_alt_src.py.txt` (the last alternative checker source written by `undo.py`).
- **`laws\`:** `b1.orl`–`b4.orl`, `perform-200.law`, `perform-1000.law`, `rule-200.law`, `rule-1000.law`.
- **`runs\`:** 142 run folders, each holding `reference.out`, `reference.trace` and, where the run completed, `reference.receipt`.

## Appendix: commands and outputs (each `cd` to the repository root, then `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B …`)

**Reproduction**
```
format_check.py   -> FORMAT CHECK (DRAFT 7) HELD: 304 of 304 laws pass, 304 written back exactly, derivations equal on 304; plants 88 of 88 caught   (identical to the evidence once CR is removed)
plant_reverts.py  -> PLANT REVERTS HELD: 40 plants and fixtures, 40 changed by at least one undoing, 6 of them only by a crash   (identical)
```

**probe1.py** (excerpt)
```
T1a dup id 0 at line 5, else declares id 1 at line 3   checker: W8 line 5 (variable 0 declared twice)
T1b ... else declares id 2 at line 3                   checker: W8 line 3 (variable 2 declared where 1 is next in the walk)
T1c claims ...                                          checker: W8 line 5 (claim 0 where 1 is next in the walk)
T2a forward rule use, int rule in a bool sum            checker: W10 line 3 (rule 'r' used before its last define)
T2b forward rule use of a bool rule as int operand      checker: W10 line 3
T3a set with an index on an int var, index rule-no-def  checker: W10 line 4
T3b item of an int var ...                              checker: W10 line 4
T3c list-of text, count rule-no-def                     checker: W10 line 3
T3e change on a bool var ...                            checker: W10 line 4
T4a a claim numbered 5                                  checker: W8 line 3
T7 self-referential first define                        checker: W10 line 3
```

**probe2.py** (excerpt)
```
T2c use between first and last define                   checker: W9 line 4 (+ on int and bool as int)
T2a again: use before both defines                      checker: W10 line 3
P1 rule in an absorbed arm, a define inside K's block    checker: W6 line 4
(given) / (over) without their space                     checker: W3 line 3
```
All other probes came out as worked by hand.

**fuzz_gates.py**, seeds 7, 1, 2, 3, 4 (30,000 laws, then 100,000 for each of the other four)
```
FUZZ GATES seed 1: {'agree': 100000, 'disagree': 0, 'crash': 0, 'gate': 95395, 'walk': 4605, 'p12': 0}
(seeds 2–4 alike; seed 7: 30000 agree, 0 disagree, 0 crash)
```

**budget_positions.py**
```
b1: 18 clauses; unbounded: predicted COMPLETED ops 45 events 17; reference COMPLETED ops 45 events 17; ENV python CPython 3.14.5 recursion-limit 1000 format_check not-imported
b2 ops 12; b3 ops 37; b4 ops 32, all equal
BUDGET POSITIONS: 134 runs compared, 0 differ
```

**chains.py**
```
checker  perform chain 100,000  7666745 bytes  accepted, written back exactly
checker  rule chain 100,000     6066750 bytes  accepted, written back exactly
checker  over chain 3,000        accepted, written back exactly
reference perform-200 exit 0 RUN COMPLETED ops 201;   perform-1000 exit 1 REFERENCE-EXCEPTION builtins.RecursionError
reference rule-200    exit 0 RUN COMPLETED ops 201;   rule-1000    exit 1 REFERENCE-EXCEPTION builtins.RecursionError
```

**undo.py**
```
W8 ordinal         probe: as built W8 line 5  under the reading W8 line 3;   whole checker run: lines that differ: 0
rule type static   probe: as built W10 line 3 under the reading W9 line 3;   lines that differ: 0
partial set check  probe: as built W10 line 4 under the reading W9 line 4;   lines that differ: 0
loops no reset     probe: as built W6 line 13 under the reading W14 line 20; lines that differ: 0
J9 fixed-width     W13->W2 line 3; W1->W1 line 3; W4->W2 line 3; W4->W2 line 4; whole run exit 1, plants 85 of 88 caught
(block naming its own clause only: W5 line 5 -> W5 line 3; lines that differ: 0)
```

**r6_readings.py**
```
mutants: 10000; verdicts that move: 0 under each reading (W8 ordinal, rule type static, partial set check, loops no reset, J9 fixed-width)
```

**echo_core.py**
```
laws: 298; holding a let with a non-empty name: 154; holding an (over ...) list of two entries or more that differ: 3
drops a name   WRITER {'LOAD-REFUSED': 154, 'WRITTEN-BACK equal': 144} -> 0 by a byte mismatch, 154 by a load refusal
drops a name   ECHO   {'LOAD-REFUSED': 154, 'WRITTEN-BACK equal': 144} -> 0 by a byte mismatch, 154 by a load refusal
reverses over  WRITER/ECHO {'LOAD-REFUSED': 3, 'WRITTEN-BACK equal': 295} -> 0 by a byte mismatch, 3 by a load refusal
```

**mutate.py**, seeds 11–14
```
MUTATE seed 12, 11432 distinct mutants: {'refused': 7162, 'accepted': 4270, 'crash': 0, 'writeback_bad': 0, 'ref_ok': 4270, 'ref_decoder_refused': 0, 'ref_exception': 0}
(seeds 11, 13, 14 alike: 0 crash, 0 decoder refusal, 0 reference exception)
```

**Trace final LF** (V10a): `runs/b1-None/reference.trace` has 17 lines and 16 LFs; it ends without an LF.
