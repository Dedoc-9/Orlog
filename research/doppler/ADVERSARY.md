# Debate record: the adversary's report on the doppler, round 1 (2026-10-26)

A subagent's report, saved verbatim by the judge. It is model output, not the owner's words, and carries no
authority; the judge's verdict (VERDICT.md in this folder) weighs it against the proponent's design and the prior-art
survey. Its experiments are in `work/doppler-adv/` (ignored by git); its MEASURED lines are this host's. The judge
reproduced DP-5 before saving this record: a claim whose 17th evaluation refuses (INDEX-OUT-OF-RANGE inside its own
condition) reads "true in 16 of 16 evaluations", WELL-FOUNDED and, with its seal ratified, GROUNDED, while the run
itself is REFUSED at that claim.

---

# The doppler: the adversary's report, round 1 (2026-10-26)

**Read:** everything the brief names, and my lineage's records. **Changed:** no tracked file. **Experiments** (`work/doppler-adv/`, ignored by git):
- `lab.py` builds the first design's two instruments literally: a taint interpreter whose every receipt is held byte-identical to the reference's, and the doppler.
- `laws.py` rebuilds fall.orl and leapfrog.orl, each held to its example's law seal.

Each script ran twice on this host as `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B work/doppler-adv/<script>`. The outputs were byte-identical except b_scale's TIMING lines. The stand-ins follow r6_indirect.py: a port is a variable set from a literal, and a log's length (D3) is a loop bound. What follows for RUN-1 is argued.

## A. `a_lattice.py` (every row MEASURED)

The domain is −1000..1000 (2,001 values) unless noted. "Truth" is the design's comparison, the claim's truth per evaluation; "standing" is UNREACHED/HELD/REFUTED. Each claim rests on the owner, with its own seal ratified by a fixture line. The reference and the Python backend agree.

| case | taint (explicit, pc) | doppler (truth, standing) | design | judged log | other log |
|---|---|---|---|---|---|
| TERM: thrust² added to e each tick overflows | clean, clean | none, shift | PORT-FREE | 10^9: true in 9 of 9, **GROUNDED**, run REFUSED OVERFLOW | refuted at 17 in all 2,001 domain runs |
| TEXT: an unread text doubles each tick | clean, clean | none, shift (0..9) | PORT-FREE | 100: 22 of 22, **GROUNDED**, TEXT-TOO-LONG at tick 23 | 5: refuted at 23 |
| MAGIC: `If thrust equals 6170203994113542144, then bump.` (a procedure) | clean, clean | none, none | PORT-FREE | 5: **GROUNDED** | magic: refuted at 1 |
| RULE: speed 3, or 9 provided thrust > 1000 | clean, tainted | none, none | PORT-FREE, UNKNOWN | 5: **GROUNDED** | 1001: refuted at 1 |
| LIST: a literal appended if thrust > 1000 | clean, clean | none, none | PORT-FREE | 5: **GROUNDED** | 1001: refuted at 1 |
| LEN: a counter's claim, thrust varied, 16 ticks | clean, clean | none, none | PORT-FREE | 16 ticks: **GROUNDED** | 17: refuted at 17 |
| LEN, no port | | | | 16 ticks: **GROUNDED** | 17: refuted |
| COST: certificate of a loop to n | | none, none | | n=1: NOT CHEAPER | n=10: CHEAPER; true in both |
| OMIT: the claim's own 17th evaluation refuses | | | | true in 16 of 16, **GROUNDED**, run REFUSED INDEX-OUT-OF-RANGE at the claim | |

## Counts

**DP-1 · FATAL. PORT-FREE licenses a GROUNDED that the log decides.**
- Six rows read PORT-FREE and GROUNDED over one log, and refuted over another.
- TERM's claim is refuted under every log of the published domain.
- "UNKNOWN never reads GROUNDED" saves nothing, because every failure reads PORT-FREE.
- Dilemma: if PORT-FREE grounds, GROUNDED is only as sound as a search the paste itself calls "not proof". If it does not ground, the lattice changes no reading.

**DP-2 · FATAL. Truth per tick cannot see anything that changes which evaluations exist:**
- the log's length (D3, D8);
- a refusal elsewhere (R4 a), since `held` ignores the run's status (court.py:231);
- reachability;
- R9's TICK-BUDGET, which would turn any port-dependent operation count (COST) into such a refusal.

Taint is termination-insensitive, which leaks more than a bit (Askarov et al., ESORICS 2008), while "true in n of n" is progress-sensitive. A sound termination-sensitive type system must treat every Int or Fix operation on a port value as a possible end of the run (OVERFLOW). That taints every later evaluation, which is nearly the coarse rule again.

**DP-3 · FATAL. Dynamic taint is not "sound for the observed run".**
- It never sees a branch not taken (MAGIC, LIST). Sound purely dynamic monitors must reject some programs that flow-sensitive static analysis accepts (Russo & Sabelfeld, CSF 2010); this one rejects nothing.
- Explicit taint misses a proviso that chooses between literals (RULE).
- "Witness found, taint clean → taint is broken" misreads a designed limit as a defect.
- Where both instruments are blind (five rows), their agreement measures what they share (T11).
- IMPRECISION: r6_indirect.py's `reads()` misses `length of L` and RULE's proviso.

**DP-4 · FATAL against R6 as amended (new).** Nothing in R2 or D3 requires a port for a tick block, yet the log's length is input. R6 fires only on "declares any port", so LEN with no port reads GROUNDED over 16 ticks and refuted over 17. Widen the trigger to any input log, or forbid a portless tick block.

**DP-5 · OVERREACH in the court; R4's falsifier already fires.** OMIT reads "true in 16 of 16" and GROUNDED, though the claim's 17th evaluation refused. interp.py counts an evaluation only once it completes (lines 251–265). R4's falsifier is a reading that "omits an evaluation that refused", and that is met today. ADVERSARY-R2 D-5 found this in Ragnarök's instrument; it is in the court too.

**DP-6 · FATAL to independence as the criterion, and to the framing.**
- A ratification binds the claim's seal, which holds the law seal (court.py:141–144), never the log.
- In v0 the law fixes the run, so the ratifier saw everything the claim's record depends on. Under RUN-1 that holds only where nothing the log controls reaches, ends or changes the claim's evaluations. The text alone decides this only for the prefix.
- In the tick block, n is the log's length. So GROUNDED rests on the log unless the claim holds at every tick of every log: an invariant, a 1-safety property.
- Independence is 2-safety (Clarkson & Schneider 2010), and neither implies the other. LEN's claim is independent and invalid; `b or not b` over a truth-value port is dependent and valid.
- Inside the tick block, R6 rightly withholds grounding from every claim that is not such an invariant, whatever its ports.
- The incompleteness worth removing is the prefix, invariants proved and entered as typed terminals (fork 9), or a ratified log (R6 b).

**DP-7 · OVERREACH. The SHA-256 analogy.**
- It holds for PORT-REACHABLE: a witness pair is public and cheap to re-check.
- It fails for PORT-FREE. SHA-256 forces the cheater to search 2^128 cases. Here the honest party does the searching, and the law's author hides the needle: a 2,001-value domain finds MAGIC with chance 1.1e-16. Each PORT-FREE is a fresh conjecture that nobody attacks.
- The falsifiers:
  - PORT-FREE: a log pair, as hard to find as the search itself;
  - a certificate: a checker defect, seen only by discharging again;
  - ACCIDENTALLY-CONSTANT: none;
  - R13: cannot fire (DP-14).
- IMPRECISION: Rice's theorem has no instance in a total, finite-state language (DOCTRINE T0). The obstacle is cost.

**DP-8 · FATAL. "Exhaustively over the bounded state space".** R9 bounds operations per tick, and it is optional; the obligation quantifies over states. `b_scale.py`:
- the reference runs about 2.2e5 ticks/s (software timing, clock step 1e-7 s);
- one Int variable with one Int port is 2^128 cases, about 5e25 years, which is the cost of a SHA-256 collision;
- fall.orl's assigned state is 321 bits, leapfrog's 448;
- overflow refuses, so translations are not total: fall.orl starting from x = 2147483645.0 is REFUSED OVERFLOW, where 0.0 completes;
- Q31.32 breaks scaling: (a·x)·y ≠ a·(x·y) in 66,651 (a=3) and 62,663 (a=0.5) of 100,000 draws.

**DP-9 · FATAL. Orbits.**
- Invariance makes a claim constant on each orbit, but independence needs it constant across orbits.
- That takes at least |logs|/|G| checks, or a group transitive on log sequences: 2^64,000 elements for R12's 1,000-tick log of one Int port.
- A handful of generators divides the space by at most |G|. fall.orl, even granted 2^64 x-translations, keeps 2^257 orbits.

**DP-10 · FATAL. Noether.** `c_noether.py`:
- **Equivariance without conservation.** fall.orl translated by 5.0 in x gives 2,942 events: 2,540 identical, 401 differing only in x by exactly 5.0, and one Say line. Meanwhile vx falls from 2.0 to 0.1758 through 311 values. The update is equivariant, yet momentum is not conserved (friction).
- **Energy.** Every tick block is time-autonomous (D2), so the channel would grant energy conservation to every law.
  - Yet leapfrog's energy wanders between 0.538976 and 0.539200 over 1,000 steps.
  - A fixed-step symplectic, momentum-preserving scheme cannot conserve energy on a non-integrable system (Ge & Marsden 1988).
- **Conservation without equivariance.** T7's guards conserve under any position-dependent pairwise force (D10).

Noether needs an invariant action, not an equivariant update. This restores the attribution L14 withdrew.

**DP-11 · FATAL. The front-end plant** (`d_frontend.py`, four executions):
- **leapfrog as written:** REFUSED INDEX-OUT-OF-RANGE at §9.2.1 on step 1; the guard never runs.
- **V1, neighbour index made by Increase:** MUST-FAILED at the guard. The plant rewrote the guard's sum into v1 − v2 − v3, while the ±J update still conserves.
- **V2, the sums made by Increase too, 1,000 steps:** REFUSED OVERFLOW at §11.2.4 (the springs now repel). The guard held at every step reached.
- **V2, 100 steps each way:** COMPLETED, reversibility true, four executions agreeing, output wrong.

Conservation catches a front-end defect only when the defect rewrites the check.

**DP-12 · FATAL. A symmetry certificate does not ride the certificate channel.**
- T1's certificate is a check written in the program and evaluated at this input. Nothing in the language quantifies over states or applies the tick to σ(s).
- Its only T1-native form is a doubled law. fall.orl with x2 = x + 5.0 reads true in 400 of 400, unplanted and planted, with four executions agreeing and the output wrong (`d_frontend.py`).
- An external 2^k discharge entering the court is a new kind of terminal: fork 9.

**DP-13 · OVERREACH. New grounding states.**
- ACCIDENTALLY-CONSTANT is a search report whose name asserts constancy and a cause, and neither is measured.
- A third grounding value needs a rule for mixed premises in the least fixed point (T12); no paste gives one (IMPRECISION).
- A search result shown beside a standing reads as one (R-12; VERDICT).

**DP-14 · FATAL. Sealed equivariance and R13.**
- **The seal.**
  - A certificate must name the law it certifies, or it can be lifted to another (L4, L8).
  - Naming the seal that covers it requires a SHA-256 fixed point.
  - Naming the law without its certificate is buildable. But then every claim seal covers the checker's seal, and a re-discharge or checker upgrade ends every ratification although no clause changed.
  - The seal covers bytes saying a check passed, not the check itself.
- **R9-bounded:** see DP-8.
- **Physics.** A Galilean boost moves x by u·t, and the law cannot see t (D2). Q31.32 has no continuous rotation. For conservation "automatically", see DP-10.
- **Import.**
  - A certificate from another law grounds nothing here (r6_indirect.py fact 3, `evidence/run1-r6-indirect.txt`, rerun here). Keyed by generator name instead, it is L4's name-keyed ratification again.
  - Equivariance belongs to the whole tick: one added clause voids it, and [0,100]^3 is not closed under translation.
  - No person can inspect a 2^321-case discharge, so the ratifier would in effect sign the checker.
  - "Four-way agreement a bonus" drops R1 and T11's rows. Yet scaling equivariance depends on rounding (DP-8), which is exactly what four executions compare.
- **R13's falsifier cannot fire.** No domain is unbounded: i64 and Q31.32 refuse on overflow, and lists and texts stop at 2^24. A shift outside the certified box refutes nothing the certificate claimed.

**DP-15 · OVERREACH. Novelty.**
- A symmetry declared in a model's text and exploited already exists:
  - Murφ's scalarsets (Ip & Dill, CHDL 1993; FMSD 1996), guaranteed by typing restrictions rather than a 2^k discharge;
  - UPPAAL's scalars (Hendriks et al., FORMATS 2003);
  - TLC's SYMMETRY, which is not checked ("all bets are off": Merz, TLA+ list).
- Equivariance from types: Reynolds 1983, and Wadler's free theorems (1989).
- Checked first-class invariants: Eiffel, JML, SPARK, Dafny.
- Only the ratification is Ørlǫg's own, and it predates this feature.

**DP-16 · FATAL. "Log only what matters" breaks replay.** The second paste would log reachable ports only, the third only the directions that matter. Both contradict RUN-1's Replay theorem and D1: a port the doppler wrongly frees (MAGIC) would be read without being logged.

**DP-17 · FATAL, procedurally (R-14).** 1a is unbuilt, no law can declare a port, and R6's incompleteness has cost no one a grounding. The recorded failures are the sheet's own (DP-4, DP-5): repair them before ruling.

**DP-18 · OVERREACH. Authorship.** One model family would write the domain, the taint rules, the generators and the checker (T11). New here: in-program checks share the front end with what they check (DP-11, DP-12), and the two instruments agreed on PORT-FREE in five rows that the log decides.

## The narrowest version I would not oppose

1. **R6 repaired:** in a run with an input log (any port, or a tick block), no claim is GROUNDED,
2. **except under PREFIX,** decided from the text alone: a claim outside the tick block and every procedure, standing before the first port declaration. Its evaluations precede every input event. Built only on a trigger.
3. **R4 in the court:** an evaluation that refused is named, and its claim is not held.
4. **DOPPLER-0, an instrument for prosecutors.**
   - It compares the court's reading of one claim over pairs of logs drawn from a sealed domain of port values and lengths.
   - Each shift is re-run on four executions.
   - It writes neither court nor ledger.
   - It is admitted only on a trigger.

No symmetry certificate, Noether channel or new grounding state.

**Outcome words:**
- `GROUNDED (before any input: §k precedes the first port declaration)`
- `UNGROUNDED (rests on input log <seal>, unratified: R6)`
- `REFUSED at evaluation <n> (<CODE>): not held`
- `SHIFT IN DOMAIN d=<d> law=<seal words>: §k reads <A> over log <l1> and <B> over log <l2>, each agreed on <m> executions. No standing is changed.`
- `NO SHIFT IN DOMAIN d=<d> law=<seal words>: <N> logs, lengths <a>..<b>; §k reads <A> in all. Not a proof: nothing is said of any log outside d.`
- `INCOMPLETE d=<d>: <n> of <N> logs run; no outcome.`

**Acceptance tests** (each plant must be caught by the row it breaks):
- **AT-1.** LEN with no port, over a 16-tick log, its seal ratified, reads UNGROUNDED. Plant: R6's present trigger, which reads GROUNDED.
- **AT-2.** TERM with a real port over 10^9 reads UNGROUNDED, and DOPPLER-0 over {1, 10^9} prints SHIFT, HELD against REFUTED. Plant: comparing truth per evaluation, which prints NO SHIFT.
- **AT-3.** LEN with lengths {16, 17} in the domain prints SHIFT. Plant: varying ports only, which prints NO SHIFT.
- **AT-4.** PREFIX:
  - a claim before the first port reads GROUNDED over two logs, with byte-identical rows;
  - a claim after it that reads no port reads UNGROUNDED;
  - a claim in a procedure performed in the tick block reads UNGROUNDED.

  Plant: exemption by "reads no port", which lets r6_indirect's claim read GROUNDED.
- **AT-5.** OMIT reads REFUSED at evaluation 17, not GROUNDED. Plant: today's tally.
- **AT-6.** MAGIC over 2,001 values prints NO SHIFT. It is kept as a monitored negative and never counted as a pass (T11).
- **AT-7.** No court output contains PORT-FREE, ACCIDENTALLY-CONSTANT or SYMMETRY, and the court output and the ledger's sha256 are unchanged by a DOPPLER-0 run. Plant: print one of those words.
