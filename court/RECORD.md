# The first court of ØRLǪG (2026-10-25): record and dispositions

## Parties
- **The record under trial:** DOCTRINE edition 1, and the code it described.
- **Logic prosecution:** `prosecution-logic.md`. Findings L1–L20 (4 FATAL), and ten points it tried and found sound
  (S1–S10).
- **Novelty prosecution:** `prosecution-novelty.md`. Findings N1–N25: 4 DEFEATS, 18 NARROWS, 3 NO-PRIOR-ART-FOUND.
- **Engineering red team:** `redteam-eng/`. Reproducers E1–E22. Its written findings arrive separately; the
  reproducers were processed directly. *(Note, 2026-10-25: the written findings are `redteam-eng/FINDINGS.md`, E1–E26.
  They arrived after this record, whose second round is still to be written.)*
- **Clean-room twin:** `../twin/NOTES.md`. An interpreter written from SPEC.md and RUNTIME-SPEC.md, and its 62 notes on
  ambiguity. *(Corrected 2026-10-25, prosecutor F8: this line called the twin "an independent interpreter written from
  SPEC.md alone". It imports the reference's `numeric_ref.py` and `seal.py`, so its agreement on numbers and seals is
  shared code; it is independent of the reference's code path, not of the specification or its author.)*
- **Defence:** none was needed. No finding was rebutted: each was conceded, repaired, or both.
- **Judge:** the court engine. `judge.py` decides `record.json`, written by `build_record.py`, under Dung's grounded
  semantics. The verdict is in `VERDICT.txt`.

## Verdict (computed)
- **13 doctrine claims IN, 21 OUT, 0 UNDECIDED.**
- **OUT:** every edition-1 claim that was attacked (T0–T4, T6–T9, P1–P5, NF, the section claims, and the
  implementation claim).
- **IN:**
  - edition 1's T5 (determinism by construction), unattacked;
  - the 12 narrowed edition-2 claims, unattacked as the record stands.
- **What IN means.** Standing under the record as written, not truth. An edition-2 claim falls the moment a finding
  that still applies to it is entered.

## Dispositions

| finding | severity | disposition |
|---|---|---|
| L1 | IMPRECISION | §0 rewritten. Löb is an analogy; Montague's hypotheses are stated; Aumann is context. |
| L2 | OVERREACH | T0 rewritten. No theorem is instantiated; intent is what cannot be computed. |
| L3 | FATAL | T1 rebased on certifying algorithms and LCF. The Artemov answer to Löb is withdrawn. |
| L4 | OVERREACH | **Repaired.** Grounding binds to the claim's own seal. Theorem names ground nothing (rows). |
| L5 | OVERREACH | **Repaired.** Plant `court-grounds-computation`, with an agreement and computation fixture. R3 is restated as a label. |
| L6 | FATAL | T3 rewritten as a counted reading. Unit cost is admitted. Little-oh is withdrawn. |
| L7 | OVERREACH | **Repaired.** NOT CHEAPER and CLAUSE NOT RUN replace RECOMPUTATION. The attribution is fixed. |
| L8 | OVERREACH | **Repaired.** D2 is a row, and stays UNGROUNDED. Dead plant wiring is removed from R4. |
| L9 | IMPRECISION | T4 and R6 corrected: CIRCULAR "rests on a cycle". |
| L10 | OVERREACH | **Repaired.** The sandwich reads VACUOUS on no claims or a contested run. Declared premises only. |
| L11 | IMPRECISION | Cousot's hypothesis restored. "Tight" is Lifschitz 1996. The chaotic row is graded a test of `chaotic_lfp`. |
| L12 | FATAL | **Repaired.** The door re-segments and refuses QUOTE-BOUNDARY (row and plant). |
| L13 | OVERREACH | **Repaired.** Idempotence is measured on repaired inputs. Retraction is DECLARED. |
| L14 | IMPRECISION | T7: Newton III, not Noether. The guards accept any position-dependent pairwise force. |
| L15 | IMPRECISION | T8: DECLARED, one program, and names are in the law. |
| L16 | FATAL | T9: a single ulp is erased about a quarter of the time. Traces localize. |
| L17 | OVERREACH | **Repaired.** Claims are keyed by claim id; inline claims each get a row; UNREACHED is a standing. |
| L18 | OVERREACH | §8 extended. |
| L19 | IMPRECISION | Counts are read from the evidence file, never typed. |
| L20 | IMPRECISION | §7 wording narrowed. |
| N1–N4 | DEFEATS | P1's mechanism is prior art (Fitting; WFS; ADF; Denecker, Marek & Truszczyński). §6 adopts the novelty prosecution's consolidation. |
| N5–N21, N25 | NARROWS | Cited in §6. Lara (2026) is named as the nearest neighbour. |
| N22–N24 | NO-PRIOR-ART-FOUND | Kept as "not found", narrowed. |
| E1 | defect | **Repaired.** Equality types its operands once (row). |
| E2 | defect | **Repaired.** Rule function names are assigned before any lowering (rows). |
| E3 | defect | **Repaired.** Absorbed clauses obey the children rule (rows). |
| E10 | defect | **Repaired.** Constant-depth If chains; NESTING-DEPTH 24; LOOP-NESTING 16. Rows at the limits on four executions. *(Corrected 2026-10-25, prosecutor F17: only LOOP-NESTING had a four-way row at its limit; NESTING-DEPTH had its refusal at 25. The four-way row at 24 was added then.)* |
| E13, E15 | defect | **Repaired.** One seal line; one oracle per claim (rows). |
| E16 | defect | **Repaired.** Procedures collected top-level and case-insensitively (rows). |
| E17 | defect | **Repaired.** Code refuses non-ASCII before normalizing (rows). |
| twin 37 | ambiguity | Settled in SPEC §11. With it, the twin matches the reference on 23/23. |
| twin 38 | defect | **Repaired.** LITERAL-RANGE replaces a crash (row). |
| twin 1–62 | ambiguities | Each settled in SPEC §11. |

## What the court established about the method
- The prosecutors' MEASURED claims were re-run before conceding. L12, L17 and L16 reproduced here. *(Note,
  2026-10-25, prosecutor F22: the logic prosecution's own scripts and outputs were kept in a session scratch folder,
  not in this repository, so L16's 1526 of 6000 cannot be rerun from this tree.)*
- Two of edition 1's falsifiers fired against edition 1 itself, as stated: T3's (L6) and T9's (L16). That is the
  apparatus working.
- Every repair is held by a self-test row. Where a defect could return silently, it is also held by a plant.
  *(Note, 2026-10-25, prosecutor F6: at commit fc19339, E18 and E22, both repaired, had no row. The next revision added
  both, E18's with a plant. By this record's own rule the finding defeats the edition-2 implementation claim
  (ed2-IMPL) as it stood; it is to be entered with the second round's record, beside the revised claim.)*
