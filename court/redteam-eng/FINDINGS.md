# Engineering red team: findings (saved verbatim by the judge from the red team's final message)

The red team's Write tool refused report files from subagents, so it sent this text in its final message. It is saved
here unchanged, apart from this header. Statuses are the red team's own, from its re-run at 17:20.

**Setup.** Runs were made from R with `PYTHONHASHSEED=0 PYTHONUTF8=1` on Windows 11, Python 3.14.5, clang 22.1.8 and
rustc 1.96.1. Everything is MEASURED on this host. `python -B court/redteam-eng/run_all.py` repeats every command and
writes the outputs to `observed/`. The tree changed between 16:56 and 17:15 while the author fixed things, and each
status below is from the 17:20 re-run.

*Redacted 2026-10-26, by the owner's word (prosecutor F42): in 15 captured observations under `observed/` and
`observed-1650/`, the home folder's path is replaced by `{session}` (the session folder) or `{python}` (the Python
installation). Nothing else in them changed, byte for byte. The captured paths remain in this repository's history,
through commit 95dac79.*

## E1, defect: FIXED 17:08
- **Reproducer:** `E1_eq_promotion_crash.orl`: `§1 Let x be 0.5.` / `§2 Say x + 1 = 1.5.`
- **Command:** `orl.py run … --backends python,c99`
- **First seen:** `KeyError: ('promote','fix')`. Also, `E1b_eq_note_twice.orl` printed its LITERAL-ROUNDED note twice.
- **Should:** SPEC §5 promotes an Int for `=`/`!=`, so the program prints `true`.
- **Where:** sema.py's `==`/`!=` branch typed both operands, then `unify()` typed them again and hit its own
  `Conv('promote')`. The conversion table has no `promote` key.
- **Scale:** 50 of 600 unsteered random programs crashed here.

## E2, defect: FIXED 17:07
- **Reproducers:**
  - `E2a_rule_in_procedure.orl`: a rule used inside a To body.
  - `E2b_rule_uses_rule.orl`: `Define s as r plus 1`.
- **First seen:** `AttributeError: 'Lowered' object has no attribute 'rule_fn'`. The reference alone prints 5 and 6
  (`observed/E2a-ref.txt`).
- **Should:** SPEC §5 and amendment 46 allow both.
- **Where:** lower.py:49-58 lowered procedures and rules before assigning `rule_fn`.
- **Scale:** 85 of 600 random programs.

## E3, defect: FIXED 17:08
- **Reproducer:** `E3_hidden_children.orl`: `§3 Otherwise, say "not two".` followed by `§3.1 Say "hidden child".`
- **First seen:** all backends agreed and printed `not two` only, yet the law held
  `(clause 4 3 (say (str "hidden child")))`. `E3b` (`§3.1 Let y be 5.`) crashed in law_bytes with an AttributeError.
- **Should:** SPEC §3 (Blocks) requires UNEXPECTED-CHILDREN.
- **Where:** `_check_children` in syntax.py exempted absorbed clauses.

## E4, defect: FIXED 17:01 (overlaps L17)
- **Reproducer:** `E4_court_inline_claim.orl`: `§2 If x = 1, we claim that x = 1.`
- **First seen:** `orl.py court` raised `AttributeError 'IfS' object has no attribute 'id'`.

## E5, defect: grounding FIXED 17:01 (overlaps L4 and L8)
- **Reproducer:** `E5_court_tautology_certificate.orl`: `We claim that true, by the certificate of §2 under the theorem
  "T"`, with `E5-fixture-ledger.jsonl`, which ratifies the theorem *name* "T" only.
- **First seen:** "check 0 ops / certified clause 2 ops", cheap, no plants declared, GROUNDED.
- **Against:** DOCTRINE edition 1 §3–§4: a tautology airlock is DECORATIVE, and a certificate that accepts anything is
  refused.
- **Now:** UNGROUNDED, but it still reads CHEAPER.

## E6: superseded (overlaps L6)
- **Reproducer:** `E6_court_recompute_certified.orl`. Clause §3.1 runs twice, and the claim recomputes it exactly.
- **Observed:** "check 4 / certified clause 8", read as cheap (now CHEAPER). This fired DOCTRINE edition 1's T3
  falsifier; edition 2 withdrew "cheaper ⇒ different".
- **Remaining point:** R4 compares one evaluation of the check with the clause's counter summed over all its runs, and
  does not say so.

## E7, defect: HOLDS
- **Reproducer:** `arbiter_plants.py` makes the Python backend write three bad receipts:
  - one with CRLF line endings;
  - one with no final LF;
  - one with an extra line, `backend ops 0 trust me`.
- **Observed:** for all three, "byte-identical … False  arbiter: agree ['c99','python'] dissent []".
- **Should:** SPEC says runs agree only if byte-identical; so do RUNTIME-SPEC §1 and §7, and amendment 57.
- **Where:** arbiter.py:58-60. `parse_receipt` uses `splitlines()` and `errors="replace"`, and drops every line that
  starts with `backend `. It is used at line 146 and in `_agree_among`.

## E8, defect: HOLDS
- **Reproducer:** `arbiter_masking.py`, using the self-test's own `reference_truncates_quotient` plant.
- **Observed:** with python and c99, the arbiter says REFERENCE-DISSENT. Adding a Rust backend planted not to compile
  turns it into BACKEND-DISSENT.
- **Where:** arbiter.py:159-166 counts failed builds in `dissent` but not in `compiled_backends`. On a host without a
  working rustc (see E11), every reference dissent is misread this way.

## E9, defect: HOLDS
- **Reproducer:** `E9_door_curly_in_literal.orl`: `§1 Say "Use “followed by” to join".`
- **Observed:** two R-QUOTE-DELIM repairs; all backends agree; the output is `Use  to join`.
- **Should:** SPEC §10 says literal contents are never changed; this is DOCTRINE T6's falsifier.
- **Where:** `_segments` in canon.py (line 127). Inside a literal, any DQUOTES character closes it, including U+2033
  DOUBLE PRIME. QUOTE-BOUNDARY does not fire because the door's own segmentation is stable here. This is the converse
  of L12.

## E10, defect: FIXED 17:07–17:08
- **First seen:**
  - `E10_python_depth_if_chain_110.orl` and `E10b` (40 nested For loops): Python IndentationError, BACKEND-DISSENT.
  - `E10c` (a 3000-arm If chain): RecursionError in the lowering.
  - `E10d` (400 nested For loops): RecursionError in sema.
- **Now:** If chains are lowered iteratively, plus NESTING-DEPTH (24) and LOOP-NESTING (16).

## E11, defect: HOLDS
- **Command:** `orl.py run examples/collatz.orl --backends python,c99,rust --workdir court/redteam-eng/work/ØRLǪG`
- **Observed:** "agree [python] dissent [c99,rust]".
  - C99 exits 2 with `orlog: cannot open file: …\�RLOG\…`. The cause is orlog_rt.h:1281-1306, `fopen` on the narrow
    `argv`, which is in the ANSI code page.
  - Rust: the GNU linker reports `cannot open output file …\xd8RLOG…`.
- **Should:** RUNTIME-SPEC §1 forbids dependence on the host and the environment.

## E12, defect: FIXED (amendment 38; the twin also found it)
- **Reproducer:** `E12_huge_float_literal.orl`.
- **First seen:** OverflowError. **Now:** LITERAL-RANGE.

## E13, defect: FIXED 17:08
- **Reproducer:** `E13_two_seals.orl`: a wrong Sealed line, then the correct one.
- **First seen:** it compiled, and the wrong seal was never checked. **Now:** SEAL-PLACE.
- E13b, a Note after the seal, is allowed by amendment 4, so it is withdrawn.

## E14: withdrawn
Amendment 25 now says what the code does.

## E15, spec gap: FIXED 17:08
- **Reproducer:** `E15_two_oracles.orl`: "by the owner, by computation".
- **First seen:** the law kept only `(computation)`. **Now:** SYNTAX.

## E16, spec gap: partly HOLDS
- `E16a` (`TO greet, DO THE FOLLOWING.`) was refused UNKNOWN-PROCEDURE when first seen; fixed 17:08.
- These are still refused UNKNOWN-PROCEDURE:
  - `E16b`: `,  do`
  - `E16e`: `,do`
  - `E16f`: `do  the`
- `E16c` (a nested To) is refused SYNTAX, not PROCEDURE-PLACE. PROCEDURE-PLACE at sema.py:177 cannot be reached.
- **Should:** SPEC §2 says spaces are skipped, and amendment 10 needs no separator.
- **Where:** the procedure table is built with the regex `^to (.+), do the following\.$` (syntax.py:224-228), while
  the statement parser reads tokens.

## E17, hardening: FIXED 17:08
- **Reproducers:**
  - `E17a`: U+212A KELVIN SIGN in an identifier was repaired by NFC, and the program ran.
  - `E17b`: U+037E was repaired to `;`.
- **Now:** both are refused NON-ASCII-CODE.

## E18, hardening: FIXED about 17:00
- **Reproducer:** `E18_door_not_idempotent.raw` (` Note:" "`) with `door_retraction.py`.
- **First seen:** pass 1 gave `' Note:"\xa0"'` and pass 2 gave `' Note:" "'` with another R-SPACE. `doorfuzz.py` found
  19 minimal counterexamples in 30,000 lines.
- **Cause:** `_context_marker` strips only U+0020.
- **Now:** these lines are refused QUOTE-BOUNDARY, with 0 counterexamples in 60,000 lines.

## E19, hardening: HOLDS
- **Reproducer:** `E19_invisible_in_literal.orl`: U+3164, U+E0041 and U+2028 inside a literal.
- **Observed:** no door event, and the bytes are printed.
- **The inconsistency:** the door refuses U+200B inside literals, but its INVISIBLE set has only 9 code points
  (canon.py:17).

## E20, spec gap: HOLDS
- **Reproducers:** `E20a` and `E20b` are identical except that E20b spells `§02 …, given §02`.
  - Their law-seals differ, jotir-bamop-jugub-ladod against lonap-nahag-jamif-hafig, because the law records
    `(given 2)` against `(given 02)`.
  - `E20c` (`§02`, then `given §2`) is refused UNKNOWN-CLAUSE.
- **Should:** SPEC §9, DOCTRINE T8, and amendment 6 (label parts compare as integers).
- **Where:** sema.py:562 and :565 write the label text, and `by_label` is keyed by the label string.

## E21, hardening: HOLDS (already known: rt_c/NOTES.md finding 8)
- **Reproducer:** `memleak.py`.
- **Observed:** peak commit for C99 is 130, 370 and 691 MiB at N = 5, 20 and 40; Python stays at 113 MiB.
- **Where:** `orl_s_take` copies are never freed (orlog_rt.h:1029).

## E22, hardening: FIXED 17:02
- **Reproducer:** `E22_ratify_non_claim.orl` (`Say "x (claim y"`).
- **First seen:** `orl.py ratify --claim §1` wrote a claim ratification (`observed-1650/E22-first-seen.txt`).
- **Now:** refused.

## E23, spec gap: HOLDS
- The fixes added three refusals that SPEC.md §5 and §10 do not list (`observed/E23-spec.txt`):
  - NESTING-DEPTH (syntax.py:207);
  - LOOP-NESTING (sema.py:257);
  - QUOTE-BOUNDARY (canon.py:194-203).

## E24, defect: HOLDS
- **Reproducer:** `E24_python_depth_and_inside_loops.orl`: 16 nested For loops, inside both new limits, around
  `Say true and (true and (…70…))`.
- **Observed:** the reference, C99 and Rust complete; Python fails with `IndentationError: too many levels of
  indentation`. E24b, with 50 `and`s, passes.
- **Where:** for `and`/`or`, the right operand's code goes inside an if-block (lower.py:308-319). The new limits count
  only clauses and loops.

## E25, defect: HOLDS
- **Reproducers:** `E25_parser_recursion_parens.orl` (120 nested parentheses) and `E25b` (100 right-nested `and`s).
- **Observed:** `orl.py check` raises RecursionError in syntax.py, with no refusal.

## E26, hardening: HOLDS (a regression from the E17 fix)
- **Reproducer:** `E26_false_door_note.orl`: `§1 Let`, then U+2000, then `x be 1.`
- **Observed:** the program is accepted. At L1 C1, a line with no literal, the door notes "LITERAL-NOT-NFC … a text
  literal is not in NFC; kept byte for byte, because it is output", and then repairs the same bytes with R-SPACE.
- **Where:** the `elif` at canon.py:182 now also runs on code segments.

## Fuzzing and other checks
- **Generators:**
  - `fuzz.py` with `fuzzgen.py` writes random valid programs. They use Int, Fix and Float with promotions and
    conversions; comparisons; lists; rules with notwithstanding; procedures; If/Otherwise/Unless; bounded While; For;
    claims with every oracle kind; and musts.
  - `edgegen.py` and `edgegen_rs.py` push every edge value through every unary and binary form.
- **Totals:**
  - 13,308 programs run and 13,134 compared, with 0 disagreements.
  - Before the fixes there were 154 crashes, all from E1 and E2.
  - 600 unsteered programs on the edited tree gave 0 crashes and 0 disagreements.
  - Logs are in `work/fuzz/log-*.jsonl`, and crashing programs in `work/fuzz/hits/`.
- **Also held:**
  - the 2^24 text and list limits agree across the reference and all three backends;
  - 250 generated C programs built with UBSan in trap mode ran with no trap.
- **Not tried:** OUTPUT-TOO-LONG, which needs 1 GiB of output per backend.
- **Disk:** `work/fuzz/w` holds about 40,000 build artifacts (several GB). They can be regenerated and deleted.
