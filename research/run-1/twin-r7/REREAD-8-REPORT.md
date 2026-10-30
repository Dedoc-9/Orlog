<!-- R7 re-read 8, saved by the draft's author, 2026-10-28: the twin's report, delivered as its message (it could not write files). Copied without change. -->

# R7 re-read 8: draft 10, the principle reaches every row of CUT-0 (the twin's report)

This is the same reviewer's eighth re-read under R7. It is review evidence: not a proof and not a ruling. The probe is **UNEXECUTED**, and its outcome is **my own worked consequence**. Nothing here shows that CUT-0 is sound or that the version-1 containment test passes, and neither is reported as shown.

## Summary

Draft 10 states his clarification faithfully. It applies all four OWED fixes as disposed, and the correction to 15.13.4.

There are 3 findings. **None needs his decision**:
- **ROWS-1** is a coherence point. His clarification puts "R2's statement-kind spellings and reach rules" before the pin. Two clauses were not brought into line with it:
  - 15.13.8's closing line still leaves CUT-0's rules for the version-1 kinds "the pin's to state [open: the pin]";
  - 15.15's 15.13.8 row still says "the reach: the pin".
- **ROWS-2** and **CHANGED-1** are drafting points.

## 1. Provenance

**Files opened**, all in `twin-r7-reread8/`:

| file | how read |
|---|---|
| `REREAD-8-BRIEF.md` | whole |
| `DRAFT-10-CHANGES.md` | whole |
| `REREAD-7-DISPOSITION.md` | whole |
| `AR-REREAD-8.md` | whole |
| `RULINGS-AS-RULED.md` | a Grep for its last section's heading, then lines 533–565 |
| `SPEC-15-DRAFT-10.md` | lines 1–70, 250–319 and 455–549, plus one Grep over the whole file for the changed wording |

**Not reopened:**
- `T10-STATEMENTS.md`, unchanged since re-read 6 as the brief says. I rely on my reading of the re-read 7 copy.
- `SPEC.md` and `RUNTIME-SPEC.md`, the same bytes, read in full earlier.
- `RULINGS-AS-RULED.md` lines 1–532, as read before.
- The rest of draft 10, which `DRAFT-10-CHANGES.md` reports as unchanged.

**SOURCE NEEDED:**
- **SN-1.** `CUT-0.md`: what counts as an "input the candidate actually reads", and how the containment test's record is checked against the candidate (ROWS-2).

## 2. His clarification (A_ROWS, 72 clauses)

His words, in part:
- "'Every input the pinned rule reads' applies to every CUT-0 row ...
  - Fix the version-1 `NOT-RUN`/`LOG-OPEN` status encoding that determines which row applies.
  - Resolve R2's statement-kind spellings and reach rules so CUT-0's structural closure is defined across every supported statement kind ...
  - Have the containment-test record enumerate the inputs the candidate actually reads. Check that list against the candidate, rather than constructing it by hand."
- "This brings R2 forward ... P6 retains its own trigger."
- "Record this as a clarification ..., not as a claim that the newly identified encodings or statement-kind rules are already settled."

### 2.1 Faithfulness

All five tagged places are faithful:

| clause | what it states | verdict |
|---|---|---|
| Legend `[ruled: claims]` | "every input the pinned rule reads, in every row of CUT-0, fixed before it" | faithful |
| 15.1.1 | "R2's statement-kind spellings and reach rules are resolved before CUT-0's digest is pinned, so that CUT-0's closure is defined across every supported statement kind" | faithful |
| 15.7.5 | "The version-1 NOT-RUN and LOG-OPEN status encoding, by which CUT-0's rows are chosen, is fixed before CUT-0's digest is pinned", tagged ruled for the timing and open for the encoding | faithful; the tag keeps it unsettled, as he asked |
| 15.13.4 | "Every input the pinned rule reads, in every row of CUT-0, is fixed before the pin"; the stop row's inputs given "in his list"; the other rows' status encoding and R2 named; the record "enumerates the inputs the candidate actually reads, and that list is checked against the candidate, not drawn up by hand" | faithful |
| 15.13.8 | "enumerates the inputs the candidate actually reads, checked against the candidate" | faithful |

15.15's rows on 15.0/15.1 ("R2, before the pin") and on 15.7.5/15.8 ("the NOT-RUN and LOG-OPEN status encoding, before the pin") are faithful. So is the closing line.

### 2.2 Coherence (every clause of A_ROWS)

**15.13.8's closing line, and 15.15's 15.13.8 row (ROWS-1).**
- The closing line still says CUT-0's "rules for the version-1 kinds in the other rows ... are the pin's to state. [open: the pin]". The 15.15 row still says "the reach: the pin".
- Under his clarification, R2's reach rules are resolved *before* the pin, so that the closure is defined for every kind. The pin can record them, but cannot be where they are decided.
- These clauses should say the reach rules are fixed by R2's ruling before the pin and stated in the pinned rule.

**15.13.4's list (ROWS-2).**
- The list reads: the stop row's inputs, "the other rows read ... status encoding", and "CUT-0's closure reads R2's ...". This is the drafter's enumeration of what is known now. Read alone, it can look exhaustive.
- His safeguard is the candidate-checked enumeration in the test's record.
- The clause should say that the checked record, not this list, decides which inputs exist. It should also say what kinds of reads count as inputs: receipt fields, trace events, and statement kinds (SN-1).

**15.7.5's NOT-RUN t sentence (CHANGED-1).**
- "It is finding 8's, resolved before the pin" carries only the tag "[open: finding 8; amended set 'identity and bytes']". The timing comes from his Q2 answer and his answer on the pin's inputs, as the sentence before tags it.

**15.9.**
- "If the cut is in `'R'`, the tick block's and the ports' frames, which its decoding needs, are derived before the pin. [follows: his answer on the pin's inputs]" This is coherent.
- P6 keeps its own trigger. 15.15's 15.9 row agrees.

**15.0 Port, Prefix and Tick block; 15.1.3.**
- Each is tagged R2 or port place, and both are now before the pin. Coherent.
- Sheet R8 (float ports) adds a type but no statement kind or status, so it is not an input of CUT-0.

**15.12.4 and its table.**
- 15.1.1 still requires a table row for every form R2 adds, and R2 is now ruled before the pin. Coherent.
- The PREFIX closure and CUT-0's reach stay "not said to be one".

**Untouched or textual matches only:**
- the legend's other tags;
- 15.0 Input log and Execution;
- 15.2 and its sub-clauses;
- 15.3 `close()` and read-once;
- 15.4;
- 15.5's bullets;
- 15.6;
- 15.7.1;
- 15.7.6;
- 15.8's lines;
- 15.10 `input-chain`;
- 15.11;
- 15.12.1, 15.12.3, 15.12.5 and 15.12.6;
- 15.13.1–3, 15.13.5–7 and 15.13.9–11;
- the 15.15 rows on 15.1.3, 15.2, 15.5/15.6, 15.7.1–3, 15.7.6, 15.10, 15.5/15.7.5 and 15.13.7;
- the status paragraph.

### 2.3 Probe (UNEXECUTED; my worked consequence)

The law:

```
1. Let a be given each tick as an integer.
2. Each tick, do the following.
2.1. Say a.
```

- The log ends `end 1 not-run 2 INPUT-MISSING a`.
- To pick the NOT-RUN/LOG-OPEN row, the pinned rule must parse the tick NOT-RUN's encoding. That encoding is now fixed before the pin.
- So the candidate-checked input list should name it. If the list did not, it would be wrong against the candidate, which is exactly what checking it against the candidate is meant to catch.

## 3. Re-read 7's OWED findings, and the correction

| finding | answered as disposed? |
|---|---|
| INPUTS-1 | **Yes.** 15.9 and its 15.15 row derive the frames before the pin if the cut is in `'R'`, tagged [follows]. |
| INPUTS-3 | **Yes.** His words are quoted in 15.13.4. |
| CHANGED-1 | **Yes.** The record naming the digest is tagged [follows: his answers on Q1, Q2 and the pin's inputs], in both 15.13.4 and 15.13.8. |
| CHANGED-2 | **Yes.** The stop's NOT-RUN t is "finding 8's, resolved before the pin". Its tag is open-only (CHANGED-1 below). |
| 15.13.4's naming | **Yes.** The stop row's inputs are now given "in his list", beside the other rows' inputs and R2. |

T10.0–T10.8 are unchanged. Nothing is proved.

## 4. Findings

| # | class | finding | needs his decision |
|---|---|---|---|
| ROWS-1 | COHERENCE | 15.13.8's closing line ("are the pin's to state [open: the pin]") and 15.15's 15.13.8 row ("the reach: the pin") still leave CUT-0's rules for the version-1 kinds to the pin. His clarification puts R2's reach rules before the pin. State that they are fixed by R2's ruling before the pin and recorded in the pinned rule. | no |
| ROWS-2 | DRAFTING | 15.13.4's list of inputs is the drafter's enumeration and can read as exhaustive. Say that the candidate-checked record governs which inputs exist, and which kinds of reads count (SN-1). | no |
| CHANGED-1 | DRAFTING | 15.7.5's "it is finding 8's, resolved before the pin" carries only an open tag. Add the ruled source of the timing (claims: his answers on Q2 and the pin's inputs). | no |

By his ruling on the re-reads, all three are to be recorded with their re-read before the build.
