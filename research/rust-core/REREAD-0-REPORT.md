# REREAD-0: the independent re-read of LAW-FORMAT-0, its report word for word (2026-10-30)

Saved as returned by the re-reader: a fresh general-purpose agent with no part in writing the document. Its brief:
- read LAW-FORMAT-0.md (sha256 `1ae57ee8…`), SPEC.md, RUNTIME-SPEC.md, and for faithfulness `src/orlog/sema.py`,
  `interp.py`, `syntax.py`, and `numeric_ref.py` for Q1 only;
- never open `research/law-sufficiency/`, nor any file of `research/rust-core/` but the draft;
- run, edit and create nothing;
- answer Q1–Q6 with evidence and list its findings by severity.

Its report follows, unedited. The only change is that the leading indentation the hand-back added to every line is
removed.

---

LAW-FORMAT-0.md read: sha256 `1ae57ee8d196a743e6d8571995eba4e7744942be7f6c74d7d98ec7d83ca60c50` (equal to the brief's).

# Independent re-read of LAW-FORMAT-0 (draft of 2026-10-30)

**What I read.** All of `research/rust-core/LAW-FORMAT-0.md`, `SPEC.md`, `RUNTIME-SPEC.md`, `src/orlog/sema.py`, `interp.py`, `syntax.py` and `numeric_ref.py`. To settle particular points I also read `front.py`, `canon.py`, `seal.py`, `lower.py`, and searched `gen_c.py`, `gen_rs.py` and `gen_py.py` for every field they read. I counted the vector file's operation names. I ran nothing except `sha256sum`, `grep` and that count, and I wrote no file. I did not open `research/law-sufficiency/`, nor anything under `research/rust-core/` other than the draft.

**What I could not check.** I did not check the evidence in the *held by* column, the checker (`format_check.py`), or whether the 298-law corpus contains the shapes named below. All three would need files I may not read, or code I may not run.

**Verdict.** The draft is not ready to hand to a clean-room author.
- One BLOCKER (F1): W1 accepts bytes that crash at run time.
- Nine MAJOR findings:
  - The id order is stated ambiguously; read the plain way, it refuses valid laws.
  - Five checks are looser than the front end: depth, promote placement, string code points, If-chain shapes and the budget check.
  - The run interface leaves outcomes open.
  - The numeric definition rests on a file the author may not read.
- Nine MINOR findings.

On the other questions:
- **Section 9.** The writer's forms match `sema.py` character for character (Q5).
- **Section 6.** 16 of the 18 derivations are right; derivations 8 and 16 need rewording.

---

## Q1. Can every numeric function be written from RUNTIME-SPEC §2–§3 and the vectors alone?

**For substance, almost.**

I checked RUNTIME-SPEC §2–§3 against `numeric_ref.py` function by function and found no disagreement:
- `i_div`'s order, DIVISION-BY-ZERO, then INEXACT-DIVISION, then OVERFLOW, is at RUNTIME-SPEC.md:46 and numeric_ref.py:73-79.
- `i_quot` and `i_rem` (RUNTIME-SPEC.md:47, 80; numeric_ref.py:82-100). The vectors hold `i_quot i:-9223372036854775808 i:-1 => !OVERFLOW` and `i_rem … => i:0`.
- `f_to_x` refuses NOT-FINITE, then INEXACT-CONVERSION, then OVERFLOW (RUNTIME-SPEC.md:58; numeric_ref.py:230-237). An inexact `x·2³²` needs `|x| < 2²¹`, so INEXACT-CONVERSION and OVERFLOW never compete.
- `f_trunc` and `f_round` refuse NOT-FINITE, then OVERFLOW.
- Canonical NaN, and `f_max`/`f_min` by comparison.
- Fix arithmetic with half-even rounding.
- The printing rules (RUNTIME-SPEC.md:89-99; numeric_ref.py:241-275).

**The gaps.** These are the places where the author must guess, or rely on the one file he may not read:
1. **The authority sentence.** SPEC.md:4-5 says *"Numeric meaning is defined by `src/orlog/numeric_ref.py`"*. SPEC.md:269 says *"RUNTIME-SPEC §2 and numeric_ref.py, with the order of refusal tests stated there"*. RUNTIME-SPEC.md:7 says *"Where this text and `numeric_ref.py` disagree, `numeric_ref.py` is the definition"*. Under D1 the author cannot detect such a disagreement. Nothing tells him that, for him, the prose and the vectors are the whole definition. (F9)
2. **`as an integer`** is `x_as_i` and `f_as_i`.
   - It is absent from RUNTIME-SPEC's table (lines 42-65).
   - The vector census has 44 operation names and none for it. `lower.py:27` and `lower.py:376` call both functions.
   - Only SPEC §8 prose defines it (SPEC.md:273-275): NOT-FINITE, then INEXACT-CONVERSION, then OVERFLOW. That prose is enough, but nothing tests it.
   - interp.py:403-414 implements it inline, which matches.
3. **Which function each conversion and promotion calls is never tabulated.** The mapping is in interp.py:400-421 and lower.py:367-386:
   - `promote fix` is `x_from_i`, which refuses OVERFLOW for `|n| ≥ 2³¹`. SPEC item 40 (SPEC.md:379) states only the Float case, and OVERFLOW on a promotion appears nowhere in prose.
   - `as a fixed` and `rounded to a fixed` from an Int are both `x_from_i`, with no rounding mode.
   - `as`/`rounded` to Float and to Fix pass `rounded = 0/1`.
4. **Comparisons.** Only `f_lt` and `f_eq` are named and have vectors (RUNTIME-SPEC.md:79, 86).
   - On Float, `<=`, `>=`, `>` and `!=` must be the native IEEE ones. They cannot be derived by negation, since `a <= b` is not `not (b < a)` for a NaN. Only SPEC.md:126-127 hints at this.
   - Fix compares raw values, and Text equality is byte equality. interp.py:327-338 uses Python's native comparisons. Neither rule is stated.
   - `zero`, `positive` and `negative` are covered by SPEC.md:390.
5. **Seal words have no vector.** SPEC.md:288-289 plus the zero case at SPEC.md:672 (`babab-babab-babab-babab`) suffice, and match seal.py:24-32.

---

## Q2. Is any W check stricter or looser than the front end?

### Stricter (it would refuse a law the front end accepts)

**(a) The order of ids, under its plain reading (F2).** Derivation 16 says *"ids 0…m−1 in clause order and, within a clause, in the order the statement writes them"*. Obligation 3 says the same for claims and musts. W8 enforces the order.

The front end numbers ids in its walk (sema.py:97, `len(self.vars)` at `declare`). That walk visits an If's arm 1 body, the block's clauses included, before the absorbed else (sema.py:158-163). The writer, though, puts the absorbed clause's inline statement in the If's own line (syntax.py:275-281, sema.py:563-565).

The text
```
§1 If true, do the following.
§1.1 Let a be 1.
§2 Otherwise, let b be 2.
```
is accepted, and becomes
```
(clause 1 0 (if (arm 1 (lit bool 1) (block 1)) (else 3 (let 1 "b" (lit int 2)))))
(clause 2 1 (let 0 "a" (lit int 1)))
(clause 3 0 absorbed)
```
Variable 1 is written on line 1, before variable 0 on line 2. If "in clause order … within a clause" means by line, W8 refuses this valid law. The same holds for claims: put `We claim that true` in both places. It also holds for W12's *"before the claim's clause"*: a certificate of §1.1 from a claim inline in §2 is accepted by the front end (sema.py:217 compares with the arm's clause), but refused if "the claim's clause" is the If's line.

The order holds only if every "clause" means section 5's *clause of a statement*. For W10 and W11 the difference cannot arise: defines and procedures are top-level, so no top-level clause stands between an If and its absorbed siblings or inside a body.

**(b) The empty law (F12).** The front end accepts a text with no clause: canon.py:124 gives `""`, syntax.py:174-264 refuses nothing, and the law is `orlog-law 0\n(decimals fixed)\n`. W1's *"the clause lines numbered 1…n"* never says that n may be 0.

**Checks I found equal to the front end:**

| check | front end |
|---|---|
| W5's children and block rules | `_check_children`, syntax.py:307-318 |
| W6 | sema.py:72-75, 181-182, 263-267 |
| W9's operator rules | sema.py:382-472 |
| W10 | sema.py:230-250, 374-378, 476-493 |
| W11 | sema.py:200-205 |
| W12 | sema.py:214-229 |
| W13 | sema.py:167, 330-363 |

### Looser (bytes no typed law can have are accepted and run)

The draft claims (LAW-FORMAT-0.md:213-214): *"A byte string that passes all of them is the image of a typed law, as far as running it goes."* It is false, by these counterexamples:

- **F1, BLOCKER: the clauses need not be a pre-order of their tree.** W1 asks only for *"a parent of 0 or an earlier clause"*. The front end's numbering forces the parent of clause k to be 0, k−1 or an ancestor of k−1 (syntax.py:162-171, 231-242). These bytes pass W1–W13:
  ```
  orlog-law 0
  (decimals fixed)
  (clause 1 0 (while 1 (lit bool 1)))
  (clause 2 0 (let 0 "x" (lit int 1)))
  (clause 3 1 (say (var 0)))
  ```
  W8's scope rule says *"A `let` in a top-level clause is visible to every later clause"* (line 262), and clause 3 is later than clause 2. At run time, clause 3 runs inside clause 1's While, before clause 2. It reads an unassigned variable: a crash (interp.py:307, KeyError). No text has this tree: label 1.1 cannot follow 2.
- **F3: no depth bound.** NESTING-DEPTH (24 label parts), LOOP-NESTING (16) and EXPRESSION-DEPTH (nesting 24, tree depth 64) have no W check (syntax.py:74-76, 228-230, 412-414; sema.py:18, 271-275). Bytes of any depth pass, and can exhaust a recursive reader's stack.
- **F4: `promote` where the front end never puts one.** For example `(let 0 "x" (promote fix (lit int 1)))`, or `(+ fix (promote fix (lit int 1)) (promote fix (lit int 2)))`.
- **F5: ⟨str⟩ may hold code points that are not scalar values,** such as `(str "\u{d800}")` or `"\u{110000}"`, and characters the door refuses in literals.
- **F6: If chains no text can write.** For example `(if (arm 1 E (block 1)) (else 1 S))`, or `(if (arm 1 E S) (arm 2 E S) (else 1 S))`.
- **F11:** a `(lit float …)` under `(decimals fixed)`, if W6 is not read to include derivation "Decimals"'s second sentence.

The names (REDECLARED, PROCEDURE-NAME) are left unchecked by design (lines 271-274). That choice is stated, so I do not count it as a defect, except for the wording in F14.

---

## Q3. Are the derivations determined by the bytes, correctly stated, and complete?

**Correct as stated, each against the code:**

| # | derivation | code |
|---|---|---|
| 1, 2 | the top, children | syntax.py:235-243 |
| 3 | cost-tracked clauses | sema.py:219 |
| 4 | the rules | sema.py:71-75 |
| 5 | the overrides | sema.py:476-493, and as used in interp.py:433 |
| 6, 7 | the claim sites and their clauses | sema.py:36, 210-213; for inline claims the `c` is the arm's clause, sema.py:159-163 |
| 9 | a change's element type | sema.py:147-155 |
| 10–15 | expression types | sema.py:324-472 |
| 17 | a rule's type | sema.py:243-248 |
| 18 | a variable's top | sema.py:97: `len(self.scopes) == 1` only for a top-level clause's own statement, since body() and block() push a scope, a procedure body pushes at least one, and a For pushes before declaring |

**Underdetermined or wrongly stated:**
- **16 (`Analysis.vars`).** The order is ambiguous, as Q2(a) shows (F2). `Analysis.vars` itself is fine, since it is in id order and the ids are written; the ambiguity bites in the W8 and obligation-3 check.
- **8.** *"a `let`'s variable: the type of its ⟨E⟩, unpromoted"*. "Unpromoted" invites a reader to strip a top-level `(promote …)`. That would give an Int variable holding a Fix value, if W9 lets such bytes through (F4, F15).

**Missing:** the seal words (F16).
- lower.py:309 emits `comp.seal_words` for `(seal)`, and the generators print them in their headers. interp.py:97 makes them from the law seal.
- They are a derivation from the bytes (SHA-256, then SPEC §9), not listed in section 6. The run interface section says the core computes the seal, but does not list the words.

**Nothing else is missing.** The interpreter reads `prog.top`, `c.absorbed`, `c.cost_tracked`, `c.children`, `s.var.{id,type}`, `s.elem`, `e.type` / `e.a.type` / `p.type`, `an.claims`, `an.rules`, `an.overrides` and the seal text. The backends add `an.vars`, `vi.top`, `an.rule_types` and `prog.clauses`' cost-tracked set (lower.py:42-62; gen_c.py:52, 287-293; gen_rs.py:56, 292-302). Each is either written in the bytes or in the list. `VarInfo.loop` is read only by sema, and is derivable as the For counter.

---

## Q4. Is section 5's table of which clause a statement runs as complete?

**What it lists is right:**
- A clause's own statement runs as the clause.
- An arm's condition and inline statement run as the arm's ⟨C⟩ (interp.py:212-216).
- An else's inline statement runs as the else's ⟨C⟩ (interp.py:217-218).
- A rule's provisos and values run as the use site (interp.py:423-440).

**Gaps:**
1. **Rule uses in conditions.** The bullet says *"the clause of the statement that uses the rule"*. A rule used in an absorbed arm's condition is used by the If statement, whose clause is the If's own. The code names the absorbed clause: interp.py:214 evaluates with `ac.id`. The bullet should say *the clause under which the use is evaluated (the bullets above)*. (F13)
2. **A performed body.** Its clauses run as their own ids, not as the performing clause (interp.py:242-244 runs `seq(s.proc.children)`). This is the opposite of a rule's provisos and values, and should be said. (F13)
3. **Cost counters.** A counter wraps a clause's statement only when that clause runs in a sequence (interp.py:132-141). So:
   - an If clause's counter covers every arm and the else, the absorbed arms' blocks included;
   - a performing clause's counter covers the body;
   - nested counted clauses grow too;
   - inline statements and absorbed clauses never have a counter of their own.
   SPEC §7 implies all this; the section claims to cover costs and does not say it. (F13)
4. **Where the host budget is checked.** The check is made at every `stmt` entry, before the early return for `define`, `procedure` and `decimals` (interp.py:149-154). It is never made for an absorbed clause (interp.py:134-135). (F7)

---

## Q5. Could two readers following sections 2–4 write different bytes?

**I found no divergence.** I compared every format string of the writer with the tables:

| piece | writer | document |
|---|---|---|
| header | sema.py:600-608 | `orlog-law 0` and `(decimals ⟨mode⟩)` |
| clause line | `(clause %d %d %s)` and `(clause %d %d absorbed)` | the same |
| statements | sema.py:551-597 | the same items, in the same order |
| expressions | sema.py:513-542 | the same |
| claims | sema.py:586: `(given %s)` with `" ".join` gives `(given )`; certificate `(certificate %d%s)` with `" " + _q(name)` | the same |
| defines | sema.py:589: `(over %s)` gives `(over )` | the same |
| string escapes | sema.py:497-506 | identical to the table at line 62 |
| type words | `_t()` gives `list-int`; conversions write `e.target` | the same |
| number formats | `%d`; Float as `%016x` of the bits from `struct.pack("<d")` read back as `"<Q"`, lowercase, most significant digit first | the same |

Items are ordered as the document gives them: `change` writes sign, variable, index, amount; `while` writes the bound then the condition; `item` and `append` write the variable first; arms come in `s.arms` order. Labels are written already canonical by `ref()` (syntax.py:396-401).

The only open point is reading, not writing: what `\u{h}` means for an h that is not a scalar value (F5).

---

## Q6. Other things a clean-room author would have to guess

- **Unstated outcomes of the run interface (F8):**
  - the exit status of a COMPLETED or REFUSED run (RUNTIME-SPEC.md:26-31 gives 0, but only for the runtimes);
  - what happens on a usage error, a malformed or uppercase TEXTSEAL, a malformed or missing `--budget`, an unreadable LAW, or an OUT that cannot be written;
  - whether `--budget` may come before TRACE, and what B's range is;
  - whether no `--budget` means unbounded;
  - what *"is not written"* means for an OUT already partly streamed. RUNTIME-SPEC §4 has `orl_say` write each line as it is said. Must the core buffer, delete or truncate? It is also unsaid for files that already exist when the law is refused.
  - which `W<k>` is reported when several checks fail, and what `<reason>` holds. W2 and W3 overlap: a non-canonical `\u{41}` breaks both.
- **The host stop before `define`, `procedure` and `decimals` clauses** (F7).
- **The core's build constraints** (std-only, no crates, its own SHA-256?). They live in RUST-CORE-0, which the author cannot read. (F17)
- **The vector file's grammar** (`i:` `x:` `f:` with uppercase bits, `b:`, `s:`, `hex:`, `!CODE`) is not described in RUNTIME-SPEC. It can be inferred. (F17)
- **Settled as far as I can tell:** the trace format and head (RUNTIME-SPEC §5), the receipt (§7), the seal words (SPEC §9), the TEXTSEAL as given, and the STOPPED-BY-HOST message (interp.py:38).

---

## Findings

### F1 — BLOCKER: W1 admits a clause order that is not the tree's pre-order
- **Document:** *"⟨parent⟩ is 0 for a top-level clause, or the id of an earlier clause"* (line 49); W1: *"a parent of 0 or an earlier clause"* (line 218). The scope rules (lines 262-269) and every "before" and "after" are phrased in clause order.
- **Evidence:** syntax.py:162-171 and 231-242: the parent of clause k is k−1, an ancestor of k−1, or none. The bytes in Q2 pass W1–W13 and read an unassigned variable at interp.py:307.
- **Proposal:** in W1, require the parent of clause k to be 0, k−1 or an ancestor of k−1. State that clause order is then document order and the tree's pre-order, so that labels are increasing.

### F2 — MAJOR: the order of variable, claim and must ids, and "the claim's clause", are ambiguous; under the plain reading W8 and W12 refuse valid laws
- **Document:** derivation 16 (line 181), obligation 3 (lines 203-206), W8 (line 225), W12 *"before the claim's clause"* (line 229), W10 *"stands after"* (line 227).
- **Evidence:** sema.py:97 and 158-163 (the walk order); syntax.py:275-281 and sema.py:563-565 (an absorbed clause's inline statement is written in the If's line); sema.py:217 (a certificate is compared with the arm's clause). The worked laws are in Q2(a).
- **Proposal:** define every "clause order" and "the clause of X" by section 5's clause of a statement (the arm's or else's ⟨C⟩), then written order within it. Equivalently, write out the walk: a clause's statement, an If's parts in written order (each arm's condition, then its body, inline or the block's clauses), then the clause's children. Add the two laws of Q2(a) as fixtures.

### F3 — MAJOR: no depth bounds; bytes of any depth pass, and a recursive reader can overflow its stack
- **Document:** lines 213-214 (*"the image of a typed law"*) and line 271 (*"What the front end checks and this list does not: the names"*).
- **Evidence:** syntax.py:74-76, 228-230 (NESTING-DEPTH), 341-343 and 412-414 (EXPRESSION-DEPTH); sema.py:18 and 271-275 (LOOP-NESTING); SPEC.md:414-418.
- **Proposal:** add a W14.
  - Clause depth ≤ 24, and loops nested ≤ 16 within one body. Both can be computed exactly from the bytes.
  - An expression-depth bound that every front-end law meets in its bytes. It cannot be the front end's 64 exactly: promotions are added after the check (each at most doubles a path), an Unless's `not` is added after the check (SPEC.md:634), parentheses vanish, and absorbed arms move into the If's line. Derive the bound and state it.
  - Or require a reader that does not recurse, and correct lines 213-214 and 271.

### F4 — MAJOR: W9 lets `(promote …)` stand where the front end never puts one
- **Document:** line 243 (*"`promote`: an int operand, with target fix or float"*); line 259 (*"Where SPEC §5 promotes an Int, the bytes hold the `(promote …)` form. A reader never promotes on its own."*), which states only one direction.
- **Evidence:** promotions come only from `unify` (one operand of an arithmetic or comparison operator whose other operand has the target type), from `fit` (the stored value of set, change and append), and from list-literal items when at least one item has the element type (sema.py:295-322, 460-472). A `let` stores its value unpromoted (sema.py:123-125). These pass W9 and have no text:
  - `(let 0 "x" (promote fix (lit int 1)))`
  - `(say (+ fix (promote fix (lit int 1)) (promote fix (lit int 2))))`
  - `(list list-fix (promote fix (lit int 1)))`
- **Proposal:** state the three places a promote may stand, exactly one per binary operator, and at least one unpromoted item per list literal. Refuse every other promote.

### F5 — MAJOR: ⟨str⟩ admits code points that are not scalar values, and characters the door refuses in literals
- **Document:** line 62 (*"every other character written `\u{h}`, where h is its code point"*); lines 66-67 (*"A text value at run time is the string's UTF-8 bytes"*).
- **Evidence:**
  - `\u{d800}` has no UTF-8 form. canon.py:76-80 decodes strictly, so no surrogate reaches a text.
  - `\u{110000}` and beyond are not code points.
  - The door refuses in literals: C0 controls (LF and tab among them), DEL, C1 controls, bidi controls, Zl and Zp, Cf other than ZWJ and ZWNJ, Hangul fillers, and the INVISIBLE set (canon.py:18-23, 229-230, 247-257).
- **Proposal:** require h to be a scalar value, at most 10FFFF and outside D800–DFFF, written in at most 6 digits. Then decide, and say, whether a text literal may hold the characters the door refuses. If it may not, list them. Note that the door's Cf test depends on Python's Unicode version. Apply the same rule to names.

### F6 — MAJOR: W5 admits If chains no text can write
- **Document:** W5 (line 222): *"the else's is the If's own clause with an inline body, or an absorbed clause … Each absorbed clause belongs to exactly one chain"*.
- **Evidence:**
  - A block `then` returns before any `;` (syntax.py:481-483). SPEC.md:520 rules *"`If true, do the following; otherwise say 2.`"* to be SYNTAX.
  - An inline else ends the chain (syntax.py:290-292), so a later Otherwise is ORPHAN-OTHERWISE (syntax.py:271-274).
  - Both `(if (arm 1 E (block 1)) (else 1 S))` and `(if (arm 1 E S) (arm 2 E S) (else 1 S))` pass W5, and their events carry clause ids no law emits. The rule also does not clearly forbid one absorbed clause named by two arms.
- **Proposal:** an else whose ⟨C⟩ is the If's own clause requires exactly one arm, with an inline body. Each absorbed clause is named by exactly one arm or else of exactly one If.

### F7 — MAJOR: the host budget's check positions are understated
- **Document:** line 155 (*"Not run in place: `define`, `procedure` and `decimals`"*); line 299 (*"Before each statement runs, including one in a body or inline"*).
- **Evidence:** interp.py:132-141 calls `stmt` for every non-absorbed clause. interp.py:151-154 checks the budget before returning for Define, ProcDef and Decimals.
  - Take `§1 Let x be 1. §2 Let y be 2. §3 Define r as 3.` with `--budget 1`. The reference stops at clause 3 (ops 2 > 1).
  - A reader that skips clauses that do nothing writes COMPLETED.
- **Proposal:** the check is made before every non-absorbed clause in a sequence, `define`, `procedure` and `decimals` included, and before every inline arm or else statement. It is never made for an absorbed clause or before a loop's iteration.

### F8 — MAJOR: the run interface leaves outcomes unspecified
- **Document:** lines 292-302.
- **Evidence:** RUNTIME-SPEC.md:26-31 (the runtimes' exit statuses), 110-112 (output is streamed), 166-176.
- **Unsaid:**
  - the exit status of a COMPLETED or REFUSED run;
  - usage errors, an uppercase or malformed TEXTSEAL, a malformed `--budget`, an unreadable LAW, an output that cannot be written;
  - argument order, and the default with no budget;
  - what "not written" means for files that exist or were opened, on a stop or a load refusal;
  - which `W<k>` is reported when several checks fail.
- **Proposal:** a table of every outcome, giving the files left, the exit status and the exact stderr. A precedence for `W<k>`: for example, the first failing line, and within it the lowest k. Separate W2 from W3 so that a non-canonical atom has a single code.

### F9 — MAJOR: the numeric definition is deferred to a file the author may not read
- **Document:** line 20 (*"the numeric functions and printing: RUNTIME-SPEC §2–§3"*).
- **Evidence:** SPEC.md:4-5 and 269; RUNTIME-SPEC.md:3-7 make `numeric_ref.py` the definition on any disagreement. There are no vectors for `x_as_i` or `f_as_i`, which lower.py:27 and 376 call.
- **Proposal:** state that, for the core, SPEC §8 plus RUNTIME-SPEC §2–§3 plus the vectors are the definition, and that a disagreement with `numeric_ref.py` is a finding. Add vectors for `as an integer`.

### F10 — MINOR: the conversion and comparison mapping is unwritten
- **Evidence:** interp.py:327-338 and 400-421; lower.py:367-386.
- **Proposal:** add a table giving the function and refusal order for each form × operand type:
  - promote fix → `x_from_i` (OVERFLOW);
  - promote float → `f_from_i`, exact;
  - `as` and `rounded` to fix from Int → `x_from_i`;
  - the comparisons `<=`, `>=`, `>`, `!=` on Float are native IEEE, not negations;
  - Fix compares raw values; Text equality is byte equality.

### F11 — MINOR: W6 does not plainly enforce the literals' mode
- **Document:** line 223 (*"Line 2's mode agrees with derivation 'Decimals'"*); line 192 (*"Every decimal literal is of that mode"*).
- **Evidence:** sema.py:337-359 makes each decimal literal by the current mode.
- **Proposal:** in W6, refuse `(lit float …)` under `fixed` and `(lit fix …)` under `floats`.

### F12 — MINOR: the empty law
- **Evidence:** canon.py:124 and syntax.py:174-264 accept a text with no clause; the law is two lines.
- **Proposal:** say that n ≥ 0, and give the two-line law.

### F13 — MINOR: section 5's table should state its rules for rule uses, performed bodies and costs
- **Document:** line 161 (*"the clause of the statement that uses the rule"*).
- **Evidence:** interp.py:214 (an arm's condition is evaluated under `ac.id`), 242-244 (performed bodies), 132-141 (cost wraps only clauses run in a sequence).
- **Proposal:** a rule use is evaluated under the clause the bullets above give. A performed body's clauses run as their own ids. The cost-counter coverage is as set out in Q4.

### F14 — MINOR: the names wording
- **Document:** lines 272-273 (*"The bytes keep the names (`let`, `procedure`, `define`), but no run reads them"*).
- **Evidence:** interp.py:425 and derivation 4 read define names: they group the defines and resolve `(rule ⟨str⟩)`.
- **Proposal:** say that rule names are compared for exact code-point equality, and that the other names are not read.

### F15 — MINOR: W9 and derivation-8 wording
- **Document:**
  - line 239: *"All four have ⟨type⟩ bool"*, of five predicates;
  - line 238: `not`'s ⟨type⟩ is not stated (it is bool, sema.py:407-410);
  - line 178: *"unpromoted"*.
- **Proposal:** "all five"; "`not`: a bool operand, ⟨type⟩ bool"; "the type of its ⟨E⟩ (never a promote, W9)".

### F16 — MINOR: the seal words are missing from section 6's derivations
- **Evidence:** lower.py:309; interp.py:97; SPEC.md:288-289.
- **Proposal:** add them as derivation 19, from the SHA-256 of the bytes read, by SPEC §9.

### F17 — MINOR: the context the author lacks
- **Evidence:** the draft cites RUST-CORE-0 and rulings D1, D3 and D5, which the author cannot read.
- **Proposal:** record here the core's build constraints, and the vector file's line grammar (RUNTIME-SPEC §9 says only what a harness does). Correct the over-claims at lines 213-214 and 271 once F1 and F3–F6 are settled.
