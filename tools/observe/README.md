# Observe: the founding slice

The question this starts on: how do I know new code does not break old code?

A law takes no input today, so one run is its whole behaviour, and comparing two runs is exact. `observe.py` compiles two texts, runs each on the reference, and reports the law, the status and the output apart. It also prints the lines of the law and of the output that differ, and says whether the status's class and refusal code are the same. It has no new syntax and changes nothing in `src/`.

```
python -B tools/observe/observe.py OLD.orl NEW.orl
python -B tools/observe/observe.py --selftest
```

## What it decides: nothing

For closed laws the owner has ruled exact output plus status (`RULINGS.md`). The tool still only reports, with prefix and subsequence shown for reference: it does not print the full seal, no authorization record exists, and nothing fails on a break, so its report is input to a person's judgment.

## What it does not show

- It runs two texts. It is not yet part of compiling.
- It does not reach open programs. Once ports exist, one run is no longer the whole behaviour, and this comparison stops being exact.
- It authorizes nothing. A change to protected observations needs a person's authorization bound to the full law seal, and no tool can grant that.
- It is one author's tool, checked by hand-worked cases and one plant. No gate row holds it.

## Next, in order, each needing the owner's word

1. Decide on the next piece: printing the full seal, then the smallest authorization record.
2. Decide whether the printer audit is authorized. That is separate work on LAU-1, and neither waits on the other.
3. Decide whether this comparison belongs in compiling, and what happens to text that declares no observation.
