# R7's tenth re-read: the brief to the twin (2026-10-29)

Since your ninth re-read, the owner has adopted its dispositions and answered its five questions (`RULINGS-AS-RULED.md`,
its last section):
- S15.5-1: T1's example corrected; the fixed number 3 is `580000000300000000`.
- S15.3-1: each read-once `'N'` is emitted at its own declaration as execution reaches it, never grouped.
- S15.1-1: with no budget the law line omits its budget part (R5's form); no budget of zero is encoded.
- S15.5-2: a law with read-once ports and no tick block has no tick records; a `t` line is LOG-RECORD.
- S15.9-1: draft 2 is the candidate byte grammar to test, not an adopted or frozen format; the version-1 reference tests
  S1 to S7 against it during the containment step, before the pin.

Draft 12 applies them, with your seven drafting fixes and the open items he kept open.

**This re-read is of the whole draft again.** His words: *"I recommend another whole-draft re-read because Draft 12
changes settled semantics and the byte grammar, not merely editorial wording."* Read every clause of
`SPEC-15-DRAFT-12.md`, title to last line.

## Your reading set

These files, in this folder. Open nothing else, and list every file you open, saying which you read whole.

- `SPEC-15-DRAFT-12.md`: the draft. Read it whole.
- `RULINGS-AS-RULED.md`: its last section holds his answers to your ninth re-read; the section before it, every ruling
  since your eighth.
- `AR-REREAD-10.md`: the answers' affected clauses, computed over draft 11. It does not bound this re-read.
- `DRAFT-12-CHANGES.md`: what draft 12 changed, and why.
- `REREAD-9-DISPOSITION.md`: your ninth re-read's findings, as proposed and then adopted.
- `CUT-SCHEMA.md`: the cut's bytes, draft 2, with its S6 row's dated note and its section on version-0 stand-ins.
- `T10-STATEMENTS.md`: T10.0 to T10.8, unchanged since your sixth re-read.
- `SPEC.md` and `RUNTIME-SPEC.md`, the same bytes as before.

## What to report

- **Faithfulness**, for every clause tagged with a ruling: whether it states the ruling as given, or adds to it,
  narrows it or alters it. Quoted words must be his.
- **Coherence**, for every clause of the draft, with the others, with SPEC §1-§14, RUNTIME-SPEC and CUT-SCHEMA.
- For each of your ninth re-read's findings, whether draft 12 answers it as its adopted disposition records.
- **The probe's grade:** wherever the draft cites the S1-S7 probe, whether it keeps "MEASURED on version-0 stand-ins
  only", and whether draft 2 is anywhere presented as adopted or frozen.

A clean report would show neither that CUT-0 is sound nor that the containment test passes; do not report either as
shown. Mark every probe unexecuted, and every fixture's outcome as your own worked consequence.

Number the findings by section (S15.0-1, …). Give each a class (DRAFTING, GAP, COHERENCE, QUESTION), and say whether
it needs his decision. Name any further source you need, without opening it.

Deliver the report as text in your reply.
