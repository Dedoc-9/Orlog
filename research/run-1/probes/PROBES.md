# RUN-1's research probes: code, outputs and the proposals they support, kept apart

Every file in this folder is an **experimental research probe**. None is the contract, the court or a gate row, and
nothing in the program reads any of them. A probe that passes supports a proposal. It never shows that a contract
holds: there is no contract yet, because nothing is ruled.

The three kinds of file stay separate:
- **code**, here in `research/run-1/probes/`;
- **outputs**, in `evidence/`, each beginning with its command, its tree and environment, its exit status and
  whether two runs were byte-identical;
- **proposals**, in `research/run-1/`: `CUT-0.md`, `ROUNDS.md`, `CONTRACT-DRAFT.md` and `TRANSFER.md`.

**Run each probe the same way:** `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/probes/NAME.py`. It exits 0
when its last line says HELD.

**Environment of the recorded outputs:** Windows 11, CPython 3.14.5, on the tree at 95dac79 with these files
uncommitted and `src/` unchanged, 2026-10-26.

| probe | supports | output | its last line, as recorded | shows | does not show |
|---|---|---|---|---|---|
| `completeness_probe.py` | CONTRACT-DRAFT §8.4, the site rule (superseded by CUT-0) | `evidence/run1-completeness.txt` | `COMPLETENESS PROBE HELD: 1 withheld, 0 gained required (0 held gained, 0 support gained), plants 2/2` | the site rule's effect on 89 claims of version 0 | its precision: it over-withholds (cut0_claims C1, D03, D11) |
| `cut0_claims.py` | CUT-0 §2, the causal cut under reading S2 | `evidence/run1-cut0-claims.txt` | `CUT-0 CLAIMS HELD: 19 of 19 cases as required, pairs and descriptors told apart, plants 9/9, 0 gains (0 unexplained), R8's exact class 5/5, the instrumented reference identical in 933 of 933 runs (290 host stops)` | 19 cases, ten of them from the two adversaries and the lineage report; three pairs the site rule cannot tell apart; the instrumented reference equal to the reference in receipts, traces and host stops, at each text's budget and at budgets that stop it part-way | soundness beyond the cases: the invariant is argued construct by construct (CUT-0.md §2), not proved; version 1's rows |
| `cut0_session.py` | CUT-0 §3, the session as a transition system | `evidence/run1-cut0-session.txt` | `CUT-0 SESSION HELD: 45 of 45 cases, 76364 legal histories with no row failed, 16132 mutations with no non-canonical log accepted, plants 13/13` | the termination loophole closed; RUN-REFUSED; sources in the history; the strict grammar; the two-layer binding; three exhaustive domains (one port to 6 events, none to 6, two to 4) | Orlog's door and execution (the law is a stand-in); a buffering host; any timing; the host's honesty |
| `t8_monotone.py` | the theorem ledger's T8 | `evidence/run1-t8-monotone.txt` | `T8 MONOTONE HELD` | the court's own `support_sets` against the lemma, over every premise graph up to 3 claims and 20,000 of 4 | larger graphs (the lemma is proved by hand in ROUNDS.md) |
| `cut0_schema.py` | `CUT-SCHEMA.md`: the refusal cut's bytes, draft 2, derived from CUT-0's rule as written | `evidence/run1-cut0-schema.txt` (draft 1's, superseded: `evidence/run1-cut0-schema-draft1.txt`); with `--v1-standins` (2026-10-29), version 1's frames on version-0 stand-ins: `evidence/run1-cut0-schema-v1-standins.txt`, MEASURED on the stand-ins only | `CUT SCHEMA DRAFT 2 HELD: 89035 refused runs, each decoding to its live cut (0 differ), a generated shape in every one; 136 shapes, encode and decode inverse; 390498 byte mutations and 2858 frame forgeries, none accepted outside the shapes; 4 of 4 fields with a witness; 7 of 8 shape rules caught, 1 equivalent; draft 1 accepted 1 mutations and 74 forgeries outside them` | the bytes carry what the rule reads and no more, each field with a witness claim; the decoder accepts only shapes the interpreter's calls can produce, by seven rules each caught when dropped (the round trip equivalent, by the grammar's structure); draft 1's 15 accepted mutations classed | that a well-formed cut happened (14 of the 15 accepted mutations change a standing: only the executions' agreement holds a cut to its run); version 1's frames, where S4 and S6 change; constructs outside the families' grammar |
| `meet_probe.py` | `SETTLEMENT-DEBATE.md` §2: the meet R8 ∧ CUT-0, option (d) | `evidence/run1-meet.txt` | `MEET PROBE HELD: 79520 refused runs, 192894 claims; the meet never above R8 (0 held, 0 supported); TIGHTER 43356, LOOSER 7; the join rises above R8 on 7 claims, its plant caught` | the meet holds and supports nothing R8 does not (support by the court's own lfp, T8 measured run by run); CUT-0's differences from R8 are 43,356 tightenings and 7 gains over the corpus and both families; the join's plant rises exactly on the gains | which tightenings are justified and which are CUT-0's conservatism (the resumption oracle can split them, not run for it); version 1's tick block; laws outside the families' grammar |
| `disagree_probe.py` | `SETTLEMENT-DEBATE.md` §7: the disagreement set between R8 and CUT-0, classified | `evidence/run1-disagree.txt` | `DISAGREEMENT CLASSIFIED: TIGHTER 43356 under Rinf: REFUTED 1968, CONFIRMED 40141, UNREACHED 1247, UNRESOLVED 0, UNMODELLED 0; LOOSER 7: REFUTED 0, CONFIRMED 0, UNREACHED 7, UNRESOLVED 0, UNMODELLED 0` | each disagreeing claim resumed by the manifold oracle (eight values, under Rinf and R1): R8 contradicted for 1,968; 40,141 true in every resumption, where E1 and E2 differ on meaning alone; 1,247 CUT-0's conservatism, concentrated in the While row; the 7 gains all unreached; every disagreement held by CUT-0's own rows (the tagged continuation equal to the probe's on every run) | values outside the eight; family E's claims are true by its grammar; real laws; version 1's tick block |
| `door_canon_probe.py` | TRANSFER.md: the session's canonical-grammar method applied to Orlog's own door and parser (DESIGN-BRIEF H2) | `evidence/run1-door-canon.txt` | `DOOR CANON PROBE HELD: the door-aware sweep finds H2's split in the door as built (33 mutants); the single sweep finds nothing; the repair breaks nothing and changes 1 frozen verdict(s)` | that a one-byte sweep (145,089 mutants) is blind to H2 and a door-aware one (58,968) finds it; that H2's repair, run in memory, breaks nothing and moves one frozen verdict (E18: QUOTE-BOUNDARY to LINE-FORM) | that the door has no other defect: only the properties checked (idempotence, door–parser agreement, totality), only these mutation sets |

## Defects these probes or their adversaries found in the probes themselves, and their repairs (2026-10-26)

| found by | defect | repair, and what holds it |
|---|---|---|
| this session | a `While` refused FUEL-EXHAUSTED held its body's claim | a loop whose own clause refused re-enters; case C6, plant `header-bit` |
| this session | `end()` was legal with a tick half assigned, so the projection dropped the assignment | END-PENDING, END-UNDISPOSED; case S8, plant `end-anytime`, row `no-assignment-disappears` |
| this session | the log reader trusted the generator | `parse_log`, the canonical grammar; its malformed cases and mutations |
| the manifold adversary, F1 | lower `While` frames read the fuel check as a stop and the top one as passable, so an input's refusal could raise a standing | reading S2 everywhere; cases F1 and F1′, plant `while-bit` |
| F2 | the cut's descriptor named the open claim's clause, not the claim | the descriptor carries the claim's id; the A23 pair, plant `descriptor-no-id` |
| F3 | a refused If added arms whose conditions had already read false | the frame records the refused arm; case A09, plant `all-arms` |
| F4 | the instrumented reference skipped the host-budget check at a loop's entry, and the equivalence never ran a host stop | the check restored; equivalence at budgets that stop each run part-way (290 host stops); plant `no-entry-check` |
| F5 | "0 gained" refused a correct gain over R8's possible reading | a gain is allowed only in R8's possible class, with the frames showing another claim open |
| G1 | a law with no each-tick port wrote `t 1 ` with a trailing space, which the parser refused | the record written with no trailing space; case S12, a zero-port exhaustive domain |
| G2 | the door's `$` accepted `1` followed by LF | `fullmatch` throughout; row D, plant `door-dollar` |
| G3 | the parser accepted A1's cause under A2 | the cause set follows the policy; malformed case, plant `a1-cause-under-a2` |
| G4 | most rows could not turn red, and six plants were caught only by named cases | row `no-value-invented`; `hold-previous` must also turn the exhaustive search red |
| G5 | the history recorded no source, so Alice's `1` and Mallory's `1` had one session record | `arrive(port, source, bytes)`; case G5, plant `no-source` |
| G6 | the host could close ticks after the run refused | RUN-REFUSED; case S11, plant `close-after-refusal` |
| G7 | "sent nothing" and "dropped by the host" give one input log and one core | by design (law-equivalence): the history and the session record tell them apart |
