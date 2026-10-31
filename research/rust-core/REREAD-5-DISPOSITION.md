# REREAD-5: the dispositions of its findings (PROPOSED, 2026-10-30; adopted, below)

**Adopted (2026-10-30).** The owner adopted N1(a), N2(a) and all three N3 confirmations, and the ten minor findings
*"as mechanical wording, test and runner corrections, provided they do not alter adopted semantics or classifications"*
(recorded whole in [RULINGS.md](RULINGS.md)). His precisions:
- N1: *"F1 did not supersede E1(b)"*: the depth gate first, then the least (line, W) among the chain and structure
  gates' failures, then the whole walk;
- N2: the write-back kept apart from output, receipts and traces, and *"not a new semantic execution path or a change of
  authority"*;
- N3: W5's narrow reading kept explicit in draft 6 and its tests; the six kinds kept; interrupted runs retained and
  counted, and never used toward acceptance.

They are applied in draft 6, the checker, the runner and SHEET.md's Amendment 5. The text below is kept as it was
proposed. *[Note, 2026-10-30, REREAD-6's M9: L1's row below proposes that draft 5's section 8 be corrected in place.
It was not: drafts stay as they are written. Its correction is draft 6's section 8.]*

**Status.** Proposed, not adopted. These dispose of the 14 findings in [REREAD-5-REPORT.md](REREAD-5-REPORT.md), the
re-read of LAW-FORMAT-0 draft 5 (sha256 `f6e871b9…`), its checker (`97df27a1…`), the reference runner (`d55ce756…`)
and SHEET Amendment 4 (`b0400caf…`). Nothing changes until the owner rules. He answers ASK N1, N2 and N3. Then:
- draft 6 applies every DRAFT item and his answers;
- the checker, `plant_reverts.py` and `ref_run.py` are amended to match;
- SHEET.md gains Amendment 5, and the files they fix are made again;
- a fresh independent re-read follows.

No core code is written before its findings are resolved. In his words: *"No Rust-core implementation,
production-source changes, gate or release changes, commit, or push is authorized. Phase 0 remains the scope."*

**What the re-read found holds** (MEASURED there; the claims below re-run here):
- **The three gates** come before any walk and recurse over nothing. On trees of 300,000 clauses failing each gate,
  the time is linear.
- **Once they pass, the walk reaches every clause exactly once.** The coverage assertion never fired on 220,000
  fuzzed laws, about 89,000 of which reached the walk, nor on 25 hand-built odd cases.
- **Every frozen file reproduces byte for byte.** This includes a full regeneration of `r6-reference.txt` (21
  minutes), and 422 mutants re-run through `ref_run.py`, every row the same.
- **R2b's expected refusals are section 8's.** One twin of each of the 15 kinds was checked by hand against sections
  2, 3 and 8.
- **The budget positions hold:** 40 runs at every B, 0 mismatches.
- **No limit on chains:** chains of 100,000 are accepted.
- **Draft 5 broke none of the B1 requirements.**
- **W11's change is equivalent, as recorded.** The two rules differ on none of 28,934 fuzzed laws.

**What it found wrong, by area:**

| | findings |
|---|---|
| the gates' precedence | **L1 (MAJOR)**: the precedence frozen as "derived from the specification" contradicts the adopted E1(b) text, which the derivation never cites. L6: two same-line ties unplanted |
| R6 and the runner | **L2 (MAJOR)**: the adjudicator gets too little of the document. **L3 (MAJOR)**: `classify`'s inputs are left to the harness, and the runner's own faults read as reference crashes. L5: the runner against its docstring |
| R2 | **L4 (MAJOR)**: R2 has no observable: the core writes no re-encoding |
| the format's text | L8 (W5 narrowed without a tag), L9 (the final `)` and items with no space), L10 (EMPTY-BLOCK under a W4 chain), L11 (allocation guesses), L14 (a step of section 7) |
| the protocol's text | L7 (structure failures partly planted), L12 (K9 and K14 against his proviso), L13 (R8's exceptions) |

**The report's count is right:** 0 BLOCKER, 4 MAJOR (L1–L4), 10 MINOR (L5–L14), 14 in all. By re-read, the findings
have run 17 (F), 19 (G), 15 (H), 17 (J), 16 (K), 14 (L).

**Which findings are mine:**
- **L1.** I wrote, in RULINGS.md's "As kept", draft 5 and Amendment 4, that no adopted rule orders one gate before
  another. The E1(b) text he adopted does: *"If any clause fails, the least such line is reported as W14, and no
  W4–W13 check is made."* I checked F8's words and his E1 bullets, not the option text "Adopt (b)" adopted. It is the
  fourth claim of mine about a rule or the walk that a re-read has refuted (H1, J1, K1, L1).
- **L3, L5:** my runner, and its docstring's undefined "last line".
- **L4:** R2's wording is mine, from the sheet he accepted. The gap was there from the start.
- **L8:** I narrowed W5 to match the checker and did not tag it or put it to him.
- **L12:** my sentence that K9 *"changes no class"*, which cannot be shown.
- **L13:** I wrote K12's R8 rule and section 10's 60-second rule, and did not reconcile them.
- **L2, L7, L9–L11, L14:** text and plants of mine.

**How each finding was checked.** Each concrete claim was run again here, read-only (scratch `rr5_check.py`):
- through `format_check.read`;
- through a copy of the checker changed in memory, which reports the least W14 line whenever one fails (E1(b)'s
  text);
- through `ref_run.py` in fresh processes, its outputs given to `classify` both as the generator filters them and as
  the raw last line.

| | severity | finding | re-run here | disposition |
|---|---|---|---|---|
| L1 | MAJOR | the frozen precedence contradicts the adopted E1(b) text | **CONFIRMED.** `REREAD-3-DISPOSITION.md:93`, option (b), adopted as *"E1 — Adopt (b)"*. Under its text, precedence plant 1 gives W14 line 28 (frozen W4 line 3) and plant 4 W14 line 28 (frozen W7 line 3); plants 2, 3 and 5 are the same either way | **ASK N1**. And **DRAFT**, whatever he rules: RULINGS.md's "As kept", draft 5's section 8 and Amendment 4 are corrected in place with a note, so that the rule reads as proposed and frozen for evidence, never as derived |
| L2 | MAJOR | R6's adjudicator gets only sections 2–4 and 8 | **CONFIRMED** by the text: W8's scope rests on section 5's "checked at", W4's labels and W6's mode on section 6, W8's numbering on section 7 | **DRAFT** (Amendment 5): the reader gets the whole of the exact draft the core was built from, named by sha256, and adjudicates against section 8 as that draft states it |
| L3 | MAJOR | `classify`'s inputs left to the harness; the runner's faults read as reference crashes | **CONFIRMED.** The raw last line of a law-mode run on Windows is empty, and turns RESULT into NO-REFERENCE-RESULT. No arguments, a budget of `1e6`, and a missing input each exit 1 and class NO-REFERENCE-RESULT | **DRAFT:** `classify` takes each run raw, as (exit status, stdout bytes, stderr bytes) or TIMEOUT, and reads its lines itself: CR LF made LF, the last line that is not empty. The runner checks its own arguments before anything runs. A runner fault prints `RUNNER-FAULT <reason>` as its last line on stderr and exits 3: a bad argument, an unreadable input, decoder1 holding a plant, an interrupt, or a text the front end refuses. `classify` raises on a runner fault. It is never a class of a case: the experiment stops there, and is void whole, as K14 says of an interrupt |
| L4 | MAJOR | R2 has no observable | **CONFIRMED** by the text: section 10's interface writes no re-encoding | **ASK N2** |
| L5 | MINOR | the runner against its docstring | **CONFIRMED.** `FRONT-END-REFUSED` exits 0 and classes NO-REFERENCE-RESULT. `SystemExit` is re-raised past the handler. A budget of `-1` gives a RESULT (`RUN STOPPED ops 0`) | **DRAFT**, with L3: a text the front end refuses is a runner fault; a `SystemExit` inside the reference is caught like any other exception (`REFERENCE-EXCEPTION builtins.SystemExit`); BUDGET is `none` or a canonical decimal, no sign and no leading zero; the usage path is documented |
| L6 | MINOR | two same-line ties with the depth gate unplanted | **CONFIRMED.** A clause 25 deep whose own If names 99: frozen W4 line 27, depth first W14 line 27. The same with an inline `while`: frozen W7 line 27, depth first W14 line 27 | **DRAFT** with N1: both planted, with what N1's answer gives |
| L7 | MINOR | three structure failures are not planted against an earlier walk failure | **CONFIRMED** here for the three probes (a shape failure, an orphan, an empty block, each on line 4 behind a W8 on line 3): W5 line 4. That moving each alone into the walk changes no plant is the report's measurement, not re-run | **DRAFT:** the three probes planted; `plant_reverts.py` undoes each alone |
| L8 | MINOR | W5 narrowed in draft 5, untagged and not put to him | **CONFIRMED.** A `say` with a child, named only by an inline if's block, gives W5 line 3 | **ASK N3**, with the tag added in draft 6 either way |
| L9 | MINOR | the final `)`, and items with no space between them, readable two ways | **CONFIRMED.** The checker tests the line's last byte (`ln.endswith(")")`); `(say(lit int 1))` and `(str"a")` give W3 | **DRAFT:** section 2 says the final `)` is the line's last byte. Section 1 says items are separated by spaces, parentheses and a string's quotes alike, so a form written with no space, or with two, parses (W2 holds) and W3 refuses its spacing |
| L10 | MINOR | are the clauses a W4 chain's block names subject to EMPTY-BLOCK? | **CONFIRMED** (W5 line 3, the checker's reading) | **DRAFT:** section 8 says it. A chain's existing names count as names for both of W5's rules, the children allowed and EMPTY-BLOCK. That follows the standing rule that only a check needing the missing clause is not made |
| L11 | MINOR | allocation guesses: HashMap's random seed, the standard library's own temporaries, CapacityOverflow, the receipt's buffer | **CONFIRMED** by the text (NOT MEASURED: no core) | **DRAFT** (section 0): a `HashMap` only with a hasher of fixed keys the core writes, and no output depends on any map's iteration order. "The run" means the law's execution: allocations sized by the command line alone are outside the rule. `TryReserveError::CapacityOverflow` is a failed allocation. The receipt's buffer reports `output` |
| L12 | MINOR | K9 and K14 against his proviso | **CONFIRMED.** K9 decides cases Amendment 3 left undefined: two LOAD-REFUSED runs with different (W, line), or two RESOURCE-EXHAUSTED runs with different kinds, are now UNSTABLE-CORE. K14's voiding stands in for E3's CORE-FAULT where an interrupt reaches the core, and says nothing of keeping the voided records | **ASK N3**. And **DRAFT**: RULINGS.md's sentence that K9 *"changes no class"* is corrected in place with a note; voided runs are kept and counted (his condition 6) |
| L13 | MINOR | R8's exceptions conflict with Amendment 4 and section 10 | **CONFIRMED** by the text (SHEET :484 against :303; draft 5 :719 against SHEET :528-530; the arbiter's `run` records no stdout and starts no process group) | **DRAFT:** Amendment 5 and section 10 state R8's exceptions together. R8's reference is the arbiter's own, not `ref_run.py`. Its core runs under the arbiter's `run`: the 600 s stop is EXTERNAL-TERMINATION for R8 alone; stdout is not recorded and there is no process group, and R8's records say so |
| L14 | MINOR | section 7's "only once" omits a step | **CONFIRMED** by the text | **DRAFT:** no `while`, `for` or procedure clause is named by a block, since a block names its arm's own clause, the If itself or an absorbed clause (W5), so no clause's children are two sequences |

## The questions for the owner

### ASK N1 (L1, L6). The gates' precedence: E1(b)'s text, or the least (line, W) among all three?

He left the order open in F1: *"Preserve any validation precedence already required by the specification. If the
specification does not determine the order, propose and freeze one explicitly before the next evidence run; do not
silently treat Draft 4's order as authoritative."* The adopted E1(b) text requires the depth gate first: *"If any clause
fails, the least such line is reported as W14, and no W4–W13 check is made … one with an earlier W4–W13 failure now
reports W14."* The chain and structure checks (W4, W5, W7) are W4–W13 checks. That sits beside his F1 remark that draft
4's order (depth, then chains) was *"the author's choice, not an adopted ruling"*.

| | what it entails |
|---|---|
| **(a) E1(b)'s text: depth first, then the least (line, W) between chains and structure** | Phase 3 reports the least W14(a)/(b) line whenever any clause fails depth. Otherwise it reports the least (line, W) among the chain gate's and the structure gate's failures. Between those two no adopted rule orders, so F8's rule governs them. **It preserves the adopted text**, as F1 asks. It is also what a core can do most simply: compute depth, stop if it fails, then check chains and structure together. **What changes:** precedence plants 1 and 4 expect W14 at line 28. L6's two ties expect W14 at line 27. It is pinned against every sequential order and against draft 5's rule (plants 3, 5 and the ties) |
| (b) draft 5's rule: the least (line, W) among all three gates | It keeps F8's one rule for every gate failure, and reports the earliest line whatever its gate. It supersedes E1(b)'s sentence, so it needs his word that F1 replaced it. **What stays:** draft 5's plants as they are; L6's two ties expect W4 and W7 at line 27 |

Recommended: **(a)**. His F1 asks to preserve the precedence the specification already requires, and E1(b)'s adopted
text requires the depth gate first. Choosing (b) would need him to say F1 superseded that text.

### ASK N2 (L4). How is R2 observed?

R2 predicts that the core *"re-encodes the law bytes it read exactly"*. But section 10's interface writes no
re-encoding. A core that runs every law correctly, yet drops a part no run reads (a name, say), would pass R3 and R4
and break section 9's round trip unseen.

| | what it entails |
|---|---|
| **(a) a write-back mode** | Section 10 gains `rust-core --write-back LAW OUT`. The load checks run; on a pass, OUT receives the bytes the core writes back from what it read, and the exit is 0; on a refusal, the load refusal's row. R2 compares OUT with LAW byte for byte on every text, and R2b's twins never reach OUT. **It observes the round trip directly**, as ruling 2 asks of the format (*"Exact reconstruction from law bytes, including the round-trip requirement"*). It costs the author a writer, which section 9 already obliges |
| (b) R2 restated | R2 becomes three things already measured: the core accepts each of the 298 (R3), refuses each twin (R2b), and prints as the law seal the SHA-256 of the bytes it read. It then no longer shows that the core keeps every written part, and its record says so |

Recommended: **(a)**. Without a written re-encoding, nothing observes the round trip, and the round trip is one of
ruling 2's three obligations.

### ASK N3 (L8, L12). Three readings that touch his proviso, to confirm or reverse

His proviso on the thirteen corrections: *"provided they do not change the adopted format rules or evidence
classifications"*. Each of these decides something the earlier text left open:

| | the reading draft 5 or Amendment 4 made | the other way |
|---|---|---|
| L8, W5's "named by a block" | only the block of an If that is a clause's statement names a clause. An inline `if` fails W7, and its parts name nothing (G8's adopted *"Their parts are not walked, numbered or checked"*). The checker always read it so | any block names its clause, inline ones included (draft 4's words). Then such a clause's children are allowed, and only W7 is reported, at the inline if's line |
| L12, K9 | two runs of a case that differ in a result outside the compared classes (two LOAD-REFUSED with different W or line, two RESOURCE-EXHAUSTED with different kinds) make the case UNSTABLE-CORE, which fails | such runs are stable by class, and differences there are recorded only |
| L12, K14 | an experiment interrupted is void whole and run again; no single case is voided. Draft 6 adds that every voided run is kept and counted | an interrupt that reaches the core is a CORE-FAULT, as E3's words read, and the experiment goes on |

Recommended: **confirm all three as written**, with K14's voided runs kept and counted (his condition 6). Each closes
a gap toward the stricter reading, and none lets an end pass as a result.

## What follows his answers

1. **LAW-FORMAT-0 draft 6:** every DRAFT item and his answers, each change marked with its finding. Drafts 0–5 and the
   six re-read reports stay as they are.
2. **The checker, `plant_reverts.py` and `ref_run.py` amended to match**, each run twice:
   - N1's precedence, its plants and their undoings, with L6's two ties;
   - L7's three probes;
   - the runner's raw `classify`, its faults and their exit status.

   `r6-reference.txt` is made again with the amended runner, twice. Its rows should not change, since no mutant run
   meets a runner fault, but that is a prediction until measured.
3. **SHEET.md Amendment 5:** N2 and N3, L2's reading set, L3's and L5's runner rules, L12's voided runs and L13's R8
   exceptions, and the files they fix, each made twice with identical bytes.
4. **A fresh independent re-read.**
5. **No core code** before its findings are resolved.
