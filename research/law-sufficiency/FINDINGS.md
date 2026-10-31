# LAW-SUFFICIENCY-0: findings (2026-10-30)

**Status.** The results of the experiment that [SHEET.md](SHEET.md) planned and the owner accepted on 2026-10-30, in
his words: *"Accepted. You may build the three tests."* This report is not a ruling, and it authorizes nothing:
- no Rust core;
- no integration of the decoder;
- no change to released semantics, the gate or version 1's path.

Every result is MEASURED on the texts and plants named here, on one host, and none is ESTABLISHED.

**Where it ran.** Here, on the Windows working copy, CPython 3.14.5, at commit `2e9805a`, with only the research files
added. `src/`, `tests/` and `vectors/` are unchanged, which the runner checks before it writes. Each test ran twice, and
the two outputs were byte-identical. The evidence:
- [`evidence/law-sufficiency-test1.txt`](../../evidence/law-sufficiency-test1.txt)
- [`evidence/law-sufficiency-test2.txt`](../../evidence/law-sufficiency-test2.txt)
- [`evidence/law-sufficiency-test3.txt`](../../evidence/law-sufficiency-test3.txt)

Each file starts with its command, its tree and the sha256 of the code that made it.

## The answer, on these texts

On every text tested, the law bytes determined the reference's run:
- **Test 1:** everything the run reads and the bytes do not write is derivable from the bytes.
- **Test 2:** texts sharing a law seal ran alike.
- **Test 3:** a decoder that reads only the bytes rebuilt runs identical to the parsed ones, and wrote the bytes back
  exactly.

All three tests HELD, and every plant came out as stated before it ran. In the sheet's terms, this is the outcome
"all three hold", MEASURED on finite sets.

## The texts

COMPAT-0's frozen set holds 3,361 texts. Of these, 300 have a law, and they are **290 distinct texts** by their bytes.
The sheet said 300: ten of the frozen ids repeat another's bytes, and a text is run once.

All eleven texts in `examples/` and `examples/spellings/` are byte-identical to frozen texts, so they add none. Every
accepted text compiles at `2e9805a`. No run was stopped by its budget, and none crashed, except where a plant made it.

## Test 1: what the run reads against what the seal writes

A recorder logged every attribute read on the compiled law's objects, by phase. The interpreter (`run`) reads 72
(class, attribute) pairs, and `law_bytes` (`seal`) reads 66. The recorder changed nothing: P and the law bytes were the
same with it as without it, on every text.

**R_run − R_seal holds 15 pairs.** Each has a written derivation from the law bytes, and test 3 runs every one of them:

| pair | read on | derived from the law bytes as |
|---|---|---|
| `Program.top` | 290 texts | the clauses whose parent id is 0 |
| `Analysis.claims` | 290 | the claim lines, by their written claim id |
| `Clause.cost_tracked` | 288 | true for a clause that a claim's `(certificate N …)` names |
| `VarInfo.type` | 147 | the let's expression type; int for a for's counter |
| `Var.type` | 86 | the variable's or the rule's type |
| `Clause.children` | 54 | the clauses whose parent id is this clause's |
| `Str.type` | 42 | text |
| `ClaimSite.id` | 39 | the claim's clause: its line's, or its arm's or else's for an inline claim |
| `Analysis.overrides` | 37 | each define's `(over …)` list, closed transitively |
| `Analysis.rules` | 37 | the define lines of each name, in clause order |
| `Cat.type` | 34 | text |
| `Change.elem` | 23 | the variable's type, or its element type when an index is written |
| `Item.type` | 7 | the list's element type |
| `BoolLit.type` | 6 | bool, written in the literal |
| `Conv.type` | 4 | the conversion's target |

**The sheet's static table, against the trace.** All seven of its pairs were traced. The trace found eight more:
`Program.top`, `ClaimSite.id`, and the `.type` of six expression kinds, which the interpreter reads on an operand
(`interp.py:203, 343, 364, 370`).

**Sealed, and never read by the run** (nine):
- `Let.name`, `ProcDef.name`, `Define.name`;
- `Claim.premises`;
- `Define.over`, which the run reads through `an.overrides`;
- `Clause.parent`, which it reads through `children`;
- `Program.clauses`, `Analysis.decimals`, `Decimals.mode`.

So the seal is finer than execution. Two laws that differ only in a name have different seals and the same run. This
experiment tests one direction only: equal seal implies equal run.

**What the backends read.** The lowering and the three generators read 20 pairs the law bytes do not write. This is
reported only; it decides nothing. Three of them are read by the backends alone: `Analysis.vars`,
`Analysis.rule_types` and `VarInfo.top`. Each has a written derivation (in `test1_reads.py`, `BACKEND_ONLY`), but no
test ran them, since D does not build them.

**Plants:**
- The interpreter made to read `Clause.line` was listed as not derivable: caught.
- The recorder made to drop `Change`'s reads left the table's `Change.elem` reported NOT TRACED: caught.

## Test 2: equal seal, equal behaviour

P, fixed before the run, is the receipt without its `backend` and `text-seal` lines.

Among the 290 texts there are 173 distinct laws, and 67 of them have two or more distinct text seals (184 texts).
Thirteen transforms were applied to each text. A variant was kept only if its law seal equalled its source's. **No
variant moved a law seal.**

| transform | kept, text seal unchanged | kept, text seal changed | refused | no site |
|---|---|---|---|---|
| CR LF; a BOM; trailing spaces; blank lines | 290 each | | | |
| NBSP in code | 288 | | | 2 |
| U+2212 minus | 30 | | | 260 |
| U+00D7 times | 6 | | | 284 |
| a Note added; a Note in NFD | | 290 each | | |
| the Title changed | | 287 | 3 (TITLE-PLACE) | |
| 0.1 written 0.10 | | 29 | 1 (LINE-CHECK) | 260 |
| a double space in code | | 279 | 9 (LINE-CHECK) | 2 |
| a keyword in capitals | | 276 | 9 (LINE-CHECK) | 5 |

The refusals are what the compiler says: a line's check syllables hash its text, and a Title must be the first line.

**The comparison.** The run covered 3,225 texts in 173 groups. Every group has two or more members, and every group
spans two or more distinct text seals. **No group's P differs.** The three spellings share one law seal and one P
across their three text seals.

**Plants:**
- The interpreter made to fold the text seal into its output: failed exactly the 173 groups, as stated.
- P made to keep the text-seal line (COMPAT-0's receipt core): failed the same 173. That shows the projection is what
  makes the comparison possible.

## Test 3: an independent decoder

The decoder D (`decoder.py`, sha256 `4f9a66b4…`) reads the law bytes alone. It builds the program and the analysis the
interpreter runs, and derives all 15 pairs above itself.

| check | result |
|---|---|
| decoded | 290 of 290 texts |
| decoded P equal to parsed P | 290 |
| `law_bytes` of D's result equal to the bytes D read | 290 |
| independence | held: D imports `struct` and syntax.py's node classes only, and names nothing that reaches the parsed path |

**Plants in the parsed path.** Each changed one structure the bytes do not write, with the law bytes held fixed. The
law bytes moved on none, and the decoded run never moved.

| plant | applied to | parsed P changed on | verdict |
|---|---|---|---|
| an override edge removed | 12 texts | 7 | caught (e.g. fall.orl: COMPLETED became REFUSED RULE-CONFLICT) |
| a claim site dropped | 39 | 39 | caught (some as a crash, IndexError) |
| `cost_tracked` flipped on a certificate's clause | 9 | 8 | caught (gcd_certificate.orl: the claim's cost 724 became 0) |
| a Change's `elem` made `fix` | 14 | 13 | caught |
| `an.rules` reversed | 19 | 0 | measured: equivalent on all 19 |

**Plants in D:**
- D deriving `elem` without the index: the decoded P differed on 8 texts, caught.
- D's source given an import of `sema`: the independence check reported it, caught.

## Failures and inconclusive results

**No test failed, and no plant was missed.** These are what the experiment left open or could not show:

1. **One decoder form was never exercised.** The `rounded` conversion form appears in no text: 0 of 290. D handles it
   by the same code as `as`, but no run has tested it.
2. **The backend derivations were never run.** Those for `Analysis.vars`, `Analysis.rule_types` and `VarInfo.top` are
   written only, and D does not build them.
3. **Reversing `an.rules` is equivalent on this set, and not shown equivalent in general.**
   - By reading `interp.py:428-436`, provisos and then the maximal definitions' values are evaluated in list order, and
     the first refusal ends the run.
   - So on a text where two of a rule's provisos or values refuse with different codes, the order would decide the code.
   - No text in the set has one. This is DECLARED from the reading, not measured. Rule order is document order, which
     the law bytes do write.
4. **The plants did not all apply everywhere.**
   - The override plant changed the run on 7 of the 12 texts it applied to; on the other 5 the removed edge decides
     nothing.
   - `cost_tracked` changed 8 of 9, and `elem` 13 of 14.
   
   These are counted, not hidden.
5. **What the recorder cannot see.**
   - It logs attribute reads, so the interpreter's dispatch on a node's class (`isinstance`) is not traced.
   - Each form's head word seals the class, and test 3's exact round trip covers it.
   - Module constants and the interpreter's own state are outside what the recorder wraps.
6. **One test-1 label was corrected before the evidence run.** A first pass labelled the three backend-only pairs NOT
   DERIVABLE, because no derivation had been written for them yet. Each was given its derivation, marked as not run,
   before the runs the evidence records.

## An incidental finding

**The docstring at `src/orlog/sema.py:6` says** *"changing 0.1 to 0.10 changes neither"* **seal. That is not what the
code does.**
- `§1 Say 0.1.` and `§1 Say 0.10.` have one law seal and two text seals (MEASURED).
- The canonical text keeps the literal as it was written.

`src/` is not changed here. The correction is for the owner to scope.

## What this does not show

- **That the law bytes are sufficient for every law.** These are finite sets: 290 texts, 2,935 variants of them (3,225
  runs in test 2) and 11 plants.
- **That D is a second implementation of execution.** D's result runs on the same interpreter, built from syntax.py's
  shared node classes.
- **That the backends read only sealed fields.** Their reads are reported; their runs are not compared here.
- **Version 1's law forms** (ports, the tick block), which §15 has yet to define.
- **That Float is identical on another host** (HOST-0), or that a Rust core is correct.
- **The prose printer** of LAU-1.

## What follows, for the owner to decide

These are proposals, not rulings:

1. **The law bytes of version 0 are the candidate boundary** for an independent core. A core would read them, and not
   prose or Python's analysis structures.
2. **The 15 derivations could become written obligations of the law-bytes format.** Any core would have to implement
   them: typing, `elem`, the override closure, the claim sites, the children and the top, and `cost_tracked`. Two
   things come with them:
   - the three backend-only derivations, which a backend-reading core also needs;
   - the order the rules are evaluated in, which is the define lines' order.
3. **Before any core is built on this boundary:**
   - a text that exercises the `rounded` conversion;
   - a measured case for rule order with refusing provisos;
   - the backends' read sets compared on runs, not only reported;
   - version 1's law forms written into §15 before the pin.
4. **The `sema.py:6` docstring** needs a separately scoped correction.

## How to run it

From the repository's root: `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/law-sufficiency/run_all.py`. It takes
about three minutes here. It runs `test1_reads.py`, `test2_equal_seal.py` and `test3_decoder.py` twice each and writes
the three evidence files.
