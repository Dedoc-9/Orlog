# Verdict: a manifold view of CUT-0 (2026-10-26)

This is the judge's verdict on whether "manifold computing" earns a place in RUN-1's contract. An outside reviewer
suggested it, preferring a discrete configuration complex to any continuous geometry, and the owner asked for it to be
researched with subagents and debated. Three agents took part, each in its own record beside this file:
- **a proponent** (`PROPONENT.md`, with `resume_oracle.py`, `fibers.py`, `make_laws.py` and `laws/`);
- **an adversary** (`ADVERSARY.md`, with `adversary/`);
- **a lineage researcher** (`LINEAGE.md`), who read the owner's earlier repositories and local folders for his own
  manifold designs.

This verdict is model output, like them, and admits nothing. Every measured claim it rests on was rerun by the judge,
as listed below. The reviewer is paraphrased, never quoted. The four criteria are the reviewer's.

## The answer

**The manifold view does not earn a place as a method.** The one testable geometric claim was that quotienting the
session's histories by commuting events shrinks what must be checked. It measured to nothing (EXHAUSTIVE on two
declared domains):

| domain | Mazurkiewicz traces | plain reachable states | commuting squares checked, all diamonds |
|---|---|---|---|
| one port, to 6 events | 22,021 | 22,021 | 99,642 |
| two ports, to 6 events | 16,395 | 16,395 | 55,448 |

Two more findings close the question:
- **The claim side has no commuting events at all.** It is one deterministic thread.
- **The owner's own "manifolds" are not state spaces** (`LINEAGE.md`, read from the code). They are a covariance or
  PCA eigenspace, a single-linkage clustering, a box with a clamp, a k-NN graph, a label, or a placeholder. None
  builds a stratified space of discrete states, and none strengthens the geometric case.

**The debate was worth running all the same.** The framing was useful as a prompt, and every win came from a
classical, non-geometric technique.

## Against the reviewer's four criteria

| criterion | met? | by what | evidence |
|---|---|---|---|
| (a) a missed aliasing or premature-completion counterexample | **met, by operational search** | the adversary found 13 defects, 5 unsound. The worst, F1: an input's refusal raised a claim's standing | each reproduced by the judge, repaired, and held by a case and a plant (`probes/PROBES.md`). After the repairs, the proponent's oracle finds none in 88,950 refused runs |
| (b) a smaller, demonstrably complete representation | **met for the session's log rows, by bisimulation and symmetry reduction** (prior art), not by geometry | the proponent's log congruence keeps only what the input log's future depends on | 0 congruence failures on every concrete state to 7 events. 352 classes stand for 65,442 histories at 6 events, and 6,705 for about 2.1 × 10^12 at 14. The 11 log rows read the same on the classes, unplanted and under all 13 of the probe's plants |
| (c) a soundness argument for claim settlement | **met as an argument and as evidence, not as a proof** | the construct-by-construct argument (`CUT-0.md` §2), and the proponent's resumption oracle, which makes the hypothetical run the definition names | no claim evaluated after the cut outside K, and none K holds evaluated again. This holds under both readings: only the first refusal passable (R1), and every refusal passable (Rinf). The runs are 61,879 EXHAUSTIVE over a declared grammar and 27,071 from 10,000 random laws. 10 of 10 unsound plants in K and 3 of 3 in the oracle are caught |
| (d) lower cost without fewer cases | **met for the session's log rows** | the congruence: classes instead of histories | OBSERVED, one loaded host: about 18 s for the concrete states to 7 events against 2.7 s for the classes to 14. The oracle costs more than K, as a test instrument should |

## What the debate changed in CUT-0

- **The adversary's 13 findings:** every measured one reproduced and is repaired, each with a case and a plant
  (`probes/PROBES.md`).
  - Reading S2 everywhere (F1).
  - The cut names the open claim by its id (F2) and a refused If's arm (F3).
  - The instrumentation checked at budgets that stop runs part-way (F4).
  - In the session model:
    - arrivals carry their source (G5);
    - RUN-REFUSED (G6);
    - the record of a law with no each-tick port (G1);
    - `fullmatch` throughout (G2);
    - the end cause set by the policy (G3);
    - the row `no-value-invented` (G4).
  - G7 stands by design. F5 corrected the probe's own acceptance check.
- **The same defect, found independently.** Before reading the adversary's record, the proponent's oracle saw the
  first form fail only through a spent `While` fuel check: 96 runs in the random family, and nowhere else. That is
  the adversary's F1. Two sides found one defect without seeing each other's work, which is the independent
  confirmation the reviewer asked for. The one minimal law is `laws/fuel-bit.orl`.
- **What reading S2 costs (MEASURED, random family).** The revision withholds 226 claims the first form held:
  - 109 are evaluated again when every refusal is passable, so they are rightly withheld;
  - 117 never are, which is the over-approximation's price.

  S2 trades those 117 for the guarantee that an earlier refusal can never raise a standing.
- **The lineage report's under-approximation plant** (a reach cut at a procedure performed inside another) is now
  case L1 and plant `shallow-reach`. The claims probe reads 19 of 19 cases and 9 of 9 plants.

## A finding left open, with a proposed rider

**A log can run past a refusing tick.** The parser accepts an input log that continues after a tick whose run
refuses (MEASURED by the proponent: 8 of 21 such logs with one port, 44 of 84 with two). No live session can write
one, because RUN-REFUSED forbids it. An offline log can, and its unread records still move `input-log-sha256`.

- **It is inherent:** the parser cannot know a tick refuses without running the law.
- **Proposed rider (DECLARED, not built):** the receipt records how many tick records went unread after a refusal.
  The core stays a function of the input log, and the leftover becomes visible.

## The judge's reruns

| claim | rerun | result |
|---|---|---|
| the resumption oracle (`resume_oracle.py`) | once, 6 min 8 s | its record line for line, line endings aside; the probe hashed `de5682e1…`, the one the proponent recorded |
| the session congruence and quotients (`fibers.py`) | once | its record line for line, line endings aside |
| the adversary's F1, F2, G1, G2, F4 | each case, through the probes | reproduced, before any repair was made |
| the lineage report's dvsm-meta-kernel smoke test and DEEQN64 convergence | read in the code | confirmed (ESTABLISHED). The smoke test's peer hashes are a constant and its threshold is 2, so it never compares a hash. DEEQN64's `converged = frame_count > 100` is labelled a placeholder in the code |

Not rerun:
- the adversary's 20,000-law fuzz and its cut-monotonicity check (the oracle covers the same ground independently);
- the lineage report's runs of the owner's repositories, beyond the two readings above.

## What to keep

- **The resumption oracle and the log congruence, as off-gate research instruments.** They are the natural checks for
  1a: the oracle against the continuation, the congruence against the session's rows. Like every probe, they are
  evidence for a proposal, never a gate row.
- **From the owner's lineage, three discrete designs** (`LINEAGE.md`, read from the code):
  - **Ursprung's PO-10:** an over-approximation checked against an exact reachable graph, with a plant. It is the
    template the oracle follows. The researcher notes that PO-10 computes `frontier_open` and never reads it; the
    judge did not check this.
  - **Urðr's `inputset`:** which record determines which quantity.
  - **A local Verðandi copy's WORKSHOP-0** (`LINEAGE.md` §2.5)**:** a census of which record each edit moved.
- **No manifold vocabulary in the contract.** A name that promises geometry where the code computes enumeration is
  the overclaim the lineage itself shows: a "certified manifold" that is a frame count, "quotient topologies" that
  are single-linkage clusters.

## Prior art

Read as each record says:
- trace spaces of concurrent programs (directed algebraic topology): one paper read in part in full text, the rest at
  abstract or secondary level;
- partial-order reduction and persistent sets, which coincide with the geometric reduction where both apply;
- bisimulation and symmetry reduction, for the congruence;
- abstract interpretation's over-approximation, for K.

No mechanism here is new.

## Does not show

- That CUT-0 is sound beyond the families checked: version 0 only; the refusal kinds the oracle models (0 runs set
  aside as "cut not modelled"); its grammar and its seeded random family.
- Anything of version 1, which is not built.
- That the owner's earlier repositories are wrong beyond the defects named, which were read or run as stated.
