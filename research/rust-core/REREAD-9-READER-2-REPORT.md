# REREAD-9, reader 2 of 3: the protocol, the runner, and the evidence and its keeping, its report word for word (2026-10-31)

Saved as returned by the reader, a fresh general-purpose agent with no part in writing anything it read. REREAD-9 ran
as three readers working at the same time, under the owner's authorization (RULINGS.md, "REREAD-9 authorized"):
reader 1 the format, the checker and the 91 challenge; reader 2 the protocol, the runner, and the evidence and its
keeping, with the hash closure; reader 3 the rulings and cross-document consistency. Each started fresh, had its own
scratch folder and its own letter for findings (NA, NB, NC), and saw nothing of the others' work.

**Its brief** is `work/rust-core/reread-9/briefs/brief-2.md`, sha256 `f440f842b3eb0b476455b68c81010203da8b4c24193936d49dc070de7984ec91`, kept in `kept/`; the reader was given only
its path and sha256, and told to check the hash before following it. The brief pinned 34 files by sha256, among them
draft 9 (`86716702…`), SHEET.md (`883888d7…`, Amendments 8 to 12) and RULINGS.md (`f8bc6d6f…`), and told the reader:
- never to open, read, list or grep anything under `research/law-sufficiency/`;
- to change nothing in the repository, in the owner's words *"Do not change the checker, runner, reference, laws,
  gate, or release files"*, and to run git read-only;
- to write only under its own scratch folder, run at most two processes of its own at once, never run mutant 09729
  through the reference, and write no absolute path or account name in its report.

No pinned file changed while the readers worked (`work/rust-core/reread-9/record.jsonl`, append-only, kept in
`kept/`). Its report follows, unedited, taken from its own transcript rather than retyped.

---

**REREAD-9, reader 2 of 3: the protocol, the runner, and the evidence and its keeping (findings NB1–NB13)**

Brief: `work/rust-core/reread-9/briefs/brief-2.md`, sha256 `f440f842b3eb0b476455b68c81010203da8b4c24193936d49dc070de7984ec91`. I checked it before reading and again at the end.

## 1. What I read and ran, and what I could not check

**Pins.** All 34 pinned files had their stated sha256 before I read them, and again after my last run (34 of 34). HEAD is `2e9805a…`. src/, tests/ and vectors/ are unchanged: `GIT_OPTIONAL_LOCKS=0 git status --porcelain --untracked-files=all -- src tests vectors` prints nothing.

**What I read**
- SHEET.md: sections 1–7 and Amendments 1–12. Amendments 7–12 and section 7 I read line by line.
- RULINGS.md, from "RUST-CORE-0 accepted" through "What follows".
- REREAD-8-DISPOSITION.md and the ruling sheet, each whole.
- Draft 9: its status, lines 104–119, 589 and 905–915.
- The first sections of the two W9 verification reports.
- Read whole: ref_run.py, ref_run_paths.py, ref_run_variants.py, run_format.py, gen_r6_mutants.py, gen_r2b_twins.py, kept_evidence.py, kept_tokens.py, kept_tokens_plants.py, and both manifests.
- gen_r6_reference.py: its docstring and lines 140–561.
- r6-reference-5.txt: its header, and all 10,000 rows by script.
- The runner's two -9-zb records whole, and the other records by diff and hash.
- In work/rust-core: the run logs, superseded/, zb3-old-check.txt, provenance/kept_plants.py, kept-plants-run1.txt and regen_gen48.py.

**What I ran.** Every Python run was `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B`, from the repository's root, with TEMP and TMP set to `<scratch>`. Appendix A lists the commands and outputs.
- `kept_evidence.py check`; `kept_tokens.py check` with no prefixes; `kept_tokens_plants.py`, twice.
- `ref_run_paths.py`, twice.
- `ref_run_variants.py`'s own `main()` and `one()`, with each copied check run one at a time, twice (see the next paragraph).
- The two `--checker` tools, each twice.
- Eleven changes to copies of the runner that its docstring forbids, each run against the check and each with a demonstration.
- Probes, all in scratch:
  - the hash closure of the sha256 values stated in Amendments 8–12;
  - r6-reference-5.txt against its header;
  - two mutants of kept_tokens.py run against its plants;
  - the token adjacency, the extra-NAME and the home-path questions;
  - one damaged byte in each kept file, in a copy of the kept folder;
  - a bytecode cache placed by PYTHONPYCACHEPREFIX;
  - a sitecustomize that raises the recursion limit.

**How I kept to two processes.** ref_run_variants.py runs three copies of the check at once, each with its own child: six or seven processes. I did not run it that way.
- A script of mine imported it and replaced only `subprocess.run` (and the naming and removal of its temp folder).
- Its own `one()` wrote all 21 copies.
- A shell then ran each copied check alone (the check plus its child), in two full passes.
- Its own `main()` then printed from each pass's saved results. That output is the record's body, byte for byte (Q4).

No process failed to start, and WinError 1450 never appeared.

**What I could not check**
- The six tokened originals: the prefixes are not given. So the 16 real-file rows of the plants (39 less 23) were not run.
- The pre-ZB3 check (`87d93a49…`) and the other superseded versions no file holds (NB9). Amendment 12's runs against the old check rest on its output file alone.
- Amendment 7's host figures. These were not asked, and 09729 was never run.

**Disclosures**
1. One `find` for repository files newer than my first scratch file walked `work/rust-core/reread-9/`. My closure script's directory walk listed that folder's entries and skipped them. Neither printed a name or read a file there; the `find` printed only the count 0. Later checks pruned the folder.
2. A search for Q5 printed five lines of `REREAD-8-READER-2-REPORT.md`, which is not among my pinned files. I did not open it.
3. My demonstrations ran the unchanged runner, and copies of it, on made-up laws of 0 to 2 operations and on stand-in decoders, as ref_run_paths.py itself does. I ran no R6 mutant.
4. One probe imported format_check with `research/law-sufficiency` on sys.path, as the `--checker` tools do, and printed one boolean.

## 2. Verdict

- **The runner and its check.** The runner is unchanged and pinned at `822c826e…`. The check holds the three points Amendment 12 states. Its record and the variants' record reproduce byte for byte. The counts are as recorded: 46 of 46; 15 of 16 with V11 not caught; ZB3's four plants caught and counted apart. The check writes nothing in the repository. (MEASURED)
- **What the check does not hold.** It does not hold the runner's own prohibitions. Eleven changes the runner's docstring forbids pass it 46 of 46, and each is shown doing what it does (NB5, NB6). Its comparison is relative to the interpreter and environment it runs in (NB7).
- **Section 7.**
  - Every item has a repetition requirement.
  - It does not name every adopted evidence-record requirement (NB1, MAJOR).
  - It asks for one record a conforming core cannot make (NB2, MAJOR).
  - It applies ATTEMPT-RECORD-0 beyond his scope (NB3).
  - It does not say whose runs byte identity covers (NB4).
- **The evidence kept.** It is exactly what the manifests name: 48 of 48 recovered, and 6 of 6 intact. Amendments 9's and 10's records are kept at their stated sha256. No kept file, compressed or decompressed, holds the home folder's path in any spelling. The keeping tools have edges:
  - a damaged kept file can make a check raise instead of report (NB12);
  - the token plants never reach the sha256 comparison (NB10);
  - two tokens side by side can restore with two wrong prefixes (NB11). No real kept file has two side by side.
- **Count.** 13 findings: 0 BLOCKER, 2 MAJOR, 11 MINOR.
- **Hash closure: passed.** Every stated sha256 of a file that exists holds, and the four records reproduce. 18 statements name versions no file holds (NB9).

## 3. Answers

### Q1: the runner's check (his ruling on ZB3 and ZB5)

**Amendment 12's three points hold (MEASURED, and the code read).**

- **The ENV and after-run lines.** The check builds them itself, whole (`ref_run_paths.py:170-186`):
  - the implementation, version and platform come from a fresh `python -B` with the same environment, in a fresh empty folder (`:147-154`);
  - the recursion limit is that interpreter's default (`:301-302`);
  - then `format_check not-imported`;
  - then exactly the orlog modules a fresh import of the runner's setup loads, each by its file's sha256: 8 for a text, 5 for a law, 5 under a stand-in decoder1.

  A run that reaches the reference must print the ENV line first, and an exit-0 run must print the after-run line last but one (`:344-349`).
- **Three bytecode cases**, one for each folder the runner's docstring names (`:296-298`, `:322-330`). Each is a copy of the runner whose root is a folder the check makes; the cache stands in one folder, and the fault must name it. The fourth-folder case stays (`:315-321`).
- **The implementation, version and platform** are compared as part of the whole ENV line. That is what catches X3 and X4.
- **One limit on "whole".** Each line is checked whole, but the check does not require that these be the only lines before the outcome. K1 passes with an extra line between them.

**The runner is unchanged and pinned (MEASURED).** Its sha256 `822c826e…` equals Amendment 7's table, r6-reference-5.txt's header, and the -9-zb records' headers (16 hex). The check itself runs whatever ref_run.py stands (`:47`) and never verifies its sha256. The pin rests on the records' headers (REASONED).

**Changes that break it.** Each is a copy of the runner outside the repository, run against a copy of the check made exactly as `one()` makes one. Every change passed the check 46 of 46 (MEASURED).

| change | the runner's words it breaks (`ref_run.py`) | what the demonstration showed (MEASURED) |
|---|---|---|
| K1: reads a clock; prints a line between ENV and CONDITIONS | "reads no clock"; "stdout holds two lines of conditions" (:48, :34) | two runs' stdout differ (`WALL <perf_counter>`) |
| K2: BUDGET from `getattr(<alias of os>, "environ")` | "no environment variable" (:48) | with REF_BUDGET=0, the completing law gives `RUN STOPPED ops 1` |
| K3: recursion limit set to 100000 for the reference, then put back | "sets no recursion limit" (:48) | the reference ran at 100000; the ENV and after-run lines read 1000 |
| K4: format_check loaded under the alias `fc_alias` | "never imports format_check" (:48) | format_check.py was loaded; the conditions lines read `not-imported` |
| K5: loads `orlog.canon` in law mode and leaves it out of the conditions lines | "every `orlog` module loaded" (:37) | canon was loaded; the lines list the five |
| K6: makes the after-run line before the reference runs | "after the reference has run, CONDITIONS after-run" (:38) | a module loaded during the run is missing; the unchanged runner lists it |
| K7: ignores TEXTSEAL in law mode | `law BUDGET TEXTSEAL PATH`; `--files` writes the receipt (:8, :11-12) | the receipt's `text-seal` is zeros, not the given seal |
| K8: ignores `--files` in law mode | the same sentence (:11-12) | the run leaves nothing; the unchanged runner leaves three files |
| K9: a text-mode stop reports one operation more | `RUN STOPPED ops <n>` (:17) | text mode, budget 0: `ops 2` where the reference stops at 1 |
| K10: classify takes a crash and a timeout as NO-REFERENCE-RESULT | classify's classes (UNSTABLE: "a crash and a timeout", SHEET.md:287) | NO-REFERENCE-RESULT; the unchanged runner gives UNSTABLE |
| K11: BUDGET's pattern ends with `$` instead of `\Z` | "a canonical decimal: digits only" (:10) | budget `5` followed by LF is taken; the unchanged runner gives RUNNER-FAULT |

Why each passes (REASONED from the code, and confirmed by the runs):
- The source rows look only at Name, Attribute and Import nodes, and at `getattr` whose first argument is literally named os or sys (`:189-209`).
- The conditions lines are compared with lines a fresh import makes, not with what the run did.
- Every law case passes TEXTSEAL as 64 zeros (`:240`).
- The `--files` cases are text mode only (`:357-359`).
- The text-mode stop's outcome line is not computed (`:259`).
- No made-up case pairs a crash with a timeout (`:370-383`).
- No case has a BUDGET with a trailing LF (`:268-273`).

**The variants' counts are as recorded (MEASURED).**
- Control: 46 of 46.
- 15 of 16 caught; V11 not caught.
- ZB3's plants: X1 34/46, X2 44/46, X3 32/46, X4 34/46. They are counted apart, and the record reads `ZB3'S PLANTS HELD: 4 of 4 caught`.
- The record reproduces byte for byte (Q4).

Amendment 12's figures against the old check (43/43, 41/43, 40/43) match `zb3-old-check.txt`. That the old check was `87d93a49…` is DECLARED; the file itself is not kept (NB9).

**The check writes nothing in the repository (MEASURED).**
- After all my runs, no repository file is newer than my first scratch file.
- There is no `__pycache__` in src/, research/rust-core/ or evidence/.
- The real runner, run some 200 times by the check, never faulted on a `__pycache__` in research/law-sufficiency.

**His words "against the runner's own recorded environment".** Amendment 12 reads them as "against a fresh interpreter". The disposition's proposal had said "with its own" (REREAD-8-DISPOSITION.md:165). Read instead against r6-reference-5.txt's recorded line, the check would also hold today: the runner's law-mode ENV line now equals that line, all 492 characters (MEASURED). The two readings part only when the environment changes (NB7).

### Q2: acceptance and the evidence kept (his I)

**Repetition (REASONED, from SHEET.md:1053-1080).** Every item has an explicit requirement:
- items 1–5: two experiments, with byte-identical output;
- items 6 and 7: made once, and again on any change of the source;
- item 8: kept for every run of items 1–5, in each of its two experiments;
- item 9: in each of the two experiments of its prediction;
- item 10: once, before the milestone is claimed.

Byte identity is defined, but the text does not say whose runs it covers (NB4).

**Every evidence-record requirement named: no (NB1).** One named requirement cannot be met by a core run (NB2). ATTEMPT-RECORD-0 is named beyond his scope (NB3).

**Inputs and outputs kept losslessly: yes, as a rule** (item 8's last bullet), and the mechanism works (MEASURED):
- `kept_evidence.py check` reads `KEPT EVIDENCE HELD: 48 of 48 files recovered exactly; 4453965 bytes kept in 955049`. Every source still stands, with the same bytes.
- My own check agrees on each kept file's sha256 and decompressed bytes.
- Each kept file is its content re-compressed by gzip at level 9 with no timestamp (48 of 48).
- No file in kept/ is missing from both manifests, and the manifest holds 48 distinct paths.
- Amendment 8's first 29 files total 4,314,387 bytes, kept in 925,357, as it states.

**The superseded records (MEASURED).**
- Amendments 9's and 10's records, kept from `work/rust-core/superseded/`, each have the sha256 their amendment states.
- Successive versions differ only in the draft's sha256 in the header, and in the format record's draft line. So Amendment 9's, rebuilt from Amendment 10's, are by their sha256 the bytes Amendment 9 fixed.

**The current records (MEASURED).**
- The -9 records carry Amendment 11's sha256 (`e4f3aa0d…`, `c46dce78…`, `0e6627df…`, `98f92a44…`, `147a12db…`).
- The -9-zb records carry Amendment 12's (`5afc2486…`, `3d2b39bb…`, `b2a7d0b5…`, `0c44460d…`, `d23da015…`). They differ from the -9 records only as Amendment 12 says; the 43 earlier paths rows are unchanged.
- The -9 checker records carry Amendment 9's (`b206c8b2…`, `59b26346…`) and reproduce.

The edges are NB12 and NB9.

### Q3: the six files (his option (c))

**Runs (MEASURED).**
- The plants, without real sources: 23 of 23 as stated, twice, byte-identical. The recorded 39 include 16 rows on the real files, which need the prefixes.
- `check` without prefixes: `TOKENED EVIDENCE HELD: 6 of 6 intact (originals not checked)`.

**What the plants cover**
- **Every spelling: in part.** Five made-up spellings are planted. The real files' REL83 and SLUG shapes appear only in the real-file rows, which I could not run.
- **Partial matches: yes.** Shorter names, a missing separator, and prefixes inside longer paths.
- **Multiple occurrences: yes.** At least three of each spelling, and a spelling beside itself. Never two different spellings side by side, although the fixture's docstring says so (0 pairs; MEASURED).
- **Missing prefixes:** 5 rows. **Extra:** 1. **Wrong:** 5, plus 2 cross-spelling. **Ambiguous:** 2.
- **But every wrong input changes the prefix's length.** A kept_tokens.py whose `restore` compares the length alone still passes all 23 (mutant m1; MEASURED). No plant reaches the sha256 comparison (NB10).

**Could a restoration pass with a wrong prefix?**
- **On a made-up file, yes.** In `before ⟦HOME_FWD⟧⟦HOME⟧ after`, two wrong prefixes (one byte moved across the boundary between the tokens) restore the exact bytes, sha256 included (MEASURED).
- **On the six real files, no.** No two tokens stand side by side in them (MEASURED). The bytes between tokens are not periodic, so no shift between two prefixes can compensate (REASONED). A single wrong prefix always changes the bytes, and the sha256 comparison refuses it (REASONED; no plant exercises this).
- **`check` given a NAME no kept file holds** still reads HELD (MEASURED; NB11).

**The home folder's path: in no kept file (MEASURED).**
- I read 110 views (each file as stored and, for .gz files, decompressed): 155,040,980 bytes.
- 10 needles: the account name, its parts of four letters or more, the 8.3 short form and its stem, each in UTF-8 and UTF-16, matched without case. 0 hits.
- None either in the scripts, the sheet or the rulings.

### Q4: the hash closure

**Stated sha256 values (MEASURED; my `closure.py`).** Amendments 8–12 make 54 full statements: 52 table rows and 2 inline.
- 36 of them name a file that exists, and all 36 hold: 26 against the files as they stand, and 10 against the superseded copies, which are kept.
- 18 name versions no file I can read holds (NB9):
  - Amendment 8's draft 9, format_check, plant_reverts, run_format and MANIFEST, its five -9 records, and its two checker records (those two stated twice);
  - Amendment 9's draft 9 and MANIFEST;
  - Amendment 10's draft 9;
  - Amendment 11's draft 9.
- Of the short forms, `822c826e`, `2965ed15`, `922e31c3`, `cc63252d` and `48d88b21` hold. `87d93a49` (the pre-ZB3 check) is held by no file.

**Reproductions (MEASURED).** Each record was written to `<scratch>/repro/`, with the header built by run_format.py's own expressions.

| record | what I made | the record | |
|---|---|---|---|
| `rust-core-ref-run-paths-9-zb.txt` | two runs exit 0, identical; `0c44460d…` | `0c44460d…` | EQUAL |
| `rust-core-ref-run-variants-9-zb.txt` | two passes exit 0, identical; `d23da015…` | `d23da015…` | EQUAL |
| `rust-core-r6-checker-9.txt` | twice `b206c8b2…` | `b206c8b2…` | EQUAL |
| `rust-core-r2b-checker-9.txt` | twice `59b26346…` | `59b26346…` | EQUAL |

**r6-reference-5.txt (MEASURED).**
- The six sha256 values its header names, and the five ENV module hashes, equal the files as they stand. decoder1 was checked by `sha256sum` only.
- The class counts equal the rows: 632, 6,994 and 2,374.
- The rows equal r6-reference-3's and r6-reference-4's. They differ from r6-reference-4's kept generation 2 at 09729 alone.

### Q5: ATTEMPT-RECORD-0 and the next generator

**Recorded as requirements, and nowhere presented as built (MEASURED by search and reading).**
- The six points are recorded whole at RULINGS.md:816-824. Amendment 8 states them as a rule (SHEET.md:1140-1142), and item 8 names them (:1075).
- The next generator's duties appear as requirements, never as built:
  - K at SHEET.md:1123-1125;
  - ZB1, ZB6, AR-1, AR-2 and K at :1224-1227;
  - ZB1's note at :809-811;
  - RULINGS.md:838-840 and :972-974;
  - REREAD-8-DISPOSITION.md:131, :163, :168, :188-189 and :301;
  - the ruling sheet, lines 162 and 165.

**The present generator lacks each one (REASONED, from the code read):**
- a child process starts at gen_r6_reference.py:295, before `Attempt` at :313 (ZB1);
- a harness exception is kept by its type alone (:362; AR-1);
- the start-failure count is taken from the one stop kept (:398-399; ZB6);
- the environment it records has no PYTHONUTF8 (:305-307; AR-2);
- `workers_may_rise` reads only the time and start conditions (:401; K).

Its pinned docstring's "written before any child process starts" is corrected by the sheet's note. It is not presented as ATTEMPT-RECORD-0.

**One caveat:** NB3.

## 4. Findings

**NB1 (MAJOR): section 7's item 8 does not name every adopted evidence-record requirement.**
- **Where.** SHEET.md:1067-1076, against the requirements it leaves out:
  - a. Amendment 4's per-case record of an R6 adjudication (:441-445, his F2 at RULINGS.md:354: *"Record the reader's determination and the exact applicable rule and diagnostic"*), and its rule that the record says only that the two readings agree (:451-454);
  - b. Amendment 6's runner-fault record: every run made, and the fault by its line, case and run (:691-694);
  - c. B1's record of a fault's identity, its line and exit status (:796-797; RULINGS.md:598);
  - d. B4's kept error and records (:801-803; RULINGS.md:623);
  - e. B5's recorded build wall time (:804-805; RULINGS.md:627);
  - f. Amendment 2's per-case evidence: the exit status, the stderr line and the files written (:255-257). Item 8 names Amendment 2 by its class words alone.
- **Evidence (REASONED).** The list is ASK I(a)'s enumeration (REREAD-8-DISPOSITION.md:244), which already left these out. His I asks that *"Every adopted evidence-record requirement is named, not merely conditions 5 and 6"*, and Amendment 8 calls the list complete. ATTEMPT-RECORD-0's points 5 and 6 may cover (b) to (d), but not (a), (e) or (f).
- **Proposal.** Name each in item 8 by its amendment, in its adopted words, as a correction implementing his I, for him to confirm.

**NB2 (MAJOR): a core run cannot make the environment record item 8 requires of it.**
- **Where.** Item 8 requires, for every run of items 1–5, *"its environment as its own process reports it"* (SHEET.md:1069-1070). This comes from Amendment 3: *"The environment is recorded by each run's own process: `platform.platform()`…"* (:304-305), where a run is any core run or reference run (:300).
- **Evidence (REASONED).** A conforming core cannot do this:
  - it reads no environment variable (draft 9:113);
  - anything on its stdout is CORE-FAULT (K10, :531-532);
  - a stderr line that is not its row's is CORE-FAULT (:205).

  So item 8 cannot be met as written, unless someone reads "own process" as "the harness", which nobody has ruled.
- **Proposal.** Put a wording to him: reference runs report their environment through their own process, as the ENV line does; for core runs, the harness records the host's platform and the build's `rustc -vV` beside each run (condition 6), never through the core's own output.

**NB3 (MINOR): item 8 applies ATTEMPT-RECORD-0 beyond his scope.**
- **Where.** SHEET.md:1075, against RULINGS.md:814: *"every remaining LAW-FORMAT-0 Phase 0 experiment attempt, not automatically to every future harness"*. Amendment 8 itself states that scope (:1140-1142).
- **Evidence (REASONED).** Items 1–5 are the core's conformance runs (phase 2, section 5), not Phase 0 attempts.
- **Proposal.** Put to him whether the milestone's experiments take ATTEMPT-RECORD-0, and mark the bullet as proposed until he rules.

**NB4 (MINOR): section 7 does not say whose runs byte identity covers.**
- **Where.** SHEET.md:1056-1058.
- **Evidence.** The experiment runs the reference again, twice, and those runs decide (:519-520). The reference's crash type on 09729 depends on free memory: TypeError in one generation, MemoryError in the other (:920-934, :992-995; MEASURED there). His ruling says *"byte identity is the acceptance condition"* (RULINGS.md:792). If the reference's runs are covered, R6 can fail byte identity on the reference's account. (REASONED)
- **Proposal.** State whose output item 1 covers. If it covers the reference's, say how 09729 is scheduled (alone, as in r6-reference-5). For him to rule.

**NB5 (MINOR): the check does not hold the runner's prohibitions (K1–K6).**
- **Where.** ref_run_paths.py:189-209 and :344-349, against ref_run.py:34-38 and :48.
- **Evidence.** See the Q1 table. Each change passes 46 of 46 and is shown working (MEASURED).
- **Proposal** (a runner-check change, his to rule):
  - require exactly the ENV line, the after-run line and the outcome on stdout;
  - ban the constant strings `environ`, `setrecursionlimit` and `format_check`, as well as the clock and dynamic imports;
  - check the conditions from inside the run, with a stand-in that reports the recursion limit and `sys.modules`, as my demonstration does.

**NB6 (MINOR): paths no case of the check reaches (K7–K11).**
- **Where.** ref_run_paths.py:240, :259, :268-273, :357-359 and :370-383.
- **Evidence.** These paths matter:
  - R5, S2, S3 and the do-nothing fixtures rest on the reference's text-mode stops (K9);
  - R4 compares the trace files that `--files` writes (K8);
  - Amendments 3 and 4 make a crash and a timeout UNSTABLE (K10).

  The pinned runner handles each correctly: the stops share one code path (:225-230), and classify is right at :123 (REASONED).
- **Proposal.** Add cases:
  - a text stopped at budget 0, with its outcome computed;
  - law mode with `--files` and a non-zero TEXTSEAL, with the receipt held to the interpreter's;
  - a made-up crash plus timeout;
  - BUDGET `5` followed by LF.

**NB7 (MINOR): the comparison is relative to the environment the check runs in.**
- **Where.** ref_run_paths.py:147-154 and :301-302; ref_run.py:163-165; SHEET.md:1354-1355.
- **Evidence (MEASURED).**
  - With a sitecustomize raising the recursion limit, the unchanged check holds 46 of 46 while every ENV line reads `recursion-limit 5000`. r6-reference-5 records 1000 as "the default", and Amendment 2 asks for *"Python's default recursion limit"* (:184).
  - With PYTHONPYCACHEPREFIX set, the unchanged runner ran a planted bytecode file for orlog/__init__.py: its stderr printed `PLANTED`, the run ended `RUN COMPLETED`, and the ENV line was unchanged. The bytecode check looks only for `__pycache__` folders, and the ENV line hashes the source files, not what runs.
- **Proposal.** For him to choose:
  - also compare against r6-reference-5's recorded line (it passes today);
  - have every harness record `sys.pycache_prefix`, `sys.flags` and the PYTHON* variables (AR-2 does this for the next generator);
  - meanwhile, say in the sheet that the check is relative to its environment.

**NB8 (MINOR): Amendment 8's J does not carry the harness rule of the option he took.**
- **Where.** SHEET.md:1106-1118, against REREAD-8-DISPOSITION.md:264. Option (b) reads: *"Any harness that classes runs, the core's included, refuses a run without the runner's ENV line, as the generator does."*
- **Evidence (REASONED).** Without that rule, a `SystemExit` raised while the modules import is classed NO-REFERENCE-RESULT (:1110-1111). His words: *"No silent reclassification."*
- **Proposal.** Record the sentence as a requirement of every harness that classes runs, or ask him whether it was adopted with (b).

**NB9 (MINOR): inputs of the standing evidence are not kept.**
- **Where.** SHEET.md:1148-1162, :1243, :1249, :1290, :1330, :1363-1365 and :1379-1384; W9-VERIFICATION-REPORT.md:20; W9-VERIFICATION-REPORT-2.md:34; work/rust-core/zb3-old-check.txt:1.
- **Evidence (MEASURED).** No readable file holds:
  - the pre-ZB3 check, `87d93a49…`. Amendment 12 measured against it "from a copy taken before the change", but that copy is nowhere;
  - the scripts that made the standing -9 records: ref_run_paths `87d93a49…`, ref_run_variants `b85295dc…` and run_format `7dab3af7…`;
  - four recorded draft-9 versions;
  - the two draft versions the verifiers read, `5880ca54…` and `d86a2aeb…`.

  `zb3-old-check.txt` has no header naming what it ran. Under his I, a hash does not replace the file.
- **Proposal.** Keep what still exists. Rebuild what can be rebuilt, as was done for `48d88b21` (exact sha256 only). Say in the sheet which versions stand by their hash alone. Give the old-check record a run_format header.

**NB10 (MINOR): the token plants never reach the sha256 comparison.**
- **Where.** kept_tokens_plants.py:88 and :140; kept_tokens.py:158.
- **Evidence (MEASURED).** Every wrong prefix in the plants changes the length. Mutant m1, whose `restore` compares the length alone, passes 23 of 23.
- **Proposal.** Plant a wrong prefix of the same length (one character changed) for each spelling, and the two-token compensation, each to be refused by sha256 alone.

**NB11 (MINOR): condition 5 has open corners.**
- **Where.** kept_tokens.py:17-18 and :174; kept_tokens_plants.py:47.
- **Evidence (MEASURED).**
  - Two tokens side by side restore exactly with two wrong prefixes.
  - `check` drops a NAME no kept file holds, and reports HELD.
  - The fixture's claim "adjacent … to the others" is false: 0 pairs.
- **Proposal.**
  - `make` refuses two tokens side by side, or the manifest records each token's offsets.
  - `check` refuses an unheld NAME.
  - Correct the fixture, or its docstring.

**NB12 (MINOR): a damaged kept file can make a check raise instead of report.**
- **Where.** kept_evidence.py:78-82, whose comment says *"reported, never a crash"*; kept_tokens.py:178-182.
- **Evidence (MEASURED).** Flipping the middle byte of each kept file, in a copy:
  - kept_evidence's check raises `zlib.error` for 10 of the 48 files;
  - kept_tokens' `check` without prefixes raises `gzip.BadGzipFile` on a damaged file.
- **Proposal.** Check the kept file's sha256 before decompressing. Catch `zlib.error` and `BadGzipFile`. Plant damage that raises `zlib.error`.

**NB13 (MINOR): `gen_r2b_twins.py --checker` does not refuse a moved HEAD or a changed tree.**
- **Where.** gen_r2b_twins.py:26-29, whose docstring says *"It refuses to write if HEAD is not the starting commit"*, against :210-213, where `checker()` makes no such check. gen_r6_mutants.py:227 does make it.
- **Evidence.** REASONED from the code.
- **Proposal.** Note it in the sheet, as was done for ZB7's docstring. r2b-twins.txt's header pins the tool, so the tool stays as it is.

## 5. Files I created (all under `<scratch>/`)

- **Scripts:** `pins.txt`, `closure.py`, `r6ref.py`, `record.py`, `variants_seq.py`, `breaks.py`, `kt_probe.py`, `mutate_kt.py`, `kt_damage.py`, `ke_probe.py`, `env_probe.py`, `small.py`.
- **Outputs:**
  - `closure.txt`, `r6ref.txt`;
  - `kept-evidence-check.txt`, `kept-tokens-check.txt`;
  - `ktp1.txt`, `ktp2.txt`, `ktmut-m1-length-only.txt`, `ktmut-m2-kept-sha-unchecked.txt`;
  - `kt-probe.txt`, `ke-probe.txt`;
  - `breaks-demo.txt`, `breaks-demo2.txt`;
  - `site-paths.out`.
- **Rebuilt records** in `repro/`: `rust-core-ref-run-paths-9-zb.txt`, `rust-core-ref-run-variants-9-zb.txt`, `r6-checker-9.run{1,2}.txt`, `r2b-checker-9.run{1,2}.txt`, and the raw runs (`paths{1,2}.*`, `variants{1,2}.*`).
- **Work folders:** `vw/` (the 21 variant copies and their outputs), `bw/`, `bw2/` (the 11 changes), `ktp1/`, `ktp2/`, `ktmut*/`, `ktprobe/`, `ktdamage/`, `keprobe/`, `envprobe/`, `site-run/`, `envcmp/`.

## 6. Appendix: commands and outputs

The repository's root is the working directory. `<scratch>` is my scratch folder.

```
sha256sum work/rust-core/reread-9/briefs/brief-2.md        -> f440f842…ec91 (equal)
sha256sum -c <scratch>/pins.txt                             -> 34 OK (before reading; again at the end)
git rev-parse HEAD                                          -> 2e9805aaa1ceeae0beb443d527680796b66f39c7
python -B research/rust-core/kept_evidence.py check         -> exit 0; KEPT EVIDENCE HELD: 48 of 48 files recovered exactly; 4453965 bytes kept in 955049
python -B research/rust-core/kept_tokens.py check           -> exit 0; TOKENED EVIDENCE HELD: 6 of 6 intact (originals not checked)
python -B research/rust-core/ref_run_paths.py  (twice)      -> exit 0, 16 s each; REF-RUN PATHS HELD: 46 of 46 as stated; stderr 0 bytes
python -B <scratch>/record.py ref_run_paths.py ...          -> made 0c44460d…ffff; the record 0c44460d…ffff: EQUAL
python -B <scratch>/variants_seq.py prepare <scratch>/vw    -> prepared 21 copies of the check: v00 … v20
(shell) python -B <scratch>/vw/vNN/paths.py, each alone     -> pass 1 in 348 s, pass 2 in 377 s; v00 and v16 exit 0 (46 of 46), the rest exit 1
python -B <scratch>/variants_seq.py report … 1 / 2          -> exit 0 / 0
python -B <scratch>/record.py ref_run_variants.py ...       -> made d23da015…bcd4; the record d23da015…bcd4: EQUAL
python -B <scratch>/breaks.py prepare; each copy's check    -> K1 … K11: each exit 0, REF-RUN PATHS HELD: 46 of 46 as stated
python -B <scratch>/breaks.py demo                          -> see the Q1 table (e.g. K3: refusal message "recursion-limit=100000"; K10: unchanged UNSTABLE, change NO-REFERENCE-RESULT)
gen_r6_mutants.py --checker research/rust-core/r6-mutants.txt <scratch>/repro/… (twice)
                                                            -> 10000 mutants; accepted 538; crashed 0; sha256 b206c8b2… (both; record equal)
gen_r2b_twins.py --checker research/rust-core/r2b-twins.txt <scratch>/repro/… (twice)
                                                            -> agrees on 1558 of 1558; sha256 59b26346… (both; record equal)
python -B <scratch>/closure.py .                            -> 54 statements: 36 held (26 the file, 10 kept superseded), 18 held by no file; 87d93a49 held by no file
python -B <scratch>/r6ref.py .                              -> header sha256 all equal; classes 632/6994/2374 equal the rows; 0 rows differ from r6-reference-3 and -4; 1 from -4.gen2 (09729)
python -B research/rust-core/kept_tokens_plants.py <scratch>/ktp1 (and ktp2)  -> 23 of 23 as stated; the two outputs byte-identical
mutant m1 (restore compares the length only)                -> KEPT-TOKENS PLANTS: 23 of 23 as stated
mutant m2 (kept file's sha256 unchecked)                    -> exit 1, zlib.error (caught by a crash)
python -B <scratch>/kt_probe.py <scratch>/ktprobe           -> two wrong prefixes: NOT REFUSED, restored == original, sha256 equal; fixture pairs side by side 0;
                                                               check with BOGUS: HELD; real files: 0 tokens side by side; home path: 110 views, 155040980 bytes, 0 hits
python -B <scratch>/ke_probe.py <scratch>/keprobe           -> RAISED zlib.error 10 of 48; reported BAD 38 of 48
python -B <scratch>/kt_damage.py …                          -> check without prefixes RAISED gzip.BadGzipFile
python -B <scratch>/env_probe.py pyc <scratch>/envprobe     -> with PYTHONPYCACHEPREFIX: exit 0; stderr ['PLANTED']; ENV line unchanged; RUN COMPLETED
PYTHONPATH=<scratch>/envprobe/site python -B research/rust-core/ref_run_paths.py
                                                            -> exit 0; REF-RUN PATHS HELD: 46 of 46 as stated; the runner's ENV line reads recursion-limit 5000
runner's law-mode ENV line vs r6-reference-5.txt's environment line  -> EQUAL (492 characters)
python -B <scratch>/small.py fcfile | sums | regzip         -> format_check from research/rust-core: True; 29/34/48 files: 4314387 in 925357 / 4325162 in 928379 / 4453965 in 955049;
                                                               no file outside both manifests; 48 of 48 re-compress to the kept bytes
diff (the -9-zb, -9 and superseded records)                 -> only the draft's sha256 in the header and the format record's draft line;
                                                               paths adds the module-count line and the three cases; 43 earlier rows unchanged
find (.git and work/rust-core/reread-9 pruned) -newer <first scratch file>  -> nothing; no __pycache__ in src, research/rust-core, evidence
```

HASH CLOSURE: PASSED: all 36 sha256 statements in Amendments 8–12 that name an existing file hold (26 against the files as they stand, 10 against the kept superseded records); the runner's two -9-zb records and the checker's two -9 records reproduce byte for byte; 18 further statements name versions no file holds (NB9) and are outside the closure.
