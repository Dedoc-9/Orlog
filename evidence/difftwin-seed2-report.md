# Reference against twin: differential run

Seed 2; 20353 texts (353 seeds and their mutants); sources key 5f5b5835a6a85fe7.

- both refused, with the same code: 19282
- both ran, receipts and output byte-identical: 1023
- disagree: 48, in 6 signatures
- mutants the door refused (not compared; the twin has no door): 0

## COMPILE ref=EXPRESSION-DEPTH twin=SYNTAX (24)

```
§1 Say ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( (.
```

## COMPILE ref=RUN twin=EXPRESSION-DEPTH (11)

```
1. Say (1) plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1.
```

## COMPILE ref=TYPE twin=UNDECLARED (10)

```
1. Say a list of 1.5 copies of y.
```

## COMPILE ref=LITERAL-RANGE twin=EXPRESSION-DEPTH (1)

```
§1 Say ( 1 ) plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 9223372036854775808 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1.
```

## COMPILE ref=UNDECLARED twin=EXPRESSION-DEPTH (1)

```
§1 Say ( 1 ) plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus Forward plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1.
```

## TIMEOUT (1)

```
Title: Counting Domino Tilings of the Aztec Diamond.
Note: A brute-force enumeration (depth-first, with an explicit stack) checked against a closed form proven by others: 2^(n(n+1)/2) tilings for order n (Elkies, Kuperberg, Larsen and Propp 1992).
Note: The two are different representations, so their agreement is evidence the enumeration counts the right region; the theorem is cited here, not ratified. The Aztec diamond appears only as an oracle source: Semiotic core TRIAGE rules it DECORATIVE as an integrity filter.
§1 For each n from 1 to 4, do the following.
§1.1 Let w be 2 times n.
§1.2 Let cells be w times w.
§1.3 Let valid be a list of cells copies of false.
§1.4 For each r from 0 to w minus 1, do the following.
§1.4.1 Let half be the smaller of r plus 1 and w minus r.
§1.4.2 For each col from n minus half to n plus half minus 1, do the following.
§1.4.2.1 Set item (r times w plus col plus 1) of valid to true.
§1.5 Let filled be a list of cells copies of false.
§1.6 Let placed be a list of 0 copies of 0.
§1.7 Let dirs be a list of 0 copies of 0.
§1.8 Let count be 0.
§1.9 Let pos be 1.
§1.10 Let mode be 1.
§1.11 While mode is not 0, at most 10000000 times, do the following.
§1.11.1 If mode is 1, do the following.
§1.11.1.1 While pos is at most cells and (not item pos of valid or item pos of filled), at most 1000 times, do the following.
§1.11.1.1.1 Increase pos by 1.
§1.11.1.2 If pos is greater than cells, do the following.
§1.11.1.2.1 Increase count by 1.
§1.11.1.2.2 Set mode to 2.
§1.11.1.3 Otherwise, if the remainder of pos minus 1 by w is less than w minus 1 and item (pos plus 1) of valid and not item (pos plus 1) of filled, do the following.
§1.11.1.3.1 Set item pos of filled to true.
§1.11.1.3.2 Set item (pos plus 1) of filled to true.
§1.11.1.3.3 Append pos to placed.
§1.11.1.3.4 Append 1 to dirs.
§1.11.1.4 Otherwise, if pos plus w is at most cells and item (pos plus w) of valid and not item (pos plus w) of filled, do the following.
§1.11.1.4.1 Set item pos of filled to true.
§1.11.1.4.2 Set item (pos plus w) of filled to true.
§1.11.1.4.3 Append pos to placed.
1.11.1.4.4. Append 2 to dirs.
§1.11.2 Otherwise, if the length of placed is 0, set mode to 0.
§1.11.3 Otherwise, do the following.
§1.11.3.1 Let top be the length of placed.
§1.11.3.2 Let cell be item top of placed.
§1.11.3.3 Let dir be item top of dirs.
§1.11.3.4 Remove the last item of placed.
§1.11.3.5 Remove the last item of dirs.
§1.11.3.6 Set item cell of filled to false.
§1.11.3.7 If dir is 1, set item (cell plus 1) of filled to false; otherwise set item (cell plus w) of filled to false.
§1.11.3.8 If dir is 1 and cell plus w is at most cells and item (cell plus w) of valid and not item (cell plus w) of filled, do the following.
§1.11.3.8.1 Set item cell of filled to true.
§1.11.3.8.2 Set item (cell plus w) of filled to true.
§1.11.3.8.3 Append cell to placed.
§1.11.3.8.4 Append 2 to dirs.
§1.11.3.8.5 Set pos to cell.
§1.11.3.8.6 Set mode to 1.
§1.12 Let expected be 1.
§1.13 For each j from 1 to n times (n plus 1) divided by 2, do the following.
§1.13.1 Set expected to expected times 2.
§1.14 Say "order " followed by n followed by ": " followed by count followed by " tilings".
§1.15 We claim that count equals expected, by the theorem "Elkies, Kuperberg, Larsen and Propp 1992: the Aztec diamond of order n has 2^(n(n+1)/2) domino tilings".
```

