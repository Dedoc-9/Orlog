<!-- Packet E, saved by the draft's author, 2026-10-26: a research subagent's final report, delivered as its message (subagents cannot write files; its output file is empty). Copied without change. -->

# Release readiness for the held five-commit push (Orlog, read-only audit, 2026-10-26)

**What I ran.** Read-only git commands (status, `diff --cached`, `ls-files -v/--eol`, `check-attr`, `check-ignore`, `grep`, `log`), five `git add -n` dry runs, `sha256sum`, `stat`, `grep`, and one script that only prints: `python -B research/run-1/twin-r7/clause_diff.py` on the two drafts.

**What I did not run.** No probe, gate, self-test or build. Nothing in the repository was staged, created, edited or deleted.

**Disclosure.** To diff clause_diff's output I briefly wrote two scratch files in the system temp folder, outside the repository, and deleted them.

**Upstream.** Not fetched. The local `@{u}` equals HEAD (95dac79).

## 1. The checklist

### A. The rulings

| # | item | dependency | evidence | defining record | state |
|---|---|---|---|---|---|
| A1 | The amended set: 12 normative rows (A2, budget, port place, session record, binding, identity and bytes, counting, PREFIX, H2, HOST-0, F1–F9, reporting) and 2 implementation rows (codes, gate rows) | the push | Only the claims row is marked RULED (ROUNDS.md:449). Nothing marks the other 14 ruled. | ROUNDS.md:628-635, 440-457; RULINGS.md:355 | **BLOCKED** by each of the 14 rows |
| A2 | The format-freeze disposition | the push | Not ruled. The recommendation is to defer to P6's trigger (ROUNDS.md:636). | CUT-SCHEMA.md:199 (P6); RULINGS.md:355-356 | **BLOCKED** by the format-freeze ruling. It is coupled to two things: finding 20 (whether `'R'` carries the cut), and the tick block's and the ports' frames, which are not derived yet (SPEC-15-DRAFT-1.md:251-252; ROUNDS.md:335). Those frames depend on port place. |
| A3 | R7 | the push (ROUNDS.md:629) | The ruled wording is at RULINGS.md:380-423. | RULINGS.md:368-423 | **OBSERVED** as ruled. ROUNDS.md:634 is stale: it still reads "his ruling, (a) or (b)", "open", and "cannot run before this push". |
| A4 | Deciders of RULING findings that sit outside the amended set: D10 (finding 24, which blocks the round), R2 (7, 37), R3's details (13–15), 1a's specification (32), the `'R'` payload (20), "minor" (45) | Building §15 (R7 point 5). No record makes them push conditions. | open | DISPOSITION.md:102-114 | **BLOCKED** for the build. Not a recorded push condition. |
| A5 | Sheet items R1, R2, R8–R12 and D1–D10; the speed verdict's R13 and R14 | 1a and 1b | open | RULINGS.md:13-16; STATUS.md:169-177 | Not push conditions under ROUNDS.md:629 |

**Task 1: each RULING finding mapped to its decider.** Each finding is mapped as DISPOSITION's own row gives it. Section references: amended-set rows are in ROUNDS.md, sheet items in RULINGS.md.

- **PREFIX** (ROUNDS.md:450): findings 3, 4, 5.
- **A2** (:442): 6, 10, 12, 54, 55.
- **Session record** (:445): 10.
- **Identity and bytes** (:447): 6, 8, 31, 35, 36, 37, 56.
- **Port place** (:444): 7, 27, 28, 43, 57, 58.
- **Sheet R2** (RULINGS.md:61-83): 7, 37.
- **Budget** (:443) and **sheet R9**: 27, 29.
- **Counting** (:448): 30, 58.
- **Codes** (:452, an implementation row): 27.
- **D10** (RULINGS.md:503-504): 24.
- **The format freeze** (with no `'R'` row of its own): 20.
- **No open item exists for:**
  - 13, 14 and 15: R3 is ruled, and its details are "left for 1a's specification" (RULINGS.md:134-138);
  - 32: 1a's specification;
  - 45: "minor". Its clause, 15.13.9, is tagged `[ruled: claims; pinned]`.

**Defects in DISPOSITION's grouped list (DISPOSITION.md:105-114):**
- It covers 28 findings, but 29 reach a ruling.
- **Finding 43 is missing.** Its decider is port place (DRAFT-1-CHANGES.md:40-41; ROUNDS.md:335).
- Three findings lose a decider their own row names:
  - 10 loses session record (DISPOSITION.md:44);
  - 27 loses the code registry (:61);
  - 37 loses R2 (:71).

**T_r: the draft-1 clauses whose tags name each pending ruling.** Line numbers are SPEC-15-DRAFT-1.md's.

| pending ruling | T_r | 15.15 rows naming it |
|---|---|---|
| R1 | 15.1.6 (L63) | L390 |
| R2 | 15.0 Port (L32); 15.0 Prefix/Tick block (L35); 15.1.1 (L45); 15.1.3 (L52) | L387, L388 |
| sheet R8 | 15.0 Port (L32) | L387 |
| R9, budget | 15.7.3 (L189) | L394 |
| R10, R11, R12, D1–D9 | none | none |
| D10 | 15.13.11 (L368) | L402 |
| A2 | 15.0 Arrival/Door/Host/Session (L37); 15.3's intro and table (L106) and its untagged bullets (L117, L120, L127); 15.3 read-once (L122); 15.3 "No value is invented" (L125); 15.3 "A door refusal" (L129) | L392 |
| session record, binding | 15.4 (L136-145) | L392 |
| identity and bytes | 15.0 Input log (L40); 15.3 read-once (L122); 15.5, all of it (L149-167); 15.6 (L171); 15.7.5 (L197); 15.7.6's out_0 bullet (L206); 15.8 `tick-ops` (L220), the unread count (L222), the line order (L229) | L393, L395, L396 |
| counting | 15.7.1 (L181); 15.7.2 (L184, L188); 15.7.3's arm bullet (L194); 15.10 invariants (L267) | L394 |
| PREFIX | 15.12.4's open note (L305) only | L400 |
| H2 | 15.1.5 (L59) | L389 |
| reporting | 15.14 (L379) | L403 |
| `'R'` payload and P6 | 15.9 `'R'` (L245) | L397 |
| R3's details | 15.2.1 (L79). Also, through 15.15 L391: 15.2's first paragraph (L70), 15.2.3 (L89), 15.2.4 (L91) and 15.2.5 (L96-98) | L391 |
| 1a's specification | 15.10 (L262, L272) | L398 |
| the speed verdict's input-chain | 15.10 (L265) | L398 |
| HOST-0, F1–F9, codes, gate rows | none | none |
| contract draft 0 (no ruling item) | L75, L87, L95, L100, L125, L195, L238, L276, L281 | L391, L399 |

**L_r candidates: terms each ruling would define, and the clauses containing them.**
- **R2 and port place** ("tick block", "prefix", "port"): L30, L48, L180, L187, L199, L252, L269, L287, L295-299, L308, L353-354, L359.
- **Identity and bytes** ("input log", "tick record", "end record", `input-log-sha256`, NOT-RUN, LOG-OPEN): L114, L140, L178, L195, L217-222, L281, L292 (15.12.3, the provenance line), L354.
- **A2** ("arrival", "door", "host", "session"): L70, L75, L151, L155-156, L200, L277-279, L335, L354.
- **Budget**: L49, L58, L220.
- **PREFIX** ("licence", "first input", "first port declaration"): L63-66, L294-299, L311, L315, L370.
- **D10** ("REFERENCE-ONLY"): 15.13.11, plus 15.12.5 and 15.12.6 through finding 24.
- **R10** ("port signature"): L151, L160, L171.
- **R1** ("read once"): L32, L47, L122, L152, L164, L179.
- **D6** ("state"): L262.

**Clauses whose tags look incomplete for a ruling they plainly depend on:**
- **R10.** It decides the port signature and PORT-SIGNATURE (RULINGS.md:444-450). No draft-1 tag names R10 (15.5 L151 and L160; 15.6).
- **Defaults D1, D3, D5, D6, D9.** None is tagged where it applies:
  - D1, dense records (RULINGS.md:486): 15.5 L152-154;
  - D3, a run completes when its log ends (RULINGS.md:490), against LOG-OPEN: 15.5 L155-157 and 15.7.5;
  - D5, binding counts 0: 15.7.1 L181;
  - D6, state: 15.10 L262;
  - D9, one JSON object per tick: 15.3 and 15.5.
- **Defaults with no clause at all:** D4 (OUTPUT-TOO-LONG per tick) and D2.
- **15.12.5 and 15.12.6** depend on D10 (finding 24) but are tagged R6 only.
- **15.12.4's body** would change under a PREFIX ruling (findings 4 and 5), but only its note carries the PREFIX tag.
- **15.13.8's tick-block and NOT-RUN/LOG-OPEN rows (L353-355) and 15.13.9 (L360)** depend on port place (finding 43), on the statuses (identity and bytes), on A2 and on the freeze. They are tagged `[pinned]` only.
- **15.13.5 (L328)**, "any code but CLAIM-REFUTED", depends on the codes row (ROUNDS.md:420, 452).
- **15.3 L117-121** name RUN-REFUSED, END-PENDING, END-UNDISPOSED and one disposition per arrival. Those are the session-record row's (ROUNDS.md:445), but the clauses carry only the section's A2 tag.
- **15.10 L259** holds finding 32's open choice under the ruled tag `[ruled: R5]`.
- **15.5 "parsed whole" (L158)** is A2's "checked whole" (ROUNDS.md:442), but is tagged identity and bytes only.
- **The twin's own tag audit was not applied.** REPORT.md records missing dependencies that DISPOSITION never numbered and draft 1 did not add:
  - 15.0 Port: R3, R5, PREFIX (REPORT.md:47);
  - 15.1.3: PREFIX, budget (:69);
  - 15.1.6: R2, PREFIX (:79);
  - 15.3: R4, R3, identity and bytes, R2/R5 (:100);
  - 15.5: R3, A2, R5 (:115);
  - 15.6: R2 (:119);
  - 15.7.3: counting (:133);
  - 15.7.5: A2 (:138);
  - 15.8 `tick-ops`: budget (:147);
  - the PREFIX note: 15.1.3 (:163);
  - draft 0's 15.13.10, now 15.13.11: R6 and the claims ruling (:168);
  - the probes P01, P02, P04 and P07 (:416, 422, 444, 463).

### B. The re-reads (task 2)

| # | item | dependency | evidence | defining record | state |
|---|---|---|---|---|---|
| B1 | The 74 changed or added clauses are owed a re-read | the build gate | The set reproduces: clause_diff's output equals DRAFT-1-CHANGES.md:51-142 exactly, CR aside (TOTAL changed 61, added 13). Both drafts' sha256 equal the record's (`367b1b48…`, `f480ea7b…`). No record of any re-read exists. | RULINGS.md:403-405; DRAFT-1-CHANGES.md:13-15 | **OBSERVED**: the set is exact and not yet re-read |
| B2 | A_r sets and the term closure | the build gate, triggered by each ruling | None recorded. No term closure exists (searched the twin-r7 records, ROUNDS, STATUS and draft 1). | RULINGS.md:398-404 | **BLOCKED** by the rulings |
| B3 | Is a re-read a push condition? | — | The owner's words make it a build condition: "no push before the final gate, and no §15 clause built before the required review" (RULINGS.md:369-370). The held-push table (ROUNDS.md:632-640) lists no re-read. | — | **OBSERVED**: no record makes the re-reads a push condition |

**Which changed clauses also fall in a pending ruling's T_r.** 22 do by explicit tag:
- 15.0 Prefix/Tick block (R2 and port place);
- 15.0 Arrival (A2);
- 15.0 Input log (identity and bytes);
- 15.1.5 (H2);
- 15.1.6 (R1);
- 15.2.1 (R3's details);
- 15.3 L117 (A2, through the section tag only);
- 15.3 L122 (A2 and identity and bytes);
- 15.3 L125 (A2);
- 15.3 L129 (A2);
- 15.5 L158 and L160 (identity and bytes);
- 15.7.2 (counting);
- 15.7.3 (budget and R9);
- 15.7.6 (identity and bytes);
- 15.8 L229 (identity and bytes);
- 15.9 (`'R'` and P6);
- 15.10 L262 (1a's specification);
- 15.10 L265 (the speed verdict);
- 15.10 L267 (counting);
- the 15.12.4 note (PREFIX);
- 15.13.11 (D10).

Beyond those:
- 4 more through 15.15's assignment to R3's details: L70, 15.2.3, 15.2.4, 15.2.5.
- 6 changed clauses whose only decider is "contract draft 0", which has no ruling item: L75, L100, 15.7.4, L238, and 15.11's two clauses.
- All 13 changed 15.15 rows name a decider.

**Clauses in two T_r at once:** 15.0 Prefix/Tick block, 15.3 L122, 15.7.3 and 15.9.

**Whether one re-read can serve both obligations.** R7 does not say.
- Point 5 needs the twin to have read the clause's current text.
- Point 4 needs a re-read "once per triggering ruling", which can only follow that ruling.
- Read literally, one reading made after ruling r, of the clause as r leaves it, meets both for r.
- A re-read made now, before the ruling, cannot count as A_r's.
- A clause in two T_r needs one re-read per ruling. R7 does not address two rulings made together.

### C. The gate (task 3)

Its scope is ROUNDS.md:639: COMPAT-0, the self-test, then every probe rerun and compared with its evidence, headers aside. Evidence closure is ROUNDS.md:640. The tree must be exact (ROUNDS.md:394, 629).

| # | rerun | defining record | evidence and its timing | state |
|---|---|---|---|---|
| C1 | COMPAT-0: `tests/compat.py check --jobs 8` | AGENTS.md:109; evidence/run1-gate-before-push.txt:1 | That file is historical: run on 95dac79, once each. `src/` and `tests/` are unchanged since 472f5dd (OBSERVED). | **NOT CHECKED** |
| C2 | The self-test: 210/210 | AGENTS.md:108; ROUNDS.md:396-398 | The same historical file | **NOT CHECKED** |
| C3 | The 8 probes. Each evidence file is in evidence/run1-*.txt, and each header names its command. | PROBES.md:13-14, 19-28 | Every evidence file is newer than its script and its transitive imports. Every last line equals PROBES.md's (OBSERVED). | the reruns: **NOT CHECKED** |
| C4 | evidence/run1-cut0-schema-draft1.txt | PROBES.md:25; CUT-SCHEMA.md:214-215 | Written at 16:49. cut0_schema.py changed after, at 17:20. Labelled SUPERSEDED in its header. | **OBSERVED**: labelled, not rerunnable as it stands |
| C5 | manifold: fibers.py, resume_oracle.py, `resume_oracle.py search`, make_laws.py | ROUNDS.md:640; their headers; manifold/VERDICT.md:84-85 | Every script is older than its output (OBSERVED). Three cannot be checked as the gate is written: `fibers-timing.txt` is "never byte-identical"; `resume_oracle-search.txt` was "run once"; make_laws.py rewrites laws/*.orl in place (make_laws.py:76-81). | **NOT CHECKED** |
| C6 | adversary: 6 current-tree reruns | RERUN.md:15-25 | Each header's sha256 equals the current file for cut0_claims, cut0_session and the script (OBSERVED). k_fuzz and k_monotone are identical "but for the seconds printed", and no mask is defined. | **NOT CHECKED** |
| C7 | adversary: 7 first-form outputs | RERUN.md:10-13, 50-60 | Three scripts changed after their output: k_monotone (19:23 against 14:14), s_attacks (19:25 against 14:10), k_repairs (19:40 against 14:09). An imported probe changed after the other four: cut0_claims at 14:38, cut0_session at 14:28. All are documented as the first form. s_drop is said to reproduce (RERUN.md:25), but no rerun output is saved. | **OBSERVED** |
| C8 | probes/float_decision.orl and fixed_decision.orl | FLOAT.md:37-38 ("MEASURED again here") | No evidence file | **NOT CHECKED**: nothing to compare |
| C9 | twin-r7/clause_diff.py | DRAFT-1-CHANGES.md:51-142 | Reproduced | **OBSERVED** |

### D. The commit partition (task 4), all OBSERVED

- 112 pending files: 23 modified and 89 untracked.
- **Commit 1:** 37 files.
- **Commit 2:** 28.
- **Commit 3:** 27.
- **Commit 4:** 2.
- **Commit 5:** 18.
- Every file falls in exactly one commit, under git's own pathspec matching (quoted, as PowerShell passes them): none in no commit, none in two.
- Every pathspec matches at least one file. All five dry runs exit 0.
- Nothing under `work/` would be staged. It is ignored (.gitignore:3), and no pending path is under it.
- `git diff --cached` is empty.
- `status.showUntrackedFiles` is unset.
- Every line of `ls-files -v` is `H`.
- ROUNDS.md:637's record ("95 files … 36, 22, 17, 2 and 18") is stale. The new files are clause_diff.py, the 6 current-tree reruns, RERUN.md, the twin-r7 records and draft 1.

### E. Private data (task 5), OBSERVED

- **The 112 pending files:** no home path, no local user name, no host name, no session id.
- **The scrub:** the 16 court files replace the path with `{session}` (4,067 times) or `{python}` (1), and every changed line carries one of them.
- **Hits that are not private:**
  - URLs in research/run-1/FLOAT.md:193-201 and court/prosecution-logic.md:578-579;
  - a third party's patch address inside a public citation URL (research/run-1/FLOAT.md:197);
  - the GitHub account `Dedoc-9` in DOCTRINE.md:6 and :544 and STATUS.md:3, already public in README.md and ADMISSION.md at HEAD.
- **History:** the 16 pushed files at HEAD still hold the path. This is F42, already recorded as open (STATUS.md:184-187).

## 2. Risks the existing records do not mention

1. **A_r would miss dependencies.** The twin's tag-audit dependencies (REPORT.md's "Missing dependencies" lines) are R7's D_r, but they appear in neither DISPOSITION nor draft 1's tags. So an A_r computed from tags and DISPOSITION would miss them.
2. **DISPOSITION's grouped list is incomplete.** It omits finding 43, and drops a decider for findings 10, 27 and 37.
3. **R10 is never tagged, and five defaults are missing.** R10 governs 15.5 and 15.6, yet no draft-1 tag names it. D1, D3, D5, D6 and D9 apply to clauses that do not name them, and D2 and D4 have no clause.
4. **"Sheet R14" does not exist.** Draft 1 cites it at L260 and L278, but RULINGS.md has no R13 or R14 (STATUS.md:175).
5. **"Door" names two functions.** At 15.0 L37 it is the input door; at 15.1.5 L59 it is the source-text door. Term closure for L_r would link H2 to A2 and R3.
6. **Some clauses no ruling can trigger.** The pin can change the `[pinned]` clauses (draft 1 L13-15), but a pin is not a ruling, so it triggers no A_r. The same holds for the "contract draft 0" clauses, and for R3's details, 1a's specification, the `'R'` payload and "minor", none of which has an item to rule.
7. **A changed statement is outside the 74.** T10.5's statement changed after the twin read it (ROUNDS.md:333 against T10-STATEMENTS.md, still at the manifest's `bf4da71…`). It is in R7's reading set but not in the re-read list.
8. **Seven historical outputs would change bytes when committed.** The first-form outputs in research/run-1/manifold/adversary/ are CRLF and not covered by `-text`. Under `* text=auto eol=lf` (.gitattributes:1; only evidence/** is protected, :12), they would be committed as LF, not as captured.
9. **RERUN.md:13 overstates.** It says each current file names "every module it ran". The headers name only cut0_claims, cut0_session and the script, not cont_oracle, k_attacks, k_fuzz, k_repairs, completeness_probe or `src/`.
10. **The gate's comparison is undefined in four places.** There is no rule for timings, a single run, CR in evidence/, or the "seconds printed" mask. make_laws.py writes into commit 1's files when rerun.
11. **The gate's own record cannot be in the gated tree.** No record says where the final gate's output goes, or how the committed tree is tied to the tree the gate ran on. A gate record written into evidence/ changes that tree.
12. **P1–P7 has no ruling item.** CUT-SCHEMA.md:176 marks the policy "the owner's to rule", but only P6's timing is a push condition.
13. **Stale text.** ROUNDS.md:634 (the R7 row), ROUNDS.md:637 (the file counts) and STATUS.md:44 ("only the claims question is ruled") no longer match.
