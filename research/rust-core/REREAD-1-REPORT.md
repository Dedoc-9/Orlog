> **A tokened copy, not the original hand-back** (2026-10-31, his ruling on the ten older reports, by REREAD-9's ASK 9-2 procedure): each spelling of the home folder's path is replaced by a token, `⟦HOME⟧` or `⟦HOME83⟧`; the original is kept outside the repository and named in `kept/TOKENED.txt` by its length and sha256, and `kept_tokens.py restore` gives it back exactly with the prefixes. After this line and the blank line below it, the file is the kept tokened bytes exactly, so its line numbers are the original's plus two.

# REREAD-1: the targeted independent re-read of LAW-FORMAT-0 draft 1 and its checker, its report word for word (2026-10-30)

Saved as returned by the re-reader, a fresh general-purpose agent with no part in writing the document or the checker.
Its brief:
- read draft 1 (sha256 `8c277a1e…`), draft 0, REREAD-0's report and dispositions, `format_check.py` and its recorded
  run, the supplementary vectors and their manifest, SPEC.md, RUNTIME-SPEC.md, and `src/orlog/` for faithfulness;
- never open `research/law-sufficiency/`;
- write nothing, and run only read-only commands;
- answer draft 1's Q1–Q6 with evidence, and list its findings, G1 onward, by severity.

Its report follows, unedited. The only change is that the leading indentation the hand-back added to every line is
removed.

---

LAW-FORMAT-0-DRAFT-1.md read: sha256 `8c277a1e6305e7301bc6316dde534f342fbe3c7b52bffb5ed4e135b056496a05`

# REREAD-1: targeted independent re-read of LAW-FORMAT-0 draft 1 and its checker (2026-10-30)

## What I read, what I ran, and what I could not check

**Read in full:**
- `research/rust-core/LAW-FORMAT-0-DRAFT-1.md` (the sha256 above, equal to the one in `evidence/rust-core-format-1.txt`);
- `LAW-FORMAT-0-DRAFT-0.md`, `REREAD-0-REPORT.md` and `REREAD-0-DISPOSITION.md`, plus `RULINGS.md` for the rulings' wording;
- `format_check.py` (sha256 `fa0a0c9be3f594c8ca67a87b195f448f5844c21494e6c2450c76356100585a64`, equal to the evidence's) and `evidence/rust-core-format-1.txt`;
- `vectors-as-integer.txt` (`2bff1c69…`), its manifest, and `gen_as_int_vectors.py` (`abbbe310…`), the last read only to check the manifest;
- `SPEC.md` and `RUNTIME-SPEC.md`;
- `src/orlog/sema.py`, `interp.py`, `syntax.py`, `numeric_ref.py` (`eacac3dd…`), `front.py` and `seal.py`.

**Read in part:** `canon.py` (lines 1–60), `lower.py` (lines 300–400) and `arbiter.py` (lines 215–260). I searched `rt_py.py`, `gen_c.py`, `gen_rs.py` and `SHEET.md` with grep.

**Not opened:** `research/law-sufficiency/`.

**Ran:** only read-only commands: `sha256sum`, `grep`, `sed`, `wc`, `git log` / `git diff`, and `python -B -c` one-liners. Each one-liner imports `format_check.py` or `src/orlog/` and tests bytes or a text in memory. I wrote no file. Environment: Git Bash on Windows, CPython 3.14.5, `PYTHONHASHSEED=0 PYTHONUTF8=1`, at HEAD `2e9805a` with the research files uncommitted. The commands and their outputs are in the appendix.

**Could not check:**
1. I did not run `format_check.main()`. It imports `common` and `closure_tests` from `research/law-sufficiency/`, which I may not read. The "302 of 302" and "22 of 22" figures are therefore the recorded evidence, not re-run. Every checker result below comes from `format_check.read(bytes)` on bytes I wrote.
2. The LS-0 and LS-1 evidence in the *held by* column.
3. What shapes the 298-law corpus contains.
4. Any compiled backend. Nothing was built.

## Verdict

Draft 1 and its checker are **not ready** to hand to the clean-room author. I found no new BLOCKER of F1's kind. There are ten MAJOR findings:

| | MAJOR finding | where |
|---|---|---|
| G1 | "runs as" in static checks (W8, W10) admits a rule cycle if read literally | document |
| G2 | perform and rule nesting, and rule cost, are unbounded; the reference crashes at depth 600 | document, needs a ruling |
| G3 | U+0000 cannot be written unambiguously; the checker refuses its own writer's `\u{0}` | document and checker |
| G4 | the checker accepts `(promote int …)` | checker |
| G5 | the checker crashes on an arm or else naming no clause | checker |
| G7 | W1's reading of a clause line is undefined, so W1, W2 and W3 overlap | document |
| G8 | which line a relational failure belongs to is underdetermined | document |
| G9 | section 8's precedence forces a parse of unbounded depth; the checker crashes at 25,000 | document and checker |
| G10 | ⟨n⟩ is unbounded in W2 and the document does not warn | document |

There are ten MINOR findings: G6 and G11–G19.

The three that most need attention before handoff:
- **G2** needs an owner ruling. A law that the front end and W1–W14 both accept can be nested to any depth through `perform` and `rule`. The reference interpreter itself raises RecursionError at depth 600. Draft 1 dropped the F3 disposition's sentence that the core "may not recurse past a fixed stack".
- **G1.** Draft 1 replaced draft 0's positional W10 ("stands after the last define") with "the use runs as a clause …". Section 5 defines that clause dynamically for a rule's values. Read literally, W10 then accepts a cycle of rules that recurses without end. The checker reads it the safe way.
- **G3.** A1(a) admits every scalar value, but the string rule makes U+0000 either unwritable or ambiguous. The checker refuses `\u{0}`, which is exactly what both its own writer and `sema.py` write.

---

## Q1. Can bytes pass W1–W14 and still fault, or run differently in two readers?

**Yes, in two ways that fault and several that diverge.**

**(a) Stack and time faults on laws that pass W1–W14, and that the front end also accepts (G2).**
- **Perform chains.** Procedure p_k performs p_{k−1}. W11 allows it, since each perform names an earlier procedure outside its body, and nothing in W1–W14 bounds the length of the chain. Rule chains are the same: r_k's value uses r_{k−1}, which W10 allows.
- **The checker accepts both** at lengths 200 and 600 (appendix C6).
- **The reference interpreter**, under Python's default recursion limit of 1000, completes length 300. At lengths 600 and 3000 it raises `RecursionError`, for both kinds of chain (C7). The causes are `interp.py:242-244` (`perform` → `seq` → `stmt`) and `interp.py:423-440` (`rule` → `eval` → `rule`).
- **Rule cost.** A law in which each rule's value uses the previous rule twice costs 2^N operations in one statement. With 18 rules and `--budget 10`, the reference reports `STOPPED-BY-HOST after 393215 counted operations (budget 10)` (C6). Section 5 makes the budget check "never … inside an expression" (draft:249), so nothing stops such a statement. At about 64 rules a single Say does not end in practice. This contradicts the HostStop docstring (`interp.py:32-35`: "no statement runs unbounded").
- **What the document promises.** Section 8's "What a pass means" promises only freedom from faults the front end prevents (draft:354-357). The front end prevents none of these, so no stated promise is broken. But the document gives the core no obligation either. A core written recursively, which is the natural way, aborts on such a law, and SHEET's R6 calls that a panic.

**(b) A rule cycle accepted under the literal reading of W10 (G1).** Take these bytes:

```
(clause 1 0 (define "b" (rule "c") - (over )))
(clause 2 0 (define "c" (rule "b") - (over )))
(clause 3 0 (say (rule "b")))
```

- **Under section 5's definition** (draft:232), a rule's values run as the use site, here clause 3. Since 3 > 2 and 3 > 1, W10 as written (draft:370) passes, and the run recurses b → c → b without end.
- **The checker refuses it**, `W10 line 3`, because it checks a define's value at the define's own clause (`format_check.py:761-764`, `856-868`; test T3). That is also what the front end does (`sema.py:373-378`) and what SPEC.md:384-385 says (item 46).

**(c) Two readers that follow the document can differ:**
- by G1: accept a cycle, or refuse it; accept a define's use of a later `let` (test T4), or refuse it;
- by G2: one reader overflows its stack, the other completes;
- by G3: refuse U+0000, or accept it;
- by G12: a claim nested inside its certificate's clause gets ref-cost 0 under SPEC §7's "afterwards", but a nonzero value under a live counter that draft:235-239 permits. Test C8's receipt prints `claim 0 4 2 2 0 2 0`;
- by G10: a 20-digit id is W2 in a reader that parses into u64, but W4, W8, W13 or W1 by the document;
- by G7 and G8: a different (line, W) on refused input.

**No read of an unassigned variable found.** I checked the scope rule (draft:414-422), together with W1's pre-order, for these cases:
- top-level lets;
- lets in a block;
- uses in an absorbed arm's condition;
- For counters;
- procedure bodies performed later;
- define values, under the define-clause reading.

In each case the declaring clause runs before any use in scope. F1's crash is closed: its plant is refused W1 line 5. **No unbounded loop** apart from (a): a While has its fuel, and a For has a finite i64 range.

## Q2. Is any check now stricter than the front end?

**In the document: no.** Each point the brief named:

- **The walk order of ids (section 7)** equals sema's walk. That walk is `sema.py:76-80` and `103-121` with `158-163`: each arm's condition, then its body, then the else; a let's variable after its value (`124-125`); a For's counter after its bounds (`173-176`); a procedure's body at its own clause (`191-195`). It also equals SPEC.md:173-174, "textual order of declaration": an absorbed clause's text line follows K's children, so text order and walk order agree for declarations. The fixtures, including the forward declaration, are accepted.
- **Promote placement (W9)** equals the front end's only three sources:
  - `unify` (`sema.py:311-322`), one operand only;
  - `fit` (`303-309`), from `assignable` for set and change and from Append;
  - list items (`460-471`), so a promoted item implies at least one item of the target type.

  A let stores its value unpromoted (`123-125`).
- **If-chain shapes** equal `syntax.py:267-298`:
  - an inline otherwise ends the chain (`290-292`);
  - a block `then` returns before any `;` (`481-483`), so a block arm cannot take an inline otherwise;
  - absorbed clauses are the next siblings in order (`last_if` is reset by any other clause).
- **W14(a) and (b)** equal the front end at the boundary (C13). The front end accepts 16 nested loops and refuses 17 with LOOP-NESTING, the same inside a procedure. It accepts clause depth 24 and refuses 25 with NESTING-DEPTH. The checker refuses a hand-made 25-deep law, `W14 line 27`.
- **W14(c)'s 126 is a valid upper bound**, so it is never stricter. The derivation, checked:
  - `ast_depth` (`syntax.py:79-92`) runs in `statement()` (`412-414`), before `_attach_otherwise` (`263`).
  - A clause's own expressions have their root at depth 2, so they are at most 63 deep. An inline statement is a child of the statement node (SPEC.md:636), so its expressions have their root at depth 3 and are at most 62 deep.
  - After the check, only two things add expression nodes: the Unless's `not` (`syntax.py:282-285`) and promotes (`sema.py:295-298`, called from `308`, `317`, `320`, `471`). `(rule …)` replaces a Var one for one, and parentheses make no node.
  - So 126 holds. The derivation has two inaccuracies (G11): the define's `unless` `not` is counted, not added after; and "at most doubles" is loose. A promoted node is an Int, and its parent has type Fix, Float, Bool, a list, or is a statement. So no two consecutive parsed nodes on a path can both carry a promote, and the true bound is at most 63 + 32 = 95. The atom-nesting limit of 24 (`syntax.py:75`, `339-343`) caps the number of promotes on a path lower still.
  - The recorded corpus maximum is 64.
- **No front-end law exceeds any W14 bound** I could derive.

**In the checker:** it is stricter than the format only on `\u{0}` (G3). No front-end text produces U+0000, because the door refuses C0 controls in literals. So the checker is stricter than A1(a), not than the front end.

## Q3. Is section 5a faithful, and is it enough?

**Faithful.** Each row matches `interp.py:287-421`, `lower.py:367-386`, `numeric_ref.py` and RUNTIME-SPEC §2. In particular:
- `promote fix` is `x_from_i`, and `promote float` is `f_from_i(·, 0)` (`interp.py:401-402`; SPEC item 40);
- `as`/`rounded` to Int from Fix is `x_as_i`/`x_round`, and from Float `f_as_i`/`f_round`;
- to Fix: from Int `x_from_i`, from Float `f_to_x`;
- to Float: `f_from_i`/`x_to_f`;
- Float comparisons are native (`interp.py:327-338`).

**Not quite enough:**
- `and`, `or` (which short-circuit, SPEC item 35, SPEC.md:364) and `not` have no row, although ⟨binary⟩ and ⟨unary⟩ contain them.
- "with rounded = 0 or 1" (draft:266-268) never says that `as` is 0 and `rounded` is 1 (`lower.py:381, 384, 386`).
- "The names are RUNTIME-SPEC §2's functions" (draft:253), but `x_as_i` and `f_as_i` are not in RUNTIME-SPEC §2. See G14.

**The supplementary vectors (C2, C3).** Every claim in the manifest holds:
- the file has 446 lines, ASCII, LF, no CR;
- `x_as_i` 178 and `f_as_i` 268;
- 189 refusals: NOT-FINITE 6, INEXACT-CONVERSION 143, OVERFLOW 40;
- the file's sha256 is `2bff1c69…`;
- the generator's sha256 is `abbbe310…`, and `numeric_ref.py`'s is `eacac3dd…`;
- the contract file is unchanged, `841240b7…`.

All 446 lines also agree with `numeric_ref.x_as_i`/`f_as_i` **and** with the interpreter's inline implementation (`interp.py:403-414`), which is a separate code path: 0 disagreements. The file covers the boundaries: ±2^63, the largest Float below 2^63, −0.0, subnormals, NaNs with payloads, ±∞, and raw `I64_MIN`/`I64_MAX`.

The author may not read the manifest (draft:27-28), so nothing in the reading set names this file's sha256 (G16).

## Q4. Does section 10 give each outcome one exit status, one set of files and one stderr line?

**Each of the six rows has one exit status and one stderr form.** "I/O error" has no fixed set of files, by design ("whatever was written before the error").

**Missing or ambiguous (G13, and G2 for the last item):**
1. **Precedence among outcomes.** A bad TEXTSEAL together with a malformed LAW could be a usage error (exit 2) or a load refusal (exit 3). An unreadable LAW with a bad TEXTSEAL could be USAGE or IO-ERROR. A stop whose trace cannot be written could exit 4 or exit 2.
2. **A run with zero events and TRACE given** (the empty law, for example). "A file is created … only when it is written" (draft:499) together with "the trace is written as events happen" suggests no file. But `rt_py.py:84` opens the trace at start, and the arbiter tells an absent trace (`None`) from an empty one (`arbiter.py:243`).
3. **The line `<n>` of a missing final LF.** The checker uses the last, incomplete line.
4. **OUT, RECEIPT and TRACE given the same path.**
5. **A TRACE path spelled `--budget`.**
6. **No row for exhausting the stack or memory.** That is G2's case, and the reference itself crashes there.

## Q5. Does `format_check.py` implement sections 2–4 and 8 as written?

**Where it matches:** the phase order (W1, then W2/W3 line by line, then W4–W14 collected and the least (line, W) taken); the walk (`visit`/`walk_seq`, lines 761-893); the scope rule (`visible`, `sibling_or_below` and `ancestor`, lines 468-479 and 731-737); W14(a), (b) and (c); the If-chain shapes; W12; W11; W13. It differs in these places:

| # | bytes | section 8 / the document | checker | kind |
|---|---|---|---|---|
| 1 | line 3 `XYZ`; line 4 holds byte 0x01 | W1 line 3 ("the first line that fails it", draft:448) | **W1 line 4** | another line (G6); it scans every line's bytes first (`400-401`) |
| 2 | line 3 `XYZ`; line 4 has no final LF | W1 line 3 | **W1 line 4** | another line (G6), lines 402 then 404-420 |
| 3 | line 1 `orlog-law 1`; line 4 is `\x01` | W1 line 1 | **W1 line 4** | another line (G6) |
| 4 | `(+ int (promote int (lit int 1)) (lit int 2))`, and the same inside `==` and `<` | refused W9: "the target is fix or float" (draft:388) | **accepted** | looser (G4): `promote_to` is the other operand's type, which may be `int` (lines 664-671, 622) |
| 5 | `(str "\u{0}")`, or a let named `"\u{0}"` | accepted by A1(a) (draft:117); its canonical form is `\u{0}` | **W2** "a \u{h} with a leading zero" (line 99) | stricter (G3) |
| 6 | an `(arm 99 …)` or `(else 99 …)` that holds a `var` or a `perform` | W4 on the If's line, with checks that need the missing clause not made (draft:364, 454-455) | **KeyError: 99** | crash (G5), lines 475-479, 731-737, 468-473 |
| 7 | a 25,000-deep chain of `not` on line 3, `(lit int 01)` on line 4 | W2 line 4 | **RecursionError** | crash (G9): `expr()` recurses (168-214) under a limit of 20000 (line 26). At depth 5,000 it reports W2 line 4 correctly |
| 8 | an inline `if` (a W7 failure) whose block names an earlier While body | W5 or W7 on the If's line (draft:451, "a failure in an inline statement belongs to its If's line") | **W8 line 4** "declared twice" | another (line, W) (G8): it walks the illegal inline If's block (802-804) |
| 9 | an inline `if` whose `(block 1)` names its own clause 1 | W7 line 3: clause 1 *is* named by a block (draft:365) | **W5 line 3** | another W: inline blocks are not counted (531-565) |
| 10 | `(clause 2 0  absorbed)` and `(clause 2 0 absorbed )` | W3 by draft:363 (spacing) | **W2** "not one form" | another W (G7) |
| 11 | a trailing or leading space on a clause line; `(clause 1  0 …)`; `(clause 01 …)`; `(clause 2 01 …)` | W3 or W2 by draft:362-363, or W1; ambiguous (G7) | **W1** | the document is ambiguous |
| 12 | an operand whose type is underived beside a promote | not checked (draft:454-455) | a W9 is checked (lines 668-671, 622-623) | no reported difference: the W8 on the same line wins |

The plants do not exercise rows 1–12, W14(a) or (b), the refusal of an id numbered out of walk order (F2), W6's literal mode (F11), or `\u{110000}` (G18).

## Q6. Did draft 1 break what REREAD-0 found right, and is each F resolved?

**Writing (REREAD-0's Q5) is unbroken.** Sections 1, 3 and 4 write exactly as draft 0 did. Draft 1 only adds the scalar-value limits and "1 to 6 digits" to the string rule. `sema._q` and the checker's `q` are identical (C11), and the recorded round trip is 302 of 302.

**The derivations REREAD-0 confirmed** (1–5, 6–7, 9, 10–15, 17, 18) are unchanged in substance. Derivations 8 and 16 are rewritten as REREAD-0 proposed.

**One regression, G1.** W10's positional "stands after" became "runs as". **One loss of traceability, G17.** The field names that ruling 2 requires (`Analysis.vars`, `Analysis.rule_types`, `VarInfo.top`) were dropped from section 6.

| finding | resolved? | evidence |
|---|---|---|
| F1 | **yes** | draft:88-95, 361; checker 409-420; the plant is refused W1 line 5 |
| F2 | **yes** for ids and claim sites; **regression** in W10 | draft:297, 319-345; fixtures accepted; G1 |
| F3 | **partly** | W14 added (draft:424-441); (a) and (b) are exact and (c) is safe (G11); the disposition's "may not recurse past a fixed stack" (REREAD-0-DISPOSITION.md:19) is absent (no "stack" or "recurs" in draft 1 except Q1); see G2 and G9 |
| F4 | **yes** in the document; the checker is looser | draft:388, 404-412; G4 |
| F5 | **partly** | scalar values are stated (draft:110-122); U+0000 is not (G3) |
| F6 | **yes** | draft:157-167, 365; both plants refused |
| F7 | **yes** | draft:244-249 equals `interp.py:132-135`, `149-154` |
| F8 | **partly** | the table, the precedence and the W2/W3 split are present; G6, G7, G8, G10 and G13 remain |
| F9 | **yes**, with G16 | draft:30-34; the vectors were checked (Q3) |
| F10 | **yes**, with G14 | draft:251-277 |
| F11 | **yes** | draft:366; checker 631-635 |
| F12 | **yes** | draft:82-83; the empty law is accepted (C12) |
| F13 | **partly** | performed bodies and rule uses are right; the cost-counter wording (G12); "runs as" carried into static checks (G1) |
| F14 | **yes** | draft:126-128 |
| F15 | **yes** | draft:294, 382-384 |
| F16 | **yes**, with G15 | draft:300 |
| F17 | **yes** | draft:18-59, 354-357 |

---

## Findings

### G1 — MAJOR: "runs as" governs static checks, but section 5 defines it dynamically for a rule's values
- **Document:**
  - draft:232: "a rule's provisos and values: the clause under which the use of the rule is evaluated";
  - W10, draft:370: "The use runs as a clause whose id is greater than the last define's of that name";
  - the scope rule, draft:414-422: "A use … runs as some clause U (section 5)". It then says "So … A define's value and proviso see the top-level variables declared before the define's clause", which does not follow when U is the use site.
- **Evidence:**
  - The front end checks a define's expressions at the define's clause: `sema.py:373-378`, `at = c.id` during the walk.
  - SPEC.md:384-385 (item 46): "the rules completely defined before it".
  - The checker does the same (`format_check.py:761-764`, `856-868`).
  - T3, the cycle in Q1(b), is refused by the checker as `W10 line 3`. Under the literal reading it is accepted and recurses without end.
  - T4 is `(define "r" (var 0) …)` at clause 1, then `(let 0 "x" …)` at clause 2, then `(say (rule "r"))` at clause 3. The checker refuses it `W8 line 3`. The literal reading accepts it.
- **Proposal:** define "the clause a part is checked at", separate from "the clause it runs as". For a define's value and proviso it is the define's own clause; everywhere else it is the clause the part runs as. Use it in W8's U and in W10. Add T3 (W10) and T4 (W8) as plants.

### G2 — MAJOR (needs a ruling): perform and rule nesting, and rule cost, are unbounded; the reference itself crashes
- **Document:**
  - W14 bounds only static nesting (draft:424-441);
  - the budget check is "never … inside an expression" (draft:249);
  - section 10 has no row for exhausting a resource;
  - F3's disposition ("The core's reader also may not recurse past a fixed stack for any accepted law", REREAD-0-DISPOSITION.md:19) is not in draft 1.
- **Evidence:**
  - C7: front-end texts with perform chains and rule chains of 600 and 3000 → the reference raises `RecursionError` (limit 1000). Length 300 → `COMPLETED`.
  - C6: with `format_check` imported, which sets the limit to 20000 (line 26), length 600 completes. So the reference's behaviour depends on a host setting.
  - C6: 18 doubling rules under `--budget 10` → `STOPPED-BY-HOST after 393215 counted operations`.
  - The checker accepts every one of these.
  - SHEET's R6 requires the core "never panics, never hangs past the budget".
- **Proposal:**
  - State that a core evaluates `perform` and rule uses without recursing on the host stack (with an explicit stack), so that any accepted law runs to its SPEC result, or else ask the owner for a bound with a defined outcome. Neither the format nor the front end can bound these today without refusing laws the front end accepts.
  - Say plainly that the budget bounds only the statements begun, not the work inside one statement.
  - Record the reference's `RecursionError` as a finding for the owner. The reference defines nothing at these depths.

### G3 — MAJOR: U+0000 cannot be written unambiguously; the checker refuses its own canonical form
- **Document:** draft:115, "h is the value in lowercase hex with no leading zero, 1 to 6 digits"; draft:121, "an `\u{h}` with a leading zero … is refused"; against draft:117, "Every scalar value may stand in a string". ⟨n⟩ says "`0` alone for zero" (draft:104), but the string rule does not.
- **Evidence:** C11:
  - `sema._q("\x00")` and `format_check.q("\x00")` both give `"\u{0}"`;
  - `format_check.read` refuses `(say (str "\u{0}"))` and a let named `"\u{0}"` with "W2 line 3: a \u{h} with a leading zero" (`format_check.py:99`);
  - `\u{1}`, `\u{202e}` and `\u{10ffff}` are accepted.

  The owner's A1(a) admits controls "provided the format defines their encoding … unambiguously".
- **Proposal:** "h is the value in lowercase hex without leading zeros (`0` alone for zero)". Fix line 99 to refuse `0` only when another digit follows it. Add a `\u{0}` fixture.

### G4 — MAJOR (checker): `(promote int E)` is accepted as an operand of an Int operator
- **Checker:** `format_check.py:668-671` passes the other operand's type as `promote_to`, and line 622 accepts any target equal to it, `int` included.
- **Evidence:** C9 accepts `(+ int (promote int (lit int 1)) (lit int 2))`, `(== bool (lit int 2) (promote int (lit int 2)))` and `(< bool (promote int …) (lit int 2))`, and writes each back exactly. The document refuses them: "the target is fix or float" (draft:388). Placement rule 1, read alone (draft:405-406, "when the other operand's type is the promote's target"), would admit them. The reference would compute `f_from_i` there (`interp.py:401-402`) and put a Float into an Int.
- **Proposal:** in the checker, set `promote_to` only to `fix` or `float`. In rule 1, write "when the other operand is fix or float and is the promote's target". Add a plant.

### G5 — MAJOR (checker): it crashes when an arm's or else's ⟨C⟩ names no clause
- **Checker:** `visible` → `sibling_or_below` → `C[u]` (lines 475-479, 731-737), and `ancestor(P, U)` (line 828), are called with a U that does not exist.
- **Evidence:** C14: `(else 99 (say (var 0)))`, `(arm 99 (var 0) …)` and `(else 99 (perform 1))` each raise `KeyError: 99`. Draft:364 and 454-455 require `W4` on the If's line. A certificate inside the same else is refused W4 correctly. SHEET R6's mutation "ids changed" can produce these bytes.
- **Proposal:** make no check that depends on U when U is not a clause. Add a plant.

### G6 — MINOR (checker): W1 is not reported at the first failing line
- **Checker:** lines 400-402 check every line's bytes, then the final LF, before the header and the clause lines.
- **Evidence:** C4, T1, T2 and T2b report line 4 where draft:448 chooses line 3 or line 1.
- **Proposal:** check each line completely, in order. Say which line a missing final LF belongs to (the last line, which has no LF).

### G7 — MAJOR: W1's reading of a clause line is undefined, so W1, W2 and W3 overlap
- **Document:** W1 requires "the clause lines numbered 1…n; each parent 0, k−1 or an ancestor" (draft:361). W2 requires canonical atoms (draft:362). W3 requires "single spaces … nothing at a line's ends" (draft:363). Nothing says what bytes W1 reads.
- **Evidence:** C4, C5 and C12:
  - `(clause 1  0 …)`, a trailing space, a leading space, `( clause …`, `(clause 01 …)` and `(clause 2 01 …)` are all W1 in the checker (by its regex, line 31);
  - `(clause 2 0  absorbed)` and `(clause 2 0 absorbed )` are W2;
  - the document's W3 names spacing and "nothing at a line's ends", and its W2 names non-canonical numbers.
- **Proposal:** define W1's clause-line prefix byte by byte. For example: `(clause `, a canonical ⟨n⟩, one space, a canonical ⟨n⟩, one space, the rest, then `)` with nothing after it. State that any defect in that prefix is W1, and that the rest, the word `absorbed` included, is W2/W3.

### G8 — MAJOR: the line of a relational failure, and the walk over malformed structure, are underdetermined
- **Document:** "Each failure belongs to the line whose bytes hold it" (draft:451) does not decide failures that involve two lines.
- **Evidence:** C10 and C15:
  - **a decimal literal before the decimals clause:** the checker reports the literal's line (`W6 line 3`). The front end reports the decimals clause (`sema.py:263-265`);
  - **an absorbed clause named by two Ifs:** the checker reports the second If's line (`W5 line 5`); line 3 or line 4 are equally defensible;
  - **two types for one rule:** the checker reports the later define (`W10 line 4`);
  - **an absorbed clause in no chain:** the checker reports the absorbed line;
  - **a block naming another clause, or a block inside an illegal inline If:** the checker walks the named body again and reports `W8 line 4` "declared twice", ahead of the W5 or W7 on the If's line. The document does not say whether the walk follows a malformed block.
- **Proposal:** name the line of each relational check (the later part, as SPEC §13 does for the front end; or the earlier). State that the walk does not enter a block that fails W5 or an inline statement that fails W7.

### G9 — MAJOR: section 8's precedence needs a parse of unbounded depth; the document does not require a parser that does not recurse
- **Document:** W2/W3 on every line comes before W14 (draft:448-450), so a reader must fully parse an arbitrarily deep line before it can report W2 on a later line.
- **Evidence:** C5. A 5,000-deep line followed by a W2 line gives the correct `W2 line 4`. At 25,000 deep, the checker raises `RecursionError` and reports no (line, W). A core that stops parsing at depth 127 reports W14 line 3 instead, which is wrong by section 8.
- **Proposal:** either state that the parser must not recurse and must accept any depth for W2/W3, or move W14(c) into phase 2 ("the first line whose parse exceeds 126 levels"). Fix the checker's parser either way.

### G10 — MAJOR: ⟨n⟩ is unbounded in W2, and the document does not warn
- **Document:** ⟨n⟩ is "the digits 0–9, no sign, no leading zero" (draft:104). Range checks come later, in W1, W4, W8 and W13.
- **Evidence:** C4. The checker, with unbounded Python integers: `(perform 1234…890)` (30 digits) → `W4`; `(var 1234…890)` → `W8`; `(clause 1234…890 …)` → `W1`. A reader that parses into u64 reports W2, or panics.
- **Proposal:** say that W2 puts no length limit on ⟨n⟩, and that each later check compares it as a decimal of any length.

### G11 — MINOR: W14(c)'s derivation misstates one addition and is loose
- **Document:** draft:435-438: "A `not` above the condition … of a define's `unless` … [added after that check]"; "a path's length at most doubles".
- **Evidence:** the define's `unless` `not` is built by the parser (`syntax.py:670-672`) and counted (SPEC.md:634-635). No two consecutive parsed nodes can both be promoted (Q2).
- **Proposal:** correct the sentence. Keep 126 if wanted, but say that it is not tight. Add a plant at depth 127 and a fixture at depth 126.

### G12 — MINOR: when a cost counter grows
- **Document:** draft:235-239: "It grows by the operations counted while that clause's statement runs".
- **Evidence:** SPEC.md:254-255 says "afterwards". C8: a claim inside its certificate clause's body reads 0 (`claim 0 4 2 2 0 2 0`), while the claim after it reads 12. A live counter gives another receipt.
- **Proposal:** "when the statement ends, its counter grows by ops − start; a claim inside the clause reads the counter as it was before". Add C8 as a worked example.

### G13 — MINOR: section 10's gaps
The items of Q4, 1–5: an order of outcomes (usage, then reading LAW, then load checks, then the run); whether a TRACE with zero events is created; the line of a missing final LF; duplicate paths; and `--budget` as a path. Also say that `<reason>` holds no LF.

### G14 — MINOR: section 5a's gaps
- Add rows for `and` and `or` (short-circuit; counted after the left operand) and for `not`.
- State that `as` is 0 and `rounded` is 1.
- Say that `x_as_i` and `f_as_i` are named by this document, not by RUNTIME-SPEC §2.
- §0 (draft:57) calls the operation names "RUNTIME-SPEC §2–§3's function names", but `sha256` is not one.

### G15 — MINOR: derivation 19 has no usable vector, and its citation is wrong
- **Document:** draft:300, "SPEC §9 gives one worked value, all zeros".
- **Evidence:** the value is at SPEC.md:672, in §14, not §9. All zeros cannot detect a wrong bit order (C16 gives `babab-babab-babab-babab`).
- **Proposal:** give a nonzero worked value. For example, the empty law's seal `91e3deb3c796c4742eb2a12ca5e20e157fdfc172d2bf25237803d58c1f28e0f5` gives the words `nalog-tupug-sivik-siduh` (C16).

### G16 — MINOR: the author cannot identify the supplementary file, and has no worked run
The sha256 (`2bff1c69…`) and the counts of `vectors-as-integer.txt` are only in the manifest, outside the reading set (draft:27-28). Put them in §0. RUNTIME-SPEC §9's event-chain check values come from `src/check_chain.py` (RUNTIME-SPEC.md:213-214), also outside the reading set. Consider one worked law → receipt and trace.

### G17 — MINOR: traceability to ruling 2 was dropped
Draft 0's section 6 named the analysis fields (`Program.top`, `Analysis.vars`, `Analysis.rule_types`, `VarInfo.top`), and its status quoted ruling 2, which names them. Draft 1 drops both. Keep the mapping where the owner and re-readers can see it, in a column or an appendix the author need not read.

### G18 — MINOR: the new checks have no plants
Add plants for:
- W14(a) at 25 and W14(b) at 17;
- an id numbered in line order rather than walk order (F2);
- `(lit float …)` under `fixed` (F11);
- G1's T3 and T4;
- `\u{110000}`;
- `promote int` (G4);
- G5's missing arm;
- a `\u{0}` fixture.

### G19 — MINOR: wording
- Draft:89, "0, when k = 1 or the clause is top-level", is circular ("top-level" means parent 0). Write "0".
- W5's "each absorbed clause is named by exactly one arm or else of exactly one If" (draft:365) does not say which line a breach belongs to (see G8).

---

## Appendix: commands and outputs (all from `⟦HOME⟧\Desktop\Orlog`, Git Bash, `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B -c '…'`)

**C1:**
```
sha256sum research/rust-core/LAW-FORMAT-0-DRAFT-1.md
→ 8c277a1e6305e7301bc6316dde534f342fbe3c7b52bffb5ed4e135b056496a05 *research/rust-core/LAW-FORMAT-0-DRAFT-1.md
sha256sum research/rust-core/vectors-as-integer.txt research/rust-core/format_check.py research/rust-core/gen_as_int_vectors.py vectors/runtime-vectors.txt src/orlog/numeric_ref.py
→ 2bff1c69…ad2f, fa0a0c9b…5a64, abbbe310…6afc, 841240b7…f204, eacac3dd…bb64; wc -l vectors/runtime-vectors.txt → 20015
```

**C2:** reads `vectors-as-integer.txt` and re-evaluates each line with `numeric_ref.x_as_i`/`f_as_i` and with a copy of `interp.convert`'s `as int` branch:
```
bytes 21474 CR False ends LF True
lines 446
Counter({'f_as_i': 268, 'x_as_i': 178})
Counter({'!INEXACT-CONVERSION': 143, '!OVERFLOW': 40, '!NOT-FINITE': 6})
grammar fails 0 disagreements 0
```
Grep: `f_as_i f:C3E0000000000000 => i:-9223372036854775808`, `f_as_i f:43E0000000000000 => !OVERFLOW`, `x_as_i x:-9223372036854775808 => i:-2147483648`.

**C3:** a census of `vectors/runtime-vectors.txt`: 43 operation names; token prefixes `f i x b ! s hex`; `f:` uppercase, `hex:` lowercase.

**The checker harness used in C4, C5, C9–C12, C14 and C15:**
```
import sys; sys.path.insert(0,"research/rust-core"); import format_check as F
H=b"orlog-law 0\n(decimals fixed)\n"
def t(name,b):
  try: F.read(b); print(name,"-> ACCEPTED")
  except F.Refused as r: print(name,"-> refused W%d line %d: %s"%(r.w,r.line,r.why))
```
C5 and C14 also catch RecursionError and Exception.

**C4:**
```
T1 H+b"XYZ\n(clause 2 0 (say (str \"a\x01\")))\n"            -> refused W1 line 4: a byte outside 0x20-0x7E and LF
T2 H+b"XYZ\n(clause 2 0 (say (lit int 1)))"                    -> refused W1 line 4: no final LF
T2b b"orlog-law 1\n(decimals fixed)\n(clause 1 0 (say (lit int 1)))\n\x01\n" -> refused W1 line 4: a byte outside 0x20-0x7E and LF
T3 H+b"(clause 1 0 (define \"b\" (rule \"c\") - (over )))\n(clause 2 0 (define \"c\" (rule \"b\") - (over )))\n(clause 3 0 (say (rule \"b\")))\n" -> refused W10 line 3: rule 'c' used before its last define
T4 H+b"(clause 1 0 (define \"r\" (var 0) - (over )))\n(clause 2 0 (let 0 \"x\" (lit int 1)))\n(clause 3 0 (say (rule \"r\")))\n" -> refused W8 line 3: variable 0 used before it is declared
T6a (perform 123456789012345678901234567890)                  -> refused W4 line 5
T6b (var 123456789012345678901234567890)                      -> refused W8 line 3
T6c (clause 123456789012345678901234567890 0 ...)             -> refused W1 line 3
T7  (clause 1  0 (say (lit int 1)))                           -> refused W1 line 3: not a clause line
T7b (clause 01 0 ...)                                         -> refused W1 line 3: clause line 1 is numbered 01
T7c an If at clause 1, then (clause 2 0 absorbed )            -> refused W2 line 4: not one form
```

**C5:**
```
deep not 5000, then a W2 error on line 4  -> refused W2 line 4: not a canonical natural number: '01'
deep not 25000, then a W2 error on line 4 -> RecursionError (the checker crashed, no (line, W))
trailing space on a clause line           -> refused W1 line 3: not a clause line
leading space on a clause line            -> refused W1 line 3: not a clause line
space after ( of clause                   -> refused W1 line 3: not a clause line
parent with leading zero                  -> refused W1 line 4: a parent that is not a canonical number
```

**C6:** with `format_check` imported, so the recursion limit is 20000. The texts are built as in C7; each is run with `compile_bytes`, then `F.read(comp.law)`, then `Interp(...).run()`:
```
perform chain 200 | front end accepts | checker accepts | reference: COMPLETED ops 201
perform chain 600 | front end accepts | checker accepts | reference: COMPLETED ops 601
rule chain 200    | front end accepts | checker accepts | reference: COMPLETED ops 201
rule chain 600    | front end accepts | checker accepts | reference: COMPLETED ops 601
rule doubling 18, budget 10 | front end accepts | checker accepts | reference: HostStop STOPPED-BY-HOST after 393215 counted operations (budget 10)
```
The doubling texts are `§1 Define r1 as 1.`, `§k Define rk as the larger of r(k−1) and r(k−1).` for k = 2…18, then `§19 Say r18.` and `§20 Say 2.`.

**C7:** without importing `format_check`, so the recursion limit is 1000. Perform chains: `§1 To p1, do the following.`, `§1.1 Say 1.`, then for i ≥ 2 `§i To pi, do the following.` and `§i.1 Perform p(i−1).`, then `§(n+1) Perform pn.`. Rule chains: `§1 Define r1 as 1.`, then `§i Define ri as r(i−1).`, then `§(n+1) Say rn.`.
```
recursion limit 1000 3.14.5
perform chain 300  | front end accepts | reference: COMPLETED ops 301
perform chain 600  | front end accepts | reference: RecursionError
perform chain 3000 | front end accepts | reference: RecursionError
rule chain 300     | front end accepts | reference: COMPLETED ops 301
rule chain 600     | front end accepts | reference: RecursionError
rule chain 3000    | front end accepts | reference: RecursionError
```

**C8:** the text `§1 Let n be 0. §2 While n < 2, at most 5 times, do the following. §2.1 Increase n by 1. §2.2 We claim that true, by the certificate of §2. §3 We claim that true, by the certificate of §2.` The front end accepts it, the checker accepts it, and the reference's receipt includes `ops 14`, `claim 0 4 2 2 0 2 0` and `claim 1 5 1 1 0 2 12`.

**C9:**
```
(say (+ int (promote int (lit int 1)) (lit int 2)))       -> ACCEPTED; rewritten identical: True
(say (== bool (lit int 2) (promote int (lit int 2))))     -> ACCEPTED; rewritten identical: True
(promote bool …), (promote text …)                        -> refused W2
(+ fix (promote fix (lit fix 1)) (lit fix 2))             -> refused W9 line 3: a promote of fix
(set 0 - (promote int (lit int 2)))                       -> refused W9 line 4
```

**C10:**
```
inline if whose block re-walks an earlier body: (clause 1 0 (while 1 (lit bool 0))) (clause 2 1 (let 0 "a" (lit int 1))) (clause 3 0 (if (arm 3 (lit bool 1) (if (arm 3 (lit bool 1) (block 1)) -)) -)) -> refused W8 line 4: variable 0 declared twice
inline if with a block of its own clause -> refused W5 line 3: clause 1 has children and no body
absorbed named by two Ifs (clauses 1 and 3 both name 2) -> refused W5 line 5: absorbed clause 2 is named twice
(clause 1 0 (say (lit fix 5))) (clause 2 0 (decimals fixed)) -> refused W6 line 3: a decimal literal before the decimals clause
orphan absorbed after a chain with no else -> refused W5 line 4: absorbed clause 2 is in no If chain
```

**C11:** a first attempt with literal backslashes failed with a Python SyntaxError, because the shell had removed a backslash. The probe was repeated with backslashes built as `chr(92)`:
```
writer _q of NUL, U+0001, U+202E, U+10FFFF: "\u{0}" "\u{1}" "\u{202e}" "\u{10ffff}"
checker q of NUL: "\u{0}"
NUL as u{0} -> refused W2 line 3: a \u{h} with a leading zero
U+0001 -> ACCEPTED;  U+202E -> ACCEPTED;  U+10FFFF -> ACCEPTED
NUL in a let name -> refused W2 line 3: a \u{h} with a leading zero
u{00} -> refused W2 line 3: a \u{h} with a leading zero
```

**C12:**
```
two spaces before absorbed / space before ) after absorbed -> refused W2 line 4: not one form
promote int in < on ints -> ACCEPTED
claim premise naming itself -> ACCEPTED   (SPEC item 32 allows it)
empty law -> ACCEPTED;  empty input -> refused W1 line 1;  only header, no LF -> refused W1 line 1: no final LF
```

**C13:**
```
loops 16 top: front end accepts, checker ACCEPTED;  loops 17 top: LOOP-NESTING
loops 16 in procedure: accepts, checker ACCEPTED;   loops 17 in procedure: LOOP-NESTING
clause depth 24: accepts, checker ACCEPTED;          clause depth 25: NESTING-DEPTH
hand-made 25-deep clause bytes -> checker refused W14 line 27: a clause 25 deep
```

**C14:**
```
(clause 1 0 (let 0 "x" (lit int 1))) (clause 2 0 (if (arm 2 (lit bool 1) (say (var 0))) (else 99 (say (var 0))))) -> checker CRASHED: KeyError 99
(arm 99 (var 0) …) -> checker CRASHED: KeyError 99
(else 99 (perform 1)) -> checker CRASHED: KeyError 99
(else 99 (claim 0 (lit bool 1) (certificate 1) (given ))) -> refused W4 line 4
```

**C15:**
```
block naming an earlier while: (clause 3 0 (if (arm 3 (lit bool 1) (block 1)) -)) after a While at 1 with a let at 2 -> refused W8 line 4: variable 0 declared twice
two types for one rule (int at clause 1, bool at clause 2) -> refused W10 line 4
```

**C16:** `compile_bytes(b"")` gives the law `b'orlog-law 0\n(decimals fixed)\n'`, seal `91e3deb3c796c4742eb2a12ca5e20e157fdfc172d2bf25237803d58c1f28e0f5`, words `nalog-tupug-sivik-siduh`. `seal_words("00"*32)` gives `babab-babab-babab-babab`.

**Grep:** `grep -n -i "stack\|recurs" research/rust-core/LAW-FORMAT-0-DRAFT-1.md` finds only line 538 (Q1's text). `grep -n "babab" SPEC.md` finds only SPEC.md:672.
