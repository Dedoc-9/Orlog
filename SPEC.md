# ØRLǪG OL-0 — normative specification

Status: DECLARED, 2026-10-25. Off the gate; no Verðandi authority. Where this text and the implementation disagree,
the disagreement is a finding: neither is presumed right. Numeric meaning is defined by
[`src/orlog/numeric_ref.py`](src/orlog/numeric_ref.py) (exact rationals) and by [RUNTIME-SPEC.md](RUNTIME-SPEC.md) §2–§7;
this document defines everything else.

**Read the amendments with the body.** §11 (v0.1), §12 (v0.2) and §13 (v0.3) amend §1–§10. Where they differ, the
amendment governs, and the later amendment governs the earlier.

A program is a sequence of lines of canonical text (UTF-8, LF). A run produces output bytes and a receipt. Two runs of
one law agree only if both are byte-identical.

## 1. Lines

Blank lines are ignored. Every other line is exactly one of:

- `Title: <free text>` — at most one, and before any clause. A final period is dropped from the title. It is not part
  of the law.
- `Note: <free text>` — a comment. It may appear anywhere and is not part of the law.
- `Sealed: <four proquints>.` — at most one, and the last non-blank line. It must equal the law's seal words (§9);
  otherwise the program is refused with `SEAL-MISMATCH`.
- A clause line: a label, one space, then a statement that ends with a period. An optional check suffix may follow:
  one space, then `[` + three lowercase letters + `]`.
  - Labels are `§N`, `§N.M`, … (U+00A7 followed by dot-separated decimal integers), or the same digits followed by a
    period (`3.1.`).
  - If the suffix is present, it must equal the line's check syllable (§9), computed over the line from the label up
    to and including the period. Otherwise the line is refused with `LINE-CHECK`.

Any other line is refused with `LINE-FORM`.

**Outline numbering.** The first label is `1`. Each later label must be one of:
- the next sibling of the previous label (its last part plus one);
- its first child (append `.1`);
- the next sibling of one of its ancestors.

Anything else is refused with `NUMBERING`. The label tree is the block structure: the children of a clause are the
clauses whose labels extend it by one part. Clause ids are 1, 2, … in document order.

## 2. Tokens (inside a statement, after its final period is removed)

| token | form |
|---|---|
| spaces | one or more U+0020, skipped |
| ref | `§` digits (`.` digits)* , e.g. `§3.1` (a clause reference) |
| num | `[0-9]+(\.[0-9]+)?` |
| str | `"` … `"`, where `""` inside stands for one `"`; no line break |
| word | `[A-Za-z][A-Za-z0-9_]*` |
| op | `<=` `>=` `!=` `-` `+` `*` `/` `(` `)` `,` `;` `:` `<` `>` `=` `'` |

**Case.** Keywords match case-insensitively; identifiers are case-sensitive.

**Reserved words.** These cannot be identifiers:

```
let be set to say if then otherwise unless while at most least times do the following for each from perform it must
hold that we claim by given define as provided notwithstanding append remove last item of length list copies is not
and or plus minus divided quotient remainder modulo equals equal less greater than even odd zero positive negative
true false sum product larger smaller absolute value square root integer part float fixed rounded followed this law
seal computation theorem owner certificate agreement decimals are floats negation increase decrease
```

Not reserved: `a`, `an`, `under`, `case`.

## 3. Statements (one per clause; the first word decides)

`E` is an expression, `C` an expression of type Bool, `X` an identifier, and `§k` a ref.

| form | notes |
|---|---|
| `Let X be E` | declares X with E's type |
| `Set X to E` · `Set item E of X to E` | X declared; types per §5 |
| `Increase X by E` · `Decrease X by E` (also `item E of X`) | numeric |
| `Say E` | output one line |
| `If C, [then] S[; otherwise[,] S]` | S is an inline statement (below) |
| `If C, [then] do the following` | block = children |
| `Unless C, S` · `Unless C, do the following` | as If with `not C` |
| `Otherwise, S` · `Otherwise, do the following` | attaches to the immediately preceding sibling If/Unless chain without an otherwise yet, else `ORPHAN-OTHERWISE` |
| `Otherwise, if C, [then] S` · `… do the following` | an else-if arm, same attachment rule |
| `While C, at most N times, do the following` | N an integer literal, 1 ≤ N ≤ 2^62 |
| `For each X from E to E, do the following` | Int bounds, inclusive; the bounds are `sum`-level expressions (§4) |
| `To <words>, do the following` | a procedure, top level only; its name is its words, lowercased and space-joined; a name may not begin with a statement word |
| `Perform <name>` or the name alone as a statement | calls the procedure |
| `It must hold that C` | a guard |
| `We claim that C[, by O][, given §a[, §b…][ and §c]]` | a claim; O as below, default `computation` |
| `[Notwithstanding §a[, §b][ and §c], ]define X as E[, provided that C][, unless C]` | a rule (§6), top level only |
| `Append E to X` · `Remove the last item of X` | lists |
| `Decimals are fixed` · `Decimals are floats` | at most once, top level, before any decimal literal |

- **Inline statements** (S) are Let, Set, Increase, Decrease, Say, Append, Remove, Perform (or a bare procedure name),
  the must form and the claim form.
- **Oracles** (O):
  - `computation`;
  - `the theorem "<name>"`;
  - `the owner`;
  - `the certificate of §k[ under the theorem "<name>"]`;
  - `agreement of §a and §b`.
- **Blocks.** A clause whose statement says `do the following` (and a While, For or To clause) must have children,
  else `EMPTY-BLOCK`. Any other clause must have none, else `UNEXPECTED-CHILDREN`. Otherwise clauses that are
  absorbed into an If chain are not separate statements.

## 4. Expressions (lowest precedence first)

```
expr    := or
or      := and ("or" and)*
and     := not ("and" not)*
not     := "not" not | "it is not the case that" not | cmp
cmp     := cat [ ("<="|">="|"!="|"<"|">"|"=") cat | "equals" cat | is-tail ]
is-tail := "is" ["not"] ("even"|"odd"|"zero"|"positive"|"negative")
         | "is" ["not"] ("less than"|"greater than"|"at least"|"at most"|["equal to"]) cat
cat     := sum ("followed by" sum)*
sum     := term (("plus"|"+"|"minus"|"-") term)*
term    := unary (("times"|"*"|"divided by"|"/"|"modulo") unary)*
unary   := "-" unary | postfix
postfix := atom ("as an integer"|"as a fixed"|"as a float"|"rounded to an integer"|"rounded to a fixed"
                 |"rounded to a float")*
atom    := num | str | "true" | "false" | "(" expr ")" | "this law's seal" | "item" unary "of" X
         | "a list of" sum "copies of" unary | "the" phrase | ["the"] X
phrase  := "sum of" sum "and" sum | "product of" sum "and" sum | "quotient of" sum "by" sum
         | "remainder of" sum "by" sum | "larger of" sum "and" sum | "smaller of" sum "and" sum
         | "absolute value of" unary | "square root of" unary | "integer part of" unary | "negation of" unary
         | "length of" X | "list" sum (("," sum)* ["and" sum])
```

- **Negated comparisons.** `is not less than` (and its kin) means `not (a < b)`, which differs from `a >= b` for a
  NaN.
- **Binary operators** are left-associative.
- **`the`.** It is a filler before an identifier only when the next word is not reserved.
- **List literals.** In a list literal, `,` and `and` continue the list only when the next token can begin an
  expression.

## 5. Types and static semantics

**Types.** Int (i64), Fix (Q31.32), Float (binary64), Bool, Text (UTF-8 bytes), and List of Int / Fix / Float / Bool.
The types come from these rules:

- **Literals.** An integer literal is Int (above 2^63−1 is `LITERAL-RANGE`). A decimal literal is Fix by default and
  Float after `Decimals are floats`.
  - Fix stores the nearest raw value, ties to even. Float stores the nearest binary64, ties to even.
  - An inexact literal is recorded as a LITERAL-ROUNDED note. That is a compile note; it is not in the law.
- **Promotion.** An Int is promoted (a counted operation, §7) wherever it meets Fix or Float:
  - as one operand of `+ - * / max min`, a comparison, `=` or `!=`;
  - as a value stored into a Fix or Float variable, list item or append;
  - as a list-literal item when the list's type is Fix or Float.
- **Operators.** Fix with Float is never mixed (`TYPE`). `quotient` and `remainder`/`modulo` take Int only. `even`
  and `odd` take Int only. `zero`, `positive`, `negative`, `neg`, `abs` and `sqrt` take any number. `integer part of`
  takes Fix or Float and yields Int.
- **Equality.** `=`/`!=` also compare Bool with Bool and Text with Text.
- **Concatenation.** `followed by` takes anything and yields Text.
- **Conversions:**

  | | as | rounded to |
  |---|---|---|
  | to an integer | from Fix or Float | from Fix or Float |
  | to a fixed | from Int or Float | from Int or Float |
  | to a float | from Int or Fix | from Int or Fix |

**Scopes:**
- Each block (and each inline arm) opens a scope. A For opens a scope holding its counter, which is read-only
  (`LOOP-VARIABLE`).
- Declaring a name that is visible in any enclosing scope, or that names a rule or a procedure, is `REDECLARED`.
  Shadowing is refused.
- A procedure body sees the top-level variables declared textually before the procedure, plus its own locals.
- A procedure may perform only procedures whose definitions it follows (no recursion, direct or mutual):
  `PERFORM-BEFORE-DEFINITION` or `UNKNOWN-PROCEDURE`.

**Rules:**
- A rule name may be used only textually after all of its Define clauses (inside a procedure: before the procedure's
  definition), else `RULE-BEFORE-DEFINITION`.
- All Define clauses of a name have one type, which is not a list.

**Ids.** Variables are numbered 0, 1, … in textual order of declaration (Let, For counter), including inside
procedure bodies. Claims are numbered 0, 1, … and musts 0, 1, … the same way.

**Other compile refusals:**
- `UNDECLARED`;
- `TYPE`;
- `FUEL` (a While bound outside 1…2^62);
- `PRIORITY-CYCLE` (the notwithstanding relation of one rule name has a cycle);
- `NOTWITHSTANDING-TARGET` (a ref that is not a Define of the same name);
- `CERTIFICATE-TARGET` (a certificate ref that is not an earlier, executed, non-procedure, non-define,
  non-claim clause);
- `AGREEMENT-TARGET`;
- `PREMISE-TARGET` (a premise that is not a claim clause);
- `UNKNOWN-CLAUSE`;
- `DECIMALS-PLACE`;
- `DEFINE-PLACE`;
- `PROCEDURE-PLACE`.

## 6. Rules (defeasible definitions)

A use of rule name R evaluates as follows, left to right, in clause order:
1. Count one operation.
2. For each Define of R, evaluate its proviso if it has one. The Define is *applicable* if it has no proviso or its
   proviso is true. Every proviso is evaluated; there is no short-circuit across Defines.
3. Remove every applicable Define that another applicable Define overrides. *Overrides* is the transitive closure of
   `notwithstanding`.
4. If none remain, refuse `RULE-UNDEFINED`.
5. Evaluate the values of the remaining Defines, in clause order, all of them before any comparison.
6. If any later value is not equal to the first (`==` on its type, so Float NaN ≠ NaN), refuse `RULE-CONFLICT`.
   Otherwise the result is the first value.

A refusal inside a rule names the clause of the statement that used the rule.

## 7. Dynamic semantics

**State.** A run holds:
- `ops` (u64, starting at 0);
- the variables (by id);
- the event chain head;
- the event count;
- the output bytes;
- the claim accumulators (one per claim id: evaluations, trues, cost, ref clause, ref cost);
- one cost counter per clause named by a certificate.

**Evaluation.** Expressions are pure and evaluate left to right, depth first. Every refusal names the clause whose
statement is executing (§6 for rules).

**Operation counting.** Add 1 to `ops` immediately before each of the following:
- every arithmetic operator, quotient, remainder, negation, absolute value, square root, larger, smaller,
  integer part;
- every conversion, including each implicit promotion;
- every comparison and predicate (`even`, `zero`, …);
- every `not`;
- every `and`/`or`, counted after its left operand, whether or not the right operand is evaluated;
- every `item … of` (after its index);
- every `length of`;
- every list construction (after its operands);
- every rule use (§6).

A concatenation of k parts adds k−1 after all its parts are evaluated. Literals, variable reads and
`this law's seal` count 0.

**Statements:**

| statement | order |
|---|---|
| Let, Set X | +1; evaluate; store (lists are copied: values, not references); event A |
| Set item | +1; index; value; bounds check (`INDEX-OUT-OF-RANGE` unless 1 ≤ k ≤ length); store; event E |
| Increase/Decrease X | +1; evaluate E; +1; add or subtract with the variable's checked rule; store; event A |
| Increase item | +1; index; +1; read the item (bounds); evaluate E; +1; add/subtract; store; event E |
| Say | +1; evaluate; the line is the value (Text as is, else printed per RUNTIME-SPEC §3); `TEXT-TOO-LONG` if it exceeds 2^24 bytes; the line plus LF is appended to the output (`OUTPUT-TOO-LONG` beyond 2^30 bytes total); event S |
| If chain | for each arm in order: +1; evaluate its condition; on true run its body and stop; if no arm ran, run the otherwise body (no count for the otherwise itself) |
| While | n = 0; repeat: +1; evaluate C; stop if false; if n = N refuse `FUEL-EXHAUSTED`; n += 1; run the body |
| For | +1; evaluate lo, then hi; k = lo; while k ≤ hi: +1; store k in the counter (event A); run the body; stop if k = hi; k += 1 |
| Perform | +1; run the body |
| must | +1; evaluate; event M; refuse `MUST-FAILED` if false |
| claim | +1; s = ops; evaluate C; cost = ops − s; event C; accumulate (evaluations+1, trues+result, cost+=cost, ref clause and ref cost = the certificate clause's id and its cost counter now, or 0 and 0); refuse `CLAIM-REFUTED` if false |
| Append | +1; evaluate; `LIST-TOO-LONG` beyond 2^24; push; event P |
| Remove the last item | +1; `EMPTY-LIST` if empty; pop; event Q (with the new length) |
| Define, To, Decimals | nothing at run time |

**Cost counters.** For a clause named by a certificate, `start = ops` before the statement (before its own +1);
afterwards its counter grows by `ops − start`.

**Text.** The text of `this law's seal` is the seal words (§9). Concatenation evaluates every part, then appends them
in order, refusing `TEXT-TOO-LONG` at the append that would exceed 2^24 bytes. Numbers print per RUNTIME-SPEC §3; Bool
prints `true`/`false`; a List prints `[a, b, c]`.

**Events and the receipt.** RUNTIME-SPEC §5 and §7, with the law-seal as given.
- A **refusal** emits event R (the code), then stops. The receipt says `status REFUSED <CODE> <clause id>`.
- **Completion** says `status COMPLETED`.
- **Event payload variable numbers** are the variable ids of §5.
- **Event payloads for list assignments** encode the whole list.

## 8. Numbers

RUNTIME-SPEC §2 and numeric_ref.py, with the order of refusal tests stated there. Integer `divided by` is exact
division, refused with `INEXACT-DIVISION` when it is not exact. `quotient` and `remainder`/`modulo` are Euclidean:
a = b·q + r with 0 ≤ r < |b|.

`as an integer`:
- **from Fix:** `INEXACT-CONVERSION` unless the fraction bits are zero, then truncation;
- **from Float:** `NOT-FINITE` for NaN or ±∞; `INEXACT-CONVERSION` if not integral; `OVERFLOW` outside i64.

`rounded to an integer` is half-even. `integer part of` truncates toward zero.

The square root of an Int is ⌊√n⌋; of a Fix it is isqrt(raw · 2^32); of a Float it is IEEE's (NaN for a negative).

## 9. Identity

- **text-seal:** sha256 of the canonical text.
- **law-seal:** sha256 of the law's bytes, which `src/orlog/sema.py` (`law_bytes`) defines.
  - The law is `orlog-law 0`, the decimals mode, then one line per clause in id order, with resolved typed literal
    values, variable ids and clause ids.
  - Titles, notes, labels' spelling, check suffixes and the seal line are not in the law.
- **Seal words:** the first 64 bits of the law-seal as four proquints (consonants `bdfghjklmnprstvz`, vowels `aiou`,
  pattern CVCVC per 16 bits, big-endian, joined by `-`).
- **Check syllable:** fold the line's UTF-8 bytes with acc ← 2·acc ⊕ byte in GF(2^8) (polynomial 0x11B), starting
  from 0. Render acc as consonant[acc >> 4] + vowel[(acc >> 2) & 3] + `nrsl`[acc & 3].

## 11. Amendments v0.1 (2026-10-25), settling the clean-room twin's 62 notes

The clean-room twin (`twin/NOTES.md`), written from this specification alone, named 62 places where a literal reader
could go two ways. Each is settled below. The number is the twin's. "Code changed" marks where the implementation was
changed to meet the reading, rather than the reading chosen to meet the implementation.

**General**
- **G1.** Runs agree when their output bytes and their receipts, minus the `backend` line, are byte-identical. Runs
  of different texts of one law also differ in `text-seal`.
- **G2.** A compile refusal writes no receipt. The arbiter's witness records its code, line and message; the
  command line exits 1.
- **G3.** Compile refusals are reported phase by phase. The first refusal in the first phase that has one is
  reported:
  1. the door, in byte order;
  2. lines, in order: LINE-FORM, TITLE-PLACE, SEAL-FORM, SEAL-PLACE, LINE-CHECK, NUMBERING;
  3. statement syntax, in clause order: SYNTAX, LEX, PROCEDURE-NAME, UNKNOWN-PROCEDURE;
  4. block shape and Otherwise attachment, in tree order: ORPHAN-OTHERWISE, EMPTY-BLOCK, UNEXPECTED-CHILDREN;
  5. DEFINE-PLACE, over all clauses;
  6. static semantics, in document walk order;
  7. PRIORITY-CYCLE;
  8. SEAL-MISMATCH.
- **G4.** Every count falls after the operation's operands are evaluated, immediately before the operation. A rule
  use is the exception: it counts first.

**§1 Lines**
- **1.** A blank line is empty or spaces only.
- **2.** The prefixes `Title:` and `Note:` are case-sensitive; any text may follow. `Sealed: ` is exact.
- **3.** A second Title, or a Title after content, is TITLE-PLACE.
- **4.** A Note may follow the Sealed line, because Notes are not law. Any other line after it is SEAL-PLACE.
- **5.** A Sealed line that is not four `-`-joined proquints is SEAL-FORM. A well-formed one that differs from the
  seal words is SEAL-MISMATCH.
- **6.** Label parts are compared as integers. `§1.` is LINE-FORM.
- **7.** Exactly one space follows the label. Code changed.
- **8.** A malformed statement is SYNTAX; an unreadable token is LEX. Both are added to §5's list.
- **9.** The two label forms may be mixed.

**§2 Tokens**
- **10.** Longest match; no separator is required.
- **11.** `:` begins nothing, so it is SYNTAX.
- **12.** Reserved words are reserved case-insensitively.
- **13.** `this law's seal` is a fixed five-token sequence; `s` is an ordinary identifier elsewhere.
- **14.** A CR cannot reach a statement, because the door has removed it.

**§3 Statements**
- **15.** Unless counts its `not`.
- **16.** Unless takes no `then` and no inline otherwise. An Otherwise clause after it attaches.
- **17.** An else-if arm takes no inline otherwise.
- **18.** An absorbed arm's condition, inline statement and events carry its own clause id.
- **19.** A While bound must be an integer literal; a decimal one is SYNTAX. A bound outside 1…2^62 is FUEL.
- **20 and 21.** A procedure's name may not begin with any reserved word (PROCEDURE-NAME). Code changed.
- **22.** Performing a procedure before its definition is PERFORM-BEFORE-DEFINITION, wherever it occurs.
- **23.** `notwithstanding` and `given` take one or more references: `§a(, §b)*( and §c)?`.
- **24.** A Define's `unless C` counts its `not`.
- **25.** A Define has at most one proviso: `provided that` or `unless`. Both together is SYNTAX.
- **26.** An optional `the` may precede any identifier position, when the next word is not reserved.
- **27.** In statements, `item U of X` takes a unary `U`, as the atom does. Parenthesize anything larger.
- **28.** A form that is not inline, written inside an inline arm, is SYNTAX.
- **29.** Setting, increasing or decreasing a For counter, item forms included, is LOOP-VARIABLE. This is checked
  before the list type.

**§3 and §5: oracles and their targets**
- **30.** A certificate target has a smaller clause id than the claim. It is not a To, Define, Decimals or claim
  clause, and not absorbed. Clauses inside procedure bodies are allowed; their counters grow each run.
- **31.** Agreement targets are earlier clauses. Ref clause and ref cost are 0 0.
- **32.** A premise is a clause whose own statement is a claim. It may be later than the claim, or the claim itself.
- **33.** A reference to no clause is UNKNOWN-CLAUSE, everywhere.

**§4 Expressions**
- **34.** Inside a list literal, `,` and `and` continue the list only before one of: a number; a text; `(`; `-`; a
  word that is not reserved; or `the`, `item`, `true`, `false`, `this`.
- **35.** `and` and `or` short-circuit.
- **36.** Unary minus is a counted negation, even on a literal.
- **37.** `is not E` (equality) is the single comparison `!=`: one operation. `is not <predicate>` and
  `is not less than`, `is not greater than`, `is not at least` and `is not at most` are a `not` around the inner
  test: two operations. This is the one reading that changed the twin's receipts. With it, the twin matches the
  reference on all 23 programs.

**§5 Types and static semantics**
- **38.** A decimal literal outside its range is LITERAL-RANGE: a Fix raw value outside i64, or a Float that rounds
  to infinity. Code changed: the compiler used to crash with CPython's OverflowError.
- **39.** List literal types:
  - Int with Fix makes Fix; Int with Float makes Float;
  - Bool goes only with Bool;
  - Fix with Float is TYPE;
  - a Text or list item is TYPE.
- **40.** An Int promoted to Float is converted exactly; otherwise INEXACT-CONVERSION.
- **41 and 42.** A promotion is counted right after its own operand or list item.
- **43.** Identity conversions, and `integer part of` an Int, are TYPE.
- **44.** `length of` applies to lists only.
- **45.** All Defines of one name have exactly one type, with no promotion between them.
- **46.** A Define's expressions see the top-level variables declared textually before it, and the rules completely
  defined before it.
- **47.** A variable may not take the name of any rule (rules are collected first, wherever they are defined). It
  may not take the lowercased name of a procedure already defined.
- **48.** Writing to a rule name is UNDECLARED, because it is not a variable.
- **49.** DECIMALS-PLACE covers all three faults.
- **50.** `zero`, `positive` and `negative` are IEEE comparisons with zero. So −0.0 is zero, and NaN is none of the
  three.

**§6 Rules**
- **51.** Priority is the static transitive closure.
- **52.** The comparisons behind RULE-CONFLICT are not counted.

**§7 Dynamic semantics**
- **53.** Event E carries the 1-based index k.
- **54.** Event E's value encoding includes its tag byte.
- **55.** Increase's promotion is counted inside "evaluate E".
- **56.** A claim never evaluated has ref clause and ref cost 0 0.
- **57.** Every receipt line, `end` included, ends with LF.
- **58.** A cost counter does not grow on a refusal. This is unobservable.

**RUNTIME-SPEC and numeric_ref**
- **59.** `as an integer` is defined in §8, and as `x_as_i`/`f_as_i` in numeric_ref.
- **60.** The square root of a negative Int or Fix is NEGATIVE-SQRT.

**§9 and §10**
- **61 and 62.** Noted. The law's bytes are defined by `sema.py`.

## 12. Amendments v0.2 (2026-10-25), from the engineering red team (court/redteam-eng/FINDINGS.md)

**New compile refusals.** Each is a deliberate bound sized to the hosts' limits (E23 asked that they be listed here):
- **NESTING-DEPTH:** clause labels have more than 24 parts.
- **LOOP-NESTING:** more than 16 While or For loops nest within one body; a procedure body starts again at 0.
- **EXPRESSION-DEPTH:** more than 24 nested parentheses, unary minuses, `not`s or phrases, or an expression tree
  deeper than 64.
- **QUOTE-BOUNDARY:** the door refuses a line where repairing a typographic quote would move a literal's boundary.

**The door:**
- A literal opened by a straight `"` closes only at a straight `"`; typographic quotes inside it are its text (E9).
- A literal opened by a typographic quote closes at U+201C, U+201D, U+201F or a straight `"`.
- U+2033 is not a quote.
- In code, any non-ASCII character outside the explicit typographic table is refused before any normalization (E17).
  NFC applies to free text only.
- Inside literals and free text, these are refused:
  - format characters (category Cf) other than ZWJ and ZWNJ;
  - Hangul fillers;
  - line and paragraph separators (E19).
- LITERAL-NOT-NFC is noted for literals only (E26).

**Labels and procedures:**
- A reference `§02` names `§2`: references and the label table use integer parts, so label spelling never reaches the
  law (E20).
- Procedures are collected from top-level clauses by the lexer, so spacing inside `, do the following` does not matter
  (E16).
- A nested `To` clause is parsed and refused PROCEDURE-PLACE.

**The arbiter:**
- Agreement is byte equality of receipts with the second line, and only that line, removed. That line must read
  `backend <name>`, and every line must end with LF (E7).
- The dissent kind is read over the backends that built. A failed build is reported in `build_failed` and never
  counted as a dissent (E8).
- Compilers and programs see relative ASCII paths, with their working directory set (E11).

## 13. Amendments v0.3 (2026-10-25), settling the twin's second round (twin/probes/EXPECTED.md)

The twin's author wrote 163 probes by hand from v0.1, each with its expected result, and named the points where v0.1
still left a reader two ways. The reference met 155 of them as first run. Each difference and each open point is
settled below. "Code changed" marks a reading the implementation was changed to meet; "against the twin" marks the
two readings settled the other way, recorded probe by probe in `twin/probes/settled.json` (the twin's own
`expected.json` is left as its author wrote it). After these changes the reference meets 161 probes and the two
settled ones (`python tests/compare_probes.py`).

**Precedence.** §11, §12 and this section amend the body. Where they differ from it, the amendment governs, and a
later amendment governs an earlier one. (The twin found the body still stating rules §11 had replaced.)

**G3, completed.** Every compile refusal belongs to exactly one phase. The first refusal in the first phase that has
one is reported, and within a phase the order is the one given here.

| phase | order within the phase | codes |
|---|---|---|
| 1. the door | `BYTES-NOT-UTF8` for the whole text first; then line by line: within a line, the characters by column, then `UNTERMINATED-TEXT`, then `QUOTE-BOUNDARY` | `BYTES-NOT-UTF8` `BIDI-CONTROL` `CONTROL-CHAR` `INVISIBLE-CHAR` `DASH-AMBIGUOUS` `NON-ASCII-CODE` `UNTERMINATED-TEXT` `QUOTE-BOUNDARY` |
| 2. lines | line by line; within a line, in the order listed | `LINE-FORM` `TITLE-PLACE` `SEAL-FORM` `SEAL-PLACE` `LINE-CHECK` `NESTING-DEPTH` `NUMBERING` |
| 3. statements | clause by clause; within a clause: `LEX`, the statement being read into tokens whole before it is parsed; then the parse, which meets `SYNTAX` or `EXPRESSION-DEPTH` reading left to right, the tree's depth checked after it; then `PROCEDURE-NAME`; then `UNKNOWN-PROCEDURE` | `LEX` `SYNTAX` `EXPRESSION-DEPTH` `PROCEDURE-NAME` `UNKNOWN-PROCEDURE` |
| 4. shape | depth-first pre-order (document order); within a clause, in the order listed | `ORPHAN-OTHERWISE` `EMPTY-BLOCK` `UNEXPECTED-CHILDREN` |
| 5. Define placement | every clause, in document order | `DEFINE-PLACE` |
| 6. static semantics | document walk order (below) | `TYPE` `UNDECLARED` `REDECLARED` `LOOP-VARIABLE` `LOOP-NESTING` `FUEL` `PROCEDURE-PLACE` `PERFORM-BEFORE-DEFINITION` `RULE-BEFORE-DEFINITION` `DECIMALS-PLACE` `LITERAL-RANGE` `UNKNOWN-CLAUSE` `CERTIFICATE-TARGET` `AGREEMENT-TARGET` `PREMISE-TARGET` `NOTWITHSTANDING-TARGET` |
| 7. priority | the static transitive closure (item 51) | `PRIORITY-CYCLE` |
| 8. the seal | the Sealed line against the law's seal words | `SEAL-MISMATCH` |
| none | an invariant of the implementation failed: a defect, never a verdict on the text | `INTERNAL` |

The self-test holds this table to the code: the set of codes it lists equals the set the front end can raise.

**Phase 1, the door.**
- **Its codes.** The door's refusals had no codes in v0.1 (the twin's open point); they are listed above.
- **Unterminated text, against the twin.** A literal not closed on its line is refused `UNTERMINATED-TEXT` by the
  door, not `LEX`. The door must know every literal's boundary before it repairs anything outside literals (T6), and
  such a line has none. Items 1 and 14 have no probe because the door delivers canonical text.

**Phase 2, lines.**
- **One pass (the twin's reading (a)).** The listed codes order the checks of one line; the first faulty line
  decides. So a `LINE-CHECK` on line 1 comes before a `LINE-FORM` on line 9.
- **`Sealed:x`.** Only the exact prefix `Sealed: `, its space included, opens a Sealed line. `Sealed:x` is
  `LINE-FORM`, as `sealed: x` is (items 2 and 5). Code changed.
- **A malformed line after the Sealed line is `LINE-FORM`, not `SEAL-PLACE`,** because `LINE-FORM` is checked first
  in a line. For the same reason a second Sealed line that is malformed is `SEAL-FORM`. Code changed.
- **Content (item 3).** A Note is not content. The Sealed line is: a Title after it is `TITLE-PLACE`. Code changed.
- **A clause line ends with a period (§1).** A clause line without one is `LINE-FORM` here. It used to be
  `STATEMENT-PERIOD` in phase 3, a code no table listed. Code changed.
- **Placement.** `NESTING-DEPTH` (§12) is checked after `LINE-CHECK` and before `NUMBERING`.

**Phase 3, statements.**
- **LEX before SYNTAX within a clause, against the twin.** A statement is read into tokens whole before it is
  parsed. The first character that begins no token is fixed by the lexical grammar alone (longest match). The
  twin's "first offending position" would make the code depend on where a parse fails, and that needs a property of
  the parser (detecting each error at the earliest token, the correct-prefix property), which nobody has shown for
  the reference. Across clauses, clause order still decides: a `SYNTAX` in clause 1 comes before a `LEX` in clause 2.
- **SYNTAX before the procedure checks within a clause.** `PROCEDURE-NAME` and `UNKNOWN-PROCEDURE` are reported only
  once the whole clause has parsed. So `Perform fly away 1.` is `SYNTAX`. Code changed: both used to be raised while
  parsing.
- **The name alone calls the procedure.** A statement whose first word is not reserved is a call, and its words to
  the end (or to a `;` in an inline arm) are the name. A name no `To` clause defines is `UNKNOWN-PROCEDURE`. So
  `Fly away.` with no procedure named `fly away` is `UNKNOWN-PROCEDURE`; it used to be `SYNTAX` ("no statement
  begins with"). A call that holds anything but words, such as `Fly 1.`, is `SYNTAX`. Code changed.
- **A call cannot begin with a reserved word (items 20 and 21).** No procedure can have such a name, so the call is
  `SYNTAX`: `Perform the go.` and `If true, do the following; otherwise say 2.` both are. The optional `the` of item
  26 belongs to identifiers, not to procedure names. Code changed for `Perform the go.`, which was
  `UNKNOWN-PROCEDURE`.
- **Empty names.** A `To` with no name, and a `Perform` with nothing after it, are `SYNTAX`. They used to be
  `PROCEDURE-NAME` and `UNKNOWN-PROCEDURE`. Code changed.
- **What the parse settles, and what it does not.** Within a statement, `SYNTAX` and the nesting part of
  `EXPRESSION-DEPTH` are met in the order of a left-to-right predictive reading of §4, with the lookahead of items
  26 and 34. That this order is independent of how a parser is written holds for predictive parsers of this grammar;
  that the reference parser is one is DECLARED, not shown.

- **EXPRESSION-DEPTH, stated exactly (a correction of §12's wording, measured against the code).** On the path from
  a statement to each atom, count the atoms (a number, a text, a name, a parenthesized expression, a phrase), the
  unary minuses and the `not`s, the atom itself included. A count over 24 is refused. So `Say 1.` counts 1, and 23
  nested parentheses around a name pass while 24 are refused (§12 said "more than 24 nested parentheses"). The
  statement's tree, the statement node counted as level 1, may be at most 64 deep: `Say` with 63 terms joined by
  `plus` passes, with 64 it is refused.

**Phase 4, shape.** "Tree order" is depth-first pre-order, which is document order (the twin's reading, probe
`g3-shape-preorder`).

**Phase 6, static semantics.**
- **Document walk order.** Top-level clauses are walked in document order. A block is walked when its clause is
  reached, and a procedure's body when its `To` clause is reached. An absorbed Otherwise arm is walked with the
  clause that absorbed it.
- **Within a statement: written order, post-order.** A statement's parts are checked in the order they are written,
  each part completely before the next. Within an expression, the operands are checked in written order and then the
  operator's own check (post-order, as G4 counts at run time). Three refinements:
  1. A name the statement declares (a Let's variable, a For's counter) is checked after the statement's
     expressions. So in `Let x be y`, with `x` declared and `y` not, the code is `UNDECLARED` (the twin's reading).
  2. A requirement on one part is checked when that part is reached: an index is an Int, a target is a list, a
     counter is not set (item 29: before the list type), a number is what is increased.
  3. A relation between two parts is checked at the later part: a value fits where it is stored, and every Define of
     a name has one type.

  So:
  - `item I of X` checks I, then X.
  - `Set item I of X to E` and `Increase item I of X by E` check I, then X, then E.
  - `Append E to X` checks E, then X, then whether E fits X.
  - `While C, at most N times` checks C, then N (`FUEL`).
  - `For each i from A to B` checks A, then B, then the counter i.
  - A Define checks its Notwithstanding references, then its name, then its value, then its proviso.
  - A `To` checks its place (`PROCEDURE-PLACE`), then its name (`REDECLARED`), then its body.
  - A claim checks its condition, then its oracle's targets, then its premises.
  - `and`, `or`, `quotient` and `remainder` type both operands before their own check.

  Code changed in the reference, which used to: check a target before its index or its value; check a Define's
  references last; and stop typing `and`, `or`, `quotient` and `remainder` at the first operand of the wrong type.
  The differential run found these (below). No accepted program changes: only which of two faults is reported.
- **LITERAL-RANGE** is static semantics (phase 6), not a reading of tokens (the twin's reading).
- **Item 29, Append and Remove on a For counter, are `TYPE`.** A counter is an Int, not a list. `LOOP-VARIABLE`
  covers Set, Increase and Decrease.
- **Item 47 both ways, and rules.** One name may not stand for a variable and a procedure, or for a rule and a
  procedure, whichever comes first. A procedure's name is compared with an identifier lowercased, since procedure
  names are lowercased words. Code changed: the reference had refused none of these.
  - A variable may not take the lowercased name of a procedure already defined (item 47). The reference compared
    without lowercasing.
  - A procedure may not take the lowercased name of a visible variable (the converse, by §5's rule).
  - A procedure may not take the lowercased name of any rule. Rules are collected first, wherever they stand.
  - A Define may not take the name of any procedure. Procedure names are collected first by the lexer (§12).
  - A procedure is defined when its body ends. So inside its own body its name is not yet taken, and the body can
    neither call it (`PERFORM-BEFORE-DEFINITION`) nor be refused a local of that name.
- **Item 48, reads.** A rule name used where a list variable is needed, as in `item 1 of r` or `length of r`, is
  `UNDECLARED`: `r` is not a variable. This holds for reads as for writes (the twin's reading).

**The twin's notes, kept as they are.**
- **Item 31.** Agreement targets may be any earlier clause. The agreement channel is never admissible for grounding
  (the court's rule), so its targets record a claim's basis and never decide a standing. No change.
- **Items 53 and 54.** The trace head depends on the law seal. `probe_run.py --seals` reruns the twin with the
  reference's seals.

**Found while settling: the door's events.** A line already refused for another character is no longer compared
for `QUOTE-BOUNDARY`. Its refused characters are missing from the repaired line, so its literals differed with no
quote involved, and the event said what had not happened (E19's line carried a false `QUOTE-BOUNDARY` after its
real refusals). The set of accepted texts and their canonical forms cannot change: a refused line refuses the text.
The red team's door fuzz, rerun after the change, finds 0 counterexamples in 60,000 lines (seed 5, MEASURED).
Code changed.

**The differential run.** `tests/diff_twin.py`. (This line first read "results below", and no results followed: the
twin's third round found it. The results are in §14.)

## 14. Amendments v0.4 (2026-10-25), settling the twin's third round (twin/probes3/EXPECTED.md)

The twin's author updated the twin to §12 and §13, reading nothing but this specification, RUNTIME-SPEC.md and the
two shared modules, and wrote 128 new probes by hand. The reference met 124 of them as first run. The twin named
twelve places where it found §12 and §13 undecided, and the four differences were all among them. Each is settled
below. The three readings settled against the twin are in `twin/probes3/settled.json`. After these, the reference
meets 125 probes as worked and 3 as settled (`python tests/compare_probes.py --dir probes3`).

1. **Only a top-level To defines a procedure** (§12). A nested To defines nothing: it is refused PROCEDURE-PLACE in
   phase 6. So a call to its name is UNKNOWN-PROCEDURE (phase 3), and a Define of its name is not REDECLARED by it.
   §13's "no To clause defines" means no top-level one. (The twin's reading, already the reference's.)
2. **A To that does not parse defines nothing.** A top-level clause defines a procedure only when its statement is a
   well-formed To. (The twin's reading, already the reference's.)
3. **Every atom counts toward EXPRESSION-DEPTH**: every form of §4's atom, including `true`, `false`,
   `this law's seal`, `item … of` and `a list of … copies of`, and not only §13's five examples. (The twin's reading,
   already the reference's.)
4. **Only a written not counts**, that is `not` and `it is not the case that`. The not inside `is not <test>`, an
   Unless's not and a Define's `unless` are counted operations at run time, but they add nothing to the nesting
   count. (The twin's reading, already the reference's.)
5. **The count, defined once.** The nesting count at a position is the number of atom positions, unary minuses and
   written nots that the left-to-right parse is inside when it reaches that position, the position itself
   included. This is the "path" §13 meant. On the left operand of `is not even` the two descriptions now agree,
   because the implicit not is not counted (item 4). (The twin's reading, already the reference's.)
6. **The count rises on entering an atom position**, before what stands there is read. So twenty-four `(` followed
   by `)` is EXPRESSION-DEPTH, not SYNTAX. Against the twin: the bound guards the parser's own recursion, so it must
   hold before the parser goes deeper.
7. **The statement's tree is the parse tree** (the nodes of `src/orlog/syntax.py`, once the statement has parsed).
   This is against the twin on parentheses only. In that tree:
   - parentheses group and make no node;
   - `a followed by b followed by c` is one node over its parts;
   - `is not <test>` (`is not less than` and its kin) is a not node over the test, and so is a Define's `unless C`.
     An Unless statement's not is added after the check, so it is not in the tree;
   - an inline statement is a child of its clause's statement;
   - conversions are nodes;
   - the X of `item I of X` and `length of X` is part of its node, not a child.

   The 64-level bound protects the stages that walk this tree (checking, lowering, generating), and none of them
   recurses on parentheses.
8. **A loop's place first.** A While or a For checks LOOP-NESTING before its own parts, as a To checks its place
   before its name. Code changed: the twin's reading.
9. **Which checks belong to a part.** A requirement belongs to a part when the statement or phrase names that part's
   type: an index, a count (`a list of N copies of V`), a bound, a condition, a stored value. It is checked when the
   part is reached. An operator's own check is a relation between its operands (unification, comparison, the
   integers of quotient and remainder, the truth values of `and` and `or`), so it comes after them.
   - `a list of 1.5 copies of y` is TYPE, from the count. This is against the twin.
   - A For's lower bound has its Int requirement checked at that bound. This is the twin's reading, already the
     reference's.
10. **Item 47 is its bullets.** "One name may not stand for a variable and a procedure" summarizes §13's bullets
    ("already defined", "visible") and adds nothing to them. So a procedure may take the name of a variable that is
    no longer visible. (The twin's reading, already the reference's.)
11. **Rules and variables are compared as spelled.** Identifiers are case-sensitive (§2). Only a procedure's name,
    being lowercased words, is compared lowercased. (The twin's reading, already the reference's.)
12. **NESTING-DEPTH is about labels.** A reference with more than 24 parts names no clause, so it is UNKNOWN-CLAUSE in
    phase 6. (The twin's reading, already the reference's.)

**Dead rules the twin found.** No canonical text reaches these; they stay, marked:
- Within one clause, PROCEDURE-NAME before UNKNOWN-PROCEDURE, and EXPRESSION-DEPTH before PROCEDURE-NAME. Only a To
  can be PROCEDURE-NAME, and a To holds no call and no expression.
- §12's "a procedure body starts again at 0". A To stands only at the top level, where the depth is 0 anyway, and a
  nested To is refused before its body is walked.
- Phase 1 and the arbiter's rules concern raw bytes and comparisons, not canonical text. The door's rows and the
  arbiter's rows hold them.

**The differential run** (`python -B tests/diff_twin.py --n 20000 --seed 1 --minimize`):
- §13's run, against the round-2 twin: 20,221 texts. 18,749 were refused alike, 1,185 ran byte-identically and 287
  disagreed:
  - 282 because that twin predated §12 and §13 (LEX first, the depth bounds, a RecursionError);
  - 1 artifact of the harness, since fixed (a zero law seal's words are `babab-babab-babab-babab`);
  - 4 orders within a statement, settled in §13.
- This round's runs, against the round-3 twin, MEASURED here:
  - seed 1, with §13's seeds: 20,221 texts. 19,036 were refused alike, 1,185 ran byte-identically and **0
    disagreed**;
  - seed 2, with this round's probes and the E21 fixtures added as seeds: 20,353 texts. 19,282 were refused alike,
    1,023 ran byte-identically and 48 disagreed:
    - 47 are the three readings settled against the twin above (items 6, 7 and 9), as mutants of their probes;
    - 1 exceeded the run's time limit. Run again without the limit, both implementations refuse it FUEL-EXHAUSTED
      after 270,000,669 operations, with byte-identical receipts.
- Agreement on these samples is consistency between two readers of one text (§8 of DOCTRINE.md); it is not a proof
  that either reads the text rightly.

## 10. What the canonical text is

The door ([`src/orlog/canon.py`](src/orlog/canon.py)) maps raw bytes to canonical text and records every action as
REPAIR, NOTE or REFUSE:
- **Never changed:** text-literal contents.
- **Repaired outside literals:** typographic variants (curly delimiters, NBSP, tab, U+2212, U+00D7, U+00F7, ≤ ≥ ≠,
  NFC), line terminators, the BOM, and trailing spaces and blank lines.
- **Refused:** bytes that are not UTF-8, bidi controls, invisible characters in code, non-ASCII letters in code, and
  ambiguous dashes.
- The door is a retraction: canonical text passes through unchanged.
