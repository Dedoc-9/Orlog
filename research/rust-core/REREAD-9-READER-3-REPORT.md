# REREAD-9, reader 3 of 3: the rulings and cross-document consistency, its report word for word (2026-10-31)

Saved as returned by the reader, a fresh general-purpose agent with no part in writing anything it read. REREAD-9 ran
as three readers working at the same time, under the owner's authorization (RULINGS.md, "REREAD-9 authorized"):
reader 1 the format, the checker and the 91 challenge; reader 2 the protocol, the runner, and the evidence and its
keeping, with the hash closure; reader 3 the rulings and cross-document consistency. Each started fresh, had its own
scratch folder and its own letter for findings (NA, NB, NC), and saw nothing of the others' work.

**Its brief** is `work/rust-core/reread-9/briefs/brief-3.md`, sha256 `b570f2682735424ce4ace6bb274909cc133480049d78afd8c3525ee4aaa4301a`, kept in `kept/`; the reader was given only
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

# REREAD-9, reader 3 of 3: the rulings and cross-document consistency (findings NC1–NC14)

## 1. What I read and ran, and what I could not check

**The brief and the pins.** I hashed the brief first: `work/rust-core/reread-9/briefs/brief-3.md` is `b570f268…a4301a`, which matches. HEAD is `2e9805aaa1ceeae0beb443d527680796b66f39c7`. All 34 pinned files hashed equal: 34 of 34 (MEASURED, appendix A1). They were not hashed again at the end; nothing I ran writes to the repository.

**Read whole:** RULINGS.md, REREAD-8-DISPOSITION.md, research/RULING-SHEET-2026-10-31.md, SHEET.md (Amendments 8 to 12 line by line), LAW-FORMAT-0-DRAFT-9.md, W9-VERIFICATION-REPORT.md and W9-VERIFICATION-REPORT-2.md.

**Read in part, only where a document's claim rests on it:**
- `format_check.py`: lines 540–569 (phase 2, W3) and the ZA5 comment at 1659;
- `plant_reverts.py`: the undoings at 290–315, and 401–403;
- `ref_run.py`: its docstring (1–40) and its exception handlers;
- `kept_tokens_plants.py`: lines 1–80;
- `kept/MANIFEST.txt` and `kept/TOKENED.txt`;
- the five `-9-zb` records, the `-9` records' headers, and the R6 and R2b checker records `-8` and `-9`;
- `r2-writeback-fixtures.txt`, and the headers of `r6-reference-4.txt` and `r6-reference-5.txt`.

**Ran.** Everything ran as `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B` from the repository's root, with TEMP and TMP set to `<scratch>`. One process at a time, and every process started on the first try.
- A quotation checker: every `*"…"*` passage in the seven documents, compared with his blockquotes in RULINGS.md.
- An attribution listing: which ruling section holds each quotation in the newer material.
- The ruled witnesses, run through `format_check.read` used as a black box.
- Every kept file checked against its manifest row, and scanned, decompressed in memory, for the account's name.
- Sums taken from the manifests, and row diffs of the checker records.

**Disclosures.**
- I counted, without reading, how often the account's name appears in the three REREAD-8 reader reports. They are not pinned. I did it to check the disposition's disclosure 7.
- I listed `evidence/`.
- I did not open `work/` or anything under `research/law-sufficiency/`.
- I did not run the checker's suite, the runner, the generator or decoder1, and I ran nothing on mutant 09729.

**Could not check:**
- the quotations of rulings 2, 3 and 4 (they are in `research/law-sufficiency/RULINGS.md`, which is closed to me);
- earlier dispositions' option texts that are quoted as "adopted" (not pinned);
- the message he was given for the ruling sheet, and what he was told before he authorized REREAD-9 (neither is kept);
- `work/` (attempt records, superseded copies);
- the verifier's scratch files;
- the 83-mutant measurement;
- the restoration of the six tokened files, which needs his prefixes. I read only the kept plant runs.

## 2. Verdict

**The rulings are carried in substance.** Each ruling made since REREAD-8 is recorded whole in RULINGS.md and carried in draft 9, SHEET.md Amendments 8 to 12, or the checker and its records.
- Every passage the newer material attributes to him appears word for word in his recorded words, under the ruling it names (MEASURED).
- No paste that came beside a ruling (the commentary, RDE-0, ISPT-0, the attempt-record proposal) is presented as his ruling.
- The ruled witnesses give the verdicts the documents state (MEASURED).
- His six conditions for REREAD-9 hold in substance.

**It is not clean: 0 BLOCKER, 2 MAJOR, 12 MINOR.**
- NC1 (MAJOR): two pinned research files hold the home path, against the rule he ranked above convenience.
- NC2 (MAJOR): section 7 claims to name "every adopted evidence-record requirement" and omits several of his own.
- The MINORs are:
  - dispositions carried short or beyond what he ruled;
  - items applied before a disposition;
  - his conditions for REREAD-9 not carried into the sheet or draft;
  - overwrites that are not disclosed;
  - stale counts and references.

## 3. Answers to the questions

### Q1. Each ruling since REREAD-8, against every document

| ruling | carried in | as he wrote it? |
|---|---|---|
| G (E2 literally; ZA1, ZA3, ZA4; the 4-clause crash) | draft 9 derivation 17 (:489, :493–506); underived list (:792–805); W9 table (:602–653); six plants and four undoings (reverts rows 131–141) | yes |
| H (91, measured vs reasoned, challenge) | draft 9 W14(c) (:721–758) and Q3 (:1175–1178); Amendment 8 (:1042–1045); depth record's last line; plants at 91/92 and undoings at 130/90 | yes. The checker's change falls under H's adopted option (a) |
| I (repetition; every record requirement; contents kept) | Amendment 8 (:1053–1104) | items 1 and 3 yes; item 2 short (NC2) |
| J (runner unchanged, SystemExit a limitation) | `ref_run.py` 822c826e… unchanged; SHEET :824–825, :1106–1118 | yes in the documents; the pinned docstring says otherwise (NC9) |
| K (memory sentence; report what is checked; no cap) | SHEET :866–867, :1120–1126, :1224–1227 | yes; binds the next generator, as option (a) he adopted said |
| L1 (generator change, subject to diff and test) | Amendment 8 :1128–1136 | yes. Reconstruction sha256 equal to `r6-reference-4.txt`'s header; trial `GEN-TRY3: 13 of 13` in both runs (MEASURED) |
| L2 (every applicable module) | SHEET :831–832, :1136–1138 | one of the two places the DRAFT named is left unnoted (NC4) |
| L3 (enumerate, verify, bring ambiguity back) | draft 9 §8; both verification reports; (A)–(D) brought back | R5 settled by wording, not brought back (NC5) |
| Sheet ruling (A)–(D) and C's limitation | draft 9 :654–696; Amendment 9 :1170–1183 | yes. Four points verbatim (:665–670); verifier credited (:654–655); witnesses MEASURED |
| Sheet ruling, the six files on condition | Amendment 9 :1198–1211 | condition 6 short for two spellings (NC10) |
| Sheet ruling, corrections; ZA7 withheld; ZA9; items named apart | Amendment 9 :1213–1237; draft 9 :28–32, :104–106, :589, :910–911 | ZA7 yes. ZA9: W3 row goes further (NC3). ZA5 applied before his word (NC5) |
| Sheet ruling, debate dispositions | RULINGS :1081–1087 | the writer narrows "show on cards"; the experiment's status is unclear (NC8) |
| Sheet ruling V (six conditions) | RULINGS (whole) only | not in SHEET.md or draft 9 (NC6) |
| R1 and R4 | draft 9 :677–696; Amendment 10; RULINGS :1113–1121 | yes. R1 witness W9 line 3, a plant, undoing to W10 (reverts row 150); R4 witness W10 line 3, not a plant (MEASURED) |
| ZA5 | draft 9 :35–37, :1029–1033; Amendment 11 | yes. The checker comment "(adopted as test corrections…)" (format_check.py:1659) is disclosed (SHEET :1312–1315) |
| ZB3, ZB5 | Amendment 12; records 46 of 46, 15 of 16, ZB3's plants 4 of 4 | yes. "against the runner's own recorded environment" is read as one reading and said so (:1354–1355) |
| REREAD-9 authorization | RULINGS :1172–1200; this brief | yes |

### Q2. What is not a ruling
- **No document presents a side paste as his ruling** (RULINGS :759–762 and :1085–1087).
- **One passage attributed to "his draft" is not in his recorded words** (NC14).
- **Applied without a disposition:**
  - ZA5's plants, before his word (since kept);
  - the re-verification's R2 and R5, as wording (NC5).
- **Entered as wording but more than wording:**
  - the W3 row's "never by writing back" (NC3);
  - R5's "needs" entry (NC5).

### Q3. Precedence and in-place notes
- **Precedence.** Amendments 8 and 9 each say they govern over the earlier ones. Amendments 10 to 12 do not say so, but each is narrow.
- **Unclear what governs:**
  - the Verðandi experiment's status (NC8);
  - which records draft 9 rests on (NC12).
- **In-place notes since REREAD-8.** I checked the 17 notes in SHEET (:4, :35, :54, :780, :809, :817, :824, :831, :845, :853, :866, :881, :884, :931, :973, :1412–1413), RULINGS :320 and draft 9 :31. Each is dated, names its finding and its ruling, and says what it corrects. One exception: draft 9 :503 (the D2 correction) carries no date.
- **Rewritten records.** I found no dated text rewritten. But bytes named by sha256 in dated amendments were overwritten in place after his I. Amendment 12 discloses five of them; NC11 lists the others.

### Q4. Quotations (MEASURED)
- **210 italic quoted passages; 172 appear verbatim in his recorded words.**
- **In the newer material** (Amendments 8–12, draft 9's new text, RULINGS' "As kept" since G–L, the ruling sheet, the disposition, the reports' headers), every passage attributed to him is found under the ruling named.
- **The other 38:**
  - 4 have his exact words but join his bullets into one quotation;
  - 1 changes case only;
  - 19 quote other sources (SPEC, the sheet's own earlier text, code, drafts, readers, the attempt-record proposal);
  - 8 quote adopted option texts, which I could not check;
  - 3 quote rulings 2–4, which I could not check;
  - 1 is his earlier B1(a) text, recorded inline rather than as a blockquote;
  - 1 changes punctuation (NC14);
  - 1 is attributed to him but not recorded (NC14).

### Q5. Counts (MEASURED unless marked)

| count | stated | recount |
|---|---|---|
| REREAD-8 findings and severities | 34 (7 MAJOR, 27 MINOR) | 34: ZA 9 (4/5), ZB 12 (1/11), ZC 13 (2/11) ✓ |
| REREAD-8 tokens | 1,186,627 | ✓ |
| attempt folders' bytes | 151,090,353 | ✓ (four runs.jsonl plus ten manifest rows) |
| laws / plants | 305 / 113 | ✓ (record; the per-draft list sums to 113) |
| plants changed by an undoing | 69, 4 only by a crash | ✓ |
| RS plants / undoings | seven / six (draft 9 :1195) | seven / **five** (NC13) |
| G undoings, H undoings, ZA5 undoings | 4, 2, 6 | ✓ |
| M10's undone count | "0 of 304" (draft 9 :1107) | record: **0 of 305** (NC13) |
| kept files | 29, 34, 48 | 29 rows sum to 4,314,387 / 925,357 ✓; 34 ✓; 48 ✓. All 54 kept files match their rows. Amendment 8's description lists 28 (NC13) |
| token plants | 39 of 39, twice alike | ✓ (kept runs equal) |
| paths / variants | 46 of 46; 15 of 16; ZB3's plants 4 of 4; X1–X4 34, 44, 32, 34 of 46 | ✓ |
| R6 / R2b rows unmoved from draft 8 | 10,000 / 1,558 | 0 rows differ, either record ✓ |
| R2 fixtures | 11, "10 of the 11" | 11; the first is in order with no repeat ✓ |
| W9-1 sweep | 168,596 = 138,384 + 30,212 (24 families) | ✓. Verdict sums ✓ in both reports; 504 laws moved W9 to W10 = 72 + 432 ✓ |
| W9-2 "about 500,000" | about 500,000 | 474,249 laws run in all |

### Q6. REREAD-9's six conditions (his ruling V)
1. **(A) to (D) in the exact language:** holds. Draft 9 §8 and Amendment 9; witnesses MEASURED.
2. **The checker implements the adopted (C):** holds. V1 gives W10 line 3, V2 gives W9 line 3 (MEASURED).
3. **The independent verifier checks it:** holds in substance, DECLARED by W9-VERIFICATION-REPORT-2 (0 disagreements). Two caveats:
   - the verifier read draft bytes `d86a2aeb…`, which are not kept;
   - R5's wording entered the W9 table after the verification (NC5, NC11).
4. **The six files resolved, plants passed:** 39 of 39 (MEASURED from the kept runs). Partial matches and repeated occurrences are not planted for REL83 or SLUG (NC10).
5. **Every remaining DRAFT item has an explicit disposition:** holds formally. Two items said to be done are carried short (NC4).
6. **The 91 challenge and the earlier prerequisites ready:** the challenge is prepared (draft 9 Q3) and E2 and W9 hold. Section 7 is "complete" only short of NC2.

His four conditions from G–L are named in draft 9. The six from the sheet ruling are not (NC6).

## 4. Findings

**NC1. MAJOR: two pinned research files hold the home path.**
- **Where:** `research/rust-core/W9-VERIFICATION-REPORT.md`:181, :188; `W9-VERIFICATION-REPORT-2.md`:135, :142. Against RULINGS.md:1028, and SHEET.md:1210–1211, :1386.
- **Evidence (MEASURED):** a case-insensitive count of the account's name gives 1 for its long form and 2 for its 8.3 short form in each file. These are the repository's absolute path and the short-form temp folder. HEAD holds none.
- **What it goes against:** his ruling II: *"The no-home-path rule takes precedence over convenience."* His condition 1 counts the 8.3 form as a spelling of that path.
- **Why the documents miss it:** Amendments 9 and 12 measure only `kept/` ("No file in kept/ … names his account"). The second report was saved after his ruling.
- **Context:** the REREAD-8 reader reports hold the 8.3 form, 7, 17 and 28 times, and reader 2's the long form once. The disposition disclosed this before his ruling (REREAD-8-DISPOSITION.md:102–103).
- **Proposal:** put it to him. Either token both reports' paths as option (c) does, or keep them outside the tree, and measure the whole research tree, not `kept/` alone.

**NC2. MAJOR: section 7 item 8 claims every adopted evidence-record requirement and omits several.**
- **Where:** SHEET.md:1067–1076. His I is at RULINGS.md:886–892.
- **His words:** *"Every adopted evidence-record requirement is named, not merely conditions 5 and 6."*
- **Evidence (REASONED, by reading).** These record requirements of his, binding on runs of items 1 to 5, are not named:
  - his first ruling's condition 3, *"Record which outcome occurred for every case"* (RULINGS:30–32);
  - F2's *"Record the reader's determination and the exact applicable rule and diagnostic"* (RULINGS:353; SHEET:441–445);
  - U2's retained runner-fault record (SHEET:691–694);
  - B1's *"Record its identity, line if available, and exit status"* (RULINGS:598);
  - B4's *"Keep its error and any records already produced"* (RULINGS:623);
  - B5's *"Record its wall time"* (RULINGS:627);
  - R8's records stating their conditions (L13, SHEET:644; K12, SHEET:535–537).

  ATTEMPT-RECORD-0's points 5 and 6 overlap B1, B4 and U2 only in part.
- **Proposal:** name each requirement in item 8 by its amendment and his words, or drop "every" and put the list to him.

**NC3. MINOR: ZA9 is carried both beyond and short.**
- **Where:** draft 9:589 (W3's row), :907–911, :1002–1003; format_check.py:557–558.
- **Beyond:** the row now says *"a reader decides W3 by the spacing rule itself, never by writing back"*, entered as ZA9's "pointer", which counts as wording. His R7-A is narrower: *"W3 must be determined by code independent of the writer used to produce `OUT`"* (RULINGS:579). It allows a separate serializer; the row forbids one.
- **Contradiction inside the draft:** section 11 says *"the checker decides W3 by writing back"*, and the code does: `written = … w_stmt(…)`, then `need(written == rest, 3, …)` (MEASURED by reading).
- **Short:** his ZA9 heading reads *"confine R7 writer plants to the writer's named code"*. Nothing says where the writer's code is named. The disposition's *"the source reading names the writer's code"* (REREAD-8-DISPOSITION:162) was not carried into section 0's source reading.
- **Proposal:**
  - reword the row in R7-A's words, or put "never by writing back" to him as a change named apart;
  - say whether "a reader" covers the checker;
  - have section 0's reading name the writer's code by lines.

**NC4. MINOR: two DRAFT items the sheet lists as done are carried short.**
- **ZB4/ZC3:** the DRAFT named two in-place notes (REREAD-8-DISPOSITION:166), and the ruling sheet's III.3 (RULING-SHEET:153) counts them done. Only SHEET:831–832 has one. SHEET:946 still reads *"the runner now hashes eight modules in each run"*, of the R6 remake, where law mode hashes five.
- **ZC2:** the DRAFT asked that RULINGS.md's note be corrected in place (:176, :300). RULINGS:763 still says *"draft 8 says what was measured and what follows"*, and ZC2 found draft 8 did not do "what follows".
- This is ZC5's mechanism again: the summary was applied, not the rows.
- **Proposal:** add the two notes.

**NC5. MINOR: items applied before a disposition.**
- **R2 and R5.** The re-verification's R2 (derivation 17's sentence, draft 9:501–502) and R5 (the `change` row's "needs", :647) were applied under RS-III (SHEET:1191–1196, :1217). They came after his ruling on the sheet and were not on it. His III covers the disposition's *"Remaining DRAFT items"*.
  - R5 settles a W9 part that the words leave open, where L3 says *"Bring back any ambiguity rather than resolving it by implementation convention"*. RULINGS' own "As kept" for L3 (:975–977) says such a part is brought back. The verifier says no verdict depends on it (REASONED, its R5).
  - For R2 the verifier offered his confirmation as an alternative to rewording.
- **ZA5.** ZA5's plants were applied in Amendment 9 (:1232–1235) before his word. RULINGS:1078–1080 says items named apart *"wait"*, and his R1/R4 ruling said it did *"not authorize … ZA5"*. He has since kept them.
- **Proposal:** list R2 and R5 in REREAD-9's disposition as applied, for his confirmation. Correct the "and waits" sentence with a note.

**NC6. MINOR: his ruling V (six conditions before REREAD-9) is carried nowhere but RULINGS.**
- **Where:** RULINGS:1052–1063; draft 9:42–44, :1168; Amendment 9.
- **Evidence:** a grep finds no statement of V in SHEET.md or draft 9. Draft 9 §12 still says *"REREAD-9 does not begin until his four conditions hold"*.
- **No record of the check:** what he accepted was *"He was told that each condition … read as met"* (RULINGS:1174). No record gives each condition with its evidence.
- **Proposal:** a dated note in Amendment 9 or a new amendment, listing V's six conditions with the evidence for each.

**NC7. MINOR: what he ruled on is misframed, and not kept.**
- RULINGS:983 says *"He was put `research/RULING-SHEET-2026-10-31.md`"*. His own words: *"I am ruling on the exact descriptions and measured consequences supplied in your message, not certifying the unseen contents"* (:1067). The ruling sheet's header (:3) says *"He ruled it"*.
- The message is not kept, so his qualification, *"The final sheet must preserve these dispositions without silently broadening them"*, cannot be checked against what he saw.
- Visible divergence: his IV says *"Show GLUE-0 verdicts on admission cards"*, where the sheet's I.2 said the card is not authorized.
- **Proposal:** keep the messages put to him (this one, and the one before the REREAD-9 authorization) beside his rulings, and reword :983.

**NC8. MINOR: the Verðandi items have no clear status.**
- **Where:** RULINGS:1045–1046, :1050, :1081–1084, :1111, :1134, :1161, :1188; SHEET:1284, :1323, :1392.
- His IV *"Authorize[s] the one Verðandi graybox scratch experiment, subject to its sheet and hand predictions first"*. Three later rulings each say they *"do not authorize … the Verðandi experiment"*.
- SHEET's *"the Verðandi experiment's two decisions"* is defined nowhere, and is not his *"the two Verðandi decisions"*.
- The card question is settled by the writer's reading (*"no card is built until he says so"*), not brought back to him.
- **Proposal:** state what is authorized and what the two decisions are, and put the card reading to him.

**NC9. MINOR: the pinned runner describes the SystemExit case as covered.**
- **Where:** ref_run.py:24–27, :173, :186. Against his J at RULINGS:902.
- **Evidence (REASONED, by reading the code):** the docstring says a failure while the reference's modules import is a runner fault *"whatever the exception"*. The import handlers catch `Exception`, so a `SystemExit` escapes.
- His J: *"Do not describe it as covered or resolved."* No note says the docstring overstates. ZC12's notes (SHEET:1222–1223) cover only names.
- **Proposal:** a note in the sheet naming these docstring lines. The runner stays pinned.

**NC10. MINOR: the token plants do not cover two of the four real spellings.**
- **Where:** kept_tokens_plants.py:22–28, :46–54; SHEET:1199–1206.
- **Evidence (MEASURED, from the code and the kept runs):** the made-up fixture plants five spellings: HOME_ESC, HOME, HOME_FWD, HOME83_ESC, HOME83. The real files hold HOME_ESC, HOME83, REL83 and SLUG.
- REL83 and SLUG are covered only by the real-file rows: restored, and missing or wrong prefix refused, each occurring once. No plant covers their partial matches or repeated occurrences, which his condition 6 requires.
- **Proposal:** add REL83 and SLUG to the fixture, with near misses and repeats.

**NC11. MINOR: records named by sha256 after his I were overwritten in place and not kept, beyond what Amendment 12 discloses.**
- **What is gone** (MEASURED: none of these is in `kept/`; whether `work/` holds copies was not checked):
  - Amendment 8's checker records `3b90928d…` and `7efae393…`; the same file names now hold `b206c8b2…` and `59b26346…`;
  - the kept manifest at Amendments 8 and 9 (`10614486…`, `d2a8f78b…`);
  - draft 9's versions `5880ca54…`, `98796b8d…`, `d86a2aeb…`, `1518796d…`, `33285ad4…` and `12d95962…`. These include the two texts the verifier read, the inputs of condition 3's verification.
- His I: *"Hashes establish identity; they do not substitute for retaining the evidence."*
- **Proposal:** disclose them beside Amendment 12's five. Rebuild what can be rebuilt, as Amendment 12 did for its five. Keep superseded drafts and manifests from now on.

**NC12. MINOR: draft 9 points at superseded records.**
- **Where:** draft 9:731–732, :1097, :1155–1157.
- **Evidence (MEASURED):** draft 9 names the `-9` records, whose header hashes draft `12d95962…` (Amendment 11's version). Amendment 12 made the `-9-zb` records for the present draft. The `-9` and `-9-zb` records differ only in their header lines.
- Draft 9 also cites *"SHEET, Amendment 8"* for the checker's R6 and R2b verdicts, though the checker and those records changed in Amendment 9.
- **Proposal:** cite the `-9-zb` records and Amendment 9.

**NC13. MINOR: three stale counts.**
- **Undoings:** draft 9:1195 says *"seven plants and six undoings"*. There are five RS undoings: RS-A, RS-B, RS-C (i), RS-C (ii) and RS-D (plant_reverts.py:303–309; reverts rows 146–152).
- **M10:** draft 9:1106–1107 says *"0 of 304"*. The record reads `BITES: 0 of 305`. The plant's label (plant_reverts.py:401, :403) still says 304.
- **Kept files:** Amendment 8's account of its 29 kept files (SHEET:1095–1099) adds up to 28. The 29 manifest rows hold five logs of evidence and records runs (`records-9`, `run-format-8`, `-8b`, `-9`, `-9b`), not four. Their sums equal 4,314,387 and 925,357.
- **Proposal:** correct in place, with notes.

**NC14. MINOR: quotations.**
- RULING-SHEET:13–14, *"In his draft's words"*: the words are not in his recorded words.
- REREAD-8-DISPOSITION:252 attributes *"every failure before `reference()` is a runner fault"* to "D5, adopted". His recorded D5 reads *"…before `reference()` begins is a runner fault, not a reference crash"*. If it is the option text, I could not check it.
- SHEET:839–840 (Amendment 7, before REREAD-8) ends his sentence with a period where his text has a colon.
- **Proposal:** record his consolidated draft, or attribute the words otherwise; mark option texts as such.

## 5. Files I created

`<scratch>/pins.txt`, `<scratch>/quotes.py`, `<scratch>/quotes.out`, `<scratch>/attrib.py`, `<scratch>/attrib.out`, `<scratch>/witnesses.py`. Nothing was written to the repository.

## 6. Appendix: commands and outputs (from the repository's root; TEMP=TMP=`<scratch>`)

- **A1.** `sha256sum -c <scratch>/pins.txt`: `34` OK, none failing. `git rev-parse HEAD`: `2e9805aaa1ceeae0beb443d527680796b66f39c7`.
- **A2.** `python -B <scratch>/quotes.py .`: `quoted passages: 210; found verbatim in his recorded words: 172; not found: 38`. The 38 are listed in `<scratch>/quotes.out`.
- **A3.** `python -B <scratch>/attrib.py .`: every newer quotation maps to its named ruling. The only `NOT FOUND` entries are rulings 2–4, Amendment 7's 632 sentence, option texts, and RULING-SHEET's "his draft".
- **A4.** `python -B <scratch>/witnesses.py`:
  - `A: W10 line 3`; `B1: W10 line 3`; `B2: W10 line 4`;
  - `C V1: W10 line 3`; `C V2 = R1: W9 line 3`;
  - `D V3: W9 line 3`; `D V4: W10 line 3`;
  - `R4 V6: W10 line 3`; exit 0.
- **A5.** `grep -ci '<account name>'` and `'<8.3 form>'`, per file:
  - W9-VERIFICATION-REPORT.md: long 1, short 2 (lines 181, 188);
  - W9-VERIFICATION-REPORT-2.md: long 1, short 2 (lines 135, 142);
  - the other documents read: 0;
  - `git grep -il` of the account's name in HEAD: one file, README.md, matching the author's name, not a path.
- **A6.** Kept files against their manifest rows: `kept files matching their manifest row: 54 not matching: 0`. Decompressed scan: `files scanned 56 files naming the account 0`.
- **A7.** Manifest sums of source and kept bytes, by row count:
  - `28 (4313608, 924895)`
  - `29 (4314387, 925357)`
  - `34 (4325162, 928379)`
  - `48 (4453965, 955049)`
- **A8.** Recounts:
  - `rest families 24 sum 30212 plus binary 168596`
  - `W9-2 laws total 474249`
  - `attempt folders 151090353`
  - `REREAD-8 tokens 1186627`
- **A9.** `diff` of the non-`#` rows, checker records `-8` against `-9`: r6 `0`, r2b `0`. Headers name `format_check.py 2965ed15…`, `agrees on 1558 of 1558`.
- **A10.** Reconstructed generator: `len 25560 sha256 48d88b2167c2c676ebcbda70804753b4b72bbaa90729e2e05348a95ba66abc87`. `r6-reference-4.txt`:2 names the same.
- **A11.** Kept tokened trial outputs: `GEN-TRY3: 13 of 13` in both. Kept token-plant runs: `KEPT-TOKENS PLANTS: 39 of 39 as stated`, the two runs byte-identical.
- **A12.** Last lines of the `-9-zb` records:
  - `FORMAT CHECK (DRAFT 9) HELD: 305 of 305 laws pass, 305 written back exactly, derivations equal on 305; plants 113 of 113 caught, 0 not run`
  - `PLANT REVERTS HELD: 69 plants and fixtures, 69 changed by at least one undoing, 4 of them only by a crash`
  - the M10 row: `BITES: 0 of 305`
  - `REF-RUN PATHS HELD: 46 of 46 as stated`
  - `REF-RUN VARIANTS HELD: 15 of 16 changes caught by the check; the control passes; 1 not caught, each said`
- **A13.** `sha256sum` of the `-9` records: `e4f3aa0d…`, `c46dce78…`, `0e6627df…`, `98f92a44…`, `147a12db…`, which are Amendment 11's. `diff` of `-9` against `-9-zb` for the format, reverts and depth records: header lines only (4, 2 and 2 lines). The `-9` records' line 3 names `LAW-FORMAT-0-DRAFT-9.md 12d95962b116cc0f`.
- **A14.** `grep` of plant_reverts.py:
  - RS undoings at :303, :304, :305, :307, :309 (five);
  - `"the 304 laws' write-back count"` at :403.
- **A15.** `grep` of SHEET.md and draft 9 for `may begin|four conditions|six conditions`: only draft 9:42–44 and :1168 (the four).
