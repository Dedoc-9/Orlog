# REREAD-1: the dispositions of its findings (PROPOSED, 2026-10-30; adopted, below)

**Adopted (2026-10-30).** The owner answered B1 with the merged six-part formulation and three precision corrections
(recorded whole in [RULINGS.md](RULINGS.md)). He then said: *"Proceed with draft 2 and its checker amendments."*

That answer replaces B1's options (a)–(c) below. The DRAFT dispositions are applied in `LAW-FORMAT-0-DRAFT-2.md`, and
the checker is amended to match (`evidence/rust-core-format-2.txt`). The comparison protocol is written into
`SHEET.md`'s Amendment 1. The text below is kept as it was proposed.

**Status.** Proposed, not adopted. These dispose of the 19 findings in [REREAD-1-REPORT.md](REREAD-1-REPORT.md), the
targeted re-read of LAW-FORMAT-0 draft 1 (sha256 `8c277a1e…`) and of its checker. Nothing changes until the owner
rules. He answers ASK B1 (G2); draft 2 then applies every DRAFT item and his answer; the checker is amended to match;
and a fresh targeted re-read follows. No core code is written before its findings are resolved (his condition 5).

**How each finding was checked.** Each concrete claim was run again here, read-only (*re-run* below). The reference's
recursion was run in a process that never imported the checker, since the checker raises Python's recursion limit.

**One discrepancy in the report.** Its verdict counts ten MAJOR findings, but its table and its list give nine: G1–G5
and G7–G10. G6 is MINOR, so ten MINOR (G6, G11–G19). These dispositions follow the list.

| | severity | finding | re-run here | disposition |
|---|---|---|---|---|
| G1 | MAJOR | "runs as" carried into static checks; read literally, W10 admits a rule cycle | the checker refuses T3, `W10 line 3`, as reported; the defect is the document's wording | **DRAFT:** define *the clause a part is checked at*: for a define's value and proviso, the define's own clause; for every other part, the clause it runs as. W8's scope and W10 use it. The run keeps section 5's "runs as". Plants: T3 (W10), T4 (W8) |
| G2 | MAJOR | perform and rule nesting, and the work inside one statement, are unbounded; the reference itself crashes | **CONFIRMED:** with Python's default limit, the reference completes a perform chain of 300 and raises `RecursionError` at 600, for perform and rule chains alike. 18 doubling rules under budget 10 stop after 393,215 operations | **ASK B1** |
| G3 | MAJOR | U+0000 cannot be written unambiguously; the checker refuses its own `\u{0}` | **CONFIRMED** (`W2 line 3`) | **DRAFT:** h is the value in lowercase hex without leading zeros, `0` alone for zero. The checker refuses a `0` only when another digit follows it. Fixture: `\u{0}` |
| G4 | MAJOR | the checker accepts `(promote int …)` | **CONFIRMED** (accepted) | **DRAFT:** rule 1 reads "when the other operand's type is fix or float and is the promote's target". The checker allows a promote only with target fix or float. Plants: `promote int` in `+`, `==` and `<` |
| G5 | MAJOR | the checker crashes on an arm or else naming no clause | **CONFIRMED** (`KeyError: 99`) | **DRAFT** (checker): no check that needs a clause is made when that clause is missing (section 8 already says so). Plants: G5's three laws, each refused W4 on the If's line |
| G6 | MINOR | W1 not reported at the first failing line | **CONFIRMED** (line 4 where line 3 fails) | **DRAFT** (checker): each line is checked completely, in order. A missing final LF belongs to the last line, the one with no LF |
| G7 | MAJOR | W1's reading of a clause line is undefined; W1, W2 and W3 overlap | **CONFIRMED** (`(clause 1  0 …)` is W1) | **DRAFT:** W1 reads a clause line's prefix byte by byte: `(clause `, a canonical ⟨n⟩, one space, a canonical ⟨n⟩, one space, then the rest, then a final `)`. Any defect in the prefix or the final `)` is W1. The rest, the word `absorbed` included, is W2/W3 |
| G8 | MAJOR | which line a relational failure belongs to; whether the walk enters malformed structure | reproduced by the report's C10, C15 | **DRAFT:** a failure that relates two lines belongs to the later one, as the front end does; a cycle belongs to each of its defines' lines. The walk enters no block that fails W5, and no inline statement that fails W7 |
| G9 | MAJOR | section 8's precedence forces a parse of unbounded depth; the checker crashes at 25,000 | **CONFIRMED** (`RecursionError`) | **DRAFT:** W14(c) becomes lexical and moves into phase 2. A line whose parentheses outside strings nest more than 130 deep is W14 on that line, checked before W2 and W3 on it. 130 is 4 statement levels plus 126. A reader's parser then never goes deeper than 130. Plants: depths 131 and 25,000 |
| G10 | MAJOR | ⟨n⟩ unbounded, unwarned | the report's C4 | **DRAFT:** W2 puts no length limit on ⟨n⟩. Every later check compares it as a decimal of any length, so a reader may not parse it into a fixed-width integer before W1–W14 hold |
| G11 | MINOR | W14(c)'s derivation misstates the define's `not` and is loose | — | **DRAFT:** the define's `unless` `not` is counted by the front end, not added after. Promotes cannot stand on two consecutive parsed nodes, so the true bound is at most 95. 126 is kept as a safe bound and said not to be tight. Plant at 127 and fixture at 126, by the lexical form (G9) |
| G12 | MINOR | when a cost counter grows | **CONFIRMED** (`claim 0 4 2 2 0 2 0`, then `claim 1 5 1 1 0 2 12`) | **DRAFT:** when the statement ends, its counter grows by ops − start. A claim inside the clause reads the counter as it stood before. C8 becomes a worked example |
| G13 | MINOR | section 10's gaps | — | **DRAFT:** the order of outcomes is usage, then reading LAW, then the load checks, then the run. TRACE, if given, is created when the run starts, so a run with no event leaves it empty. A missing final LF belongs to the last line. Paths that repeat are a usage error. A positional argument may not begin with `--`. `<reason>` holds no LF |
| G14 | MINOR | section 5a's gaps | — | **DRAFT:** rows for `and` and `or` (short-circuit, counted after the left operand) and for `not`. `as` passes rounded = 0, `rounded` passes 1. `x_as_i` and `f_as_i` are named here, not in RUNTIME-SPEC. The vectors' `sha256` lines test the core's SHA-256 |
| G15 | MINOR | derivation 19's worked value | **CONFIRMED:** the empty law's seal `91e3deb3…` gives `nalog-tupug-sivik-siduh` | **DRAFT:** that worked value; the all-zero case cited at SPEC §14 (SPEC.md:672), not §9 |
| G16 | MINOR | the author cannot identify the supplementary file; no worked run | — | **DRAFT:** §0 gives the file's sha256, line counts and refusal counts. An appendix gives worked laws → receipts and traces, produced by the reference and marked as data, as the vectors are |
| G17 | MINOR | traceability to ruling 2 dropped | — | **DRAFT:** section 6 regains the analysis field each derivation stands for, in a column the author need not use, and the status quotes ruling 2 again |
| G18 | MINOR | the new checks have no plants | — | **DRAFT:** plants for: W14(a) at 25; W14(b) at 17; an id in line order rather than walk order; `(lit float …)` under `fixed`; T3; T4; `\u{110000}`; `promote int`; G5's missing arm. Fixture for `\u{0}` |
| G19 | MINOR | wording | — | **DRAFT:** "0" for a top-level parent; W5's breach lines by G8 |

## The question for the owner

**B1 (G2). A law the front end accepts can nest `perform` and rule uses to any depth, and can make one statement's work
grow exponentially.** Examples are a chain of 600 procedures each performing the last, and 64 rules each using the
previous one twice. The reference itself raises Python's `RecursionError` from about 600 levels, at its default
recursion limit, so it defines no result there. The budget is checked only between statements, so it cannot stop the
work inside one. What should the core's milestone require?

| | what it entails |
|---|---|
| **(a) robust core, reference as it is** | The core evaluates `perform` and rule uses with explicit stacks, never the host's, so every accepted law runs to its SPEC result, or stops at a statement boundary under its budget. The format says plainly that the budget bounds the statements begun, not the work inside one. R3, R5 and R6 compare only where the reference gives a result within a stated wall-clock bound. A law on which the reference crashes or runs past that bound is recorded as "no reference result", neither a pass nor a fail. The reference's `RecursionError`, and its HostStop docstring's "no statement runs unbounded" (`interp.py:32-35`), are recorded as findings on the reference, to be corrected separately. |
| (b) a defined dynamic bound | A maximum nesting of `perform` and rule uses, with a defined host outcome beyond it, in the core and in the reference alike. That changes the reference's behaviour, so it needs a ruling on `src/` and the specifications. Not authorized now. |
| (c) a static bound in the format | A W15 refusing laws whose chains of procedures and rules exceed some D. Stricter than the front end: the core would refuse laws the reference runs. It also leaves the exponential case open. |

Recommended: **(a)**. It changes no released semantics, it keeps the reference the authority, and the core cannot be
crashed by a law the format accepts. It amends the accepted sheet's R3, R5 and R6 (their comparison domain), so it
needs your word.

## Findings for the owner on the reference itself (to scope separately, not in this milestone)

- `src/orlog/interp.py` evaluates `perform` and rule uses recursively on Python's stack. It raises `RecursionError`
  from about 600 nested levels at the default limit (MEASURED here). Its result there depends on a host setting.
- `interp.py:32-35`, the HostStop docstring, says *"no statement runs unbounded"*. One statement's work can grow
  exponentially through rule uses (393,215 operations from 18 rules, MEASURED). Each statement does end, but no bound
  stops it in practice.

These join the two correction proposals already owed: `examples/legal.orl`'s note, and `sema.py:6`'s docstring.

## What follows his answer

1. **LAW-FORMAT-0 draft 2:** every DRAFT item and his answer, each change marked with its finding. Drafts 0 and 1 and
   both re-read reports stay as they are.
2. **`format_check.py` amended to match:**
   - the clause a part is checked at;
   - the lexical W14(c) in phase 2;
   - W1's prefix;
   - the relational lines;
   - no walk into malformed structure;
   - the G3, G4, G5 and G6 fixes;
   - G18's plants and the `\u{0}` fixture.
   
   It runs twice, with every law still accepted.
3. **A fresh targeted re-read** of draft 2 and the checker.
4. **No core code** before its findings are resolved.
