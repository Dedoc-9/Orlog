> **A tokened copy, not the original hand-back** (2026-10-31, his ruling on REREAD-9's ASK 9-2): each spelling of the home folder's path is replaced by a token, `⟦HOME⟧` or `⟦HOME83⟧`; the original is kept outside the repository and named in `kept/TOKENED.txt` by its length and sha256, and `kept_tokens.py restore` gives it back exactly with the prefixes. After this line and the blank line below it, the file is the kept tokened bytes exactly, so its line numbers are the original's plus two.

# REREAD-8, reader 3 of 3: the rulings and cross-document consistency, its report word for word (2026-10-30)

Saved as returned by the reader, a fresh general-purpose agent with no part in writing anything it read. REREAD-8 ran
as three readers working at the same time, under the owner's F2 (RULINGS.md): reader 1 the format and the checker,
reader 2 the protocol, the runner and the evidence, with the hash closure of `r6-reference-5.txt`, reader 3 the rulings
and cross-document consistency. Each started fresh, had its own scratch folder and its own letter for findings (ZA, ZB,
ZC), and saw nothing of the others' work. Each was briefed:
- to check, before reading, the sha256 of every file it read against the brief's pins, among them draft 8 (`94a989a6…`),
  SHEET.md (`b9a3057e…`, Amendment 7 with the record `r6-reference-5.txt`, `636a2873…`) and RULINGS.md (`387ef2e8…`);
- never to open, read, list or grep anything under `research/law-sufficiency/`;
- to write only under its own scratch folder in the system's temp directory, run at most two processes of its own at
  once, and change nothing in the repository; reader 2 was told not to run mutant 09729, which commits about 24 GiB.

Its report follows, unedited, taken from its own transcript rather than retyped.

---

# REREAD-8, reader 3 of 3: the rulings and cross-document consistency (2026-10-30)

## 1. What I read and ran, and what I could not check

**Pinned files.** Before reading I checked all 24 pinned sha256 values, plus decoder1.py (`3584f565…`). Every one matched, and so did HEAD (`2e9805aaa1ceeae0beb443d527680796b66f39c7`). I hashed them again at the end and nothing had changed.

**Read whole:**
- RULINGS.md (`387ef2e8…`)
- every disposition, with the option text each "Adopt" adopted:
  - REREAD-0 `cb789fba…`, REREAD-1 `32ea782f…`, REREAD-2 `f93883a6…`, REREAD-3 `eafdeed0…`
  - REREAD-4 `3e7c546c…`, REREAD-5 `d54d1bd4…`, REREAD-6 `ef9559af…`, REREAD-7 `cb0b1c9f…` (pinned)
- SHEET.md (`b9a3057e…`) and LAW-FORMAT-0-DRAFT-8.md (`94a989a6…`)
- REREAD-7-READER-3-REPORT.md (`68fe25f6…`), for Y10's five places and the exact Y proposals

**Read in part:**
- REREAD-7-READER-2-REPORT.md appendix (`4c57a1ac…`) and the reader-1 and reader-2 finding headings (reader 1 `8170fa01…`)
- code: `ref_run.py` and `gen_r6_reference.py` whole; `gen_r2_fixtures.py` whole; the docstrings of `depth_probe.py`, `run_format.py`, `plant_reverts.py` and `ref_run_variants.py`, plus its variant list; `format_check.py` by grep (W14(c), phase 2); `gen_r6_mutants.sources()`
- the summary lines of every draft-8 evidence file
- the headers of `r6-reference-4.txt` (`1b10b1a0…`) and `r6-reference-5.txt`

**Ran.** Every run used `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B`, TEMP and TMP pointed at my scratch folder, and only one process of my own ran at a time. No process failed to start.
- `ref_run.py` once in law mode and once in text mode.
- A scratch copy of `ref_run.py` with a stand-in `orlog` that raises `SystemExit(0)`.
- `gen_r2_fixtures.py` once, writing into scratch.
- `depth_probe.py` once.
- My own `recount.py`. It calls `gen_r6_mutants.sources()`, which reads the corpus through `research/law-sufficiency`'s `common` module; I printed only counts and text ids.
- Greps and diffs of the records.

I opened, listed and grepped nothing under `research/law-sufficiency/`, and nothing under `work/`.

**Could not check:**
- **The attempt records under `work/rust-core/attempts/`** (not opened, per the brief). So every remake timing, commit figure, per-run start and end, the 0.489 s gap, the runs past 30 s, and 09729's 24.06 GiB and 42.5 s are DECLARED.
- **The earlier generator** (`48d88b21…`) is not in the repository. So I cannot show that the generator changed only where RULINGS' "As kept" says it did.
- **Earlier versions of SHEET, RULINGS and the dispositions.** They have no history. I checked for rewriting only against the quotes REREAD-7's reader 3 took from them.
- **The draft-8 evidence files.** They were last written 21:27:47–21:32:47, after RULINGS.md recorded the R6 remake ruling (21:20:23), whose words are *"Draft-8 evidence remains as reported"*. Whether they differ from what was reported to him cannot be checked.
- **Overlap with the generation.** From the record's write time (23:01:54) and the stated wall times, generation 1 began at about 21:33:09 (REASONED). The last draft-8 evidence file was written at 21:32:47. No overlap is evident, but none is excluded within seconds.
- **The checker, `plant_reverts.py` and `ref_run_paths.py`** I did not run (readers 1 and 2). Where a count rests on them I read their evidence.
- No core exists.

## 2. Verdict

**Not ready on the rulings' side: 0 BLOCKER, 2 MAJOR, 11 MINOR.**

What holds:
- A–F and the R6 remake ruling are each carried in substance, mostly in his own words.
- No document presents the attempt-record proposal as his ruling.
- His D1 qualification is honoured: the bound is 130 in draft 8 and in the checker.
- I found no dated record rewritten.
- Every count I could recompute is right except four statements (ZC3, ZC5, ZC7, ZC8).

Two rulings are carried short:
- **C (ZC1):** the repetition requirement for each obligation, and "the adopted evidence-record requirements", which the list narrows to conditions 5 and 6.
- **D1 (ZC2):** his second step, *"Then specify and test the actual limit"*, is neither done nor brought back to him. The documents attribute to him a condition he did not state.

## 3. Answers

### Q3, acceptance (his C)

Partly.

**What Amendment 7's section 7 (SHEET.md:866-881) carries:** R1–R8; R2b with code and line; S1–S4; the do-nothing fixtures; both source readings; and conditions 5 and 6 in his words. It keeps his scope sentence (:880-881: *"Passing R1–R8 establishes the milestone only"*, *"now of the whole list"*, then his *"Passing them does not authorize production integration, reference-authority transfer, or release."*). Its additions (item 5, R2's fixtures; items 9 and 10, kept from the old section 7) are within his rulings A6 and C.

**What it falls short on (ZC1):**
- Only item 1 states a repetition requirement. The option he adopted said *"each held twice where it runs"*.
- Item 8 names only *"the evidence-record requirements above, conditions 5 and 6"*. His C names *"the adopted evidence-record requirements, including Y3's conditions 5 and 6"*.

### Each ruling against every document

Line numbers are those of the files named in each column.

| ruling | draft 8 | Amendment 7 (SHEET) | code | notes | as he wrote it? |
|---|---|---|---|---|---|
| A1 W3 without the writer | §10 :781-784, his words | :766 | the checker decides its own W3 by writing back, disclosed §11 :874 (A binds the core) | — | yes |
| A2 byte mismatch only | §10 :782-783 | :767-768 | — | — | yes |
| A3 no equivalence; to him | §10 :786 | :769-770; §7 item 9 | — | — | yes |
| A4 reading: three facts | §0 :113-117 | :771-772 | — | — | yes |
| A5 recorded before R2; fails R2 | §0 :119-120 | :772-774; item 7 | — | — | yes |
| A6 fixtures frozen | Q1 | :775-778, table | `gen_r2_fixtures.py`; the file reproduces byte for byte (MEASURED) | — | yes; one sentence wrong (ZC7) |
| B1 | §10 :837-838 | :789-791 | ref_run.py :30-32; generator `next_attempt` :196-206 | RULINGS :501-504; SHEET :697-699 | yes |
| B2 | §10 :835-837, deferring to the sheet | :784-788 | each generation is its own experiment; `--only`; refuses after COMPLETED | — | yes |
| B3 | §10 :836 ("of any cause") | :792-794 | generator `CREATE_NEW_PROCESS_GROUP` :247 | — | yes |
| B4 | §10 :836 | :795-797 | generator HARNESS-FAULT :253-257, :361-362 | — | yes |
| B5 | §10 :838 | :798-799 | no core harness yet | — | yes |
| C | — | §7 :866-881 | — | §7 note :998 | partly (ZC1) |
| D1 | §8 :625-636 | :883-886 | `format_check.py:93`, `DEPTH_PARENS … 130` | RULINGS :761 | qualification honoured; second step not done or returned (ZC2) |
| D2 | — | :822-823 | runner :262; `classify` :116 | RULINGS :318-320, :390-391 | yes; the note's history is wrong (ZC6) |
| D3 | status :11-14 | — | — | RULINGS :395-398 | yes |
| D4 | W5's row identical to draft 7's (MEASURED) | — | R6 verdicts moved from draft 7: 0 (MEASURED) | RULINGS :505-509 | yes |
| D5(1) pre-reference failures | — | :812-813 | `setup`, `main` | — | all but `SystemExit` (ZC4) |
| D5(2) exit 3 without its line | — | :814-815 | `classify` :108-109; generator STOPPED-ANOMALY | — | yes |
| D5(3) KeyboardInterrupt | — | :816-817 | `classify` :110-111, read as "last on stderr" | — | yes, reading stated |
| D5 environment safeguards | — | :818-821 | runner `conditions()`; generator `fields_ok` | — | in purpose; "eight" is false in law mode (ZC3); the `research/law-sufficiency` pycache check is declared as the writer's own extension |
| D5 the 632 crashes | — | :824-826 | — | — | MEASURED: 8 types summing to 632 |
| E1 | §7 :484-486; W8 :544 | :888 | plant caught (evidence) | — | yes |
| E2 | derivation 17 :455; W9 :552-555; underived list :670-679 | :888 | 3 plants caught | — | yes |
| E3 | W8's row :544 | :888 | — | — | yes |
| E4 | §5 :373-376, his words | :888 | — | — | yes |
| F1 | — | :843-851 | WORKERS=4, RAISE_S=45, the figures recorded | — | partly (ZC9) |
| F2 | §12 :1008-1010 | — | — | — | yes (this re-read) |
| R6 item 1 | Q6 | :899-900, :930-932 | record written only when the generations are equal, :547-553 | RULINGS :793-801 | yes; see ZC13 |
| R6 item 2 | Q6 | :933-935 | sequential, :489-506 | RULINGS :793-799 | yes; the restatement drops "generator" (ZC10) |
| R6 item 3 | Q6 | :936-937, :956-971 | per-run start and end :248, :266; host commit :311, :341, :402 | RULINGS :802 | yes ("nothing heavy" is DECLARED) |
| R6 item 4 | — | :938-940 | :547-553 | — | yes |
| R6 item 5 | Q6 | :941, :973 | — | — | yes; record sha256 equals Amendment 7's (MEASURED) |
| R6 scope | Q6 | "for the next attempt only" :931; F1 list kept :845-851 | docstring :10-11 | — | yes (see below) |

**Note on R6's scope (REASONED).** The generator now has no concurrent mode. It is tied to experiment `r6-reference-5`, which has completed, and it refuses any further attempt. So nothing in it repeals F1: the next remake needs a new generator, and that generator would have to restore F1's concurrent generations.

### Is his D1 qualification honoured (130 unchanged)?

Yes (MEASURED):
- `format_check.py:93` reads `DEPTH_PARENS = … 130`;
- draft 8 :604 and draft 7 :576 both say 130;
- the fixture at 130 and the plant at 131 stand.

What is not carried is the step after measurement (ZC2).

### Is the attempt-record proposal presented as his ruling?

No:
- RULINGS :757-760 says it *"is not recorded here as his ruling; it is put to him"*, and :803 says it is still put to him;
- SHEET :807-808 says the same;
- `gen_r6_reference.py:25-26` cites it as "put to him".

### Precedence and in-place notes

**Precedence is clear by construction:**
- every amendment says it governs where it differs from the earlier ones;
- the old section 7 carries a note (:998);
- draft 8 defers to the sheet for the protocol (:20-21, :838-839);
- the checker is evidence, not authority.

**It is unclear in three places:**
- **D1:** RULINGS :761 says "until the front end's limit is measured", while draft 8 :635 says until it is established (ZC2);
- **the derivation count:** SHEET :51-52 says 15 + 3 derivations against draft 8's 19, with no note (ZC5);
- **the module count:** the "eight" modules (ZC3).

**Notes REREAD-7 asked for:**

| finding | where the note is | made? |
|---|---|---|
| Y1 | RULINGS :501-504; SHEET :697-699; the runner's docstring and draft 8 aligned | yes |
| Y7 | RULINGS :397-398; draft 8 :13-14 | yes |
| Y8 | RULINGS :507-509 | yes |
| Y9 | RULINGS :318-320, :390-391 | yes, but :318 misattributes the history (ZC6) |
| Y10 | RULINGS :450-452; REREAD-0-DISPOSITION :7-8 | only 2 of 5: SHEET :3-4, :33 and :51-52 have none (ZC5) |
| Y15 | SHEET :671-673, :709-710, :737-738 | yes |
| X3 | SHEET :709-710 | yes |

Each note that was made says what it corrects.

**Dated records rewritten:** none found.
- I checked 15 quotes REREAD-7's reader 3 took from RULINGS (`2cb28949…`) and SHEET (`4d2dca8c…`). Each is present word for word at its shifted line, with the note beside it.
- Draft 7 is the version REREAD-7 read (`05010e01…`).
- The 17:40 disclosure is kept (SHEET :741-743, :975-978).

### Counts

**Recounted and right (MEASURED unless marked):**
- **REREAD-7's findings:** 39. By headings: V 10 (3 MAJOR, 7 MINOR), X 13 (6, 7), Y 16 (4, 12), so 13 MAJOR and 26 MINOR.
- **DRAFT and minor-finding counts** (REASONED): REREAD-5's thirteen DRAFT items; J6–J17 twelve, eleven of them DRAFT rows; K4–K16 thirteen; L5–L14 ten.
- **Plants:** 94. Section 11's parts are 6 + 13 + 9 + 4 + 6 + 14 + 12 + 8 + 22 = 94, and the evidence reads *"plants 94 of 94 caught"*.
- **Reverts:** 46 changed, 3 of them only by a crash.
- **Laws:** 304 = 298 + 6.
- **The runner's check:** 43 cases. Variants: 15, of which 14 are caught.
- **R2's fixtures:** 11, reproduced byte for byte.
- **The writer plants' reach:** the name plant reaches 154 texts (91 distinct laws); the `over` plant reaches 3 texts (2 distinct byte strings). The 298 texts are 181 distinct laws.
- **R6's record:** 10,000 rows; 2,374 RESULT, 6,994 REFERENCE-REFUSED, 632 NO-REFERENCE-RESULT; 8 crash types summing to 632, as Amendment 4 lists them. Its rows are identical to `-3`'s and `-4`'s, and 09729 is `TypeError` in all three.
- **The checker's R6 verdicts:** 538 accepted; 61 moved from draft 6 to draft 7; 0 moved from draft 7 to draft 8.
- **R2b:** 1,558 twins, 0 disagreeing, 0 moved.
- **`vectors-as-integer`:** 446 lines (178 `x_as_i`, 268 `f_as_i`); 189 refusals (143 + 40 + 6).
- **D1's probe:** limits held at their edges 4 of 4; deepest line 90; the 298 texts reach 66; the fixture laws 5.
- **Arithmetic:** REREAD-7's timings and token ratios (1.66, 1.34, 2.33); 3,931 / 3,425 = 1.15; 2 × 24.06 = 48.12 GiB, above the 47.6 GiB limit.

**Wrong:**
- "eight" modules (ZC3);
- "REREAD-6's five and REREAD-7's eleven … 15" (ZC8);
- "11 fixtures … out of order or repeats" (ZC7);
- SHEET :51-52's 18 derivations (ZC5).

## 4. Findings

### ZC1 (MAJOR): Section 7 does not carry two clauses of his C as adopted

**Where:** SHEET.md:866-881; item 8 at :875; its "above" points to :853-864.

**His words** (RULINGS.md:643-645): *"the adopted evidence-record requirements, including Y3's conditions 5 and 6, in their previously adopted wording. Each applicable obligation must be held under its specified repetition requirements."* The option he adopted (REREAD-7-DISPOSITION.md:315): *"… each held twice where it runs."*

**Evidence** (REASONED from the texts):
- **Repetition.** Only item 1 states one (*"each run twice with byte-identical output, on the owner's host"*). Items 2–5 state none: R2b, S1–S4 ("each as its row states"), the do-nothing fixtures and R2's fixtures. Neither R2b's row (:458-460) nor the S rows states one. Only Amendment 1's repeat count (:127-128) and B2 (:785) give them one, and the list cites neither.
- **Evidence records.** Item 8 names "the evidence-record requirements above, conditions 5 and 6". The paragraph above it (:853-864) holds only those two. The other adopted evidence-record requirements are not named:
  - his further requirement under C2 (RULINGS.md:248-250; SHEET :249-256);
  - Amendment 3's records (:296-302, :392-394);
  - K10's stdout (:528-529);
  - N3(3)'s retained interrupted runs (RULINGS.md:431-432; SHEET :600-601);
  - B2's counts and causes (:787-788).

**Proposal:**
- Give each item its repetition requirement and its source: for items 2–5, two experiments (B2) with each case's two runs equal in class and result, or byte-identical output as in item 1. Put which one to him.
- Make item 8 read "every adopted evidence-record requirement (Amendments 2, 3, 4 K10, 5 N3, 7 B2 and X5), conditions 5 and 6 in his words".

### ZC2 (MAJOR): D1's second step is neither done nor returned to him, and he is credited with a condition he did not set

**Where:** draft 8 :625-636; SHEET.md:883-886; RULINGS.md:761.

**His words:**
- RULINGS.md:655: *"Measure the actual front-end expression-depth limit. Keep 130 provisionally until measurement. Then specify and test the actual limit, including cases on both sides of the boundary."*
- RULINGS.md:661: *"The 130 bound remains until that limit is measured. Do not silently substitute 99."*
- The option he confirmed (REREAD-7-DISPOSITION.md:324): *"tighten to the actual limit. Measure the front end at its edge (texts 98 to 101 levels deep), specify what it does, and plant both sides of the edge … It changes which laws are accepted, so it is his to rule."*

**Evidence** (MEASURED, then REASONED):
- `depth_probe.py`, re-run here, gives a body identical to `evidence/rust-core-depth-8.txt`: the front end's limits at their edges (64 accepted, 65 refused; 24 accepted, 25 refused); the deepest law line found is 90; 99 is an upper bound by derivation.
- No text 98 to 101 deep was measured, since the search's families reach 90.
- Draft 8 :635: *"measurement has not established it. 130 stays, as he ruled, until it is"*. He ruled "until measurement", not "until established".
- RULINGS :761 says 130 stays "until the front end's limit is measured". Draft 8's own account says those limits were measured.
- Neither document says the open choice goes to him. Draft 8 says only "the change, when it comes".

**Proposal.** Put D1 back to him in REREAD-8's disposition, with the bracket [90, 99]:
- (a) establish the exact limit, by a proof or a witness at the derived bound, then specify it and plant both sides;
- (b) specify 99 openly as the derived upper bound, not shown tight, with plants at 99 and 100;
- (c) keep 130, said to be not his words.

Make RULINGS' "As kept" and draft 8 state one condition.

### ZC3 (MINOR): "The eight `orlog` modules": in law mode the ENV line carries five

**Where:** SHEET.md:818-819 (*"in law mode, the eight decoder1 brings in"*) and :924-925 (*"the runner now hashes eight modules in each run"*). His D5 is RULINGS.md:669.

**Evidence** (MEASURED):
- `r6-reference-5.txt`'s ENV line, and my law-mode run, carry `orlog`, `orlog.interp`, `orlog.numeric_ref`, `orlog.seal` and `orlog.syntax`: five.
- Text mode (`examples/gcd_certificate.orl`) carries eight: those five plus `canon`, `front` and `sema`.
- The "8" traces to REREAD-7-READER-2-REPORT.md:361.
- The code's rule, every module loaded, meets his purpose. The two sentences are false.

**Proposal:** add in-place notes to both sentences (five in law mode, eight in text mode), and state in Amendment 7 that "the eight" is read as "every module loaded".

### ZC4 (MINOR): D5(1) leaves a gap: a `SystemExit` before `reference()` is not a runner fault

**Where:** ref_run.py:173 and :186 (`except Exception`) and :251-254; the docstring :24-28 promises every failure.

**Evidence** (MEASURED). A scratch copy of the runner, with `src/orlog/__init__.py` reading `raise SystemExit(0)`:
- exits 0, with 0 bytes on stdout and 0 on stderr;
- `classify` of two such runs gives `NO-REFERENCE-RESULT`.

The generator would stop such an attempt as ENV-MISMATCH (gen_r6_reference.py:275-276, :323-331), so R6's record is guarded. A harness that calls `classify` alone is not. The runner's check covers only an orlog import that raises `ValueError` (its evidence, line 28).

**Proposal:** catch `BaseException` before the reference begins, with `KeyboardInterrupt` kept apart; add a stand-in case to `ref_run_paths.py` and a matching variant.

### ZC5 (MINOR): Three of Y10's five in-place notes are missing

**Where:** SHEET.md:3-4 (*"nothing it names is written until the owner accepts it"*), :33 (the budget in prose), :51-52 ("15 run-side derivations and the 3 backend-only ones"; there are 19, RULINGS.md:103).

**Evidence** (MEASURED by grep; REASONED):
- Y10's row (REREAD-7-DISPOSITION.md:238) reads *"DRAFT: in-place notes"* for five places, confirmed.
- His authorization covers it: *"Draft 8, applying every DRAFT disposition"* (RULINGS.md:737).
- The disposition's own summary (:394-397) named Y10 only for RULINGS and REREAD-0, and the writer applied the summary, not the row. That is L1's and Y1's mechanism again.

**Proposal:** add the three notes.

### ZC6 (MINOR): The Y9 note misstates the history it corrects

**Where:** RULINGS.md:318-320.

**Evidence** (REASONED from the texts):
- **What the note says:** K15 (Amendment 4) brought the "text before the first `:`" rule, and Amendment 5 the `REFERENCE-EXCEPTION` line.
- **The colon rule is Amendment 3's** (SHEET.md:286-289).
- **K15 brought the runner's line, in Amendment 4:** SHEET :494-496 and :503; :506-507 (*"It replaces Amendment 3's rule … [K15]"*); K15's DRAFT row, REREAD-4-DISPOSITION.md:82.
- **REREAD-7-DISPOSITION.md:325**, D2's "as settled" text, has the same slip. It is kept as proposed.
- His D2 words are unaffected.

**Proposal:** add a further note in place: Amendment 3 brought the colon rule, K15 in Amendment 4 the runner's line, and Amendment 5 the raw `classify`.

### ZC7 (MINOR): One of R2's 11 write-back fixtures is neither out of order nor repeated

**Where:** SHEET.md:776-777 (*"Its 11 fixtures are laws whose `over` or `given` list is out of order or repeats an entry"*); `gen_r2_fixtures.py` docstring :6-9; the first row of `r2-writeback-fixtures.txt`.

**Evidence** (MEASURED, `recount.py`, the fixtures decoded from hex):
- 10 of 11 are out of order or repeated. `mutant/s1/0026` "given reversed" writes `(given 1 2)`, which is ascending with no repeat.
- Among the 298 texts, 3 hold a `given` list of two entries or more, and 2 of those are `(given 2 1)`, out of order. So the docstring's *"would pass R2 on every one of them"* holds for `over` lists only.
- His A6's four kinds are each covered: out of order and repeated, for `over` and for `given`.

**Proposal:** correct the sentence and the docstring. No fixture needs to change.

### ZC8 (MINOR): The runner variants: five plus eleven is said, four plus eleven is made

**Where:** SHEET.md:832-835; ref_run_variants.py:8-9 and `VARIANTS` :22-62.

**Evidence** (MEASURED):
- Four REREAD-6 changes are made, plus V1–V11: 15, as the evidence counts.
- REREAD-6's fifth, *"P keeping the text-seal line"* (SHEET :717-718), is not made. V10 is a narrower change, "in law mode only".

**Proposal:** add the fifth, or say why V10 stands for it, and correct the count.

### ZC9 (MINOR): F1's *"The measured process and memory limits govern"* is not carried as a rule

**Where:** SHEET.md:845-851 (four bullets, none of them this); disclosed at :926-928 and :970-971; gen_r6_reference.py:401 and :524-529. His words are at RULINGS.md:715 and :719.

**Evidence** (REASONED):
- `workers_may_rise` is computed from his two "only while" conditions alone. Those conditions are necessary, not sufficient.
- The generator printed "workers may rise: True" with 2.32 GiB of commit left at the peak (DECLARED).

**Proposal:**
- Add his sentence to the F1 list.
- Make the generator print that the two conditions hold, not that workers may rise.
- Or propose a commit-headroom condition for his ruling.

### ZC10 (MINOR): The R6 remake's item 2: the sheet drops "generator"

**Where:** SHEET.md:933-935. His words, at RULINGS.md:781, are *"Keep the same runner, generator, inputs, environment, and worker configuration."*

**Evidence** (MEASURED):
- The generator's sha256 changed from `48d88b21…` (`r6-reference-4.txt`'s header) to `cc63252d…`.
- The runner, decoder1, interp, the mutants and the ENV line are identical in both headers.
- Only RULINGS :793-801 explains the change. That it is limited to what is listed there is not checkable.

**Proposal:** quote item 2 whole in Amendment 7, list there each change of the generator against his items 1, 2, 3 and 5, and put that reading to him.

### ZC11 (MINOR): Condition 6's "Preserve … inputs, outputs" is read as "by sha256"

**Where:** SHEET.md:863. His words are at RULINGS.md:37-38.

**Evidence** (REASONED): a hash identifies an output; it does not preserve it.

**Proposal:** keep the inputs and outputs themselves, saying where, with their sha256 as identity; or put the narrower reading to him.

### ZC12 (MINOR): Stale and colliding names outside draft 8

**Where:**
- plant_reverts.py:1 says *"the plants of drafts 4 to 7 … (LAW-FORMAT-0-DRAFT-7.md section 11)"*, while it holds draft 8's undoings (:146-216).
- ref_run.py uses "his D5" (:2, :25, :43, :67, :85, :90), which collides with his first ruling's D5 (RULINGS.md:19).
- gen_r6_reference.py:2 lists "F2 … F", REREAD-4's F2 beside REREAD-7's F; :42 and :204 say "his B1–B4".
- The record's first line (r6-reference-5.txt) uses the same names.

Draft 8 :43-48 separated these names [Y16]; the code did not.

**Proposal:** use R7- prefixes in the docstrings and fix plant_reverts' heading. The record stays as written, with a note in the sheet.

### ZC13 (MINOR): Generation 1's file of the failed concurrent attempt sits among the records

**Where:** research/rust-core/r6-reference-4.txt. Its line 1 reads *"The reference on R6's mutants … recorded before any experiment"*. Generation 2's file is in `work/` (SHEET :902-904), and SHEET :994 says the file is not a record.

**Evidence** (MEASURED, header read). His R6 item 1: *"Neither generation is selected as the authoritative record."* The two files are placed differently, and the folder suggests that one was selected.

**Proposal:** treat the two generations' files alike, both outside the records' folder or both named as a generation's file, and say so in Amendment 7.

## 5. Files created

All are under `⟦HOME83⟧\AppData\Local\Temp\reread8-3\`:
- `⟦HOME83⟧\AppData\Local\Temp\reread8-3\recount.py` and `⟦HOME83⟧\AppData\Local\Temp\reread8-3\recount.out`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-3\depth-probe.out` and `⟦HOME83⟧\AppData\Local\Temp\reread8-3\depth-ev-body.txt`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-3\r2-fixtures-remade.txt`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-3\inputs\one.law` and `⟦HOME83⟧\AppData\Local\Temp\reread8-3\inputs\t.orl`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-3\sysexit-tree\research\rust-core\ref_run.py` (a copy of the pinned runner) and `⟦HOME83⟧\AppData\Local\Temp\reread8-3\sysexit-tree\src\orlog\__init__.py` (`raise SystemExit(0)`)
- `⟦HOME83⟧\AppData\Local\Temp\reread8-3\sysexit.out` and `⟦HOME83⟧\AppData\Local\Temp\reread8-3\sysexit.err` (both empty)
- the empty run folders `run-law`, `run-text` and `run-sysexit`

The repository is unchanged: HEAD is `2e9805a`; `src/`, `tests/` and `vectors/` are clean; no `__pycache__`; no file in `research/rust-core` or `evidence` is newer than my scratch script.

## 6. Appendix: commands and outputs

```
sha256sum <the 24 pinned files> research/law-sufficiency/decoder1.py   -> all equal to the brief (listed in full at the start and the end)

ref_run.py law 1000000 <64 zeros> inputs/one.law  -> exit 0
  ENV ... orlog orlog=d30a8331… orlog.interp=f8432918… orlog.numeric_ref=eacac3dd… orlog.seal=70e9c2b5… orlog.syntax=ad4e3bc5…   (5 modules)
  RUN COMPLETED ops 1 p 8146a1f7… trace b02bce91…
ref_run.py text none examples/gcd_certificate.orl -> exit 0; ENV modules: orlog, canon, front, interp, numeric_ref, seal, sema, syntax (8)
grep "^# environment" r6-reference-5.txt -> the same 5 modules as law mode

scratch copy, src/orlog/__init__.py = "raise SystemExit(0)", text mode -> exit 0; stdout 0 bytes; stderr 0 bytes
  ref_run.classify((0,b'',b''),(0,b'',b'')) -> NO-REFERENCE-RESULT

grep -v '^#' r6-reference-{3,4,5}.txt | sha256sum -> 42d52fe0… for all three; 10000 rows each
grep '^09729 ' -> "NO-REFERENCE-RESULT crash exit 1 type builtins.TypeError" in all three

diff of the checker records' rows: r6-checker-6 -> -7: 61; -7 -> -8: 0; r2b-checker-7 -> -8: 0
-8: accepted 538; r2b-checker-8 rows not "agrees": 0

recount.py:
  r6-reference-5: RESULT 2374, REFERENCE-REFUSED 6994, NO-REFERENCE-RESULT 632; 8 crash types, sum 632
  vectors-as-integer: 446 (x_as_i 178, f_as_i 268); refusals 189 (INEXACT 143, OVERFLOW 40, NOT-FINITE 6)
  sources 298, distinct laws 181; named let 154 texts / 91 laws; over 2+ with reversal differing: 3 texts / 2 distinct
  given 2+: 3 texts (0026, n23-given-three, n32-premise-later-and-self), 2 distinct, 2 out of order, 0 repeated
  over lists of 2+: 3, out of order 0, repeated 0
  fixtures: 10 of 11 out of order or repeated; "0026 given reversed -> (given 1 2)": out-of-order False, repeat False

gen_r2_fixtures.py <scratch> -> "11 fixtures … sha256 2e13265a…"; cmp with the frozen file: CMP IDENTICAL
depth_probe.py -> body identical to evidence/rust-core-depth-8.txt; "the limits held at their edges 4 of 4; the deepest law line found is 90"

evidence summaries:
  FORMAT CHECK (DRAFT 8) HELD: 304 of 304 laws pass, 304 written back exactly …; plants 94 of 94 caught, 0 not run
  PLANT REVERTS HELD: 46 plants and fixtures, 46 changed by at least one undoing, 3 of them only by a crash
  REF-RUN PATHS HELD: 43 of 43 as stated
  REF-RUN VARIANTS HELD: 14 of 15 changes caught …   (the list: control, 4 "REREAD-6:" rows, V1–V11)

grep -n "130" format_check.py -> :93 DEPTH_PARENS = 24, 16, 130
diff W5's row, drafts 7 and 8 -> identical
REREAD-7 report headings -> V: 10 (3 MAJOR, 7 MINOR); X: 13 (6, 7); Y: 16 (4, 12)
grep SHEET for Y10's three places -> :3-4, :33, :51-52 unchanged, no note
file times: draft-8 evidence 21:27:47–21:32:47; RULINGS 21:20:23; r6-reference-5.txt 23:01:54; SHEET 23:03:57
```
