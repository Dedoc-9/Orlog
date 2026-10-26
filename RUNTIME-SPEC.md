# ØRLǪG OL-0 runtime contract (C99 and Rust)

Status: DECLARED, 2026-10-25. This is the contract every backend runtime implements. The numeric meaning of
every function is defined by `src/orlog/numeric_ref.py` (exact rationals, one rounding at the end); a runtime
implements the same rule with integer and IEEE operations and is held to it by `vectors/runtime-vectors.txt`
(20,015 lines, sha256 `841240b72cb580414483d217928b2794e033eb3745fd99b13946de1ef107f204`). Where this text and
`numeric_ref.py` disagree, `numeric_ref.py` is the definition and the disagreement is a finding to report.

The runtime never decides anything about operation counting, evaluation order or which events happen: the
generated code does. The runtime supplies checked arithmetic, exact printing, the event hash chain, the
output file, the receipt and refusals.

## 1. Hard constraints

- **C:** one header `orlog_rt.h`, every function `static`, ISO C99 only. It must compile warning-free with
  `clang -std=c99 -pedantic -Wall -Wextra -O2 -ffp-contract=off -fno-fast-math`. No compiler extensions:
  no `__int128`, no `__builtin_*`, no `#pragma` other than `STDC FP_CONTRACT OFF`. Only the standard library
  (`stdint.h stdio.h stdlib.h string.h math.h float.h limits.h`). Include `<float.h>` first, then
  `#if FLT_EVAL_METHOD != 0` → `#error` (before `<float.h>` the macro is undefined and the test passes vacuously),
  and `#pragma STDC FP_CONTRACT OFF`. 128-bit products and quotients are
  built from `uint64_t` halves. Signed overflow must never occur (it is undefined in C): test before you add.
  `INT64_MIN % -1` and `INT64_MIN / -1` are undefined in C: never evaluate them.
- **Rust:** one file `orlog_rt.rs`, standard library only, no crates, no `unsafe`. It must compile warning-free
  with `rustc --edition 2021 -O`. It is pasted at the top of a generated program (`mod rt { ... }` is NOT used:
  the generated `main` follows in the same file), so it must not define `main`. `i128`/`u128` are allowed.
- **Both:** files opened in binary mode; output and receipt written with LF only; no locale, no clock, no
  environment variable read, no randomness. Exit status 0 for a completed or refused run. Otherwise, with a message
  on stderr: 2 when a file cannot be opened or written (both runtimes), and in Rust also for wrong usage or a seal
  argument that is not 64 hex digits; 3 in C for a misuse of the runtime by the generated code or an allocation that
  fails. None of these is a refusal of the contract, and none writes a receipt that claims one. (Amended 2026-10-25
  to what both runtimes do: prosecutor F29.)

## 2. Numeric functions

Names are given in C (`orl_` prefix); the Rust names drop the prefix and are methods of `Rt` when they can
refuse (they take `&mut self`), associated functions when they cannot. `c` is the clause id (`uint32_t` / `u32`)
passed to `refuse`. A refusal code is one of: `OVERFLOW DIVISION-BY-ZERO INEXACT-DIVISION NEGATIVE-SQRT
INEXACT-CONVERSION NOT-FINITE INDEX-OUT-OF-RANGE EMPTY-LIST NEGATIVE-LENGTH LIST-TOO-LONG TEXT-TOO-LONG
OUTPUT-TOO-LONG` (and the generated code's own `CLAIM-REFUTED MUST-FAILED FUEL-EXHAUSTED RULE-CONFLICT
RULE-UNDEFINED`).

| C | Rust | vector op | meaning (numeric_ref) |
|---|---|---|---|
| `int64_t orl_i_add(a,b,c)` / `_sub` / `_mul` | `rt.i_add(a,b,c)` … | `i_add` … | checked; `OVERFLOW` |
| `orl_i_neg(a,c)`, `orl_i_abs(a,c)` | `rt.i_neg(a,c)`, `rt.i_abs(a,c)` | `i_neg`, `i_abs` | checked |
| `orl_i_div(a,b,c)` | `rt.i_div` | `i_div` | exact quotient: `DIVISION-BY-ZERO`, then `INEXACT-DIVISION`, then `OVERFLOW` |
| `orl_i_quot(a,b,c)`, `orl_i_rem(a,b,c)` | `rt.i_quot`, `rt.i_rem` | `i_quot`, `i_rem` | Euclidean: a = b·q + r, 0 ≤ r < |b| |
| `orl_i_isqrt(a,c)` | `rt.i_isqrt` | `i_isqrt` | floor square root; `NEGATIVE-SQRT` |
| `orl_i_max(a,b)`, `orl_i_min(a,b)` | `Rt::i_max`, `Rt::i_min` | `i_max`, `i_min` | `a > b ? a : b`, `a < b ? a : b` |
| `orl_x_from_i(n,c)` | `rt.x_from_i` | `x_from_i` | raw = n·2³², checked |
| `orl_x_add/_sub(a,b,c)`, `orl_x_neg/_abs(a,c)` | | `x_add` … | checked |
| `orl_x_mul(a,b,c)` | | `x_mul` | round-half-even(a·b / 2³²), checked |
| `orl_x_div(a,b,c)` | | `x_div` | `DIVISION-BY-ZERO`; round-half-even(a·2³² / b), checked |
| `orl_x_sqrt(a,c)` | | `x_sqrt` | isqrt(a·2³²); `NEGATIVE-SQRT` |
| `orl_x_trunc(a)`, `orl_x_round(a)` | `Rt::x_trunc`, `Rt::x_round` | | to Int: toward zero; half-even |
| `orl_x_max/_min(a,b)` | `Rt::x_max/_min` | | as Int |
| `double orl_x_to_f(a, rounded, c)` | `rt.x_to_f(a, rounded: bool, c)` | `x_to_f a b:r` | exact or `INEXACT-CONVERSION`; rounded = nearest-even |
| `int64_t orl_f_to_x(x, rounded, c)` | `rt.f_to_x` | `f_to_x` | `NOT-FINITE`; x·2³² exact or `INEXACT-CONVERSION` (rounded: half-even); `OVERFLOW` |
| `double orl_f_canon(x)` | `Rt::f_canon` | | any NaN → bits `0x7FF8000000000000` |
| `orl_f_add/_sub/_mul/_div(a,b)` | `Rt::f_add` … | `f_add` … | native IEEE op, then canon (division by ±0 is IEEE: ±inf or NaN) |
| `orl_f_neg(a)`, `orl_f_abs(a)`, `orl_f_sqrt(a)` | | `f_neg` … | native, then canon; sqrt of negative → NaN |
| `orl_f_max/_min(a,b)` | | `f_max`, `f_min` | `a > b ? a : b`, `a < b ? a : b` (NOT `fmax`) |
| `double orl_f_from_i(n, rounded, c)` | `rt.f_from_i` | `f_from_i` | exact or `INEXACT-CONVERSION`; rounded = nearest-even |
| `int64_t orl_f_trunc(x,c)`, `orl_f_round(x,c)` | `rt.f_trunc`, `rt.f_round` | | `NOT-FINITE`, `OVERFLOW`; toward zero / half-even |
| `int64_t orl_f_bits(x)`, `double orl_bits_f(i)` | `Rt::f_bits`, `Rt::bits_f` | | bit casts (memcpy / to_bits) |

Amendments of 2026-10-25, from the runtimes' authors (the vectors are unchanged):
- **Decide NaN on the bits.** With optimization, LLVM may fold a floating-point test such as `is_nan(x) ? CANON : x`
  or `a < 0 ? NaN : sqrt(a)` into the bare operation. This is legal for LLVM, because it treats the NaN bits an
  operation produces as unspecified. The result then carries the hardware's default NaN (`0xFFF8…` on x86-64).
  - Both runtimes therefore test NaN with integer operations on the bit pattern.
  - The C runtime tests through `memcpy`; the Rust runtime through `black_box`.
  - This is a hazard managed, not removed. A future optimizer could fold the bit test too. The arbiter's trace
    comparison would then catch the difference; nothing prevents it.
- **Every Float slot in every payload is canonical**: in `'A'`, `'E'`, `'P'` and inside `'L'`. Values inside a
  program are canonical already, so this only matters for runtime functions called directly.
- **Table gaps.**
  - `x_trunc`, `x_round`, `x_max`, `x_min`, `f_trunc` and `f_round` have vectors under those op names.
  - `f_lt` and `f_eq` are the native comparisons.
  - `i_quot` and `i_rem` refuse `DIVISION-BY-ZERO`; `i_quot` also refuses `OVERFLOW`.

Notes the vectors enforce:
- Conversions int→double and fix→double must NOT rely on the C cast's implementation-defined rounding:
  compute the exactness test and the rounded value with integer operations, then build the double exactly
  (for example `ldexp` of an integer of at most 53 bits, which is exact).
- `f_lt`, `f_eq` vectors are the native IEEE comparisons (`<`, `==`); NaN compares false.
- Vectors give doubles by their bits; arguments may be signalling NaNs or NaNs with payloads.

## 3. Printing (exact decimals; `fmt_i`, `fmt_x`, `fmt_f` vectors)

- Int: decimal, `-` for negatives (handle INT64_MIN).
- Fix: sign, the integer part of |raw|/2³², then `.` and every fraction digit until the remainder is zero
  (at most 32), or `.0` when the fraction is zero. Computed exactly: `frac*10` fits in 64 bits.
- Float: `NaN`, `Infinity`, `-Infinity`; otherwise sign (from the sign bit, so `-0.0`), then the EXACT decimal
  value of the binary64 with the same rule as Fix (`.0` when integral; every digit, trailing zeros removed).
  The smallest subnormal prints 1074 fraction digits. Use a small bignum (base 10⁹ limbs in `uint32_t`):
  for value m·2^e with e ≥ 0 multiply by 2 e times; for e < 0 compute m·5^(−e) and place the point (−e)
  digits from the right. Both runtimes must reproduce every `fmt_f` vector byte for byte.
- Bool: `true` / `false`. List: `[` elements printed by their type, separated by `, `, `]`.

## 4. Text builder, output, Say

One builder per runtime. `orl_s_reset()`, `orl_s_lit(p, n)` (raw UTF-8 bytes), `orl_s_i(v)`, `orl_s_x(raw)`,
`orl_s_f(x)`, `orl_s_b(v)`, `orl_s_t(orl_text)`, `orl_s_list(tag, const int64_t *slots, uint64_t n)` (tag `I X F B`;
floats stored as their bits). Each append refuses `TEXT-TOO-LONG` (clause = the clause given to the last
`orl_s_reset(c)`, so `orl_s_reset` takes `c`) if the builder would exceed 2²⁴ bytes. `orl_text orl_s_take(void)`
returns a heap copy owned by the temp stack (§4a). Rust: `rt.s_reset(c)`, `rt.s_lit(&[u8])`, `rt.s_i(i64)`,
`rt.s_x(i64)`, `rt.s_f(f64)`, `rt.s_b(bool)`, `rt.s_t(&[u8])`, `rt.s_list(tag: u8, &[i64])`, `rt.s_take() -> Vec<u8>`.

`orl_say(c)`: the line is the builder's bytes plus one LF (0x0A). Refuse `OUTPUT-TOO-LONG` if total output would
exceed 2³⁰ bytes. Write the line to the output file, add it to the running SHA-256 of all output, then emit event
`'S'` with the line as payload.

C type: `typedef struct { const uint8_t *p; uint32_t n; } orl_text;` with `orl_text orl_t_lit(const char *p,
uint32_t n)` (wraps, no copy) and `int orl_t_eq(orl_text a, orl_text b)` (byte equality).

## 4a. Ownership (C; red team E21 and rt_c finding 8, added 2026-10-25)

Before E21's repair, a text made by `followed by` and every list made or copied stayed on the heap until the run
ended. Now every heap text and list the C runtime makes has exactly one owner, a variable's slot or the temp stack:
- **The temp stack.** `size_t orl_tmp_mark(void)` and `void orl_tmp_release(size_t mark)`. `orl_s_take`, `orl_l_new`
  and `orl_l_from` (and so `orl_l_copy`) push what they make onto it. The generated code takes a mark before each
  clause statement and each While iteration, and releases back to it after.
- **A text variable** owns one buffer, its slot: `typedef struct { uint8_t *p; uint32_t cap; } orl_tslot;` and
  `void orl_t_store(orl_text *var, orl_tslot *slot, orl_text v)`. A store copies the value into the slot, reusing the
  buffer while the value fits, and frees the old buffer only after the copy, so storing a variable's own text is safe.
- **A list variable** owns its buffer: `void orl_l_store(orl_list *var, orl_list t)` copies the items in. A list read
  from a variable is always a copy, so the source is never the destination's buffer.
- **Slots are static**, one per variable id. That is sound because the language refuses recursion, so each variable
  has at most one live instance, and lists hold only numbers and truth values.
- **The bound.** Live heap text is at most (text variables + the text temporaries along one chain of active statements
  + the builder) × 2²⁴ bytes, and live list memory at most (list variables + the list temporaries along that chain) ×
  2²⁴ × 8 bytes, however long the run. DECLARED in general; measured on two programs (`evidence/e21-*.txt`).
- **Rule.** Never let a store free before it copies, and never add a maker of heap texts or lists that does not push
  onto the temp stack. None of this is visible in an output or a receipt.

Rust and Python own their values by scope (`Vec<u8>`, `Vec<i64>`, Python objects); the generated mark and release
are no-ops there.

## 5. The event hash chain

`head0 = SHA-256("orlog-trace-0" (13 ASCII bytes) || law_seal (32 raw bytes))`. Each event:
`head = SHA-256(head (32) || kind (1 byte) || clause (u32 big-endian) || len (u32 big-endian) || payload)`,
then `events += 1`. If a trace path was given, append the line
`<events> <kind as ASCII char> <clause> <payload as lowercase hex, or - if empty> <head lowercase hex>\n`.

Value encodings (all integers big-endian): Int `'I'` + 8 bytes two's complement; Fix `'X'` + 8 bytes raw;
Float `'F'` + 8 bytes of the canonical bits; Bool `'B'` + 1 byte (0/1); Text `'T'` + u32 length + bytes;
List `'L'` + element tag + u32 count + elements (8 bytes each for I/X/F, 1 byte each for B).

| kind | function (C) | payload |
|---|---|---|
| `'A'` | `orl_ev_assign_i/_x/_f/_b(c, var, v)`, `orl_ev_assign_t(c, var, orl_text)`, `orl_ev_assign_l(c, var, tag, slots, n)` | u32 var + value encoding |
| `'E'` | `orl_ev_item(c, var, uint64_t index, tag, int64_t slot)` | u32 var + u64 index + value encoding of the slot under tag |
| `'P'` | `orl_ev_push(c, var, tag, slot)` | u32 var + value encoding |
| `'Q'` | `orl_ev_pop(c, var, uint64_t newlen)` | u32 var + u64 newlen |
| `'S'` | (inside `orl_say`) | the line bytes incl. LF |
| `'C'` | (inside `orl_claim`) | u32 claim id + 1 byte result |
| `'M'` | (inside `orl_must`) | u32 must id + 1 byte result |
| `'R'` | (inside `orl_refuse`) | the ASCII code |

Rust: `rt.ev_assign_i(c, var, v)` and so on; lists as `&[i64]`.

## 6. Claims, musts, refusal, finish, init

- `orl_init(int argc, char **argv, const char *backend, const char *law_hex, const char *text_hex,
  uint32_t n_claims, const uint32_t *claim_clause)`: argv[1] output path, argv[2] receipt path, optional argv[3]
  trace path. Rust: `Rt::init(backend: &str, law_hex: &str, text_hex: &str, claim_clause: &[u32]) -> Rt`
  (reads `std::env::args_os()`).
- `orl_claim(id, c, int result, uint64_t cost, uint32_t ref_clause, uint64_t ref_cost)`: emit `'C'`; accumulate per
  claim id (ids are 0-based): evaluations += 1, trues += result, cost += cost, and store ref_clause and ref_cost
  (latest). If result is 0, `orl_refuse("CLAIM-REFUTED", c)`.
- `orl_must(id, c, result)`: emit `'M'`; if result is 0, `orl_refuse("MUST-FAILED", c)`.
- `orl_refuse(code, c)` (never returns): emit `'R'` with the code, write the receipt with
  `status REFUSED <code> <c>`, flush and close the files, `exit(0)`. Rust: `rt.refuse(code, c) -> !`.
- `orl_finish()` (never returns): receipt with `status COMPLETED`, close, `exit(0)`.
- Ops: a plain public counter `uint64_t orl_ops` (Rust `rt.ops: u64`) that only the generated code changes.

## 7. The receipt (byte-identical across backends except the `backend` line)

```
orlog-receipt 0
backend <name>
law-seal <64 lowercase hex>
text-seal <64 lowercase hex>
status COMPLETED                  (or: status REFUSED <CODE> <clause>)
output-bytes <decimal>
output-sha256 <64 lowercase hex>
events <decimal>
trace-head <64 lowercase hex>
ops <decimal>
claims <n_claims>
claim <id> <clause> <evaluations> <trues> <cost> <ref-clause> <ref-cost>     (one line per declared claim, id order)
end
```

## 8. Lists (slots are `int64_t`; floats as bits; bools as 0/1)

C: `typedef struct { int64_t *v; uint64_t len, cap; } orl_list;` `orl_list orl_l_new(int64_t n, int64_t fill, c)`
(`NEGATIVE-LENGTH`, `LIST-TOO-LONG` above 2²⁴), `orl_list orl_l_from(uint64_t n, const int64_t *slots)`,
`orl_list orl_l_copy(const orl_list *)`, `int64_t orl_l_get(const orl_list *, int64_t k, c)` (1-based;
`INDEX-OUT-OF-RANGE`), `void orl_l_set(orl_list *, int64_t k, int64_t v, c)`, `void orl_l_push(orl_list *, int64_t v,
c)` (`LIST-TOO-LONG`), `void orl_l_pop(orl_list *, c)` (`EMPTY-LIST`), `int64_t orl_l_len(const orl_list *)`.
Rust: `Vec<i64>` with `rt.l_new(n, fill, c)`, `rt.l_get(&v, k, c)`, `rt.l_set(&mut v, k, x, c)`, `rt.l_push(&mut v,
x, c)`, `rt.l_pop(&mut v, c)`; length via `v.len() as i64`.

## 9. Required tests (each runtime ships them)

A harness (`test_rt.c` / `test_rt.rs`) that reads `vectors/runtime-vectors.txt`, runs every line through the
runtime (a refusal is observed by the harness, e.g. by a test hook that records the code instead of exiting), and
prints `RUNTIME VECTORS <passed> / <total>` and every failing line. Pass means 20015 / 20015. Plus an event-chain
check: law seal = SHA-256("law"); events `'S'` clause 1 payload `hello\n`, `'A'` clause 2 payload var 0 + Int 42,
`'R'` clause 3 payload `OVERFLOW`; print head0 and the head after each event, four heads in all. The reference values
are produced by `src/check_chain.py`.
