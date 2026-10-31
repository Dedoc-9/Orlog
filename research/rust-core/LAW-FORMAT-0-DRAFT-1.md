# LAW-FORMAT-0: `orlog-law 0`, the written machine form of a version-0 law (draft 1, 2026-10-30)

**Status.** Draft 1 of RUST-CORE-0's phase 0. It is not a ruling and not yet the core's specification. It applies
REREAD-0's 17 dispositions, which the owner accepted on 2026-10-30 with his answers A1(a) and A2(a) (recorded whole
in [RULINGS.md](RULINGS.md)). A fresh targeted re-read of this draft and of its checker comes before any core code:

> *"Final boundary: draft 1, checker amendments, and another independent re-read are authorized. Rust-core
> implementation, production integration, gate changes, and release changes remain unauthorized."*

- **Draft 0 stays as it was:** `LAW-FORMAT-0-DRAFT-0.md`, sha256 `1ae57ee8…`, the version REREAD-0 read. Its report is
  `REREAD-0-REPORT.md`, and the dispositions are in `REREAD-0-DISPOSITION.md`.
- **Each change from draft 0** carries its finding in brackets, for example *[F1]*.
- **Disagreements:** where this draft and the code at `2e9805a` disagree, that is a finding, and neither is presumed
  right.
- **The checker is evidence, not authority.** In the owner's words: *"the checker is evidence for the format, not the
  format's authority. Its agreement with the document cannot substitute for the independent re-read."*

## 0. For the core's author [F9, F17]

**What you read**, and nothing else (ruling D1):
- this document;
- `SPEC.md` and `RUNTIME-SPEC.md`;
- `vectors/runtime-vectors.txt`, the contract's 20,015 lines;
- `research/rust-core/vectors-as-integer.txt`, 446 supplementary lines for `as an integer` (ruling A2(a)): test data
  generated from the reference, not part of the contract.

You may not read `src/`, `rt_rs/`, `rt_c/`, `twin/`, `research/law-sufficiency/` or any other file of
`research/rust-core/`.

**Where numbers are defined.**
- SPEC.md and RUNTIME-SPEC.md say that numeric meaning is defined by `src/orlog/numeric_ref.py`. You do not read it.
  For you, numbers are defined by SPEC §8, RUNTIME-SPEC §2–§3, section 5a below, and the two vector files.
- If they disagree with the reference, that is a finding for the owner. It is not something you resolve, and it is
  not a reason to read the reference.

**How the core is built:**
- one program, Rust edition 2021, the standard library only;
- no crates, no Cargo, no `unsafe`;
- built by bare `rustc --edition 2021 -O`, warning-free;
- its own SHA-256, written from FIPS 180-4 and checked by the vectors' `sha256` lines;
- no clock, no environment variable, no randomness;
- every file in binary mode, LF only.

**The vector files' lines**, one per line, ASCII, LF: `<op> <arg> … => <result>`. Each argument and each result is one
of:

| token | meaning |
|---|---|
| `i:<int>` | an Int, signed decimal |
| `x:<int>` | a Fix, its raw Q31.32 value, signed decimal |
| `f:<16 hex>` | a Float, its 64 bits, **uppercase** hex |
| `b:0` or `b:1` | a Bool |
| `s:<text>` | printed text, verbatim to the end of the line |
| `hex:<hex>` | bytes, lowercase hex, possibly empty |
| `!<CODE>` | the result is a refusal with that code |

The operation names are RUNTIME-SPEC §2–§3's function names, with `x_as_i` and `f_as_i` for `as an integer` from Fix
and from Float. A harness runs each line and checks the result, as RUNTIME-SPEC §9 says. The law bytes write a Float
in lowercase hex (section 3); the vector files write it in uppercase.

## 1. Notation

`⟨x⟩` names a part defined in this document. `·` is one space (0x20). Every line ends with LF (0x0A). A form is a
parenthesized list: `(`, its items separated by exactly one space, `)`. No space follows `(`, and none precedes `)`,
except in the two empty forms of section 4 (`(given·)` and `(over·)`), which are written with that one space.

**Lines of the law bytes** are numbered from 1: line 1 is `orlog-law 0`, line 2 the decimals line, and clause k is on
line k + 2. A refusal names a line by this number (section 8).

## 2. The bytes

A law is the bytes:

```
orlog-law 0 LF
(decimals ⟨mode⟩) LF
⟨clause line 1⟩ LF
…
⟨clause line n⟩ LF
```

- **n may be 0** *[F12]*. The empty law is exactly `orlog-law 0` LF `(decimals fixed)` LF, which is what an empty text
  compiles to.
- **Every byte** is in 0x20–0x7E, or is LF. There is no CR, no tab, no byte above 0x7E, and no other control byte.
- **⟨mode⟩** is `fixed` or `floats`.
- **Clause line k** (k = 1…n, in order, with no gap) is `(clause k ⟨parent⟩ ⟨statement⟩)` or `(clause k ⟨parent⟩
  absorbed)`.
- **The tree's order** *[F1]*. Clause k's ⟨parent⟩ is one of:
  - 0, when k = 1 or the clause is top-level;
  - k − 1;
  - an ancestor of clause k − 1.

  The clause order is therefore the tree's pre-order, the order of a document: a clause comes after its parent, and
  every descendant of a clause comes before that clause's next sibling. "Before" and "after" in this document mean this
  order. It is also the order of the clauses' outline numbers (section 6, Labels).
- **There is nothing** after the last line's LF.

**The law seal** is SHA-256 of these bytes, exactly (SPEC §9). **The seal words** are derivation 19.

## 3. Atoms

| atom | written | canonical form |
|---|---|---|
| ⟨n⟩, a natural number (ids, the fuel, Int and Fix literal values) | decimal | the digits 0–9, no sign, no leading zero (`0` alone for zero) |
| ⟨hex16⟩, a Float literal | 16 hex digits | lowercase, exactly 16: the 64 bits of the binary64 as an unsigned integer, most significant digit first |
| ⟨str⟩, a string | `"` … `"` | see below |
| ⟨label⟩, a clause reference by outline number | dotted decimals | each part a canonical ⟨n⟩ of at least 1, joined by `.`: the clause's outline number (section 6, Labels) |
| ⟨word⟩ | letters, digits, `-`, `+`, `*`, `/`, `<`, `>`, `=`, `!` | exactly the words this document lists, and no others |

**A string** *[F5, A1(a)]* is a sequence of Unicode scalar values: code points 0–0x10FFFF, outside 0xD800–0xDFFF.
Between its quotes, each scalar value is written in order:
- `"` as `\"`;
- `\` as `\\`;
- any other value from U+0020 to U+007E as itself;
- every other value as `\u{h}`, where h is the value in lowercase hex with no leading zero, 1 to 6 digits.

Every scalar value may stand in a string, the controls and the bidirectional controls included (the owner's ruling
A1(a)). Which characters a *text* may contain is the source language's business, not the format's. The format needs no
Unicode table. Its constraints are these:
- an `\u{h}` that names a surrogate, or a value above 0x10FFFF, is refused;
- so is an `\u{h}` with a leading zero or more than 6 digits;
- so is a value written as `\u{h}` that the rules above write as itself, or the reverse.

A text value at run time is the UTF-8 encoding of the string's scalar values.

**Names** (of a `let`, a `procedure`, a `define`, and in `(rule …)`) are strings by the same rules. *[F14]* A run reads
rule names only: a `(rule ⟨str⟩)` names the defines whose name is the same sequence of scalar values, compared exactly.
No run reads the other names. They are kept and written back, and nothing checks them (section 8).

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
- ⟨body⟩ is `(block ⟨C⟩)`, meaning the children of clause ⟨C⟩, or one inline statement.

**The shapes of an If chain at clause K** *[F6]*:
- the first arm's ⟨C⟩ is K;
- each later arm's ⟨C⟩ is an absorbed Otherwise clause;
- the else is one of:
  - `-`;
  - an else whose ⟨C⟩ is an absorbed clause, with an inline or a block body;
  - an else whose ⟨C⟩ is K itself. That is the inline otherwise of the If's own line, `If C, S; otherwise S`. It is
    allowed only when the chain has exactly one arm, that arm's body is inline, and the else's body is inline.
- A `(block ⟨C⟩)` in an arm or an else always names that arm's or else's own ⟨C⟩.
- The chain's absorbed clauses are the siblings that come right after K, in written order: the later arms, then an
  absorbed else.

*(Corrected before REREAD-0, 2026-10-30. The first draft said every later arm and every else carries an absorbed
clause's id; the checker refused 20 of the 298 laws on that rule.)*

**Oracles (⟨oracle⟩):**
- `(computation)`
- `(owner)`
- `(theorem ⟨str⟩)`
- `(certificate ⟨C⟩)` or `(certificate ⟨C⟩ ⟨str⟩)`, the latter under a named theorem
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
| `(promote ⟨target⟩ ⟨E⟩)` | an implicit promotion of an Int (SPEC §5), counted like a conversion (SPEC §7); it stands only where W9 says | ⟨target⟩ |
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

**The types (⟨type⟩):** `int`, `fix`, `float`, `bool`, `text`, and the list types `list-int`, `list-fix`,
`list-float`, `list-bool` (⟨list type⟩).

## 5. What runs, and where

**The walk** *[F2]*. Running a sequence of clauses runs each clause's statement in clause order, and skips each
absorbed clause (an absorbed clause is reached only through its If). A run runs the sequence of top-level clauses.
Running a statement S as clause C goes as follows:
- **an If:** for each arm in written order, evaluate its condition as the arm's ⟨C⟩. On true, run its body and stop:
  an inline body runs as the arm's ⟨C⟩, and `(block ⟨C⟩)` runs the sequence of ⟨C⟩'s children. If no arm ran, run
  the else's body, likewise.
- **a While, a For:** as SPEC §7 says. The body is the sequence of C's children.
- **a procedure, a define, a decimals:** nothing in place (but see the budget check below). A procedure's body runs only
  through `perform`.
- **a perform:** runs the sequence of the procedure clause's children. Each of those clauses runs as its own id, not as
  the performing clause *[F13]*.
- **any other statement:** as SPEC §7 says.

**The clause a statement runs as** *[F13]*. This is the clause SPEC §7 names in events and refusals. It is also "the
clause of the statement" throughout this document:
- a clause's own statement: the clause's id;
- an arm's condition and its inline statement: the arm's ⟨C⟩;
- an else's inline statement: the else's ⟨C⟩;
- a rule's provisos and values: the clause under which the use of the rule is evaluated, by the bullets above. So a use
  in an absorbed arm's condition runs as that absorbed clause (SPEC §6).

**Cost counters** *[F13]*. A clause named by a certificate has a cost counter (SPEC §7). It grows by the operations
counted while that clause's statement runs as one clause of a sequence:
- an If clause's counter covers every arm and the else, the absorbed arms' blocks included;
- a performing clause's counter covers the procedure's body;
- the counters of nested counted clauses grow too.

An absorbed clause is never run as a member of a sequence, and an inline statement is not a clause, so neither has a
counter of its own. (W12 forbids a certificate to name an absorbed clause.)

**The host budget's check** *[F7]*. When a budget B is given (section 10), the check "if ops > B, stop" is made
immediately before each statement is run:
- each non-absorbed clause of a sequence, the do-nothing statements `define`, `procedure` and `decimals` included;
- each inline arm or else statement.

It is never made for an absorbed clause, before an arm's condition, before a loop's iteration, or inside an expression.

## 5a. The functions behind the operators *[F10]*

The names are RUNTIME-SPEC §2's functions (`i_` Int, `x_` Fix, `f_` Float). The refusal order is RUNTIME-SPEC's, or
SPEC §8's where it says.

| form, by operand type | function | notes |
|---|---|---|
| `+ - * /`, `max`, `min` on int, fix, float | `i_add` … `x_div` … `f_min` | by ⟨type⟩ |
| `quot`, `rem` | `i_quot`, `i_rem` | Euclidean (SPEC §8) |
| `neg`, `abs`, `sqrt` | `i_neg`/`x_neg`/`f_neg`, …, `i_isqrt`/`x_sqrt`/`f_sqrt` | by the operand's type |
| `trunc` | `x_trunc`, `f_trunc` | |
| `rounded int` from fix, float | `x_round`, `f_round` | half-even |
| `as int` from fix | `x_as_i` | INEXACT-CONVERSION unless the fraction bits are zero; then truncation |
| `as int` from float | `f_as_i` | NOT-FINITE, then INEXACT-CONVERSION, then OVERFLOW (SPEC §8). Vectors: the supplementary file |
| `as fix`, `rounded fix` from int | `x_from_i` | one function for both; OVERFLOW when the value does not fit Q31.32 |
| `as fix`, `rounded fix` from float | `f_to_x` with rounded = 0 or 1 | |
| `as float`, `rounded float` from int | `f_from_i` with rounded = 0 or 1 | |
| `as float`, `rounded float` from fix | `x_to_f` with rounded = 0 or 1 | |
| `promote fix` | `x_from_i` | OVERFLOW when the Int does not fit Q31.32 |
| `promote float` | `f_from_i` with rounded = 0 | INEXACT-CONVERSION when the Int has no exact binary64 |
| `<` on float | `f_lt` | IEEE |
| `==` on float | `f_eq` | IEEE: NaN ≠ NaN, and −0 = +0 |
| `<=`, `>`, `>=`, `!=` on float | IEEE's own comparison | not by negating another: every comparison with a NaN is false, except `!=`, which is true |
| `< <= > >= == !=` on int and fix | the signed integers, a Fix by its raw value | |
| `==`, `!=` on bool | equality of the two truth values | |
| `==`, `!=` on text | equality of the bytes | |
| `even`, `odd`, `zero`, `positive`, `negative` | SPEC §5, §8 | on a Float, `zero` is true of ±0, and a NaN is neither positive nor negative |

## 6. The derivations

A reader must derive each of these from the bytes alone. The interpreter or the backends read each of them, and none
is written in the bytes as such. The *held by* column names the test that measured the derivation against the analysis
at `2e9805a` (LS-0, LS-1: LAW-SUFFICIENCY-0 and -1; FC: the checker, section 11).

| # | derivation | from the bytes | read by | held by |
|---|---|---|---|---|
| 1 | **the top** | the clauses whose ⟨parent⟩ is 0, in clause order | run | LS-0 test 3; FC |
| 2 | **children** | the clauses whose ⟨parent⟩ is this clause's id, in clause order | run | LS-0 test 3; FC |
| 3 | **cost-tracked clauses** | the clauses named by some `(certificate ⟨C⟩ …)` | run | LS-0 test 3; FC |
| 4 | **the rules** | for each rule name, its `define` clauses in clause order | run | LS-0 test 3; LS-1 E2; FC |
| 5 | **the overrides** | for each rule name and each of its defines d, the set of define clauses d beats: the transitive closure of the `(over …)` lists | run | LS-0 test 3; FC |
| 6 | **the claim sites** | the claims in claim-id order (0, 1, …), each with the clause it runs as (section 5); the receipt lists them in that order | run | LS-0 test 3; FC |
| 7 | **a claim site's clause** | the clause the claim runs as: its own clause, or the arm's or else's ⟨C⟩ for an inline claim | run | LS-0 test 3; FC |
| 8 | **a variable's type** | a `let`'s variable: the type of its ⟨E⟩, which is never a `promote` (W9) *[F15]*; a `for`'s counter: int | run, backends | LS-0 test 3; LS-1 E3; FC |
| 9 | **a change's element type** | without an index: the variable's type; with one: the variable's list element type | run | LS-0 test 3 |
| 10–15 | **an expression's type** | section 4's type column; for `(var ⟨V⟩)` derivation 8, for `(rule ⟨str⟩)` derivation 17 | run (Say, Cat's parts, a conversion's and a unary operator's operand), backends | LS-0 tests 1 and 3; LS-1 E1 |
| 16 | **the variables** | every variable, `let` and `for` alike, in id order. The ids are 0…m−1 in the order the walk of section 7 meets their declarations *[F2]* | backends | LS-1 E3, E4; FC |
| 17 | **a rule's type** | the type of its first `define`'s value | run (through 10–15), backends | LS-1 E3; FC |
| 18 | **a variable's top** | true exactly for a `let` that is the statement of a top-level clause, not inline; false for every other `let` and every `for` counter | backends | LS-1 E3, E4; FC |
| 19 | **the seal words** *[F16]* | the first 64 bits of the SHA-256 of the bytes, as four proquints (SPEC §9); the value of `(seal)`, and printed by the backends | run, backends | not measured against the reference here (SPEC §9 gives one worked value, all zeros) |

Two further derivations hold no field:

- **Labels.** A clause's outline number. The top-level clauses are numbered 1, 2, … in clause order, absorbed ones
  included. Each clause's children are numbered by appending `.1`, `.2`, … to its parent's number. A ⟨label⟩ in
  `given` or `agreement` names the clause whose outline number it is. (A text may spell a reference `§02`. The front
  end reads it as `2`, and the bytes hold `2`.)
- **Decimals.** ⟨mode⟩ in line 2 is the mode of the law's `(decimals …)` clause if it has one, else `fixed`. Every
  decimal literal is of that mode: `(lit fix …)` under `fixed`, `(lit float …)` under `floats` (W6).

## 7. The order obligations

These hold in any reader. They are part of the format, not accidents of one implementation.

1. **A rule's definitions are taken in clause order.** Every proviso first, in clause order, then the values of the
   definitions that remain, in clause order. The first refusal ends the run (SPEC §6). Which refusal a law ends in can
   depend on this order (LS-1 E2).
2. **A sequence runs in clause order,** and an If chain's arms in written order (section 5).
3. **Ids are numbered by the walk** *[F2]*. The walk is section 5's order of running, taken over the whole law without
   evaluating anything:
   - the top-level sequence;
   - in a sequence, each non-absorbed clause in clause order;
   - in a clause:
     - its statement's own expressions, in the order SPEC §7 evaluates them;
     - for an If, each arm in written order: its condition, then its body (an inline statement, or the block's
       sequence), then the else's body;
     - for a While, a For or a procedure: its children's sequence after the statement.
   
   Variables, claims and musts each get ids 0, 1, … in the order the walk meets their declaration:
   - a `let`'s variable, after its value;
   - a `for`'s counter, after its bounds and before its body.

   A procedure's body is walked once, where its clause stands, not where it is performed.

   **Example.** The walk can number a declaration written on an earlier line after one written on a later line. For the
   text `§1 If true, do the following. §1.1 Let a be 1. §2 Otherwise, let b be 2.` the bytes are:

   ```
   (clause 1 0 (if (arm 1 (lit bool 1) (block 1)) (else 3 (let 1 "b" (lit int 2)))))
   (clause 2 1 (let 0 "a" (lit int 1)))
   (clause 3 0 absorbed)
   ```

   Variable 1 is written on line 3, before variable 0 on line 4. That is right: the walk meets `a` (in arm 1's block)
   before `b` (in the else).
4. **A `define`'s `(over …)` list keeps its written order.** The order does not change the closure, but the round trip
   writes it back as written.

## 8. Well-formedness: what a reader must refuse

A reader that runs law bytes must refuse, before anything runs, every byte string that breaks one of these checks
(ruling D3). Each mirrors a check the front end makes, named in parentheses.

**What a pass means** *[F17]*. Format validity is not the same as source admissibility (the owner's distinction under
A1). A byte string that passes every check is meant to run without a fault the front end would have prevented. Its
text literals and names may still hold characters no text can (A1(a)). Its names are unchecked. Whether every check
holds that promise is question Q1 for the targeted re-read.

| | check |
|---|---|
| W1 | **the bytes and the tree** *[F1, F12]*: section 2's character set; the two header lines; the clause lines numbered 1…n (n ≥ 0); each parent 0, k−1 or an ancestor of k−1; the final LF |
| W2 | **the forms and their atoms** *[F8]*: every line parses as section 4's forms, each atom canonical by section 3 (numbers, hex, labels, words, and each string in exactly its canonical escapes) |
| W3 | **the spacing** *[F8]*: single spaces between items, none after `(` or before `)` but in `(given·)` and `(over·)`, nothing at a line's ends. Once W2 holds, writing what was read gives the line back exactly if and only if W3 holds |
| W4 | every ⟨C⟩ names an existing clause; every ⟨label⟩ is the outline number of an existing clause |
| W5 | **bodies and If chains** *[F6]* (EMPTY-BLOCK, UNEXPECTED-CHILDREN, ORPHAN-OTHERWISE): a clause has children exactly when it is a `while`, `for` or `procedure`, or is named by a `(block ⟨C⟩)`, and then at least one; a block names its arm's or else's own ⟨C⟩; every If chain has section 4's shape; each absorbed clause is named by exactly one arm or else of exactly one If |
| W6 | **places and the decimals** *[F11]* (DEFINE-PLACE, PROCEDURE-PLACE, DECIMALS-PLACE): `define`, `procedure` and `decimals` are top-level clause statements, never inline. There is at most one `decimals`, and the walk meets no decimal literal before it. Line 2's mode is derivation "Decimals". A `(lit fix …)` stands only under `fixed`, a `(lit float …)` only under `floats` |
| W7 | **inline**: an inline body is a form section 4 marks inline |
| W8 | **variables** *[F2]* (UNDECLARED, LOOP-VARIABLE): ids are numbered by the walk (section 7), each declared once. Each use is in scope (below). A `for` counter is never set, changed, appended to or removed from |
| W9 | **types and promotions** *[F4, F15]* (TYPE): every expression's type agrees with SPEC §5 by the rules below, and a `promote` stands only where the rules below put one |
| W10 | **rules** (RULE-BEFORE-DEFINITION, NOTWITHSTANDING-TARGET, PRIORITY-CYCLE): every define of a name has one type, not a list; a proviso is bool; each `(over ⟨C⟩)` names a define of the same name; no define beats itself in the closure; a `(rule ⟨str⟩)` names a rule with at least one define. The use runs as a clause whose id is greater than the last define's of that name; inside a procedure's body, it is the procedure's clause id that must be greater |
| W11 | **procedures** (PERFORM-BEFORE-DEFINITION, UNKNOWN-PROCEDURE): `(perform ⟨C⟩)` names a `procedure` clause whose id is less than that of the clause the perform runs as, and the perform is not in that procedure's body |
| W12 | **claims** *[F2]* (CERTIFICATE-TARGET, AGREEMENT-TARGET, PREMISE-TARGET), all relative to the clause the claim runs as: a certificate's ⟨C⟩ is a smaller id, not absorbed, and its statement is not a `procedure`, `define`, `decimals` or `claim`; agreement's two labels name clauses with smaller ids; each `given` label names a clause whose own statement is a `claim` |
| W13 | **ranges** (FUEL, LITERAL-RANGE): a While's ⟨n⟩ is in 1…2^62; Int and Fix ⟨n⟩ are ≤ 2^63−1; a Float literal is finite with sign bit 0; a text literal is at most 2^24 bytes of UTF-8 |
| W14 | **depth** *[F3]* (NESTING-DEPTH, LOOP-NESTING, EXPRESSION-DEPTH), see below |

**W9's rules, by form.** "Numeric" means int, fix or float.
- **`+ - * / max min`:** the two operands' types, after promotion, are one numeric type, which is ⟨type⟩.
- **`quot`, `rem`:** two int operands; ⟨type⟩ int.
- **`< > <= >=`:** after promotion, one numeric type; ⟨type⟩ bool.
- **`==`, `!=`:** after promotion, one type that is numeric, bool or text; ⟨type⟩ bool.
- **`and`, `or`:** two bool operands; ⟨type⟩ bool.
- **`not`:** a bool operand; ⟨type⟩ bool. *[F15]*
- **`even`, `odd`:** an int operand. **`zero`, `positive`, `negative`:** a numeric operand. All five have ⟨type⟩ bool.
  *[F15]*
- **`neg`, `abs`, `sqrt`:** a numeric operand of the same type as ⟨type⟩.
- **`trunc`:** a fix or float operand; ⟨type⟩ int.
- **`as`, `rounded`:** SPEC §5's table of sources and targets.
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
- **Conditions** of `if`, `while`, `must` and `claim`: bool.
- **`for`'s bounds:** int.
- **`append`:** a list variable, and a value that after promotion has its element type.
- **`remove-last`:** a list variable.

**Where a `promote` may stand** *[F4]*, exactly as SPEC §5 promotes. Everywhere else it is refused.
1. **As one operand** of `+ - * / max min`, of a comparison, or of `==` or `!=`, when the other operand's type is the
   promote's target. At most one operand of an operator is a promote, and the other is not one.
2. **As the stored value** of a `set`, a `change` or an `append`, when the variable's type (or its element type) is
   the promote's target. Never as a `let`'s value.
3. **As an item** of a `list` whose element type is the promote's target, with at least one item of that list not a
   promote.

A `promote`'s operand is never a `promote`, since its type is int. A reader never promotes on its own.

**The scope of a variable (W8).** A use (`var`, `item`, `length`, `set`, `change`, `append`, `remove-last`) runs as some
clause U (section 5). It is in scope when:
- **for a `let` that is the statement of clause D:** U is a later sibling of D (both top-level, or both children of one
  clause), or a descendant of such a sibling;
- **for a `let` inline in an arm or an else:** never. The arm opens its own scope.
- **for a `for` counter declared by clause F:** U is a descendant of F.

So a use inside a procedure's body sees the top-level variables declared before the procedure's clause. A `define`'s
value and proviso see the top-level variables declared before the `define`'s clause.

**W14, depth** *[F3]*:
- **(a)** a clause is at most 24 deep: a top-level clause is depth 1, its children depth 2. This is the front end's 24
  label parts.
- **(b)** a `while` or `for` clause has at most 16 `while` and `for` clauses among itself and its ancestors, counting
  only those below the nearest `procedure` ancestor. This is the front end's 16 nested loops within one body.
- **(c)** every expression in the bytes is at most **126** deep. Here a form with no expression operand (a literal,
  `seal`, `var`, `rule`, `length`) is depth 1, and every other form is one more than its deepest operand.

  The derivation, for the re-read to check:
  1. The front end refuses a statement whose parsed tree is deeper than 64 (`EXPRESSION-DEPTH`). There the statement
     counts as depth 1 and each operand one deeper, so every expression it holds is at most 63 deep as parsed.
  2. After that check the analysis adds two things. A `promote` above an Int operand or value: each parsed node has at
     most one directly above it, so a path's length at most doubles. A `not` above the condition of an Unless, or of a
     define's `unless` (SPEC §11 items 15 and 24): one level, on a bool root, which is never promoted.
  3. So a stored value's path is at most 63 + 63 = 126. A condition's is at most 1 + 63 + 62 = 126, its bool root
     taking no promote.
  
  The front end checks (a) and (b) itself. (c)'s bound is derived, and is not one the front end checks in the bytes.

**What the front end checks and this list does not:** the names. Shadowing and a name used for two things
(REDECLARED, PROCEDURE-NAME) concern the text's words. A reader keeps each name as written, and does not check them.
Two laws that differ only in names have different seals and the same run.

**Which refusal is reported** *[F8]*. A reader reports exactly one, chosen this way:
1. W1, scanning from the start: the first line that fails it.
2. Else, line by line: the first line that fails W2, or W3 when W2 holds for it. On one line, W2 is reported before W3.
3. Else, among every failure of W4–W14: the one on the least line, and on that line the least W.
   - Each failure belongs to the line whose bytes hold it. A failure in an inline statement belongs to its If's line.
     A clause's children or If-chain shape belongs to that clause's line. A notwithstanding cycle belongs to the line
     of each define in it. Line 2's mode belongs to line 2.
   - A check that needs something an earlier failure leaves underived (a missing clause, an undeclared variable's
     type, a rule with no define) is not made.

**What refusing means.** A reader refuses by writing no file and ending with a load refusal (section 10).

## 9. Exact reconstruction (the round trip)

A reader keeps every written part:
- names and strings;
- labels;
- the order of `(over …)` lists and of `given` labels;
- the absorbed clauses.

Writing it back by sections 2–4 gives the bytes it read, byte for byte. W2 and W3 refuse every other bytes.

Writing is defined by the tables. For every form, items are written in the table's order, separated by one space, atoms
canonical. Two writers that follow this document write identical bytes for one law. REREAD-0's Q5 compared every form
with the writer at `2e9805a`, character for character, and found no divergence.

**Held by:** LS-0 test 3 (290 of 290); LS-1 E1, E3 (298 of 298); FC (298 of 298).

## 10. The run interface *[F8]*

`rust-core LAW TEXTSEAL OUT RECEIPT [TRACE] [--budget B]`. The arguments are positional. `--budget B` may only be the
last two.
- **LAW:** a path to the law bytes.
- **TEXTSEAL:** exactly 64 lowercase hex digits. It is printed in the receipt's `text-seal` line as given. It is the
  caller's input: it is not in the law bytes, and the core never derives or validates it (the owner's ruling). Only its
  form is checked.
- **OUT, RECEIPT, TRACE:** RUNTIME-SPEC §6's output, receipt and trace paths.
- **B:** a canonical decimal from 0 to 2^64−1. Without `--budget`, there is no budget.

**Output is buffered,** and written only at the end of a completed or refused run. The trace is written as events
happen, if TRACE is given. The receipt is written last.

| outcome | when | files | exit | stderr |
|---|---|---|---|---|
| completed | the run ends | OUT, the TRACE if given, then RECEIPT (`status COMPLETED`) | 0 | nothing |
| refused | the run refuses (SPEC §7) | OUT up to the refusal, the TRACE, then RECEIPT (`status REFUSED <CODE> <clause>`) | 0 | nothing |
| stopped | the budget's check (section 5) finds ops > B | the TRACE alone, if given, holding every event before the stop; OUT and RECEIPT not written | 4 | `STOPPED-BY-HOST after <ops> counted operations (budget <B>)` |
| load refusal | the bytes fail a check (section 8) | none: no file is opened for writing | 3 | `LAW-REFUSED W<k> line <n>: <reason>` |
| usage error | wrong argument count or order; TEXTSEAL not 64 lowercase hex digits; B not a canonical decimal in range | none | 2 | `USAGE: <reason>` |
| I/O error | LAW cannot be read, or OUT, RECEIPT or TRACE cannot be written | whatever was written before the error; never a RECEIPT after it | 2 | `IO-ERROR: <reason>` |

- `<k>`, `<n>`: the W and the line chosen in section 8. `<reason>` is free text, which no comparison reads.
- A file is created, or truncated if it exists, only when it is written. The core removes nothing, so a caller that
  wants no stale file removes it before the run, as the arbiter does.
- The receipt's backend line is `backend rust-core` (ruling D5). Its law seal is the SHA-256 of the bytes read,
  computed by the core.

## 11. How this document is held to the code, and the code to it

**The checker.** `research/rust-core/format_check.py`, written from sections 2–4 and 8. It is outside the core
author's reading set. On every one of LAW-SUFFICIENCY's 298 laws, and on the fixture laws below:
- it parses the bytes and checks W1–W14;
- it writes them back;
- it computes the derivations and compares them with the analysis's own.

Every law must pass and come back exactly. Each planted malformation must be refused, on the line and by the W that
section 8 chooses.

**The fixture laws** *[F2, F12]* are REREAD-0's valid laws, which the checker must accept:
- the forward-declaration law of section 7;
- the same law with a claim in each place;
- a certificate of §1.1 from a claim inline in §2's otherwise;
- the empty law.

**The plants** are REREAD-0's counterexamples, which the checker must refuse:
- F1's three clauses, refused W1;
- a 300-deep chain of `not` (F3), refused W14;
- F4's three promotes, refused W9;
- F6's two If chains, refused W5;
- a `\u{d800}`, refused W2.

Draft 0's thirteen plants stay. **Evidence:** `evidence/rust-core-format-1.txt`.

**What it does not show.**
- That every law the front end can produce passes W1–W14. It shows that the 298 and the fixtures do.
- That no byte string passing them can fault, which is Q1 below.
- In the owner's words, the checker *"cannot substitute for the independent re-read"*.

## 12. Questions for the targeted re-read

- **Q1.** With F1–F17 applied, can a byte string pass W1–W14 and still fault a run (crash, read an unassigned variable,
  loop without bound, overflow a stack), or run differently in two readers that follow this document?
- **Q2.** Is any check now stricter than the front end? In particular: the walk order of ids (section 7), the promote
  placements, the If-chain shapes, and W14(c)'s bound of 126. Is that bound's derivation right, and tight enough that
  no front-end law exceeds it?
- **Q3.** Is section 5a's table faithful to SPEC, RUNTIME-SPEC and the vectors, and is it enough for an author who
  never reads `numeric_ref.py`?
- **Q4.** Is section 10's table complete? Does every outcome have one exit status, one set of files and one stderr?
- **Q5.** Does the checker (`format_check.py`) implement sections 2–4 and 8 as written? Name every place it is
  stricter, looser, or reports another (line, W) than section 8 chooses.
- **Q6.** Did any change from draft 0 break what REREAD-0 found right (Q5's writing, the 16 derivations)?

## Changes from draft 0

| finding | where |
|---|---|
| F1 | section 2, the tree's order; W1 |
| F2 | sections 5 and 7, the walk; derivation 16; W8; W12; the example |
| F3 | W14 |
| F4 | W9, where a promote may stand; derivation 8 |
| F5 | section 3, strings as scalar values; A1(a) |
| F6 | section 4, the shapes of an If chain; W5 |
| F7 | section 5, the host budget's check |
| F8 | section 8, which refusal is reported; W2 and W3 kept apart; section 10's table |
| F9 | section 0, where numbers are defined; A2(a)'s vectors |
| F10 | section 5a |
| F11 | W6 |
| F12 | section 2, n ≥ 0 and the empty law |
| F13 | section 5, the clause a statement runs as, performed bodies, cost counters |
| F14 | section 3, names |
| F15 | W9's wording; derivation 8 |
| F16 | derivation 19 |
| F17 | section 0, for the core's author; section 8, what a pass means |
