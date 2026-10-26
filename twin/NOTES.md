# ØRLǪG OL-0 clean-room twin: notes on the specification

**Status, 2026-10-25 (third round).** `twin.py` now follows SPEC §12 and §13 wherever they reach a canonical
text (it still has no door). The round-3 probes, what §12 and §13 still leave open, and the rules no canonical text
can reach are in `probes3/EXPECTED.md` (`python probe_run.py --dir probes3 --check`, and `--alts` for the other
readings, which are `--alt` names such as `procs-all` or `tree-no-paren`). `--alt lex-lazy` restores the round-2
reading that §13 settled against the twin; `python probe_run.py --check --settled` reads `probes/settled.json`.
The round-2 status below and the round-one record are kept as written.

**Status, 2026-10-25 (second round).** SPEC v0.1 §11 settled every item below with one reading, and `twin.py`
now follows §11. Item 37's default is now the reading that `--alt 37` gave in round one, so `--alt 37` now gives
the round-one reading. What §11 still leaves open, and the probes that test each §11 item, are in
`probes/EXPECTED.md`. The rest of this file is the round-one record, as written.

Written 2026-10-25 by the twin's author. The only things read were `SPEC.md`, `RUNTIME-SPEC.md`,
`src/orlog/numeric_ref.py`, `src/orlog/seal.py` and `twin/inputs/`. Nothing else under the folder was read
or searched, and no expected output was seen. Nothing here says which reading the existing implementation
took: every item is a place where a literal reader could go two ways, and the comparison decides.

## What was built, and what ran

- `twin/twin.py`: `python twin.py [--alt N,N...] PROGRAM.orl LAW_SEAL TEXT_SEAL OUTPUT_PATH RECEIPT_PATH [TRACE_PATH]`.
  It parses the canonical text (SPEC §1-§4), types and numbers variables, claims and musts (§5), and runs with
  exact operation counting, the event chain and refusals (§6-§8, RUNTIME-SPEC §2-§7). Numbers are
  `numeric_ref.py`'s own functions and seal words / check syllables are `seal.py`'s, both loaded by file path
  so that no other module of the package runs. Standard library only. Exit 0 for a completed or refused run,
  1 for a compile refusal (G2), 2 for a usage error or an unreadable file.
- `twin/run_all.py`: runs every program of `twin/inputs/manifest.json` into `twin/out/` as `NAME.out`,
  `NAME.receipt` and, as an aid to comparison, `NAME.trace` (RUNTIME-SPEC §5 trace lines).
- `--alt N,...` flips the NOTES items 15, 18, 24, 35, 36, 37, 52, 53, 54 and 57 to their other reading, to
  test whether a disagreement is explained by that item. Without it the twin's own choices hold.

Run here (Windows, Python 3.14.5), MEASURED: 23 of 23 programs produced a receipt; 10 COMPLETED (aztec,
chaos, collatz, gcd_certificate, leapfrog, legal, phrases, plankton, symbols, words) and 13 REFUSED, each
`refuse-NAME` with the code its name says. Two runs gave byte-identical files. `words`, `symbols` and
`phrases` (one law seal) gave receipts identical except for the `text-seal` line. Every given text seal equals
the sha256 of its file. Sanity of the values (not of the counting): Aztec 2, 8, 64, 1024 tilings; Collatz 111
steps, peak 9232; leapfrog returns bit for bit to its start. Ops and events of `legal` (129), `gcd_certificate`
(791, certificate cost 763 = 38 Euclid steps of 20 ops plus the last test of 3), `chaos` (21031) and the 13
refusals were counted again by hand from the readings below and agree. That shows the twin is consistent
with its own readings, not that the readings are the intended ones.

Not done by the twin: the door (§10; the input is taken to be canonical text already), the law's bytes (§9;
the law seal is taken as given), and LITERAL-ROUNDED notes (computed nowhere, printed nowhere).

## Readings that change the given inputs' receipts

MEASURED on the twin: each line is the twin rerun on all 23 inputs with `--alt N`, compared with its default.

| item | other reading | inputs whose receipt changes |
|---|---|---|
| 18 | an absorbed Otherwise arm names the chain's If clause | aztec (trace-head) |
| 24 | a Define's `unless C` counts no `not` | legal (ops 129 → 121) |
| 35 | `and`/`or` always evaluate the right operand | aztec (REFUSED INDEX-OUT-OF-RANGE at clause 17, ops 164); legal (ops 129 → 136) |
| 36 | `-` on a literal is a negative literal (0 ops) | chaos (21031 → 21030), leapfrog (168078 → 168077), refuse-negative-sqrt (4 → 3) |
| 37 | `is not E` (equality) is one `!=` | aztec (809980 → 792268), collatz (1276 → 1164), gcd_certificate (791 → 752, and the claim's ref cost) |
| 52 | each RULE-CONFLICT comparison counts | refuse-rule-conflict (ops 3 → 4) |
| 53 | event E carries the index k−1 | aztec, leapfrog (trace-head) |
| 54 | event E carries the raw slot, without the tag byte | aztec, leapfrog (trace-head) |
| 57 | no LF after `end` | every receipt (its last byte) |
| 15 | `Unless C` counts no `not` | none (no input has Unless) |

Item 26's other reading (no filler `the` in `Let the n be 27.`) would refuse phrases.orl at compile time; the
manifest gives phrases the same law seal as words, so the existing implementation accepted it. Every other
item below is invisible on these 23 inputs: it changes only programs that none of them is.

## General

**G1. Preamble: "Two runs of one law agree only if both are byte-identical" cannot mean the whole receipt.**
The receipt carries `text-seal`, which differs between texts of one law (words, symbols and phrases share a law
seal and have three text seals), and `backend`, which RUNTIME-SPEC §7 exempts. Readings: (a) "both" = the
output bytes and the receipt; (b) the output and the receipt without its `text-seal` and `backend` lines.
(a) contradicts §9 and RUNTIME-SPEC §7, so the comparison has to use (b). Nothing to choose in the twin.

**G2. What a compile refusal produces is unspecified.** The receipt needs a law seal, which a refused program
does not have, and RUNTIME-SPEC §1 defines exit status only for runs (0) and unopenable files (2). Readings:
(a) a receipt with some status line; (b) no receipt. Chose (b): nothing is written, `twin: compile refused
CODE clause N line L: detail` goes to stderr, exit 1. A usage error also exits 2, which RUNTIME-SPEC §1
reserves for a file that cannot be opened.

**G3. The order of compile refusals is unspecified.** A program with two faults can be refused with two
different codes by two conforming implementations. Chose: lines in order (within a line: line form, then the
statement's syntax, then the check suffix, then numbering); then one pass over the clause tree in document
order (per clause: EMPTY-BLOCK / UNEXPECTED-CHILDREN, then ORPHAN-OTHERWISE and the placement codes, then
types and names in textual order, expression before declaration); PRIORITY-CYCLE at the last Define of the
name; SEAL-MISMATCH last, since it needs the law.

**G4. §7 "Add 1 to ops immediately before each of the following": before or after the operation's operands?**
Some entries say "after" explicitly (`item … of` after its index, list construction after its operands,
`and`/`or` after the left operand, concatenation after its parts), which can be read two ways: (a) they are
clarifications, and every count falls just before the operation is applied, after its operands (post-order);
(b) they are the exceptions, and the other operations count before their operands are evaluated
(pre-order). Chose (a), with the one stated exception of a rule use (§6: count first, then the provisos). Only
the ops at a refusal can differ: `Say (7 divided by 0) plus 1` refuses at ops 2 under (a), 3 under (b).
No input refuses inside a nested operand, so the inputs agree under both.

## §1 Lines

**1. "Blank line".** (a) only the empty line; (b) also a line of spaces. Chose (b). Canonical text has no
trailing spaces (§10), so the case should not arise; a twin that refused it would be stricter, not wrong.

**2. The prefixes `Title:`, `Note:`, `Sealed:`.** Not said: whether they match case-insensitively (§2's
keyword rule is about tokens inside a statement), whether a space must follow the colon, whether the free text
may be empty. Chose: exact case; `Title:` alone or `Title: text` accepted, `Title:text` refused LINE-FORM;
the same for `Note:`.

**3. A second Title, or a Title after a clause: no code is named.** (a) LINE-FORM ("any other line"); (b) some
other code. Chose (a).

**4. Contradiction: `Note` "may appear anywhere", yet `Sealed` must be "the last non-blank line".** A Note after
the Sealed line is allowed by the first rule and refused by the second. Chose: refused, LINE-FORM (also for
two Sealed lines), naming the Sealed line. The code (LINE-FORM or SEAL-MISMATCH) and the line named are
both guesses.

**5. A malformed Sealed line.** "Four proquints" does not say how they are joined; §9 joins seal words by `-`.
(a) a line that is not four `-`-joined proquints is LINE-FORM; (b) it is SEAL-MISMATCH. Chose (a): only a
well-formed line that differs from the seal words is SEAL-MISMATCH. Space-joined proquints are LINE-FORM.

**6. Labels with leading zeros, and `§1.`.** "Dot-separated decimal integers" admits `§01` and `1.02.`.
(a) compare parts as integers (`§01` is 1); (b) as text, or refuse. Chose (a). `§1.` (section sign and a final
period) is neither listed form and is LINE-FORM.

**7. "A label, one space, then a statement".** (a) exactly one space; (b) one or more. Chose (a): a statement
that begins with a space is LINE-FORM. A statement of only its period is LINE-FORM.

**8. No refusal code exists for a malformed statement** (an expression that does not parse, a token that begins
no token, a missing keyword, trailing words). §5's list has no SYNTAX code. Chose LINE-FORM: the line is not
"a label, one space, then a statement". Every syntax refusal of the twin is therefore LINE-FORM.

**9. Mixing the two label forms (`§1` and `2.`) in one program** is not addressed. Chose: allowed.

## §2 Tokens

**10. Whether tokens must be separated.** "Spaces ... skipped" does not require them. Chose longest match per
position with no separator needed (`3*n+1`, `x1` is one word, `2times3` is `2` then the word `times3`).

**11. `:` is an op token that no production uses.** Any `:` in a statement is therefore LINE-FORM. If it was
meant for something (a label separator, a Title inside a clause), that is missing from §3-§4.

**12. Reserved words and case.** "Keywords match case-insensitively; identifiers are case-sensitive" leaves
open whether `Sum` or `ITEM` may be identifiers. Chose: reservation is case-insensitive, so `Let Sum be 2.`
is LINE-FORM.

**13. `this law's seal` and the word `s`.** It tokenizes as `this law ' s seal`. `s` is in neither the reserved
nor the "not reserved" list, and gcd_certificate uses `s` as a variable. Chose: the phrase is the fixed
five-token sequence; `s` is an ordinary identifier elsewhere.

**14. "No line break" in a text literal.** A CR inside a literal: chose LINE-FORM (canonical text has no CR).

## §3 Statements

**15. Does `Unless C` count a `not`?** "As If with `not C`": (a) the condition is the expression `not C`, so
+1 for the `not`; (b) the polarity is flipped for free. Chose (a). No input has Unless (`--alt 15`).

**16. `Unless` forms.** `If` lists `[then]` and `[; otherwise[,] S]`; `Unless` lists neither. (a) literal: neither
is allowed with Unless; (b) "as If" brings both. Chose (a): `Unless C, then S` and `Unless C, S; otherwise S`
are LINE-FORM. A following `Otherwise, ...` clause does attach to an Unless chain.

**17. An else-if arm with an inline otherwise** (`Otherwise, if C, S; otherwise S`) is not listed. Chose literal:
LINE-FORM.

**18. Which clause an absorbed Otherwise arm names, in events and refusals.** "Otherwise clauses that are
absorbed into an If chain are not separate statements" and "every refusal names the clause whose statement is
executing" read two ways: (a) the arm's own clause names its condition and its inline statement; (b) the
whole chain is one statement, so the If (or Unless) clause names everything in it except the children of
block arms. Chose (a): it names the line where the text is. CHANGES aztec: its events at clauses 32
("Otherwise, set mode to 2.") and 33 ("Otherwise, if the length of placed is 0, set mode to 0.") would carry 19
and 16 under (b), so its trace-head differs (`--alt 18`).

**19. The While bound.** A decimal literal (`at most 5.0 times`): LINE-FORM or FUEL? An integer literal above
2^63−1: LITERAL-RANGE or FUEL? Chose LINE-FORM for a decimal and FUEL for any integer outside 1…2^62.

**20. "A name may not begin with a statement word".** "Statement word" is undefined, and no code is given.
Chose the 19 words that decide a statement (let set increase decrease say if unless otherwise while for to
perform it we notwithstanding define append remove decimals), compared lowercased, and LINE-FORM.

**21. A bare procedure name can be `do the following`.** `If C, do the following; otherwise S` is not the block
form (text follows it), so it parses as an If whose inline arm performs a procedure named "do the
following", refused UNKNOWN-PROCEDURE unless such a procedure exists (`To do the following, do the following.`
parses, and then that If performs it: run here). Chose: as parsed. The grammar should forbid the name.

**22. Performing a procedure before its definition at top level.** The rule is stated for procedures performing
procedures. (a) refused everywhere (PERFORM-BEFORE-DEFINITION); (b) allowed at top level, since every
procedure is known by then. Chose (a), by the code's name.

**23. `Notwithstanding §a[, §b][ and §c]` has no ellipsis**, unlike `given §a[, §b…][ and §c]`. (a) literal: at
most three references; (b) any number. Chose (a): a fourth is LINE-FORM.

**24. Does a Define's `unless C` count a `not`?** §6 says only "evaluate its proviso". (a) the proviso is
`not C`, +1 (as item 15); (b) free. Chose (a). CHANGES legal: §4 "unless resident is true" is evaluated at
each of 8 uses of `rate`, ops 129 against 121 (`--alt 24`).

**25. A Define with both `, provided that C1` and `, unless C2`.** The combination, its evaluation order,
short-circuit and counting are unstated. Chose: `C1 and not C2`, counted as an `and` (+1 after C1) and, only
when C1 is true, C2 and +1 for the `not`. No input has both.

**26. The filler `the` in statement positions.** §4 states the rule for expressions ("a filler before an
identifier"), while §3 writes `Let X be E`; phrases.orl needs `Let the n be 27.` Chose: an optional `the`
before every identifier position (Let, Set, Increase, Decrease, Append and Remove targets, the For counter,
the defined name, `length of`, `item … of`) when the next word is not reserved. It is not applied to
procedure names (`Perform the step` names "the step"), which are not identifiers.

**27. The index of `Set item E of X` and `Increase item E of X`.** The table says E (an expression); the atom
writes `"item" unary "of" X`. (a) a full expression, ending at `of`; (b) a unary, as in the atom. Chose (a).
Every index in the inputs is a name, a literal or parenthesized, so both agree on them.

**28. A non-inline form inside an arm** (`If C, define …`, `If C, while …`): not an inline statement, no code
named. Chose LINE-FORM.

**29. What LOOP-VARIABLE covers.** "Read-only": chose Set, Increase and Decrease of the counter, checked
before the value's type; `Set item … of i`, `Append … to i` and `Remove … of i` are TYPE (the counter is not a
list).

## §3 and §5: oracles and their targets

**30. CERTIFICATE-TARGET: "an earlier, executed, non-procedure, non-define, non-claim clause".** "Executed"
and "non-procedure" are unclear: is "non-procedure" not a To clause, or not inside a procedure body? Is
"executed" a clause with a run-time statement, or one guaranteed to have run before the claim? Is an absorbed
Otherwise clause (no statement of its own, no "own +1" to start the counter at) allowed? Chose: the target's id
is less than the claim clause's; it is not a To, Define, Decimals or claim clause; it is not an absorbed
Otherwise; clauses inside procedure bodies are allowed (their counter grows each time they run).

**31. AGREEMENT-TARGET is named and never defined.** Chose, as a guess: both references exist, are distinct,
and each meets item 30's rule. `agreement of` sets the claim's ref clause and ref cost to 0 0.

**32. PREMISE-TARGET and inline claims.** Is an If clause whose arm is a claim "a claim clause"? Chose: no;
only a clause whose own statement is a claim. Premises may name later claims (plankton does) and the claim
itself.

**33. A reference to no clause.** In `notwithstanding`, `given` and `certificate of` it could be UNKNOWN-CLAUSE
or the specific code (it is "not a Define of the same name", "not a claim clause"…). Chose UNKNOWN-CLAUSE
everywhere.

## §4 Expressions

**34. "Can begin an expression" (list literals).** (a) the first tokens of `expr`, which include `not` and
`it`; (b) those of a list item (`sum`). Chose (a), literally: `the list 1 and not b` continues the list and is
LINE-FORM, where (b) ends the list and gives TYPE (a list `and` a Bool).

**35. `and`/`or` short-circuit only by implication.** The one hint is "counted after its left operand, whether
or not the right operand is evaluated". Chose short-circuit (the right operand is not evaluated when the left
decides). CHANGES aztec, which completes only under it (otherwise `item pos of valid` with pos = cells+1
refuses INDEX-OUT-OF-RANGE at clause 17), and legal's provisos (ops 129 against 136) (`--alt 35`). A rule's
Defines are all evaluated (§6), short-circuit applying only inside each proviso.

**36. Unary minus on a literal.** The grammar has no negative literals, so `-4` is the negation of 4. (a) a
counted negation (+1); (b) a negative literal, 0 ops. Chose (a). CHANGES refuse-negative-sqrt (`Let a be -4`,
ops 4 against 3), leapfrog (`-0.5`) and chaos (`-2.0`), one op each (`--alt 36`).

**37. `is not E` (equality) costs two operations.** "`is not less than` (and its kin) means `not (a < b)`";
"its kin" is not enumerated. (a) every `is not` form is `not (…)`, the comparison and the `not` both counted;
(b) `is not E` is the single comparison `!=`. Chose (a) (`is not even` is also `not (even)`). The results
agree, NaN included; the counts do not. CHANGES aztec (`mode is not 0`), collatz (`n is not 1`) and
gcd_certificate (`r is not 0`, which also changes the certificate's ref cost) (`--alt 37`).

## §5 Types and static semantics

**38. A decimal literal outside its range has no code.** A Fix literal of 2^31 or more (`3000000000.0`), and a
Float literal whose nearest binary64 is infinite. Chose LITERAL-RANGE for both. For the Float the spec's
"nearest binary64" is itself unclear: by distance it is the largest finite double, by IEEE rounding infinity.

**39. The element type of a list literal is not stated.** Chose: all Bool → Bool; any Float → Float; any Fix
→ Fix; else Int; Bool mixed with numbers, Fix with Float, or any Text or list item → TYPE.

**40. Is an Int promoted to Float exactly or rounded?** "Promoted (a counted operation)" names neither `as a
float` (INEXACT-CONVERSION above 2^53) nor `rounded to a float`. Chose exact. (Int to Fix is `x_from_i`, exact
or OVERFLOW, either way.)

**41. When a promotion is counted.** (a) right after its own operand (an implicit conversion around it, then
the other operand); (b) after both operands, just before the operator. Chose (a). It changes the ops at a
refusal and can change the refusal's code: in `3000000000 plus (1.5 plus 7 divided by 0)` (a) refuses
OVERFLOW (promoting 3000000000 to Fix) and (b) DIVISION-BY-ZERO. No input promotes.

**42. When a list-literal item is promoted.** The same question; chose right after each item.

**43. Identity conversions and `integer part of` an Int.** The table omits `Int as an integer`, `Fix as a fixed`
and `Float as a float`; §5 says `integer part of` takes Fix or Float. Chose TYPE for all of them.

**44. `length of` a Text.** Chose: lists only (TYPE). The runtime has no text length.

**45. Define clauses of one rule with Int and Fix values.** "One type": (a) refused (TYPE); (b) promoted to
Fix. Chose (a).

**46. Which variables a Define's expressions see** is unstated. Chose: the top-level variables declared
textually before that Define (as a procedure body's view).

**47. Name collisions.** "A name that names a rule or a procedure": (a) all rule and procedure names, wherever
defined, so a Let before the first Define of the same name is REDECLARED; (b) only those defined textually
before. Chose (a). Procedure names are lowercased, so a variable is compared with them lowercased (`Let Go be 1`
after `To go` is REDECLARED); rule names are case-sensitive, like identifiers.

**48. `Set`, `Increase`, `Append` or `item … of` on a rule name.** UNDECLARED (it is not a declared variable)
or TYPE? Chose TYPE.

**49. DECIMALS-PLACE.** "At most once, top level, before any decimal literal": chose one code for all three
faults, a second `Decimals are fixed` included, and "before" textually, procedure bodies included.

**50. `zero`, `positive`, `negative` on −0.0 and NaN.** By IEEE comparison with zero, or by the sign bit? Chose
comparison: −0.0 is zero and not negative; NaN is none of the three.

## §6 Rules

**51. The transitive closure of `notwithstanding`: over all Defines, or over the applicable ones?** If A
overrides B and B overrides C, and A and C apply but B does not, (a) the static closure lets A override C;
(b) a closure over the applicable Defines does not, so A and C are both compared. Chose (a). legal comes out
the same under both.

**52. Are RULE-CONFLICT comparisons counted?** §6 counts only step 1; §7 counts "every comparison". Chose: not
counted. CHANGES refuse-rule-conflict (ops 3 against 4) (`--alt 52`).

## §7 Dynamic semantics

**53. The index carried by event E.** `orl_ev_item(c, var, uint64_t index, …)`: (a) the language's k
(1-based); (b) the slot k−1. Chose (a). CHANGES aztec and leapfrog (trace-head) (`--alt 53`).

**54. "Value encoding of the slot under tag"** (event E). (a) the value encoding of RUNTIME-SPEC §5, with its
tag byte (`'I'` + 8 bytes, `'B'` + 1 byte), as event P's "value encoding" plainly is; (b) the raw slot. Chose
(a). CHANGES aztec and leapfrog (trace-head) (`--alt 54`).

**55. Increasing a Fix or Float variable (or item) by an Int.** The statement table (`+1; evaluate E; +1;
add`) does not show the promotion. Chose: its +1 falls inside "evaluate E", before the add's +1.

**56. A claim never evaluated.** Its ref clause and ref cost are "stored (latest)" at evaluation; before any,
chose 0 0, even for a certificate oracle.

**57. Whether the receipt's last line `end` ends with LF.** RUNTIME-SPEC §7 shows the lines, §1 says "LF only".
Chose an LF after every line, `end` included. CHANGES every receipt's last byte (`--alt 57`).

**58. A certificate's cost counter when its statement refuses** is never grown (the run stops). Unobservable:
counters appear only through claims.

## RUNTIME-SPEC and numeric_ref

**59. Nothing defines the exact conversion `as an integer` numerically.** `numeric_ref.py` and RUNTIME-SPEC §2
have `x_trunc`, `x_round`, `f_trunc` and `f_round` only; the checked forms (Fix: INEXACT-CONVERSION unless
the fraction bits are zero; Float: NOT-FINITE, then INEXACT-CONVERSION, then OVERFLOW) exist only in SPEC
§8. The twin follows SPEC §8, in that order.

**60. SPEC §8 omits NEGATIVE-SQRT** for an Int or a Fix ("the square root of an Int is ⌊√n⌋");
`numeric_ref.py` refuses it, and the twin follows `numeric_ref.py`, as RUNTIME-SPEC directs.

## §9 and §10

**61. The law seal is taken as given.** The twin cannot compute it (`sema.py`'s `law_bytes` was not read). A
Sealed line is compared with the seal words of the given law seal, so a wrong given seal would refuse a good
program SEAL-MISMATCH. No input has a Sealed line.

**62. Unobservable in a run:** the Title's dropped final period, the Notes, the label spelling, the check
suffixes, and the door's REPAIR/NOTE/REFUSE records.
