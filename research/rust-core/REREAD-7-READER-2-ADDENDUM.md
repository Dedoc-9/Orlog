> **A tokened copy, not the original hand-back** (2026-10-31, his ruling on the ten older reports, by REREAD-9's ASK 9-2 procedure): each spelling of the home folder's path is replaced by a token, `⟦HOME⟧` or `⟦HOME83⟧`; the original is kept outside the repository and named in `kept/TOKENED.txt` by its length and sha256, and `kept_tokens.py restore` gives it back exactly with the prefixes. After this line and the blank line below it, the file is the kept tokened bytes exactly, so its line numbers are the original's plus two.

# REREAD-7, reader 2 of 3: the hash-closure addendum, word for word (2026-10-30)

The owner's fourth condition for REREAD-7: *"Once the final record is installed, verify its exact SHA-256 against
Amendment 6. The re-read is not complete until that check passes."* After the remade record
`research/rust-core/r6-reference-3.txt` was installed and Amendment 6's two placeholders were filled, reader 2 (the
same agent whose report is `REREAD-7-READER-2-REPORT.md`, resumed after the other two readers had finished) was asked
to check: (a) the record's sha256 against the value Amendment 6 states, at both places; (b) its rows against
`r6-reference-2.txt`'s; (c) the scripts its header names, by their sha256 now; (d) that SHEET.md changed only in the
placeholders. Its reply follows, unedited, taken from its own transcript rather than retyped.

---

# Addendum to REREAD-7 reader 2: hash closure

All four checks pass. I ran them read-only, on the owner's host. HEAD is still `2e9805aaa1ceeae0beb443d527680796b66f39c7`, and I wrote nothing in the repository.

## What I ran

- `sha256sum` on `SHEET.md`, `r6-reference-3.txt`, `r6-reference-2.txt`, `ref_run.py`, `gen_r6_reference.py`, `decoder1.py`, `src/orlog/interp.py` and `r6-mutants.txt`.
- `grep -n` for `r6-reference-3` and `R6REF7` in `SHEET.md`, and `sed -n 728,748p` to read the lines that were filled in.
- My script `%TEMP%\reread7-2\closure.py` (`⟦HOME83⟧\AppData\Local\Temp\reread7-2\closure.py`).
- `diff` of the rows and of the headers of `r6-reference-2.txt` and `r6-reference-3.txt` (everything after the 7 header lines, then the 7 header lines).

## Results

**(a) The stated sha256: PASSED.**
- `r6-reference-3.txt` hashes to `bbfcddb589ed272c11d51d69a0254c2ac17f499c9480f914502783f7c8a42f6a`.
- `SHEET.md` (now `26bf1fce…`, as you said) states that value exactly twice: line 733, in the text, and line 747, in the files table.
- No `<R6REF7_*>` placeholder is left.

**(b) The rows: PASSED.**
- Both files have 10,000 rows, equal and in the same order.
- Everything after the 7 header lines is byte-identical. `diff` prints nothing for the rows.

**(c) The header: PASSED.**
- It names `gen_r6_reference.py` by `eda219736b136c405afa184969899cf8dfe3be192e31829a5eb2195a53985da1` and `ref_run.py` by `162d4ec776f0c02d1fdc32ff8b6cbc0a65b039511fa51d4997125a37329a0d16`, both equal to the files now.
- It also names decoder1 (`3584f565…`), `interp.py` (`f8432918…`) and the mutants (`a8f704fb…`), each equal to its file.
- Its first line now reads "SHEET.md Amendments 4 to 6 … rulings F2, N3 and U2".
- Only header lines 1 to 3 differ from `r6-reference-2.txt`'s.

**(d) The sheet changed only in the placeholders: PASSED.**
- I put the filled text back by hand: the sha256, in both places, became `<R6REF7_SHA>`, and the note became `<R6REF7_NOTE>`. The note is 390 characters over 4 lines, from "Its rows are those of Amendment 5's record" to "byte for byte equal to the first."
- The result hashes to `4d2dca8c11b3577eb8d236bb26af691091532d2acb7ca57569ce4822952faafb`, the version I read. It has 777 lines, against 780 now.
- So nothing else in `SHEET.md` changed.

## Remarks

- **The new note's claims.** I confirm one of them myself: "Its rows are those of Amendment 5's record, every one". The rest I can only call DECLARED:
  - the wall times (1,673 s and 1,752 s);
  - the second generation ending at 17:40 with `WinError 1450` and writing nothing;
  - the remade generation being byte-equal to the first.
- **X5.** Mutant 09729's row survived both generations, one of them made beside the three readers. That is consistent with X5, and it does not remove X5: the margin to the 60-second limit stays as I measured it.
- **X8.** The note records the process-creation failure as narrative only, not as an interruption under the sheet's rule. That is the gap X8 names.

HASH CLOSURE: PASSED
