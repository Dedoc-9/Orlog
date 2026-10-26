# The Rust runtime of ØRLǪG OL-0 (rt_rs)

Written 2026-10-25 against `RUNTIME-SPEC.md` (DECLARED 2026-10-25) and `src/orlog/numeric_ref.py`. Nothing under
`rt_c/` was read. `vectors/runtime-vectors.txt` and `numeric_ref.py` were not edited (their sha256 after the work:
`841240b7…f204`, the spec's value, and `dd831475…5f47`).

*Note (the maintainer, 2026-10-25, prosecutor F38 and F20):* the tracked `numeric_ref.py` hashes `eacac3dd…`,
unchanged since commit 83eb044; the `dd831475…` above was the file in the scratch folder at the time of writing, and
nothing records what differed. The vectors regenerate from the tracked file byte-identically (sha256 `841240b7…`).
The vector runs are recorded in `evidence/rt_rs-vectors-O.txt` and `evidence/rt_rs-vectors-O0.txt` (20015 / 20015
both ways, byte-identical, no warning).

## What is here

| file | what |
|---|---|
| `orlog_rt.rs` | the runtime: one file, std only, no `unsafe`, no `mod`, no `main`, no top-level `use` |
| `test_rt.rs` | the harness of spec §9: `include!("orlog_rt.rs")`, every vector line, the event-chain check, extra checks |
| `smoke.rs` | a program shaped like a generated one; modes `complete`, `chain`, `refute` |
| `check_smoke.py` | an independent check of smoke's output, trace and receipt (encodings from the spec, values from numeric_ref, hashes from hashlib) |
| `gen_extra_vectors.py` | about 192,000 extra differential lines from numeric_ref in the official format (not the contract) |
| `mutants.py` | plants six defects in copies of the runtime and requires the harness to fail on each |
| `nan_fold_witness.rs` | the witness for finding F1 below |

## Results (run here, 2026-10-25: Windows 11, rustc 1.96.1 x86_64-pc-windows-gnu, Python 3.14.5)

- `rustc --edition 2021 -O test_rt.rs -o test_rt.exe` and the same without `-O`: no warning, no output. The same for
  `smoke.rs` both ways, and for the runtime pasted (concatenated, not included) above a minimal generated `main`
  that carries its own `use std::io::Write;`, both ways.
- `test_rt.exe ..\vectors\runtime-vectors.txt`: `RUNTIME VECTORS 20015 / 20015`, with `-O` and without.
- Chain heads, both builds, identical to `python -B src\check_chain.py` by `diff` (after removing the CR that Python's
  redirected stdout writes on Windows):
  `head0 0cc0deef…97ca`, `head1 4accb340…68c4`, `head2 22d273a9…1992`, `head3 bd049436…6ad9`.
- `RUNTIME EXTRA 31 / 31` (lists, limits, claims, list printing: values written by hand in the harness).
- Smoke, both builds: `SMOKE CHECK PASSED` for all three modes; the chain run's receipt holds
  `trace-head bd0494368f0f…6ad9` = head3 through real files and a real `i_add` overflow; the files of the `-O` and
  the plain build are byte-identical; every file LF only.
- Extra vectors: `192448 / 192448` (seed 1) and `192489 / 192489` (seed 2), both builds.
- `mutants.py`: `MUTANTS CAUGHT 6 / 6` (x_mul's tie rule, no NaN canonicalization, fmt_f's 5^13, a method calling the
  wrong pure function, a SHA-256 constant, a truncating i_quot). An earlier seventh plant (i_div testing OVERFLOW
  before INEXACT-DIVISION) was dropped as an equivalent mutant: the only overflowing Int quotient, MIN / -1, is exact.
- Exit status: 0 for completed and refused runs; 2 with a message on stderr for a missing argument, an output or
  trace path whose folder does not exist.

Does not show: any other platform, CPU or rustc version; the safeguard of F1 rests on `black_box`, which Rust
documents as best-effort, so the vectors must be run again on every new toolchain. `check_smoke.py` and the runtime
were written by one author from one reading of the spec: they agree, which shows consistency, not that the reading is
the C author's. The C runtime is the independent witness. *(Note, the maintainer, 2026-10-25, prosecutor F37: a
separate witness, of one model family with this author.)*

## How it is built

- **Shape.** Every refusable operation is a pure `orl_*(...) -> OrlR<T>` (`Err` holds the code) plus a thin `Rt`
  method that refuses on `Err`. Methods that can refuse or that change the run take `&mut self`; the others are
  associated functions (`Rt::f_add`). The harness runs every refusable vector through both paths.
- **Names.** Pasted at the top of a generated file, so: no top-level `use` (a generated `use std::io::Write;` would
  collide), every top-level name begins `Orl`, `orl_` or `ORL_` except `Rt`, and every item carries
  `#[allow(dead_code)]` (rustc 1.96 does not warn about unused `pub` items of a binary but does about private ones;
  the attribute keeps a generated program warning-free whichever parts it uses).
- **No panic in either build.** Every arithmetic step is checked, wrapping or bounded by its comment, and every shift is
  guarded (a debug build panics on overflow and on a shift by the width). Products and quotients use `i128`/`u128`;
  `INT64_MIN % -1` is never evaluated in `i64`. The debug build passing every vector is evidence for this.
- **Conversions** to binary64 are built from integers (`orl_to_f64_bits`: round the magnitude to 53 bits half-even, then
  assemble the bits); no `as` cast decides a rounding. **Float to Int/Fix** decomposes the bits.
- **Exact printing.** A base-10^9 bignum: the mantissa is made odd, then `m·2^e` is `m` times 2^e (chunks of 2^30)
  or `m·5^k / 10^k` (chunks of 5^13); the last fraction digit is then always 5, so nothing is stripped.
- **SHA-256** (FIPS 180-4), streaming; output, chain and receipt use it.
- **Test hook.** `Rt::with_sinks` (private) builds a run over optional files; with `test_unwind` set, `refuse` and
  `finish` emit their event and then panic with the status line instead of writing the receipt and exiting. Only
  the harness sets it; `Rt::init` never does.

## F1. NaN canonicalization must be decided on the bits (MEASURED)

The first build failed 69 `f_sqrt` vectors at `-O` only: negative arguments gave `FFF8000000000000` instead of
`7FF8000000000000`. Both `if a.is_nan() || a < 0.0 { CANON } else { a.sqrt() }` and
`let r = a.sqrt(); if r.is_nan() { CANON } else { r }` compiled to a bare `sqrtsd`. The IR optimizer rewrites
`is_nan(sqrt(a))` as `a < 0`; the IR still held `select(a < 0, 0x7FF8…, sqrt(a))`. The x86 backend then drops that
select, and `sqrtsd` returns x86's default NaN. `nan_fold_witness.rs` reproduces it: cases 1 and 4 print `FFF8…` at `-O`
and `7FF8…` without it. The runtime now canonicalizes in the integer domain on `black_box(x.to_bits())`
(`orl_canon_bits`), used by `f_canon` and by the 'F' encoding; `f_sqrt` is `f_canon(a.sqrt())`.

The spec warns about the C cast's rounding but not about this. The C runtime goes through the same kind of backend
under clang, so the same fold may meet a float-level guard there. Suggested spec text: *decide canonicalization on the
bits (memcpy / to_bits), never by selecting a NaN constant at the float level; check it at the release optimization
level.*

## Decisions the spec left open (each a place where two runtimes could part)

1. **'F' inside lists.** Spec §5 gives Float's value encoding as the canonical bits; for 'L' elements it says only
   "8 bytes each for I/X/F". I canonicalize F elements of 'L', and the F values of 'E' and 'P', too. This matters
   only for a slot holding a non-canonical NaN, which `f_max`/`f_min` and `bits_f` can make (F2).
2. A B slot other than 0/1 encodes as 1 and prints `true`. An unknown list tag prints as Int and encodes 8 bytes.
3. `say` leaves the builder as it was; `s_take` copies and does not clear. Before any `s_reset`, TEXT-TOO-LONG names
   clause 0. `s_list` checks the 2^24 limit piece by piece, which refuses exactly when the whole append would and
   never builds past the limit in memory.
4. Limits: TEXT-TOO-LONG when the builder would pass 2^24 bytes (2^24 itself is allowed); OUTPUT-TOO-LONG when the
   output plus the line would pass 2^30; LIST-TOO-LONG for `l_new(n)` with n > 2^24 and for a push at length 2^24.
   Event payload lengths are u32, which holds only while lists and texts keep those limits. A slice handed to
   `ev_assign_l` is not checked.
5. Claims: `result` is `bool` in Rust (C has `int`). An id outside the declared claims still emits 'C' but
   accumulates nothing and does not refuse. Counters and costs wrap mod 2^64 (C's `uint64_t`). A claim never evaluated
   reports `ref-clause 0 ref-cost 0`. Accumulation happens before CLAIM-REFUTED, so the receipt counts the failed
   evaluation.
6. Rust signatures the spec does not spell out: `ev_item(c, var, index: u64, tag: u8, slot: i64)`,
   `ev_push(c, var, tag, slot)`, `ev_pop(c, var, newlen: u64)`, `claim(id, c, result, cost: u64, ref_clause: u32,
   ref_cost: u64)`, `must(id, c, result)`. `l_get`/`l_set` take slices. `l_pop` returns nothing, as C's `void`.
7. Files: all three are created by `init`, in the order output, receipt, trace (the trace only with argv[3]); extra
   arguments are ignored. Exit 2 also for fewer than two paths, a seal that is not 64 hex digits (either case,
   printed lowercase), and a failed write or flush. The spec names only "a file cannot be opened". When a later file
   fails, the earlier ones are left created and empty.
8. Arguments are read with `std::env::args_os()`. The spec says `args()`, which panics on a path that is not UTF-8.
9. In Rust, nested refusable calls must go through temporaries (`let t = rt.x_from_i(1, c); rt.x_div(t, d, c)`):
   `rt.x_div(rt.x_from_i(1, c), …)` borrows `rt` mutably twice. This is a constraint on the code generator. It also
   makes the evaluation order explicit.

## Findings about the spec and numeric_ref

- **F2. f_max/f_min pass a NaN through uncanonicalized.** numeric_ref's module text says every NaN result is replaced
  by the canonical NaN. Its `f_max`/`f_min` (`a if a > b else b`) do not do that, and the spec's table agrees with the
  functions. The vectors pin it: 26 `f_max` and 26 `f_min` lines return `FFF8000000000000`. The NaN is then visible
  through `f_bits`, and through list encodings unless decision 1 is shared. The rule itself is not ambiguous; only the
  docstring contradicts it.
- **F3. Table gaps.** The spec's vector-op column is empty for `x_trunc`, `x_round`, `x_max`, `x_min`, `f_trunc` and
  `f_round`, yet the vectors hold 50, 50, 40, 40, 161 and 161 lines of them. `f_lt`/`f_eq` have 1,076 lines each and
  no runtime function: the harness tests them as the native `<` and `==` a generated program writes. `fmt_b` has no
  vector. The table does not name the refusals of `i_quot`/`i_rem` (DIVISION-BY-ZERO, and OVERFLOW for `i_quot(MIN,
  -1)`); numeric_ref does.
- **Suspected vector errors: none.** Every line passes as written.

## Commands (from `rt_rs`, Git Bash; PowerShell takes the same with `.\` before an exe)

```
rustc --edition 2021 -O test_rt.rs -o test_rt.exe
rustc --edition 2021 test_rt.rs -o test_rt_debug.exe
./test_rt.exe ../vectors/runtime-vectors.txt
./test_rt_debug.exe ../vectors/runtime-vectors.txt
(cd .. && python -B src/check_chain.py)          # compare the head lines

rustc --edition 2021 -O smoke.rs -o smoke.exe
mkdir -p build/run_O
for m in complete chain refute; do ./smoke.exe build/run_O/$m.out build/run_O/$m.receipt build/run_O/$m.trace $m; done
python -B check_smoke.py build/run_O             # SMOKE CHECK PASSED

python -B gen_extra_vectors.py build/extra-vectors-1.txt 1 && ./test_rt.exe build/extra-vectors-1.txt
python -B mutants.py                             # MUTANTS CAUGHT 6 / 6 (about a minute)
rustc --edition 2021 -O nan_fold_witness.rs -o build/nan_fold_witness.exe && ./build/nan_fold_witness.exe -2
```

Set `PYTHONHASHSEED=0` for the Python steps (they were run with it).
