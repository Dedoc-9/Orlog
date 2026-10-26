# §11 probes: expected outcomes

Written by the clean-room twin's author from SPEC.md v0.1 (§11) alone, 2026-10-25. Each probe is a canonical `.orl` text in this folder; `manifest.json` gives its text seal and its law seal as UNKNOWN. Every expectation was worked by hand from §11 and then checked against the twin (`python twin/probe_run.py --check`); the twin did not write them. `expected.json` holds the same expectations for a machine.

How to read an entry:
- **refused CODE**: a compile refusal, so no receipt (§11 G2).
- otherwise the receipt lines that do not depend on the law seal: `status`, `output-bytes`, `output-sha256`, `events`, `ops`, `claims` and each `claim` line; and the output. `law-seal`, `text-seal` and `trace-head` are left out (the trace head starts from the law seal). The output never contains the seal words.
- **§11**: the expectation rests on §11 alone. **twin**: it also rests on a twin reading of a point §11 leaves open (listed at the end), and *other reading* gives the outcome under the alternative.
- A Sealed line in a probe uses the words `lusab-lusab-lusab-lusab`, well formed and (barring a 2^-64 chance) not the law's, so a run that reaches phase 8 is SEAL-MISMATCH under any law seal.

| probe | items | tests | expected | basis |
|---|---|---|---|---|
| `g3-lines-before-syntax` | G3 | phase 2 (NUMBERING, line 2) before phase 3 (SYNTAX, clause 1) | refused **NUMBERING** | §11 |
| `g3-line-order-check` | G3 | phase 2 goes line by line: LINE-CHECK on line 1 before LINE-FORM on line 2 | refused **LINE-CHECK** | twin; *other reading:* LINE-FORM, if phase 2's code list were passes over all lines |
| `g3-line-order-numbering` | G3 | the same with NUMBERING on line 2 and LINE-FORM on line 3 | refused **NUMBERING** | twin; *other reading:* LINE-FORM, if phase 2's code list were passes over all lines |
| `g3-syntax-before-shape` | G3 | phase 3 (SYNTAX, clause 2) before phase 4 (EMPTY-BLOCK, clause 1) | refused **SYNTAX** | §11 |
| `g3-unknown-procedure-before-shape` | G3 | UNKNOWN-PROCEDURE is phase 3, before phase 4's ORPHAN-OTHERWISE | refused **UNKNOWN-PROCEDURE** | §11 |
| `g3-unknown-procedure-clause-order` | G3 | phase 3 goes clause by clause: UNKNOWN-PROCEDURE (clause 1) before SYNTAX (clause 2) | refused **UNKNOWN-PROCEDURE** | twin; *other reading:* SYNTAX, if phase 3's code list were passes over all clauses |
| `g3-procedure-name-clause-order` | G3, 20 | PROCEDURE-NAME (clause 1) before SYNTAX (clause 3), clause order | refused **PROCEDURE-NAME** | twin; *other reading:* SYNTAX, if phase 3's code list were passes over all clauses |
| `g3-orphan-before-empty` | G3 | one clause both orphaned and empty: ORPHAN-OTHERWISE is listed first | refused **ORPHAN-OTHERWISE** | §11 |
| `g3-shape-tree-order` | G3 | phase 4 in tree order: UNEXPECTED-CHILDREN (clause 1) before ORPHAN-OTHERWISE (clause 4) | refused **UNEXPECTED-CHILDREN** | twin; *other reading:* ORPHAN-OTHERWISE, if phase 4's code list were passes over the tree |
| `g3-shape-preorder` | G3 | 'tree order' as depth-first pre-order: the orphan at §1.1 comes before §2's children | refused **ORPHAN-OTHERWISE** | twin; *other reading:* UNEXPECTED-CHILDREN, if 'tree order' were breadth-first |
| `g3-define-place-before-static` | G3 | phase 5 (DEFINE-PLACE, clause 3) before phase 6 (TYPE, clause 1) | refused **DEFINE-PLACE** | §11 |
| `g3-perform-order-is-static` | G3, 22 | PERFORM-BEFORE-DEFINITION is static (phase 6): phase 4's ORPHAN-OTHERWISE wins | refused **ORPHAN-OTHERWISE** | §11 |
| `g3-static-before-cycle` | G3 | phase 6 (TYPE, clause 3) before phase 7 (PRIORITY-CYCLE) | refused **TYPE** | §11 |
| `g3-cycle-before-seal` | G3 | phase 7 (PRIORITY-CYCLE) before phase 8 (SEAL-MISMATCH) | refused **PRIORITY-CYCLE** | §11 |
| `g3-literal-range-is-static` | G3, 38 | LITERAL-RANGE (clause 1) is static semantics, so SYNTAX (clause 2) wins | refused **SYNTAX** | twin; *other reading:* LITERAL-RANGE, if literals were range-checked while reading tokens (phase 3) |
| `g3-let-expression-first` | G3 | Let x (REDECLARED) be y (UNDECLARED): the expression is checked first | refused **UNDECLARED** | twin; *other reading:* REDECLARED, if the declared name were checked before its expression |
| `g3-syntax-then-lex` | G3, 8 | a misplaced token before an unreadable one: the first offending position decides | refused **SYNTAX** | twin; *other reading:* LEX, if a statement were read into tokens whole before parsing |
| `g3-lex-then-syntax` | G3, 8 | an unreadable token before a misplaced one | refused **LEX** | twin; *other reading:* SYNTAX, if unreadable characters were set aside until a parse succeeded |
| `g4-count-after-operands` | G4 | plus is counted after its operands, so the refusal inside them comes at ops 2 | `status REFUSED DIVISION-BY-ZERO 1`, no output, `output-bytes 0`, `events 1`, `ops 2`, `claims 0` | §11 |
| `g4-rule-counts-first` | G4, 6 | a rule use counts before its provisos; the refusal names the using clause | `status REFUSED DIVISION-BY-ZERO 3`, no output, `output-bytes 0`, `events 2`, `ops 4`, `claims 0` | §11 |
| `n02-title-no-space` | 2 | Title: takes any text, no space needed | `status COMPLETED`, output `1\n`, `output-bytes 2`, `events 1`, `ops 1`, `claims 0` | §11 |
| `n02-title-empty` | 2 | Title: with no text | `status COMPLETED`, output `1\n`, `output-bytes 2`, `events 1`, `ops 1`, `claims 0` | §11 |
| `n02-note-no-space` | 2 | Note: takes any text | `status COMPLETED`, output `1\n`, `output-bytes 2`, `events 1`, `ops 1`, `claims 0` | §11 |
| `n02-title-lowercase` | 2 | prefixes are case-sensitive: 'title:' is no Title line | refused **LINE-FORM** | §11 |
| `n02-sealed-no-space` | 2, 5 | 'Sealed:' without its space is not the exact 'Sealed: ' | refused **LINE-FORM** | twin; *other reading:* SEAL-FORM, if any line starting 'Sealed:' were a Sealed line |
| `n02-sealed-lowercase` | 2 | 'sealed: ' is not the exact prefix | refused **LINE-FORM** | §11 |
| `n03-two-titles` | 3 | a second Title | refused **TITLE-PLACE** | §11 |
| `n03-title-after-clause` | 3 | a Title after a clause | refused **TITLE-PLACE** | §11 |
| `n03-title-after-note` | 3 | a Title after a Note: is a Note 'content'? | `status COMPLETED`, output `1\n`, `output-bytes 2`, `events 1`, `ops 1`, `claims 0` | twin; *other reading:* TITLE-PLACE, if a Note counts as content |
| `n04-note-after-sealed` | 4, 5 | a Note may follow the Sealed line; the words then mismatch the law (phase 8) | refused **SEAL-MISMATCH** | §11 |
| `n04-clause-after-sealed` | 4 | a clause after the Sealed line | refused **SEAL-PLACE** | §11 |
| `n04-second-sealed` | 4 | a second Sealed line | refused **SEAL-PLACE** | §11 |
| `n04-title-after-sealed` | 3, 4, G3 | a Title after the Sealed line: TITLE-PLACE is checked before SEAL-PLACE | refused **TITLE-PLACE** | §11 |
| `n04-junk-after-sealed` | 4, G3 | a malformed line after the Sealed line: LINE-FORM is checked first | refused **LINE-FORM** | §11 |
| `n05-sealed-space-joined` | 5 | proquints joined by spaces | refused **SEAL-FORM** | §11 |
| `n05-sealed-three` | 5 | three proquints | refused **SEAL-FORM** | §11 |
| `n05-sealed-bad-letter` | 5 | 'c' is not a proquint consonant | refused **SEAL-FORM** | §11 |
| `n05-sealed-no-period` | 5 | no final period | refused **SEAL-FORM** | §11 |
| `n05-sealed-mismatch` | 5 | well formed, but not the law's words | refused **SEAL-MISMATCH** | §11 |
| `n06-leading-zeros` | 6 | label parts compared as integers: §01, §1.01, §002 are 1, 1.1, 2 | `status COMPLETED`, output `1\n2\n`, `output-bytes 4`, `events 2`, `ops 3`, `claims 0` | §11 |
| `n06-section-and-period` | 6 | '§1.' is neither label form | refused **LINE-FORM** | §11 |
| `n07-two-spaces` | 7 | exactly one space after the label | refused **LINE-FORM** | §11 |
| `n08-syntax` | 8 | a malformed statement | refused **SYNTAX** | §11 |
| `n08-lex-character` | 8 | a character that begins no token | refused **LEX** | §11 |
| `n08-lex-unterminated` | 8 | an unterminated text literal | refused **LEX** | §11 |
| `n08-lex-dot` | 8 | a second decimal point: '.' begins no token | refused **LEX** | §11 |
| `n09-mixed-labels` | 9 | the two label forms mixed | `status COMPLETED`, output `1\n2\n3\n`, `output-bytes 6`, `events 3`, `ops 3`, `claims 0` | §11 |
| `n10-no-separators` | 10 | no separator between tokens | `status COMPLETED`, output `13\n`, `output-bytes 3`, `events 1`, `ops 3`, `claims 0` | §11 |
| `n10-longest-word` | 10 | longest match: 'times3' is one word, so the statement does not parse | refused **SYNTAX** | §11 |
| `n11-colon` | 11 | ':' begins nothing | refused **SYNTAX** | §11 |
| `n12-reserved-any-case` | 12 | 'Sum' is reserved | refused **SYNTAX** | §11 |
| `n12-keywords-any-case` | 12 | keywords in any case | `status COMPLETED`, output `4\n`, `output-bytes 2`, `events 2`, `ops 3`, `claims 0` | §11 |
| `n13-seal-phrase-and-s` | 13 | 's' is an identifier; this law's seal is a phrase (compared, not printed) | `status COMPLETED`, output `5\ntrue\n`, `output-bytes 7`, `events 3`, `ops 4`, `claims 0` | §11 |
| `n15-unless-counts-not` | 15 | Unless counts its not: arm, not, Say | `status COMPLETED`, output `1\n`, `output-bytes 2`, `events 1`, `ops 3`, `claims 0` | §11 |
| `n16-unless-then` | 16 | Unless takes no then | refused **SYNTAX** | §11 |
| `n16-unless-inline-otherwise` | 16 | Unless takes no inline otherwise | refused **SYNTAX** | §11 |
| `n16-unless-otherwise-attaches` | 16, 15 | an Otherwise clause attaches to an Unless | `status COMPLETED`, output `2\n`, `output-bytes 2`, `events 1`, `ops 3`, `claims 0` | §11 |
| `n17-elseif-inline-otherwise` | 17 | an else-if arm takes no inline otherwise | refused **SYNTAX** | §11 |
| `n18-arm-condition-clause` | 18 | an absorbed arm's condition names its own clause (3, not 2) | `status REFUSED DIVISION-BY-ZERO 3`, no output, `output-bytes 0`, `events 2`, `ops 4`, `claims 0` | §11 |
| `n18-arm-statement-clause` | 18 | an absorbed arm's inline statement names its own clause | `status REFUSED DIVISION-BY-ZERO 3`, no output, `output-bytes 0`, `events 2`, `ops 4`, `claims 0` | §11 |
| `n18-arm-claim-clause` | 18 | an inline claim in an absorbed arm is declared at its own clause | `status COMPLETED`, no output, `output-bytes 0`, `events 1`, `ops 3`, `claims 1`, `claim 0 2 1 1 1 0 0` | §11 |
| `n19-decimal-bound` | 19 | a decimal While bound | refused **SYNTAX** | §11 |
| `n19-zero-bound` | 19 | a bound of 0 | refused **FUEL** | §11 |
| `n19-bound-over` | 19 | 2^62 + 1 | refused **FUEL** | §11 |
| `n19-bound-max` | 19 | 2^62 is allowed | `status COMPLETED`, no output, `output-bytes 0`, `events 0`, `ops 1`, `claims 0` | §11 |
| `n19-bound-beyond-i64` | 19 | a bound beyond i64 is FUEL, not LITERAL-RANGE | refused **FUEL** | §11 |
| `n20-name-reserved-the` | 20 | a name beginning with 'the' | refused **PROCEDURE-NAME** | §11 |
| `n20-name-statement-word` | 20 | a name beginning with 'say' | refused **PROCEDURE-NAME** | §11 |
| `n21-name-do-the-following` | 21 | the name 'do the following' | refused **PROCEDURE-NAME** | §11 |
| `n20-reserved-word-inside-name` | 20 | reserved words after the first are allowed | `status COMPLETED`, output `1\n1\n`, `output-bytes 4`, `events 2`, `ops 4`, `claims 0` | §11 |
| `n21-call-reserved-first-word` | 21, 20 | a call whose first word is reserved ('do the following' as an arm) | refused **SYNTAX** | twin; *other reading:* UNKNOWN-PROCEDURE (or PROCEDURE-NAME), if such a call were parsed as a name |
| `n22-perform-before-definition` | 22 | a top-level call before the definition | refused **PERFORM-BEFORE-DEFINITION** | §11 |
| `n22-recursion` | 22 | a procedure performing itself | refused **PERFORM-BEFORE-DEFINITION** | §11 |
| `n22-mutual` | 22 | mutual recursion | refused **PERFORM-BEFORE-DEFINITION** | §11 |
| `n23-notwithstanding-four` | 23 | notwithstanding with four references | `status COMPLETED`, output `5\n`, `output-bytes 2`, `events 1`, `ops 2`, `claims 0` | §11 |
| `n23-given-three` | 23, 32 | given with three references, one of them the claim itself | `status COMPLETED`, no output, `output-bytes 0`, `events 3`, `ops 3`, `claims 3`, `claim 0 1 1 1 0 0 0`, `claim 1 2 1 1 0 0 0`, `claim 2 3 1 1 0 0 0` | §11 |
| `n24-define-unless-counts` | 24 | a Define's unless counts its not | `status COMPLETED`, output `1\n`, `output-bytes 2`, `events 2`, `ops 4`, `claims 0` | §11 |
| `n25-two-provisos` | 25 | provided that and unless together | refused **SYNTAX** | §11 |
| `n26-the-everywhere` | 26 | the filler in every identifier position | `status COMPLETED`, output `7\n3\n3\n5\n`, `output-bytes 8`, `events 13`, `ops 22`, `claims 0` | §11 |
| `n27-set-item-unary` | 27 | the index of Set item is a unary | refused **SYNTAX** | §11 |
| `n27-increase-item-parenthesized` | 27 | a parenthesized index | `status COMPLETED`, output `[1, 7]\n`, `output-bytes 7`, `events 4`, `ops 8`, `claims 0` | §11 |
| `n28-define-in-arm` | 28 | a Define inside an inline arm | refused **SYNTAX** | §11 |
| `n28-while-in-arm` | 28 | a While inside an inline arm | refused **SYNTAX** | §11 |
| `n29-set-item-counter` | 29 | Set item of a For counter: LOOP-VARIABLE before the list type | refused **LOOP-VARIABLE** | §11 |
| `n29-increase-item-counter` | 29 | Increase item of a For counter | refused **LOOP-VARIABLE** | §11 |
| `n29-decrease-counter` | 29 | Decrease a For counter | refused **LOOP-VARIABLE** | §11 |
| `n29-append-to-counter` | 29 | Append to a For counter (not a set, increase or decrease) | refused **TYPE** | twin; *other reading:* LOOP-VARIABLE, if item 29 covered every write |
| `n30-certificate-later` | 30 | a later target | refused **CERTIFICATE-TARGET** | §11 |
| `n30-certificate-to` | 30 | a To clause | refused **CERTIFICATE-TARGET** | §11 |
| `n30-certificate-define` | 30 | a Define clause | refused **CERTIFICATE-TARGET** | §11 |
| `n30-certificate-decimals` | 30 | a Decimals clause | refused **CERTIFICATE-TARGET** | §11 |
| `n30-certificate-claim` | 30 | a claim clause | refused **CERTIFICATE-TARGET** | §11 |
| `n30-certificate-absorbed` | 30 | an absorbed Otherwise clause | refused **CERTIFICATE-TARGET** | §11 |
| `n30-certificate-in-procedure` | 30 | a clause inside a procedure body: its counter grows each run (2 + 2) | `status COMPLETED`, no output, `output-bytes 0`, `events 4`, `ops 9`, `claims 1`, `claim 0 6 1 1 1 3 4` | §11 |
| `n30-certificate-chain` | 30 | an If chain's counter covers its absorbed arms | `status COMPLETED`, output `2\n`, `output-bytes 2`, `events 3`, `ops 5`, `claims 1`, `claim 0 4 1 1 0 2 3` | §11 |
| `n31-agreement-earlier-any` | 31 | agreement of an earlier To and an earlier Define | `status COMPLETED`, no output, `output-bytes 0`, `events 1`, `ops 1`, `claims 1`, `claim 0 4 1 1 0 0 0` | §11 |
| `n31-agreement-same-clause` | 31 | agreement of one clause with itself | `status COMPLETED`, no output, `output-bytes 0`, `events 2`, `ops 3`, `claims 1`, `claim 0 2 1 1 1 0 0` | §11 |
| `n31-agreement-later` | 31 | a target that is not earlier | refused **AGREEMENT-TARGET** | §11 |
| `n32-premise-later-and-self` | 32 | premises later than the claim, and the claim itself | `status COMPLETED`, no output, `output-bytes 0`, `events 2`, `ops 2`, `claims 2`, `claim 0 1 1 1 0 0 0`, `claim 1 2 1 1 0 0 0` | §11 |
| `n32-premise-inline-claim` | 32 | an If clause whose arm is a claim is not a claim clause | refused **PREMISE-TARGET** | §11 |
| `n33-unknown-notwithstanding` | 33 | notwithstanding a missing clause | refused **UNKNOWN-CLAUSE** | §11 |
| `n33-unknown-given` | 33 | given a missing clause | refused **UNKNOWN-CLAUSE** | §11 |
| `n33-unknown-certificate` | 33 | a certificate of a missing clause | refused **UNKNOWN-CLAUSE** | §11 |
| `n33-unknown-agreement` | 33 | agreement with a missing clause | refused **UNKNOWN-CLAUSE** | §11 |
| `n34-list-stops-before-not` | 34 | 'and not' ends the list, so 'and' joins a list and a Bool | refused **TYPE** | §11 |
| `n34-list-goes-on-before-name` | 34 | 'and' before a name continues the list | `status COMPLETED`, output `[1, 2]\n`, `output-bytes 7`, `events 2`, `ops 3`, `claims 0` | §11 |
| `n34-list-goes-on-before-minus-and-the` | 34 | ',' before '-' and 'and' before 'the' continue the list | `status COMPLETED`, output `[1, -2, 3]\n`, `output-bytes 11`, `events 2`, `ops 4`, `claims 0` | §11 |
| `n34-list-goes-on-before-item` | 34 | 'and' before 'item' continues the list | `status COMPLETED`, output `[1, 6]\n`, `output-bytes 7`, `events 2`, `ops 5`, `claims 0` | §11 |
| `n35-short-circuit` | 35 | the right operand is not evaluated (it would be out of range) | `status COMPLETED`, output `false\ntrue\n`, `output-bytes 11`, `events 3`, `ops 6`, `claims 0` | §11 |
| `n36-minus-on-literal-counted` | 36 | -4 is a counted negation | `status COMPLETED`, output `-4\n`, `output-bytes 3`, `events 2`, `ops 3`, `claims 0` | §11 |
| `n37-is-not-forms` | 37 | is not E and is not equal to E: one op; is not less than, is not even: two | `status COMPLETED`, output `true\ntrue\nfalse\nfalse\ntrue\n`, `output-bytes 27`, `events 5`, `ops 12`, `claims 0` | §11 |
| `n37-is-not-nan` | 37, 50 | NaN: is not n is true; is not less than 1.0 is true; >= 1.0 is false | `status COMPLETED`, output `true\ntrue\nfalse\n`, `output-bytes 16`, `events 5`, `ops 10`, `claims 0` | §11 |
| `n38-fix-literal-over` | 38 | a Fix literal of 2^31 | refused **LITERAL-RANGE** | §11 |
| `n38-fix-literal-rounds-over` | 38 | a Fix literal that rounds to raw 2^63 | refused **LITERAL-RANGE** | §11 |
| `n38-fix-literal-max` | 38 | the largest Fix, exactly | `status COMPLETED`, output `2147483647.99999999976716935634613037109375\n`, `output-bytes 44`, `events 1`, `ops 1`, `claims 0` | §11 |
| `n38-float-literal-huge` | 38 | 10^309 as a Float literal | refused **LITERAL-RANGE** | §11 |
| `n38-float-literal-midpoint` | 38 | halfway between DBL_MAX and 2^1024 rounds (to even) to infinity | refused **LITERAL-RANGE** | §11 |
| `n38-float-literal-below-midpoint` | 38 | one below the midpoint rounds to DBL_MAX | `status COMPLETED`, output `1797693134862315708145274237…50404026184124858368.0\n`, `output-bytes 312`, `events 1`, `ops 1`, `claims 0` | §11 |
| `n39-int-with-fix` | 39, 42 | Int with Fix makes a Fix list; the Int item's promotion counts | `status COMPLETED`, output `[1.0, 2.5]\n`, `output-bytes 11`, `events 1`, `ops 3`, `claims 0` | §11 |
| `n39-int-with-float` | 39 | Int with Float makes a Float list | `status COMPLETED`, output `[1.0, 0.5]\n`, `output-bytes 11`, `events 1`, `ops 3`, `claims 0` | §11 |
| `n39-bool-with-int` | 39 | Bool goes only with Bool | refused **TYPE** | §11 |
| `n39-fix-with-float` | 39 | Fix with Float | refused **TYPE** | §11 |
| `n39-text-item` | 39 | a Text item | refused **TYPE** | §11 |
| `n40-promotion-inexact` | 40 | 2^53 + 1 promoted to Float | `status REFUSED INEXACT-CONVERSION 2`, no output, `output-bytes 0`, `events 1`, `ops 2`, `claims 0` | §11 |
| `n40-promotion-exact` | 40 | 2^53 is exact; the sum rounds | `status COMPLETED`, output `9007199254740992.0\n`, `output-bytes 19`, `events 1`, `ops 3`, `claims 0` | §11 |
| `n41-promotion-before-right-operand` | 41 | the left promotion overflows before the right operand divides by zero | `status REFUSED OVERFLOW 1`, no output, `output-bytes 0`, `events 1`, `ops 2`, `claims 0` | §11 |
| `n42-promotion-before-next-item` | 42 | a list item's promotion comes before the next item | `status REFUSED OVERFLOW 1`, no output, `output-bytes 0`, `events 1`, `ops 2`, `claims 0` | §11 |
| `n41-promotion-counts` | 41 | promotions in an operator and a comparison are counted | `status COMPLETED`, output `2.5\ntrue\n`, `output-bytes 9`, `events 2`, `ops 6`, `claims 0` | §11 |
| `n43-int-as-integer` | 43 | Int as an integer | refused **TYPE** | §11 |
| `n43-integer-part-of-int` | 43 | integer part of an Int | refused **TYPE** | §11 |
| `n43-fix-as-fixed` | 43 | Fix as a fixed | refused **TYPE** | §11 |
| `n44-length-of-text` | 44 | length of a Text | refused **TYPE** | §11 |
| `n45-int-and-fix-defines` | 45 | Define clauses of Int and Fix | refused **TYPE** | §11 |
| `n46-define-sees-earlier-variables` | 46 | a Define cannot see a later variable | refused **UNDECLARED** | §11 |
| `n46-define-uses-complete-rule` | 46 | a Define may use a rule completely defined before it | `status COMPLETED`, output `3\n`, `output-bytes 2`, `events 1`, `ops 4`, `claims 0` | §11 |
| `n46-define-uses-incomplete-rule` | 46 | a rule not completely defined before | refused **RULE-BEFORE-DEFINITION** | §11 |
| `n47-variable-before-procedure` | 47 | a local named as a procedure defined later is allowed | `status COMPLETED`, output `2\n`, `output-bytes 2`, `events 2`, `ops 4`, `claims 0` | §11 |
| `n47-variable-after-procedure` | 47 | a variable named (lowercased) as a procedure already defined | refused **REDECLARED** | §11 |
| `n47-procedure-after-variable` | 47 | a procedure named as a visible variable (the converse) | refused **REDECLARED** | twin; *other reading:* COMPLETED (ops 1, events 1), if item 47 restricted variables only |
| `n47-variable-named-rule` | 47 | a variable named as a rule defined later | refused **REDECLARED** | §11 |
| `n48-set-rule` | 48 | Set a rule name | refused **UNDECLARED** | §11 |
| `n48-append-to-rule` | 48 | Append to a rule name | refused **UNDECLARED** | §11 |
| `n48-increase-rule` | 48 | Increase a rule name | refused **UNDECLARED** | §11 |
| `n48-item-of-rule` | 48 | item of a rule name (a read, not a write) | refused **UNDECLARED** | twin; *other reading:* TYPE, if only writes to a rule name were UNDECLARED |
| `n49-decimals-nested` | 49 | Decimals not at top level | refused **DECIMALS-PLACE** | §11 |
| `n49-decimals-twice` | 49 | Decimals twice | refused **DECIMALS-PLACE** | §11 |
| `n49-decimals-after-literal` | 49 | Decimals after a decimal literal | refused **DECIMALS-PLACE** | §11 |
| `n49-decimals-after-literal-in-procedure` | 49 | after a decimal literal inside an earlier procedure | refused **DECIMALS-PLACE** | §11 |
| `n50-signed-zero-and-nan` | 50 | -0.0 is zero, not negative; NaN is none of the three | `status COMPLETED`, output `true\nfalse\nfalse\nfalse\nfalse\n`, `output-bytes 29`, `events 7`, `ops 15`, `claims 0` | §11 |
| `n51-static-closure` | 51 | §4 overrides §2 through the inapplicable §3 | `status COMPLETED`, output `1\n`, `output-bytes 2`, `events 2`, `ops 3`, `claims 0` | §11 |
| `n52-conflict-not-counted` | 52 | the comparison behind RULE-CONFLICT is not counted | `status REFUSED RULE-CONFLICT 3`, no output, `output-bytes 0`, `events 1`, `ops 2`, `claims 0` | §11 |
| `n52-agreeing-values-not-counted` | 52 | three equal values: two comparisons, uncounted | `status COMPLETED`, output `1\n`, `output-bytes 2`, `events 1`, `ops 2`, `claims 0` | §11 |
| `n53-event-e-index-and-tag` | 53, 54 | event E carries the 1-based index and a tagged value (visible in the trace) | `status COMPLETED`, no output, `output-bytes 0`, `events 4`, `ops 8`, `claims 0` | §11 |
| `n55-increase-promotion-counts` | 55 | Increase of a Fix by an Int: +1, promotion +1, add +1 | `status COMPLETED`, output `2.5\n`, `output-bytes 4`, `events 3`, `ops 5`, `claims 0` | §11 |
| `n55-increase-promotion-refusal` | 55 | the promotion refuses before the add is counted | `status REFUSED OVERFLOW 2`, no output, `output-bytes 0`, `events 2`, `ops 3`, `claims 0` | §11 |
| `n56-unevaluated-claim` | 56 | a claim never evaluated has ref clause and ref cost 0 0 | `status COMPLETED`, no output, `output-bytes 0`, `events 1`, `ops 2`, `claims 1`, `claim 0 2 0 0 0 0 0` | §11 |
| `n59-fix-as-integer` | 59 | -3.0 as an integer is -3; 2.5 refuses | `status REFUSED INEXACT-CONVERSION 2`, output `-3\n`, `output-bytes 3`, `events 2`, `ops 5`, `claims 0` | §11 |
| `n59-float-as-integer-overflow` | 59 | 2^63 is integral and finite, then OVERFLOW | `status REFUSED OVERFLOW 3`, output `4\n`, `output-bytes 2`, `events 2`, `ops 4`, `claims 0` | §11 |
| `n59-float-as-integer-inexact` | 59 | 2.5 as an integer | `status REFUSED INEXACT-CONVERSION 2`, no output, `output-bytes 0`, `events 1`, `ops 2`, `claims 0` | §11 |
| `n59-float-as-integer-nan` | 59 | NaN as an integer | `status REFUSED NOT-FINITE 3`, no output, `output-bytes 0`, `events 2`, `ops 4`, `claims 0` | §11 |
| `n60-negative-sqrt-int` | 60 | the square root of -4 | `status REFUSED NEGATIVE-SQRT 1`, no output, `output-bytes 0`, `events 1`, `ops 3`, `claims 0` | §11 |
| `n60-negative-sqrt-fix` | 60 | the square root of -0.25 (Fix) | `status REFUSED NEGATIVE-SQRT 1`, no output, `output-bytes 0`, `events 1`, `ops 3`, `claims 0` | §11 |
| `n60-float-sqrt-negative` | 60 | Float: NaN for a negative, -0.0 for -0.0 | `status COMPLETED`, output `NaN\n-0.0\n`, `output-bytes 9`, `events 2`, `ops 6`, `claims 0` | §11 |

Output digests (`output-sha256`) of the probes that run, for byte comparison:

- `g4-count-after-operands`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `g4-rule-counts-first`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `n02-title-no-space`: `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865`
- `n02-title-empty`: `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865`
- `n02-note-no-space`: `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865`
- `n03-title-after-note`: `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865`
- `n06-leading-zeros`: `a6e2b7a040683432de03a18fd8a1939a2fdf82585b364bfc874bdd4095c4cae1`
- `n09-mixed-labels`: `14c5e74c4b96ccef41cd94db73a9ec3348038ac094feca4fd897cecffa07cdae`
- `n10-no-separators`: `1a252402972f6057fa53cc172b52b9ffca698e18311facd0f3b06ecaaef79e17`
- `n12-keywords-any-case`: `7de1555df0c2700329e815b93b32c571c3ea54dc967b89e81ab73b9972b72d1d`
- `n13-seal-phrase-and-s`: `41fa93db86707a4aaca67dbe0deb71f40461c113f6c516524fa73edf7c9938a9`
- `n15-unless-counts-not`: `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865`
- `n16-unless-otherwise-attaches`: `53c234e5e8472b6ac51c1ae1cab3fe06fad053beb8ebfd8977b010655bfdd3c3`
- `n18-arm-condition-clause`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `n18-arm-statement-clause`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `n18-arm-claim-clause`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `n19-bound-max`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `n20-reserved-word-inside-name`: `ad0fadf63cc7cd779ce475e345bf4063565b63a3c2efef1eebc89790aaa6acba`
- `n23-notwithstanding-four`: `f0b5c2c2211c8d67ed15e75e656c7862d086e9245420892a7de62cd9ec582a06`
- `n23-given-three`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `n24-define-unless-counts`: `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865`
- `n26-the-everywhere`: `e69b2044cb9511361231e79de24c6ac125b8adc115ff9e4da21ef01308920e6a`
- `n27-increase-item-parenthesized`: `eac45f807cbf7f81c39e9cb5b45645a5669d8345a5050ab5de97fe1f2576733b`
- `n30-certificate-in-procedure`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `n30-certificate-chain`: `53c234e5e8472b6ac51c1ae1cab3fe06fad053beb8ebfd8977b010655bfdd3c3`
- `n31-agreement-earlier-any`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `n31-agreement-same-clause`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `n32-premise-later-and-self`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `n34-list-goes-on-before-name`: `1fb3ffcf3df89e31f56932d4a64a23eede8a2f6707898bf14d1fc42a78286868`
- `n34-list-goes-on-before-minus-and-the`: `3b8901140a9bacbe55633a7dbb232e26f6b5059def5f0e92893fe80a18e55cd1`
- `n34-list-goes-on-before-item`: `0f16334da44c39740370fd6fe9ef6e50c1004df1af4caa9f5edc73853f151217`
- `n35-short-circuit`: `b8c77a864147a827751b38954756ea3294b6e725092a22825bd82be8cff2ec1c`
- `n36-minus-on-literal-counted`: `8fbfec21acf8f74313698199401f9eb352920bd889b4865b272e657167808aa0`
- `n37-is-not-forms`: `0ff9850ba3cdaa76835231fc4e346bde8b1ea0f3ae55c3a9e4f080851b0d549a`
- `n37-is-not-nan`: `0823bd24a3b200a27310872ca7794008d70b316ae5841675b1acf789e4169aec`
- `n38-fix-literal-max`: `9adb003ebec5c61d0423dc8e3a7d7f14117725e823b1f7edfd56c7320e3087d8`
- `n38-float-literal-below-midpoint`: `1733a5b6d410ce5f89bc7e8606dcb5658da0e51fd473563b37bb7c0f11bf6802`
- `n39-int-with-fix`: `57fc6378132ffaa4ac70e409d6bc137cdb5424c22c53e3811c70bb69f819623f`
- `n39-int-with-float`: `047285899277c06b05e03e6a4f08ae56c764c6918e0518f1a25003a0dc7bdcce`
- `n40-promotion-inexact`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `n40-promotion-exact`: `c3834dac02e6c083ca45e7228ad877dbefd8953657593b08a1365cf78103af9a`
- `n41-promotion-before-right-operand`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `n42-promotion-before-next-item`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `n41-promotion-counts`: `88f1e0514a6c535cc3d248ffb6232c839a95a13caadabff7b18baf9e11b6ab58`
- `n46-define-uses-complete-rule`: `1121cfccd5913f0a63fec40a6ffd44ea64f9dc135c66634ba001d10bcf4302a2`
- `n47-variable-before-procedure`: `53c234e5e8472b6ac51c1ae1cab3fe06fad053beb8ebfd8977b010655bfdd3c3`
- `n50-signed-zero-and-nan`: `615873448a3275fe40306925f4d7e70793057f8829e35b6ba7fbd2ef23747b34`
- `n51-static-closure`: `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865`
- `n52-conflict-not-counted`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `n52-agreeing-values-not-counted`: `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865`
- `n53-event-e-index-and-tag`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `n55-increase-promotion-counts`: `686513ed91231892fbf0c4e72acee20264caa8538e8389157a942a808dba6531`
- `n55-increase-promotion-refusal`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `n56-unevaluated-claim`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `n59-fix-as-integer`: `0f90e0b3538d04df294950dcec75952d7e07f1bb044e73e795c410d677b3c268`
- `n59-float-as-integer-overflow`: `7de1555df0c2700329e815b93b32c571c3ea54dc967b89e81ab73b9972b72d1d`
- `n59-float-as-integer-inexact`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `n59-float-as-integer-nan`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `n60-negative-sqrt-int`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `n60-negative-sqrt-fix`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `n60-float-sqrt-negative`: `58afae218ab41ad99969306e609f6dc2426060b212253dc666bdf69722d12eb6`

The events of `n53-event-e-index-and-tag` (kind, clause, payload; independent of the law seal):

- `A 1 000000004c42000000020100`
- `E 2 0000000000000000000000024201`
- `A 3 000000014c490000000200000000000000050000000000000006`
- `E 4 000000010000000000000002490000000000000007`

## Points of §11 still open

The probes marked *twin* rest on these. Each names the probe that separates the readings.

- **§11 against the body (a contradiction).** §11 does not say that it overrides the text above it, and the body still states the replaced rules: §1 "Any other line is refused with LINE-FORM" and Sealed as "the last non-blank line" (items 3, 4, 5, 8: TITLE-PLACE, SEAL-PLACE, SEAL-FORM, SYNTAX, LEX); §3 "a name may not begin with a statement word" (item 20: any reserved word), `Notwithstanding §a[, §b][ and §c]` (item 23), `[, provided that C][, unless C]` (item 25) and `Set item E of X` (item 27); §4 "can begin an expression" (item 34); §5 "names a rule or a procedure" (item 47: a procedure already defined) and its code list (item 8 says SYNTAX and LEX are added to it; they are not). The twin follows §11 wherever they differ.
- **G3 phases 2, 3 and 4.** Each phase lists several codes after its order ("lines, in order: LINE-FORM, TITLE-PLACE, ..."). Read (a): one pass in that order, the listed codes ordering the checks of one line or clause, so the first faulty line or clause decides; or (b): one pass per code, so a LINE-FORM on line 9 beats a LINE-CHECK on line 1. The twin takes (a). Probes g3-line-order-check, g3-line-order-numbering, g3-unknown-procedure-clause-order, g3-procedure-name-clause-order and g3-shape-tree-order separate them. Phase 4's "tree order" is taken as depth-first pre-order (document order), not breadth-first: probe g3-shape-preorder.
- **G3 phase 3, SYNTAX and LEX in one clause.** Listed SYNTAX before LEX, but a statement holding both an unreadable token and a misplaced one can be read three ways: lexed whole first (LEX always), parsed with a lazy lexer (the first offending position decides), or parsed without the unreadable characters (SYNTAX whenever the parse fails). The twin takes the first offending position. Probes g3-syntax-then-lex and g3-lex-then-syntax separate all three.
- **G3 phase 6, order within one clause.** "Document walk order" does not order two faults of one statement: `Let x be y` with x already declared and y undeclared. The twin checks the expression first (UNDECLARED). Probe g3-let-expression-first.
- **G3, which phase LITERAL-RANGE is in.** Not listed. The twin types literals in phase 6. Probe g3-literal-range-is-static.
- **G3 phase 1 and items 1, 14.** The door's refusals have no codes in SPEC, and a canonical text cannot carry a spaces-only line or a CR, so items 1 and 14 have no probe; the twin assumes canonical input.
- **Item 3, "content".** §1 says a Title comes "before any clause"; §11 says "after content". Is a Note content? Is the Sealed line? The twin counts clause lines and the Sealed line. Probe n03-title-after-note.
- **Items 2 and 5, a line starting "Sealed:" without the space.** "`Sealed: ` is exact" can mean that only "Sealed: " opens a Sealed line (so `Sealed:x` is LINE-FORM, the twin's reading) or that such a line is a malformed Sealed line (SEAL-FORM). Probe n02-sealed-no-space.
- **Items 20 and 21, calls.** PROCEDURE-NAME is given for a definition. A call whose first word is reserved (`If C, do the following; otherwise S`; `Perform the go`) can never name a procedure: SYNTAX (twin), UNKNOWN-PROCEDURE, or PROCEDURE-NAME? Probe n21-call-reserved-first-word.
- **Item 29, Append and Remove.** "Setting, increasing or decreasing ... item forms included" leaves Append and Remove on a counter: TYPE (twin, the counter is not a list) or LOOP-VARIABLE. Probe n29-append-to-counter.
- **Item 47, the converse.** A variable may not take a procedure's name; may a procedure take a visible variable's name? §5's general rule says REDECLARED (twin); item 47 alone says nothing. Probe n47-procedure-after-variable. Also: inside a procedure's own body, is that procedure "already defined"? The twin says no (it is defined when its body ends, as for PERFORM-BEFORE-DEFINITION).
- **Item 48, reads.** "Writing to a rule name is UNDECLARED". Reading a rule name where a list variable is needed (`item 1 of r`, `length of r`) is not a write: UNDECLARED (twin) or TYPE? Probe n48-item-of-rule.

## Notes

- **Item 31 (clear, perhaps unintended).** Agreement targets are "earlier clauses" of any kind (a To, a Define, a claim, an absorbed Otherwise, the same clause twice), while certificate targets exclude those. The twin follows the text. Probes n31-*.
- **Items 53 and 54 (only in the trace).** The trace head depends on the law seal, which the probes leave UNKNOWN. `probe_run.py --seals FILE` reruns with the reference's seals to compare trace heads; the event payloads given for n53-event-e-index-and-tag do not depend on the seal.
- **Items 1, 14, 58, 61, 62, G1, G2.** No probe: a canonical text carries no spaces-only line and no CR (1, 14); 58, 61 and 62 are unobservable; G1 and G2 are about comparing and reporting (every refused probe shows G2: no receipt).
