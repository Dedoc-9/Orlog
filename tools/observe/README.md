# Observe: the founding slice

The question this starts on: how do I know new code does not break old code?

A law takes no input today, so one run is its whole behaviour, and comparing two runs is exact. `observe.py` compiles two texts, runs each on the reference, and reports the law, the status and the output apart. It also prints the lines of the law and of the output that differ, and says whether the status is the same. It has no new syntax and changes nothing in `src/`.

```
python -B tools/observe/observe.py OLD.orl NEW.orl
python -B tools/observe/observe.py --selftest
```

## What it decides: nothing

The preservation relation is OPEN by the owner's ruling, so the tool reports exact, prefix and subsequence side by side and calls none of them the verdict. "Same status" is a fact about two strings and decides nothing either: a refusal's string includes where it happened, so a clause that only moved reads as a different status. A relation is his to choose, and choosing one makes this tool a check.

## What it does not show

- It runs two texts. It is not yet part of compiling.
- It does not reach open programs. Once ports exist, one run is no longer the whole behaviour, and this comparison stops being exact.
- It authorizes nothing. A change to protected observations needs a person's authorization bound to the full law seal, and no tool can grant that.
- It is one author's tool, checked by hand-worked cases and one plant. No gate row holds it.

## Next, in order, each needing the owner's word

1. Rule on the preservation relation, at least for closed laws.
2. Decide whether the printer audit is authorized. That is separate work on LAU-1, and neither waits on the other.
3. Only then decide whether this comparison belongs in compiling, and what happens to text that declares no observation.
