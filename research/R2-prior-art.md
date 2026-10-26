# R2: Prior art and exact technical facts for ØRLǪG

Researched 2026-10-25. **CHECKED**: I read the named source, as a fetched page or a search *extract* quoting it, both through a summarizing tool. **MEMORY**: from training, not re-read. "None found" means the sources read do not say it.

## A. Prose, controlled-language and legal-language programming

|System|What it is, backends|(a) byte-identical on 3+ hosts|(b) runtime receipts|(c) declared FP determinism|
|---|---|---|---|---|
|**Catala** (Merigoux, Chataing, Protzenko, 2021)|A statute DSL built on Lawsky's prioritized default logic, with `exception`, `label`, `under condition` and `consequence` (CHECKED, *extract*). Core compilation steps proved in F* (CHECKED). An interpreter plus OCaml, Python, C and Java backends; R added in 0.9.0; 1.0.0 on 2025-11-10, 1.3.0 on 2026-10-01 (CHECKED).|Only a goal: 1.3.0 says traces from generated code "should be identical" to the interpreter's (Java, Python, OCaml; not C) (CHECKED). No output-identity contract.|JSON trace events (BeginCall, VariableDefinition, DecisionTaken), not hashed (CHECKED)|No floats: integer is `Z`, money is `Z` cents, decimal is `Q` rationals; `round` rounds half away from zero (CHECKED, runtime 1.1.0)|
|**Lexon** (Diedrich, 2018)|Plain-English contracts compiled to Solidity (CHECKED, project *extract*) and Sophia (CHECKED, forum *extract*). lexon.org claims JavaScript output and "100% deterministic", both self-reported (CHECKED).|No|None found|n/a|
|**Logical English** (Kowalski, Dávila, Calejo)|Controlled English as "syntactic sugar" for Prolog. Runs on SWI-Prolog and s(CASP); named rules for exception hierarchies are still on the roadmap (CHECKED).|No|s(CASP) justification trees (Arias et al. 2020; CHECKED): explanations, not receipts|None found|
|**ACE / APE** (Fuchs, Kaljurand, Kuhn)|Parses controlled English to DRS, FOL, TPTP, OWL, SWRL, RuleML and paraphrase (CHECKED)|No (logic, not programs)|No|n/a|
|**Inform 7** (Nelson)|Natural-language source, through Inter and Inform 6, to Glulx or Z-machine (CHECKED). Version 10's `-format=C` emits C for 32-bit targets (CHECKED, forum).|No|No|None found|
|**L4 / Legalese** (SMU CCLaw)|Current docs: `UNLESS` is classical (A AND NOT B), with no priority inference (CHECKED). The 2022 research L4 has rule annotations `subjectTo` and `despite` (the notwithstanding pattern), compiled away to SMT (classical) or ASP (non-monotonic) (CHECKED, paper text). Backends: none found.|None found|None found|None found|
|**Blawx** (Jason Morris, Lexpedite)|A Blockly web IDE over SWI-Prolog and s(CASP), with explanations (CHECKED). Defeasibility uses `according_to`-style wrapping (CHECKED, *extract*).|No|Explanations only|None found|
|**Accord Project Ergo**|Contract logic. Compiler written in Coq and OCaml; compiles to JavaScript; repository archived 2023-09-07 (CHECKED).|No|None found|None found|

- **COBOL** (CODASYL, 1959) has English-like statements and decimal fixed-point PICTURE data. COBOL 2002 added floating point, and COBOL 2014 replaced its portable arithmetic with IEEE 754 types (CHECKED).
- **HyperTalk** (Winkler, 1987, HyperCard) is an English-like scripting language that influenced AppleScript (CHECKED). AppleScript shipped in 1993 (MEMORY).

## B. Verification-aware languages with several backends

- **Dafny.** Documented targets: C#, Java, JavaScript, Python, Go, and C++ with "limited support" (CHECKED, User Guide). Rust has been experimental since 4.7.0 and is still being worked on in 4.11.0, but is not in the documented list (CHECKED, release notes). Agreement between backends is tested, not promised: XDsmith (ISSTA 2022, 31 bugs) and fuzz-d/DafnyFuzz (30 bugs) run programs on every backend and treat mismatches as bugs (CHECKED, *extracts*).
- **F\*** extracts to OCaml or F#. Low\* goes to C (or Wasm) through KaRaMeL, and Vale goes to assembly (CHECKED, README *extract*). KaRaMeL produces readable C (CHECKED).
- **Why3** extracts to OCaml (its main target), to C (partial: no unbounded integers, arrays, datatypes or floats) and to Java (CHECKED).
- **Lean 4.** The toolchain ships `leanc`, a build of Clang (CHECKED). Compiled code goes through C (MEMORY). A new code generator was deployed in June 2025 (CHECKED, FRO roadmap *extract*).
- **Rocq (Coq)** extracts to OCaml, Haskell and Scheme, with JSON for debugging. Its manual warns that axioms and user-supplied realizations are not checked (CHECKED).
- **K framework.** It has a Haskell backend (CHECKED) and an LLVM backend for concrete execution (MEMORY). Chen, Lin, Trinh and Roşu (CAV 2021) generate a proof object for each program execution, which a trusted proof checker verifies (CHECKED, paper text).

**Is identical output across backends a stated contract anywhere?** None found among these. The closest are Catala's goal of identical traces (above); Ethereum's EELS, an executable Python reference whose fixtures validate clients written in other languages (geth, besu, nethermind, reth) (CHECKED); WebAssembly's OCaml reference interpreter, which exists to pin down the exact semantics and runs the spec tests (CHECKED); and Lingua Franca (C, C++, Python, TypeScript, Rust), which promises deterministic concurrency, not identical numbers (CHECKED).

## C. Exact technical facts

**C99.**
- `FLT_EVAL_METHOD` (`<float.h>`): −1 indeterminable; 0 each type in its own range and precision; 1 float and double as double; 2 everything as long double; other negatives implementation-defined (CHECKED).
- `#pragma STDC FP_CONTRACT ON|OFF|DEFAULT` allows contraction, such as an FMA. Its default state is implementation-defined (CHECKED).

**Clang and GCC contraction.**
- Clang documents `-ffp-contract=on` (fuse within one statement, honour the pragma) as the C and C++ default (CUDA `fast`, HIP `fast-honor-pragmas`); the default `-ffp-model=precise` keeps it (CHECKED). Projects saw it take effect from Clang 14, even at -O0 (CHECKED, skcms commit).
- LLVM issue #54927 (April 2022; CHECKED): the front end emits `llvm.fmuladd`, which becomes `fmadd` on AArch64 but a separate multiply and add on the default x86-64 subtarget, which has no FMA. The constant folder fused regardless of target, so compile-time and run-time results could differ.
- So baseline x86-64 never fuses; FMA needs an FMA target such as `-mfma` or `-march=haswell` (MEMORY). Building for x86-64-v3 gained FMA and broke package tests (gcc list, 2023; CHECKED).
- GCC defaults to `off` in ISO modes (`-std=c11` and the like) and to `fast` otherwise; `on` is implemented for C and C++ (CHECKED).

**Rust.**
- RFC 3514, `float_semantics` (started 2023-10-14; merged, as it is in the RFC book; CHECKED): IEEE 754-2008 operations, roundTiesToEven, default exceptions without traps, no flush-to-zero, no other rounding modes. Strict semantics forbid turning `a*b+c` into an FMA without explicit opt-in. A NaN result has a non-deterministic sign, and its quiet bit and payload come from an allowed set (preferred NaN, quieted or unchanged input propagation, target-specific). Const-evaluated NaNs may differ from run-time ones. i586 (x87) and old MIPS do not conform.
- In the f64 docs, transcendental functions have "unspecified precision", which may vary by platform, version and even from call to call. `mul_add` rounds once (CHECKED).

**CPython.**
- CPython has required IEEE 754 floats since 3.11. `repr` has given the shortest string that round-trips, using David Gay's algorithm, since 3.1 and 2.7 (CHECKED).
- `math` is a thin wrapper over the platform's libm, so transcendental results depend on the platform (CHECKED).
- Shortest-digit printers differ: Rust uses Grisu with a Dragon fallback (`flt2dec`), and Java's `Double.toString` may print two digits where one round-trips (CHECKED). Exponent notation differs too (MEMORY).

**int64 to double.**
- C99 §6.3.1.4: exact values are unchanged; otherwise the result is the nearest higher or lower value, chosen in an implementation-defined way; with IEEE arithmetic, round to nearest (CHECKED, cppreference). Annex F ties it to the current rounding mode (MEMORY).
- Rust `as f64` gives the closest value, roundTiesToEven (CHECKED).
- Python `float(int)` has given the closest float since 2.7 (CHECKED), breaks ties to even per CPython's source comment (Dickinson, issue 3166; CHECKED, *extract*), and raises OverflowError when out of range (CHECKED).

**Default NaN.**
- x86 SSE's "indefinite" quiet NaN has the sign bit set: 0xFFF8000000000000 in binary64 (CHECKED: Raymond Chen 2013 and QEMU; I derived the hex).
- Arm's default NaN is positive, 0x7FF8000000000000 (CHECKED, Arm doc *extract*). Under FEAT_AFP its sign follows FPCR.AH (CHECKED, QEMU *extract*).
- RISC-V always produces the positive canonical NaN and never propagates payloads (CHECKED, ISA manual).

**Correctly rounded libm.**
- IEEE 754-2019 clause 9.2 recommends, without requiring: the exp and log families, pow, pown, powr, rootn, compound, hypot, rSqrt, trig (including sinPi to atan2Pi) and hyperbolics. If provided they must be correctly rounded, which was added in 2019 (CHECKED through Wikipedia, not the standard).
- CORE-MATH (Inria, Zimmermann) is correctly rounded in every rounding mode: single-argument binary32 functions checked exhaustively, the rest on hard cases. glibc 2.42 took about 30 binary32 functions; 2.43 took binary64 acosh, asinh, atanh, erf, erfc, lgamma and tgamma (CHECKED).
- RLIBM (Rutgers; CHECKED): RLIBM-32 (PLDI 2021), RLIBM-ALL (POPL 2022: one polynomial for many formats and all rounding modes, by rounding to odd at n+2 bits), RLIBM-PROG (PLDI 2022), MultiRound (PLDI 2025). It covers float32, posits, bfloat16 and tf32; binary64 is not listed.
- LLVM libc aims to be correctly rounded in all four rounding modes and marks each function; some are listed with ULP errors instead (CHECKED).
- C23 reserves names beginning `cr_` for correctly rounded functions (MEMORY).

**WebAssembly.**
- Full profile: NaN outputs are canonical if every NaN input is canonical, otherwise any arithmetic NaN, with a non-deterministic sign (CHECKED).
- Wasm 3.0 (announced 2025-09-17) adds a deterministic profile: only positive canonical NaNs and fixed relaxed-SIMD behaviour; `memory.grow` and `table.grow` stay non-deterministic (CHECKED).

**Java.**
- JEP 306 (JDK 17) made all floating point strict; `strictfp` became redundant, with a lint warning; the motivation was x87 versus SSE2 (CHECKED).
- `StrictMath` must reproduce fdlibm 5.3 for 18 functions, from sin to log1p (CHECKED).
- The `Double.toString` fix shipped in JDK 19 (JDK-4511638, Giulietti) and uses Schubfach (CHECKED, *extract*).

**Float printing.** Dragon4: Steele and White, PLDI 1990 (CHECKED, *extract*). Grisu: Loitsch, PLDI 2010; Grisu3 detects that it has failed on about 0.5% of inputs and needs a fallback (CHECKED, secondary). Ryū: Adams, PLDI 2018, shortest round-trip output with a correctness proof (CHECKED). Schubfach: Giulietti, the algorithm behind the JDK 19 fix (CHECKED, *extract*).

**Box2D and Rapier.**
- Box2D v3 (Catto, August 2024) claims algorithmic, multithreaded and cross-platform determinism, tested on x64 and ARM with MSVC, GCC and Clang. It uses `-ffp-contract=off`, no fast-math, its own sin, cos and atan2 approximations (sqrt was found deterministic) and a deterministic contact order, and a CI test compares a hash of the body transforms and the step count (CHECKED).
- Rapier's `enhanced-determinism` feature excludes `simd8`, keeps the parallel solver equal to the sequential one, needs strictly IEEE 754-2008 platforms (Wasm included) and routes transcendentals through nalgebra's `ComplexField` (CHECKED).

**ISO/IEC TR 18037 (Embedded C).**
- It adds fixed-point arithmetic, named address spaces and basic I/O hardware addressing. Revised 2008, reviewed 2013 (CHECKED); first edition 2004 (MEMORY).
- GCC implements `_Fract`, `_Accum` and `_Sat` from the N1169 draft, on some targets only (CHECKED).

## D. Unicode source-code safety

- **UTS #55, Unicode Source Code Handling** (Leroy, Davis). Drafted in 2023 alongside Unicode 15.1; currently Version 2, Revision 5, 2024-01-29 (CHECKED). It recommends: displaying code by its lexical structure, so bidi never splits an "atom"; making default-ignorable characters visible; finding confusable identifiers with UTS #39 skeletons and checking mixed scripts per chunk of an identifier; comparing identifiers under NFC (NFKC with case folding in case-insensitive languages) and never silently normalizing string literals; warning when directional controls span atoms; and never dropping an unexpected line break (CHECKED).
- **UTS #39** (v18.0.0, 2026-08-27): identifier status and type, the General Security Profile, `skeleton`/`bidiSkeleton` confusables, mixed-script detection, restriction levels (CHECKED).
- **UAX #31** (revision 45, 2026-09-01): XID_Start/XID_Continue syntax, profiles, normalized and case-insensitive identifiers (R4, R5), immutable Pattern_Syntax and Pattern_White_Space, LRM/RLM as ignorable format controls (CHECKED).
- **UAX #15** (revision 58, 2026-08-12) defines NFC, NFD, NFKC and NFKD. Normalization is idempotent and stable for assigned characters (CHECKED).
- **Trojan Source** (Boucher and Anderson; arXiv 2021, USENIX Security 2023). CVE-2021-42574 covers bidi reordering and CVE-2021-42694 homoglyphs (CHECKED). Rust 1.56.1 added two deny-by-default lints for the nine bidi codepoints in literals and comments (CHECKED); GCC added `-Wbidi-chars=none|unpaired|any`, default `unpaired` (CHECKED, patch *extracts*).
- **Silent canonicalization is old:** Python normalizes identifiers to NFKC, turns CR LF and CR into LF (even in literals) and ignores a UTF-8 BOM; Rust normalizes identifiers to NFC and warns on `confusable_idents` (RFC 2457) (CHECKED).

## E. Novelty threats (adversarial)

|Planned feature|Closest prior art|Not new|Possibly new|
|---|---|---|---|
|Controlled English with unless / provided that / notwithstanding, defeasible priority|Catala; L4 2022 `subjectTo`/`despite`; Blawx and Logical English on s(CASP); ACE; Inform 7|Defeasible priority over legal rules; English-like surfaces; "despite" as notwithstanding|Drafting connectives as first-class operators of a general-purpose controlled English; "provided that" as an operator: none found|
|A canonicalizer that repairs safe faults with a receipt for each and refuses bidi controls and confusables|ftfy (uncurls quotes, normalizes line breaks, applies NFC; `fix_and_explain` returns steps that `apply_plan` replays) (CHECKED); Python and Rust lexers; Rust and GCC bidi lints; UTS #55 and #39|Repairs, explained and replayable repairs, and refusals each exist|One admission step in a compiler front end that joins safe repairs, per-repair receipts and refusals|
|Byte-identical output from Python, C99 and Rust, with the reference interpreter as authority|Catala (interpreter plus four backends, trace goal); Dafny (differential testing); EELS; the Wasm reference interpreter; RFC 8785 JCS (canonical JSON for hashing and signing, numbers by ECMAScript serialization; 2020; CHECKED)|Multi-backend code generation; an interpreter as oracle; canonical numbers across languages|Identity across three hosts stated as a per-program contract, with an authority on mismatch: none found|
|Exact integer and fixed-point arithmetic plus binary64 under a declared envelope|COBOL; Catala (Z/Q/cents); TR 18037; Ada fixed point (MEMORY); JEP 306 with StrictMath; Wasm's deterministic profile; RFC 3514; Box2D and Rapier; oneMKL CNR (bitwise reproducible for one executable and a fixed thread count, per ISA path; CHECKED, *extract*)|Every ingredient, declared reproducibility conditions included|An envelope declared in the language and checked across its own backends|
|Runtime receipts carrying hash chains|Haber–Stornetta 1991; Schneier–Kelsey 1999 (citations CHECKED; their hash-linking MEMORY); in-toto links hashing materials and products (CHECKED); SLSA provenance; RISC Zero "receipts" attesting a guest's execution (CHECKED); K's per-execution proof objects; Catala traces|Hash-chained logs, execution receipts (even the word), certificates for each run|Receipts as part of a language's semantics, identical across backends; the name collides with RISC Zero's|
|Runtime claim grading with oracle provenance|HOL4 oracle tags, inherited by every derived theorem (CHECKED); Isabelle prints oracle-based theorems with [!] (CHECKED, *extract*); Lean's `#print axioms` and compiler-trust axioms (CHECKED, *extract*); SLSA levels; W3C Verifiable Credentials 2.0 (Recommendation 2025-05-15; claims with an issuer and a proof; CHECKED, *extract*)|Trust tracked by provenance (statically), graded levels (for builds)|The language runtime grading its own run-time claims: none found|

Plainly, no single feature is new. The strongest threats are Catala (legal semantics, several backends, interpreter, traces), K (a certificate per execution), RISC Zero (receipts) and HOL4 (oracle provenance). Not found anywhere: the combination, under a stated contract of byte-identical output across hosts.

## Unconfirmed

- MEMORY only: Lean 4 compiling through C, K's LLVM backend, C23 `cr_`, AppleScript 1993, Annex F's int-to-float wording, the x86 FMA flags.
- IEEE 754-2019 read only through Wikipedia; the NaN hex values derived from descriptions of the sign bit; FEAT_AFP from a QEMU extract; L4's current backends not found.

## Sources

github.com/CatalaLang/catala/releases, ocaml.org/p/catala/1.1.0/catala.runtime_ocaml/Catala_runtime/index.html, arxiv.org/abs/2103.03198, lexon.org, github.com/LogicalContracts/LogicalEnglish, github.com/Attempto/APE, intfiction.org/t/inform-7-v10s-compile-to-c-question/57163, legalese.com/l4/concepts/legal-modeling/default-reasoning, arxiv.org/abs/2205.07335, github.com/Lexpedite/blawx, arxiv.org/abs/2009.10238, github.com/accordproject/ergo, en.wikipedia.org/wiki/COBOL, en.wikipedia.org/wiki/HyperTalk, raw.githubusercontent.com/dafny-lang/dafny/master/docs/DafnyRef/UserGuide.md, raw.githubusercontent.com/dafny-lang/dafny/master/RELEASE_NOTES.md, amazon.science/publications/testing-dafny-experience-paper, github.com/FStarLang/karamel, why3.org/doc/exec.html, lean-lang.org/doc/reference/latest/Build-Tools-and-Distribution/, rocq-prover.org/doc/V9.0.0/refman/addendum/extraction.html, fsl.cs.illinois.edu/publications/chen-lin-trinh-rosu-2021-cav.pdf, github.com/ethereum/execution-specs, github.com/WebAssembly/spec/tree/main/interpreter, lf-lang.org/docs/, en.cppreference.com/w/c/types/limits/FLT_EVAL_METHOD, en.cppreference.com/w/c/preprocessor/impl, en.cppreference.com/w/c/language/conversion, clang.llvm.org/docs/UsersManual.html, gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html, github.com/llvm/llvm-project/issues/54927, gcc.gnu.org/pipermail/gcc/2023-September/242487.html, rust-lang.github.io/rfcs/3514-float-semantics.html, doc.rust-lang.org/std/primitive.f64.html, doc.rust-lang.org/reference/expressions/operator-expr.html, docs.python.org/3/whatsnew/{2.7,3.1,3.11}.html, docs.python.org/3/library/math.html, devblogs.microsoft.com/oldnewthing/20130221-00/?p=5183, docs.riscv.org/reference/isa/unpriv/f-st-ext.html, webassembly.github.io/spec/core/appendix/profiles.html, webassembly.org/news/2025-09-17-wasm-3.0, openjdk.org/jeps/306, docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/StrictMath.html, bugs.openjdk.org/browse/JDK-4511638, core-math.gitlabpages.inria.fr, people.cs.rutgers.edu/~sn349/rlibm/, libc.llvm.org/headers/math/index.html, en.wikipedia.org/wiki/IEEE_754, github.com/ulfjack/ryu, box2d.org/posts/2024/08/determinism/, rapier.rs/docs/user_guides/rust/determinism/, gcc.gnu.org/onlinedocs/gcc/Fixed-Point.html, en.wikipedia.org/wiki/Embedded_C, unicode.org/reports/tr55/, unicode.org/reports/tr39/, unicode.org/reports/tr31/, unicode.org/reports/tr15/, arxiv.org/abs/2111.00169, trojansource.codes, blog.rust-lang.org/2021/11/01/cve-2021-42574/, rust-lang.github.io/rfcs/2457-non-ascii-idents.html, docs.python.org/3/reference/lexical_analysis.html, ftfy.readthedocs.io/en/latest/explain.html, rfc-editor.org/rfc/rfc8785, dev.risczero.com/terminology, github.com/in-toto/docs/blob/master/in-toto-spec.md, slsa.dev/spec/v1.0/levels, hol-theorem-prover.org/docs/trindemossen-2/Reference/Thm.mk_oracle_thm, intel.com/content/www/us/en/developer/archive/training/conditional-numerical-reproducibility-cnr.html
