# Re-read 1: the disposition of the twin's 31 findings (2026-10-26)

The twin's report is `REREAD-1-REPORT.md`, saved unchanged: 12 findings on finding 24's ruling (F24-1 to F24-12), 16 on
the PREFIX licence (PREFIX-1 to PREFIX-16) and 3 on T10.5's statement. Each is disposed below by the draft's author.
Nothing here is ruled. A finding that needs his word is put to him, and his answer is recorded in his words.

**Classes of disposition:**
- **DRAFT:** a drafting defect, fixed in draft 3;
- **ASK:** put to the owner;
- **WITH F6:** decided with finding 6's ruling;
- **D_r:** a dependency found after the sets were computed, recorded in `AR-F24-PREFIX.md` and read at the next re-read;
- **LEDGER:** a fix to `ROUNDS.md`;
- **OPEN:** an open question already recorded elsewhere, left there;
- **NOTED:** no change.

## Checked against the files first

- **The twin's partial reads.** It read SPEC.md and RUNTIME-SPEC.md only in part this time, and relied on its full
  reading during the review. CHECKED: both files have the same sha256 in the review's reading set and in this one
  (`MANIFEST.md`, `27dfff0c…` and `0bd571d6…`), so the parts it did not reopen are the parts it read before.
- **F24-1.** CHECKED: SPEC §14 says "Agreement on these samples is consistency between two readers of one text … it is
  not a proof" (SPEC.md line 684). The draft's added "only 1b's agreement can show that" contradicts it.
- **F24-5.** CHECKED against the court as built (`src/orlog/court.py`, `panel`). Integrity is its own column (AGREED,
  INCOMPLETE, CONTESTED or REFERENCE-ONLY). The evaluation column (REFUTED, true in k of k, R8's refused evaluation,
  UNREACHED) prints beside it, and held requires agreement. So REFERENCE-ONLY is not ranked among the evaluation
  standings; both columns print. The court as built decides it.
- **PREFIX-10.** CHECKED against the same function: a claim reads GROUNDED only if it is held, its channel is
  admissible (`grounding_admissible`: never computation or agreement), and a ledger line ratifies its own seal. The
  draft's "held, a ratified seal and a channel that can ground" is right.
- **The twin's grounding probes** write the default `computation` channel, which `grounding_admissible` refuses. The
  twin said so (SN-D); its GROUNDED readings hold only for a claim "by" an admissible channel.
- **The record's own gap.** His answer adopts the labels "D" and "B1 + 4a + 5c + K1". They are defined in packet A §4
  (alternative D) and packet B §3.1 to §3.4 (B1, 4a, 5c, K1). The excerpt given to the twin carried only packet A §5's
  and packet B §4's wordings, so the twin could not read the labels' definitions. K1's definition decides two of its
  findings (PREFIX-1 and PREFIX-4). This is put to him (ASK 1).

## The dispositions

| # | disposition | what is done |
|---|---|---|
| F24-1 | DRAFT | "only 1b's agreement can show that" removed from 15.13.11 |
| F24-2 | DRAFT | the adopted sentence "E2 defines the claim-specific continuation condition; it does not erase the court's backend-agreement requirement" stated in 15.13.11, unquoted (adopted, not his words); 15.13.1, 15.13.4 and 15.12.2 tagged with F24 where they now depend on it |
| F24-3 | DRAFT | 15.12.5 scoped: in a real reading the claim is held only once court R1 is met, which before 1b it is not (15.13.11) |
| F24-4 | DRAFT | 15.12.5's tags split: its first sentence R6's, its 1a sentence F24's |
| F24-5 | DRAFT | decided by the court as built (checked above): REFERENCE-ONLY is the integrity column, and the evaluation column prints beside it in 15.13.12's order. Stated in 15.13.11, tagged [v0] |
| F24-6 | ASK 3 | whether R6's version-0 control (no log) is configured, as condition 1 reads literally, or measured |
| F24-7 | NOTED | both adopted texts stand: the rows run (packet A, "as R6's first rider requires"); the proposal's "may" grants no exemption from the rider |
| F24-8 | DRAFT | "(1 to 4)" removed |
| F24-9 | D_r | 15.13.6, 15.13.10 and 15.13.12 added to A_F24 |
| F24-10 | DRAFT | his scope sentence stated whole in 15.13.11, in his words |
| F24-11 | OPEN | how a configured result is labelled so that it is never read as an agreement record or a core belongs to the amended set's "reporting" row (15.14). Added there as an open item |
| F24-12 | DRAFT | a 15.15 row for D10's open two-commit split |
| PREFIX-1 | ASK 1, DRAFT | K1 follows the tick block's body (packet B §3.4), which is reading B. 15.13.8's closing line, which stated reading A, is removed |
| PREFIX-2 | DRAFT | with that line removed, 15.12.4's whole-law form (packet B §4: "licenses no claim of the law") is the only one |
| PREFIX-3 | ASK 2 | the closure's rule table, proposed from K1 and SPEC §3's statement kinds |
| PREFIX-4 | ASK 1 | K1 starts from the top-level clauses from the boundary on and follows Performs, so an unperformed To after the boundary adds nothing (PX-6 licensed) *[withdrawn 2026-10-27 by his answer: PX-6's outcome must follow from the whole rule applied to a fixture]* |
| PREFIX-5 | DRAFT | R6's "first input" stated as the first port value bound, or the first `'T'` in a law with no port, never the loading of the log; tagged [open: finding 6] |
| PREFIX-6 | WITH F6 | the binding place must not precede the boundary, or B1 is wider than R6. Put to him with finding 6 |
| PREFIX-7 | DRAFT | 15.0's sentence made a pointer, untagged as ruled |
| PREFIX-8 | DRAFT | the description of D-18's boundary removed; the adopted words kept |
| PREFIX-9 | DRAFT | the adopted words restored: "a claim may be conservatively excluded even when a particular execution would never reach an input-dependent path" |
| PREFIX-10 | NOTED | checked above; the sentence tagged [v0] |
| PREFIX-11 | DRAFT | R6's "exempt" and the ruling's "licensed" said to name one thing |
| PREFIX-12 | DRAFT | 15.1.6, 15.3's read-once bullet and 15.1.3 name PREFIX; ruled tags removed from text that is not his |
| PREFIX-13 | D_r | 15.1.1 and 15.13.6 added to A_PREFIX; SPEC §3's statement table is the rule table's source (ASK 2) |
| PREFIX-14 | DRAFT | 15.15 rows for the rule table, if it stays open, and for finding 6's presupposition |
| PREFIX-15 | NOTED | harmless, and robust if port places change |
| PREFIX-16 | OPEN | whether a refusal before the boundary may withhold a licensed claim is the question his R6 record already leaves open ("Its scope is his reason's": a refusal inside the prefix, `hoisted_omit.orl`) |
| T10.5-1 | LEDGER | "one frame" becomes "one activation" |
| T10.5-2 | LEDGER | the uniqueness argument names the arm selector |
| T10.5-3 | LEDGER | the editorial note moved out of the statement |

**Totals:** 16 DRAFT; 4 ASK, put as three questions (PREFIX-1 and PREFIX-4 share ASK 1, and PREFIX-1 also has a
DRAFT part); 1 WITH F6; 2 D_r; 3 LEDGER; 2 OPEN; 3 NOTED. That is 12 + 16 + 3 = 31 findings, each disposed once.

## His answers to the three questions (2026-10-27)

Recorded whole in `RULINGS.md`, "The labels' definitions, the closure's rule table, and R6's control":
- **ASK 1 (PREFIX-1, PREFIX-4):** the labels adopt the definitions they designate, recorded as adopted text; the
  conclusions drawn from them are not ruled. The tick block has its own closure rule that follows its body; unknown
  kinds fail closed. PX-6 is not marked licensed: its outcome must follow from the whole rule applied to a fixture.
  The PREFIX-4 row's "(PX-6 licensed)" above is withdrawn by his answer.
- **ASK 2 (PREFIX-3):** the rule table adopted, under his four conditions, port declarations among the no-addition
  kinds. It establishes no individual claim's licence or standing.
- **ASK 3 (F24-6):** R6's row and its paired control share the configured witness; a measured version-0 control is a
  separate row, labelled as a distinct measurement.

## What follows

Draft 3 applies the DRAFT dispositions and the answers to the three questions. The excerpt of the rulings gains the
labels' definitions if he confirms ASK 1. The twin then re-reads every clause draft 3 changes, together with the D_r
additions, before anything is built. That re-read can be batched with finding 6's and finding 8's sets.
