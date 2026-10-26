# §12 and §13 probes: expected outcomes

Written by the clean-room twin's author from SPEC.md (body, §11, §12, §13) alone, 2026-10-25. Each probe is a canonical `.orl` text in this folder; `manifest.json` gives its text seal and its law seal as UNKNOWN. Every expectation was worked by hand before the twin ran on the probe; the twin is checked against them with `python twin/probe_run.py --check --dir probes3`, and its alternative readings with `python twin/probe_run.py --dir probes3 --alts`. `expected.json` holds the same expectations for a machine.

How to read an entry:
- **refused CODE**: a compile refusal, so no receipt (§11 G2).
- otherwise the receipt lines that do not depend on the law seal (`status`, `output-bytes`, `events`, `ops`, `claims` and each `claim` line) and the output.
- **basis**: `§12` or `§13` when that text decides the outcome; `twin reading` when it does not, with the other reading, the twin's `--alt` switch for it, and the outcome under it.
- A Sealed line uses `lusab-lusab-lusab-lusab`, well formed and (barring 2^-64) not the law's words.

| probe | rule | tests | expected | basis |
|---|---|---|---|---|
| `p2-depth-24-passes` | §12 NESTING-DEPTH | a label of 24 parts is allowed | `status COMPLETED`, output `1\n`, `output-bytes 2`, `events 1`, `ops 24`, `claims 0` | §12 |
| `p2-depth-25-refused` | §12 NESTING-DEPTH | a label of 25 parts | refused **NESTING-DEPTH** | §12 |
| `p2-line-check-before-depth` | §13 phase 2 | one line: LINE-CHECK is listed before NESTING-DEPTH | refused **LINE-CHECK** | §13 |
| `p2-depth-before-numbering` | §13 phase 2 | one line both 25 parts deep and misnumbered: NESTING-DEPTH first | refused **NESTING-DEPTH** | §13 |
| `p2-numbering-line-before-depth-line` | §13 phase 2 | one pass, line by line: NUMBERING on line 2 before NESTING-DEPTH on line 3 | refused **NUMBERING** | §13 |
| `p2-seal-place-before-depth` | §13 phase 2 | after the Sealed line, SEAL-PLACE is listed before NESTING-DEPTH | refused **SEAL-PLACE** | §13 |
| `p2-reference-of-25-parts` | §12 NESTING-DEPTH | a reference (not a label) of 25 parts names no clause | refused **UNKNOWN-CLAUSE** | twin reading; *other reading* (`--alt ref-parts`): NESTING-DEPTH, if the bound on a label's parts also bounded references → refused **NESTING-DEPTH** |
| `p2-period-inside-literal` | §13 phase 2 | the line ends with a quote, its period inside the literal | refused **LINE-FORM** | §13 |
| `p2-sealed-prefix-opens` | §13 phase 2 | 'Sealed: ' opens a Sealed line; what follows is malformed | refused **SEAL-FORM** | §13 |
| `p2-second-sealed-malformed` | §13 phase 2 | a second Sealed line that is malformed: SEAL-FORM before SEAL-PLACE | refused **SEAL-FORM** | §13 |
| `p2-no-period-after-sealed` | §13 phase 2 | a clause line without its period after the Sealed line: LINE-FORM first | refused **LINE-FORM** | §13 |
| `p2-bad-check-after-sealed` | §13 phase 2 | after the Sealed line: SEAL-PLACE before LINE-CHECK | refused **SEAL-PLACE** | §13 |
| `p2-title-after-note-after-sealed` | §13 phase 2 | the Sealed line is content, a Note is not | refused **TITLE-PLACE** | §13 |
| `p2-line-check-line-1-before-line-form-line-9` | §13 phase 2 | §13's own example | refused **LINE-CHECK** | §13 |
| `p3-lex-before-syntax` | §13 phase 3 | the statement is read into tokens whole: '@' is LEX though '=' fails first | refused **LEX** | §13 |
| `p3-lex-at-the-end` | §13 phase 3 | a SYNTAX fault early, an unreadable '?' last | refused **LEX** | §13 |
| `p3-syntax-clause-1-before-lex-clause-2` | §13 phase 3 | across clauses, clause order decides | refused **SYNTAX** | §13 |
| `p3-syntax-before-procedure-name` | §13 phase 3 | a To with a reserved first word that does not parse | refused **SYNTAX** | §13 |
| `p3-perform-fly-away-1` | §13 phase 3 | §13's own example | refused **SYNTAX** | §13 |
| `p3-syntax-before-unknown-procedure` | §13 phase 3 | an unknown call and a syntax fault in one clause | refused **SYNTAX** | §13 |
| `p3-name-alone-unknown` | §13 phase 3 | §13's own example: the name alone, defined nowhere | refused **UNKNOWN-PROCEDURE** | §13 |
| `p3-call-holds-a-number` | §13 phase 3 | §13's own example | refused **SYNTAX** | §13 |
| `p3-perform-the-name` | §13 phase 3 | the filler 'the' is not part of a call | refused **SYNTAX** | §13 |
| `p3-call-reserved-first-word` | §13 phase 3 | a call in an Unless arm beginning with a reserved word | refused **SYNTAX** | §13 |
| `p3-to-without-name` | §13 phase 3 | a To with no name | refused **SYNTAX** | §13 |
| `p3-perform-nothing` | §13 phase 3 | a Perform with nothing after it | refused **SYNTAX** | §13 |
| `p3-call-in-arm-to-semicolon` | §13 phase 3 | an inline arm's call ends at ';' | `status COMPLETED`, output `2\n`, `output-bytes 2`, `events 1`, `ops 2`, `claims 0` | §13 |
| `p3-unknown-call-in-arm-never-run` | §13 phase 3 | UNKNOWN-PROCEDURE is static, run or not | refused **UNKNOWN-PROCEDURE** | §13 |
| `p3-call-to-nested-to` | §12 procedures, §13 phase 3 | procedures are collected from top-level clauses, so a nested To's name is no procedure | refused **UNKNOWN-PROCEDURE** | twin reading; *other reading* (`--alt procs-all`): PROCEDURE-PLACE, if every To clause's name were collected (§13: 'a name no To clause defines') → refused **PROCEDURE-PLACE** |
| `p3-malformed-to-defines-nothing` | §12 procedures, §13 phase 3 | a call (clause 1) of a name whose top-level To (clause 2) does not parse | refused **UNKNOWN-PROCEDURE** | twin reading; *other reading* (`--alt procs-lexer`): SYNTAX, if the lexer collected the words after 'To' whether or not the clause parses → refused **SYNTAX** |
| `p3-to-spacing` | §12 procedures | spacing inside ', do the following' and the name does not matter | `status COMPLETED`, output `1\n`, `output-bytes 2`, `events 1`, `ops 2`, `claims 0` | §12 |
| `p3-procedure-name-of-nested-to` | §12 procedures, §13 phase 3 | a nested To is parsed: PROCEDURE-NAME (phase 3) before PROCEDURE-PLACE (phase 6) | refused **PROCEDURE-NAME** | §13 |
| `ed-23-parens-pass` | §13 EXPRESSION-DEPTH | 23 nested parentheses around a name: 24 on the path | `status COMPLETED`, output `5\n`, `output-bytes 2`, `events 2`, `ops 2`, `claims 0` | §13 |
| `ed-24-parens` | §13 EXPRESSION-DEPTH | 24 nested parentheses around a name: 25 | refused **EXPRESSION-DEPTH** | §13 |
| `ed-63-terms-pass` | §13 EXPRESSION-DEPTH | Say with 63 terms joined by plus: the tree is 64 deep | `status COMPLETED`, output `63\n`, `output-bytes 3`, `events 1`, `ops 63`, `claims 0` | §13 |
| `ed-64-terms` | §13 EXPRESSION-DEPTH | with 64 terms: 65 deep | refused **EXPRESSION-DEPTH** | §13 |
| `ed-23-minuses-pass` | §13 EXPRESSION-DEPTH | 23 unary minuses and a number: 24 | `status COMPLETED`, output `-1\n`, `output-bytes 3`, `events 1`, `ops 24`, `claims 0` | §13 |
| `ed-24-minuses` | §13 EXPRESSION-DEPTH | 24 unary minuses and a number: 25 | refused **EXPRESSION-DEPTH** | §13 |
| `ed-23-nots-pass` | §13 EXPRESSION-DEPTH | 23 nots over 1 = 1: 24 on the path to each 1 | `status COMPLETED`, output `false\n`, `output-bytes 6`, `events 1`, `ops 25`, `claims 0` | §13 |
| `ed-24-nots` | §13 EXPRESSION-DEPTH | 24 nots: 25 | refused **EXPRESSION-DEPTH** | §13 |
| `ed-23-phrases-pass` | §13 EXPRESSION-DEPTH | 23 nested phrases and a number: 24 | `status COMPLETED`, output `1\n`, `output-bytes 2`, `events 1`, `ops 24`, `claims 0` | §13 |
| `ed-24-phrases` | §13 EXPRESSION-DEPTH | 24 nested phrases: 25 | refused **EXPRESSION-DEPTH** | §13 |
| `ed-mixed-24-pass` | §13 EXPRESSION-DEPTH | 6 nots, 6 parentheses, 6 minuses, 5 phrases and a number: 24 | `status COMPLETED`, output `true\n`, `output-bytes 5`, `events 1`, `ops 19`, `claims 0` | §13 |
| `ed-mixed-25` | §13 EXPRESSION-DEPTH | the same with a seventh minus: 25 | refused **EXPRESSION-DEPTH** | §13 |
| `ed-item-counts` | §13 EXPRESSION-DEPTH | 24 nested 'item ... of' around a number: is 'item' an atom? | refused **EXPRESSION-DEPTH** | twin reading; *other reading* (`--alt depth-atoms5`): COMPLETED, if only §13's five kinds (number, text, name, parenthesized expression, phrase) were counted → `status COMPLETED`, output `1\n`, `output-bytes 2`, `events 2`, `ops 27`, `claims 0` |
| `ed-true-counts` | §13 EXPRESSION-DEPTH | 24 parentheses around true: is 'true' an atom? | refused **EXPRESSION-DEPTH** | twin reading; *other reading* (`--alt depth-atoms5`): COMPLETED, if true were not counted (it is none of §13's five kinds) → `status COMPLETED`, output `true\n`, `output-bytes 5`, `events 1`, `ops 1`, `claims 0` |
| `ed-is-not-not-counted` | §13 EXPRESSION-DEPTH | the not of 'is not less than' on the right operand's path | `status COMPLETED`, output `false\n`, `output-bytes 6`, `events 1`, `ops 3`, `claims 0` | twin reading; *other reading* (`--alt depth-isnot`): EXPRESSION-DEPTH, if the not that item 37 puts around the test were one of 'the nots' → refused **EXPRESSION-DEPTH** |
| `ed-is-not-left-operand` | §13 EXPRESSION-DEPTH | 23 parentheses around the left operand of 'is not even' | `status COMPLETED`, output `true\n`, `output-bytes 5`, `events 1`, `ops 3`, `claims 0` | twin reading; *other reading* (`--alt depth-isnot-tree`): EXPRESSION-DEPTH, if the not of item 37 were on the tree path to every atom below it (a path a left-to-right reading has passed before the not is written) → refused **EXPRESSION-DEPTH** |
| `ed-unless-not-not-counted` | §13 EXPRESSION-DEPTH | the implicit not of Unless on its condition's path | `status COMPLETED`, output `1\n`, `output-bytes 2`, `events 1`, `ops 4`, `claims 0` | twin reading; *other reading* (`--alt depth-implicit-not`): EXPRESSION-DEPTH, if Unless's not (counted at run time, item 15) were on the path → refused **EXPRESSION-DEPTH** |
| `ed-missing-atom` | §13 EXPRESSION-DEPTH | 24 '(' then ')': a 25th atom is expected but absent | refused **SYNTAX** | twin reading; *other reading* (`--alt depth-entry`): EXPRESSION-DEPTH, if the count were taken on entering an atom position → refused **EXPRESSION-DEPTH** |
| `ed-met-before-later-syntax` | §13 phase 3 | the nesting part is met left to right, before a later SYNTAX | refused **EXPRESSION-DEPTH** | §13 |
| `ed-after-earlier-syntax` | §13 phase 3 | a SYNTAX fault before the deep part | refused **SYNTAX** | §13 |
| `ed-tree-checked-after-parse` | §13 phase 3 | a 64-term tree whose parse fails at its end: SYNTAX | refused **SYNTAX** | §13 |
| `ed-before-unknown-procedure` | §13 phase 3 | EXPRESSION-DEPTH before UNKNOWN-PROCEDURE in one clause | refused **EXPRESSION-DEPTH** | §13 |
| `ed-tree-before-unknown-procedure` | §13 phase 3 | the tree's depth before UNKNOWN-PROCEDURE | refused **EXPRESSION-DEPTH** | §13 |
| `ed-clause-1-before-syntax-clause-2` | §13 phase 3 | clause order across clauses | refused **EXPRESSION-DEPTH** | §13 |
| `ed-tree-paren-node` | §13 EXPRESSION-DEPTH | 63 terms, the first parenthesized: is '( )' a node of the tree? | refused **EXPRESSION-DEPTH** | twin reading; *other reading* (`--alt tree-no-paren`): COMPLETED, if parentheses were not nodes of the tree → `status COMPLETED`, output `63\n`, `output-bytes 3`, `events 1`, `ops 63`, `claims 0` |
| `ed-tree-cat-one-node` | §13 EXPRESSION-DEPTH | 64 parts joined by 'followed by' | `status COMPLETED`, output `1111111111111111…1111111111\n`, `output-bytes 65`, `events 1`, `ops 64`, `claims 0` | twin reading; *other reading* (`--alt tree-cat-binary`): EXPRESSION-DEPTH, if 'followed by' were a left-associative binary node → refused **EXPRESSION-DEPTH** |
| `ed-tree-inline-below-clause` | §13 EXPRESSION-DEPTH | an inline Say of 63 terms in an If arm | refused **EXPRESSION-DEPTH** | twin reading; *other reading* (`--alt tree-inline-root`): COMPLETED, if an inline statement rooted its own tree → `status COMPLETED`, output `63\n`, `output-bytes 3`, `events 1`, `ops 64`, `claims 0` |
| `ed-tree-is-not-two-nodes` | §13 EXPRESSION-DEPTH | 'is not less than' with a right operand of 62 terms | refused **EXPRESSION-DEPTH** | twin reading; *other reading* (`--alt tree-isnot-one`): COMPLETED, if 'is not less than' were one node → `status COMPLETED`, output `false\n`, `output-bytes 6`, `events 1`, `ops 64`, `claims 0` |
| `ed-tree-length-name` | §13 EXPRESSION-DEPTH | 63 terms, the first 'the length of xs': is xs a node? | `status COMPLETED`, output `63\n`, `output-bytes 3`, `events 2`, `ops 66`, `claims 0` | twin reading; *other reading* (`--alt tree-name-node`): EXPRESSION-DEPTH, if the name in 'length of X' were a node below the phrase → refused **EXPRESSION-DEPTH** |
| `ed-tree-conversions` | §13 EXPRESSION-DEPTH | 63 conversions in a row | refused **EXPRESSION-DEPTH** | twin reading; *other reading* (`--alt tree-no-conv`): COMPLETED, if conversions were not nodes of the tree → `status COMPLETED`, output `1.0\n`, `output-bytes 4`, `events 1`, `ops 64`, `claims 0` |
| `ln-16-pass` | §12 LOOP-NESTING | 16 nested For loops | `status COMPLETED`, output `1\n`, `output-bytes 2`, `events 17`, `ops 33`, `claims 0` | §12 |
| `ln-17-mixed` | §12 LOOP-NESTING | 17 nested loops, While and For alternating | refused **LOOP-NESTING** | §12 |
| `ln-ifs-do-not-count` | §12 LOOP-NESTING | 16 loops with 7 If blocks between them | `status COMPLETED`, output `1\n`, `output-bytes 2`, `events 17`, `ops 40`, `claims 0` | §12 |
| `ln-siblings-do-not-nest` | §12 LOOP-NESTING | 17 loops in sequence | `status COMPLETED`, no output, `output-bytes 0`, `events 0`, `ops 17`, `claims 0` | §12 |
| `ln-place-before-condition` | §12 LOOP-NESTING, §13 phase 6 | the 17th loop's condition is undeclared | refused **LOOP-NESTING** | twin reading; *other reading* (`--alt loop-parts-first`): UNDECLARED, if a loop's own parts were checked before its nesting → refused **UNDECLARED** |
| `ln-procedure-body` | §12 LOOP-NESTING | a procedure of 16 nested loops performed inside a loop | `status COMPLETED`, output `1\n`, `output-bytes 2`, `events 18`, `ops 36`, `claims 0` | §12 |
| `w-let-expression-before-name` | §13 phase 6 | Let x (REDECLARED) be a TYPE fault | refused **TYPE** | §13 |
| `w-for-bound-before-counter` | §13 phase 6 | For i (REDECLARED) from y (UNDECLARED) | refused **UNDECLARED** | §13 |
| `w-for-upper-bound-before-counter` | §13 phase 6 | For i (REDECLARED) from 1 to 2.5 (TYPE) | refused **TYPE** | §13 |
| `w-for-lower-bound-type-at-once` | §13 phase 6 | For from 1.5 (TYPE) to y (UNDECLARED) | refused **TYPE** | twin reading; *other reading* (`--alt for-bounds-post`): UNDECLARED, if the bounds' Int requirement were checked after both bounds → refused **UNDECLARED** |
| `w-item-index-before-list` | §13 phase 6 | item 1.5 (TYPE) of y (UNDECLARED) | refused **TYPE** | §13 |
| `w-set-item-list-before-value` | §13 phase 6 | Set item of an Int (TYPE) to y (UNDECLARED) | refused **TYPE** | §13 |
| `w-set-item-index-before-counter` | §13 phase 6 | Set item 1.5 (TYPE) of a counter (LOOP-VARIABLE) | refused **TYPE** | §13 |
| `w-increase-item-numbers-before-value` | §13 phase 6 | Increase item of a Bool list (TYPE) by y | refused **TYPE** | §13 |
| `w-append-value-before-list` | §13 phase 6 | Append y (UNDECLARED) to an Int (TYPE) | refused **UNDECLARED** | §13 |
| `w-while-condition-before-fuel` | §13 phase 6 | While 1 (TYPE), at most 0 times (FUEL) | refused **TYPE** | §13 |
| `w-while-undeclared-before-fuel` | §13 phase 6 | While y, at most 5*10^18 times (FUEL) | refused **UNDECLARED** | §13 |
| `w-define-references-before-name` | §13 phase 6 | a Define naming a later procedure, notwithstanding §9 | refused **UNKNOWN-CLAUSE** | §13 |
| `w-define-name-before-value` | §13 phase 6 | Define go (a later procedure's name) as y | refused **REDECLARED** | §13 |
| `w-to-walked-before-define` | §13 phase 6, §13 item 47 | To go (clause 1) walked before Define go notwithstanding §9 (clause 2): the To meets the rule's name first | refused **REDECLARED** | §13 |
| `w-define-value-before-proviso` | §13 phase 6 | a TYPE value, an undeclared proviso | refused **TYPE** | §13 |
| `w-define-target-before-value` | §13 phase 6 | notwithstanding a Define of another name; value undeclared | refused **NOTWITHSTANDING-TARGET** | §13 |
| `w-define-one-type-at-value` | §13 phase 6 | the one-type relation is checked at the value, before the proviso | refused **TYPE** | §13 |
| `w-to-place-before-name` | §13 phase 6 | a nested To named as a visible variable | refused **PROCEDURE-PLACE** | §13 |
| `w-to-name-before-body` | §13 phase 6 | a To named as a visible variable, its body undeclared | refused **REDECLARED** | §13 |
| `w-claim-condition-before-oracle` | §13 phase 6 | an undeclared condition, a certificate of §9 | refused **UNDECLARED** | §13 |
| `w-claim-oracle-before-premises` | §13 phase 6 | a later certificate target, an unknown premise | refused **CERTIFICATE-TARGET** | §13 |
| `w-and-types-both-operands` | §13 phase 6 | 1 and y: both operands typed before and's own check | refused **UNDECLARED** | §13 |
| `w-and-check-before-later-operand` | §13 phase 6 | (true and 1) or y: the and's check completes first | refused **TYPE** | §13 |
| `w-quotient-types-both-operands` | §13 phase 6 | the quotient of 1.5 by y | refused **UNDECLARED** | §13 |
| `w-operator-check-before-next-operand` | §13 phase 6 | (1 plus true) plus z: post-order | refused **TYPE** | §13 |
| `w-copies-count-post-order` | §13 phase 6 | a list of 1.5 copies of y | refused **UNDECLARED** | twin reading; *other reading* (`--alt copies-count-first`): TYPE, if the count's Int requirement were checked when the count is reached, as an index's is → refused **TYPE** |
| `w-for-counter-last` | §13 phase 6 | For i (a rule's name) from 1 to y | refused **UNDECLARED** | §13 |
| `w-agreement-written-order` | §13 phase 6 | agreement of a later clause and a missing one | refused **AGREEMENT-TARGET** | §13 |
| `w-literal-range-in-written-order` | §13 phase 6 | LITERAL-RANGE (left operand) before UNDECLARED | refused **LITERAL-RANGE** | §13 |
| `w-increase-number-before-value` | §13 phase 6 | Increase a Text (TYPE) by y (UNDECLARED) | refused **TYPE** | §13 |
| `i47-variable-after-procedure-upper` | §13 item 47 | Let GO after To go | refused **REDECLARED** | §13 |
| `i47-procedure-after-visible-variable` | §13 item 47 | To go after Let Go | refused **REDECLARED** | §13 |
| `i47-procedure-after-invisible-variable` | §13 item 47 | To go after a go whose block has ended | `status COMPLETED`, output `2\n`, `output-bytes 2`, `events 2`, `ops 4`, `claims 0` | twin reading; *other reading* (`--alt visible-global`): REDECLARED, if 'one name may not stand for a variable and a procedure' covered variables no longer visible → refused **REDECLARED** |
| `i47-define-then-procedure` | §13 item 47 | Define go, then To go | refused **REDECLARED** | §13 |
| `i47-procedure-then-define-case` | §13 item 47 | To go, then Define Go (compared lowercased) | refused **REDECLARED** | §13 |
| `i47-local-in-own-body` | §13 item 47 | a local of the procedure's own name inside its body | `status COMPLETED`, output `1\n`, `output-bytes 2`, `events 2`, `ops 3`, `claims 0` | §13 |
| `i47-variable-in-later-procedure` | §13 item 47 | a later procedure's local named as an earlier procedure | refused **REDECLARED** | §13 |
| `i47-define-named-as-nested-to` | §12 procedures, §13 item 47 | a Define named as a nested To | refused **PROCEDURE-PLACE** | twin reading; *other reading* (`--alt procs-all`): REDECLARED, if every To clause's name were collected → refused **REDECLARED** |
| `i47-rule-and-variable-case-sensitive` | §13 item 47 | Let R beside Define r | `status COMPLETED`, output `3\n`, `output-bytes 2`, `events 2`, `ops 4`, `claims 0` | twin reading; *other reading* (`--alt rule-var-lower`): REDECLARED, if a variable were compared with rule names lowercased → refused **REDECLARED** |
| `i47-counter-named-procedure` | §13 item 47 | a For counter Go after To go | refused **REDECLARED** | §13 |
| `i47-multiword-name-and-variable` | §13 item 47 | To go home beside a variable go | `status COMPLETED`, output `1\n`, `output-bytes 2`, `events 2`, `ops 3`, `claims 0` | §13 |
| `i47-own-call-in-block` | §13 item 47 | a procedure calling itself from an inline arm | refused **PERFORM-BEFORE-DEFINITION** | §13 |
| `i29-append-to-counter` | §13 item 29 | Append to a For counter | refused **TYPE** | §13 |
| `i29-remove-from-counter` | §13 item 29 | Remove from a For counter | refused **TYPE** | §13 |
| `i29-decrease-item-of-counter` | §13 item 29 | Decrease item of a For counter | refused **LOOP-VARIABLE** | §13 |
| `i48-length-of-rule` | §13 item 48 | length of a rule name | refused **UNDECLARED** | §13 |
| `i48-remove-from-rule` | §13 item 48 | Remove from a rule name | refused **UNDECLARED** | §13 |
| `i48-set-item-of-rule` | §13 item 48 | Set item of a rule name | refused **UNDECLARED** | §13 |
| `i48-item-of-rule` | §13 item 48 | item of a rule name | refused **UNDECLARED** | §13 |
| `ref-leading-zero-certificate` | §12 references | a certificate of §01 names §1 | `status COMPLETED`, no output, `output-bytes 0`, `events 2`, `ops 3`, `claims 1`, `claim 0 2 1 1 1 1 1` | §12 |
| `ref-leading-zero-notwithstanding` | §12 references | notwithstanding §001 names §1 | `status COMPLETED`, output `2\n`, `output-bytes 2`, `events 1`, `ops 2`, `claims 0` | §12 |
| `ref-leading-zero-given` | §12 references | given §01 names §1 | `status COMPLETED`, no output, `output-bytes 0`, `events 2`, `ops 2`, `claims 2`, `claim 0 1 1 1 0 0 0`, `claim 1 2 1 1 0 0 0` | §12 |
| `nested-to-empty-block` | §12 procedures, §13 phase 4 | a nested To without children: EMPTY-BLOCK (phase 4) | refused **EMPTY-BLOCK** | §13 |
| `nested-to-place` | §12 procedures | a nested To is parsed and refused | refused **PROCEDURE-PLACE** | §12 |
| `x-nesting-depth-before-lex` | §13 phase table | NESTING-DEPTH (phase 2, line 2) before LEX (phase 3, clause 1) | refused **NESTING-DEPTH** | §13 |
| `x-expression-depth-before-orphan` | §13 phase table | EXPRESSION-DEPTH (phase 3) before ORPHAN-OTHERWISE | refused **EXPRESSION-DEPTH** | §13 |
| `x-define-place-before-loop-nesting` | §13 phase table | DEFINE-PLACE (phase 5) before LOOP-NESTING (phase 6) | refused **DEFINE-PLACE** | §13 |
| `x-loop-nesting-before-later-type` | §13 phase table | LOOP-NESTING in walk order, before a later TYPE | refused **LOOP-NESTING** | §13 |
| `x-expression-depth-before-literal-range` | §13 phase table | EXPRESSION-DEPTH (phase 3) before LITERAL-RANGE (6) | refused **EXPRESSION-DEPTH** | §13 |
| `x-empty-block-before-loop-nesting` | §13 phase table | the 17th loop has no children: EMPTY-BLOCK (phase 4) | refused **EMPTY-BLOCK** | §13 |

## Corrections after the first run

The twin was run on these probes once their expectations were written. It disagreed with one hand-worked value, and the working was wrong; the probes involved are listed with what changed and why.

- `w-define-references-before-name`: Text changed after the first run: see the correction of w-to-walked-before-define.
- `w-define-name-before-value`: Text changed after the first run: its first text passed for the reason of w-to-walked-before-define.
- `w-to-walked-before-define`: Corrected: first worked as UNKNOWN-CLAUSE (the Define's references before its name), which overlooked that the walk reaches the To at clause 1 first, and that 'a procedure may not take the lowercased name of any rule. Rules are collected first' (§13). The twin's REDECLARED was right; this was the first text of w-define-references-before-name.

## Points of §12 and §13 still open

Each names the probes that separate the readings; the twin's reading is its default, the other its `--alt`.

- **§12 against §13: which To clauses define a procedure (phase 3).** §12 says procedures are collected from top-level clauses; §13 says a call names a procedure unless 'no To clause defines' it. A nested To clause has a name but is refused PROCEDURE-PLACE in phase 6. The twin takes §12's mechanism: a nested To defines nothing (p3-call-to-nested-to, i47-define-named-as-nested-to). A To clause that does not parse defines nothing either (p3-malformed-to-defines-nothing); 'collected by the lexer' could mean the words after 'To' are collected before any parse.
- **EXPRESSION-DEPTH: which atoms count.** §13 lists 'a number, a text, a name, a parenthesized expression, a phrase'. §4's atom has five more forms: true, false, this law's seal, 'item U of X' and 'a list of N copies of V'. The twin counts every atom of §4 (ed-item-counts, ed-true-counts).
- **EXPRESSION-DEPTH: which nots count.** §13 counts 'the nots'. Item 37 makes 'is not less than' a not around the test, item 15 gives Unless a not, item 24 gives a Define's 'unless' a not. The twin counts only written not and 'it is not the case that' (ed-is-not-not-counted, ed-unless-not-not-counted). §13 defines the count on 'the path from a statement to each atom' (a tree) but says it is met reading left to right: the two disagree for the left operand of 'is not even' or 'is not less than', which a left-to-right reading has passed before the not is written (ed-is-not-left-operand). The twin's reading is the one under which they agree.
- **EXPRESSION-DEPTH: where the count is exceeded.** 'Met in the order of a left-to-right predictive reading' does not say whether an atom position that holds no atom counts. The twin counts atoms that are there (ed-missing-atom).
- **EXPRESSION-DEPTH: what the statement's tree is.** Only the plus chain is given. Not said: whether parentheses are nodes (ed-tree-paren-node), whether 'followed by' is one node of k parts as §7 evaluates it or a binary chain (ed-tree-cat-one-node), whether an inline statement is a node below its clause's statement (ed-tree-inline-below-clause), whether 'is not less than' is two nodes (ed-tree-is-not-two-nodes), whether conversions are nodes (ed-tree-conversions), whether the name in 'length of X' is a node (ed-tree-length-name). The twin: parentheses, conversions and the inline statement are nodes, a concatenation is one node, 'is not less than' is a not over a comparison, X is part of its phrase.
- **LOOP-NESTING: where in the loop's statement.** §13 orders a While's parts (C, then N) and a For's (A, B, the counter) but not LOOP-NESTING among them; a To's place is checked first. The twin checks a loop's place first (ln-place-before-condition).
- **Phase 6: a requirement on an operand.** Refinement 2 checks 'a requirement on one part' when that part is reached, while an expression's operands are checked before 'the operator's own check'. For a For's bound (a statement part) the twin checks Int at the bound (w-for-lower-bound-type-at-once); for 'a list of N copies of V' (an expression) after both operands (w-copies-count-post-order). §13 settles 'item I of X' (the index at I) and quotient (after both) only.
- **Item 47: 'one name may not stand for a variable and a procedure'.** The lead sentence reads over the whole program; its bullets restrict it to a procedure already defined and a visible variable. The twin follows the bullets (i47-procedure-after-invisible-variable).
- **Rules and variables: case.** Only procedure names are said to be compared lowercased. The twin compares a variable with a rule name exactly, as identifiers (i47-rule-and-variable-case-sensitive).
- **NESTING-DEPTH and references.** Labels are bounded at 24 parts; a reference of 25 parts names no clause, UNKNOWN-CLAUSE in the twin (p2-reference-of-25-parts).

## Rules no canonical text can reach

- **PROCEDURE-NAME against UNKNOWN-PROCEDURE, and EXPRESSION-DEPTH against PROCEDURE-NAME, within a clause.** Only a To clause can be PROCEDURE-NAME, and a To clause holds no call and no expression, so the order within a clause between these codes never decides anything.
- **'A procedure body starts again at 0' (LOOP-NESTING).** A To stands only at top level (a nested To is PROCEDURE-PLACE, and §13 checks the place before the body), so its body is at loop depth 0 however the rule reads; only a dynamic reading (calls adding their callee's loops) would differ (ln-procedure-body).
- **Phase 1 and QUOTE-BOUNDARY.** The door's codes and its literal rules cannot be reached by a canonical text: the twin takes canonical text.
