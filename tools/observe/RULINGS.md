# Rulings on observe

## Status Comparison Ruling (2026-11-04)

A changed status is a break. Status means:
- Class: COMPLETED or REFUSED
- Code: refusal code where one exists (split from the clause location)
- Location: printed for a reader, not compared

NO VERDICT on either side is undetermined: neither preserved nor broken,
and it never reads as a pass.

The line relation remains OPEN pending real edits.

## Output Preservation Ruling (2026-11-04)

**Output preservation, closed laws.** For a closed law, output preservation requires exact equality of the output lines, and the status must match under the status ruling: the class, and the refusal code where one exists. Any added, removed, changed or reordered line, and any status change, is a change to a protected observation and needs an authorization under A_L: declared by a person with authority over the target and bound to the full 256-bit law seal. An authorized change is not a break; the authorization is the record that the change was declared. This qualifies the status ruling: an authorized status change is not a break. A text that no longer compiles is a break, by a different mechanism: it has no law and no seal, so no authorization can bind to it. NO VERDICT on either side is undetermined: neither preserved nor broken, and it never reads as preserved. The relation for open laws remains OPEN. This can be loosened later; loosening needs a ruling.

**Scope.** Change management only. No law byte, compile result, seal or COMPAT row changes.

**Enforcement.** None yet. No record format exists, the tool does not print the full seal, and --require is not built. Until those exist this is followed by hand, and the tool's report is input to a person's judgment, not a check.

**Limits.** The cost figures come from ten stand-in pairs written by one hand: they show the shape of the friction, not its size in real work.

**For the record format, deferred.** An authorization for a change binds both seals, old and new. A change to a protected observation always changes the seal; a seal change does not always change an observation, so a seal change is necessary for a break, not sufficient.
