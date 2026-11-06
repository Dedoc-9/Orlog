# Audit: `probe-spellings.txt`, the bytes committed and the bytes captured (2026-10-31)

A record of a discrepancy, by the owner's decision of 2026-10-31 (WP3.1 of the corrective scope): *"create the
historical audit record for `probe-spellings.txt`, with both sizes, hashes, evidence, and limits. Neither hash is to be
described as the original."* It corrects nothing and replaces nothing.

## What the file is

`research/run-1/probe-spellings.txt` is the output of `research/run-1/probe_spellings.py`, a measurement for RUN-1's
rulings: what version 0 does with each candidate spelling of the new forms, and whether any line of COMPAT-0's frozen
texts would be captured by one. `research/run-1/RULINGS.md` (line 45) names it as that probe's output. The probe writes
with `print` (its lines 73–92), so the file was made by redirecting its standard output.

## The discrepancy (MEASURED, 2026-10-31)

| | bytes | CR bytes | sha256 |
|---|---|---|---|
| the committed blob, `c797af4` (2026-10-26 04:14:55 −0700) | 2,735 | 0 | `8ddef62dcdba4b6b741eecc9cedebb019444bfc75d1e17ae8563cec82fbfa640` |
| the working copy on the host where it was made | 2,758 | 23 | `5d834ed405ac8f5c377d2b5b38da8ca71ae537740e1780a03c2339f50030cb45` |

The two differ only in line ends: the working copy ends each of its 23 lines with CR LF, and the blob is the same text
with LF. The file was committed under `.gitattributes`' rule `* text=auto eol=lf`, which stores a text file's CR LF as
LF; no exact-path `-text` rule covered it. No record made before this one states either sha256.

## The evidence, and what it does not show

- **The generator's output today** (MEASURED, 2026-10-31, on the same host): `probe_spellings.py`, run with its
  standard output read as bytes, prints exactly the working copy's 2,758 bytes (sha256 `5d834ed4…`); the committed
  blob is that output with CR LF made LF. This shows where the working copy's bytes come from today. It does not show
  that those were the bytes first captured, nor which bytes were offered to the commit.
- **The working copy's modification time** (OBSERVED): 2026-10-26 04:12:02 −0700, under three minutes before the
  commit. A time stamp can be carried over by a copy, so it identifies nothing by itself, and it does not close the
  gap above.
- **The line ends of a redirected stdout on Windows** are CR LF (`AGENTS.md` §5); the generator's present output is
  consistent with that, and with nothing more.

The discrepancy is established. Which bytes were originally captured is not established, and neither sha256 above is
the original capture's seal.

## Disposition

- The commit `c797af4` and its blob stay as they are: no history is rewritten, and no replacement blob is committed.
- The working copy is not committed, and is not designated the original. Any later version of this file committed
  with its CR bytes (under a `-text` rule) would be a separate decision of the owner, made on evidence he accepts, and
  would be labelled with that provenance.
- The rule that would have kept such bytes, and the order of its checks, is the byte-sensitive evidence paragraph of
  `AGENTS.md` §5 (WP3.2 of the same scope).
