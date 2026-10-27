# The refusal cut's bytes, derived from CUT-0's rule as written (2026-10-26, research only)

The fork (`FORK.md`) records the cut in v1's `'R'` event from 1a on, whichever settlement rule is admitted. The
outside reviews asked for two things before anything freezes:
- the cut's schema derived from CUT-0's decision procedure and tested against the adversarial fixtures;
- no field kept without a demonstrated role.

The latest review proposes a ruling for 1a:
- R8 stays the sole admitted settlement rule;
- CUT-0 runs only as a research setting, with the four-field cut as its candidate evidence;
- the format does not freeze until four conditions hold.

This record answers those four conditions. The reviews are paraphrased, never quoted. Nothing here is ruled or
built, and the format freezes only by the owner's ruling.

The probe is `probes/cut0_schema.py`, and its output is `evidence/run1-cut0-schema.txt`, twice byte-identical. Draft 1,
written earlier the same day, is kept at the end with its own evidence.

## The four conditions, and where each stands

| the review's condition | where | where it stands |
|---|---|---|
| the schema derived from CUT-0's rule as written, not from the implementation | §1 | **done, and it changed the bytes.** Read from `CUT-0.md` §2, the rule reads a For's bit only below the top and an If's arm only on top. Draft 1 carried a top For's bit, in a flag byte on every frame, and accepted flag states no run reaches. Draft 2 drops the flag |
| each field's removal reproducible and tied to a decision change | §3 | **done.** Four witnesses, each a named claim of a named case whose standing flips, printed with both payloads and both K̂ |
| the decoder refuses malformed and non-canonical bytes and accepts only valid canonical ones | §2, §3 | **done for the form, with a boundary.** Canonical by structure: every field is fixed-width and range-checked, and what a frame carries is fixed by its kind and place. Seven shape rules hold the form to what the interpreter can produce: 0 accepted outside it across 390,498 byte mutations and 2,858 frame forgeries. **A well-formed cut of the program is accepted whether or not the run produced it:** the form cannot tell, and 14 of 15 such single-byte changes would change a standing. What holds a cut to its run is the executions' agreement |
| an explicit compatibility policy for existing receipts and refusal records | §4 | **proposed, from the formats as built.** No version-1 record exists anywhere, so nothing existing changes. The format must freeze, by ruling, before the first v1 receipt is frozen anywhere |

## 1. The derivation, from the rule as written

The rule (`CUT-0.md` §2): *held when every completed evaluation is true, it is not open at the cut, and it is not in
K̂.* That is the proposal's own text, quoted from this repository. Its three inputs:
- **the completed evaluations** come from the receipt's claim lines, not from the cut;
- **the open claim** comes from the cut;
- **K̂** is computed "from the frames outward".

So the cut must carry what K̂ reads, and nothing more. The rule's construct table, row by row:

| the rule's text (`CUT-0.md` §2) | what it reads of the cut | the field |
|---|---|---|
| a sequence: "the next sibling that is not an absorbed Otherwise; at the block's end, the owning frame" | where each frame stands in its block | each frame's **statement**: its clause, and a **selector**, because an inline arm statement runs in its If's frame and two statements can share a clause (F2) |
| `Perform`: "a return only to the frame below, the actual caller" | the frames below the top | the **whole stack**, outermost first |
| `For`: "refused in the body: the body, if passes remain. Refused at its own clause: the body" | the bit, for a For below the top only | a **bit**, only on a For that is not the last frame |
| `While`: "always the body" (reading S2) | nothing | — |
| If chain: "a condition refused (the If on top): that arm onward ... Inside an arm: when it ends, the chain completes" | the refused arm, for the top If only | an **arm**, only on an If that is the last frame |
| `Claim`: "open at the cut: that claim, by its id" | the top statement, when it is a claim | none of its own: a statement holds one claim, so the id is read from the top frame's (clause, selector) |
| a rule use, and statements with no body | nothing | — |
| "Values are unknown and refusals are ignored" | no value, no operation count | — |

**What draft 1 carried that the rule does not read:**
- a top For's bit (flags 1, 2 and 4 on the last frame);
- a flag byte on frames that carry nothing.

Its decoder also accepted flag states no run reaches: flag 4 below the top, and a top If with flag 0.

**The code** is kept because v0's `'R'` event already carries it, and the receipt's status line names it. CUT-0's
decision does not read it. It is the refusal's identity, not a decision field.

**Two witnesses agree on what is read: the rule's text and the probe's `continuation()`** (`probes/cut0_claims.py`,
which reads exactly a frame's statement, a For's bit below the top, and the top If's arm). One author wrote both, so
their agreement shows consistency, not truth (G23). §3's witnesses are what stand against a shared mistake: each drops
one field and shows a decision the rule makes change.

## 2. The bytes, draft 2

```
payload := u8 len(code) || code || u16 nframes || frame*                                   (big-endian)
frame   := u32 clause || u16 sel || [u8 more: a For not last] || [u16 arm: an If that is last]
  sel   = 0xFFFF: the clause's own statement; else k: arm k's inline statement of the If chain the clause heads or
          belongs to (k = the number of conditions for the Otherwise arm)
```

**The decoder holds the form to the shapes the interpreter can produce.** Each violation is refused with its reason:

| rule | what it refuses | read from | version 1 |
|---|---|---|---|
| S1 root | a first frame that is not a top-level clause's own statement | `Interp.run` calls `seq` on the top level (`interp.py` 120) | the tick block is a top-level statement; DECLARED |
| S2 nesting | a frame that is not something the frame before it runs: a loop's child, the performed procedure's child, a block arm's child | `seq`, `body` and `stmt` (`interp.py` 132–147, 213–244) | the tick block's body adds one more parent; DECLARED |
| S3 inline | an arm's inline statement anywhere but directly after its own If | `body` runs an inline statement in place (`interp.py` 143–147) | unchanged |
| S4 top kind | a last frame whose statement cannot refuse at its own clause: in version 0, a Perform | a Perform counts and runs its body, with no refusal of its own (`interp.py` 242–244) | **v0 only.** TICK-BUDGET refuses at any counted operation, a Perform's included (`CONTRACT-DRAFT.md` 4.3) |
| S5 ranges | a bit other than 0 or 1; an arm that names no condition | — | unchanged |
| S6 event | an `'R'` event whose clause is not the last frame's, or for an If not the refused condition's | every refusal names the executing statement's clause, except an If's condition, which names its arm's (`interp.py` 213–216) | **open:** 4.3 refuses TICK-BUDGET "at the clause whose statement is executing", and does not say whether an If's condition operation names the head's clause or the arm's. Version 0's refusals inside a condition name the arm's |
| S7 code | a code raised by one statement kind alone, on a last frame of another kind | CLAIM-REFUTED, MUST-FAILED, FUEL-EXHAUSTED, OUTPUT-TOO-LONG and EMPTY-LIST are each raised once, in one branch (`interp.py` 267, 250, 226, 208, 280; the probe checks each line) | TICK-BUDGET is raised at any kind |

Then:
- the code registry: 17 codes, computed from the source (`interp.py`'s refusals and `numeric_ref.py`'s), equal to
  draft 1's hand list. Version 1 adds TICK-BUDGET;
- the count;
- no trailing bytes;
- `encode(decode(b)) == b`.

**Canonical by structure.** Every field is fixed-width. What a frame carries is decided by its statement's kind and its
place, and every value is range-checked. So no cut has two spellings, and the decoder is injective without the round
trip. Measured: with the round trip removed, no corpus accepts anything more (an equivalent mutant, by that argument).
The round trip stays as a guard.

**The shapes, generated the other way.** The probe walks each program from the top down, the way `Interp.seq`, `body`
and `stmt` call, and lists every cut shape the calls can produce. That list is finite, because version 0 refuses
recursion. The decoder checks parents from the bottom up. The two are written apart, by one author.

## 3. MEASURED

| check | result |
|---|---|
| every refused run decodes to its live cut, on every field the bytes hold, with the same K̂ | **89,035 refused runs, 0 differ:** 85 of the cases, the frozen texts, the fixtures and the examples; 61,879 of family E (exhaustive over its grammar) and 27,071 of family G (seeded) |
| every live cut is a generated shape | in all 89,035 |
| the frames that carry no bit, or an arm, by their place | in family G, 1,285 runs refused at a For's own bounds (a top For, no bit) and 1,943 at an If's condition (a top If, its arm), each decoding to its live cut; 3,776 refused inside an open claim's evaluation. The frozen corpus has no top For |
| the shapes of the 19 case programs | 136 shapes; encode and decode inverse on every one |
| byte mutations of the cases' own payloads, with their code and event clause: every value at every offset, every deletion, duplication, insertion and truncation | 337,936 tried. **15 accepted, all valid shapes and all canonical: 9 positions the run passed through, 6 shapes it never reached. 14 of the 15 decide a claim otherwise than the live cut** |
| byte mutations of all 136 shapes | 52,562 tried: 149 accepted, 0 outside the shapes, 0 non-canonical |
| frame forgeries: every frame deleted, substituted or inserted, from every live cut and every shape, with every bit and arm | 2,858 tried: 136 accepted, **0 outside the shapes** |
| the event's clause: every clause of the program, and one that does not exist, on each frozen run's cut | 389 tried: a wrong clause accepted 0 times, the right one refused 0 times |
| the code: every registered code on each frozen run's cut | 1,445 tried: an incoherent code accepted 0 times, a coherent one refused 0 times |
| size | at most 77 bytes (9 frames) |

**Each field's role, as a witness.** Each row drops one field from the bytes and reads the same refused run:

| field dropped | case | claim | with the field | without it | K̂ with → without |
|---|---|---|---|---|---|
| the frames below the top | C1′ | 0 | withheld | **held** | {0} → {} |
| a For's bit, below the top | C2′ | 0 | held | **withheld** | {} → {0} |
| the selector of an inline statement | A23 | 0, 1 | held, withheld | **withheld, held** | {1} → {0} |
| the top If's refused arm | A09 | 0 | held | **withheld** | {} → {0} |

The evidence prints both payloads of each row, and the command reproduces them. A row counts as a witness only when
the bytes lack the field and a standing flips.

*Repaired later the same day (`SETTLEMENT-DEBATE.md` §3).* The selector's plant first left the selector in the bytes
and had the decoder ignore it, so its two payloads were equal. It now writes only "an inline statement": A23's payload
ends `…0000` in place of `…0001`, and the same two claims swap.

**Each shape rule is needed.** Dropping one lets something through, and each drop is caught by the corpus named:

| rule dropped | caught by |
|---|---|
| S1 root | forgeries (83 accepted outside the shapes); shape mutations (15) |
| S2 nesting | forgeries (1,419); case mutations (35); shape mutations (230) |
| S3 inline | forgeries (21) |
| S4 top kind | forgeries (18); shape mutations (3) |
| S5 ranges | shape mutations (166) |
| S6 event | the event clauses (304 wrong clauses accepted) |
| S7 code | the codes (360 incoherent codes accepted) |
| the round trip | **equivalent** in every corpus, as the structure predicts (above) |

**Draft 1's 15 accepted mutations, classed** (the review asked that they be told apart from encodings that should
have been refused):
- **1 should have been refused.** C5 at offset 31 makes the top frame its loop's If with flag 0: a top If without its
  refused arm, a state no run reaches. Draft 2's grammar cannot express it.
- **12 are positions the run passed through.** These are another pass's bit, an earlier statement, or the other arm.
- **2 are valid shapes the run never reached.** They are A23's and A23′'s other claim.
- **None was non-canonical.**

On the same frame forgeries, one edit from each live cut with every flag value, draft 1 accepted 157. **74 of them lie
outside the shapes:**
- 51 are flag states no run reaches: a bit on a top For, flag 4 below the top, or a top If without its arm;
- 16 are frames not nested in the frame before, which draft 2 refuses by S2 or S3;
- 7 are top Performs, which draft 2 refuses by S4.

Draft 2 accepts none outside the shapes, on those forgeries and on the forgeries from every shape.

**What this means: the form proves a cut well-formed, never that it happened.**
- A cut that is a valid shape of its program decodes and decides, and 14 of 15 single-byte changes that stay valid
  change a standing.
- What holds a cut to its run is where it lives. It sits in the `'R'` event, the trace head commits it, the head is in
  the receipt core, and four executions must write the same core (`CUT-0.md` §2, "Where it would live").
- A single lying host can write a consistent forged cut, as it can write a consistent session (`CUT-0.md` §3).
  Integrity is not truth.

**Does not show:**
- version 1's frames (the tick block, the ports, TICK-BUDGET), which are DECLARED. S4 is version 0's alone, and S6 is
  open under 4.3;
- that the generated shapes are exactly the reachable ones. They are reachable by the calls' structure. S4 still
  admits a top statement whose expression cannot refuse by value, such as `Let i be 0`, which no run reaches;
- that the families cover every construct (they are the proponent's grammar and seed);
- anything about R8, which reads none of these fields.

## 4. The compatibility policy (proposed; the owner's to rule)

**The facts, read from the code:**
- **A version-0 law** writes `orlog-law 0` (`sema.py` 601). Its trace head starts from `"orlog-trace-0"` (`interp.py`
  91), its `'R'` payload is the code alone (`interp.py` 108), and its receipt is `orlog-receipt 0`, with the trace
  head in it (`interp.py` 74).
- **COMPAT-0 freezes each frozen text's receipt core** by its sha256 (`tests/compat.py`). A change to version 0's `'R'`
  payload would change the core of every refused text and fail the gate.
- **The court reads a refusal from the receipt's status line** (`court.py` 245–247), never from the `'R'` payload.
- **Version 1** (`CONTRACT-DRAFT.md` 5.3 and 6.1): a law headed `orlog-law 1` requires `orlog-receipt 1`, and its
  trace head starts from `"orlog-trace-1"`. The law's header fixes which trace and receipt a run writes.
- **No version-1 record exists.** Nothing in `src/` writes `orlog-law 1`. The repository holds the words only in
  research prose and in the session model's stand-in law.

**The policy:**

| | rule |
|---|---|
| P1 | **Version-0 records stay as they are.** They are never rewritten, re-encoded or read under version 1's grammar. A version-0 `'R'` payload is the code alone |
| P2 | **No cut is drawn from a version-0 record.** It has none, and none is reconstructed: a Perform emits no event, and replaying the reference to recover one was rejected. CUT-0 over version-0 texts runs only in research, on the instrumented reference's frames, labelled as such. It is never a reading of a record |
| P3 | **R8's readings of every record are unchanged.** R8 reads the status line and the claim lines, and no field of the cut |
| P4 | **The grammar is chosen by the law's header** (5.3), never by sniffing the payload. A version-1 payload that does not decode under its grammar is a malformed trace, refused with its reason, with no fallback to version 0's |
| P5 | **A change to the cut's bytes after the freeze is a new trace version** (`orlog-trace-2`) and a new receipt version, never an edit of version 1's grammar. Each version's decoder is kept while records of it exist. A record whose version has no decoder is UNCLASSIFIED, never reinterpreted |
| P6 | **The format freezes by the owner's ruling, before the first version-1 receipt is frozen anywhere** (a COMPAT-1 baseline, a vector or a fixture). Freezing a refused version-1 receipt freezes its trace head, and so the cut's bytes |
| P7 | **A reading names its versions:** the trace version it decoded, the settlement rule's digest and the core it read. A later reading is linked beside it, never written over it (the seams' versioned history, below) |

**One cost, under every option.** The cut is in the receipt core, so the reference and the three compiled backends
must compute the same cut. The frame stack becomes a twin surface in `gen_c`, `gen_rs` and `gen_py`, held by the
agreement record.

## Draft 1, superseded the same day

Draft 1 put a flag byte on every frame: 0 for none; 1 or 2 for a For's bit; 4 for a For whose bounds refused; 3 and
an arm for an If. Its probe measured:
- 89,035 refused runs decoding to the live K̂;
- 3,812 single-byte mutations, with 15 accepted, all canonical;
- four field plants caught.

Its output is kept, marked superseded, as `evidence/run1-cut0-schema-draft1.txt`. The draft-2 probe reruns draft 1's
decoder on its own 3,812 mutations and reproduces the 15.

It was superseded for two reasons:
- the derivation from the rule found two values the rule never reads;
- the shape check found one of its 15 accepted mutations, and 74 of its accepted forgeries, outside what a run can
  produce.

Its results stand as measured. Its claim that every field had a role held for the four fields, and not for the
values its flag allowed.

## The reviews' six seams, disposition by disposition

| seam | disposition |
|---|---|
| the cut's schema | **derived from the rule and tested here (draft 2).** Two of the reviewer's five fields are kept. `refusal_code` is kept as the refusal's identity, not a decision field. `frame_stack` is made precise as statement, selector, a bit below the top and an arm on top. Three fields are left out: `open_claims` is derived (at most one claim is open, the top statement); `operation_count` and `tick_index` are not read. The format freezes only by ruling (P6). An old record is never reinterpreted (P1, P5) |
| the comparison's classes | **accepted.** Each difference carries: a direction (TIGHTER, LOOSER, UNCHANGED, MIXED) over a defined ordering; an evidence reference to a registered finding, by record and number (`ADVERSARY-ROUND-D.md` 1–26, `manifold/ADVERSARY.md` F1–F5 and G1–G7); and a disposition (EXPLAINED, UNRESOLVED, REJECTED). An unexplained difference blocks admission |
| claims settled under R8 | **accepted: versioned history.** A reading keeps its rule identity. A later rule's reading is linked beside it, never written over it. Re-evaluation or migration needs the owner's ruling and preserves both readings |
| triggers for promotion | **accepted, without the time trigger.** The gate has four parts: T10 discharged, or its debt waived explicitly by the owner (a waiver, never a pass); every finding in the frozen register disposed; zero unexplained differences on the frozen corpora; the owner's ruling. **Corrections:** CUT-0's obligation is T10, not T11. There is no "beta" admission and no promotion by deadline: a deadline lapses privileges, not obligations |
| host-agnostic evidence | **accepted, already in place.** The receipt core is the host-independent projection. Host and build identity stay in the session record and the agreement record (`ROUNDS.md`, the review's point 1). The reviewer's premise that "F1 ruled backend identity into the receipt" was a proposal, rejected there |
| appeals | **accepted.** An appeal is an append-only record linked to the two readings and the comparison. It names the appellant, the objection, the authority that disposes of it, and the outcome. It never changes a receipt or a reading, and a researcher's finding stays distinct from the owner's authority |
