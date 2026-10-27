# The statements of T10.0 to T10.8, as they stand for R7's fourth re-read (2026-10-27)

Extracted from `research/run-1/ROUNDS.md`'s theorem ledger, as before: each row's statement column only. T10.7 is scoped and T10.8 is new, after the third re-read's F6-3.

- **T10.0.** **T10 by row (split by the owner's claims ruling, 2026-10-26).** T10 holds when T10.1 to T10.6 hold (and T10.7 from version 1), the rows cover every statement kind, and the cut records the frames exactly

- **T10.1.** **The rest of a block.** When a frame's statement ends, the run goes on with the next sibling that is not an absorbed Otherwise, and at the block's end with the owning frame. K̂ adds everything those siblings may execute, with values ignored

- **T10.2.** **The refused If.** A condition refused at arm i leaves arms i onward and the Otherwise able to run. The arms before i read false in this pass

- **T10.3.** **A For.** Below the top, it repeats exactly when its bit says passes remain. Its bounds are evaluated once, at entry (ESTABLISHED, `interp.py`'s For). Refused at its own clause, its body follows

- **T10.4.** **A While.** Under S2 it always may repeat: its condition is unknown, and its fuel check is a passable refusal. Refused at its own clause, its body follows

- **T10.5.** **A Perform.** On the stack, a procedure returns only to the frame below it, the actual caller. Since there is no recursion, each procedure has at most one activation on the stack (its Perform's frame and the frames of its body's statements, nested ones included), so the cut, whose arm selector names an inline arm's own frame, names each call without ambiguity. Reached in the continuation, its whole body counts, transitively. Refused at its own operation (version 1 only), its body follows. *(Reworded 2026-10-26 by the twin's finding 42: "since there is no recursion" had been given as the reason for the return, which holds on any stack; what it supports is the uniqueness. Reworded again 2026-10-27 by its re-read, T10.5-1 to -3: "one frame" became "one activation", the arm selector is named, and this note moved after the statement. And by its second re-read, T10.5-4: nested statements' frames named.)*

- **T10.6.** **The open claim.** A claim whose evaluation is open at the cut is withheld, named by its id, since two claims can share a clause (F2)

- **T10.7.** **The tick block (version 1; added 2026-10-26 by `SPEC-15-DRAFT.md`'s review).** Below the top, the tick block may run its body again, since another tick may run. At NOT-RUN t or LOG-OPEN, the cut is the tick block's head before tick t, and K̂ is the tick block and every procedure performed from it. *Scoped 2026-10-27 by finding 6's ruling (re-read 3's F6-3): this holds only when the law declares no read-once port or its log holds the read-once record; the read-once stop is T10.8.*

- **T10.8.** **The read-once stop (version 1; added 2026-10-27 by finding 6's ruling, re-read 3's F6-3).** When the log lacks the read-once record, the cut is the first read-once declaration, a top-level frame not begun, and K̂ is the rest of the block from it, the tick block's body and every procedure performed included, transitively, values ignored; its withholdings name the row "the read-once stop"
