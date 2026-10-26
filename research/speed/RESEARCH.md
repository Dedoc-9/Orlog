# Debate record: the prior-art survey for the speed debate (2026-10-26)

A subagent's report, saved verbatim by the judge. It is model output, not the owner's words, and carries no
authority. Its source grades ([P], [A], [S], [U]) are its own and say how each source was read; "derived here"
marks its own reasoning. Its working files are in `work/speed-research/` (ignored by git), not in this repository.

---

# The speed debate: prior-art survey (the research party, 2026-10-26)

Model output from the research party of the debate set out in `research/speed/PROPOSAL.md`. It carries no authority,
nothing in it is built, and it changes no tracked file. It surveys what shipped systems, specifications and papers
say about the four questions (Q1 the two-speed reconciler, Q2 a language swap or GPU authority, Q3 the view tier,
Q4 a headroom standard), then gives its own reading, marked as such, and the open points.

## How to read this

**Source grades** (how each source reached me):
- **[P]** primary source, read in full or in the relevant part;
- **[A]** abstract or summary page only;
- **[S]** a secondary account;
- **[U]** a search snippet only.

**How "read" happened.** Web pages were read through a fetch tool that renders the page and answers questions about
it with a smaller model; long specifications were paged through to the sections named. A [P] from that route means
the relevant part reached me through that reader, not that I saw every byte. PDFs the reader could not parse were
extracted locally to text with `work/speed-research/scripts/pdftext.py` (standard library) and read directly; those
are marked "(text read here)". Search snippets are [U]; they are reported as such, and no conclusion in §12 rests on
a [U] item alone.

**Claim grades** follow `README.md` ("How to read this README"): MEASURED (seen in a recorded run, one host), OBSERVED
(seen once, not recorded), ESTABLISHED (a cited result), DECLARED (a commitment or an assertion not shown, including
a statement of absence), NOT_MEASURED, SPECULATIVE. A published measurement by others is ESTABLISHED as a cited
result, never MEASURED: nothing of it was run here. A vendor's assertion without a method is DECLARED (the vendor's).

**Derived here** marks my own reasoning or arithmetic. The arithmetic is in `work/speed-research/scripts/derive.py`,
its output in `work/speed-research/derive-out.txt`.

**Fixed rule.** Every latency, refresh or frame-time figure below is the source's own. None is a claim about Ørlǫg,
Verðandi, this host or anything built here, and none is a claim about feel.

**What the first attempt left, and what was reused** (`work/speed-research/`, checked before use):
- `dl/` five PDFs and `txt/` their extracted text: Gladman et al. 2025 (libm accuracy), the rr extended technical
  report, Sloan's 2013 JCGT paper, Spjut et al. 2019, and WPI-CS-TR-21-06. The texts are coherent; I read their
  relevant parts directly.
- `scripts/pdftext.py`: read in full. It imports `re`, `sys` and `zlib`, reads one PDF and writes one text file.
  Reused for five more PDFs (Sloan 2002, Sloan 2008, a Knight and Leveson summary, VESA's Adaptive-Sync CTS r1.0,
  an MIT FPGA report).
- `scripts/sh_check.py`: its docstring named the wrong compared spelling (it said 3z² − r²; the code compares 3z² − 1),
  now corrected with a note, and its unused expression turned into an assertion. Rerun: the same printed lines as the
  first attempt's output, which the rerun overwrote after I had read it (§11).
- The Ørlǫg documents and code cited were read from `work/speed-research/tree/`, a `git archive` of HEAD (f16dc26).
  Nothing of Ørlǫg was run.

---

## 1. Deterministic lockstep and desync detection in shipped games

**Bettner and Terrano, "1500 Archers on a 28.8: Network Programming in Age of Empires and Beyond"** (GDC 2001; the
Game Developer reprint) [P].
- Shows (ESTABLISHED): every machine ran the same simulation on the same commands. Turns were about 200 ms, and a
  command issued in one turn was scheduled two turns later. Turn length followed the slowest machine and the worst
  ping. Out of sync was detected by checksums of the world, objects, pathfinding, targeting and other systems, and it
  stopped the game. These were the project's hardest bugs: small differences compounded (a misplaced deer changed
  foraging, later food totals), so the mismatch surfaced far from its cause. Diagnosis used traces of about 50 MB. A
  later engine (RTS3) added tagged sync-tracking macros, compiled out of release builds.
- Does not show: how often checksums ran, their size or cost; anything on floating point.

**Factorio Friday Facts** #47 (2014-08-15), #55 (2014-10-10), #76 (2015-03-06), #188 (2017-04-28) [P].
- Shows (ESTABLISHED): peers exchange only player actions, a few hundred bytes a second each (#76). The routine check
  is a deliberately incomplete per-tick CRC of a few cheap values that depend on much of the state (every player's
  state, the count of active entities, a production-statistics snapshot), compared across all players every tick; a
  mismatch reconnects the player and re-downloads the map (#55). A full-map CRC every tick exists as a debugging mode,
  accurate but slow, its cost growing with the map (#55). With a save written every tick as well, the game ran at
  single-digit frames a second; replaying the save then names the first desynced tick exactly, and a binary diff of the
  two tagged saves usually shows one variable (#47). Desync reports carry the server's and the client's state (#188).
- Does not show: how often the heuristic CRC misses a divergence (one in an unsampled variable is caught only when it
  reaches a sampled one); any cost figure in normal play; anything after 2017.

**OpenTTD**, `docs/desync.md` and `docs/debugging_desyncs.md` (current master) [P].
- Shows (ESTABLISHED): lockstep, with commands scheduled for a future network frame and executed in the same frame
  and order everywhere. The server sends, now and then, the game logic's random-number-generator state for a frame as
  the checksum; a mismatch disconnects the client. Detection is a late failure signal: one cited desync was noticed
  only after 20 in-game years. Localization is by replay: commands are logged to `commands-out.log`, replayed from the
  first savegame with the recorded checksums compared, and periodic `dmp_cmds` saves narrow the window. A debug level
  recomputes caches every tick. Listed causes: state missing from savegames, stale caches, unstable sorts,
  architecture-dependent computation, a command's test run that changes state.
- Does not show: the checksum interval; any cost.

**Forrest Smith, "Synchronous RTS Engines and a Tale of Desyncs" and "... 2: Sync Harder"** (2011; Supreme Commander,
Demigod) [P].
- Shows (ESTABLISHED): a simulation layer at a fixed 10 ticks a second and a user layer up to about 60 frames a
  second that interpolates between ticks. A command issued in tick 7 runs in tick 11. The whole game state is hashed
  once a second and compared; a mismatch ends the game. Debugging walked the state printing memory hashes (a binary
  search), and ran games in loops on many machines; one hunt took almost a week (a dangling pointer). The CPU was put
  in a strict IEEE mode. Recovery is harder than prevention: with two players nobody can tell which state is right.
- Does not show: the hash function, its size or cost.

**0 A.D.** source on master: `TurnManager.cpp`, `NetClientTurnManager.cpp`, `ComponentManagerSerialization.cpp`,
`HashSerializer.h` [P] (code read through the reader).
- Shows (ESTABLISHED): after each turn the client computes a state hash and sends it to the server in a sync-check
  message. Turn 1 and every 20th turn get a full hash (a code comment says about every 10 s in multiplayer); the
  others a quick hash, which covers only the position component plus the random-number state and the next entity id.
  The hash is MD5 over the serialized components of non-local entities. On a mismatch the client writes an
  out-of-sync dump of that turn.
- Does not show: the cost of either hash. The default turn length is 200 ms according to forum posts [U].

**Riot Games, "Determinism in League of Legends"**: Introduction (2017-06-20), Unified Clock, Implementation, Fixing
Divergences (2018-05-01) [P].
- Shows (ESTABLISHED): server network recordings replayed to reproduce a match, unthrottled (recovery to the 40th
  minute often under 3 minutes). The scope is gameplay determinism, not identical memory. Several random generators
  were unified into one, seeded by the game's id; six clock APIs became one (about six months). Frame deltas stayed
  variable rather than a fixed step, and recording and replaying them is a stated design goal. Divergences are found
  by comparing per-frame state logs (hierarchical key-values written
  only when a value changes, at two levels of detail) from a live run and its replay; a script names the first
  divergence. Checksums were rejected because they show that states differ, not where. 2,000 to 3,000 games a day
  were replayed on dedicated machines; a one-in-5,000 bug was isolated by bisecting about 580,000 constructor calls in
  about 20 replays of about 6 s each. Playback on another OS diverged more often.
- Does not show: compiler floating-point settings; the cost of the logs.

**Derived here.** Every shipped system splits detection from localization. Detection is a cheap periodic digest: a
sampled CRC every tick (Factorio), a quick hash every turn (0 A.D.), a full hash every second (Supreme Commander) or
every 20 turns (0 A.D.), the random-number state now and then (OpenTTD). Localization is a heavy record made or
replayed on demand: saves every tick, dumps, per-frame state logs, command logs. Detection latency runs from one tick
to decades of game time. None of the systems read here ships a per-assignment cryptographic chain in play (DECLARED:
an absence in what was read); the nearest is a debugging mode (Factorio's full CRC with a save every tick).

## 2. Rollback netcode

**GGPO Developer Guide** and `src/lib/ggpo/sync.h` (pond3r/ggpo) [P].
- Shows (ESTABLISHED): the game must be deterministic, its whole state saveable and loadable through callbacks
  (renderer, audio and textures excluded), and able to advance one frame without rendering. The advance callback runs
  many times during a rollback, so rendering and sound must wait for it. The random generator lives in the saved
  state with equal seeds at frame 0; no wall clock in state; pointers rebased on load. A sync-test session rolls back
  one frame on every frame and compares the two executions. In the source, `MAX_PREDICTION_FRAMES` is 8 and the
  saved-state ring has 10 slots, each with a checksum field.
- Does not show: floating-point guidance; a per-frame budget.

**GGRS** (Rust; docs.rs, current) [P].
- Shows (ESTABLISHED): save, load and advance requests each frame; a maximum prediction window of 8 by default (0 is
  lockstep). Its sync test rolls back and resimulates the last `check_distance` frames every frame (default 2) and
  compares checksums; peer-to-peer desync detection compares checksums across peers at an interval.
- Does not show: anything across platforms.

**Michael Stallone, "8 Frames in 16ms: Rollback Networking in Mortal Kombat and Injustice 2"** (GDC 2018) [U] (the
session listing in a search snippet; the GDC Vault was in maintenance), and Edgegap's write-up of it [S].
- Shows: the title and abstract (rolling back and resimulating up to eight frames inside 16 ms) [U]. From the
  write-up [S]: a seven-entry rollback ring, three frames of input delay, an idle frame of 13 ms after optimization
  (30 ms in the first rollback build), serialization as the core of the work, thousands of in-tick "fencepost"
  checks to locate desyncs, replay from recorded pad input, restore parallelized from 2.7 to 1.3 ms.
- Does not show: any of the [S] figures checked against the talk itself.

**Derived here.** Rollback needs three things: determinism, a whole-state save and load cheap enough to take every
frame, and room for W + 1 simulation steps in one displayed frame at worst, with W of 7 or 8 in these sources. On the
skeptic's MEASURED-once c99 figure for a 1,000-body tick (0.86 ms, per-event SHA-256 included,
`research/roadmap-debate/SKEPTIC.md`), 8 steps take 6.9 ms: 41% of a 60 Hz frame and 88% of a 128 Hz tick. On
fall.orl's 1.34 µs a tick, 8 steps take about 11 µs (`derive-out.txt` §5). RUN-1 leaves snapshots to SNAP-1, so
rollback is out of RUN-1's reach either way.

## 3. Server-authoritative competitive games

**Gabriel Gambetta, "Fast-Paced Multiplayer (Part II): Client-Side Prediction and Server Reconciliation"** [P].
- Shows (ESTABLISHED): the meaning of reconciliation in this genre. The client numbers its inputs and keeps those not
  yet acknowledged; the server reports the last input it processed; when an authoritative state arrives, the client
  resets to it and reapplies the pending inputs. Prediction relies on the world being deterministic enough that the
  prediction usually matches.
- Does not show: tick rates; mispredictions among several players (left to the next part).

**Riot Games, "Peeking into VALORANT's Netcode"** (2020-07-28) and **"VALORANT's 128-Tick Servers"** (2020-08-31) [P].
- Shows (ESTABLISHED): the server is authoritative and steps the simulation at a fixed 128 steps a second; client
  moves carry numbers on a shared timeline and wait in a short queue; a missing move is predicted by repeating the
  last inputs. Clients predict, and the server's correction snaps a client back. Hit registration rewinds the world
  to what the shooter saw, with the rewind capped. Their model of peeker's advantage is about 141 ms at baseline,
  about 40 ms less with 128-tick servers, about 35 ms round trips and 60 fps clients; skilled playtesters noticed 10 ms
  differences. A 128 Hz tick is 7.8 ms; three games a core with 10% held back leaves 2.34 ms a game a frame; server
  frame time went from about 50 ms to under 2 ms, tracked by subsystem.
- Does not show: whether client and server run the same code, or any bit-identity between them.

**Other titles' tick rates.** CS2: servers record the moment a move or shot begins between ticks ("sub-tick"),
reported at 64 Hz [U]. Overwatch: the GDC 2017 session listing says its networked simulation uses determinism for
responsiveness and precision [U]; updates went from about 21 to 63 a second [U]. Apex Legends: 20 Hz; Respawn's own
argument, quoted by others, is about five frames of delay at 20 Hz against three at 60 Hz for three times the
bandwidth and CPU [U]. Fortnite 30 Hz and Battlefield V 60 Hz, from a measurement reported by PC Gamer [U]. League of
Legends: frame deltas usually under 0.033 s [P, Unified Clock]. Supreme Commander 10 Hz [P]; Age of Empires 200 ms
turns [P]. Valve's Source networking article and Bernier's GDC 2001 paper refused the fetch (HTTP 403); Bernier is
summarized in the WPI taxonomy below [S].

**Liu, Xu and Claypool, "A Survey and Taxonomy of Latency Compensation Techniques for Network Computer Games"**
(WPI-CS-TR-21-06, 2021) [P] (text read here).
- Shows (ESTABLISHED): "time warp" rolls the game back to when the client acted, applies the action and rolls
  forward; it is also called latency or lag compensation, or rollback. Its known artifact is being "shot around the
  corner"; commercial shooters cap how far back a server rewinds. The idea descends from Jefferson's virtual time.
- Does not show: measured costs of any technique in a shipped game.

**Derived here.** In this genre, "reconciliation" means the authority overwrites the client's prediction and the
client replays its pending inputs. A mismatch is expected, corrected and never recorded as a defect, and no two
executions are compared for agreement. Ørlǫg's reconciler (Q1) is the opposite relation: two executions must agree
byte for byte, and a mismatch is a defect located to its first event. It resembles lockstep desync detection, not
client reconciliation.

## 4. Floating-point determinism across compilers, CPUs and GPUs

### What the specifications guarantee

- **IEEE 754-2019.** Not read (paywalled). Two sources I read state its position: it recommends, and does not
  require, correctly rounded elementary functions (Gladman et al., below) [S]; its clause 11 says reproducible
  results need the cooperation of language standards, language processors and users, and that a language standard
  should support reproducible programming (WG21 P3375R3, below) [S].
- **C11** (N1570 draft) [P]. A floating expression may be contracted (evaluated as one operation with one rounding);
  whether and how is implementation-defined unless the `FP_CONTRACT` pragma forbids it (§6.5 ¶8, footnotes 89–90).
  The pragma's default state is implementation-defined (§7.12.2). The accuracy of `+ − * /` and of `<math.h>` is
  implementation-defined and may be declared unknown (§5.2.4.2.2, the end of ¶6 read). `FLT_EVAL_METHOD` takes −1, 0,
  1 or 2 (¶9).
- **C++** [S]: per P3375R3, the representations and accuracy of floating-point operations are implementation-defined,
  and the as-if rule lets compilers fuse and reorder. **WG21 P3375R3, "Reproducible floating-point results"**
  (2025-05-12) [P] proposes five correctly rounded functions (add, subtract, multiply, divide, square root) and leaves
  `<cmath>` out, since reproducible transcendental functions would require specifying the algorithms.
- **Compilers.** GCC [P]: `-ffp-contract` defaults to `off` for C in a standards-compliant mode (`-std=c11` and the
  like) and `fast` otherwise. Clang [P]: `on` (fusion within a statement) by default, `fast` for CUDA,
  `fast-honor-pragmas` for HIP; the default `-ffp-model=precise` keeps contraction on. MSVC [P]: `/fp:precise` by
  default, which since Visual Studio 2022 generates no contractions unless `/fp:contract` is given (earlier versions
  could). nvcc [P]: `--fmad=true` (contraction on) by default, with `--ftz=false`, `--prec-div=true`,
  `--prec-sqrt=true`; `--use_fast_math` flips the last three and maps math functions to faster intrinsics.
- **Rust**, RFC 3514 [P]: the basic operations follow IEEE 754-2008 with round-to-nearest-even, each rounded on its
  own, with `mul_add` as the explicit fused operation. That leaves no room for an automatic fused multiply-add, though
  the RFC does not discuss contraction by name in my reading (derived here). NaN sign and payload are
  non-deterministic; flush-to-zero is not in the specified behaviour except on 32-bit ARM NEON; 32-bit x86 through
  x87 deviates; library functions' accuracy is unspecified.
- **Vulkan, SPIR-V environment**, "Precision and Operation of SPIR-V Instructions" [P]. OpFAdd, OpFSub and OpFMul are
  correctly rounded; so is OpFmaKHR, a true fused multiply-add behind optional features. The rounding direction is
  implementation-defined (either neighbour) unless the RoundingModeRTE or RTZ execution mode is used, itself behind
  features. Denormals may be flushed by default; DenormPreserve and DenormFlushToZero are behind features. OpFDiv
  2.5 ULP (|y| in [2⁻¹²⁶, 2¹²⁶]); inversesqrt 2 ULP; sqrt inherited from 1/inversesqrt; atan and atan2 4096 ULP;
  `fma` inherited from a multiply then an add, so it may or may not be fused. Without NoContraction an implementation
  may rearrange operations, including the number of roundings; unannotated operations default to AllowContract and
  AllowReassoc among other fast-math flags. The exp, log and sin rows were illegible in my read.
- **GLSL 4.60** [P]: `a+b`, `a−b`, `a*b` correctly rounded; `a*b+c` one or two roundings; `a/b` 2.5 ULP; exp and exp2
  3 + 2·|x| ULP; log and log2 3 ULP outside [0.5, 2] and absolute error 2⁻²¹ inside; inversesqrt 2 ULP; trigonometric
  functions of undefined precision; denormals may be flushed; the rounding mode is unspecified but within 1 ULP. The
  `precise` qualifier forbids reassociation and the fusing of `a*b+c` into an fma.
- **WGSL** (W3C Candidate Recommendation Draft of 2026-10-21; the floating-point sections read from the editor's
  source, `wgsl/index.bs` on main, because the reader truncated the published page) [P]: no rounding mode is
  specified; no exceptions; a finite-math assumption makes a runtime overflow, infinity or NaN indeterminate; the
  sign of zero may be ignored; inputs and outputs of the operations in the accuracy tables may be flushed to zero;
  implementations may reassociate, and may fuse when the result is at least as accurate; `fma` may be unfused.
  Accuracy (f32): `+ − *` correctly rounded; `/` 2.5 ULP; exp and exp2 3 + 2·|x| ULP; log and log2 absolute 2⁻²¹ in
  [0.5, 2] and 3 ULP outside; sin and cos absolute 2⁻¹¹ in [−π, π]; inverseSqrt 2 ULP; sqrt and pow inherited.
- **Direct3D 11 floating-point rules** [P]: 32-bit add, subtract and multiply within 0.5 ULP, which allows truncation
  instead of round-to-nearest-even; 32-bit denormals flushed to sign-preserved zero on input and output of arithmetic;
  fused operations (mad, dp3) no less accurate than the worst serial order of their parts, each part allowed 1 ULP;
  NaN bit patterns not preserved; sqrt and rcp 1 ULP; doubles optional, IEEE 754R with denormals kept. HLSL Shader
  Model 6.2 adds a 32-bit denormal mode (preserve, ftz, any) [U].
- **Metal** [U]: fast math is on by default in Xcode builds; with it off, the math mode is safe and the functions
  precise.
- **NVIDIA, "Floating Point and IEEE 754 Compliance for NVIDIA GPUs"** (white paper, v13.4) [P]: fused multiply-add
  formed by the compiler makes GPU results differ from a CPU's (its A·A + B example: 0 on x86 SSE, about 2⁻⁴⁶ with
  FMA, both conforming); the CUDA math library and the host libm are independent and neither is correctly rounded;
  double `sin` within 2 ULP.

### Measured studies

- **Gladman, Innocente, Mather, Zimmermann, "Accuracy of Mathematical Functions in Single, Double, Double Extended,
  and Quadruple Precision"** (August 2025) [P] (text read here). Thirteen libraries, among them glibc 2.42, Intel's,
  AMD LibM 5.1, Musl, Apple's, LLVM libc 20.1.8, MSVC 2022, CUDA 12.8 and ROCm 6.2.4. Binary32 bounds are exhaustive
  (upper bounds); binary64 values come from a search (lower bounds). They differ by library: binary32 `cos` ranges
  from 0.500 ULP (LLVM libc, correctly rounded) through 0.561 (glibc) to 2.91 (Newlib), with 1.52 for CUDA and 1.61
  for ROCm; `sqrt` is correctly rounded everywhere. Some libraries dispatch different code by CPU feature, and the
  rsqrt and rcp instructions differ between Intel and AMD, so one binary can give different results on different
  hardware (ESTABLISHED).
- **Zahid, Laguna, Le, "Testing GPU Numerics: Finding Numerical Differences Between NVIDIA and AMD GPUs"**
  (arXiv 2410.09172, 2024) [P]. Random programs (Varity) compiled with nvcc and hipcc at equal optimization levels
  and run on V100 and MI250X GPUs, 652,600 runs: about 0.98% of FP64 runs differed, 1.10% after HIPIFY conversion,
  and about 9% of FP32 runs, nearly all under fast math (13,877 against 45 at -O0). Causes found: math-library
  differences (`fmod`, `ceil` cases), fast math, intermediate handling (ESTABLISHED).
- **Erin Catto, "Determinism"** (Box2D v3, 2024-08-27) [P]. Cross-platform float determinism held in one CI scenario
  across MSVC, Clang and GCC on x64 and ARM by: no fast math, `-ffp-contract=off`, and its own sine, cosine and
  atan2, because `atan2f` differed across platforms; `sqrtf` was the same (a hardware instruction). It compares a
  hash of the final state, not each step, and calls the property fragile under compiler updates (ESTABLISHED).
- **Glenn Fiedler, "Floating Point Determinism"** (2010) [P]: cross-machine results are possible "if" (same compiler
  and binary, same architecture, strict IEEE modes, no x87 extended precision, the FPU state checked every tick, no
  fused or transcendental operations); it collects reports: none across AMD and Intel at Gas Powered Games,
  trigonometry differing between AMD and Intel in Battlezone 2, MotoGP replays failing across Xbox and PC and between
  debug and release builds.
- **Bruce Dawson, "Floating-Point Determinism"** (2013) [P]: one binary on one CPU is the easy case; one binary across
  CPUs needs the estimate instructions and CPU-dispatched libraries avoided; different binaries are much harder.
- **FTTN** (CCGrid 2024) [U]: the numerical behaviour of NVIDIA and AMD matrix accelerators (extra precision bits,
  accumulation order, subnormals) is not documented.
- Verðandi's own measurement across JavaScript engines is in §10.

**Derived here.** Of the GPU rules read, only add, subtract and multiply are required to be correctly rounded, and
Direct3D 11 relaxes even those to 0.5 ULP. Division, square root and the transcendental functions are ULP-bounded;
denormals may flush; contraction is allowed unless NoContraction or `precise` forbids it. No API read fixes a GPU
float result to the bit. That supports R8 b (float ports deferred) and keeps GPU floats out of receipts.

## 5. Exact integer and fixed-point work on GPUs

- **WGSL** [P]: the runtime scalar types are `i32`, `u32`, `f32` and `f16`. The 64-bit `AbstractInt` exists only while
  a shader is created. Concrete integer arithmetic wraps modulo 2³². Division by zero gives the dividend, and so does
  the most negative value divided by −1; the remainder in those cases is 0; shift counts are taken modulo the bit
  width at run time. The integer semantics are total and defined, but there is no 64-bit runtime integer, and no
  built-in in the built-in sections I read returns the high half of a 32 × 32 product (ESTABLISHED).
- **Vulkan** [P]: `shaderInt64` is an optional feature; 64-bit atomics are separate features. The Vulkan hardware
  database (vulkan.gpuinfo.org, crowdsourced) showed device coverage of 68.22% for `shaderInt64`, 32.46% for
  `shaderFloat64` and 96.7% for `shaderInt16` when I read it (OBSERVED, one look at a live database on 2026-10-26).
- **Direct3D 12** [P]: `Int64ShaderOps` is a capability bit, so optional.
- **Metal** [U]: 64-bit integer math from the Apple3 family; 64-bit atomics from Apple9 only.
- **CUDA** [U]: native 64-bit integer types; in PTX, integer division by zero yields an unspecified, machine-specific
  value.
- **AMBER GPU** (pmemd.cuda) logistics page [P]: by default, single-precision arithmetic with 64-bit fixed-point
  integer accumulation (SPFP); the page calls GPU runs self-consistent because accumulation is in integers, and says
  forces can overflow the fixed point at close contacts. GPU and CPU trajectories diverge quickly. An older AMBER page
  calls the model bitwise reproducible [U] (ESTABLISHED as AMBER's statement; its conditions not given).
- **OpenMM** platform documentation [P]: the CUDA property `DeterministicForces` makes force sums reproducible at a
  small cost; with PME, the Reference, OpenCL and double-precision CUDA platforms are deterministic, while
  single-precision CUDA and the CPU platform are not; none of this is promised for future versions.
- **Tinker-HP** [U]: 64-bit fixed-point force accumulation with 34 fractional bits.
- **GPUDet** (ASPLOS 2013) [U]: deterministic GPU hardware at about 2× average slowdown, 4% for compute-bound work.
  **Deterministic Atomic Buffering** (MICRO 2020) [U]: only atomics ordered, about 23% average slowdown, simulated.
- **Yang, Riasanovsky, Deng, Sarkar, "Taming Bitwise Behavior in GPU Kernels with Tensor Core"** (arXiv 2609.11356,
  2026-09-10) [A]: deterministic kernels still differ in bits between configurations, mainly by reduction order;
  holding one order costs up to 20%; they report a static checker of bit-equivalence across NVIDIA PTX and AMD GCN,
  and bit agreement with cuBLAS on tested GEMMs on Hopper and Blackwell. No cross-vendor bit equality is claimed.
- **Photon Quantum** documentation [P] (a CPU engine, C#): simulation in Q48.16 fixed point; multiply is the raw
  product shifted right 16, divide the dividend shifted left 16 then divided; trigonometry and square root by tuned
  lookup tables; float conversions marked unsafe and banned inside the simulation.
- **mas-bandwidth/fixed** (README) [P]: a Q48.16 C library claiming bit-identical results across platforms through
  integer-only arithmetic and transcendental functions; 128-bit intermediates native or emulated on MSVC; test suites
  compare against frozen hashes, and deliberately broken builds must fail (planted errors); CI on Linux x64, macOS
  arm64 and Windows (DECLARED by the project; its CI is its evidence).
- **Haque and Pande, "Hard Data on Soft Errors"** (2009) [A]: MemtestG80 on over 20,000 Folding@home hosts: about two
  thirds of the GPUs tested showed pattern-sensitive memory soft errors in the field, none in controlled lab tests.

**Derived here.** Integer arithmetic on GPUs is exact wherever it is defined, and the shipped deterministic GPU
simulations got determinism from integer accumulation, never from controlling floats. None claims agreement across
vendors; AMBER claims self-consistency, OpenMM determinism on a platform. Ørlǫg's Q31.32 multiply needs a
64 × 64 → 128-bit product. WGSL has neither 64-bit integers nor a 32 × 32 → 64 multiply, so each Fix product there
would be built from 16-bit limbs: 16 partial products of 16 × 16 bits plus carries, against one or a few instructions
on a CPU (a count, not a time).

## 6. Spherical harmonics in rendering

- **Ramamoorthi and Hanrahan, "An Efficient Representation for Irradiance Environment Maps"** (SIGGRAPH 2001) [A]
  (the abstract in the SIGGRAPH history archive; the authors' sites refused the connection). Nine coefficients give
  irradiance with about 1% average error, and irradiance is a quadratic polynomial in the normal's x, y, z.
- **Sloan, Kautz, Snyder, "Precomputed Radiance Transfer for Real-Time Rendering in Dynamic, Low-Frequency Lighting
  Environments"** (SIGGRAPH 2002) [A] (abstract, text read here): lighting and transfer in low-order SH; diffuse
  shading reduces to a dot product of 9- to 25-element vectors, glossy to matrices.
- **Sloan, "Stupid Spherical Harmonics (SH) Tricks"** (GDC 2008 companion paper) [P] (text read here, relevant
  parts): each band is equivalent to polynomials of its degree; appendix A2 lists the basis as polynomials in x, y, z.
  Its convention puts a minus sign on the m = ±1 functions; `sh_check.py`'s construction carries none, so sign
  conventions differ between sources (derived here).
- **Sloan, "Efficient Spherical Harmonic Evaluation"** (JCGT 2:2, 2013) [P] (text read here): the real SH can be
  written as polynomials of a point on the unit sphere; band l is the polynomial basis of degree l restricted to the
  sphere. Snyder's trick: dividing P_l^m by sin^m θ leaves a polynomial in z, and the sin^m θ cos mφ and sin mφ parts
  become polynomials in x and y; code is generated from recurrences.
- **Confirmed here** (MEASURED, §11): bands 0 to 6 built as polynomials with rational coefficients are each
  homogeneous of degree l and harmonic, and all 1,176 distinct pairs are orthogonal over the sphere, in exact
  rationals. K²π is rational for l ≤ 2, so each constant K carries a factor 1/√π.
- **Fixed-point implementations found.** The judge's law: Q31.32, bands 0 to 2, three backends agreeing with the
  reference, worst error 1.23 units of 2⁻³² against binary64 (MEASURED by the judge, `work/speed/JUDGE-MEASUREMENTS.md`
  §1; not re-run here). Bloomberg, "Four-Channel FPGA Ambisonic Audio System" (MIT 6.111, 2009) [P] (text read here):
  16-bit fixed-point SH coefficients precomputed into ROMs for 4,096 positions (two-dimensional, 11 harmonics),
  18 × 18 multiplies keeping 16 bits. A 1985 Ohio State geodesy report on exact integer-mode generation of SH from
  homogeneous harmonic polynomials [U]. No fixed-point SH lighting in a shipped game engine turned up in these
  searches (DECLARED: an absence of a find, not of the thing).

**Derived here.** Evaluating SH at a direction needs no transcendental function: products and sums, plus one square
root and divisions to normalize the direction, all of which Fix defines with one rounding each. The constants K are
irrational, so a law either rounds them as literals (the judge's law did, with notes) or folds them into the
coefficients as data and evaluates only rational polynomials. Two spellings equal on the exact sphere give different
raw values on the 2⁻³² grid in about half of all directions (§11), so the spelling, the sign convention and the
normalization are part of a law's meaning and must be declared.

## 7. Measuring latency for competitive play

- **Spjut, Boudaoud, Binaee, Kim, Majercik, McGuire, Luebke, Kim, "Latency of 30 ms Benefits First Person Targeting
  Tasks More Than Refresh Rate Above 60 Hz"** (SIGGRAPH Asia 2019 Technical Briefs) [P] (text read here). Eight
  skilled players; refresh rates of 60, 120, 240 and 360 Hz crossed with three latency levels, equalized by buffering
  frames at the higher rates; click-to-photon recorded during the trials, means about 22–25, 52–58 and 82–91 ms by
  level. Latency had a significant effect on completion time in both tasks; refresh rate's effect was small and only
  marginal once its latency reduction was removed. It calls 144 and 240 Hz the esports norms of 2019. The apparatus
  is in a supplement I did not read (ESTABLISHED, with that boundary).
- **NVIDIA, "Introducing NVIDIA Reflex"** (2020-09-01) [P]: system latency runs from a click to the change on the
  display, made of peripheral, game, render (game + render = PC) and display latency. The Reflex Latency Analyzer in
  360 Hz G-SYNC displays detects the click at a USB passthrough and times it to the on-screen change; the alternative
  named is a high-speed camera (1,000 fps resolves about 1 ms). DECLARED by NVIDIA: most players play at 50–100 ms
  of system latency, and 12 against 20 ms gave a 182 ms difference in an aiming task in its research.
- **AMD Frame Latency Meter 1.0** (GPUOpen, 2024-07-22) [P]: from a mouse event to the frame's change in a captured
  screen region, through AMF or DXGI desktop duplication; results to CSV. Press reports say it injects a synthetic
  mouse movement and averages 16 measurements a row [U].
- **Intel PresentMon**, `README-ConsoleApplication.md` [P]: `MsBetweenPresents`, `MsBetweenDisplayChange`,
  `DisplayedTime`, `MsUntilDisplayed`, `DisplayLatency`, `MsClickToPhotonLatency`, `MsAllInputToPhotonLatency`,
  `MsPCLatency`. Its "photon" is the moment the frame is displayed, from Windows event tracing, not measured light.
- **Android Frame Pacing library** [P]: pacing means frames presented at even intervals matching a swap interval.
  Failure modes: uneven numbers of refresh periods per frame (49, 16, 33 ms for 30 fps on 60 Hz) and queue stuffing,
  which adds latency. Presentation timestamps and fences are the remedies.
- **VESA Adaptive-Sync Display CTS r1.0** (2022-04-29) [P] (text read here): certification mandates for the
  AdaptiveSync tier: a variable-refresh range up to at least 144 Hz and down to at most 60 Hz; gray-to-gray at most
  5 ms on average over 20 transitions; overshoot at most 20% and undershoot at most 15%; flicker limits; frame-drop
  and jitter tests; photosensor instruments. I found no end-to-end input-latency mandate in its text (DECLARED: an
  absence in my reading).
- **ITU-T G.1072** (approved 2020-01-13) [U]: an opinion model predicting cloud-gaming quality of experience from
  network and encoding parameters; a planning tool, not a latency requirement.
- **Refresh rates in competitive use** [U]: 540 Hz panels from several makers; 600 Hz (MSI, ZOWIE) and 750 Hz (Koorui,
  HKC) announced; LG announced 1,000 Hz (May 2026). No tournament ruleset naming a refresh rate or a latency turned up.
- Riot's peeker's-advantage model (§3) [P] and Respawn's frames-of-delay argument (§3) [U] are budgets of their own
  systems, not standards.

**Derived here.** No standards body I found publishes a competitive input-to-photon requirement. What exists is a
vendor's definitions (NVIDIA), a display certification (VESA: refresh range, gray-to-gray, flicker, drops), a QoE
model (ITU-T) and studies (Spjut et al.). The instruments start and stop at different events (a device click, an OS
input event, a Present call, a flip, light at a photodiode), so their numbers compare in kind only. That is Verðandi's
G4 rule for cross-apparatus numbers, and G21's route of one instrument per segment.

## 8. Record-and-replay verification and N-version execution

- **O'Callahan, Jones, Froyd, Huey, Noll, Partush, "Engineering Record And Replay For Deployability"** (USENIX ATC
  2017, extended technical report) [P] (text read here). rr records everything that crosses the user-kernel boundary
  (system-call results, signals, the timing of asynchronous events) and runs one thread at a time. It names an
  execution point by the retired-conditional-branch counter, the only deterministic counter on modern Intel CPUs, plus
  the registers. Recording costs under 2× except on `make`. Small replay bugs surface long after their cause, so rr
  carries dense consistency assertions, compares memory checksums and checkpoints at chosen points between record and
  replay, and can log registers at every single step (ESTABLISHED).
- **Riot's replay** (§1) [P]: record, replay, compare per-frame state logs, name the first divergence.
- **Deterministic multithreading** [U]: Kendo (ASPLOS 2009) orders lock acquisitions by a logical time built from
  performance counters, and is deterministic only for race-free programs; Dthreads (SOSP 2011) runs threads as
  processes with copy-on-write memory and matched pthreads on most benchmarks, against earlier systems up to 8.4×
  slower. GPUDet and DAB are in §5.
- **Knight and Leveson, "An Experimental Evaluation of the Assumption of Independence in Multiversion Programming"**
  (IEEE TSE 12(1), 1986) [A] (the abstract, reproduced in a course summary, text read here) and [S] (the summary).
  27 versions from one specification at two universities, a million tests: each version very reliable, yet tests
  where more than one version failed were far more frequent than independence predicts; the summary reports the
  independence hypothesis rejected at α = 0.01 (ESTABLISHED).
- **Avižienis, "The N-Version Approach to Fault-Tolerant Software"** (1985) [U]: N ≥ 2 versions from one
  specification, a decision algorithm over their outputs; the method rests on independent failures.
- **Yang, Chen, Eide, Regehr, "Finding and Understanding Bugs in C Compilers"** (Csmith, PLDI 2011) [U]: random
  programs free of undefined and unspecified behaviour, compiled by several compilers, outputs compared: over 325
  bugs in three years; every compiler crashed or miscompiled, except that no wrong-code bug was found in CompCert in
  about six CPU-years. **McKeeman, "Differential Testing for Software"** (1998) [U] named the method.
- **Cox et al., "N-Variant Systems"** (USENIX Security 2006) [U]: diversified variants run on the same inputs, and a
  divergence is read as an attack.

**Derived here.** Agreement among N executions shows consistency, not truth: failures that are shared do not show.
Ørlǫg's four executions share one specification, one numeric reference and one author's reading of both. The twin's
paper round (R7) and the plants are its hedges. Verðandi's `AGENTS.md` §8 says the same of its own twins: one
author wrote both, so their agreement shows consistency, not truth (its G23).

## 9. The cost of per-step commitments

**What shipped systems commit, and when** (sources in §1–§2, §5, §8):

| system | commitment | when |
|---|---|---|
| Factorio | CRC of a few sampled values; full-map CRC only as a debugging mode | every tick |
| 0 A.D. | MD5 of positions and the random-number state (quick); of every component (full) | quick each turn; full on turn 1 and every 20th |
| Supreme Commander | hash of the whole state | once a second (every 10 ticks) |
| OpenTTD | the game logic's random-number state | now and then |
| Age of Empires | checksums of world, objects, pathfinding, targeting | not stated |
| GGPO, GGRS | a checksum per saved frame; sync tests; peer comparison | every frame (sync test), an interval (peers) |
| Photon Quantum | frame checksum sent to the server | every *Checksum Interval* ticks (60 by default in its API reference [U]), 0 advised for release |
| League of Legends | no checksum: per-frame logs of changed values | every frame, while diagnosing |
| rr | memory checksums and checkpoints | at chosen points, while diagnosing |
| Verðandi graybox | FNV-1a 64 over every state leaf's bits | every tick of its self-test replays (§10) |
| Ørlǫg v0 | SHA-256 chained per event (`RUNTIME-SPEC.md` §5) | every event |

**Photon Quantum's configuration manual** [P] adds that a cross-platform checksum mode has a significant performance
cost and is for debugging only.

**Hash throughput, published** (one machine each; orders of magnitude only):
- **xxHash README** [P]: on an i7-9700K with clang 10 `-O3`: XXH3 59.4 GB/s with AVX2 and 31.5 with SSE2; XXH64 19.4;
  FNV64 1.2 (noted for poor avalanche); BLAKE2 1.1; SHA-1 0.8; MD5 0.6. Small-data velocity: XXH3 133.1, SHA-1 5.6,
  MD5 7.8, BLAKE2 5.1 (units as the README gives them). Not for adversarial use (ESTABLISHED).
- **eBASH / SUPERCOP** result pages (supercop-20261018) [P], SHA-256 median cycles a byte: AMD Ryzen 7 1700 (Zen,
  2017): 24.88 at 8 bytes, 4.68 at 64 bytes, 2.02 for long messages. Intel Xeon E3-1220 v5 (Skylake, 2015): 290.29 at
  8 bytes and 45.45 at 64 bytes (both flagged for a wide spread), 7.69 for long messages. BLAKE3: 35.33, 4.07 and 1.75
  on the Ryzen; 35.88, 3.96 and 1.91 on the Xeon (ESTABLISHED). The Ryzen's long-message SHA-256 figure looks like
  hardware SHA instructions; the page does not say (derived here).
- **Ørlǫg's runtimes** implement SHA-256 in portable C and Rust (`rt_c/orlog_rt.h`, `rt_rs/orlog_rt.rs` at HEAD), as
  `RUNTIME-SPEC.md` §1 requires (no builtins) (ESTABLISHED, read from the code).
- **The judge's ablation** (`work/speed/JUDGE-MEASUREMENTS.md` §3; MEASURED twice by the judge, not re-run here): on
  the SH law, removing the per-event SHA-256 takes the c99 time a direction from about 4.9–5.1 µs to 0.44 µs. That is
  91% of the time, about 0.18 µs an event (`derive-out.txt` §4).
- **Block counts** (derived here, `derive-out.txt` §3): an event's hashed message is 41 bytes plus its payload, so
  'A', 'P', 'Q', 'C', 'M' and RUN-1's 'T' and 'N' events take one SHA-256 compression each, while an 'E' item event
  (21-byte payload) takes two, and an 'S' line over 14 bytes two or more.

**Incremental and set commitments.**
- Zobrist (1970) [U]: a position's key is the XOR of random keys for its parts, updated by XOR on each move, at a cost
  proportional to the change.
- Bellare and Micciancio, "A New Paradigm for Collision-free Hashing: Incrementality at Reduced Cost" (1997) [U]:
  incremental, parallelizable collision-free hashing (MuHash, AdHash).
- Clarke, Devadas, van Dijk, Gassend, Suh, "Incremental Multiset Hash Functions and Their Application to Memory
  Integrity Checking" (2003) [U]: multiset hashes updated in time proportional to the change; the XOR form is only
  set-collision resistant.
- Verðandi's DSC-0 probe (`../Verdandi/docs/ROADMAP.md`, the DSC-0 entry): a tree commitment kept beside a chain
  verifies nothing of the chain's heads for less than replay costs (ESTABLISHED there). The flat hash of the whole
  state per edit grows with the world, past a tenth of a 60 Hz frame at 1,024 × 1,024 cells at the workshop's rate
  (MEASURED there). Its owner kept it an isolated reference probe.

**Derived here.** A digest's cost scales with what it covers: a whole-state hash with the state's size, a per-event
chain with the number of events, an incremental hash with the change. In Ørlǫg's per-event chain, 32 of the 54 bytes
an assignment hashes are the previous head, and every event pays its own padded compression (hundreds to thousands
of cycles on the published tables). Streaming a tick's event records (kind, clause, length, payload) through one
SHA-256 chained per tick would still commit every event in order, at about a third of the compressions: 22 bytes, or
0.34 of a block, for an assignment instead of one block, and 0.47 instead of two for an 'E' item (`derive-out.txt`
§8). That would be a new trace definition, and its time is NOT_MEASURED. A non-cryptographic hash is one to two
orders of magnitude cheaper per byte on these published tables, and buys no resistance to a forger.

## 10. Verðandi's records bearing on this survey (read, never written)

- `../Verdandi/docs/GHOSTS.md`: G4 (numbers from different harnesses compare as ratios within a run, never as
  absolutes across runs); G5 (one host, one corpus); G7 (render headroom reaches the screen only out of phase with the
  present; no low-latency, competitive or input-to-photon claim); G8 (the software frame is 14.8–15.7 ms at p50,
  longer than one refresh, with no dominant phase); G10 (thin statistics: at n = 200, p99 is the third-largest sample;
  the refresh estimate spread 63‰ over five runs; its remedies: 1,000 samples a cell so p99 is the 11th-largest, a
  same-run comparator, a declared margin, host-state snapshots); G13 (the same court 40–60% slower on another run the
  same day, cause unmeasured); G21 (the live loop has no latency, frame-rate or feel number; the route is one
  instrument per segment, registered before its number).
- `../Verdandi/graybox/README.md`, "The simulation's contract: rules 1" and "What is not shown": the browser
  engines' `Math.sin`, `Math.cos` and `Math.hypot` reached authoritative state and differed by one ULP between engines:
  node 22 against Chromium 141, `sin` on 5 of 745 arguments and `cos` on 2 of 745 (in Verðandi's build container);
  Firefox 157 against Chromium 141 on the owner's machine, `hypot` on 943 of 3,523 and `sin` on 1 of 745 (observed
  once). Rules 1 replace them with algorithms built only from operations ECMA-262 fixes, and every tick's snapshot then
  matched across Chromium 141, node 22, Firefox 157 and Edge 155 on the tactical map (MEASURED once, as Verðandi
  grades it; `../Verdandi/docs/ROADMAP.md`, DET-MATH-0).
- The same README's self-test section: a per-tick FNV-1a 64 state hash with plants against a hash blind to a leaf
  (`hash-coverage`); `fx-noninterference`, where a twin whose view feedback is changed must stay identical at every
  tick, with a planted tick that reads the flashes; `snapshot-resume`; `render-readonly`, where the state is the same
  after frames drawn by both renderers. These are tests of a view that never writes back.
- `../Verdandi/AGENTS.md` §8, the lesson "Hash whole numbers": a value interpolated by the GPU is not exact, and
  hashing it scattered results into noise (lesson 72).

## 11. Measurements and arithmetic made here

**`work/speed-research/scripts/sh_check.py`, rerun** (MEASURED on this host, Python 3.14.5, `PYTHONHASHSEED=0`,
`python -I -B sh_check.py 6 100000`; output `work/speed-research/sh_check-out.txt`):
- bands 0 to 6, 49 functions: each homogeneous of degree l and harmonic; 0 of 1,176 distinct pairs with a nonzero
  inner product over the sphere (exact rationals);
- K²π rational for every l ≤ 2 (1/4, 3/4, 5/48, 5/12, 5/4); K × the polynomial reproduces the constants usually
  cited (0.282095; 0.488603; 0.182091 × 6 = 1.092548 for xy; 0.630783 × (z² − x²/2 − y²/2) = 0.315392 (2z² − x² − y²);
  0.182091 × 3 = 0.546274 for x² − y²);
- on 100,000 seeded directions normalized on the Q31.32 grid (half-even products and quotients, floor square root):
  x² + y² + z² misses 1 by at most 2 raw units, and 3z² − 1 differs in raw value from 2z² − x² − y² in 49,951 of
  100,000; the assertion that 3z² − r² equals 2z² − x² − y² held on every direction.
- Does not show: Ørlǫg's own Fix (this is a Python model of RUNTIME-SPEC §2's rules, not `numeric_ref.py`); any error
  bound; any band above 6. Falsifier: a band-l polynomial that is not harmonic or not homogeneous, a nonzero
  off-diagonal inner product, or a different count on rerun with the same seed.

**`work/speed-research/scripts/derive.py`** (arithmetic, not a measurement of a machine; output
`work/speed-research/derive-out.txt`): periods for tick and refresh rates, Riot's per-game budget (2.3438 ms),
SHA-256 blocks per event kind, the judge's hashing share, rollback step budgets, per-tick commitment storage per hour
(32-byte heads at 128 Hz: 14.75 MB; 8-byte digests: 3.69 MB), binary-search probes (at most 19 for an hour at
128 Hz), and compressions per event chained per event against streamed per tick (§8 of the output).

---

## 12. What this means for Ørlǫg's four questions (my reasoning, derived here)

Everything in this section is SPECULATIVE unless it says otherwise.

### Q1. The two-speed design and the reconciler

1. **Detection and localization are separate layers.** Ørlǫg already localizes finely: the arbiter's `localize`
   (`src/orlog/arbiter.py`) names the first divergent event (an assignment, say), its kind, clause and both payloads
   (ESTABLISHED, read from the code). That is finer than any shipped game's tooling in this survey; only rr's
   single-step register logs go finer. What a two-speed setup lacks is the detection layer: a commitment the fast
   execution emits during play, cheap enough to keep, which the replaying executions recompute and compare.
2. **R5's 'T' event makes the head at each tick a cumulative per-tick commitment.** Because the chain is cumulative,
   a mismatch at tick t persists at every later tick, so the first differing tick can be found by binary search over
   per-tick heads: at most 19 comparisons for an hour at 128 Hz (`derive-out.txt` §7). This holds barring a SHA-256
   collision. A per-tick state hash that is not chained would allow a divergence to "heal" and would need a linear
   scan.
3. **What the sheet does not yet say.**
   - **A per-tick record.** Receipt 1 holds totals and the trace holds every event. Lockstep systems exchange a
     digest per tick or per interval and fetch detail on demand. A per-tick record (tick, events so far, ops so far,
     head at 'T', output-chain value) is the comparable unit, and the sheet names no artifact for it.
   - **Operations per tick.** Today an ops-only difference, with equal traces, is reported as "traces equal; the
     difference is outside the event chain" (arbiter, ESTABLISHED). With ticks, R9's budget makes per-tick ops
     decisive, so committing ops in the 'T' payload or in the per-tick record would locate such a difference to its
     tick.
   - **Inputs against computation.** With 'N' events in the chain (R5), the kind of the first divergent event would
     tell an input difference from a computational one, as Verðandi's comparator does by reporting the first
     differing input and the first differing state separately. The sheet's formats would cover this once built.
4. **The commitment's cost during play.** On the SH law, about 91% of a compiled backend's time is the per-event
   SHA-256 (the judge, MEASURED). Three ways out appear in the prior art and the arithmetic, each with a price:
   - keep the per-event chain and pay for it;
   - chain per tick instead, streaming the tick's event records through one SHA-256 (about a third of the
     compressions, §9). It stays cryptographic and still commits every event in order, but it is a new trace
     definition, and RUN-1 is the rung that writes `orlog-trace-1`;
   - add a second, cheaper digest per tick, or the chain only every N ticks (as Photon Quantum and 0 A.D. do), which
     the replaying executions compute too. That digest would be evidence of nothing; it would only bring detection
     forward.
   In every case admission keeps a full cryptographic commitment on all four executions.

### Q2. A language swap, and a GPU authority

1. **A faster language would not remove the measured costs.** The judge's ablation puts the arithmetic at about a
   tenth of the compiled marginal time on that law and the rest in hashing; the skeptic's measurements put the cost of
   a run in process starts and rebuilds. A faster language leaves both in place. None of the lockstep sources read
   names its implementation language as its limit (DECLARED: an absence in what was read).
2. **A GPU as authority conflicts with the law's rule that the reference is the authority**, and the prior art adds
   reasons on its own:
   - 64-bit integers are optional (68% of devices in one database, OBSERVED) or absent (WGSL);
   - edge cases are unspecified in some instruction sets (PTX division by zero [U]) where the runtime contract refuses
     instead;
   - the shader compiler is the driver's, so every driver update is a new compiler; Verðandi's G6, by its heading,
     holds instruction-level invariance to be a goal and not a proof;
   - consumer GPUs showed memory soft errors in the field (Haque and Pande, 2009);
   - the shipped deterministic GPU simulations claim self-consistency on a platform, never agreement across vendors;
   - the per-event chain is a total order, while a GPU's work is parallel; a tree commitment would be a new content
     function, and Verðandi's DSC-0 found that a tree kept beside a chain verifies none of the chain's heads.
3. **What could exist** is a GPU backend as a fifth execution, Int and Fix only, held to the reference's receipt byte
   for byte by the arbiter, its partial products built from 16-bit limbs where only 32-bit integers exist. It would be
   evidence by agreement, never authority.

### Q3. The view tier

1. **The prior art separates simulation from view** by rate (Supreme Commander's 10 Hz simulation and 60 fps view;
   VALORANT's fixed 128 Hz step with interpolation) and by state: GGPO leaves the renderer and audio out of saved
   state and defers rendering until a rollback ends; NetherRealm keeps particles and sounds out of rollback; Riot claims
   gameplay determinism only. The view reads after the tick settles and has no path back.
2. **Ørlǫg could hold the view tier the way Verðandi holds its renderers.** The receipt with a view attached must be
   byte-identical to the receipt without one (as `render-readonly` does). A view that writes back is a plant that
   must be refused (as `fx-noninterference` does with a tick that reads the flashes). The view consumes the tick's
   events, which SKEPTIC.md already reads as a stream of state changes, and never a port: floats stay out (R8 b), and
   no GPU float is hashed (Verðandi's lesson 72).
3. **What must be in the law, in Fix, is whatever decides play.** That is Verðandi's rule, as
   `research/speed/PROPOSAL.md` and Verðandi's `AGENTS.md` §3 state it from `../Verdandi/docs/BOUNDARIES.md` (not
   itself read here): the renderer may decorate and must not decide what blocks. VALORANT's hit registration is
   decided on the server by a rewind, not by the client's picture. A graphical quantity enters the law only if a rule
   reads it: a line of sight, or a light level that a stealth rule reads. SH lighting can then be computed in Fix (the
   judge measured agreement on bands 0 to 2), with its spelling, sign convention and constants declared and its error
   bound stated. Otherwise SH stays in the view, in float, hashed by nothing.

### Q4. A headroom standard written Verðandi's way

1. **There is no published competitive latency standard to adopt.** The instruments differ by their endpoints, and
   Verðandi's G7 and the debate's fixed rules forbid a latency claim. "Headroom" should therefore be stated in the
   law's own terms: the resident execution's per-tick compute time relative to a declared tick period, on a named
   host, against a comparator in the same run. It is a software timing, never a latency.
2. **A preregistered measurement**, fixed before any number (each value the owner's to rule):
   - **Quantity:** wall time per tick of the resident execution, from the high-resolution counter, with the clock's
     step stated (`time.perf_counter` is 1e-07 s here, per the judge's record).
   - **Sample:** N ≥ 1,000 ticks a cell after a declared warm-up, so that p99 is the 11th-largest; report the 12
     largest beside it (G10).
   - **Cells:** law × execution (c99, Rust; the reference as a comparator) × commitment (the chain on, and off as an
     ablation, as the judge did).
   - **Comparator:** cells interleaved in one run; only within-run ratios carry across runs (G4, G13).
   - **Margin:** declared before the run, for example p99 at most half the period at the declared tick rate (3.9 ms at
     128 Hz). Riot's 2.34 ms a game is one studio's budget, not a standard.
   - **Host:** named by its record, with host-state snapshots beside the run (G13).
   - **Verdict and boundary:** a label, never a latency, frame rate, input-to-photon figure or feel; nothing about
     another host.
   - If prediction or rollback is ever adopted, the cell becomes W + 1 steps a frame.
3. **An input-to-photon number, if ever wanted**, needs one instrument per segment, each registered before its number
   (G21): device to OS (a USB analyzer), OS to Present and Present to flip (PresentMon's events), flip to light (a
   photosensor, as VESA's gray-to-gray method uses, or NVIDIA's analyzer). A software-only tool such as FLM covers only
   part of the path.

## 13. Open points the debate should settle

1. Does RUN-1 define a per-tick record (tick, events, ops, head at 'T', output chain) as part of its formats, or is
   that left to SNAP-1 or SESSION-0?
2. Should the 'T' event's payload, or that record, carry the tick's operation count, so that an ops-only divergence
   (equal traces) is located to its tick, given that R9 makes per-tick ops decisive?
3. Does the fast play execution keep the per-event SHA-256 chain, or emit a cheaper per-tick digest that the
   replaying executions also compute? If cheaper: which function, at what interval, and with what written status (it
   detects; it never evidences)?
4. Since RUN-1 writes `orlog-trace-1` anyway: should it chain per event, as R5 has it, or per tick over the tick's
   event records (about a third of the SHA-256 compressions, still committing every event in order, localization
   within a tick then read from the trace's records)? Its time would have to be measured before anyone relies on it.
5. When does the reconciler compare: every tick, every N ticks, or at session end? What does a mismatch do: stop the
   session, mark the branch (R4's rule), or continue with the verdict pending?
6. Is "reconciler" in the owner's sense the lockstep check (agreement, mismatch as defect) and not the genre's client
   reconciliation (overwrite and replay)? The survey reads it as the former; the owner's word is the owner's to gloss.
7. Can the view tier be held by a plant (the receipt with and without a view byte-identical; a writing view refused)
   before any view is built?
8. Does any rule read a graphical quantity (light level, line of sight)? If so: is the SH basis declared with its
   spelling, sign convention and constants (rounded literals or folded into data), and is its error bound stated?
9. Is a GPU backend in scope at all? If so: Int and Fix only, a fifth execution under the arbiter and never an
   authority; how 64-bit products are built where WGSL has 32-bit integers only; and what a driver update means for
   its identity.
10. Float ports (R8 b): the cross-host evidence the sheet asks for first (HOST-0) should include transcendental
    functions, which the prior art and Verðandi both measured differing between libraries and engines.
11. The headroom measurement: the tick rate, the margin, the sample size, the comparator, the host record; and whether
    rollback's W + 1 steps are in scope.
12. Do the four executions count as N-version evidence at all, given Knight and Leveson and a single author? Is the
    twin's paper round (R7) the remedy, or does it need diversity of reading too?
13. List-heavy laws pay two SHA-256 compressions per 'E' item event. Does the cost model for any commitment budget
    count blocks, not events?

---

## Sources

Grades as in "How to read this". Local files are repository-relative.

**Ørlǫg** (read at HEAD f16dc26 from the snapshot): `research/speed/PROPOSAL.md`; `RUNTIME-SPEC.md` §1, §2, §5, §7;
`research/run-1/RULINGS.md` (R4–R10, D1–D10); `research/roadmap-debate/SKEPTIC.md`; `src/orlog/arbiter.py`
(`localize`); `rt_c/orlog_rt.h`; `rt_rs/orlog_rt.rs`; `README.md` and `AGENTS.md` §6 (claim grades);
`work/speed/JUDGE-MEASUREMENTS.md` (the judge's record).

**Verðandi** (read only): `../Verdandi/docs/GHOSTS.md` (G2, G4, G5, G7, G8, G10, G13, G21; G6 and G23 by heading);
`../Verdandi/graybox/README.md`; `../Verdandi/docs/ROADMAP.md` (DET-MATH-0, DSC-0); `../Verdandi/AGENTS.md` §3 and §8.

**§1** [P] https://www.gamedeveloper.com/programming/1500-archers-on-a-28-8-network-programming-in-age-of-empires-and-beyond ·
[P] https://factorio.com/blog/post/fff-47 · [P] https://factorio.com/blog/post/fff-55 ·
[P] https://factorio.com/blog/post/fff-76 · [P] https://factorio.com/blog/post/fff-188 ·
[P] https://github.com/OpenTTD/OpenTTD/blob/master/docs/desync.md ·
[P] https://github.com/OpenTTD/OpenTTD/blob/master/docs/debugging_desyncs.md ·
[P] https://www.forrestthewoods.com/blog/synchronous_rts_engines_and_a_tale_of_desyncs/ ·
[P] https://www.forrestthewoods.com/blog/synchronous_rts_engines_2_sync_harder/ ·
[P] https://raw.githubusercontent.com/0ad/0ad/master/source/simulation2/system/TurnManager.cpp ·
[P] https://raw.githubusercontent.com/0ad/0ad/master/source/network/NetClientTurnManager.cpp ·
[P] https://raw.githubusercontent.com/0ad/0ad/master/source/simulation2/system/ComponentManagerSerialization.cpp ·
[P] https://raw.githubusercontent.com/0ad/0ad/master/source/simulation2/serialization/HashSerializer.h ·
[U] https://wildfiregames.com/forum/topic/89632-is-5-turns-per-second-too-many/ ·
[P] https://www.riotgames.com/en/news/determinism-league-legends-introduction ·
[P] https://www.riotgames.com/en/news/determinism-league-legends-unified-clock ·
[P] https://www.riotgames.com/en/news/determinism-league-legends-implementation ·
[P] https://www.riotgames.com/en/news/determinism-league-legends-fixing-divergences

**§2** [P] https://github.com/pond3r/ggpo/blob/master/doc/DeveloperGuide.md ·
[P] https://raw.githubusercontent.com/pond3r/ggpo/master/src/lib/ggpo/sync.h · [P] https://docs.rs/ggrs/latest/ggrs/ ·
[P] https://docs.rs/ggrs/latest/ggrs/struct.SessionBuilder.html ·
[U] https://gdcvault.com/play/1025021/8-Frames-in-16ms-Rollback (listing via search; the vault was in maintenance) ·
[S] https://edgegap.com/blog/game-backend-deep-dive-mortal-kombat-x-injustice-2-rollback

**§3** [P] https://gabrielgambetta.com/client-side-prediction-server-reconciliation.html ·
[P] https://www.riotgames.com/en/news/peeking-valorants-netcode · [P] https://www.riotgames.com/en/news/valorants-128-tick-servers ·
[U] https://www.counter-strike.net/cs2 · [U] https://gdcvault.com/play/1024001/-Overwatch-Gameplay-Architecture-and ·
[U] https://www.tweaktown.com/news/53392/overwatchs-upcoming-pc-patch-improve-tick-rate/index.html ·
[U] https://www.pcgamer.com/apex-legends-tick-rate/ ·
[U] https://edgegap.com/blog/game-server-tick-rate-explained-gameplay-precision-vs-infrastructure-cost ·
[U] https://developer.valvesoftware.com/wiki/Latency_Compensating_Methods_in_Client/Server_In-game_Protocol_Design_and_Optimization (HTTP 403) ·
[P] `work/speed-research/dl/wpi-21-06/wpi-21-06.pdf` (https://ftp.cs.wpi.edu/pub/techreports/pdf/21-06.pdf)

**§4** [P] https://port70.net/~nsz/c/c11/n1570.html · [P] https://open-std.org/JTC1/SC22/WG21/docs/papers/2025/p3375r3.html ·
[P] https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html · [P] https://clang.llvm.org/docs/UsersManual.html ·
[P] https://learn.microsoft.com/en-us/cpp/build/reference/fp-specify-floating-point-behavior ·
[P] https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/index.html · [P] https://docs.nvidia.com/cuda/floating-point/index.html ·
[P] https://rust-lang.github.io/rfcs/3514-float-semantics.html ·
[P] https://docs.vulkan.org/spec/latest/appendices/spirvenv.html ·
[P] https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.html · [P] https://www.w3.org/TR/WGSL/ and
https://raw.githubusercontent.com/gpuweb/gpuweb/main/wgsl/index.bs ·
[P] https://learn.microsoft.com/en-us/windows/win32/direct3d11/floating-point-rules ·
[U] https://github.com/microsoft/DirectXShaderCompiler/wiki/Shader-Model-6.2 ·
[U] https://developer.apple.com/documentation/metal/mtlcompileoptions/mathmode.md ·
[P] `work/speed-research/dl/accuracy/glibc242.pdf` (Gladman, Innocente, Mather, Zimmermann, August 2025) ·
[P] https://arxiv.org/html/2410.09172v1 · [P] https://box2d.org/posts/2024/08/determinism/ ·
[P] https://gafferongames.com/post/floating_point_determinism/ ·
[P] https://randomascii.wordpress.com/2013/07/16/floating-point-determinism/ · [U] https://arxiv.org/html/2403.00232v1

**§5** [P] https://vulkan.gpuinfo.org/listfeaturescore10.php ·
[P] https://docs.vulkan.org/refpages/latest/refpages/source/VkPhysicalDeviceFeatures.html ·
[P] https://learn.microsoft.com/en-us/windows/win32/api/d3d12/ns-d3d12-d3d12_feature_data_d3d12_options1 ·
[U] https://developer.apple.com/metal/Metal-Feature-Set-Tables.pdf ·
[U] https://docs.nvidia.com/cuda/parallel-thread-execution/index.html · [P] https://ambermd.org/GPULogistics.php ·
[U] https://ambermd.org/gpus14 · [P] https://docs.openmm.org/latest/userguide/library/04_platform_specifics.html ·
[U] https://arxiv.org/pdf/2011.01207 · [U] https://people.ece.ubc.ca/aamodt/papers/jooybar.asplos2013.pdf ·
[U] https://engineering.purdue.edu/tgrogers/publication/chou-micro-2020/ · [A] https://arxiv.org/abs/2609.11356 ·
[P] https://doc.photonengine.com/quantum/v3/manual/quantum-ecs/fixed-point · [P] https://github.com/mas-bandwidth/fixed ·
[A] https://arxiv.org/abs/0910.0505

**§6** [A] https://history.siggraph.org/?p=116946 · [A] https://jankautz.com/publications/prtSIG02.pdf (text read here) ·
[P] https://www.ppsloan.org/publications/StupidSH36.pdf (text read here) ·
[P] `work/speed-research/dl/sloan-jcgt/paper.pdf` (JCGT 2:2, 2013) ·
[P] https://fpga.mit.edu/videos/2009/team01/report.pdf (text read here) ·
[U] https://kb.osu.edu/items/53bbdaaf-649d-4b54-a9a2-50d0cd99828c

**§7** [P] `work/speed-research/dl/spjut2019/paper.pdf` (doi 10.1145/3355088.3365170) ·
[P] https://www.nvidia.com/en-us/geforce/news/reflex-low-latency-platform/ ·
[P] https://gpuopen.com/learn/frame-latency-meter-flm-1-0/ ·
[U] https://www.tomshardware.com/video-games/pc-gaming/amd-introduces-free-and-open-source-frame-latency-meter-utility-works-with-all-gpus-no-high-speed-camera-or-sensor-required ·
[P] https://github.com/GameTechDev/PresentMon/blob/main/README-ConsoleApplication.md ·
[P] https://developer.android.com/games/sdk/frame-pacing ·
[P] https://vesa.org/wp-content/uploads/2022/05/Adaptive-Sync-Display-CTS-r1.0.pdf (text read here) ·
[U] https://www.itu.int/rec/T-REC-G.1072 · [U] https://www.techspot.com/community/topics/msi-reveals-600hz-gaming-monitor-koorui-one-ups-with-750hz-model.290087/ ·
[U] https://hothardware.com/news/aoc-540hz-agon-gaming-monitor-dominate-esports

**§8** [P] `work/speed-research/dl/rr/rr.pdf` (O'Callahan et al., extended technical report) ·
[U] https://people.csail.mit.edu/mareko/asplos073-olszewski.pdf · [U] https://people.cs.umass.edu/~emery/pubs/dthreads-sosp11.pdf ·
[A][S] https://www.kth.se/social/files/564df871f2765419e306178d/KnightLeveson.pdf (text read here) ·
[U] https://arxiv.org/pdf/1504.03256 · [U] https://www-old.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf ·
[U] https://dblp.org/pid/40/4856 · [U] https://www.usenix.org/legacy/events/sec06/tech/cox.html

**§9** [P] https://doc.photonengine.com/quantum/v3/manual/config-files ·
[U] https://doc-api.photonengine.com/en/quantum/current/class_photon_1_1_deterministic_1_1_deterministic_session_config.html ·
[P] https://github.com/Cyan4973/xxHash · [P] https://bench.cr.yp.to/results-hash/amd64-rumba7.html ·
[P] https://bench.cr.yp.to/results-hash/amd64-samba.html · [U] https://minds.wisconsin.edu/handle/1793/57624 ·
[U] https://eprint.iacr.org/1997/001 · [U] https://dspace.mit.edu/handle/1721.1/149987

**Local reading aids** (`work/speed-research/`): `scripts/pdftext.py`, `scripts/sh_check.py`, `scripts/derive.py`,
`scripts/renumber_open_points.py` (a one-off edit aid for this file), `txt/` (extracted texts), `sh_check-out.txt`,
`derive-out.txt`, `tree/` (the HEAD snapshot).
