# Noted for later (not started)

## A clause-ontology appendix to LAW-FORMAT-0 (the owner's note, 2026-10-30)

**Status.** Noted at his word, *"note for later"*. Not started, not scheduled, not a ruling. It does not enter draft 1
or the targeted re-read of draft 1 unless he says so.

His note, whole:

> Yes—but I would map clauses ontologically in a narrow, operational sense, not introduce a new semantic ontology into
> Ørlǫg.
>
> There is a real benefit before the Rust core: LAW-FORMAT-0 now has to describe not just how clauses are encoded, but
> how their relationships determine execution. The clause-order finding demonstrates why a flat list of clause types is
> insufficient.
>
> I would build a clause ontology map with five dimensions:
>
> | Dimension | What it records |
> | --- | --- |
> | Kind | The existing grammatical clause or statement form. |
> | Structure | Parent, children, arm membership, and ordering. |
> | Binding | What the clause declares, references, or makes available. |
> | Execution | When it is evaluated, what it reads or changes, and whether it can refuse. |
> | Representation | Its law-byte encoding and the fields derived from it. |
>
> For every existing clause form, the map should answer:
>
> 1. What is it?
> 2. What can contain it?
> 3. What can it contain?
> 4. What does it depend on?
> 5. When does it execute?
> 6. What observable outcomes can it produce?
> 7. Which bytes and derivations represent it?
>
> Three constraints are essential.
>
> - No invented categories. Start from the grammar, specifications, and actual interpreter behavior. Don't create
>   abstract clause classes just because they seem philosophically elegant.
> - No duplicate authority. The map explains existing constructs; LAW-FORMAT-0 remains the machine-format contract, and
>   the specifications remain authoritative for language behavior.
> - No semantic shortcuts. Two clauses that look structurally similar must not be declared equivalent unless their
>   execution and observable consequences support that conclusion.
>
> ## Why this matters beyond the Rust core
>
> This map could eventually become the bridge between the language's grammar, compiler diagnostics, LLM-assisted law
> construction, and independent implementations.
>
> An LLM could work with explicit relationships—permitted children, required bindings, evaluation order, and possible
> refusal outcomes—instead of guessing at legal clause combinations from prose.
>
> But I would not make it a new runtime layer or require the Rust core to implement an ontology engine. It should be a
> specification and verification artifact.
>
> My recommendation: add a clause-ontology appendix to LAW-FORMAT-0, built from existing constructs and checked against
> the 298-law corpus. Keep it descriptive, not normative beyond the obligations already established by the
> specifications. Have the independent re-reader check that every clause form and execution-relevant relationship is
> accounted for.
>
> That gives Ørlǫg an explicit structural account of what its clauses are and how they relate, without prematurely
> inventing a second language inside the language.

**Where it would start, when he asks.**
- Draft 1's section 4 (the forms, which may stand inline), sections 5 and 7 (the walk, the clause a statement runs
  as, cost counters, the budget's check), section 6 (the derivations) and W5–W12 already hold most of the seven
  answers for each form.
- The appendix would gather them per form, add nothing normative, and be checked against the 298 laws by
  `format_check.py`'s walk.
