# RUN-1, the open run: the rulings it needs (a sheet for the owner, 2026-10-26)

RUN-1 gives a program declared input ports and a tick block, and records every input as an event in the trace. It is
the roadmap's fourth rung, after COMPAT-0 (built, b85df56), HOST-0 and these rulings
(`research/roadmap-debate/VERDICT.md`). Every one of the five uses (a game or reality engine, a language, an API, an
editing interface, tools for testing) needs it, and none can be reached from today's closed programs. It is also the
hardest thing to add later: it fixes the next receipt, the next trace and the shape of every API built after it.

This sheet asks for the owner's word on each choice RUN-1 must make. Each ruling gives its options, what each entails,
the theorem or design under it, a falsifier, and a recommendation. Rule with the numbers ("R1 b, R2 as written, …"), or
"as recommended" for any group. Nothing here is built, and nothing changes until he rules.

**Ruled so far:** R3 a (2026-10-26).

**Fixed whatever is ruled:**
- **COMPAT-0 must hold.** Every text v0 accepted keeps its law bytes and its run. RUN-1's forms are therefore spelled
  only where v0 refuses SYNTAX at the statement itself, so they take no meaning away from an existing text.
- **No word is newly reserved.** fall.orl names its loop variable `tick`, and COMPAT-0's plant reserve-tick shows that
  reserving the word would break it.
- **Measured** by `research/run-1/probe_spellings.py`, output in `probe-spellings.txt`:
  - every recommended spelling below is refused SYNTAX at the statement by v0;
  - no line of COMPAT-0's 3,361 frozen texts has any of these forms;
  - the call-shaped candidates ("Receive …", "Take …") are refused UNKNOWN-PROCEDURE instead, because v0 reads a
    statement whose first word is not reserved as a call. They are excluded.

## The theorems RUN-1 rests on

| theorem | what it says | what would falsify it |
|---|---|---|
| **Replay** | every value from outside becomes an event before it is read, so a run is a function of the law and its input log alone, and the trace head commits to both | a recorded log whose receipt differs between two runs, or between two of the four executions |
| **Alignment** | inputs are addressed by (tick, port), never by the order a law happens to read them, so an edited law re-runs over an old log tick for tick | a law edited outside its port declarations that reads an old log out of step (a plant: a misaligned entry, which must be refused, not shifted) |
| **Tick termination** | every loop is bounded and there is no recursion, so every tick ends | a tick that does not end: impossible by construction, held by SPEC's bounds |
| **Capability** | a law reads only the ports it declares | a port read that is not declared, refused at compile time |

These are DECLARED. The arbiter would MEASURE replay per session, four ways.

## Before 1a: the reference and the specification

### R1. Where a world's properties live
The skeptic's question: is a property such as gravity part of the law, of its inputs, or of a data section sealed
apart?

| option | entails | design |
|---|---|---|
| a. In the law, as today | nothing new | the seal names the whole world, but every property change makes a new law: previews rebuild (0.33–1.3 s, the skeptic's measurement), and every ratification of its claims ends |
| **b. A port read once, before the first tick:** `Let gravity be given as a fixed.` | the value lives in the input log's header; the law's seal stays the same when the value changes; the receipt names the log's seal | one mechanism for both kinds of port: one input door, one encoding, one event kind. A "data section" is the log's read-once ports |
| c. A third file, a data section sealed apart | a new artifact type with its own seal, door and receipt line | the same effect as b, with one more format to keep |

**Recommended: b.** The trade-off is that a property moved out of the law leaves the law's claims conditional on the
log, and the court must say so (R6). **Falsifier:** change a read-once value and the law seal moves, or a claim reads
GROUNDED on the strength of the log.

### R2. The spellings
| form | spelling | v0 (measured) |
|---|---|---|
| a port read each tick | `Let thrust be given each tick as a fixed.` | SYNTAX at the statement |
| a port read once | `Let gravity be given as a fixed.` | SYNTAX at the statement |
| the tick block | `Each tick, do the following.` | SYNTAX at the statement |
| the tick block with a budget (R9) | `Each tick, at most 100000 operations, do the following.` | SYNTAX at the statement |

- **Types:** `an integer` and `a fixed` are v0's own words. `a truth value` and `a text` are new, inside the port form
  only, and reserved nowhere else. Float ports are R8.
- **Places:** ports at the top level, before the tick block; one tick block, the last top-level clause. New compile
  codes go into SPEC §13's phase table in the same change:
  - PORT-PLACE: a port elsewhere;
  - TICK-PLACE: a tick block elsewhere, or a second one;
  - PORT-VARIABLE: a port assigned. A port is read-only, as a For counter is.
- **Rejected spellings:**
  - `For each tick, do the following.` is SYNTAX in v0 too, but a For loop that lost its bounds would silently become
    a tick block.
  - `On each tick, …` is SYNTAX in v0, but its first word is not reserved.
  - `Receive …` and `Take …` are calls in v0.

**Recommended: the spellings above.** **Falsifier:** COMPAT-0 BROKEN after 1a, or any frozen text newly refused with a
v1 code.

### R3. How input text becomes a value
| option | entails | design |
|---|---|---|
| a. Exact or refused (the conversion rule) | a decimal that is not exactly a Fix value is refused at the door; the log never holds a rounded value | rounding is forbidden. Inputs must arrive already on the 2^-32 grid, or as raw values |
| **b. Rounded once and noted (the literal rule)** | the door rounds half-even, as for a literal, writes the rounded value into the log and a note into its report | rounding is visible and recorded, never silent. An input is text someone wrote, and a literal is treated the same way |

Either way the log holds typed encodings only (RUNTIME-SPEC §5), written once by a Python input door, so no runtime
ever parses decimal text and no host's strtod can diverge. **Recommended: b**, consistent with literals (SPEC §5:
"Fix stores the nearest raw value, ties to even"). **Falsifier:** a backend that parses decimal input (a plant, which
must be caught), or a rounded value with no note.

**Ruled 2026-10-26: a, against the recommendation.** His words: *"I rule in favor of Option a (The Conversion Rule) for
R3."* His reasons, in his words: *"The true, structural differentiator is reversibility under COMPAT-0 and the
preservation of data provenance."* Option a *"treats rounding as a client-side capability rather than an engine-side
compromise."*
- **What it settles.**
  - The door never rounds. A decimal that is not exactly a Fix value is refused, and inputs arrive on the 2^-32 grid
    or as raw values.
  - The log holds only values the supplier sent.
  - A later version may relax this to rounding as an extension, refused becoming accepted. The reverse would break
    every recorded log (COMPAT-0's rule).
- **What falls away.** The rider proposed under b, keeping the supplier's original text under a seal so that a rounding
  stays auditable, is not needed: no value is rounded.
- **The falsifier, under a.**
  - A value in the log that is not exactly the one its text names (a plant: a door that rounds).
  - A backend that parses decimal input.
- **The enactment.** His message opened with the door's grammar: *"The entrance tool filters all incoming port streams
  using a restrictive ASCII regular expression sieve. This occurs before passing strings to Python's Fraction
  constructor, neutralizing format exploitation"* (Python's `Fraction` alone accepts `1e3`, `3/4`, ` 1.5 `, `+1`,
  `1_000` and the Arabic-Indic digit `٣`: measured in the walk-through). The message was cut off there, and he gave
  the other five the same day, as "now finalized for the input door under Option a", in his words:
  - *"Double-Bounded Range Checks: The door must explicitly validate that the parsed value sits securely within the
    strict raw storage parameters of the `Fix` bounds (`MIN_FIX_RAW` and `MAX_FIX_RAW`), actively protecting the lower
    negative boundary against floor overflow errors down to −2147483648.5."* In the code the bounds are
    `numeric_ref.I64_MIN` and `I64_MAX` on the raw value: `-2147483648` is accepted (raw −2^63), and
    `-2147483648.5` is refused.
  - *"Integer Port Restrictions: An incoming string hitting a port explicitly typed as `an integer` must fail
    instantly if a fraction or decimal component is detected. Truncation or automatic floor-rounding at the gate is
    blocked."*
  - *"Boolean Uniqueness: Truth-value channels accept exactly one invariant string spelling for `true` and one for
    `false`. Alternative representations, case variations, or numeric bits (`1`/`0`) are refused."*
  - *"Text Byte Purity: String inputs are preserved byte-for-byte as sent. Non-NFC unicode payloads generate an
    explicit report note; CP1252 character maps are rejected outright."* The note needs no seal of its own: it can
    be recomputed from the logged bytes.
  - *"Raw Value Spellings & Neighbor Refusals: Raw hexadecimal scalar strings are given an isolated syntactic prefix
    that the text grammar tracks separately from standard base-10 decimals. When a user input is rejected for
    non-alignment with the 2^-32 fixed-point grid, the door's refusal message must explicitly compute and output the
    two nearest valid representable grid coordinates to the client."*

  Left for 1a's specification, each a detail his words fix in kind but not in spelling:
  - the one spelling each for true and false;
  - the raw prefix, and how a raw value's sign is written;
  - whether text also refuses what the literal door refuses (format characters other than ZWJ and ZWNJ, Hangul
    fillers, line and paragraph separators).

### R4. What a refusal does in a run with ticks
| option | entails | design |
|---|---|---|
| **a. It ends the branch** | the run stops at the refusing tick; the receipt says REFUSED code, clause and tick; recovery is a new branch from an earlier snapshot (SNAP-1), and the refused branch stays in the record | the refuted claim's evaluation stands |
| b. It rolls the tick back and the run goes on | friendlier to a game loop | it erases the refutation: the court would read "true in n of n" for ever. A rolled-back refusal is a laundered verdict |

**Recommended: a.** **Falsifier:** a session whose court reading omits an evaluation that refused. *(Note,
2026-10-26: the doppler debate found this falsifier already firing in version 0 (DP-5). A claim whose evaluation
refused partway read "true in 16 of 16" and GROUNDED. The court's R8 now names that evaluation and does not hold the
claim: `evidence/court-r8.txt`.)*

### R5. Versions and headers
- `orlog-law 1`, only when a v1 form appears, so v0 laws stay byte-identical. It adds the law lines
  `(port <var> "<name>" <type> each-tick|once)` and `(tick <clause>[ budget <N>])`.
- `orlog-trace-1`: `head0 = SHA-256("orlog-trace-1" || law_seal)`. New events: `'T'`, the tick number (u64); `'N'`, a
  port's value (u32 var and the value encoding of RUNTIME-SPEC §5). Each tick emits `'T'`, then one `'N'` per
  each-tick port in declaration order, then the body. The read-once ports' `'N'` events come before the first `'T'`.
- `orlog-receipt 1` adds `ticks <n>` and `input-log-sha256 <hex>`. It replaces `output-sha256` with `output-chain
  <hex>`, where out_t = SHA-256(out_{t−1} || SHA-256(the output of tick t)). A snapshot then carries the output as one
  hash; a plain running SHA-256 would need a hash midstate, which CPython's hashlib cannot export.

**Recommended: as written.** **Falsifier:** any v0 receipt or law byte changed (COMPAT-0), or a snapshot that cannot
reproduce the output chain.

### R6. What the input log is to the court
| option | entails | design |
|---|---|---|
| **a. Data, never a channel** | in a run with an input log (the law declares a port, or has a tick block), no claim is GROUNDED, whatever its channel and whatever is ratified, except under the licence below; the court shows the log's seal as provenance: "rests on input log <seal>, unratified" | replayable is not admissible (DOCTRINE T12, limit 4). A log is a value chosen by whoever ran the session, and it can never raise a standing |
| b. Testimony | a person may ratify a log's seal ("this is what the sensor recorded"); a claim over that log could be GROUNDED only with both its own seal and the log's ratified | the supplier's word becomes explicit and signed, as the ledger makes a ratification. That is a court change, in the territory of typed terminals (DOCTRINE §9, fork 9) |

**Recommended: a for RUN-1; b as a later fork.**
- **The trigger is any input log.** A tick block with no port still takes input, because the log's length sets how
  many ticks run (D3). A claim in it can hold over 16 ticks and be refuted at 17.
- **The licence, PREFIX**, decided from the text: a claim is exempt only if every evaluation of it precedes the first
  input.
  - It must stand before the first port declaration, outside the tick block.
  - It must not sit in a procedure performed at or after the first port declaration. The licence is decided by
    evaluation, never by position alone: a claim inside a procedure stands textually before the tick block and still
    runs during it.
  - Nothing the log sets exists before its first input, so a prefix claim's whole claim line is fixed by the law: its
    evaluations, its trues, its cost and its certified clause's cost.
  - A wider licence would exempt a claim with no path from any port, shown by two independent derivations, and must
    then cover the whole claim line, since a certificate's cost reading can move with a port while its truth does not.
    It waits for a trigger (`research/doppler/VERDICT.md`).
- **Falsifier:** a claim in a run with an input log that reads GROUNDED outside the licence. The acceptance rows:
  - a claim that reads only `x`, where `x` is updated from a port, rests on the owner and has its own seal ratified,
    reads UNGROUNDED;
  - a claim in a tick block with no port reads UNGROUNDED (plant: the trigger "declares any port");
  - a claim in a procedure performed in the tick block reads UNGROUNDED (plant: licensing by clause position);
  - a claim before the first port, in a procedure performed after a port is read, is not licensed (plant: "before the
    first port declaration is enough").
  The narrow wording below is that row's plant, and must be caught.
- **Sound, not complete.** Rule a never reads a false GROUNDED, but it also withholds grounding from a claim that
  depends on no port at all. That is a known limit. The backward slice (fork 4) lifts it: a claim whose evaluation
  provably depends on no port could be groundable again.
- **Time and randomness add no second case.** No runtime reads a clock, the environment or entropy (RUNTIME-SPEC §1).
  Under RUN-1 they could enter only as ports (D7), so they fall under this same rule.

*Amended 2026-10-26, before any ruling.* The first wording read: "a claim whose condition reads a port stays a claim of
the program's computation and is never GROUNDED". It misses dependence through state. A claim about `x` never reads the
port, but its truth depends on the log once `x` is updated from the port, and the court sees only direct, declared
dependence (L10). `research/run-1/r6_indirect.py` measures this in version 0, with the port played by a variable set
once from a literal (`evidence/run1-r6-indirect.txt`):
- the claim's condition reads `x` alone;
- its truth turns on the stand-in, holding at 1 and 2 and refuted at the 17th tick at 6;
- with its own seal ratified it reads GROUNDED. That is legitimate in version 0, where the value is in the ratified law
  and a different value gives a different claim seal.

With a real port the law and the claim seal stay the same for every log, so the narrow wording would let that claim
read GROUNDED over a log nobody vouched for. A control shows the narrow check itself works: it does withhold grounding
from a claim that reads the stand-in directly.

*Amended again 2026-10-26, after the doppler debate, before any ruling* (`research/doppler/VERDICT.md`):
- **The trigger** was "declares any port". It missed a tick block with no port, whose log's length is input (DP-4).
- **The licence (PREFIX)** was added, decided by evaluation (N-1) and covering the whole claim line (N-2). The debate's
  proponent and adversary both arrived at it, and the adversary's fixtures measured each hole. The judge reran the
  procedure case and the cost case.

### R7. A twin round before the backends
| option | entails | design |
|---|---|---|
| **a. A paper round first** | the twin's author reads SPEC §15 alone and hand-works probes before 1a's code is final; each difference is settled in writing, as in rounds 1 to 3 | the cheapest time to find a misreading of §15 is before three generators and two runtimes encode it. Every earlier round found reference defects and open readings (62 notes; then 163 and 128 probes) |
| b. After 1b | faster to a first session | readings would be settled against code that already exists in five places |

**Recommended: a**, the skeptic's "hold the twin's paper round first". **Falsifier:** a §15 reading that the twin and
the reference work differently and that §15 does not settle.

## Before 1b: the backends

### R8. Float ports
| option | entails | design |
|---|---|---|
| a. Allowed | the door converts decimal text to binary64 (correctly rounded, noted) or takes the bits; a NaN is refused at the door | floats meet inputs before any second host has measured them |
| **b. Deferred** | v1 ports are Int, Fix, Bool and Text; Float ports wait for HOST-0 and for fork 3 (floats in identity) | the owner's "pays twice" argument favours a sealed fixed-point dialect for simulation. Floats across hosts are NOT_MEASURED, and flush-to-zero is not checked (DOCTRINE T5) |

**Recommended: b.**

### R9. A budget per tick
| option | entails | design |
|---|---|---|
| a. None in the law | every tick ends anyway (bounded loops, no recursion), and the host's budget stops a session without a verdict (STOPPED-BY-HOST) | the host's stop is not the law's verdict, so a slow tick is never a refusal |
| **b. Optional in the law:** `Each tick, at most N operations, do the following.` | a tick past N refuses TICK-BUDGET: an event in the trace, at the same operation on every execution, because operations are counted, not timed | the owner's measure: "a tick that exceeds its budget produces a signed refusal event, never an overrun". The budget is in the law, so the seal covers it |

**Recommended: b.** **Falsifier:** a tick over its budget that runs on, or whose refusal comes at a different
operation in two executions.

### R10. What an input log is bound to
| option | entails | design |
|---|---|---|
| **a. The port signature** (names, types, kinds, order; its sha256 in the log's header) | an edited law with the same ports replays an old log; a different signature is refused PORT-SIGNATURE | alignment: an edit's preview runs the candidate law over the world's own log. That is EDIT-0's preview and the App Studio's cheap exploration |
| b. The law seal | every edit invalidates every log | strict, but no edit could ever be previewed against a recorded session |

**Recommended: a.** **Falsifier:** a log replayed against a law whose ports differ, without a refusal.

### R11. Build identity by the law
The skeptic's step: pass the text seal to the compiled program at run time instead of compiling it in, so that editing
a note stops rebuilding both compiled backends (1.71 s measured). It changes `orl_init`'s arguments, which 1b changes
anyway for the input log's path, so the two changes become one revision of the runtime contract. **Recommended: yes, in
1b.** **Falsifier:** a note edit that rebuilds a backend, or a receipt whose text seal differs from the reference's.

### R12. RUN-1's admission record (DOCTRINE §9, fork 8)
Proposed record:
- **Trigger:** all five uses need input, and none is reachable from a closed program (the architect and the skeptic
  independently).
- **Discriminator:**
  - COMPAT-0 HELD after 1a and after 1b;
  - a recorded 1,000-tick log gives byte-identical receipt 1 on all four executions;
  - each plant caught: a dropped `'N'` event, located at its first divergent event; a backend that parses decimal
    input; a misaligned log entry, refused rather than shifted; a tick over its budget that runs on; R6's narrow
    wording, which lets a claim that depends on a port only through state read GROUNDED; R6's present trigger, which
    misses a tick block with no port; licensing by clause position;
  - **the court one-sided.** RUN-1's floor (R6) only withholds. Measure it as `tests/court_monotone.py` measures R8:
    over COMPAT-0's frozen texts and its own fixtures, no standing may be gained in any of the three orders (support
    with CIRCULAR, grounding, held), every changed reading must be counted, and two plants must be caught: a comparator
    blind to CIRCULAR, and a court that grants (the reporting pass's finding 12 replaced a plant that read the
    measurement backwards). The licence grants by design, so it is held instead by its own rows above.
- **Scope:** `src/`, `rt_c/`, `rt_rs/`, `tests/`, SPEC §15, a RUNTIME-SPEC section for v1, a new
  `vectors/input-vectors.txt`. `runtime-vectors.txt` is untouched.
- **Exit:** the discriminator met; the twin's round settled; the self-test green twice and byte-identical.

**Recommended: approve as written.**

## Defaults, stated so they can be overruled

- **D1. Dense records.** Every tick record holds every each-tick port. The door may accept a sparse convenience form,
  but it writes the log dense.
- **D2. The tick number is not visible to the law.** A law that needs it counts ticks itself, so no new expression is
  added.
- **D3. No end-of-session block.** A run completes when its log ends.
- **D4. OUTPUT-TOO-LONG per tick**, 2^30 bytes, not per run: SPEC §7's total would end any long session.
- **D5. Binding a port counts 0 operations**, as reading a variable does.
- **D6. State.** Persistent state is the top-level variables declared before the tick block. The tick block opens a
  scope, as every block does (SPEC §5), so its own Lets are made afresh each tick.
- **D7. Not in v1:** list ports; clock, random and file ports. Randomness is a seeded read-once port and a PRNG written
  in the law. Also not in v1: a pull-style input statement, which would break alignment.
- **D8. Claims.** A claim in the tick block is evaluated each tick, and the court reads it as "true in n of n" over the
  session. A claim before the tick block is evaluated once.
- **D9. The log's source.** Input values arrive as strings, never as JSON numbers, since an i64 above 2^53 does not
  survive a JavaScript client. The door reads one JSON object per tick and writes `orlog-inputs 0`.
- **D10. Two commits.** 1a holds the reference and SPEC §15, with COMPAT-0 green; until 1b, the court reads v1 runs as
  REFERENCE-ONLY and holds no claim. 1b holds the backends, the runtimes and the input vectors.

## What this sheet does not decide

- Snapshots, sessions and the test socket (SNAP-1, SESSION-0, RPC-0): later rungs, which RUN-1's formats are shaped to
  serve.
- Distribution: networked play, a remote ledger, a listener reachable from another machine.
- Whether a log can ground a claim: R6 keeps it from doing so in RUN-1.
- Anything about intent. A port declares what a law reads, not what its author meant the world to be.
