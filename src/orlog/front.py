"""The front end, end to end: raw bytes -> canonical text -> clause tree -> typed law -> seals."""
import hashlib

from .canon import canonicalize
from .sema import Analysis, law_bytes
from .seal import seal_words
from .syntax import OrlogError, parse_program


class Compiled:
    """Everything a run, a backend and a receipt need, computed once."""

    def __init__(self, raw):
        self.raw = raw
        self.raw_seal = hashlib.sha256(raw).hexdigest()
        self.canon = canonicalize(raw)
        self.error = None
        if self.canon.text is None:
            first = self.canon.refusals[0]
            self.error = OrlogError(first["rule"], first["line"], first["reason"])
            return
        self.text = self.canon.text
        self.text_seal = hashlib.sha256(self.text.encode("utf-8")).hexdigest()
        try:
            self.prog = parse_program(self.text)
            self.an = Analysis(self.prog).run()
            self.law = law_bytes(self.prog, self.an)
            self.law_seal = hashlib.sha256(self.law).hexdigest()
            self.seal_words = seal_words(self.law_seal)
            if self.prog.seal is not None and self.prog.seal[0] != self.seal_words:
                raise OrlogError("SEAL-MISMATCH", self.prog.seal[1],
                                 "the law was sealed %s but now reads %s: it changed after it was sealed"
                                 % (self.prog.seal[0], self.seal_words))
        except OrlogError as e:
            self.error = e

    @property
    def ok(self):
        return self.error is None


def compile_bytes(raw):
    return Compiled(raw)
