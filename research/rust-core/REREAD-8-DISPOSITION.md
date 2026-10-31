# REREAD-8: the dispositions of its findings, the three readers' in one (PROPOSED, 2026-10-30; ruled, below)

**Ruled (2026-10-30).** The owner ruled G to L (recorded whole in [RULINGS.md](RULINGS.md)): G adopted; H adopted
provisionally at 91; I adopted; J, the runner left unchanged and its limitation kept; K adopted; L1 confirmed; L2
confirmed with a clarification; L3 not confirmed. His principle: *"the checker must implement the adopted wording, not a
more permissive interpretation that happens to pass the existing corpus."* His precisions, among others:
- H: *"Until that challenge is complete, 91 is the candidate limit, not a proven maximum."*
- J: *"the uncaught `SystemExit` case remains a documented limitation. Do not describe it as covered or resolved."*
- L3: *"Write down the exact W9 parts and their individual type checks in Draft 9. Then independently verify that the
  checker implements that enumeration."*

The text below is kept as it was proposed.

**Status.** Proposed, not adopted. These dispose of the 34 findings in REREAD-8's three reports, as for REREAD-7:
*"Merge the three reports, preserve every finding and its provenance, resolve overlaps explicitly, and bring me one
disposition with clearly separated rulings required."*

The three reports:
- [REREAD-8-READER-1-REPORT.md](REREAD-8-READER-1-REPORT.md): the format and the checker, findings ZA1–ZA9 (4 MAJOR,
  5 MINOR);
- [REREAD-8-READER-2-REPORT.md](REREAD-8-READER-2-REPORT.md): the protocol, the runner and the evidence, ZB1–ZB12
  (1 MAJOR, 11 MINOR), with the hash closure of `r6-reference-5.txt`;
- [REREAD-8-READER-3-REPORT.md](REREAD-8-READER-3-REPORT.md): the rulings and cross-document consistency, ZC1–ZC13
  (2 MAJOR, 11 MINOR).

In all: 0 BLOCKER, 7 MAJOR, 27 MINOR. Two more, AR-1 and AR-2, are mine, found against ATTEMPT-RECORD-0 before the
reports came; no reader raised them.

**What they read**, each file checked against its pinned sha256 first (all 24 held for all three readers):
- LAW-FORMAT-0 draft 8 (`94a989a6…`), its checker (`3bc07ca8…`), `plant_reverts.py` (`d1f1c663…`) and
  `depth_probe.py` (`886ca922…`);
- the reference runner (`822c826e…`), its check (`87d93a49…`) and `gen_r6_reference.py` (`cc63252d…`);
- the record `r6-reference-5.txt` (`636a2873…`) and the draft-8 evidence;
- SHEET.md (`b9a3057e…`). It is `a18e0af6…` since one note was added, after the readers finished (ATTEMPT-RECORD-0);
- RULINGS.md (`387ef2e8…`). It is `ccd71e89…` since ATTEMPT-RECORD-0 was recorded, after the readers finished.

**The hash closure passed** (his R6 remake ruling's item 5; F2). Reader 2 checked that `r6-reference-5.txt` hashes to
`636a2873…`, the value at both places Amendment 7 states it; that it is both generations' files byte for byte, each at
its attempt's `output_sha256`; that its 10,000 rows equal `r6-reference-3.txt`'s; and that its header names the
runner, the generator, decoder1, `interp.py`, the mutants and the five ENV modules by their sha256 as they are. Its last
line begins *"HASH CLOSURE: PASSED"*. The re-read is complete.

**What happens next.** Nothing changes until he rules. He answers ASK G to L. Then draft 9, the checker and the sheet's
Amendment 8 apply every DRAFT item and his answers, and a fresh independent re-read follows. No core code is written
before its findings are resolved. In his words: *"Authorization remains unchanged: Phase 0 only."*

## What the re-read found holds

**The format and the checker** (reader 1, MEASURED there):
- the checker, `plant_reverts.py` and `depth_probe.py` each ran twice, byte for byte alike, and each equals the body of
  its evidence record: 304 of 304 laws pass and are written back exactly, 94 of 94 plants caught; 46 of 46 plants and
  fixtures changed by at least one undoing;
- the six new plants each bite by their own undoing; R2's 11 write-back fixtures are each accepted and written back
  exactly;
- section 10 and section 0 carry his A: no core was found that meets the text and escapes both writer plants;
- B1's termination argument re-derives; 130 is kept (`DEPTH_PARENS = … 130`, its fixture and plant standing).

**The protocol and the evidence** (reader 2, MEASURED there):
- the hash closure, above. Generation 2 started 0.489 s after generation 1's last run ended, and every figure of
  Amendment 7's tables reproduces from the attempt records;
- 93 mutants, chosen by a rule frozen before any outcome was seen (sha256 `9e7f26fb…`, 09729 excluded by the brief),
  each give their row in two fresh runs, twice;
- 14 plants in a copy of the generator behave as the sheet says, but P11 (ZB1) and P13 (ZB6);
- `ref_run_paths.py` gives 43 of 43, twice, equal to its record; the variants give 14 of 15, as recorded; the checker's
  `-8` records are made again byte for byte.

**The rulings** (reader 3): A to F and the R6 remake ruling are each carried in substance, mostly in his words. No
document presents the attempt-record proposal as his ruling. His D1 qualification is honoured. No dated record was
found rewritten (15 quotes REREAD-7 took were found word for word). Every count it could recompute is right but four
(ZC3, ZC5, ZC7, ZC8).

## The measurements (MEASURED; software readings from the session's own records)

| reader | wall | tokens | tool uses |
|---|---|---|---|
| 1, the format and the checker | 1,807.5 s | 391,451 | 54 |
| 2, the protocol, the runner and the evidence | 1,827.5 s | 364,529 | 74 |
| 3, the rulings | 1,290.1 s | 430,647 | 59 |

All three were started at about 23:10 and the last finished about 30.5 minutes later; 1,186,627 tokens in all. No
process failed to start.

## Disclosures

1. **Readers 1 and 2 each ran a whole-tree `git status --untracked-files=all` first.** Its output listed the names of
   untracked files under `research/law-sufficiency/`. Neither opened, read or grepped any of them. Reader 2 ran it
   without `GIT_OPTIONAL_LOCKS=0`, so git may have refreshed `.git/index`; no tracked content changed. Reader 2 also
   listed `work/`'s top-level folder names once. The brief forbade listing that folder and did not foresee `git status`.
2. **Reader 2 saw short lines of `decoder1.py`**, quoted in the tracebacks the attempt records keep, which its brief let
   it read. A brief that opens attempt records to a reader who must not read decoder1 should say so.
3. **Reader 3 did not open `work/`** (its brief), so it held the remake's figures as DECLARED. Reader 2 reproduced them.
4. **09729 was not run** (the brief). Its 24.06 GiB and 42.5 s alone stay measured once, here (Amendment 7).
5. **Nothing pinned changed while they read.** ATTEMPT-RECORD-0 came while they were at work. It was recorded in
   RULINGS.md, and noted in SHEET.md, after all three had finished. Reader 3 hashed its files again at its end:
   unchanged.
6. **The draft-8 evidence and the R6 remake ruling** (reader 3's "could not check"). The ruling was recorded at 21:20.
   The draft-8 evidence was made again from 21:27:47 to 21:32:47, because draft 8's Q6 was edited for the ruling, and
   that was reported to him that evening. `run_format.py`'s two logs (21:08:23 and 21:32:47) are byte for byte equal:
   its five summary lines did not change. The records' earlier bytes were not kept, so they are not compared. The last
   record was written 19 s before generation 1's commit was first read, at 21:33:06: no overlap (MEASURED, by the files'
   times and the attempt record).
7. **The saved reports name each reader's scratch folder** under the account's temp directory, as every report since
   REREAD-1 has. They are kept word for word.

## Which findings are mine

All 34 are of work I wrote; none finds his words wrong. Those that repeat a mechanism or a claim of mine:
- **ZC5: I applied the disposition's summary of Y10, not Y10's row.** The row named five places; I noted two. That is
  L1's and Y1's mechanism, a third time.
- **ZC2: I gave him a condition he did not set.** Draft 8 says 130 stays *"as he ruled, until it is"* established, and
  `depth_probe.py`'s summary line says the same. He said until it is measured. My own "As kept" note in RULINGS.md says
  "until the front end's limit is measured", so the two documents disagree.
- **ZB1:** Amendment 7 and the generator's docstring say `attempt.json` is written before any child process starts. The
  generator starts one before it. I found it in a read-only check against ATTEMPT-RECORD-0 and told him before the
  reports came, as with ZB6, AR-1 and AR-2.
- **ZA1 and ZA3:** my checker departs from E2 as he adopted it.
- **ZB4 and ZC3:** "eight modules" came from REREAD-7's reader 2 into my D5 text, which he adopted. In law mode the
  runner hashes five.
- **ZB8:** "about four seconds" was my estimate from the runs' positions in records that keep no time for a run.
  Reader 2's simulation puts it at about 36 s. Neither is a measurement.
- **ZC10:** my restatement of his item 2 dropped "generator".

## The overlaps, resolved

| cluster | findings | the one issue | disposed by |
|---|---|---|---|
| C1, E2 in the checker | ZA1, ZA2, ZA3, ZA4, ZA5 | derivation 17 and W9's parts are not implemented as stated, and the text contradicts itself on a self-using first define | DRAFT (ZA1, ZA3, ZA5); ASK G (ZA2); ASK L3 (ZA4) |
| C2, D1's limit | ZA8, ZC2 | the deepest law line is 91 by a witness; his second step was neither done nor brought back; a condition is attributed to him | ASK H; DRAFT (ZC2's wording) |
| C3, acceptance and the records | ZC1, ZC11, ZB9 | section 7 states one repetition requirement and two evidence-record requirements; "preserve" is read as "by sha256"; the attempt records do not travel with the record | ASK I |
| C4, the runner's edges | ZB2 = ZC4, ZB11 | a `SystemExit` before the reference is not a runner fault; an interrupt is labelled a runner fault | ASK J |
| C5, the generator | ZB1, ZB6, AR-1, AR-2 | its record begins after one child process; a harness exception keeps its type alone; the start-failure count stops at one; `PYTHONUTF8` goes unrecorded | DRAFT, for the next generator (ATTEMPT-RECORD-0) |
| C6, F1's memory sentence | ZB10 = ZC9 | "workers may rise" ignores memory | ASK K |
| C7, the failed attempt's files | ZB12 = ZC13 | its two generations' files are kept unevenly | DRAFT |
| counts | ZB4 = ZC3, ZB5 = ZC8, ZB7 = ZC7 | five modules, four of REREAD-6's changes, ten fixtures of eleven | DRAFT; ASK L2 (the "eight") |

**Where the readers differ:**
- **On facts:** D1's bracket. Reader 3 took draft 8's "between 90 and 99". Reader 1 measured a 91-deep line and argued
  that 91 is the limit. Reader 1's is the newer fact; ASK H takes it.
- **On severity:** nowhere. Each pair above is MINOR in both reports.

## The findings, each with its reader

Each concrete claim was run again here, read-only, where the row says so:
- scratch `check_za.py`: laws A, B and C, ZA3's two laws and ZA4's `neg` law through `format_check.read`, and the
  91-deep witness through the checker; the witness's text through the front end (`compile_bytes`);
- scratch `check_ref5.py`: the pair's sha256, the gap, the peaks and 09729's rows;
- the generator's lines 295, 313, 362 and 364–399 read; greps of the text.

Where a claim was not run here, the row says so. Line numbers are the readers', in the files as they read them;
SHEET.md's lines after 808 are one later since the ATTEMPT-RECORD-0 note.

| | reader, severity | finding | re-run here | disposition |
|---|---|---|---|---|
| ZA1 | 1, MAJOR | the checker types a rule by its first *derived* define, against derivation 17; the same fallback crashes on a 4-clause law | **CONFIRMED:** law B gives W9 line 3; law C raises `AssertionError: the rules' types did not hold still`. Reader 1 measured that the strict reading moves no plant, fixture or corpus law; not re-run | **DRAFT:** a rule's type is its first define's in clause order, underived when that value's is. Laws B and C planted (W10 line 3), each undone. Draft 9 says how derivation 17 is computed without recursion |
| ZA2 | 1, MAJOR | a first define that uses its own rule: his E2 words against section 8's "the type its form gives it" | **CONFIRMED:** law A gives W9 line 3 | **ASK G** |
| ZA3 | 1, MAJOR | a promote's own W9 parts are skipped when its place is underived | **CONFIRMED:** both laws give W10 line 3 | **DRAFT:** both parts made whatever the place; both laws planted (W9 line 3), each undone |
| ZA4 | 1, MAJOR | W9's parts are not enumerated, so the checker's split is a guess | **CONFIRMED:** `(neg bool (rule "r"))` gives W9 line 3, where reading the rule as two conjuncts that both need the operand gives W10 | **ASK L3** |
| ZA5 | 1, MINOR | no plant pins E1 for claims and musts, or W9's parts outside set and change | not re-run. Reader 1 measured each undoing moving nothing but its own witness | **DRAFT:** the six witnesses planted, each with its undoing |
| ZA6 | 1, MINOR | E1's wording reads as one counter for all three kinds | not re-run (the text, as cited) | **DRAFT:** "each kind numbered on its own" |
| ZA7 | 1, MINOR | E4 overrides SPEC's `u64` without saying so | not re-run (reader 1's greps of SPEC.md:209 and RUNTIME-SPEC.md:177) | **DRAFT:** section 0 says the unbounded count governs for the core, whatever those lines say, and extends it to the cost counters, the claims' costs and evaluations, and the stop's printed count |
| ZA8 | 1, MINOR | D1's probe misses a reachable 91-deep line | **CONFIRMED:** the witness's text compiles in the front end to the law reader 1 saved (`74cd16d5…`); the checker accepts it, writes it back exactly, and its deepest line is 91 | **ASK H.** **DRAFT:** the witness and the argument recorded; the probe searches the family that reaches 91 |
| ZA9 | 1, MINOR | how far "the writer" extends is unstated; section 8's W3 row has no pointer to section 10 | not re-run (the text, as cited) | **DRAFT:** W3's row says it is decided by the spacing rule, never by writing back (section 10); the source reading names the writer's code, and R7's writer plants go in that code alone |
| ZB1 | 2, MAJOR | a harness fault before `attempt.json` is written leaves no record and is not counted | **CONFIRMED** by the code: the recursion-limit probe at :295 starts a child before `Attempt(...)` at :313 | **DRAFT, for the next generator** (ATTEMPT-RECORD-0, point 1): the folder and `attempt.json` first; any exception after `next_attempt` writes `end.json` INTERRUPTED, HARNESS-FAULT; P11 kept as a plant. The generator that made `r6-reference-5` is not changed (his ATTEMPT-RECORD-0), and its docstring stays as it is, since the record's header pins it; Amendment 7's sentence is corrected in place, with a note |
| ZB2 | 2, MINOR | a `SystemExit` while the reference's modules import is not a runner fault | not re-run. Readers 2 and 3 measured it apart: exit 0 or 1, no runner line, `classify` gives NO-REFERENCE-RESULT | **ASK J** |
| ZB3 | 2, MINOR | the runner's check does not hold the ENV line's completeness, the bytecode check's folders, or the implementation and version | not re-run. Reader 2's three variants pass 43 of 43 | **DRAFT:** the check computes the modules a fresh import loads and requires equality, plants a `__pycache__` in each folder by name, and compares the implementation, version and platform with its own |
| ZB4 | 2, MINOR | law mode's ENV line lists five modules, not eight | **CONFIRMED:** the record's header lists five | **DRAFT:** in-place notes at SHEET.md :819 and :924 (five in law mode, eight in text mode); **ASK L2** |
| ZB5 | 2, MINOR | the variants make four of REREAD-6's five changes | not re-run | **DRAFT:** the fifth (P keeping the text-seal line, in both modes) added; reader 2 measured the check catching it, 40 of 43. The record reads 15 of 16 |
| ZB6 | 2, MINOR | `process_start_failures` counts only the first stop | **CONFIRMED** by the code: `halt` keeps one stop (:364–368), and the count is taken from it (:398–399). `r6-reference-5`'s attempts had none | **DRAFT, for the next generator:** the count is of the `start_failure` lines in `runs.jsonl` |
| ZB7 | 2, MINOR | one of R2's 11 fixtures is in order and has no repeat | not re-run (the fixtures file's first row, read: `(given 2 1) -> (given 1 2)`) | **DRAFT:** "10 of the 11", in the sheet, with a note; `gen_r2_fixtures.py`'s docstring is noted there and not changed, since the fixtures' header pins it |
| ZB8 | 2, MINOR | Amendment 7's "about four seconds" is not supported | not re-run (reader 2's simulation) | **DRAFT:** corrected in place: both generations reached 09729 together, and generation 2's runs failed within about 1.4 s, inside generation 1's first run. Neither figure is a measurement |
| ZB9 | 2, MINOR | the attempt records would not travel with the record | **CONFIRMED:** `work/` is ignored; sizes measured here (ASK I) | **ASK I** |
| ZB10 | 2, MINOR | `workers may rise` ignores memory | **CONFIRMED** (disclosed in Amendment 7) | **ASK K** |
| ZB11 | 2, MINOR | an interrupt reaching a reference run is labelled RUNNER-FAULT, against B3's adopted *"never become a runner fault or a reference crash"* | not re-run. The disposition is INTERRUPTED either way | **ASK J** |
| ZB12 | 2, MINOR | the two generations of `r6-reference-4` are kept unevenly | **CONFIRMED** by listing | **DRAFT:** generation 1's file moves beside generation 2's, as `work/rust-core/r6-reference-4.gen1.txt`, its bytes unchanged; Amendment 7 says "`r6-reference-4`'s generation 1", with generation 2's one differing row beside it |
| ZC1 | 3, MAJOR | section 7 states one repetition requirement, and two of the adopted evidence-record requirements | **CONFIRMED:** RULINGS.md :643–645 against SHEET.md :876 | **ASK I** |
| ZC2 | 3, MAJOR | D1's second step neither done nor brought back; a condition attributed to him | **CONFIRMED:** draft 8 :635 against RULINGS.md :655, :661 and :761 | **ASK H.** **DRAFT:** draft 9 and `depth_probe.py` say "measured", as he did; RULINGS.md's note corrected in place |
| ZC3 | 3, MINOR | = ZB4 | = ZB4 | = ZB4 |
| ZC4 | 3, MINOR | = ZB2 | = ZB2 | = ZB2 |
| ZC5 | 3, MINOR | three of Y10's five in-place notes are missing | not re-run (reader 3's greps) | **DRAFT:** the three notes, at SHEET.md :3–4, :33 and :51–52 |
| ZC6 | 3, MINOR | the Y9 note misstates the history it corrects | not re-run | **DRAFT:** a further note in place: Amendment 3 brought the colon rule, K15 in Amendment 4 the runner's line, Amendment 5 the raw `classify` |
| ZC7 | 3, MINOR | = ZB7 | = ZB7 | = ZB7 |
| ZC8 | 3, MINOR | = ZB5 | = ZB5 | = ZB5 |
| ZC9 | 3, MINOR | = ZB10 | = ZB10 | = ZB10 |
| ZC10 | 3, MINOR | the sheet's restatement of the R6 remake's item 2 drops "generator" | **CONFIRMED:** the headers of `r6-reference-4.txt` and `-5` name generators `48d88b21…` and `cc63252d…`. The earlier generator's source is not kept | **DRAFT:** item 2 quoted whole in Amendment 8; **ASK L1** |
| ZC11 | 3, MINOR | condition 6's "Preserve … inputs, outputs" is read as "by sha256" | **CONFIRMED** by the text | **ASK I** |
| ZC12 | 3, MINOR | stale and colliding names: `plant_reverts.py`'s heading; "his D5", "his B1–B4" and "F2 … F" in the runner, the generator and the record | not re-run | **DRAFT:** `plant_reverts.py`'s heading corrected (its evidence made again). The runner's and the generator's names are noted in the sheet and not changed, since the record's header pins both files |
| ZC13 | 3, MINOR | = ZB12 | = ZB12 | = ZB12 |
| AR-1 | mine, MINOR | a harness exception the generator does not expect is kept by its type alone (:362), not its message or traceback (ATTEMPT-RECORD-0, point 5) | read in the code | **DRAFT, for the next generator:** the message and traceback kept in `end.json` |
| AR-2 | mine, MINOR | `attempt.json`'s environment names `PYTHONHASHSEED` and not `PYTHONUTF8=1`, which every run is given (:246, :305–307; point 3) | read in the code | **DRAFT, for the next generator:** every variable the runs are given is recorded |

## The questions for the owner

### ASK G (ZA2). A first define that uses its own rule

His E2: *"A first definition that uses its own rule leaves the type underived; the relevant use remains W10."* Draft 8's
section 8 also says that every other expression *"has the type its form gives it"*. Law A,
`(define "r" (as int (rule "r")))`, meets both: by his words r is underived, so W10; by its form, `as int` makes r int,
and `as int` from int fails W9. The checker follows the form (W9 line 3, confirmed here).

| | what it entails |
|---|---|
| **(i) his words govern** | "Uses its own rule" means a mention of the rule in the first define's value, followed through other rules' first defines. Such a rule is underived whatever its form gives. Section 8's list gains that item; the checker finds the cycle by the mentions alone, without types. Law A gives W10 line 3 and is planted. What it moves on the corpus and R6's mutants is NOT_MEASURED, and is measured before draft 9 is final |
| (ii) the form governs | The parenthetical is narrowed to a value whose type flows back to its own rule. Law A stays W9 and is planted. His sentence is noted as covering that case only |

Recommended: **(i)**. It is his adopted sentence as written.

### ASK H (ZA8, ZC2). W14(c): the front end's actual limit

His D1: *"Then specify and test the actual limit, including cases on both sides of the boundary."* And: *"The 130 bound
remains until that limit is measured."*

What is known now:
- the front end's two limits hold at their edges: a tree 64 deep, expressions nested 24 deep (MEASURED, reader 1 and
  draft 8's probe);
- a text the front end accepts writes a law line 91 deep (MEASURED by reader 1, confirmed here). One level more is
  refused for nesting; a longer chain is refused for the tree;
- no line can be deeper than 91: at most 3 wrappers, 64 tree nodes and 24 promotes, since each promote below the
  topmost sits under a conversion whose operand costs a nesting level (REASONED, reader 1; not re-read independently).
  Draft 8's 99 left out what the nesting limit does to the promotes.

| | what it entails |
|---|---|
| **(a) 91, in draft 9** | W14(c) becomes 91: the witness's line accepted, a 92-deep line refused, both planted. The argument is stated, and REREAD-9 is asked to break it. If it is wrong, the checker would refuse a law the front end writes; REREAD-9 reads it before any core exists |
| (b) 130 until REREAD-9 has re-read the argument, then 91 | the same, one draft later |
| (c) 130 | kept, and said in draft 9 to be not his words |

Recommended: **(a)**. The witness establishes 91 from below; only the upper side rests on the argument, and the
re-read that follows draft 9 tests it before anything depends on it. Never 90, which would refuse a law the front end
writes.

### ASK I (ZC1, ZC11, ZB9). Section 7's repetition, the evidence records, and where they are kept

His C: *"the adopted evidence-record requirements, including Y3's conditions 5 and 6, in their previously adopted
wording. Each applicable obligation must be held under its specified repetition requirements."* The option he adopted:
*"each held twice where it runs"*. Section 7 states a repetition for item 1 only, and item 8 names conditions 5 and 6
alone. Condition 6's "preserve" is read as "named by sha256". The attempt records behind Amendment 7's 0.489 s,
2.32 GiB and 5 ms are in `work/`, which is not tracked.

Measured here: the four attempt folders hold 151,090,353 bytes; compressed by Python's own `gzip` at level 9, 3,468,085.
The largest file is 37,974,177 bytes, under GitHub's 100 MB limit.

| | what it entails |
|---|---|
| **(a) every obligation with its repetition, every record kept** | Items 2 to 5 of section 7, like item 1, are each run twice with byte-identical output, on the owner's host. Item 8 names every adopted evidence-record requirement by its amendment (2; 3; 4's K10; 5's N3(3); 7's B2 and X5; ATTEMPT-RECORD-0), conditions 5 and 6 in his words. "Preserve" keeps the inputs and outputs themselves, each named by sha256. The attempt records of `r6-reference-4` and `-5` go into the tracked tree, compressed, each archive named by sha256 in Amendment 8 |
| (b) the same, the attempt records left in `work/` | the figures in Amendment 7 cannot be checked from a clone |
| (c) section 7 as it is | his C is carried short (ZC1) |

Recommended: **(a)**.

### ASK J (ZB2 = ZC4, ZB11). The runner's two edges, and the record

D5, adopted: *"every failure before `reference()` is a runner fault"*. B3, adopted: reference runs *"never become a
runner fault or a reference crash"*. The runner lets a `SystemExit` raised while the reference's modules import through
as a crash, and labels an interrupt RUNNER-FAULT.

No row of `r6-reference-5.txt` is either case: the generator refuses a run without its ENV line (ENV-MISMATCH, reader
2's P14), and an interrupt ends the attempt INTERRUPTED either way. But the record's header pins the runner
(`822c826e…`), so a changed runner needs a new record. His R6 remake exception applies *"only to the next R6 remake"*,
which is made; a new record would need his ruling on its form, since F1's concurrent generations failed.

| | what it entails |
|---|---|
| (a) change the runner now | `BaseException` caught before the reference, `KeyboardInterrupt` apart; an interruption line of the runner's own, which `classify` raises as Interrupted; the check and a variant hold each. Then `r6-reference-6`, in a form he rules, about 90 minutes of the host (`-5` took 5,323 s), and a hash closure. Its rows are predicted equal |
| **(b) keep the runner and the record** | Both edges are stated in Amendment 8 as known. Any harness that classes runs, the core's included, refuses a run without the runner's ENV line, as the generator does. The runner changes when a record is next made for another reason. B3's "never a runner fault" is read as the sheet states it: the disposition is INTERRUPTED either way |

Recommended: **(b)**. No outcome moves, and a remake brings back 09729's 2.32 GiB margin.

### ASK K (ZB10 = ZC9). F1's memory sentence

His F1: *"The measured process and memory limits govern."* The generator's rule applies his two conditions alone, and
printed `workers may rise: True` for both generations with 2.32 GiB of commit left at the peak.

| | what it entails |
|---|---|
| **(a) his sentence, and a truthful field** | Amendment 8 adds his sentence to F1's list. The next generator prints that F1's two conditions hold, not that workers may rise, and reports the commit left at the peak beside it. No numeric memory rule until it is measured for, as his ruling on the cap said |
| (b) a numeric condition now | workers rise only while the peak commit plus the largest run's own peak stays under the limit. The attempt records keep no run's own commit, so the rule would rest on one measurement of 09729 |

Recommended: **(a)**.

### ASK L. Three things settled beyond his words, to confirm or reverse

| | as settled | recommended |
|---|---|---|
| **L1** (ZC10) | His item 2: *"Keep the same runner, generator, inputs, environment, and worker configuration."* The generator changed (`48d88b21…` to `cc63252d…`), only to do what items 1, 2, 3 and 5 ask (RULINGS.md, "As kept"); each run was made as before. The earlier generator's source is not kept, so the extent of the change cannot be checked from the repository | **confirm** that reading |
| **L2** (ZB4 = ZC3) | D5's *"the eight `orlog` modules"*, my words from REREAD-7, adopted. The runner hashes every module loaded: five in law mode, eight in text mode | **confirm** "every module loaded" |
| **L3** (ZA4) | W9's parts are not listed. The checker splits each rule one way: `neg`, `abs` and `sqrt` with a result part; arithmetic as {⟨type⟩ numeric, a = ⟨type⟩, b = ⟨type⟩} | **confirm** the checker's split, listed in draft 9 with each part's inputs, one plant for each form a reader could split otherwise. It moves no verdict, by construction. The other way: he names a split |

## What follows his answers

1. **LAW-FORMAT-0 draft 9:** every DRAFT item and his answers to G, H and L3, each change marked with its finding.
   Drafts 0–8 and the re-read reports stay as they are.
2. **The checker, `plant_reverts.py` and `depth_probe.py`:** ZA1, ZA3, ZA5's six plants, ZA8's witness and his G and H.
   Each is run twice, each new plant bites, and the evidence is made again as `-9`.
3. **`ref_run_paths.py` and `ref_run_variants.py`:** ZB3 and ZB5, and the runner as J rules.
4. **SHEET.md Amendment 8:**
   - section 7 as I is ruled, and F1's sentence as K;
   - ATTEMPT-RECORD-0, stated for every remaining Phase 0 attempt;
   - in-place notes: ZB1's sentence, ZB4, ZB7, ZB8, ZB12, ZC5's three places, and ZC12's names. The generator's and
     `gen_r2_fixtures.py`'s docstrings are noted, not changed, since records pin both files.
5. **RULINGS.md:** ZC6's note, and ZC2's correction of my note.
6. **The next generator**, whenever a record is made again: ZB1, ZB6, AR-1 and AR-2, under ATTEMPT-RECORD-0.
7. **REREAD-9's briefs:** `git status` only for named paths, with `GIT_OPTIONAL_LOCKS=0` (disclosure 1).
8. **A fresh independent re-read,** three readers as F2 settled.
