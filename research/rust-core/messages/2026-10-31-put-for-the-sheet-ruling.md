# The message put to him with the ruling sheet of 2026-10-31 (2026-10-31), word for word

He ruled on this message, not on the sheet's unseen contents. In his words: *"I am ruling on the exact descriptions and measured consequences supplied in your message, not certifying the unseen contents."* (his ruling on the ruling sheet, RULINGS.md). Kept by his D6 (his ruling on REREAD-9's disposition).

Taken from the session's own transcript by a script, never retyped. The text follows, unedited.

---

The sheet is at [RULING-SHEET-2026-10-31.md](research/RULING-SHEET-2026-10-31.md), every item marked PROPOSED. It follows your draft's five sections and keeps Phase 0 apart from the debate. Where your draft couldn't fill in (A) to (D), it now has the exact text, a whole witness law for each choice, and what each choice moves.

**My recommendations on (A) to (D):**
- **(A) and (B):** take only the parts the words actually state.
  - For `neg`, `abs` and `sqrt` that means dropping the inferred "⟨type⟩ is numeric" part.
  - For the comparisons, "one numeric type" describes the pair of operands, so the kind is checked together with the equality.

  The reason is your own G principle, *"the checker must implement the adopted wording, not a more permissive interpretation that happens to pass the existing corpus."* Neither change moves any existing verdict (measured).
- **(C) changed while I wrote the sheet, and I want you to know before you rule.**
  - The literal reading, that "undeclared" means no clause declares the variable, looked like the obvious choice.
  - I tried it in a copy of the checker. On 83 of R6's 10,000 mutants the types cycled and never settled, the same kind of non-terminating loop you asked about earlier, while the current checker settles on all of them.
  - So that reading can't be adopted until its own least fixed point is defined.
  - I recommend the checker's current reading: a variable counts as declared once the walk has met it. Variables, unlike rules, are already numbered and scoped by the walk (E1, W8). This should be stated explicitly, though it is the "typing as met" approach E2 rejected for rules.
  - If you'd rather have the order-free reading, those 83 mutants are its test.
- **(D):** keep the checker's choice, the first declaration met, consistent with E1's numbering. The checker doesn't change.

**The six files:** I recommend option (c).
- Replace your account's path prefix with a token, separately for each way it is spelled (escaped, plain, short 8.3 form).
- Record the original's sha256, and have the check restore the files byte for byte when given the prefix, failing without it.

That keeps the evidence lossless and in the repository, with no home path in it. It still has to be built and tested with plants before use. Keeping them outside the tree is the simpler fallback.

**The leftover DRAFT items** are each listed with a recommendation. Most are wording, plants or in-place notes that move nothing. Two contain genuinely new obligations that I marked yours rather than recommending:
- extending the unbounded operation count to the other counters (ZA7);
- confining R7's writer plants to the writer's named code (ZA9).

**One correction to your draft:** in (C) it is the checker under test that types variables as met. The independent verifier is what found it.

Both of the sheet's quotes match their sources, and every witness I didn't run myself is labelled as such.
