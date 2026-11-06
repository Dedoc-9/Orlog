"""RUST-CORE-0: worked examples for LAW-FORMAT-0's appendix A (REREAD-1 finding G16), produced by the reference.

Run from the repository's root: PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/rust-core/gen_worked.py

For each text it writes, as data (like the vectors):
- the law bytes and the text seal;
- the reference's receipt, with its backend line `reference`, and its trace;
- the seal words.
The core's receipt differs from these only in its backend line, `backend rust-core`. The output is
research/rust-core/worked-examples.md, with its provenance. It is pasted into the draft's appendix A."""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "src"))
from orlog import interp                  # noqa: E402
from orlog.front import compile_bytes     # noqa: E402
from orlog.seal import seal_words         # noqa: E402

S = "§"
TEXTS = [
    ("the empty law", ""),
    ("a let and a say", "%s1 Let x be 2.\n%s2 Say x plus 3.\n" % (S, S)),
    ("a refusal", "%s1 Say 1.\n%s2 Say 1 divided by 0.\n" % (S, S)),
    ("a cost counter read inside and after its clause (REREAD-1 C8)",
     "%s1 Let n be 0.\n%s2 While n < 2, at most 5 times, do the following.\n%s2.1 Increase n by 1.\n"
     "%s2.2 We claim that true, by the certificate of %s2.\n%s3 We claim that true, by the certificate of %s2.\n"
     % (S, S, S, S, S, S, S)),
]


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    out = ["Produced by `research/rust-core/gen_worked.py` (sha256 %s) from the reference at `2e9805a`:"
           % sha(os.path.abspath(__file__)),
           "`src/orlog/interp.py` sha256 %s, `src/orlog/numeric_ref.py` sha256 %s. Data, as the vectors are."
           % (sha(os.path.join(ROOT, "src", "orlog", "interp.py")), sha(os.path.join(ROOT, "src", "orlog", "numeric_ref.py"))),
           ""]
    for i, (name, text) in enumerate(TEXTS, 1):
        c = compile_bytes(text.encode("utf-8"))
        assert c.ok, name
        it = interp.Interp(c.prog, c.an, c.law_seal, c.text_seal, trace=True).run()
        out.append("**A.%d, %s.**" % (i, name))
        out.append("")
        out.append("The law bytes:")
        out.append("```")
        out.append(c.law.decode("ascii").rstrip("\n"))
        out.append("```")
        out.append("TEXTSEAL `%s`; the law seal `%s`; the seal words `%s`." % (c.text_seal, c.law_seal, seal_words(c.law_seal)))
        out.append("")
        out.append("The reference's receipt (the core's differs in its backend line only):")
        out.append("```")
        out.append(it.receipt("reference").decode("ascii").rstrip("\n"))
        out.append("```")
        out.append("Its trace (%d events)%s" % (len(it.trace), ":" if it.trace else ": empty."))
        if it.trace:
            out.append("```")
            out.extend(it.trace)
            out.append("```")
        out.append("")
    text = "\n".join(out) + "\n"
    with open(os.path.join(HERE, "worked-examples.md"), "wb") as f:
        f.write(text.encode("utf-8"))
    print(text)


if __name__ == "__main__":
    main()
