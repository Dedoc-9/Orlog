# LAW-FORMAT-0: `orlog-law 0`, the written machine form of a version-0 law (draft 3, 2026-10-30)

**Status.** Draft 3 of RUST-CORE-0's phase 0. It is not a ruling and not yet the core's specification.

**What it applies:**
- REREAD-1's 19 dispositions and the owner's ruling B1, as draft 2 did;
- REREAD-2's 15 dispositions (`REREAD-2-DISPOSITION.md`), adopted by the owner with C1(a), C2(a) and three precision
  rulings (recorded whole in [RULINGS.md](RULINGS.md)). His comparison protocol is in SHEET.md, Amendments 1 and 2.

**What comes next.** A fresh targeted independent re-read of this draft, of its checker and of SHEET Amendment 2 comes
before any core code. In his words, it covers *"the four original B1 requirements and these new corrections"*. The B1
requirements: *"termination reasoning, budget preservation, explicit-stack requirements, and the distinction between
detected resource failure and external process termination."*

**Ruling 2, which this document answers** (2026-10-30): *"The format must make explicit obligations of: Every
execution-relevant derivation required by the interpreter and backends, including `Analysis.vars`,
`Analysis.rule_types`, and `VarInfo.top`. The order of a rule's definitions, because that order can determine which
refusal terminates execution. Exact reconstruction from law bytes, including the round-trip requirement."* *[G17]*

**History, kept as it was:**
- Draft 0 is `LAW-FORMAT-0-DRAFT-0.md` (`1ae57ee8…`), read by REREAD-0.
- Draft 1 is `LAW-FORMAT-0-DRAFT-1.md` (`8c277a1e…`), read by REREAD-1.
- Draft 2 is `LAW-FORMAT-0-DRAFT-2.md` (`f3b6c2a0…`), read by REREAD-2.
- Each change carries its finding in brackets: *[H1]* for a change from draft 2, *[G1]* for one from draft 1, *[B1]*,
  *[C1]* or *[C2]* for his rulings.
- Where this draft and the code at `2e9805a` disagree, that is a finding, and neither is presumed right.
- The checker is evidence, not authority (his word).

## 0. For the core's author

**What you read**, and nothing else (ruling D1):
- this document, its appendix A (worked runs) included;
- `SPEC.md`, sha256 `27dfff0cb50feb64f65844d6a0f480778df9b775a67827b50cd4d8b8ee7f6de5`, and `RUNTIME-SPEC.md`, sha256
  `0bd571d6f6bc8117af8161184c3e180e2d56a646000d900eb85bb2dfdd20ec35` *[H15]*;
- `vectors/runtime-vectors.txt`: the contract's 20,015 lines, sha256
  `841240b72cb580414483d217928b2794e033eb3745fd99b13946de1ef107f204`;
- `research/rust-core/vectors-as-integer.txt` *[G16]*: sha256
  `2bff1c69faeed37dbf4379aa1a2e6efd64bfb39711bf9b5a0a22977c7ddbad2f`. It has 446 lines (`x_as_i` 178, `f_as_i` 268),
  of which 189 are refusals (NOT-FINITE 6, INEXACT-CONVERSION 143, OVERFLOW 40). It is supplementary test data for `as
  an integer`, generated from the reference (ruling A2(a)), not part of the contract.

You may not read `src/`, `rt_rs/`, `rt_c/`, `twin/`, `research/law-sufficiency/` or any other file of
`research/rust-core/`.

**Where numbers are defined.**
- SPEC.md and RUNTIME-SPEC.md say that numeric meaning is defined by `src/orlog/numeric_ref.py`. You do not read it.
  For you, numbers are defined by SPEC §8, RUNTIME-SPEC §2–§3, section 5a, and the two vector files.
- If they disagree with the reference, that is a finding for the owner, not something you resolve.

**How the core is built:**
- one program, Rust edition 2021, the standard library only;
- no crates, no Cargo, no `unsafe`;
- built by bare `rustc --edition 2021 -O`, warning-free;
- no clock, no environment variable, no randomness;
- every file in binary mode, LF only;
- its own SHA-256, written from FIPS 180-4. The vectors' `sha256` lines check it.

**How it evaluates** *[B1, H11]*. These are implementation obligations, not language constructs:
- **Explicit stacks.** `perform` and rule uses are evaluated with explicit stacks the core keeps, never by recursion on
  the host's call stack. A rule use stands inside an expression, so the expression evaluator, too, must not recurse on
  the host's stack through a rule use.
- **The host call stack** is bounded by a constant that depends only on W14's bounds (section 8). It never depends on how
  deeply a law chains `perform` or rule uses.
- **Fallible allocation.** These stores grow only by fallible allocation (`Vec::try_reserve` and the like): the explicit
  stacks, lists, text values, the output buffer and the trace. An allocation that fails ends the run with detected
  resource exhaustion (section 10).

Nothing here promises that every process-level memory failure can be detected (the owner's second correction). An end
of the core that section 10 does not give is a core fault (section 10; SHEET, Amendment 2) *[C1]*.

**The vector files' lines**, one per line, ASCII, LF: `<op> <arg> … => <result>`. Each argument and each result is
one of:

| token | meaning |
|---|---|
| `i:<int>` | an Int, signed decimal |
| `x:<int>` | a Fix, its raw Q31.32 value, signed decimal |
| `f:<16 hex>` | a Float, its 64 bits, **uppercase** hex |
| `b:0` or `b:1` | a Bool |
| `s:<text>` | printed text, verbatim to the end of the line |
| `hex:<hex>` | bytes, lowercase hex, possibly empty |
| `!<CODE>` | the result is a refusal with that code |

**The operation names** *[G14]*:
- RUNTIME-SPEC §2–§3's function names;
- `x_as_i` and `f_as_i` for `as an integer`, named by this document (section 5a), not by RUNTIME-SPEC;
- `sha256`, which tests the core's SHA-256.

A harness runs each line and checks its result, as RUNTIME-SPEC §9 says. The law bytes write a Float in lowercase hex
(section 3), and the vector files write it in uppercase.

## 1. Notation

`⟨x⟩` names a part defined in this document. `·` is one space (0x20). Every line ends with LF (0x0A). A form is a
parenthesized list: `(`, its items separated by exactly one space, `)`. No space follows `(`, and none precedes `)`,
except in the two empty forms of section 4 (`(given·)` and `(over·)`), which are written with that one space.

**Lines** are numbered from 1: line 1 is `orlog-law 0`, line 2 the decimals line, and clause k is on line k + 2. A
refusal names a line by this number (section 8).

## 2. The bytes

A law is the bytes:

```
orlog-law 0 LF
(decimals ⟨mode⟩) LF
⟨clause line 1⟩ LF
…
⟨clause line n⟩ LF
```

- **n may be 0.** The empty law is exactly `orlog-law 0` LF `(decimals fixed)` LF (appendix A.1).
- **Every byte** is in 0x20–0x7E, or is LF. There is no CR, no tab, no byte above 0x7E, and no other control byte.
- **⟨mode⟩** is `fixed` or `floats`.
- **Clause line k** (k = 1…n, in order, with no gap) is, byte for byte, the **prefix** *[G7]* followed by the
  **rest** and a final `)`:
  - **the prefix:** `(clause`, one space, k as a canonical ⟨n⟩, one space, ⟨parent⟩ as a canonical ⟨n⟩, one space;
  - **the rest:** either ⟨statement⟩ or the word `absorbed`.

  A defect in the prefix or the final `)` is W1. A defect in the rest is W2 or W3 (section 8). That includes spacing
  around `absorbed`.
- **The tree's order.** Clause k's ⟨parent⟩ is 0 for a top-level clause *[G19]*, k − 1, or an ancestor of clause
  k − 1. The clause order is therefore the tree's pre-order, the order of a document: a clause comes after its parent,
  and every descendant of a clause comes before that clause's next sibling. "Before" and "after" mean this order, which
  is also the order of the outline numbers (section 6, Labels).
- **There is nothing** after the last line's LF.

**The law seal** is SHA-256 of these bytes, exactly (SPEC §9). **The seal words** are derivation 19.

## 3. Atoms

| atom | written | canonical form |
|---|---|---|
| ⟨n⟩, a natural number (ids, the fuel, Int and Fix literal values) | decimal | the digits 0–9, no sign, no leading zero (`0` alone for zero), **of any length** *[G10]* |
| ⟨hex16⟩, a Float literal | 16 hex digits | lowercase, exactly 16: the binary64's 64 bits as an unsigned integer, most significant digit first |
| ⟨str⟩, a string | `"` … `"` | below |
| ⟨label⟩, a clause reference by outline number | dotted decimals | each part a canonical ⟨n⟩ of at least 1, joined by `.` |
| ⟨word⟩ | letters, digits, `-`, `+`, `*`, `/`, `<`, `>`, `=`, `!` | exactly the words this document lists, and no others |

**An ⟨n⟩ is read as a decimal of any length** *[G10]*. W2 places no limit on its length. Every later check (W1, W4,
W8, W13) compares it as a number of that length. A reader therefore may not parse an ⟨n⟩ into a fixed-width integer
before those checks pass. An id greater than any clause, variable or claim is that check's failure, not a parse
failure.

**A string** is a sequence of Unicode scalar values: the code points 0–0x10FFFF outside 0xD800–0xDFFF (ruling A1(a)).
Between its quotes, each value is written in order:
- `"` as `\"`;
- `\` as `\\`;
- any other value from U+0020 to U+007E as itself;
- every other value as `\u{h}`, where h is the value in lowercase hex **without leading zeros** (`0` alone for zero),
  1 to 6 digits *[G3]*. So U+0000 is `\u{0}`, and U+0001 is `\u{1}`.

Every scalar value may stand in a string, controls and bidirectional controls included. Which characters a *text* may
contain is the source language's concern, not the format's. The format holds no Unicode table. It refuses:
- an `\u{h}` naming a surrogate or a value above 0x10FFFF;
- an `\u{h}` with a leading zero before another digit, or with more than 6 digits;
- any value not written in exactly the canonical way above.

A text value at run time is the UTF-8 encoding of the string's scalar values.

**Names** (of a `let`, a `procedure`, a `define`, and in `(rule …)`) are strings by the same rules. A run reads rule
names only: a `(rule ⟨str⟩)` names the defines whose name is the same sequence of scalar values, compared exactly. No
run reads the other names. They are kept and written back, and nothing checks them.

## 4. The forms

### Statements (⟨statement⟩), each the statement of one clause, or inline in an arm or an else

| form | SPEC construct | may stand inline |
|---|---|---|
| `(let ⟨V⟩ ⟨str⟩ ⟨E⟩)` | Let: variable ⟨V⟩, its name, its value | yes |
| `(set ⟨V⟩ ⟨E or -⟩ ⟨E⟩)` | Set X (`-`) or Set item I of X: the index, then the value | yes |
| `(change ⟨sign⟩ ⟨V⟩ ⟨E or -⟩ ⟨E⟩)` | Increase (`+`) or Decrease (`-`): the variable, its index or `-`, the amount | yes |
| `(say ⟨E⟩)` | Say | yes |
| `(if ⟨arm⟩ … ⟨arm⟩ ⟨else⟩)` | an If chain: one or more arms, then its otherwise or `-` | no |
| `(while ⟨n⟩ ⟨E⟩)` | While, its bound and its condition; the body is this clause's children | no |
| `(for ⟨V⟩ ⟨E⟩ ⟨E⟩)` | For, its counter, from, to; the body is this clause's children | no |
| `(procedure ⟨str⟩)` | To; its body is this clause's children | no |
| `(perform ⟨C⟩)` | Perform; ⟨C⟩ is the procedure's clause id | yes |
| `(must ⟨M⟩ ⟨E⟩)` | the must form, must id ⟨M⟩ | yes |
| `(claim ⟨K⟩ ⟨E⟩ ⟨oracle⟩ (given ⟨label⟩ … ⟨label⟩))` | the claim form, claim id ⟨K⟩; its premises, possibly none (`(given·)`) | yes |
| `(define ⟨str⟩ ⟨E⟩ ⟨E or -⟩ (over ⟨C⟩ … ⟨C⟩))` | Define: its rule's name, its value, its proviso or `-`, the definitions it overrides by clause id in written order, possibly none (`(over·)`) | no |
| `(append ⟨V⟩ ⟨E⟩)` | Append | yes |
| `(remove-last ⟨V⟩)` | Remove the last item | yes |
| `(decimals ⟨mode⟩)` | Decimals | no |

**Parts of the If chain:**
- ⟨arm⟩ is `(arm ⟨C⟩ ⟨E⟩ ⟨body⟩)`.
- ⟨else⟩ is `(else ⟨C⟩ ⟨body⟩)` or `-`.
- ⟨body⟩ is `(block ⟨C⟩)`, the children of clause ⟨C⟩, or one inline statement.

**The shapes of an If chain at clause K:**
- the first arm's ⟨C⟩ is K;
- each later arm's ⟨C⟩ is an absorbed Otherwise clause;
- the else is `-`, or an else whose ⟨C⟩ is an absorbed clause, with an inline or a block body, or an else whose ⟨C⟩ is
  K itself. That last is the inline otherwise of the If's own line (`If C, S; otherwise S`). It is allowed only when
  the chain has exactly one arm, that arm's body is inline, and the else's body is inline;
- a `(block ⟨C⟩)` in an arm or an else names that arm's or else's own ⟨C⟩;
- the chain's absorbed clauses are the siblings right after K, in written order: the later arms, then an absorbed
  else.

**Oracles (⟨oracle⟩):**
- `(computation)`
- `(owner)`
- `(theorem ⟨str⟩)`
- `(certificate ⟨C⟩)` or `(certificate ⟨C⟩ ⟨str⟩)`
- `(agreement ⟨label⟩ ⟨label⟩)`

### Expressions (⟨E⟩)

| form | meaning | its type (derivations 10–15) |
|---|---|---|
| `(lit int ⟨n⟩)` | an Int literal, n ≤ 2^63−1 | int |
| `(lit fix ⟨n⟩)` | a Fix literal; n is the raw Q31.32 value, ≤ 2^63−1 | fix |
| `(lit float ⟨hex16⟩)` | a Float literal: finite, sign bit 0 | float |
| `(lit bool 0)`, `(lit bool 1)` | false, true | bool |
| `(str ⟨str⟩)` | a text literal, at most 2^24 bytes of UTF-8 | text |
| `(seal)` | this law's seal words (derivation 19) | text |
| `(var ⟨V⟩)` | the variable ⟨V⟩'s value | the variable's type |
| `(rule ⟨str⟩)` | a use of the rule so named (SPEC §6) | the rule's type |
| `(⟨binary⟩ ⟨type⟩ ⟨E⟩ ⟨E⟩)` | a binary operator; ⟨type⟩ is its result's type | ⟨type⟩ |
| `(⟨unary⟩ ⟨type⟩ ⟨E⟩)` | a unary operator; ⟨type⟩ is its result's type | ⟨type⟩ |
| `(as ⟨target⟩ ⟨E⟩)`, `(rounded ⟨target⟩ ⟨E⟩)` | a conversion (SPEC §5, §8; section 5a) | ⟨target⟩ |
| `(promote ⟨target⟩ ⟨E⟩)` | an implicit promotion of an Int (SPEC §5), counted like a conversion; it stands only where W9 says | ⟨target⟩ |
| `(cat ⟨E⟩ ⟨E⟩ …)` | concatenation, two parts or more | text |
| `(item ⟨V⟩ ⟨E⟩)` | item I of the list variable ⟨V⟩ | the list's element type |
| `(length ⟨V⟩)` | the length of the list variable ⟨V⟩ | int |
| `(list-of ⟨E⟩ ⟨E⟩)` | a list of count copies of value | list of the value's type |
| `(list ⟨list type⟩ ⟨E⟩ …)` | a list literal, one item or more | ⟨list type⟩ |

**The operators:**
- ⟨binary⟩ is one of `+ - * / max min quot rem == != < > <= >= and or`.
- ⟨unary⟩ is one of `neg abs sqrt not trunc even odd zero positive negative`.
- ⟨target⟩ is `int`, `fix` or `float`.
- A form is read as binary by its four items and as unary by its three. `-` is only binary.
- `quot` and `rem` are SPEC's quotient and remainder/modulo. `trunc` is `integer part of`. `==` and `!=` are SPEC's
  `=` and `!=`.

**The types (⟨type⟩):** `int`, `fix`, `float`, `bool`, `text`, `list-int`, `list-fix`, `list-float`, `list-bool`.

## 5. What runs, and where

**Termination** *[B1, H10]*. Every accepted run ends after finitely many counted operations, and so ends. The reasons:
- **Nothing recurses.** Two measures decrease along every chain:
  - **Performs.** W6 makes every procedure top-level. W11 requires a performed procedure P to have a smaller id than
    the clause the perform is checked at, and the perform to be outside P's body. Inside a procedure Q's body, then,
    P < Q. Procedure ids strictly decrease along every chain of performs.
  - **Rule uses.** W10 checks a define's value and proviso at the define's own clause, and requires a used rule's last
    define to come before that clause. So along every chain of rule uses, the last define of each rule comes before
    the last define of the rule that uses it.
  - **The two together.** A rule's value and proviso are expressions, and an expression holds no `perform` and no
    statement. So no rule use leads to a perform, and the graph of performs and rule uses has no cycle.
- **Every loop is bounded.** Every `while` has a bound, and refuses `FUEL-EXHAUSTED` past it (W13; SPEC §7). Every `for`
  runs over a finite range of Int.
- **No expression loops,** and a list grows at most to 2^24 items, a text to 2^24 bytes (SPEC §7).
- **Uncounted work is bounded.** Every loop iteration, perform and rule use counts at least one operation (SPEC §7).
  So the work between two counted operations is bounded by the law's length and by the list and text bounds. That
  includes do-nothing clauses, skipped absorbed clauses and list copies.

This is a structural guarantee, DECLARED by construction, not measured. It is not a guarantee of practical completion.
The number of operations has no practical bound: a chain of rules each using the previous one twice doubles its work at
each step, and a `for` from −2^63 to 2^63−1 runs 2^64 times. Accepting a law promises no completion in available time
or memory.

**The walk.** Running a sequence of clauses runs each clause's statement in clause order, and skips each absorbed
clause (an absorbed clause is reached only through its If). A run runs the sequence of top-level clauses. Running a
statement S as clause C goes as follows:
- **an If:** for each arm in written order, evaluate its condition as the arm's ⟨C⟩. On true, run its body and stop:
  an inline body runs as the arm's ⟨C⟩, and `(block ⟨C⟩)` runs the sequence of ⟨C⟩'s children. If no arm ran, run
  the else's body, likewise.
- **a While, a For:** as SPEC §7 says. The body is the sequence of C's children.
- **a procedure, a define, a decimals:** nothing in place (but see the budget's check below). A procedure's body runs
  only through `perform`.
- **a perform:** runs the sequence of the procedure clause's children. Each of those clauses runs as its own id.
- **any other statement:** as SPEC §7 says.

**Explicit stacks** *[B1, H11]*. A law may chain `perform` and rule uses to any depth, and a reader must run it. The
language sets no limit (W10, W11), and this format adds none. A host's recursion depth is an implementation detail and
never a language restriction (section 0).

**Syntactic depth is not execution nesting** *[his second qualification]*. W14 bounds the clause tree and the
parentheses of one line: how a law is written. It does not bound how deeply performs and rule uses chain when the law
runs. W14 is checked before any traversal that could recurse without bound (section 8), so a reader refuses an
over-deep tree without crashing. Chains of performs and rule uses stay the explicit-stack obligation of section 0.

**The clause a statement runs as.** This is the clause SPEC §7 names in events and refusals:
- a clause's own statement: the clause's id;
- an arm's condition and its inline statement: the arm's ⟨C⟩;
- an else's inline statement: the else's ⟨C⟩;
- a rule's provisos and values, when used: the clause under which the use is evaluated, by these same rules. So a use
  in an absorbed arm's condition runs as that absorbed clause (SPEC §6, and §11 item 18) *[H15]*.

**The clause a part is checked at** *[G1]*. This is the clause the static checks of section 8 use. It is a different
thing from the clause a part runs as:
- a `define`'s value and proviso are checked at the `define`'s own clause;
- every other part is checked at the clause it runs as.

So a rule's value is checked once, where it is written, and never at the places it is used.

**Cost counters** *[G12]*. A clause named by a certificate has a cost counter. The counter grows when that clause's
statement, run as one clause of a sequence, **ends**: it grows by the operations counted from that statement's start
(SPEC §7, "afterwards"). Until then it stands as it was. So a claim inside the clause's own body reads the counter as it
stood before the statement began (appendix A.4: the inner claim reads 0, the claim after it reads 12). An absorbed
clause is never run as a member of a sequence, and an inline statement is not a clause, so neither has a counter of its
own. (W12 forbids a certificate to name an absorbed clause.)

**The budget's check.** This is the established position, unchanged *[B1, the owner's first correction]*. When a
budget B is given (section 10), the check "if ops > B, stop" is made immediately before each statement is run:
- before each non-absorbed clause of a sequence, the do-nothing statements `define`, `procedure` and `decimals`
  included;
- before each inline arm or else statement.

It is never made for an absorbed clause, before an arm's condition, before a loop's iteration, or inside an expression.
Operations are counted exactly as SPEC §7 counts them, wherever they fall. The check reads the count; it never counts.

**What the budget does not bound** *[B1, H1]*. The check is made at the positions above and at no others. Between one
check and the next, operations are counted and nothing stops the run, so ops may exceed B by any amount before the next
check stops it. Which work lies between two checks follows from the positions alone. A check stands before each clause
of a sequence, and the body of a `while`, a `for`, a `perform` or a `(block ⟨C⟩)` is run as a sequence (the walk,
above). So a run can stop inside those statements, at a clause of their body. In his words: *"Work may exceed the budget
between check points, but not necessarily throughout an entire enclosing statement."* (Draft 2 said a statement that
begins within the budget runs to its end. That was wrong, and is withdrawn *[H1]*.)

The budget is not an operation counter, and it is not a fuel allowance. (A deterministic fuel accounting would be a new,
versioned language feature, by the owner's ruling, not a reading of this one.)

## 5a. The functions behind the operators

The names are RUNTIME-SPEC §2's functions (`i_` Int, `x_` Fix, `f_` Float), and two this document names. The refusal
order is RUNTIME-SPEC's, or SPEC §8's where it says.

| form, by operand type | function | notes |
|---|---|---|
| `+ - * /`, `max`, `min` on int, fix, float | `i_add` … `x_div` … `f_min` | by ⟨type⟩ |
| `quot`, `rem` | `i_quot`, `i_rem` | Euclidean (SPEC §8) |
| `neg`, `abs`, `sqrt` | `i_neg`/`x_neg`/`f_neg`, …, `i_isqrt`/`x_sqrt`/`f_sqrt` | by the operand's type |
| `trunc` | `x_trunc`, `f_trunc` | |
| `rounded int` from fix, float | `x_round`, `f_round` | half-even |
| `as int` from fix | `x_as_i` *[G14: named here]* | INEXACT-CONVERSION unless the fraction bits are zero; then truncation |
| `as int` from float | `f_as_i` *[G14: named here]* | NOT-FINITE, then INEXACT-CONVERSION, then OVERFLOW (SPEC §8). Vectors: the supplementary file |
| `as fix`, `rounded fix` from int | `x_from_i` | one function for both; OVERFLOW when the value does not fit Q31.32 |
| `as fix`, `rounded fix` from float | `f_to_x`, rounded = 0 for `as`, 1 for `rounded` *[G14]* | |
| `as float`, `rounded float` from int | `f_from_i`, rounded = 0 for `as`, 1 for `rounded` | |
| `as float`, `rounded float` from fix | `x_to_f`, rounded = 0 for `as`, 1 for `rounded` | |
| `promote fix` | `x_from_i` | OVERFLOW when the Int does not fit Q31.32 |
| `promote float` | `f_from_i`, rounded = 0 | INEXACT-CONVERSION when the Int has no exact binary64 |
| `and` *[G14]* | — | evaluate the left; count one operation; if false, the result is false and the right is not evaluated; else the right is the result (SPEC §7, item 35) |
| `or` *[G14]* | — | evaluate the left; count one operation; if true, the result is true and the right is not evaluated; else the right is the result |
| `not` *[G14]* | — | count one operation; the negation |
| `<` on float | `f_lt` | IEEE |
| `==` on float | `f_eq` | IEEE: NaN ≠ NaN, and −0 = +0 |
| `<=`, `>`, `>=`, `!=` on float | IEEE's own comparison | not by negating another: every comparison with a NaN is false, except `!=`, which is true |
| `< <= > >= == !=` on int and fix | the signed integers; a Fix by its raw value | |
| `==`, `!=` on bool | equality of the two truth values | |
| `==`, `!=` on text | equality of the bytes | |
| `even`, `odd`, `zero`, `positive`, `negative` | SPEC §5, §8 | on a Float, `zero` is true of ±0, and a NaN is neither positive nor negative |

## 6. The derivations

A reader derives each of these from the bytes alone. The interpreter or the backends read every one of them, and none
is written in the bytes as such.
- **The *held by* column** names the test that measured the derivation against the analysis at `2e9805a`: LS-0 and LS-1
  are LAW-SUFFICIENCY-0 and -1, FC the checker.
- **The *analysis field* column** *[G17]* names, for re-readers, the field of `sema.py`'s analysis each derivation
  stands for. The core's author need not use it.

| # | derivation | from the bytes | read by | held by | analysis field |
|---|---|---|---|---|---|
| 1 | **the top** | the clauses whose ⟨parent⟩ is 0, in clause order | run | LS-0 test 3; FC | `Program.top` |
| 2 | **children** | the clauses whose ⟨parent⟩ is this clause's id, in clause order | run | LS-0 test 3; FC | `Clause.children` |
| 3 | **cost-tracked clauses** | the clauses named by some `(certificate ⟨C⟩ …)` | run | LS-0 test 3; FC | `Clause.cost_tracked` |
| 4 | **the rules** | for each rule name, its `define` clauses in clause order | run | LS-0 test 3; LS-1 E2; FC | `Analysis.rules` |
| 5 | **the overrides** | for each rule name and each of its defines d, the defines d beats: the transitive closure of the `(over …)` lists | run | LS-0 test 3; FC | `Analysis.overrides` |
| 6 | **the claim sites** | the claims in claim-id order, each with the clause it runs as; the receipt lists them so | run | LS-0 test 3; FC | `Analysis.claims` |
| 7 | **a claim site's clause** | the clause the claim runs as | run | LS-0 test 3; FC | `ClaimSite.id` |
| 8 | **a variable's type** | a `let`'s variable: the type of its ⟨E⟩, which is never a `promote` (W9); a `for`'s counter: int | run, backends | LS-0 test 3; LS-1 E3; FC | `VarInfo.type` |
| 9 | **a change's element type** | without an index: the variable's type; with one: the list's element type | run | LS-0 test 3 | `Change.elem` |
| 10–15 | **an expression's type** | section 4's type column; for `(var ⟨V⟩)` derivation 8, for `(rule ⟨str⟩)` derivation 17 | run, backends | LS-0 tests 1 and 3; LS-1 E1 | `.type` of `Var`, `Str`, `Cat`, `Conv`, `Item`, `BoolLit` (and every expression node) |
| 16 | **the variables** | every variable, in id order; ids 0…m−1 in the order the walk of section 7 meets their declarations | backends | LS-1 E3, E4; FC | `Analysis.vars` |
| 17 | **a rule's type** | the type of its first `define`'s value | run, backends | LS-1 E3; FC | `Analysis.rule_types` |
| 18 | **a variable's top** | true exactly for a `let` that is the statement of a top-level clause, not inline | backends | LS-1 E3, E4; FC | `VarInfo.top` |
| 19 | **the seal words** | the first 64 bits of the bytes' SHA-256 as four proquints (SPEC §9). Worked value *[G15]*: the empty law's seal `91e3deb3c796c4742eb2a12ca5e20e157fdfc172d2bf25237803d58c1f28e0f5` gives `nalog-tupug-sivik-siduh` (appendix A.1). SPEC §14 (SPEC.md:672) gives the all-zero case, `babab-babab-babab-babab` | run (`(seal)`), backends | appendix A | the seal words (`Compiled.seal_words`) |

**Two further derivations hold no field:**
- **Labels.** The top-level clauses are numbered 1, 2, … in clause order, absorbed ones included. Each clause's children
  are numbered by appending `.1`, `.2`, … to its parent's number. A ⟨label⟩ names the clause whose outline number it is.
- **Decimals.** ⟨mode⟩ in line 2 is the mode of the law's `(decimals …)` clause if it has one, else `fixed`. Every
  decimal literal is of that mode.

## 7. The order obligations

1. **A rule's definitions are taken in clause order:** every proviso first, then the values of those that remain. The
   first refusal ends the run (SPEC §6; LS-1 E2).
2. **A sequence runs in clause order,** and an If chain's arms run in written order.
3. **Ids are numbered by the walk.** The walk is section 5's order of running, taken over the whole law without
   evaluating anything:
   - the top-level sequence;
   - in a sequence, each non-absorbed clause in clause order;
   - in a clause, its statement's own expressions in SPEC §7's order;
   - for an If, each arm's condition, then its body (an inline statement, or the block's sequence), then the else's
     body;
   - for a While, a For or a procedure, its children's sequence after the statement.

   Variables, claims and musts get ids 0, 1, … in the order the walk meets their declarations:
   - a `let`'s variable comes after its value;
   - a `for`'s counter comes after its bounds and before its body.

   A procedure's body is walked once, where its clause stands. Example: for `§1 If true, do the following. §1.1 Let a
   be 1. §2 Otherwise, let b be 2.`, the bytes are:
   ```
   (clause 1 0 (if (arm 1 (lit bool 1) (block 1)) (else 3 (let 1 "b" (lit int 2)))))
   (clause 2 1 (let 0 "a" (lit int 1)))
   (clause 3 0 absorbed)
   ```
   Variable 1 is written on line 3, before variable 0 on line 4, because the walk meets `a` before `b`.
4. **A `define`'s `(over …)` list keeps its written order.**

## 8. Well-formedness: what a reader must refuse

A reader that runs law bytes must refuse, before anything runs, every byte string that breaks one of these checks
(ruling D3). Each mirrors a check the front end makes.

**What a pass means.** Format validity is not the same as source admissibility (the owner, under A1). A byte string
that passes every check:
- runs without any fault that the front end's checks prevent;
- ends after finitely many operations (section 5, Termination).

Its text literals and names may hold characters no text can. Its names are unchecked. Running it may still meet a
resource limit of the host (section 10's operational outcomes). **No check limits how deeply `perform` and rule uses
chain when the law runs** *[B1]*. W14 bounds only how the law is written: its clause tree and its lines (section 5,
syntactic depth is not execution nesting).

| | check | the line it belongs to *[G8]* |
|---|---|---|
| W1 | **the bytes and the tree:** the character set; line 1; line 2; each clause line's prefix and final `)` (section 2); the clause lines numbered 1…n (n ≥ 0); each parent 0, k−1 or an ancestor of k−1; the final LF | the line that fails; a missing final LF belongs to the last line, the one with no LF *[G6]* |
| W2 | **the forms and their atoms:** the rest of every clause line parses as section 4's forms; each atom canonical by section 3, each string in exactly its canonical escapes; the word `absorbed` when the rest is no form | that line |
| W3 | **the spacing:** single spaces between items, none after `(` or before `)` but in `(given·)` and `(over·)`, and none around `absorbed`. Once W2 holds, writing back gives the rest exactly if and only if W3 holds | that line |
| W4 | every ⟨C⟩ names an existing clause; every ⟨label⟩ is an existing clause's outline number | the line holding the reference |
| W5 | **bodies and If chains** (EMPTY-BLOCK, UNEXPECTED-CHILDREN, ORPHAN-OTHERWISE): a clause has children exactly when it is a `while`, `for` or `procedure`, or is named by a `(block ⟨C⟩)`, and then at least one; a block names its arm's or else's own ⟨C⟩; every If chain has section 4's shape; each absorbed clause is named by exactly one arm or else of exactly one If | a chain's shape, and a block it names: the If's line. Children: that clause's line. An absorbed clause in no chain: its own line. One named by two Ifs: the later If's line |
| W6 | **places and the decimals** (DEFINE-PLACE, PROCEDURE-PLACE, DECIMALS-PLACE): `define`, `procedure` and `decimals` are top-level clause statements, never inline. There is at most one `decimals`, and the walk meets no decimal literal before it. Line 2's mode is derivation "Decimals". A `(lit fix …)` stands only under `fixed`, a `(lit float …)` only under `floats` | a misplaced statement, or a literal of the wrong mode: its own line. A second `decimals`: its line. A decimal literal before the `decimals`, and line 2's mode against a `decimals` clause: the `decimals` clause's line, the later one. Line 2's mode with no `decimals` clause: line 2 |
| W7 | **inline:** an inline body is a form section 4 marks inline | the If's line |
| W8 | **variables** (UNDECLARED, LOOP-VARIABLE): ids are numbered by the walk (section 7), each declared once; each use is in scope (below); a `for` counter is never set, changed, appended to or removed from | the line holding the declaration or the use |
| W9 | **types and promotions** (TYPE): below | the line holding the expression |
| W10 | **rules** (RULE-BEFORE-DEFINITION, NOTWITHSTANDING-TARGET, PRIORITY-CYCLE) *[G1]*: every define of a name has one type, not a list; a proviso is bool; each `(over ⟨C⟩)` names a define of the same name; no define beats itself in the closure. A `(rule ⟨str⟩)` names a rule with at least one define. The use is **checked at** a clause whose id is greater than the last define's of that name; inside a procedure's body, the procedure's clause id must be greater instead | a use: its line. Two types: the later define's line. A cycle: each define's line in it. Every other failure (an `(over ⟨C⟩)` that names no define of the name, a proviso that is not bool, a value that is a list): the line holding the define, as W4 gives the line holding a reference *[H14]* |
| W11 | **procedures** (PERFORM-BEFORE-DEFINITION, UNKNOWN-PROCEDURE): `(perform ⟨C⟩)` names a `procedure` clause whose id is less than the clause the perform is checked at, and the perform is not in that procedure's body | the perform's line |
| W12 | **claims** (CERTIFICATE-TARGET, AGREEMENT-TARGET, PREMISE-TARGET), relative to the clause the claim is checked at: a certificate's ⟨C⟩ is a smaller id, not absorbed, and not a `procedure`, `define`, `decimals` or `claim`; agreement's labels name clauses with smaller ids; each `given` label names a clause whose own statement is a `claim` | the claim's line |
| W13 | **ranges** (FUEL, LITERAL-RANGE): a While's ⟨n⟩ is in 1…2^62; Int and Fix ⟨n⟩ are ≤ 2^63−1; a Float literal is finite with sign bit 0; a text literal is at most 2^24 bytes of UTF-8 | that line |
| W14 | **depth**, below | (a), (b): the clause's line; (c): that line |

**W9's rules, by form.** "Numeric" means int, fix or float.
- **`+ - * / max min`:** after promotion, one numeric type, which is ⟨type⟩.
- **`quot`, `rem`:** two int operands; ⟨type⟩ int.
- **`< > <= >=`:** after promotion, one numeric type; ⟨type⟩ bool.
- **`==`, `!=`:** after promotion, one type that is numeric, bool or text; ⟨type⟩ bool.
- **`and`, `or`:** two bool operands; ⟨type⟩ bool. **`not`:** a bool operand; ⟨type⟩ bool.
- **`even`, `odd`:** an int operand. **`zero`, `positive`, `negative`:** a numeric operand. All five have ⟨type⟩ bool.
- **`neg`, `abs`, `sqrt`:** a numeric operand of ⟨type⟩.
- **`trunc`:** a fix or float operand; ⟨type⟩ int.
- **`as`, `rounded`:** SPEC §5's table.
- **`promote`:** an int operand; the target is fix or float.
- **`item`:** an int index into a list variable. **`length`:** a list variable. **`list-of`:** an int count, and a
  value of type int, fix, float or bool.
- **`list`:** each item, after promotion, is ⟨list type⟩'s element, which is int, fix, float or bool.

**The statements:**
- **`let`:** any type, and its value is never a `promote`.
- **`set` without an index:** the value, after promotion, has the variable's type. **With one:** an int index, a list
  variable, and the element type.
- **`change`:** as `set`, and the type is numeric.
- **`say`, `cat`'s parts:** any type.
- **The conditions** of `if`, `while`, `must` and `claim`: bool.
- **`for`'s bounds:** int.
- **`append`:** a list variable, and a value that after promotion has its element type.
- **`remove-last`:** a list variable.

**Where a `promote` may stand**, exactly as SPEC §5 promotes, and nowhere else:
1. **As one operand** of `+ - * / max min`, a comparison, `==` or `!=`, **when the other operand's type is fix or
   float and is the promote's target** *[G4]*. At most one operand is a promote, and the other is not.
2. **As the stored value** of a `set`, `change` or `append`, when the slot's type (the variable's, or its element's) is
   fix or float and is the promote's target. Never as a `let`'s value.
3. **As an item** of a `list` whose element type is fix or float and is the promote's target, with at least one item
   not a promote.

**The scope of a variable (W8)** *[G1]*. A use is in scope when the clause U it is checked at (section 5) relates to
the declaration like this:
- **a `let` that is the statement of clause D:** U is a later sibling of D (both top-level, or both children of one
  clause), or a descendant of such a sibling;
- **a `let` inline in an arm or an else:** never;
- **a `for` counter declared by clause F:** U is a descendant of F.

So a define's value and proviso, checked at the define's clause, see the top-level variables declared before it. A use
inside a procedure's body sees the top-level variables declared before the procedure's clause.

**W14, depth:**
- **(a)** A clause is at most 24 deep: a top-level clause is depth 1, its children depth 2. This is the front end's 24
  label parts.
- **(b)** A `while` or `for` clause has at most 16 `while` and `for` clauses among itself and its ancestors, counting
  only those below the nearest `procedure` ancestor. This is the front end's 16 nested loops in one body.
- **(c)** *[G9, G11]* No clause line nests parentheses outside strings more than **130** deep. This is checked
  lexically, before the line is parsed (phase 2 below), so a reader's parser never goes deeper.
  - **The count** *[H5]*. Scan the line from its first byte, keeping a running count, which may go below zero:
    - outside a string, `(` adds one and `)` takes one away;
    - a string opens at a `"` outside a string, and closes at the next `"` inside it that is not escaped;
    - inside a string, `\` skips the byte after it, and no byte changes the count.

    The line fails W14(c) if the count ever exceeds 130. An unbalanced line can pass this count and then fail W2.
  - **The derivation,** for the re-read *[H9]*:
    1. The front end refuses a statement whose parsed tree is deeper than 64 (`syntax.py`'s `ast_depth`, 64). A
       clause's own expressions are therefore at most 63 deep as parsed, and an inline statement's at most 62.
    2. After that check, only two things add expression nodes: an If-Unless's `not` above a condition, and promotes.
       (A define's `unless` `not` is built by the parser and counted within the 64.)
    3. A promoted node is an Int, and its parent is a Fix, Float, Bool or list node, or a statement, which is never
       promoted. So no two consecutive parsed nodes on a path both carry a promote. An expression in the bytes is then
       at most 63 + 32 = 95 deep, an If-Unless's condition 96, and an inline statement's expression 62 + 31 = 93.
    4. The forms around them: a condition lies inside the clause, the `if` and its `arm`, so 3 + 96 = 99 levels. An
       inline statement's expression lies inside those three and the statement, so 4 + 93 = 97. Any other expression
       lies inside the clause and its statement, so 2 + 95 = 97. So 99 levels suffice.

    The bound 130 is kept, as safe and not tight.

**Which refusal is reported** *[G6, G9]*. A reader reports exactly one:
1. **Phase 1**, line by line from the start: the first line that fails W1. Each line is checked completely before the
   next.
2. **Phase 2**, line by line: the first clause line that fails one of these three checks, in this order:
   - W14(c)'s lexical count;
   - W2;
   - W3.
3. **Phase 3**, among every failure of W4–W14 (W14(c) excepted): the one on the least line, and on that line the
   least W, by the attribution in the table above.
   - **Depth first** *[H2, his second qualification]*. W14(a) and (b) are computed from the parent links, without
     recursion, before the walk: a clause's depth is its parent's plus one, and a parent always comes first. **The walk
     enters no clause deeper than 25.** So it is at most 25 deep, however deep the tree. The reported (line, W) is the
     same as if the whole tree were walked:
     - every clause it skips descends from a clause 25 deep, which fails W14(a) on its own line, and lies on a later
       line;
     - every line this table gives a failure of a skipped part is later still (that part's own line, or the later of
       two lines).

     This bounds the walk of the clause tree only. It sets no limit on chains of performs or rule uses.
   - A check that needs something an earlier failure leaves underived is not made: a missing clause, an undeclared
     variable's type, a rule with no define. That includes a promote's place when the other operand's type is
     underived *[H8]*.
   - **The walk enters no block of an If chain that fails W5, and no inline statement that fails W7** *[G8]*. Their
     parts are not walked, numbered or checked.

**What refusing means.** A reader refuses by writing no file and ending with a load refusal (section 10).

## 9. Exact reconstruction (the round trip)

A reader keeps every written part: names, strings, labels, the order of `(over …)` lists and of `given` labels, and
the absorbed clauses. Writing it back by sections 2–4 gives the bytes it read, byte for byte. W2 and W3 refuse every
other bytes. Two writers that follow this document write identical bytes for one law (REREAD-0 Q5; REREAD-1 Q6).

**Held by:** LS-0 test 3 (290 of 290); LS-1 E1, E3 (298 of 298); FC.

## 10. The run interface

`rust-core LAW TEXTSEAL OUT RECEIPT [TRACE] [--budget B]` *[G13]*
- **LAW:** a path to the law bytes *[H12]*.
- **TEXTSEAL:** exactly 64 lowercase hex digits. It is printed in the receipt's `text-seal` line as given. It is the
  caller's input: it is not in the law bytes, and the core never derives or validates it (the owner's ruling). Only its
  form is checked.
- **OUT, RECEIPT, TRACE:** RUNTIME-SPEC §6's output, receipt and trace paths *[H12]*.
- **B:** a canonical decimal from 0 to 2^64−1. Without `--budget` there is no budget.
- **The arguments** are positional. `--budget B` may only be the last two.
- **A usage error** is any of these *[H12]*:
  - a wrong number or order of arguments;
  - a positional argument that begins with `--`;
  - TEXTSEAL not 64 lowercase hex digits;
  - B not a canonical decimal in range;
  - two of OUT, RECEIPT and TRACE the same path, compared as the strings given.

**The order of outcomes** *[G13, H12]*:
1. the arguments, which give a usage error;
2. reading LAW, which gives an I/O error;
3. the load checks, which give a load refusal;
4. the run.

Detected resource exhaustion can end any stage from 2 on, and is reported at the stage where it happens. Running out of
memory while reading or loading LAW is resource exhaustion (kind `law`), not an I/O error.

**When each file is written:**
- TRACE, if given, is created when the run starts, after the load checks, so a run with no event leaves it empty. The
  trace is written as events happen *[H12]*.
- Output is buffered, and written to OUT only when a completed or refused run ends. The receipt is written last.
- A file is created, or truncated if it exists, only when it is written.
- The core removes nothing, so a caller that wants no stale file removes it before the run, as the arbiter does
  *[H12]*.

| outcome | kind | when | files | exit | stderr |
|---|---|---|---|---|---|
| completed | language | the run ends | TRACE (if given), OUT, then RECEIPT (`status COMPLETED`) | 0 | nothing |
| refused | language | the run refuses (SPEC §7) | TRACE, OUT up to the refusal, then RECEIPT (`status REFUSED <CODE> <clause>`) | 0 | nothing |
| stopped | budget (the host's) *[H12]* | the budget's check (section 5) finds ops > B | TRACE alone, holding every event before the stop; OUT and RECEIPT not written | 4 | `STOPPED-BY-HOST after <ops> counted operations (budget <B>)` |
| load refusal | format | the bytes fail a check (section 8) | none: no file is opened for writing | 3 | `LAW-REFUSED W<k> line <n>: <reason>` |
| usage error | operational | the arguments (above) | none | 2 | `USAGE: <reason>` |
| I/O error | operational | LAW cannot be read, or OUT, RECEIPT or TRACE cannot be written | whatever was written before; never a RECEIPT after it | 2 | `IO-ERROR: <reason>` |
| **resource exhaustion, detected** *[B1, H12]* | **operational** | an allocation the core makes by a fallible call fails, at any stage from reading LAW on | whatever was written before stays; never a RECEIPT | **5** | `RESOURCE-EXHAUSTED: <kind>`, the kind one of `law`, `stack`, `list`, `text`, `output`, `trace` |

- `<k>`, `<n>`: the W and the line chosen in section 8. `<reason>` is free text, which no comparison reads *[H12]*.
- Every stderr line ends with exactly one LF and holds no other *[H12]*.
- SPEC §12 says of the stop that *"the law said nothing"*. It is the host's budget, not a language outcome, though it is
  compared (SHEET R5).

**Any other end is a core fault** *[C1]*. The core ends only by one of the rows above. The harness classes every other
end as CORE-FAULT, which fails the prediction being tested (SHEET, Amendment 2). Other ends include:
- an exit status no row gives, a panic's for example;
- a stack overflow, or an abort;
- an end whose files or stderr contradict its row: exit 0 without a receipt, say.

In his words: *"An unknown exit status, panic, stack overflow, or other unexpected core termination is a core fault,
not an unlisted operational outcome."* Section 0 forbids host recursion on chains of performs and rule uses, and
requires fallible allocation for the named stores, so that a law cannot drive the core to such an end.

**External termination** *[B1, C1, the owner's second correction]*. The process can also be ended from outside: by the
harness at its 60-second limit, or by the operating system, an out-of-memory kill for example. Such an end may give no
diagnostic and no defined exit status. The harness classes it EXTERNAL-TERMINATION only when it ended the run itself, or
on evidence it records of the host's act. Otherwise the end is a core fault. It is never relabeled as a resource-handling
result. The core does not and cannot promise to catch it. Nothing here promises that every process-level memory failure
can be detected.

**What the operational outcomes are not.** Detected exhaustion, external termination, usage and I/O errors are never:
- a language refusal;
- the budget's stop;
- a completed run.

They carry no receipt, and no comparison reads them as a result. Where the reference's class is RESULT, any of them
is a coverage failure, never a pass. Two runs of one case whose classes differ are an unstable core, which fails (SHEET,
Amendment 2) *[C1, C2]*.

The receipt's backend line is `backend rust-core` (ruling D5). Its law seal is the SHA-256 of the bytes read, computed
by the core.

## 11. How this document is held to the code, and the code to it

**The checker.** `research/rust-core/format_check.py`, written from sections 2–4 and 8. It is outside the core
author's reading set. On every one of LAW-SUFFICIENCY's 298 laws and the fixture laws below:
- it parses the bytes and checks W1–W14;
- it writes them back;
- it computes the derivations and compares them with the analysis's own.

Every law must pass and come back exactly. Every plant must be refused on the line and with the W that section 8
chooses. The checker sets **no** limit on how deeply `perform` and rule uses chain (the owner's ruling B1). Its walk of
the clause tree is bounded by phase 3's depth rule, and it refuses an over-deep tree without crashing *[H2]*. The
re-read is asked to verify both.

**Fixture laws**, which the checker must accept *[H13]*:
- REREAD-0's four: the forward declaration, forward claims, a certificate from an inline otherwise, the empty law;
- a perform chain of 3,000 and a rule chain of 3,000 *[B1]*;
- `\u{0}` in a string *[G3]*;
- a clause line nested exactly 130 deep *[G11]*.

**Plants**, which it must refuse: 52 in all.
- draft 0's thirteen and draft 1's nine;
- draft 3's eight *[H2, H5–H8, H13]*:
  - 30,000 nested `while` clauses (W14 at line 19) and 30,000 nested If blocks (W14 at line 27), refused without
    crashing *[H2]*;
  - H5's two unbalanced lines: one whose count never exceeds 130 (W2), one whose count does (W14);
  - `remove-last` on a `for` counter (W8) *[H6]*;
  - an absorbed clause named by two Ifs through `(block …)` (W5 at the later If's line) *[H7]*;
  - a promote beside a rule with no define (W10, not W9) *[H8]*;
  - G5's third law, an else naming clause 99 after a procedure (W4) *[H13]*;
- draft 2's twenty-two *[G18, G7]*:
  - G7's two: two spaces in the prefix (W1), and two spaces before `absorbed` (W3);
  - W14(a) at 25 clauses deep;
  - W14(b) at 17 loops;
  - an id numbered in line order rather than walk order;
  - `(lit float …)` under `fixed`;
  - REREAD-1's T3 (a rule cycle through define values, W10) and T4 (a define's value using a later `let`, W8);
  - `\u{110000}`;
  - `promote int` in `+`, `==` and `<` (G4);
  - an else and an arm naming clause 99 (G5, W4);
  - a clause line nested 131 deep, and one nested 25,000 deep followed by a W2 line (G9, W14 on the deep line);
  - the W1 order cases T1, T2, T2b (G6);
  - REREAD-1's C10 cases: an inline `if` with a block (W7), a decimal literal before `decimals` (W6 at the
    `decimals` line), and an absorbed clause named by two Ifs (W5 at the later If's line).

**Evidence:** `evidence/rust-core-format-3.txt`. The records of drafts 0, 1 and 2 are kept.

**What it does not show.**
- That every law the front end can produce passes W1–W14. It shows that these laws do.
- That no byte string passing them can fault.
- Any run of the core.

In the owner's words, the checker *"cannot substitute for the independent re-read"*.

## 12. Questions for the fresh re-read

These are the owner's four B1 requirements, his new corrections, and the draft's own:
- **Q1, termination.** Is section 5's termination reasoning complete and right? Can any accepted law run without end,
  through any construct?
- **Q2, budget preservation.** Do sections 5 and 10 keep the budget exactly as the reference has it? That covers:
  - the check's positions, do-nothing clauses included;
  - that operations are counted as SPEC §7 counts them;
  - the stop's report.

  Does any sentence redefine the budget, or generalize beyond the exact positions, as his first correction and his
  first qualification forbid?
- **Q3, explicit stacks.** Are explicit-stack evaluation and fallible allocation stated as implementation obligations,
  not as language rules? Does anything in the document, the sheet or the checker impose a limit on chains of `perform`
  or rule uses? Is syntactic depth kept apart from execution nesting (his second qualification)? Does the checker
  refuse an over-deep clause tree without crashing, and is the walk's bound shown to leave every reported (line, W)
  unchanged?
- **Q4, detected against external.** Do section 10 and SHEET Amendment 2 keep these apart from each other and from
  every language outcome: detected resource exhaustion, external termination and a core fault? Do they promise to
  catch nothing that cannot be caught? Can any end of the core pass for a result merely because it stopped (his third
  qualification)?
- **Q5, the protocol.** Does SHEET Amendment 2 fix the comparison protocol completely before any experiment? That
  covers the reference as shipped, the classes, coverage, R6's limit, S3's values and procedure, and evidence records
  that keep his five distinctions apart. Do `s3-budgets.txt` and `gen_s3_budgets.py` match it?
- **Q6.** Is each of H1–H15 resolved as its disposition says? Give a table, and check each new plant tests what its
  finding says.
- **Q7.** Does the checker implement sections 2–4 and 8 as written, phase by phase, line by line and W by W?
- **Q8.** Anything a clean-room author would still have to guess.

## Changes from draft 2

| finding | where |
|---|---|
| H1 | section 5, what the budget does not bound (his first qualification) |
| H2 | section 5, syntactic depth against execution nesting; section 8, phase 3's depth first; the checker; section 11 |
| H5 | W14(c), the count |
| H6, H7 | the checker; section 11 |
| H8 | section 8, checks not made; the checker; section 11 |
| H9 | W14(c), the derivation |
| H10 | section 5, termination |
| H11 | section 0, how it evaluates; section 5, explicit stacks |
| H12 | section 10 |
| H13 | section 11's lists; the checker's docstrings |
| H14 | W10's line |
| H15 | section 0, the two specifications' sha256; section 5, SPEC §11 item 18 |
| C1 | section 0; section 10, any other end is a core fault, external termination; SHEET Amendment 2 |
| C2 | section 10; SHEET Amendment 2 (the reference as shipped, R6, S3's values) |

## Changes from draft 1 (draft 2's, kept)

| finding | where |
|---|---|
| B1 | section 0 (how it evaluates); section 5 (termination, explicit stacks, what the budget does not bound); section 8 (what a pass means); section 10 (resource exhaustion, external termination); SHEET Amendment 1 |
| G1 | section 5, the clause a part is checked at; W8; W10; W11; W12 |
| G3 | section 3, `\u{0}` |
| G4 | W9, where a promote may stand |
| G5 | the checker; section 8, checks not made |
| G6 | section 8, phase 1; W1's line |
| G7 | section 2, the prefix; W1; W2 |
| G8 | the table's line column; the walk and malformed structure |
| G9 | W14(c), lexical, in phase 2 |
| G10 | section 3, ⟨n⟩ of any length |
| G11 | W14(c)'s derivation |
| G12 | section 5, cost counters; appendix A.4 |
| G13 | section 10 |
| G14 | section 0, operation names; section 5a |
| G15 | derivation 19 |
| G16 | section 0, the supplementary file; appendix A |
| G17 | the status (ruling 2); section 6's analysis-field column |
| G18 | section 11, the plants |
| G19 | section 2, the parent; W5's lines |

## Appendix A: worked runs, produced by the reference (data)

The core must reproduce each one, its backend line excepted (`backend rust-core`), with the TEXTSEAL given.

Produced by `research/rust-core/gen_worked.py` (sha256 163e54f4b30f1d3ad6cef3189f5408a3af3886347e504a79df91633314dfb738) from the reference at `2e9805a`:
`src/orlog/interp.py` sha256 f843291861798c85c90716430a00b24663e4d7521f6cecdf268cb197c7e94d27, `src/orlog/numeric_ref.py` sha256 eacac3dd7c4dfda903f1927994ea8b3a95ba866b3485fb1c6b91428cb5f6bb64. Data, as the vectors are.

**A.1, the empty law.**

The law bytes:
```
orlog-law 0
(decimals fixed)
```
TEXTSEAL `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; the law seal `91e3deb3c796c4742eb2a12ca5e20e157fdfc172d2bf25237803d58c1f28e0f5`; the seal words `nalog-tupug-sivik-siduh`.

The reference's receipt (the core's differs in its backend line only):
```
orlog-receipt 0
backend reference
law-seal 91e3deb3c796c4742eb2a12ca5e20e157fdfc172d2bf25237803d58c1f28e0f5
text-seal e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
status COMPLETED
output-bytes 0
output-sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
events 0
trace-head 7715e904c45590b3390600b39035119c4e43ef4e7654a2176acd27ff817fa65a
ops 0
claims 0
end
```
Its trace (0 events): empty.

**A.2, a let and a say.**

The law bytes:
```
orlog-law 0
(decimals fixed)
(clause 1 0 (let 0 "x" (lit int 2)))
(clause 2 0 (say (+ int (var 0) (lit int 3))))
```
TEXTSEAL `88e22c52d51ec526acaa7f81a756a3cb7f43b091bf40a62bd741d2f1ca0e1c37`; the law seal `6304879cfa306423bde86f555dab2a3d9b58487e61372e623ee1ae4f95f4d61e`; the seal words `kasah-mivis-zomub-kibog`.

The reference's receipt (the core's differs in its backend line only):
```
orlog-receipt 0
backend reference
law-seal 6304879cfa306423bde86f555dab2a3d9b58487e61372e623ee1ae4f95f4d61e
text-seal 88e22c52d51ec526acaa7f81a756a3cb7f43b091bf40a62bd741d2f1ca0e1c37
status COMPLETED
output-bytes 2
output-sha256 f0b5c2c2211c8d67ed15e75e656c7862d086e9245420892a7de62cd9ec582a06
events 2
trace-head b419cc706a28145fc6d15204c541808c8b1e6396f2cf1f26f033f63b091c0e2c
ops 3
claims 0
end
```
Its trace (2 events):
```
1 A 1 00000000490000000000000002 6f4033604a8ac71abf356b8f3e84483c7666a43ea90805cc1ff93b553a8c7cc6
2 S 2 350a b419cc706a28145fc6d15204c541808c8b1e6396f2cf1f26f033f63b091c0e2c
```

**A.3, a refusal.**

The law bytes:
```
orlog-law 0
(decimals fixed)
(clause 1 0 (say (lit int 1)))
(clause 2 0 (say (/ int (lit int 1) (lit int 0))))
```
TEXTSEAL `70751059da2fba395c50aa0eab1f5ee5b934c623c514303c0e7207bb2a888f84`; the law seal `e6d8b12f7b694133eba2d2d87b241fe51dbbe1dcd4721028b35fd0bd5c8c57df`; the seal words `virim-rahoz-loton-hahug`.

The reference's receipt (the core's differs in its backend line only):
```
orlog-receipt 0
backend reference
law-seal e6d8b12f7b694133eba2d2d87b241fe51dbbe1dcd4721028b35fd0bd5c8c57df
text-seal 70751059da2fba395c50aa0eab1f5ee5b934c623c514303c0e7207bb2a888f84
status REFUSED DIVISION-BY-ZERO 2
output-bytes 2
output-sha256 4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865
events 2
trace-head 6ed0717fc44eb9cffab2f5d40365af51cda3179d3785fc82c74bda2a3f73eda6
ops 3
claims 0
end
```
Its trace (2 events):
```
1 S 1 310a 504d87ff9640c0c1c1f656076b94c35da0c630ab03b682908621ee08515cbd9d
2 R 2 4449564953494f4e2d42592d5a45524f 6ed0717fc44eb9cffab2f5d40365af51cda3179d3785fc82c74bda2a3f73eda6
```

**A.4, a cost counter read inside and after its clause (REREAD-1 C8).**

The law bytes:
```
orlog-law 0
(decimals fixed)
(clause 1 0 (let 0 "n" (lit int 0)))
(clause 2 0 (while 5 (< bool (var 0) (lit int 2))))
(clause 3 2 (change + 0 - (lit int 1)))
(clause 4 2 (claim 0 (lit bool 1) (certificate 2) (given )))
(clause 5 0 (claim 1 (lit bool 1) (certificate 2) (given )))
```
TEXTSEAL `5df6a00e450ce11b4163146bdce7e3b7a4d51c44813d67f7cf6841433821ad8b`; the law seal `e5f37d43618027876a969be4fbb3f79371325cba5de7ddb313930cf43cd70cbf`; the seal words `vilug-lujag-kakab-fival`.

The reference's receipt (the core's differs in its backend line only):
```
orlog-receipt 0
backend reference
law-seal e5f37d43618027876a969be4fbb3f79371325cba5de7ddb313930cf43cd70cbf
text-seal 5df6a00e450ce11b4163146bdce7e3b7a4d51c44813d67f7cf6841433821ad8b
status COMPLETED
output-bytes 0
output-sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
events 6
trace-head 72b60be361eea0da803df2f6764fba98de41aff2c6cbac7957187a3c2d5bef2b
ops 14
claims 2
claim 0 4 2 2 0 2 0
claim 1 5 1 1 0 2 12
end
```
Its trace (6 events):
```
1 A 1 00000000490000000000000000 5df1ba66697fdc66a7150bbe2db5ecebfe080a44278454e73042de18467953c5
2 A 3 00000000490000000000000001 45b29220b0d679fd4b4275fecfedf443400b9bd325acd79d049862571ebbf38e
3 C 4 0000000001 3325562db199e3577e59767fbc4eabf87264cc616b70d18c9a61e14597ebd1e4
4 A 3 00000000490000000000000002 7f0cf79be99b15ffcc0fbd5c67857064dbfd370548ffd233e9b9dda5b51a56ca
5 C 4 0000000001 ed8a874bb7530b3f81e2a10d75ef5780394b699f105bb84b897f801bb9019655
6 C 5 0000000101 72b60be361eea0da803df2f6764fba98de41aff2c6cbac7957187a3c2d5bef2b
```

