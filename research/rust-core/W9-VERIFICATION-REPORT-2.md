> **A tokened copy, not the original hand-back** (2026-10-31, his ruling on REREAD-9's ASK 9-2): each spelling of the home folder's path is replaced by a token, `⟦HOME⟧` or `⟦HOME83⟧`; the original is kept outside the repository and named in `kept/TOKENED.txt` by its length and sha256, and `kept_tokens.py restore` gives it back exactly with the prefixes. After this line and the blank line below it, the file is the kept tokened bytes exactly, so its line numbers are the original's plus two.

# W9 re-verified against his rulings (A) to (D), the verifier's second report word for word (2026-10-31)

His ruling on the ruling sheet of 2026-10-31: *"I do not accept the checker under test as the authority for its own
correctness. The independent verifier's finding must remain the source of the discrepancy, and the corrected checker must
be independently checked against the amended wording."* The verifier of `W9-VERIFICATION-REPORT.md` was asked again: to
read the amended draft 9 and say whether it states each ruling exactly, to set its decider's switches to his rulings and
change nothing else, to run its sweeps against the corrected checker as a black box, never reading the checker's code,
and to bring back anything still ambiguous. It wrote only under its own scratch folder and changed nothing in the
repository.

Its report follows, unedited, taken from its own transcript rather than retyped.

---

## Re-verification of draft 9's W9 enumeration against the owner's rulings (A) to (D)

### 1. Verdict

**The checker and my decider agree on every law I ran: about 500,000 laws, with 0 disagreements (MEASURED).**
- The decider was set to the rulings: A none, B both, V met, and an id declared twice typed by the first declaration the walk meets.
- The checker was the amended one, used as a black box only.

**The amended text states (A), (B) and (D) exactly, and states (C) operationally without ambiguity (REASONED).** Four points are brought back for the owner, below as R1 to R4; a fifth, R5, decides no verdict. Of those four:
- one (R1) is whether the text states his (C) words exactly;
- one (R4) is a residue of (D) that the text does not decide.

**Of my earlier findings:**
- D4 and D6 are now stated correctly.
- D2 is corrected, with the caveat in R2.
- D5 is stated for `set` and `append`; the one residue (R5) decides no verdict.

### 2. The amended text, ruling by ruling

What I read: draft 9 sha256 `d86a2aeb…ce9793`, covering the status, section 6 (derivations 8, 16 and 17, and "Derivation 17, computed"), section 7, section 8 (the W9 table, "The four questions, ruled", the promote places, scope, the underived list) and section 11's new plants.

- **(A) is exact.** The `neg`, `abs`, `sqrt` row now has the two operand parts and "no part on ⟨type⟩ alone … needs none". The witness `(say (neg bool (rule "r")))` is given as W10 at line 3.
- **(B) is exact.** The comparison and `==`/`!=` rows now have one part of the pair: "one type, and it is numeric" (or numeric, bool or text), needing both operands.
  - My B=both implementation makes three parts together once both operands are derived: equality, and each operand's kind.
  - That conjunction is the same predicate as the draft's single part, so every verdict is the same (REASONED).
- **(C) is unambiguous as an operational rule.** The underived list now says: "A variable is undeclared at a use when the walk has not met its declaration by the clause the use is checked at". Derivation 8 points to it.
  - Every case where it can show is a rule used on a line before its first define (REASONED in the first report). In every such case the rule decides one outcome.
  - The draft's two (C) witnesses match my V1 (W10 at line 3) and V2 (W9 at line 3).
- **(D) is exact for an id written twice.** Derivation 8: "an id declared twice keeps the type of the first declaration the walk meets". The witnesses match my V3 (W9) and V4 (W10), and walk order is followed (V7, W9).
- **D2 is corrected.** Derivation 17 now says a type that would come round a cycle "through a variable as through rules, is underived: it is the least fixed point", noted as corrected after D2.
- **D4 is correct.** The promote row: "where it stands at none of the three places, nothing, and the part fails".
- **D6 is correct.** The conversion row: "allows for the conversion (`as` or `rounded`) and the target".
- **D5 is correct for `set` and `append`.** The indexed `set` value part and the `append` value part are "made only when the variable is a list". `change` takes the value part through "as for `set`".

**Brought back:**

- **R1, (C) and the word "scope".** His words, as the draft quotes them: *"Variable typing follows the variable's declaration and scope as encountered by the prescribed walk."*
  - The draft's rule leaves scope out entirely. Its second (C) plant pins that: a variable met earlier but never in scope (an inline `let`) is typed, giving W9 at line 3.
  - If "and scope" is meant to enter typing, that plant would be W10 at line 3 (scope and walk-order together).
  - Witness V2:
    ```
    orlog-law 0
    (decimals fixed)
    (clause 1 0 (say (neg fix (rule "q"))))
    (clause 2 0 (if (arm 2 (lit bool 1) (let 0 "y" (lit int 1))) -))
    (clause 3 0 (define "q" (var 0) - (over )))
    ```
    The checker gives W9 at line 3 (MEASURED).
  - Proposal: ask him to confirm that scope does not make an out-of-scope variable's type underived, then say so in the underived list.

- **R2, derivation 17's least fixed point against his words.** Derivation 17 now states the combined typing's cycles as a least fixed point, reached "within one walk more than there are rules". His words: *"The variable convention does not establish a general order-free or least-fixed-point typing system."*
  - The two can be read together: one is D2's cycle rule, the other is about the convention.
  - But a reader could take derivation 17's sentence as the very thing he says is not established.
  - The verdict is not in question. Under (C) with E2, a cycle through a variable still arises, since y is met before the define:
    ```
    orlog-law 0
    (decimals fixed)
    (clause 1 0 (say (neg fix (rule "q"))))
    (clause 2 0 (let 0 "y" (rule "q")))
    (clause 3 0 (define "q" (var 0) - (over )))
    ```
    The checker gives W10 at line 3, and so does my decider (MEASURED).
  - Proposal: he confirms that D2's sentence stands with his ruling, or it is reworded to name only the cycle's result (underived).

- **R3, a note on the 83 mutants.**
  - The draft's parenthesis says a first attempt at the literal reading (i) "never settled on 83 of R6's 10,000 mutants".
  - The literal reading need not fail to settle (REASONED). Under the least-fixed-point formulation that derivation 17 itself now states, reading (i) is monotone, since each type comes "from at most one other rule's type". So it settles within one walk more than there are typed nodes.
  - My decider implements (i) that way and asserts settling. It settled on every law I ran under V=any: 300,000 random laws, the 168,596-law sweep, and the rest (MEASURED). I did not run R6's mutants.
  - So the 83 measure that attempt's formulation ("typed by its declaration in the last walk"). This does not touch his ruling, which stands. It bears only on whether the parenthesis describes the evidence exactly, and on his clause "without a separately specified termination and fixed-point contract".

- **R4, (D)'s residue: a misnumbered declaration.**
  - Derivation 8 speaks of written ids. Section 7 says "the i-th declaration the walk meets has id i … a repeated or misnumbered one included", and derivation 16 lists "ids 0…m−1 in the order the walk … meets their declarations".
  - The text does not say whether the second `let 0`, which is the second declaration met, declares variable 1.
  - Witness V6:
    ```
    orlog-law 0
    (decimals fixed)
    (clause 1 0 (say (neg int (rule "q"))))
    (clause 2 0 (let 0 "y" (lit int 1)))
    (clause 3 0 (let 0 "z" (lit fix 1)))
    (clause 4 0 (define "q" (var 1) - (over )))
    ```
  - The checker gives W10 at line 3: written ids, so variable 1 is undeclared (MEASURED). Reading the second `let` as variable 1 would make q fix, and give W9 at line 3.
  - Proposal: derivation 8 says which.

- **R5, no verdict depends on it.** The `change` row's "the slot's type (the variable's, or its element's) is numeric", needing the variable's type, does not say whether it is made for an indexed `change` on a variable that is not a list. "The variable is a list" fails on the same line, so the verdict is W9 either way (REASONED). Optional wording.

### 3. Re-runs at the ruled switches (A none, B both, V met, first declaration)

The decider's code is unchanged: sha256 `3dfef0d3…19ca`, the file the first report ran. Only the switch values passed by the drivers changed. The checker is sha256 `2965ed15…279c`; it and the draft were unchanged before and after the runs (MEASURED by hash).

| run | laws | ruled reading agrees | the readings not chosen, for contrast |
|---|---|---|---|
| targeted (every table row; my hand expectations against my decider: 0 mismatches) | 258 | 258 | (form, alone) 249; (none, alone) 254; (form, both) 253 |
| exhaustive sweep | 168,596 | 168,596 | (form, alone, met) 168,092; (none, alone, met) 168,164; (form, both, met) 168,524. The 72 A laws and 432 B laws now all give W10 |
| D1 sweep: first defines reading a variable at 10 kinds of place | 2,970 | V=met 2,970 | V=any 2,333; V=scope 2,333 |
| floats mode | 2,379 | 2,379 | |
| random, seeds 0 to 299,999 | 300,000 | 300,000 | (form, alone, met) 299,811; (none, alone, met) 299,861; (form, both, met) 299,948; (none, both, any) 299,098; (none, both, scope) 299,277 |
| first report's extra probes | 28 | 28 | |
| the draft's own (A) to (D) witnesses and the probes above | 18 | 18 | |

- **Sweep verdicts from the checker:** ok 948, W9 162,613, W10 5,035.
- **Random verdicts from the checker:** ok 130,139, W9 113,771, W10 56,090.
- **Every form occurs.** Every form in the table appears in at least 5,074 random laws, and every law agrees.
- **No checker exception, and no verdict outside ok, W9 and W10.**

### 4. Disagreements

**None.** The checker against my decider at the ruled switches: 0 in every run above (MEASURED).

### 5. Independence and conduct

- **Independence.** I have not read any part of `research/rust-core/format_check.py`: not before, and not now that it has changed. That includes its typing code, and I did not diff it. I used only `fc.read` and `fc.Refused` (`.w`, `.line`).
- **What I read.** Only draft 9. I did not read `RULINGS.md`, or anything under `research/law-sufficiency/`.
- **Git.** I ran `git status` once, restricted to the paths of the two files.
- **Processes.** One process at a time, and none failed to start.
- **Repository.** Nothing in it was written.

### 6. Files

All in `⟦HOME83⟧\AppData\Local\Temp\w9verify\`.
- **New this round:** `minimal3.py`, `extra_ruled.py`, `r2_sweep_rest.json`, `r2_sweep_binary.json`, `r2_random_A.json`, `r2_random_B.json`, and `w9decide.at-first-report.py.txt` (a copy of the unchanged decider).
- **Drivers changed (switches only):** `run_targeted.py`, `run_random.py`, `run_sweep.py`, `run_fwd.py`, `run_floats.py`.
- **Kept:** the first round's JSON files.

### Appendix: commands and outputs

Every command was run from `⟦HOME⟧\Desktop\Orlog` with the prefix `TEMP="$W" TMP="$W" PYTHONHASHSEED=0 PYTHONUTF8=1 python -B`, where `W='⟦HOME83⟧\AppData\Local\Temp\w9verify'`.

- `run_targeted.py`: `cases 258; decider-vs-hand mismatches 0`; `A=none B=both V=met: 258 of 258`.
- `run_sweep.py r2_sweep_rest.json <24 families>`: `laws 30212 in 37.9s; errors 0; other W {}`; TOTAL none/both/met `30212`.
- `run_sweep.py r2_sweep_binary.json binary`: `laws 138384 in 173.3s; errors 0; other W {}`; none/both/met `138384`.
- `run_fwd.py`: `laws 2970`; `V=any 2333`, `V=met 2970`, `V=scope 2333`.
- `run_floats.py`: `floats mode: compared 2379, agree 2379, other {}`.
- `run_random.py 0 150000 r2_random_A.json`: `compared 150000 of 150000 in 185.2s; {'W9': 56815, 'ok': 65015, 'W10': 28170}; other W {}; errors 0`; `A=none B=both V=met agrees on 150000 of 150000`.
- `run_random.py 150000 150000 r2_random_B.json`: `compared 150000 of 150000 in 185.2s; {'ok': 65124, 'W9': 56956, 'W10': 27920}`; `A=none B=both V=met agrees on 150000 of 150000`.
- `extra_ruled.py`: `extra probes at the ruled switches: 28, checker vs decider disagreements 0`.
- `minimal3.py`: `disagreements checker vs decider: 0 of 18`. It includes:
  - (A) W10 at 3; (B) W10 at 3 and W10 at 4;
  - (C) V1 W10 at 3, V2 W9 at 3; (D) V3 W9 at 3, V4 W10 at 3, V7 W9 at 3;
  - V6 W10 at 3; C1 and C2 W10 at 3, C3 W9 at 3;
  - P1 W9 at 3, P2 W10 at 3;
  - the three D5 laws W9 at 4.
- The class lines `run_random.py` prints still carry the label "decider(form,alone)". That label is stale: it is the first reading listed, which is now the ruled one.

**Grades.** Runs and hashes: MEASURED, here. Equivalences and the text analysis: REASONED. What the draft states: DECLARED.
