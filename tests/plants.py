"""Plants made in memory: a copy of a module with exact edits, loaded fresh, so that a plant changes nothing on disk
and nothing another row reads. The reporting pass planted this way (research/reporting-pass/reproducers/_common.py),
and its findings 1 to 5, 9 and 15 to 18 were predicates inside a function, which no module switch can reach.
"""
import os
import types

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def planted(rel, edits):
    """rel: a file of the repository (src/orlog/court.py, orl.py). edits: [(old, new)]; each old must occur exactly
    once, or the plant is refused: a plant whose text moved is no plant. A module of the orlog package keeps its
    relative imports; orl.py keeps its own path, so its ROOT is the repository's."""
    path = os.path.join(ROOT, rel)
    with open(path, "rb") as fh:
        text = fh.read().decode("utf-8")
    for old, new in edits:
        n = text.count(old)
        if n != 1:
            raise AssertionError("plant on %s: its text occurs %d times, not once: %r" % (rel, n, old[:80]))
        text = text.replace(old, new)
    name = os.path.splitext(os.path.basename(rel))[0]
    in_package = rel.replace("\\", "/").startswith("src/orlog/")
    mod = types.ModuleType(("orlog._planted_" if in_package else "_planted_") + name)
    if in_package:
        import orlog  # noqa: F401  (the package, so that the copy's relative imports resolve)
        mod.__package__ = "orlog"
    mod.__file__ = path
    exec(compile(text, path + " (planted)", "exec"), mod.__dict__)
    return mod
