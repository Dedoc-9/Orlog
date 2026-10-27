# The adversary's outputs, rerun on the repaired tree (2026-10-26)

**Why.** Before the held push, the release check reran the manifold adversary's seven recorded outputs. Six no longer
reproduced. They record the attack on CUT-0's **first form**, before the repairs that the attack itself caused. Two
of the scripts also crashed on the repaired probes.

The owner asked that the historical records be kept and that current-tree evidence stand beside them. His words:
*"Do not present first-form results as if they were produced by the release candidate."*

**The first form** is the probes `probes/cut0_claims.py` and `probes/cut0_session.py` as they stood before the F1–F4
and G1–G7 repairs (`ADVERSARY.md`). That code was never committed, so no digest of it exists. What dates it: the
historical outputs were written between 14:09 and 14:16 on 2026-10-26, before the probes' last changes
(`cut0_session.py` 14:38, `cut0_claims.py` 15:05). Each current file names the sha256 of the two probes and of its own script. *Corrected 2026-10-26: this sentence had said "every module it ran". The other modules it ran (`cont_oracle.py`, `completeness_probe.py`, and `k_attacks.py`, `k_fuzz.py` or `k_repairs.py` where a script imports them) and `src/orlog` are those of the tree its Date line names, and no digest of them is recorded (`packets/E-release-gate.md`, risk 9).*

## The records, side by side

| output | historical record (first form) | current-tree rerun | twice |
|---|---|---|---|
| `k_attacks` | `k_attacks.txt`, 14:11 | `k_attacks-current.txt` | byte-identical |
| `k_criteria` | `k_criteria.txt`, 14:12 | `k_criteria-current.txt` | byte-identical |
| `k_repairs` | `k_repairs.txt`, 14:09 | `k_repairs-current.txt` | byte-identical |
| `s_attacks` | `s_attacks.txt`, 14:10 | `s_attacks-current.txt` | byte-identical |
| `k_fuzz-20000` | `k_fuzz-20000.txt`, 14:15 | `k_fuzz-20000-current.txt` | identical but for the seconds printed |
| `k_monotone-20000` | `k_monotone-20000.txt`, 14:14 | `k_monotone-20000-current.txt` | identical but for the seconds printed |
| `s_drop` | `s_drop.txt`, 14:16 | (none needed) | reproduces the record byte for byte, headers aside |

## Each change, tied to its repair

**How a change is tied.** A **plant** puts one first-form defect back into today's probe, through the probe's own
`PLANT` switch, and reruns the script. When the old outcome returns, that repair accounts for the change. **Reading**
means the tie rests on the code alone.

| change (historical → current) | repair | tied by |
|---|---|---|
| `k_fuzz`: 26 S2 counterexamples, each a spent While bit → 0 | F1 (reading S2 everywhere) | **plant `while-bit`:** the rerun reproduces the record but for one descriptor line |
| `k_monotone`: 578 points missing part of K at the cut → 0 | F1 | **plant `while-bit`:** the record but for one descriptor line |
| `k_attacks`: 3 claims unsound under S2 → withheld; A26 and A27 read alike | F1 | **plant `while-bit`:** the summary returns to "3 unsound under S2" |
| `k_attacks`: 1 candidate imprecision (A09's kind) → held | F3 (the refused arm onward) | **plant `all-arms`:** the summary returns to "1 candidate imprecisions" |
| `k_criteria`, `k_attacks`: the open claim's mark `!` → `!id` | F2 (the open claim named by its id) | **plant `descriptor-no-id`:** `k_criteria` reproduces its record byte for byte |
| the descriptor's printed form: a While as `w` (not `.` or `+`); a refused If as `?n` | the print format since S2 and F3 | **reading** `descriptor()` in `probes/cut0_claims.py`. A print format has no plant |
| `k_repairs`: every comparison now agrees; the host-stop equivalence's "different 1" → 0 | F1–F4, now in the probe | **reading:** the script measures each repair against "the probe as it stands", which is now the repaired probe. F4 is the budget check at a loop's entry |
| `s_attacks`: `door(b'1\n')` accepted → refused INPUT-SYNTAX | G2 (the door matches whole) | **plant `door-dollar`:** the record's line returns |
| `s_attacks`: edits accepted outside A2's image, 20 → 0 | G3 (A2's end cause is INPUT-MISSING only) | **plant `a1-cause-under-a2`:** such edits are accepted again (12, over today's smaller set of 13 logs) |
| `s_attacks`: the session record of the alice/mallory history, `f7a00f9d96f96d1c` → `b1a31a93fc26015c` | G5 (the source in the history) | **plant `no-source`:** the record hashes to `f7a00f9d96f96d1c` again |
| `s_attacks`: the projection `t 1 ` → `t 1`, and `check_run` no longer fails `projection-parses` | G1 (no trailing space with no each-tick port) | **reading** `serialize` in `probes/cut0_session.py`. G1 has no plant |
| `s_attacks`: the plant row `no-value-invented` now caught by `hold-previous` | G4's row, added after the attack | **reading** the probe's rows |
| `s_attacks`: section 7's history, legal then → refused RUN-REFUSED | G6 (only the end after the run refused) | **reading;** the script's fix below |
| `s_attacks`, sections 1 and 5: the domains' sizes (102,383 → 102,323 histories; 214,429 → 187,556; distinct logs 16 → 14 and 21 → 13; hold-previous's failures 1,062 → 354) | several G repairs at once | **not tied to one repair.** Ten of the session probe's thirteen plants were tried alone on section 1's domains, and none restores the old sizes, since the first form differed in several rules at once. Not tried: `budget-uncounted`, `lenient-hex` and `record-without-history`. In both runs every row holds ("rows failed: none"), so what moved is the set of legal histories, not a check |

## The scripts' three changes

Each change is dated in its file. Each is a compatibility change with the repaired probes, and none changes what a
check measures:
- **`k_monotone.py`:** its snapshot frame gains `"arm": None`, the value the probe's own `CutInterp` gives a frame at
  a statement's entry. Without it, the F3 repair's `continuation()` raised `KeyError`.
- **`k_repairs.py`:** a case that requires a reading per claim (A23 and A23′, added to the probe after the attack) is
  compared claim by claim. Before, the first claim was compared with the whole table and always read DIFFERS. The
  script's label "the probe's 13 cases" is the adversary's text, left as written; the probe now has 19.
- **`s_attacks.py`:** section 7 reports the session model's refusal (RUN-REFUSED, the G6 repair) instead of raising.
  The crash had also printed the checkout's absolute path in its traceback.

**Does not show:**
- that the first form behaved as the historical outputs say beyond what they print. Its code is gone, and the plants
  reinstate one defect at a time, not the whole first form;
- the domain sizes' exact decomposition by repair (the last row above).
