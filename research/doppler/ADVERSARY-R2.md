# Debate record: the adversary's report on the proponent's design, round 2 (2026-10-26)

A subagent's report, saved verbatim by the judge. It is model output, not the owner's words, and carries no
authority. It was written after the adversary read PROPONENT.md and RESEARCH.md and ran the proponent's probe; its
experiments are in `work/doppler-adv/` (ignored by git); its MEASURED lines are this host's.

---

# The doppler: the adversary's report, round 2 (2026-10-26)

**Ran:**
- `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B work/doppler-probe/run_all.py`: DOPPLER PROBE HELD. This rewrote `work/doppler-probe/out/`, which git ignores.
- My fixtures against the probe's own A, B, search and plug-in, imported unchanged: `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B work/doppler-adv/r2.py`. Two runs were byte-identical, and every MEASURED line below is from it.

No tracked file changed.

## 1. My counts against this design

- **Answered (12).**
  - DP-1 and DP-3: PORT-FREE and taint are gone. All seven of my port fixtures read FLOWS in both A and B (TERM, TEXT, MAGIC, RULE, LIST, LEN, COST). MAGIC reads FLOWS although neither the probe's search (22 worlds) nor mine (2,001) sees a shift. The certifier no longer depends on a domain.
  - DP-4: the floor's trigger is repaired, in prose.
  - DP-7 to DP-12, and DP-14 to DP-16: conceded or dropped.
- **Partly answered (2).**
  - DP-2: the record now carries the count of evaluations, reachability and refusal. TERM and TEXT, which depend on the port only through a refusal, read FLOWS. But only 3 of 107 pairs are FIXED, as the proponent concedes.
  - DP-6: see (a) and N-2.
- **Survive (3).**
  - DP-5: OMIT, through the plug-in, reads true in 16 of 16, GROUNDED.
  - DP-17: no trigger is named.
  - DP-18: conceded, and now measured as a blind spot both derivations share (N-2).
- **Made wider (1).** DP-13: there are four new words near the grounding axis, two of which overclaim (b). There is also a new reading, GROUNDED (up to N ticks), with no rule for premises (N-5).

## 2. New defects in the design

No fixture reads FIXED where a claim's record shifts with a port value. Two read FIXED where what the session shows still shifts: PROC through the log's length, and CERT through the cost fields of the claim line.

**N-1 · FATAL as written. "Before the tick block" licenses claims that are evaluated inside it.**
- R2 places the tick block last, and SPEC allows procedures at the top level only. So every procedure's claims stand textually before the tick block.
- PROC: claim §3.2 is in a procedure performed only in the loop §5. A and B read FIXED over the declared port.
- Through the plug-in, 16 ticks read true in 16 of 16, GROUNDED; 17 ticks read REFUTED at 17.
- The licence must be decided by evaluation, not by text. My PREFIX said "outside every procedure"; the design's claim to contain PREFIX dropped that condition.
- Its sentence "a claim before every port declaration is FIXED by construction" is false. PREPROC is a claim before the port, in a procedure performed after the port is used. A and B rightly read FLOWS, and the search shifts at 7 → 0.
- LEN with no port reads GROUNDED through the plug-in as built. The tick-block rule exists only in prose.

**N-2 · OVERREACH. The certified record is smaller than the court's claim line.**
- CERT is a certificate claim whose certified loop runs to thrust. A and B read FIXED, and it reads GROUNDED for both values.
- The court's reading moves anyway: thrust 0 gives NOT CHEAPER (receipt `claim 0 6 1 1 1 4 1`), and thrust 5 gives CHEAPER (`… 4 11`).
- The search compares only (evaluations, trues), and finds no shift in 17 worlds. Under R9 these counts become refusals.
- FIXED must cover the whole claim line, or the court must withhold a licensed claim's cost reading.

**N-3 · OVERREACH. R9's channel is built in A only** (budget.py: "B does not implement it"). For a budgeted law, "FIXED needs both" fails.

**N-4 · OVERREACH. Each-tick ports, RUN-1's main form, are NOT MEASURED.** Every stand-in is a top-level Let read once (`candidate_ports`), and the search sets one value per run. So per-tick variation, |D|^ticks, is never attacked, and that variation is exactly the horizon fork's premise.

**N-5 · IMPRECISION. Horizons need a premise rule.** A claim GROUNDED up to N with a premise grounded up to M < N should read up to min(N, M). No rule says so, and the horizon lives in the ledger (fork 9).

**Premises and the filter: answered.** The filter acts before the fixed point. §3, FIXED and given a flowing §4, stays UNGROUNDED (rerun: R6 ROWS HELD). Its only hole is N-1, reached through a premise in a procedure.

## 3. The four questions

**(a) The horizon fork survives DP-6.**
- FIXED is 2-safety over logs of length N.
- R2 puts nothing after the tick block, and D3 has no end block. So a shorter log's record is a prefix of an N-tick record.
- One agreed N-tick run in which the claim holds therefore gives the claim at every tick of every log up to N. That is DP-6's invariant, bounded at N: independence plus one run is exactly what grounding needs up to N.
- I concede it, once N-1, N-3 and N-4 are closed and N-5 is ruled. A backend divergence in another session only lowers that session's reading.

**(b) The words.**
- **FIXED BY THE LAW** reads as settled, true by law, or repaired. It hides "per port, at one length, under rules A and B, as DECLARED", and in the tick block it licenses nothing. A word that needs a forbidden interpretation is the wrong word (Ragnarök, decision 1).
- **FLOWS FROM p** reads as "depends on p". That is false for the probe's 6 hand-proven false positives and its guarded-port row. It is a path in the rules, not a flow.
- **SHIFTS WITH p** is acceptable when it carries its values and evaluation.
- **DISPUTED** is acceptable, but it stands next to the court's CONTESTED (integrity) and will be confused with it.
- Proposed instead: NO PATH FROM p (A, B); PATH FROM p; SHIFTS WITH p; A AND B DIFFER.

**(c) Consistency by construction, plus diversity of code paths.**
- A and B share the rule table, the reading of interp.py, the author, and the front end, through the law bytes B parses.
- Each plant switches off a rule the table has, so cross-catching shows that every rule is load-bearing in both. A rule the table lacks cannot be planted. CERT is such a shared omission, read FIXED by both.
- Outside the rules stands only the search, which attacked 3 FIXED pairs on the population. My seven fixtures add seven consistent data points.
- That is evidence for the claim's record within the table's scope (OBSERVED; one model family on both sides), and none for the table's completeness.

**(d) Tokens: sound for claim records, not for sessions, and worth nothing before 1a.**
- The kind check refuses Say, concatenation, arithmetic, ordering, literals and token-valued rules. So data independence (Wolper) holds for claim records, given a correct checker.
- The trace is not invariant under the equality pattern. In the probe's K1 law, (5, 9, 13) and (6, 10, 14) share one equality pattern: their claim lines are equal and their trace heads differ (MEASURED). Assignment events carry token bytes, and the input-log seal differs by definition.
- So "sessions can be cached per orbit" holds for claim records only, not for receipts.
- A token needs:
  - a new value tag in RUNTIME-SPEC §5, for events and the log;
  - identity defined as exact bytes after the door's JSON decoding, so U+00E9 and e followed by U+0301 are two tokens;
  - equality in three generators and two runtimes;
  - a twin round.
- The law cannot print a token, but token bytes still reach traces and the arbiter's divergence notes.
- Tokens cannot index lists or be ordered, so entity tables stay integers. Each-tick tokens cost B_{k·n} runs.
- Before 1a there is no port to type (R-14).

## 4. My narrowest version, revised

**What changed it.** A refusal-sensitive static analysis read FLOWS on every fixture I had, including MAGIC, which no search finds. It is a certifier where a search is only a prosecutor. I withdraw my claim that nothing beyond PREFIX can be licensed soundly without search.

To be built only on a trigger:
1. **R6 repaired:** in a run with an input log (any port, or a tick block), no claim is GROUNDED, except under item 2.
2. **The licence:**
   - NO PATH FROM every port, in both A and B;
   - every evaluation of the claim precedes the first tick;
   - the record covered is the whole claim line: evaluations, trues, cost, and the certified clause's cost.
3. **R4 in the court:** an evaluation that refused is named, and its claim is not held.
4. **The search** compares whole claim lines over a sealed domain of values and lengths. It re-runs each shift on four executions and licenses nothing.
5. **Deferred:** the horizon fork waits for N-3, N-4 and a fork-9 ruling. Tokens wait for a RUN-1 type ruling.

**Outcome words:**
- `GROUNDED (no path from any port; §k is evaluated before the first tick)`
- `UNGROUNDED (rests on input log <seal>, unratified: R6)`
- `NO PATH FROM <p> (A, B)` / `PATH FROM <p>` / `A AND B DIFFER`
- `SHIFTS WITH <p>: <a> → <b>, claim line <x> → <y>, evaluation <n>`
- `REFUSED at evaluation <n> (<CODE>): not held`

**Acceptance tests** (each plant must be caught by its own row):
- **AT-1.** PROC at 16 ticks reads UNGROUNDED. Plant: licensing by clause position.
- **AT-2.** PREPROC reads PATH FROM thrust. Plant: licensing "before every port declaration".
- **AT-3.** CERT reads PATH FROM thrust, or its licensed row is byte-identical at thrust 0 and 5. Plant: a record without the certified clause's cost.
- **AT-4.** The probe's budget fixture reads PATH at budget 4 in both A and B. Plant: B without R9, which reads A AND B DIFFER.
- **AT-5.** LEN with no port reads UNGROUNDED through the plug-in. Plant: the plug-in as built.
- **AT-6.** OMIT reads REFUSED at evaluation 17. Plant: today's tally.
- **AT-7.** All seven round-1 port fixtures read PATH in both A and B. MAGIC's search stays NO SHIFT, kept as a monitored negative.
