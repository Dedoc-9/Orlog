# How RUN-1 reconciles with floating point: an adversarial reading and a consensus (2026-10-26)

The owner asked how the contract reconciles with floating point. He forwarded four texts, which are paraphrased
here, never quoted:
- an outside reviewer's proposed rulings for the held decisions;
- the reviewer's proposals to advance the fourteen recommendations;
- a three-guarantee account of floating point (bitwise, semantic, tolerance);
- a proposed numerical assurance layer, "Nexus", with a decision firewall, a numeric cut and an N0 to N4 ladder.

He asked for Verðandi's lessons to be used, for a web search, and for an adversarial reading ending in a consensus.
Nothing here is ruled.

## 1. What Orlog already fixed (read in the code, and measured)

DOCTRINE T5, *Determinism by construction, in fixed and floating point*, already sets the numeric layer:

| type | arithmetic | how determinism is held |
|---|---|---|
| **Int** | checked i64, exact division, Euclidean quotient and remainder | exact |
| **Fix** | Q31.32: raw i64 / 2^32, each product and quotient rounded once, half to even | exact on the raw integers |
| **Float** | binary64, the basic operations only (`+ − × ÷ √`), every NaN canonical, decided on the bits | each operation correctly rounded by IEEE 754 in all three languages |

The rules around them:
- no library transcendentals;
- no contraction: the C backend is built `-ffp-contract=off -fno-fast-math` (`src/orlog/arbiter.py`, `C_FLAGS`);
- conversions exact or refused unless `rounded` is written;
- literals rounded once, and noted.

The evidence, MEASURED on this host:
- 20,015 vectors pass in the C and the Rust runtime, each at two optimisation levels;
- a second, independent derivation and 113 hand-worked cases agree with the vectors;
- under `-ffp-contract=fast -march=native` a naive C loop diverges, while the C Ørlǫg generates has no FMA instruction.

T5 states its own limits: no other host is measured, and flush-to-zero is not checked at run time. R8 recommends
deferring float *ports* until HOST-0.

**MEASURED again here, for this question** (`probes/float_decision.orl`, `probes/fixed_decision.orl`, `orl.py run
--show`). Every result below came out the same in all four executions (the reference, Python, C99, Rust):

| law | result |
|---|---|
| floats: `0.1 plus 0.2` against `0.3` | `float: not equal` |
| the same float, `as a fixed` | REFUSED INEXACT-CONVERSION, all four alike |
| fixed: `0.1 plus 0.2` against `0.3` | `fixed: equal`, since each literal rounds once to the 2^-32 grid |
| fixed: `0.1 plus 0.1 plus 0.1` against `0.3` | `fixed: three tenths not equal` |

The four executions agree on a decision that exact real arithmetic would make differently. That is T11's lesson in
numbers: **agreement is determinism, not accuracy.** And a binary fixed-point grid does not make decimal tenths exact.

## 2. What Verðandi learned (read in its records; its code was not run)

Verðandi's graybox ran the experiment these texts propose (`graybox/README.md`, *The simulation's contract: rules 1*).
The owner's ruling of 2026-10-11, in his words:
- *"investigate and implement the deterministic math layer now"*;
- *"Keep the scope limited to authoritative state, and let the measured divergence—not a blanket desire for identical
  math—determine which operations need replacement"*;
- *"if the contract is cross-browser deterministic simulation, test state transitions and serialized state—not just a
  handful of function outputs."*

What followed:
- **The divergence was measured.** Two V8 versions differed on `Math.sin` and `Math.cos` by one unit in the last place,
  on a few arguments in a hundred. Firefox against Chromium differed on `Math.hypot` for about a quarter of its
  arguments (R-6).
- **The replacements were built from fixed operations only.** `sin`, `cos` and `atan2` are fdlibm's algorithms, written
  in the language's own correctly rounded operations. `sqrt` and `hypot` are correctly rounded through integer square
  roots. Every constant is written as its bits, and no literal has more than 20 significant digits.
- **A `math-fence`** makes the engine's 23 approximated functions throw, and every run must replay the same states
  under it. A plant tick that calls `Math.cos` is caught.
- **A counterfactual engine** perturbed the last bit of every `sin`, `cos` and `hypot` call. The state's bits parted at
  tick 1172 of 1787 and ended 2.8 × 10⁻¹⁴ m apart, with no cell, footing or hit different. The decisions held while
  the bits did not.
- **NaN is refused at the input,** because the language does not fix a NaN's bits.

Verðandi's other lessons that apply here:
- **Hash whole numbers:** a value the GPU interpolates is not exact, and hashing it scattered results into noise
  (lesson 72).
- **Square roots:** compute them with `math.sqrt`, correctly rounded on every machine, never with `**` or `pow`
  (REACH-1).
- **Numbers are read as the decimals written:** never with `float()` alone, and never compared as doubles (the art
  file's NUMBER grammar, HELD-0).
- **Predicates on shapes are exact:** integers and fractions, never a float compared (MARK-0).
- **Never claim determinism across platforms or browsers** without the measurement (Verðandi's AGENTS.md §3).
- **A model proposes, the host decides:** "A provider proposes; nothing it says reaches the world but through the
  gateway's reading and the director's verdict", and no model may supply a rung, a record or a detector reading
  (STUDIO, ADMISSION-0).

## 3. What the web adds (searched 2026-10-26; secondary sources marked)

- **Reproducibility needs everyone's cooperation.** IEEE 754-2019's reproducibility clause gives reproducible results
  only for programs reliably translated into reproducible operations on reproducible formats, and it needs the
  language, its processor and its user to cooperate. C++ does not specify floating-point behaviour at all, which the
  WG21 "reproducible floating-point results" papers (P3375) set out to change. This is secondary: the primary clause
  was not found.
- **Correctly rounded math libraries are still arriving.** CORE-MATH's correctly rounded binary32 functions entered
  glibc during 2025, with more under review in 2026. A platform's `sin` is not yet a fixed function, and Verðandi's
  measured divergence agrees.
- **Rust leaves a NaN's bits nondeterministic,** even between compile time and run time (RFC 3514). Orlog's
  canonical NaN, decided on the bits, is required, not cosmetic.
- **FMA contraction changes results,** and clang's default contraction depends on a pragma; contraction once broke
  AArch64 test bots that compared bits. Orlog passes `-ffp-contract=off` explicitly. Rust does not contract unless
  `mul_add` is written (from memory, not re-read).
- **Directed rounding can be simulated** with round-to-nearest, using widened bounds (Rump and Zimmermann, 2007).
  Widening by one unit in the last place is sound only for operations whose error is below it, as correctly rounded
  basic operations are.

## 4. The adversarial reading

### Against the three-guarantee account

- **Tolerance-based agreement is rejected.** A tolerance between executions is a lenient comparison, the class of
  defect E7 named: a CRLF receipt once counted as agreeing.
- **"Same decisions, different intermediates" is incoherent in Orlog.** The trace commits every value an assignment
  makes (`'A'` events carry value encodings), and the owner's R5 ruling keeps the per-event chain. An intermediate
  difference changes the trace head and reads as a dissent. Allowing it would mean dropping values from the trace,
  which is the localisation the owner ruled to keep (*"destroys our core epistemic edge"*).
- **The guarantee that remains is bitwise.** It holds for everything committed, with T5's restricted operations as
  the only floats.
- **Its advice on integer scaling is right, but the scale must be the domain's.** Q31.32 is a binary grid, and
  measured, `0.1 plus 0.1 plus 0.1` is not `0.3` in it. A domain of tenths or cents decides in Int, counted in its own
  unit.

### Against Nexus

- **The decision firewall answers a different question.** In Orlog the four executions already agree bit for bit, so
  the firewall would not remove a cross-backend divergence; there is none to remove. What it adds is accuracy: whether
  a float decision equals the one exact real arithmetic would make. That is worth having where a law needs it, but it
  is not determinism, and the pitch runs the two together.
- **Its own verdicts must be deterministic.** Certified, inconclusive or refused must come out the same in all four
  executions, or the firewall becomes a new source of dissent. Built from correctly rounded basic operations with
  widening that is outward by construction, it is. Built on a platform `sin`, it is not (CORE-MATH, R-6).
- **It belongs in the law, not the runtime.** It can be written in Orlog from the basic operations, as Verðandi wrote
  fdlibm in its own operations. A refusal it causes is an ordinary refusal, with its code and the cut, so CUT-0 needs
  no separate numeric-cut format.
- **"Refuse when inconclusive" is a new way to end a session.** An input that lands near a boundary would end the run
  (R4), the same question A2 answered for malformed input. Each law or door must choose it openly, never as a hidden
  default.
- **The N0–N4 ladder is a scalar scorecard,** which the lineage's discipline forbids ("Report witnesses side by side").
  Its rungs are not ordered: Orlog has determinism (N1) and portability on one host (part of N4) without error bounds
  (N2). Keep the five properties as separate witnesses.
- **"A model proposes, a verifier decides" is right, and not new.** It is Verðandi's studio rule (section 2). Adopt
  the rule; no new layer is needed for it.

### Against the fourteen advancements

Most already exist in this round's records:

| advancement | where it already stands |
|---|---|
| the replay verifier | `verify_session` and the transition system in `probes/cut0_session.py` |
| the evidence graph | the two-layer binding |
| the canonical bijection | `parse_log` and `serialize`, with every single-byte mutation and the adversary's 217 multi-byte edits |
| the meter's conservation | T6's identities, checked over every legal history |
| the verifier of the proof-carrying cut | the court computing K̂ from the law and the cut, with the resumption oracle beside it |
| bounded model checking | the exhaustive domains (76,364 histories) and the congruence to 14 events |
| the impact engine | **Verðandi's RUNG-0** (`tools/rung.py classify`: a change's rung from the trusted base's closure and the change's meaning), a transfer candidate for Orlog |
| refinement guided by counterexamples | how C2 became CUT-0 |

**The one addition taken:** each consumer of the shared reach analysis (`Reach`) states its own soundness
requirement. CUT-0 and PREFIX need an over-approximation; a future use might not.

**The one point not ours:** "ten refusals in one tick" is no part of the held decisions.

**The proposed compatibility classifier** (SAME, COMPATIBLE-EXTENSION, BREAKING) **is premature.** R10 a reads every
port-signature change as breaking, the simplest sound rule. The edits that must cross a change belong to the later
port-adapter fork.

## 5. The consensus proposed

| # | position | grade of its basis |
|---|---|---|
| F1 | **Bitwise reproducibility of everything committed** (trace, receipt core, tick lines) across the four executions, **under a declared execution profile:** the law, the log, the version, and each execution's build. No tolerance, and no "same decisions, different intermediates": R5's per-event chain rules both out. The receipt core stays portable, with no host identity in it. Which executions agreed, and on what hosts and builds, is the arbiter's agreement record, never the receipt's (`ROUNDS.md`, the review's point 1). The evidence today is one host: the guarantee is the requirement, and its measurement grows with HOST-0 | ESTABLISHED (T5, R5); MEASURED on one host |
| F2 | **Determinism is not accuracy.** No receipt or court line claims a float decision equals exact arithmetic | MEASURED (`float_decision.orl`: agreed four ways, inexact) |
| F3 | **A decision that must be exact uses an exact type in the domain's own unit:** Int counted in cents or tenths, or Fix where the domain is dyadic. Conversions stay exact or refused, and the door exact or refused (R3 a) | MEASURED (INEXACT-CONVERSION; three tenths in Fix) |
| F4 | **Floats stay as T5 has them:** the basic operations, a canonical NaN, no contraction, no platform transcendental. A law that needs `sin` writes it from the basic operations, as Verðandi's rules 1 did, chosen by measured divergence in the owner's words. Its admission record names the algorithm and its provenance (for example, fdlibm 5.3 and its revision). **The limit, kept permanently:** identity of algorithm, constants and operations gives bitwise conformance between backends, and no accuracy. Accuracy can be checked without circularity on samples, against an independent computation of higher precision (Verðandi measures its `sin` against 70 decimal digits). A bound over every input needs a proof, which no finite test supplies | ESTABLISHED (T5); MEASURED in Verðandi (R-6); web (RFC 3514, CORE-MATH, FMA) |
| F5 | **R8 b stays:** no float ports until HOST-0 measures a second host, an AArch64 host among them, with flush-to-zero checked | DECLARED (one host only) |
| F6 | **Certified enclosures are a later, law-level library,** not a runtime layer in RUN-1. They are written from correctly rounded basic operations with outward widening, so their verdicts are themselves bitwise reproducible, and a refusal they cause is an ordinary refusal with its cut. The widening is derived for each operation it covers, from that operation's error bound. One unit in the last place is not assumed to suffice everywhere: it does for correctly rounded basic operations, whose error is half a unit, and for nothing else without its own proof. What an inconclusive verdict does is written in the law, never a runtime default | DECLARED |
| F7 | **No guarantee ladder:** determinism, portability, error bounds, decision stability and specification completeness are reported side by side | ESTABLISHED (the lineage's rule) |
| F8 | **A model proposes, the verifier decides,** stated once in the contract's preface, with Verðandi's studio rule as its precedent | ESTABLISHED (Verðandi) |
| F9 | **Compatibility is a measurement, not a promise.** A version that claims COMPAT-0 publishes the corpus and its version, the texts tested, the changed texts with their seals before and after, each change's reason and amendment, and the toolchain. The report measures; RULINGS.md says which outcomes are allowed. A strict audit passes only with no change. A justified change is a settled change, reported as such, never counted as none. COMPAT-0 already works this way (`tests/compat/README.md`) | ESTABLISHED (COMPAT-0's design) |

**Does not show:**
- any host but this one;
- that T5's float layer is enough for a law that needs transcendental functions (none here does);
- the primary text of IEEE 754-2019 clause 11, which was not found.

**Falsifiers:**
- two executions whose committed bytes differ under one law, one log and one version;
- a receipt or court line implying accuracy;
- a float port admitted before HOST-0.

## Sources (web, 2026-10-26)

- [P3375R2: Reproducible floating-point results (WG21)](https://open-std.org/JTC1/SC22/WG21/docs/papers/2025/p3375r2.html)
  and [P3375R3](https://open-std.org/JTC1/SC22/WG21/docs/papers/2025/p3375r3.html)
- [Demmel et al., efficient reproducible summation](https://ieeemilestones.ethw.org/w/images/a/ae/Demmel_algors_efficient_reproducible_summation.pdf)
- [glibc: atan2pif from CORE-MATH (libc-alpha, 2025)](https://gcc.gnu.org/pipermail/libc-alpha/2025-January/164423.html)
  and [cosf from CORE-MATH (2026)](https://patchwork.sourceware.org/project/glibc/patch/20260325192357.1284741-6-adhemerval.zanella@linaro.org/)
- [Rust RFC 3514: float semantics](https://rust-lang.github.io/rfcs/3514-float-semantics.html)
- [LLVM D24481: the FP-contraction default](https://reviews.llvm.org/D24481) and
  [cfe-dev: "FP Contract = fast?"](https://lists.llvm.org/pipermail/cfe-dev/2017-March/053108.html)
- [Rump and Zimmermann (2007): interval operations in rounding to nearest](https://www.tuhh.de/ti3/paper/rump/RuZi07.pdf)
