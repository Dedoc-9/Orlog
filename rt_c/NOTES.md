# ORLOG OL-0: the C99 runtime (rt_c)

Written 2026-10-25 against `RUNTIME-SPEC.md` (DECLARED 2026-10-25) and `src/orlog/numeric_ref.py`. Everything
below was run on one Windows host: clang 22.1.8, target `x86_64-pc-windows-msvc`, Python 3.14.5. Nothing under
`rt_rs/` was read. `numeric_ref.py`, the vectors and `check_chain.py` were read and run, never edited.

## Files

| file | what |
|---|---|
| `orlog_rt.h` | the runtime: one header, every function `static inline`, ISO C99, only the seven headers the spec allows |
| `test_rt.c` | the harness: every vector line, the event-chain check of section 9, and 34 extra checks |
| `smoke.c` | a stand-in for a generated program: init, builder, say, every event kind, must, claims, finish (`-DSMOKE_REFUSE`: ends refused) |
| `check_smoke.py` | rebuilds a smoke run's expected output, events, chain and receipt from the spec's encodings (struct, hashlib) and numeric_ref's own values and formatters, without the C runtime, and compares them byte for byte |
| `plants.py` | planted defects: 26 one-line changes to copies of the header, each of which must be caught by a witness, plus an unchanged control that must pass |
| `run-O2.txt`, `run-O0.txt`, `plants-run.txt`, `check_chain-output.txt`, `build-O*.log` | the outputs of the last runs (the build logs are the compiler's whole output: empty). *Dated 2026-10-25 (prosecutor F34):* recorded at commit 83eb044, before E21 changed the header; run again on the changed header they are identical (the prosecutor's re-run; for the vectors, `evidence/rt_c-vectors-O2.txt` and `-O0.txt`) |
| `chain-*.txt`, `smoke-*.txt` | the files those runs wrote (receipts, traces, outputs) |

## Results

Each was run here, on the host above. None is a claim about another compiler, platform or libm.

- **MEASURED.** `test_rt.exe ..\vectors\runtime-vectors.txt` prints `RUNTIME VECTORS 20015 / 20015` built at `-O2`
  (the required command) and at `-O0`. No line fails, and the two outputs are byte-identical. The vectors file's
  sha256 is the spec's `841240b7...f204`. A refusable line passes only if two calls agree with it: the pure function
  (code through an out-parameter) and the contract's `orl_*` wrapper. The wrapper's refusal is seen through the
  `ORL_TEST` hook, and the clause it carries is checked too. Print lines pass through both the formatter and the
  builder, and SHA-256 lines one-shot and streamed (1, 7, 63 and 64 bytes at a time).
- **MEASURED.** Chain heads, identical to `python -B src\check_chain.py` (compared with `diff` after removing the CR
  that Python's redirected stdout adds on Windows):
  `head0 0cc0deef006a60381a23a0e869077ebae76e4ecca00696b16f2878b4b62f97ca`,
  `head1 4accb3403d8415a2b4d8e81dda37d99ea98dbe20366a240cfd2b7faa1df268c4`,
  `head2 22d273a90da5710475ffdb2c745f19fabd69bd215390a0ec29593f5d28fd1992`,
  `head3 bd0494368f0ffb775791853f0d178c10470402a5b7e642b1ba75969e4dfb6ad9`.
  The chain runs through the real API (`orl_init` with files, `orl_say`, `orl_ev_assign_i`, `orl_refuse`). Its trace
  and its `REFUSED OVERFLOW 3` receipt were checked against those heads.
- **MEASURED.** Zero compiler diagnostics with `-std=c99 -pedantic -Wall -Wextra -ffp-contract=off -fno-fast-math` at
  `-O2` and `-O0` for `test_rt.c`, for `smoke.c` and its refusing variant, and for a minimal program that includes
  the header and calls nothing (with and without `ORL_TEST`). `-Weverything` (information only, compiling `smoke.c`)
  reports inside the header only `-Wunsafe-buffer-usage` (raw pointers, inherent in C) and `-Wmissing-noreturn`. The second cannot be
  answered in C99 without an extension. There are no conversion or sign warnings.
- **MEASURED.** `check_smoke.py` finds both smoke runs equal to its independent reconstruction: output (1335 and 1353
  bytes), every trace line (36 and 38 events) and the whole receipt.
- **MEASURED.** `plants.py`: all 26 planted defects are caught and the control is clean. The plants cover rounding
  ties, Euclid, refusal order, isqrt, conversions, NaN canonicalisation, f_max, printing, SHA-256, a wrapper's
  clause, the chain's byte order, output hashing, F and B encodings, claim accumulation, the three limits and list
  indexing. Two first runs were not clean, and both are recorded here:
  - The B-encoding plant was missed at first. Measured cause: `orl_ev_assign_b` and `orl__enc_elem` both
    normalised, so either copy alone was an equivalent mutant. Normalisation now happens once, in `orl__enc_elem`.
    An extra check (`ev_assign_b` with 2 gives the same head as with 1) catches the plant.
  - An ASan plant of the Float buffer at 1076 bytes was not reported. Measured cause: the longest text in the
    vectors is 1076 bytes. An extra check now prints the negative smallest subnormal (1077 bytes). ASan is silent at
    1077 and reports at 1076, so the bound is exact. The header allows 1100.
- **MEASURED, on executed paths only.** A UBSan build in trap mode
  (`-fsanitize=undefined,float-divide-by-zero -fsanitize-trap=...`) of the final harness runs the vectors (20015 /
  20015), the chain and the 34 extras, and both smoke variants, without a trap. As an apparatus check, a planted unchecked `a + b` in `i_add` traps (exit 132). An ASan
  build (its runtime DLL put on PATH from `C:\Program Files\LLVM\lib\clang\22\lib\windows`) runs everything clean.

**A defect of the harness, found and repaired.** At first the harness wrote its chain files into the working
directory. At 16:02 a run of `test_rt.exe` with `orlog\` as its working directory left `chain-output.txt`,
`chain-receipt.txt` and `chain-trace.txt` at the top of `orlog\`. Every command of mine set `rt_c\` as the working
directory, so the run was most likely another agent's check. They are byte-identical to `rt_c`'s and
`backend c99`. The files now go beside the executable (`exe_dir` from `argv[0]`). Run from `orlog\`, the harness
was measured to write into `rt_c\` and leave the top-level files unchanged. Those three files are outside this
folder, so they were left in place; deleting them loses nothing.

`does_not_show`. Sanitizers see only the paths that ran. The "never evaluated" claims for signed overflow,
`INT64_MIN / -1` and `% -1` rest on reading the code, which tests before every computation, and the UBSan run
supports them for these inputs. `orl_f_sqrt` uses the C library's `sqrt`, which IEEE 754 requires to be correctly
rounded; it agreed with all 161 vectors here, and nothing more is shown. The float operations assume IEEE binary64
arithmetic in round-to-nearest (see finding 6). The 2^24 list allocation and the 2^24 builder were exercised; a 2^30
output was not written (the limit was tested by setting the byte counter). Falsifiers: any vector line, any head,
any smoke byte or any plant verdict that differs on a re-run.

## Design decisions the spec left open

1. **Refusals: a pure function and its wrapper.** `orl__NAME(..., const char **e)` returns the value and sets `*e`.
   `orl_NAME(..., c)` calls `orl_refuse(*e, c)`. With `ORL_TEST` defined, `orl_refuse` and `orl_finish` call
   `orl_test_refuse_hook(code, c)` (code NULL for finish). They do so after the 'R' event, the receipt and the
   closing of the files, and before `exit`. The harness's hook longjmps, so `setjmp.h` is in the harness only and
   the header uses only the seven allowed headers.
2. **`static inline` for every function.** This was measured here. An unused plain `static` function in a header
   draws `-Wunused-function`, so a generated program that uses part of the runtime would not compile warning-free.
   An unused `static inline` function in a header draws nothing. The C header must therefore be `#include`d, not
   pasted into the program's own file: in the main file even `static inline` draws the warning.
   *Note (the maintainer, 2026-10-25, prosecutor F33):* `src/orlog/gen_c.py` pastes the header into each generated
   program all the same, so a generated program compiled under the contract's flags draws `-Wunused-function` (57
   warnings for collatz.c, observed by the prosecutor). The arbiter builds with `-Wno-unused-function` (`C_FLAGS` in
   `arbiter.py`), so its builds are silent. The decision stands for the header used as a library; the generator
   departs from it.
3. **`_CRT_SECURE_NO_WARNINGS`** is defined on `_WIN32` before the first include. On this host `fopen` otherwise
   draws `-Wdeprecated-declarations` (measured). The header must come before any other header.
4. **Int to double** (`f_from_i`, `x_to_f`): the integer is rounded to at most 53 bits by integer arithmetic (ties to
   even), cast (exact for at most 53 bits), then scaled by `ldexp` (exact: every result is normal or zero). Double
   to Int (`f_to_x`, `f_trunc`, `f_round`) works on the bits: |x| = m * 2^k.
5. **128-bit work**: products from 32-bit halves. A quotient comes from a native division of the high word, then
   64 restoring shift-subtract steps. `isqrt` runs two bits at a time over a 128-bit radicand (precondition < 2^120;
   callers pass at most 2^95). Fix rounding is done on magnitudes, because half-even is symmetric.
6. **Float printing**: m is reduced to odd. For e >= 0 the bignum is multiplied by 2^29 per step; for e < 0 by 5^13
   per step, and the point is placed (-e) digits from the right, which yields exactly (-e) fraction digits, the last
   a 5. The bignum is base 10^9 in `uint32_t` limbs.
7. **`f_div` by zero** is written out as numeric_ref writes it, not left to the C division (finding 6).
   **`f_sqrt`** tests for NaN and negatives before calling `sqrt`.
8. **Encodings**: a Float is written with its canonical bits wherever it is encoded (an 'A' scalar, list elements,
   'E' and 'P'), and a Bool as one byte that is 1 for any nonzero slot or C truth value.
9. **Say** leaves the builder as it is; the generated code resets it. Appends made before any `orl_s_reset` refuse
   with clause 0.
10. **Exit statuses beyond the spec's 0 and 2.** Status 2 covers a missing output or receipt path, a file that cannot
    be opened, and a file that cannot be written. On a write failure, output and trace are closed first, and the
    receipt is written only if they closed cleanly, so a receipt never describes a failed file. Status 3, with a
    message on stderr, covers misuse by the generated code and memory: a seal that is not exactly 64 hex digits, a
    claim id at or above `n_claims`, an unknown tag, a list literal above 2^24, an event payload whose bytes differ
    from its declared length, and out of memory.
11. **Seals** are accepted in either case and printed in lowercase in the receipt.
12. **Claim cost** accumulates modulo 2^64 (C unsigned).
13. **`orl_ops`** is `static`, which suits a program that is one translation unit.
14. **Added beyond the contract**: `orl_l_free`. The contract has no way to release a list or an `orl_s_take` copy
    (finding 8).
    *Note (the maintainer, 2026-10-25, prosecutor F35):* since E21's repair the runtime frees temporaries when each
    statement ends and replaced buffers on each store, and the contract says so (RUNTIME-SPEC §4a). `orl_l_free`
    stays, and the generator does not call it. Its comment in `orlog_rt.h` ("the runtime never frees one") is stale,
    and is to be corrected with the header's next change, so that the recorded runs of this round stay of one header.

## Findings about the spec and numeric_ref

1. **numeric_ref contradicts itself on NaNs; the vectors follow the functions.** Its docstring says every NaN result
   is replaced by the canonical quiet NaN, and that this replacement is part of the semantics. But `f_max` and
   `f_min` return a NaN operand unchanged, as the spec's `a > b ? a : b` requires, and the vectors enforce it
   (line 11248: `f_max f:0000000000000000 f:FFF8000000000000 => f:FFF8000000000000`). So `f_bits` can observe a
   non-canonical NaN that entered through `bits_f`. Events and printing canonicalise, so traces still agree. These
   two functions are also not symmetric: `f_max(NaN, x) = x` but `f_max(x, NaN) = NaN` (line 16041 for `f_min`).
   The docstring, or the semantics, should say which is meant.
2. **"Begin with `#if FLT_EVAL_METHOD != 0`"** cannot be literal. Without `<float.h>` first, the macro is undefined,
   `#if` reads it as 0, and the check passes vacuously. The header includes `<float.h>` and then checks.
3. **Section 4 names `orl_s_reset()` without an argument**, then says it takes `c`. The header takes `c`.
4. **The exit statuses** cover only "completed or refused" (0) and "cannot open" (2). Running out of memory, misuse
   by the generated code, and write failures are unspecified; decision 10 is this runtime's answer, and the Rust
   runtime may answer differently.
5. **The list encoding** says "8 bytes each for I/X/F" without saying that F elements are canonical, as the scalar
   F encoding is. B elements are said to be 1 byte but not normalised. Decision 8 canonicalises and normalises.
   The index in 'E' is not said to be 0- or 1-based; the generator decides.
6. **The float semantics assume IEEE 754 (C99 Annex F),** which the header cannot test. Clang on this target does not
   define `__STDC_IEC_559__`. C99 leaves a zero divisor undefined even for doubles, which decision 7 avoids. The
   other exceptional cases, overflow to infinity, inf - inf, and 0 * inf, still rely on IEEE behaviour from the
   compiler and the hardware. The header checks only `FLT_EVAL_METHOD`, `FLT_RADIX`, `DBL_MANT_DIG`,
   `DBL_MAX_EXP`, `DBL_MIN_EXP` and `CHAR_BIT`.
7. **`orl_l_from(n, slots)` has no clause**, so a literal longer than 2^24 cannot refuse `LIST-TOO-LONG` (decision
   10). Claim cost overflow is unspecified (decision 12).
8. **No release** for lists or texts: a generated loop that copies a list or takes a text grows without bound.
9. **Table gaps**: the "vector op" column is empty for `x_trunc`, `x_round`, `x_max`/`x_min`, `f_trunc` and
   `f_round`, yet the vectors hold all of them. `f_lt` and `f_eq` vectors exist with no runtime function: they test
   the generated code's native `<` and `==`, as the harness does.

## The vectors

No vector line is believed wrong. All 20,015 agree with this runtime, written from numeric_ref's definitions. Two
lines worth noticing, both as numeric_ref defines them: `i_quot` refuses `(INT64_MIN, -1)` with `OVERFLOW`, but
`i_rem` returns 0 for the same pair (lines 1793 and 1794). Coverage limits observed: binary float operations never
receive a signalling NaN (the fixed pairs stop before the sNaNs), and the longest `fmt_f` text is 1076 bytes, not
the 1077 a negative subnormal prints. The extra checks cover the second.

## Commands (from `...\scratchpad\orlog\rt_c\`, Git Bash or cmd)

*Note (the maintainer, 2026-10-25, prosecutor F36):* the scratch folder is gone; the project lives in its repository.
Run these from the repository's root as AGENTS.md §4 gives them, with the chain folder as the harness's second
argument, so that the tracked `rt_c/chain-*.txt` are not rewritten.

```
clang -std=c99 -pedantic -Wall -Wextra -O2 -ffp-contract=off -fno-fast-math test_rt.c -o test_rt.exe
clang -std=c99 -pedantic -Wall -Wextra -O0 -ffp-contract=off -fno-fast-math test_rt.c -o test_rt_O0.exe
test_rt.exe ..\vectors\runtime-vectors.txt            (chain-*.txt go beside the exe; a 2nd argument names another folder)
test_rt_O0.exe ..\vectors\runtime-vectors.txt
cd .. && python -B src\check_chain.py                  (compare its four lines with the harness's head0..head3)

clang -std=c99 -pedantic -Wall -Wextra -O2 -ffp-contract=off -fno-fast-math smoke.c -o smoke.exe
clang -std=c99 -pedantic -Wall -Wextra -O2 -ffp-contract=off -fno-fast-math -DSMOKE_REFUSE smoke.c -o smoke_refuse.exe
smoke.exe smoke-output.txt smoke-receipt.txt smoke-trace.txt
smoke_refuse.exe smoke-refuse-output.txt smoke-refuse-receipt.txt smoke-refuse-trace.txt
python -B check_smoke.py smoke-output.txt smoke-receipt.txt smoke-trace.txt complete
python -B check_smoke.py smoke-refuse-output.txt smoke-refuse-receipt.txt smoke-refuse-trace.txt refuse

python -B plants.py                                    (about a minute; builds in plants_build\, then removes it)
```

Set `PYTHONHASHSEED=0` for the Python runs, and `PYTHONUTF8=1` when output is redirected.

## 2026-10-25, later: text and list ownership (red team E21; finding 8 above)

Added by the reference's maintainer, not by this runtime's author. Finding 8 ("no release for lists or texts") is
repaired in this header and in the C generator (`src/orlog/gen_c.py`, `src/orlog/lower.py`):
- A text made by `followed by` (`orl_s_take`) and every new list (`orl_l_new`, `orl_l_from`, and so `orl_l_copy`)
  is pushed on a temp stack. The generated code takes a mark (`orl_tmp_mark`) before each clause statement and each
  While iteration, and releases back to it (`orl_tmp_release`) afterwards.
- A text variable owns a static slot (`orl_tslot`; `orl_t_store` copies, then frees). A list variable owns its
  buffer (`orl_l_store` copies in). A procedure's list locals are static.
- The bound rests on the language's rules of no recursion and no text in a list:
  - live text ≤ (text variables + the text temporaries along one chain of active statements + the builder) × 2^24
    bytes;
  - live list memory ≤ (list variables + the list temporaries along that chain) × 2^24 × 8 bytes.

MEASURED here, 2026-10-25 (files in `evidence/`):
- `RUNTIME VECTORS 20015 / 20015` at -O2 and at -O0, the two outputs byte-identical (`e21-rt_c-vectors-O2.txt`).
- The red team's `memleak.py`, a 16 MiB text rebuilt N times (Python's peak was 113 MiB throughout;
  `e21-memleak-before.txt`, `e21-memleak-after.txt`):

  | | N = 5 | N = 20 | N = 40 |
  |---|---|---|---|
  | C peak commit, before | 130 MiB | 370 MiB | 691 MiB |
  | C peak commit, after | 58 MiB | 58 MiB | 58 MiB |

- A 2,000,000-item list stored N times: 77 and 505 MiB at N = 4 and 32 before, and 46 and 46 MiB after
  (`e21-lists-before.txt`, `e21-lists-after.txt`). *Corrected 2026-10-25 (prosecutor F15):* this line said the
  figures before were "measured on commit 7186e50". The script imports `child_peak` from `tests/selftest.py`, which
  7186e50 does not have, so it was run from the work folder against the runtime before finding 8's repair, not on
  that commit unmodified. The script is tracked from the next round as `tests/e21_list_leak.py`, and gives 46 and 46
  MiB again (`evidence/e21-lists-rerun.txt`).
- `python -B tests/asan_c.py`: 29/29 programs clean under -fsanitize=address and byte-identical to the reference.
  Its plant, a store that frees before it copies, is caught as heap-use-after-free (`e21-asan.txt`,
  `e21-asan-plant.txt`).
- The self-test's E21 rows: four fixtures identical on all four executions; memory flat; the plant (temporaries
  never released) caught.
