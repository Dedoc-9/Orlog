# LAW-FORMAT-0: `orlog-law 0`, the written machine form of a version-0 law (draft, 2026-10-30)

**Status.** A draft of RUST-CORE-0's phase 0, owed by the owner's ruling 2 of 2026-10-30:

> *"The format must make explicit obligations of: Every execution-relevant derivation required by the interpreter and
> backends, including `Analysis.vars`, `Analysis.rule_types`, and `VarInfo.top`. The order of a rule's definitions,
> because that order can determine which refusal terminates execution. Exact reconstruction from law bytes, including
> the round-trip requirement."*

It is not a ruling, and it is not yet the core's specification. Its independent re-read comes first, and that
re-read's findings are disposed before any core is written (his condition 1). Where this draft and the code at
`2e9805a` disagree, the disagreement is a finding, and neither is presumed right.

**What it is for.** The core's author reads this document, SPEC.md, RUNTIME-SPEC.md and `vectors/runtime-vectors.txt`,
and nothing else (ruling D1). This document says what the law bytes are, what each one means in SPEC's terms, what
must be derived from them, in what order, and what a reader must refuse.

**What it leaves to the specifications:**
- what a statement does when it runs: SPEC §6 (rules), §7 (dynamic semantics, operation counting) and §8 (numbers);
- the numeric functions and printing: RUNTIME-SPEC §2–§3;
- the event chain, the trace and the receipt: RUNTIME-SPEC §5 and §7;
- the seal words: SPEC §9.

SPEC §9 says the law bytes are what `sema.py`'s `law_bytes` writes. This document is the same definition, written out,
and section 11 says how the two are held together.

## 1. Notation

`⟨x⟩` names a part defined in this document. `·` is one space (0x20). Every line ends with LF (0x0A). A form is a
parenthesized list: `(`, its items separated by exactly one space, `)`. No space follows `(`, and none precedes `)`,
except in the two empty forms of section 4 (`(given·)` and `(over·)`), which are written with that one space.

## 2. The bytes

A law is the bytes:

```
orlog-law 0 LF
(decimals ⟨mode⟩) LF
⟨clause line 1⟩ LF
…
⟨clause line n⟩ LF
```

- **Every byte** is in 0x20–0x7E, or is LF. There is no CR, no tab, no byte above 0x7E, and no other control byte.
- **⟨mode⟩** is `fixed` or `floats` (section 6, the Decimals obligation).
- **Clause line k** (k = 1…n, in order, with no gap) is `(clause k ⟨parent⟩ ⟨statement⟩)` or `(clause k ⟨parent⟩
  absorbed)`.
  - ⟨parent⟩ is 0 for a top-level clause, or the id of an earlier clause.
  - ⟨statement⟩ is a statement form (section 4).
  - `absorbed` marks an Otherwise clause taken into an If chain. It holds no statement of its own.
- **There is nothing** after the last clause line's LF.

**The law seal** is SHA-256 of these bytes, exactly (SPEC §9).

## 3. Atoms

| atom | written | canonical form |
|---|---|---|
| ⟨n⟩, a natural number (ids, the fuel, Int and Fix literal values) | decimal | the digits 0–9, no sign, no leading zero (`0` alone for zero) |
| ⟨hex16⟩, a Float literal | 16 hex digits | lowercase, exactly 16: the 64 bits of the binary64 as an unsigned integer, most significant digit first |
| ⟨str⟩, a string | `"` … `"` | each character of the string, in order: `"` written `\"`; `\` written `\\`; a character from U+0020 to U+007E (other than those two) written as itself; every other character written `\u{h}`, where h is its code point in lowercase hex with no leading zero |
| ⟨label⟩, a clause reference by outline number | dotted decimals | each part canonical as ⟨n⟩, at least 1, joined by `.`: the clause's outline number (section 6, Labels) |
| ⟨word⟩ | letters, digits, `-`, `+`, `*`, `/`, `<`, `>`, `=`, `!` | exactly the words this document lists, and no others |

A ⟨str⟩ is the only place `"` and `\` appear. A string's characters are code points. A text value at run time is the
string's UTF-8 bytes.

## 4. The forms

### Statements (⟨statement⟩), each the statement of one clause, or inline in an arm or an else

| form | SPEC construct | may stand inline |
|---|---|---|
| `(let ⟨V⟩ ⟨str⟩ ⟨E⟩)` | Let: variable ⟨V⟩, its name ⟨str⟩, its value ⟨E⟩ | yes |
| `(set ⟨V⟩ ⟨E or -⟩ ⟨E⟩)` | Set X (`-`) or Set item I of X: the index, then the value | yes |
| `(change ⟨sign⟩ ⟨V⟩ ⟨E or -⟩ ⟨E⟩)` | Increase (`+`) or Decrease (`-`): the variable, its index or `-`, the amount | yes |
| `(say ⟨E⟩)` | Say | yes |
| `(if ⟨arm⟩ … ⟨arm⟩ ⟨else⟩)` | an If chain: one or more arms, then its otherwise or `-` | no |
| `(while ⟨n⟩ ⟨E⟩)` | While, its bound ⟨n⟩ and its condition; the body is this clause's children | no |
| `(for ⟨V⟩ ⟨E⟩ ⟨E⟩)` | For, its counter ⟨V⟩, from, to; the body is this clause's children | no |
| `(procedure ⟨str⟩)` | To (a procedure's definition); its body is this clause's children | no |
| `(perform ⟨C⟩)` | Perform: ⟨C⟩ is the procedure's clause id | yes |
| `(must ⟨M⟩ ⟨E⟩)` | the must form, must id ⟨M⟩ | yes |
| `(claim ⟨K⟩ ⟨E⟩ ⟨oracle⟩ (given ⟨label⟩ … ⟨label⟩))` | the claim form, claim id ⟨K⟩; its premises, possibly none, written `(given·)` | yes |
| `(define ⟨str⟩ ⟨E⟩ ⟨E or -⟩ (over ⟨C⟩ … ⟨C⟩))` | Define: its rule's name, its value, its proviso or `-`, the definitions it overrides by clause id, in the order written, possibly none, written `(over·)` | no |
| `(append ⟨V⟩ ⟨E⟩)` | Append | yes |
| `(remove-last ⟨V⟩)` | Remove the last item | yes |
| `(decimals ⟨mode⟩)` | Decimals | no |

**Parts of the If chain:**
- ⟨arm⟩ is `(arm ⟨C⟩ ⟨E⟩ ⟨body⟩)`.
- ⟨else⟩ is `(else ⟨C⟩ ⟨body⟩)` or `-`.
- ⟨body⟩ is `(block ⟨C⟩)`, meaning the children of clause ⟨C⟩, or one inline statement.
- An arm's or an else's ⟨C⟩ is the clause it is written in:
  - the first arm's is the If's own clause;
  - every later arm's is an absorbed Otherwise clause's id (SPEC §11 item 18);
  - an else's is either the If's own clause, when the otherwise is inline in the If's own line (`If C, S; otherwise
    S`, and then its body is inline), or an absorbed Otherwise clause's id.

  *(Corrected 2026-10-30, before the re-read. The first draft said every later arm and every else carries an absorbed
  clause's id. The checker refused 20 of the 298 laws on that rule, each with an inline otherwise in the If's own
  line.)*

**Oracles (⟨oracle⟩):**
- `(computation)`
- `(owner)`
- `(theorem ⟨str⟩)`
- `(certificate ⟨C⟩)` or `(certificate ⟨C⟩ ⟨str⟩)`, the latter being under a named theorem
- `(agreement ⟨label⟩ ⟨label⟩)`

### Expressions (⟨E⟩)

| form | meaning | its type (section 6, Types) |
|---|---|---|
| `(lit int ⟨n⟩)` | an Int literal, n ≤ 2^63−1 | int |
| `(lit fix ⟨n⟩)` | a Fix literal; n is the raw Q31.32 value, ≤ 2^63−1 | fix |
| `(lit float ⟨hex16⟩)` | a Float literal: finite, sign bit 0 | float |
| `(lit bool 0)`, `(lit bool 1)` | false, true | bool |
| `(str ⟨str⟩)` | a text literal, at most 2^24 UTF-8 bytes | text |
| `(seal)` | this law's seal words | text |
| `(var ⟨V⟩)` | the variable ⟨V⟩'s value | the variable's type |
| `(rule ⟨str⟩)` | a use of the rule so named (SPEC §6) | the rule's type |
| `(⟨binary⟩ ⟨type⟩ ⟨E⟩ ⟨E⟩)` | a binary operator; ⟨type⟩ is its result's type | ⟨type⟩ |
| `(⟨unary⟩ ⟨type⟩ ⟨E⟩)` | a unary operator; ⟨type⟩ is its result's type | ⟨type⟩ |
| `(as ⟨target⟩ ⟨E⟩)`, `(rounded ⟨target⟩ ⟨E⟩)` | a conversion (SPEC §5, §8) | ⟨target⟩ |
| `(promote ⟨target⟩ ⟨E⟩)` | an implicit promotion of an Int (SPEC §5): counted like a conversion (SPEC §7) | ⟨target⟩ |
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

Statements run as SPEC §7 says. A run starts at the top-level clauses (parent 0), in clause order. Running a sequence
of clauses runs each clause's statement in clause order, and skips each absorbed clause.

**Bodies:**
- A While's, a For's and a procedure's body is its clause's children.
- A ⟨body⟩ of `(block ⟨C⟩)` is clause ⟨C⟩'s children.
- An inline ⟨body⟩ is its one statement.

**Not run in place:** `define`, `procedure` and `decimals`. A procedure runs its body only through `perform`.

**The clause of a statement** (what SPEC §7 names in events, refusals and costs):
- a clause's own statement: the clause's id;
- an arm's condition and its inline statement: the arm's ⟨C⟩;
- an else's inline statement: the else's ⟨C⟩;
- a rule's provisos and values, when used: the clause of the statement that uses the rule (SPEC §6).

## 6. The derivations

A reader must derive each of these from the bytes alone. The interpreter or the backends read every one of them, and
none is written in the bytes as such. The *held by* column names the test that measured the derivation against the
analysis's own; its evidence is in `evidence/law-sufficiency-*.txt`.

| # | derivation | from the bytes | read by | held by |
|---|---|---|---|---|
| 1 | **the top** (`Program.top`) | the clauses whose ⟨parent⟩ is 0, in clause order | run | LS-0 test 3 |
| 2 | **children** (`Clause.children`) | the clauses whose ⟨parent⟩ is this clause's id, in clause order | run | LS-0 test 3 |
| 3 | **cost-tracked clauses** (`Clause.cost_tracked`) | the clauses named by some `(certificate ⟨C⟩ …)`; a cost counter is kept for each (SPEC §7) | run | LS-0 test 3 (plant: 8 of 9) |
| 4 | **the rules** (`Analysis.rules`) | for each rule name, its `define` clauses in clause order | run | LS-0 test 3; LS-1 E2 |
| 5 | **the overrides** (`Analysis.overrides`) | for each rule name and each of its defines d, the set of define clauses d beats: the least set closed under "d beats each clause in its `(over …)`, and whatever those beat", that is, the transitive closure | run | LS-0 test 3 (plant: 7 of 12) |
| 6 | **the claim sites** (`Analysis.claims`) | the claims in claim-id order (0, 1, …), each with the clause it stands in (section 5); the receipt lists them in that order (RUNTIME-SPEC §7) | run | LS-0 test 3 (plant: 39 of 39) |
| 7 | **a claim site's clause** (`ClaimSite.id`) | the clause the claim stands in: its own clause, or the arm's or else's ⟨C⟩ for an inline claim | run | LS-0 test 3 |
| 8 | **a variable's type** (`VarInfo.type`) | a `let`'s variable: the type of its ⟨E⟩, unpromoted; a `for`'s counter: int | run, backends | LS-0 test 3; LS-1 E3 |
| 9 | **a change's element type** (`Change.elem`) | without an index: the variable's type; with one: the variable's list element type | run | LS-0 test 3 (plant: 13 of 14); D-plant |
| 10–15 | **an expression's type** (`.type` of `Var`, `Str`, `Cat`, `Conv`, `Item`, `BoolLit`, and of every expression form, which the backends also read) | the type column of section 4's expression table; for `(var ⟨V⟩)` the variable's type (8), for `(rule ⟨str⟩)` the rule's type (17) | run (Say, Cat's parts, a conversion's and a unary operator's operand), backends | LS-0 tests 1 and 3; LS-1 E1 |
| 16 | **the variables** (`Analysis.vars`) | every variable, `let` and `for` alike, in id order, ids 0…m−1 in clause order and, within a clause, in the order the statement writes them | backends | LS-1 E3, E4 |
| 17 | **a rule's type** (`Analysis.rule_types`) | the type of its first `define`'s value ⟨E⟩ | run (through 10–15), backends | LS-1 E3 |
| 18 | **a variable's top** (`VarInfo.top`) | true exactly for a `let` that is the statement of a top-level clause (parent 0), not inline; false for every other `let` and every `for` counter | backends | LS-1 E3 (plants: 1 of 1, 143 of 143), E4 |

Two further derivations hold no field, and a reader needs both:

- **Labels.** A clause's outline number. The top-level clauses are numbered 1, 2, … in clause order, absorbed ones
  included. Each clause's children are numbered by appending `.1`, `.2`, … to its parent's number. A ⟨label⟩ in
  `given` or `agreement` names the clause whose outline number it is. (The text may spell a reference `§02`. The front
  end reads that as `2`, and the bytes hold `2`.)
- **Decimals.** ⟨mode⟩ in line 2 is the mode of the law's `(decimals …)` clause if it has one, else `fixed`. Every
  decimal literal is of that mode: `(lit fix …)` under `fixed`, `(lit float …)` under `floats`.

## 7. The order obligations

These hold in any reader, and are part of the format, not accidents of one implementation:

1. **A rule's definitions are taken in clause order.** Every proviso first, in clause order. Then the values of the
   definitions that remain, in clause order. The first refusal ends the run (SPEC §6). Which refusal a law ends in
   can depend on this order (LS-1 E2: two pairs of fixtures; the plant that reverses it changes the parsed run and not
   the decoded one).
2. **A sequence of clauses runs in clause order.** An If chain's arms are tried in written order.
3. **Ids are dense and in written order:**
   - variables, 0…m−1 (derivation 16);
   - claims, 0…k−1, in clause order and, within a clause, in the order written;
   - musts, 0…j−1, the same way.
4. **A `define`'s `(over …)` list keeps its written order.** It does not change the closure (derivation 5), but the
   round trip writes it back as written.

## 8. Well-formedness: what a reader must refuse

A reader that runs law bytes must refuse, before anything runs, every byte string that breaks one of these (ruling
D3). Each mirrors a check the front end makes, named in parentheses. A byte string that passes all of them is the
image of a typed law, as far as running it goes.

| | check |
|---|---|
| W1 | the bytes are as section 2 says: the character set, the two header lines, the clause lines numbered 1…n, a parent of 0 or an earlier clause, the final LF |
| W2 | every line parses as section 4's forms, with section 3's canonical atoms and section 1's spacing |
| W3 | **canonical**: writing what was read gives the bytes back exactly (section 9) |
| W4 | every ⟨C⟩ names an existing clause; every ⟨label⟩ is the outline number of an existing clause |
| W5 | **children only where a body is, and If chains as written** (EMPTY-BLOCK, UNEXPECTED-CHILDREN). A clause has children exactly when it is a `while`, `for` or `procedure`, or is named by some `(block ⟨C⟩)`, and then it has at least one. A `(block ⟨C⟩)` in an arm or an else names that arm's or else's own ⟨C⟩, and each clause is named by one block at most. In an If chain: the first arm's ⟨C⟩ is the If's own clause; each later arm's is an absorbed clause; the else's is the If's own clause with an inline body, or an absorbed clause. The chain's absorbed clauses come right after the If clause, as its consecutive siblings, in written order. Each absorbed clause belongs to exactly one chain |
| W6 | **places** (DEFINE-PLACE, PROCEDURE-PLACE, DECIMALS-PLACE): `define`, `procedure` and `decimals` are top-level. There is at most one `decimals`, and no decimal literal stands in a clause before it. Line 2's mode agrees with derivation "Decimals" |
| W7 | **inline**: an inline body is one of the forms section 4 marks inline |
| W8 | **variables** (UNDECLARED, LOOP-VARIABLE): ids are dense and in order (obligation 3), each declared once. Each use of ⟨V⟩ is in its scope, and it is never set, changed, appended to or removed from if it is a `for` counter |
| W9 | **types** (TYPE): every expression's type agrees with SPEC §5 for its form. See the rules below |
| W10 | **rules** (RULE-BEFORE-DEFINITION, NOTWITHSTANDING-TARGET, PRIORITY-CYCLE): every define of a name has one type, not a list. A proviso is bool. Each `(over ⟨C⟩)` names a define of the same name. The closure (derivation 5) has no clause beating itself. A `(rule ⟨str⟩)` names a rule with at least one define, and stands after the last define of that name (inside a procedure's body: the procedure's clause stands after it) |
| W11 | **procedures** (PERFORM-BEFORE-DEFINITION): `(perform ⟨C⟩)` names a `procedure` clause before the performing clause, and the performing clause is not inside that procedure's body |
| W12 | **claims** (CERTIFICATE-TARGET, AGREEMENT-TARGET, PREMISE-TARGET): a certificate's ⟨C⟩ is before the claim's clause, is not absorbed, and is not a `procedure`, `define`, `decimals` or `claim`. Agreement names two clauses before the claim's clause. Each `given` label names a clause whose statement is a `claim` |
| W13 | **ranges** (FUEL, LITERAL-RANGE): a While's ⟨n⟩ is in 1…2^62. Int and Fix ⟨n⟩ are ≤ 2^63−1. A Float literal is finite with sign bit 0. A text literal is at most 2^24 bytes of UTF-8 |

**W9's rules**, in SPEC §5's terms. "Numeric" means int, fix or float.
- `+ - * / max min`: two operands of one numeric type, which is ⟨type⟩.
- `quot`, `rem`: two int operands; ⟨type⟩ is int.
- `< > <= >=`: two operands of one numeric type; ⟨type⟩ is bool.
- `==`, `!=`: two operands of one type that is numeric, bool or text; ⟨type⟩ is bool.
- `and`, `or`: two bool operands; ⟨type⟩ is bool.
- `not`: a bool operand.
- `even`, `odd`: an int operand. `zero`, `positive`, `negative`: a numeric operand. All four have ⟨type⟩ bool.
- `neg`, `abs`, `sqrt`: a numeric operand, of the same type as ⟨type⟩.
- `trunc`: a fix or float operand; ⟨type⟩ is int.
- `as` and `rounded`: SPEC §5's table of sources and targets.
- `promote`: an int operand, with target fix or float.
- `item`: an int index into a list variable. `length`: a list variable. `list-of`: an int count, and a value whose type
  is int, fix, float or bool.
- `list`: items whose type equals ⟨list type⟩'s element, which is int, fix, float or bool.

**The statements:**
- `let`: any type.
- `set` without an index: the value's type equals the variable's. With one: an int index, a list variable, and the
  element type.
- `change`: as `set`, and the element type is numeric.
- `say`, `cat`'s parts: any type.
- Conditions of `if`, `while`, `must` and `claim`: bool.
- `for`'s bounds: int.
- `append`: a list variable, and a value of its element type.
- `remove-last`: a list variable.

Where SPEC §5 promotes an Int, the bytes hold the `(promote …)` form. A reader never promotes on its own.

**The scope of a variable (W8)**, by SPEC §5's scopes:
- A `let` in a top-level clause is visible to every later clause, and to their descendants.
- A `let` that is a clause's statement in a body is visible to the later clauses of that body, and to their
  descendants.
- A `let` inline in an arm or an else is visible nowhere else: the arm opens its own scope.
- A `for` counter is visible to the For's descendants only.
- A use inside a procedure's body sees the top-level variables declared before the procedure's clause, and the
  body's own.
- A `define`'s value and proviso see the top-level variables declared before the `define`'s clause.

**What the front end checks and this list does not:** the names. Shadowing and a name used for two things (REDECLARED)
concern the text's words. The bytes keep the names (`let`, `procedure`, `define`), but no run reads them. A reader
keeps each name as written. It does not check them, because a law whose names collide could not have come from the
front end, and its run would be the same.

**What refusing means.** A reader refuses by writing no output, no receipt and no trace, and by ending with a load
refusal: RUST-CORE-0's interface, section 10.

## 9. Exact reconstruction (the round trip)

A reader keeps every written part: names, strings, labels, the order of `(over …)` lists and of `given` labels, and
the absorbed clauses. Writing it back by sections 2–4 gives the bytes it read, byte for byte (W3).

Writing is defined by the tables. For every form, items are written in the table's order, separated by one space,
atoms canonical. Two writers that follow this document write identical bytes for one law.

**Held by:** LS-0 test 3 (290 of 290); LS-1 E1, E3 (298 of 298), for the Python decoders. A reader that cannot write
back exactly what it read has misread something, and W3 refuses it.

## 10. The run interface (RUST-CORE-0's, recorded here for the core's author)

`rust-core LAW TEXTSEAL OUT RECEIPT [TRACE] [--budget B]`

| part | meaning |
|---|---|
| `LAW` | a path to the law bytes. Refused if they fail W1–W13: nothing is written, the exit status is 3, and one stderr line reads `LAW-REFUSED W<k>: <reason>` |
| `TEXTSEAL` | 64 lowercase hex digits, printed in the receipt's `text-seal` line as given. The reader checks only its form. It is the caller's input: it is not in the law bytes, and the core never derives or validates it (the owner's ruling) |
| `OUT`, `RECEIPT`, `TRACE` | RUNTIME-SPEC §6's output, receipt and trace paths |
| `--budget B` | the host's budget of counted operations. Before each statement runs, including one in a body or inline, if `ops` > B the run stops. The receipt is not written. The trace keeps every event before the stop. The output is not written. The exit status is 4, and one stderr line reads `STOPPED-BY-HOST after <ops> counted operations (budget <B>)`. No event is emitted for the stop |

The receipt's backend line is `backend rust-core` (ruling D5). Its law seal is the SHA-256 of the bytes read,
computed by the core.

## 11. How this document is held to the code, and the code to it

- **Byte for byte.** For every one of LAW-SUFFICIENCY's 298 laws, a checker written from sections 2–4 and 8
  (`research/rust-core/format_check.py`) parses the bytes, checks W1–W13, and writes them back. Every law must pass and
  come back exactly. Planted malformations must each be refused, by the check that names them. Its evidence goes in
  `evidence/rust-core-format.txt`.
- **The derivations** are held by LAW-SUFFICIENCY's tests (section 6's *held by* column), whose decoders were written
  from `sema.py`'s writer. The checker also computes each derivation from the bytes and compares it with the
  analysis's own.
- **What it does not show.** That every law the front end can produce passes W1–W13. It shows that the 298 do. A check
  too strict for some law outside them is caught by R6's mutants only by chance. Q2 asks the re-read to look for one
  by reading.

## 12. Questions for the independent re-read

- **Q1.** SPEC §8 and RUNTIME-SPEC say numeric meaning is defined by `numeric_ref.py`. The core's author may not read
  it (D1). Are RUNTIME-SPEC §2–§3 and the vectors enough to write every numeric function, refusal order included,
  without it? Name each place they are not.
- **Q2.** Is any W check stricter than the front end, so that a law the front end accepts would be refused? Or looser,
  so that bytes no typed law has would run?
- **Q3.** Is any derivation in section 6 underdetermined by the bytes? Or is any one that a run or a backend reads
  missing?
- **Q4.** Is section 5's table of which clause a statement runs as complete? That covers events, refusals, cost
  counters and claim sites, inline and absorbed.
- **Q5.** Could two readers that follow sections 2–4 write different bytes for one law?
- **Q6.** Anything a clean-room author would have to guess.
