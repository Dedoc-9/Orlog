# REREAD-0: the dispositions of its findings (PROPOSED, 2026-10-30)

**Status.** Proposed, not adopted. These are the dispositions of the 17 findings in
[REREAD-0-REPORT.md](REREAD-0-REPORT.md), the independent re-read of LAW-FORMAT-0 (sha256 `1ae57ee8…`). Nothing here
changes the document yet. The owner answers the two ASK items. LAW-FORMAT-0's draft 1 then applies every DRAFT item and
his answers, and a targeted re-read of the changes follows. No core code is written before that (his condition 1).
*[Note, 2026-10-30, REREAD-7's Y10: adopted. He accepted these dispositions with A1(a) and A2(a), recorded whole in
[RULINGS.md](RULINGS.md). The text below is kept as it was proposed.]*

**How each finding was checked.** Each concrete claim was run again here, read-only, with
`format_check.py`, `decoder1.py` and the reference. The re-reader could run nothing. *Re-run* below gives what that
run showed.

**One discrepancy in the report.** Its verdict counts nine MAJOR and nine MINOR findings. Its list has eight of each:
MAJOR F2–F9 and MINOR F10–F17, with F1 the BLOCKER. These dispositions follow the list.

| | severity | finding | re-run here | disposition |
|---|---|---|---|---|
| F1 | BLOCKER | W1 lets the clause order differ from the tree's pre-order | **CONFIRMED.** The bytes pass `format_check.py`, and the decoded run crashes (`KeyError: 0`) | **DRAFT:** W1 requires clause k's parent to be 0, k−1, or an ancestor of k−1, so clause order is the tree's pre-order; the scope rules then hold as written. Plant: these bytes, refused W1 |
| F2 | MAJOR | the order of ids and "the claim's clause" are ambiguous; the plain reading refuses valid laws | **CONFIRMED.** `§1 If true, do the following. §1.1 Let a be 1. §2 Otherwise, let b be 2.` is accepted by the front end and refused W8 by the checker. The certificate variant is accepted, since the checker already compares with the arm's clause | **DRAFT:** write out the walk that numbers ids: a clause's statement, an If's parts in written order (each arm's condition, then its body, inline or the block's clauses, in that order), then the clause's children. Ids are dense in walk order. "The claim's clause" is section 5's clause of the statement. The re-reader's two laws become fixtures the checker must accept |
| F3 | MAJOR | no depth bounds | **CONFIRMED.** A 300-deep chain of `not` is accepted | **DRAFT:** W14 bounds what the front end bounds: at most 24 label parts, loops nested at most 16 within one body, and an expression depth in the bytes derived from the front end's 64 (promotions and an Unless's `not` added after its check), with the derivation written out for the targeted re-read to check. The core's reader also may not recurse past a fixed stack for any accepted law |
| F4 | MAJOR | `promote` accepted where the front end never writes one | **CONFIRMED.** All three examples are accepted | **DRAFT:** a `promote` stands only where SPEC §5 promotes: one operand of an arithmetic operator, a comparison, `==` or `!=` whose other operand has the target type (exactly one per operator); the stored value of `set`, `change` and `append`; a list literal's items, with at least one item unpromoted. Refuse every other. Plants: the three examples |
| F5 | MAJOR | strings may hold non-scalar code points, and characters the door refuses | **PARTLY CONFIRMED.** The checker already refuses `\u{d800}` and `\u{110000}` (W2), but the document does not say so. It accepts `\u{7f}` and `\u{202e}`, which the front end refuses in a literal (`BIDI-CONTROL`) | **DRAFT** for scalar values: the document states what the checker does (at most 10FFFF, outside D800–DFFF, no leading zero). **ASK A1** for the door's characters |
| F6 | MAJOR | If chains no text writes | **CONFIRMED.** Both examples are accepted; the front end refuses `do the following; otherwise` (SYNTAX) | **DRAFT:** an else in the If's own clause needs exactly one arm, and that arm inline. Each absorbed clause is named by exactly one arm or else of one If. Plants: both examples |
| F7 | MAJOR | the host budget's check positions | **CONFIRMED.** `§1 Let x be 1. §2 Let y be 2. §3 Define r as 3.` under budget 1 stops after 2 operations, at the define clause | **DRAFT:** the check is made before every non-absorbed clause in a sequence, `define`, `procedure` and `decimals` included, and before each inline arm or else statement. Never for an absorbed clause, and never before a loop's iteration. R5's half-budget runs then cover it |
| F8 | MAJOR | the run interface leaves outcomes open | not a claim to re-run | **DRAFT:** a table of every outcome: completed, refused, stopped, load-refused, usage error, unreadable or unwritable file, TEXTSEAL malformed (uppercase included), budget malformed. For each: the files left, the exit status and the exact stderr. Output buffered, so that nothing is written on a stop or a load refusal. A load refusal reports the first failing line, and within it the lowest W. W2 (grammar and atoms) is kept apart from W3 (spacing and order only), so a non-canonical atom has one code |
| F9 | MAJOR | numeric meaning deferred to `numeric_ref.py`; no vectors for `as an integer` | **CONFIRMED** by reading: no `x_as_i` or `f_as_i` line in `vectors/runtime-vectors.txt` | **DRAFT:** for the core, SPEC §8 with RUNTIME-SPEC §2–§3 and the vectors is the definition, and a disagreement with `numeric_ref.py` is a finding. **ASK A2** for the missing vectors |
| F10 | MINOR | the mapping from conversions and comparisons to functions | — | **DRAFT:** add the table (promote fix → `x_from_i`, OVERFLOW; promote float → `f_from_i`; Float's `<= >= > !=` native IEEE; Fix by raw value; Text by bytes) |
| F11 | MINOR | W6 and the literals' mode | the checker already enforces it | **DRAFT:** say it in W6 |
| F12 | MINOR | the empty law | accepted by the front end and by the checker | **DRAFT:** n ≥ 0; give the two-line law; add it as a fixture |
| F13 | MINOR | section 5: rule uses, performed bodies, costs | — | **DRAFT:** as proposed |
| F14 | MINOR | names: rule names are read | — | **DRAFT:** as proposed |
| F15 | MINOR | wording ("all four", `not`'s type, "unpromoted") | — | **DRAFT:** as proposed |
| F16 | MINOR | the seal words as a derivation | — | **DRAFT:** add derivation 19 |
| F17 | MINOR | the context the author lacks | — | **DRAFT:** a section for the core's author: std-only Rust, built by bare `rustc`, its own SHA-256, the vector file's line grammar. The over-claims at the old lines 213-214 and 271 are corrected |

## The two questions for the owner

**A1 (F5). May a text literal (or a name) in the law bytes hold a character the door refuses in a literal?** Those are
C0 and C1 controls, DEL, bidi controls, line and paragraph separators, format characters other than ZWJ and ZWNJ,
Hangul fillers, and the door's invisible set.

| | what it entails |
|---|---|
| **(a) yes** | A reader refuses only code points that are not scalar values. Such a law has no text, but its run is defined: the characters are output bytes like any other. The claim "the image of a typed law" narrows to "except the characters of its text literals and names". The reader depends on no Unicode table |
| (b) no | LAW-FORMAT-0 lists the door's refused set exactly, and every reader refuses it. The list follows `canon.py`'s rules, whose format-character test depends on the Unicode version of the Python that runs the door, so every reader carries a frozen table of that version |

Recommended: **(a)**. It keeps the core free of a Unicode table, and the run is defined either way.

**A2 (F9). How is `as an integer` (`x_as_i`, `f_as_i`) given vectors?** The contract file has none.

| | what it entails |
|---|---|
| **(a) a supplementary vector file** | Generated from `numeric_ref.py` by a script in `research/rust-core/`, in the contract's line format. Kept apart from `vectors/runtime-vectors.txt`, which is not touched. Covers each refusal (NOT-FINITE, INEXACT-CONVERSION, OVERFLOW) and the boundaries. The core's author may read this file as data, as D1 allows for the vectors; the generator script stays outside their reading set |
| (b) no new vectors | `as an integer` is checked only through R3's receipts, on the texts that use it |

Recommended: **(a)**. Ruling D1 names "the vectors", so a second vector file needs your word.

## What follows the answers

1. **LAW-FORMAT-0, draft 1:** every DRAFT item and the answers, each change marked with its finding.
2. **`format_check.py` grows to match:**
   - the pre-order, the walk order, promote placement, If-chain shapes, W14, and the load refusal's precedence;
   - the re-reader's laws as fixtures it must accept (F2, F12);
   - his counterexamples as plants it must refuse (F1, F3, F4, F6).
   
   It runs twice, with all 298 laws still accepted.
3. **A targeted re-read of draft 1's changes,** by a fresh reader.
4. **Then the clean-room core.**
