# Fork the settlement, not the truth: an adversarial consensus (2026-10-26)

*Ruled since, 2026-10-26: option (d), not this record's (c). The meet R8 ∧ CUT-0 is admitted, with E2 as HELD's
meaning (`RULINGS.md`, the claims ruling; `SETTLEMENT-DEBATE.md`). This record stands as written.*

The owner forwarded three things, and nothing here is ruled:
- **an outside proposal to fork CUT-0's adoption.** Keep R8 as the admitted rule while CUT-0 is built and attacked as
  an experiment, with authority merging only through a versioned ruling.
- **an outside adversarial review of that proposal.** Fork the semantics, not the repository; pin execution,
  settlement and assurance in one manifest; classify a difference's direction, never its correctness; promote
  nothing on a deadline.
- **his own pointer** to the verifiable-computation workbench on his GitHub and his computer, and the reviewer's
  reading of it as Orlog's unifying architecture.

The outside texts are paraphrased here, never quoted.

## 1. What the record establishes first

| fact | where | what it changes |
|---|---|---|
| **The workbench is Dentatus, Orlog's ancestor**, and its design is the one Orlog carries: deterministic, content-addressed, nondeterminism captured at the boundary, integrity ≠ truth. Read from its code (`manifold/LINEAGE.md` §2.8): a missing input silently becomes 0 (`lockstep/tick.py` 45); predicted inputs are hashed into the "corrected" truth (`rollback.py` 71-72); its "causal frontier" stops at depth 6, an under-approximation that would hold claims wrongly; refusals never reach the history (`chronicle/core.py` 81-83) | the lineage record, ESTABLISHED (re-read) | The workbench's five rules are what Orlog and RUN-1 already state: replay, boundary capture, content-addressed records, distinct outcomes, independent verification. **RUN-1's design is the repair of Dentatus's defects**, each forbidden by a rule here: nothing invented, A2, a history with its refusals, a continuation that over-approximates. Adopting "the workbench" adds a name, not a mechanism |
| **R8 is the court as built, and it reads E1**: a claim is held when every completed evaluation was true | `src/orlog/court.py` | Kept as the admitted rule for v1, R8 holds an interrupted claim of the tick block, as Round D's F19 found. R6 a bounds the harm: no claim of the tick block is ever GROUNDED. A PREFIX claim reads the same under both rules past a refusal at a tick (the owner's R6 settlement). The two rules differ on held and support, and on a PREFIX claim cut off inside the prefix |
| **CUT-0 needs the cut, and v0 records only the refusal's code** | `interp.py:108`: the `'R'` event's payload is the code | Reading R8 and CUT-0 over the same evidence requires the cut in v1's `'R'` event. Without it, CUT-0 needs the reference to replay, a fact only one execution states, which was rejected. **The fork does not defer this format decision; it forces it into 1a** |
| **The court already carries its rules** | `court.py:361` returns `"rules": COURT_RULES` with every reading | A settlement identity is one line, the digest of the rule set, printed with every reading beside the core digest it read. No new artifact is needed |
| **The adversaries' register is frozen** | `ADVERSARY-ROUND-D.md` (26 findings) and `manifold/ADVERSARY.md` (13), each disposed in `ROUNDS.md` (Round D) and `probes/PROBES.md` | A gate can name its findings by record and number |
| **The review again names T11 as CUT-0's proof** | the ledger | CUT-0's obligation is **T10**. T11 is COMPAT-0's preservation and T12 the conjecture. A waiver of T11 would say nothing about CUT-0 |

## 2. The proposal and its review, disposition by disposition

| point | disposition |
|---|---|
| fork the semantics, not the repository | **accepted.** One codebase, with the settlement rule as a parameter of `panel`. That is R8's own precedent: the reporting pass's finding 1 made R8 a parameter read at its shipped value, never a module switch |
| one framework, the rule the only variable; the common-mode risk | **accepted.** The resumption oracle computes what a run evaluates by executing the reference, apart from the court, so a defect shared by the court's two readings does not pass it unseen |
| a gate of PASS, FAIL or UNRESOLVED per obligation; the owner the authority; no promotion on a deadline | **accepted.** A residual debt can be admitted only by the owner's explicit, scoped waiver, and a waiver is not a proof. A review deadline lapses the experiment's privileges, never its obligations. If no one rules, the admitted rule stays |
| a manifest pinning execution, settlement and assurance | **accepted, from what exists.** Execution is the receipt core and its agreement record. Settlement is the court reading's rule digest. Assurance is the ledger and the evidence each probe's header names. The session record already binds history, log and core. A reading binds the core it read, its rule digest and the ledger |
| deltas classified TIGHTER, LOOSER, UNCHANGED, KNOWN-DEFECT-REPRODUCED or UNCLASSIFIED, never a correctness verdict | **accepted.** `probes/cut0_claims.py` already classifies this way: "withheld by the cut" is TIGHTER; a gain is LOOSER, allowed only where the frames show another claim was open. The vocabulary becomes the review's, and an UNCLASSIFIED delta blocks admission |
| a trusted boundary for the comparison | **accepted.** Raw receipts, traces with their cuts, and machine-checked comparisons, with the reporting tested against them rather than read from a summary |
| a consumer's profiles | **accepted.** `orl.py court` reads with the admitted rule alone. The experimental rule runs only in the research harness, never as a flag a caller sets in the admitted contract |
| the workbench as the unifying architecture | **accepted as a description, not a new layer** (section 1) |

## 3. The choice before the owner, now with three options

The previous question had two options: build CUT-0 with its debt named, or prove T10 first. The fork adds a third,
and this record recommends it.

| option | what 1a builds | what it costs | what it risks |
|---|---|---|---|
| **(c) the fork** (recommended) | the court admits **R8 (E1)** and names its rule digest. **The cut is recorded in the `'R'` event from 1a on.** CUT-0 (E2) is built as an experimental settlement parameter in the research harness, compared on frozen corpora by delta class, with the oracle as a row. It is admitted only by a later ruling, with every obligation PASS or explicitly waived by the owner | the cut's bytes in `orlog-trace-1` (one-way, needed under every option); a settlement parameter; a rule digest in the reading | E1's known over-holding of interrupted claims, which R6 bounds (never GROUNDED in the tick block), named in DOCTRINE as the admitted semantics |
| (a) CUT-0 admitted, debt named | the court admits CUT-0 (E2) with T10 graded DECLARED and MEASURED | the same format, and the debt carried by running code | a defect in the argument reaching admitted readings. Two were found on the day it was written (C6, F1) |
| (b) prove T10 first | nothing of CUT-0 until a proof is written and checked | delay | none to the readings; R8 stays meanwhile, as under (c) |

**Why (c).**
- It keeps authority where the evidence is: R8 is built, its rows are in the gate, and COMPAT-0 holds it.
- It loses nothing in v1 that R6 does not already guard.
- It pays now only the format decision every option needs.
- It turns the debate's evidence into a standing comparison, not a one-off.

The held set's claims row changes with it: **E1 admitted for 1a, E2 the candidate**, admitted later or never by
ruling. The owner's R6 settlement for PREFIX claims holds under both.

## Does not show

- That E2 is the right standing in the end: that is the owner's ruling, and T10.
- That R8's over-holding is harmless outside what R6 bounds: support and the held reading still differ, and the
  difference is named, not removed.
- Anything of Dentatus beyond the files the lineage researcher read.
