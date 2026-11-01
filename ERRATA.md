# Errata

Corrections to the wording of files that are not themselves changed. Each entry says where the words are, what they
say, how to read them, and why the file stays as it is.

## E1 (2026-10-31): "exact rationals" describes Int and Fix, not Float

By the owner's decision of 2026-10-31 (WP4, option (c), of the corrective scope): *"Correct the overbroad
exact-rationals description in an erratum outside the three files. Do not reopen the R6 reference, move hashes,
regenerate outputs, or change `ref_run_paths.py` in this release."*

Three passages describe the numeric reference as exact rational arithmetic throughout. The reference computes Int and
Fix exactly, and Float with the host's binary64 operations. Read each passage as corrected below.

| where | as written | read as |
|---|---|---|
| `SPEC.md`, line 5 | "(exact rationals)" | "(Int and Fix in exact integer and rational arithmetic; Float in the host's binary64 operations, every NaN they produce made canonical)" |
| `RUNTIME-SPEC.md`, line 4 | "(exact rationals, one rounding at the end)" | "(Int and Fix in exact integer and rational arithmetic, rounded once at the end by an explicit rule; Float in the host's binary64 operations, every NaN they produce made canonical)" |
| `src/orlog/numeric_ref.py`, docstring lines 1–4 | "written by definition over exact rationals. … every rule is stated as a mathematical value (Fraction, int) and rounded once, at the end, by an explicit rule." | "Orlog OL-0 numeric semantics, written by definition. Int and Fix rules are stated as mathematical values (int, Fraction) and rounded once, at the end, by an explicit rule; Float rules use the host's binary64 operations (+, −, ×, ÷ and math.sqrt), with every NaN they produce made canonical; conversions between the types are checked exactly with Fraction." |

**What the code does** (read, 2026-10-31):

- **Int:** Python integers, with an overflow check.
- **Fix:** integers and `Fraction`, rounded half to even (`x_mul`, `x_div`, `x_trunc`, `x_round`).
- **Float:** the host's binary64 operations, `a + b`, `a - b`, `a * b`, `a / b` and `math.sqrt`, each passed through
  `f_canon` so that a NaN is made canonical.
- **Conversions:** checked exactly with `Fraction` (`f_from_i`, `x_to_f`, `f_to_x`, `f_as_i`, the decimal forms).

`README.md` and `AGENTS.md` have said so since `2e9805a`. Nothing here changes a behavior, a verdict, a vector or a
claim: the correction narrows the description to what the code does.

**Why the three files are not changed.** Each is cited by its sha256: `SPEC.md` (`27dfff0c…`) and `RUNTIME-SPEC.md`
(`0bd571d6…`) in LAW-FORMAT-0's drafts 3–9 and `research/run-1/twin-r7/MANIFEST.md`; `numeric_ref.py` (`eacac3dd…`) in
drafts 2–9 and other records. `numeric_ref.py`'s sha256 is also recorded in `research/rust-core/r6-reference-5.txt`,
which the reference runner's check (`research/rust-core/ref_run_paths.py`) holds module by module: with only the
docstring changed, that check read 38 of 56 in a throwaway clone (MEASURED, 2026-10-31). Correcting the files
themselves is option (a), kept for a later package authorized on its own.
