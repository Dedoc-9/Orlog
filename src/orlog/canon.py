"""The door: raw source bytes -> one canonical text, with a receipt for every change.

Three classes of action, each recorded with its rule, place and bytes:
  REPAIR  the bytes are changed; the rule names why the change cannot alter meaning
          (the grammar reads both forms identically, and output text is never touched)
  NOTE    the bytes are kept, but recorded (an invisible joiner inside a text literal)
  REFUSE  the bytes are not repaired, because no rule can show a repair is safe

The principle: repair what the grammar interprets, preserve what the program outputs,
refuse what neither can vouch for. Canonicalization is meant to be a retraction:
canon(canon(x)) == canon(x) with no repairs. That is DECLARED; the self-test checks it on texts
that needed repairs, and the red team's door fuzz samples it (prosecutor F27: this line had said
"checked by the self-test, not assumed", which no finite check can make true of every input).
"""
import hashlib
import unicodedata

BIDI = set([0x061C, 0x200E, 0x200F]) | set(range(0x202A, 0x202F)) | set(range(0x2066, 0x206A))
INVISIBLE = {0x00AD, 0x180E, 0x200B, 0x2060, 0x2061, 0x2062, 0x2063, 0x2064, 0xFEFF}
JOINERS = {0x200C, 0x200D}
DQUOTES = {0x201C, 0x201D, 0x201E, 0x201F}      # U+2033 DOUBLE PRIME is not a quote (red team E9)
CURLY_CLOSERS = {0x201C, 0x201D, 0x201F}
HANGUL_FILLERS = {0x115F, 0x1160, 0x3164, 0xFFA0}
SQUOTES = {0x2018, 0x2019, 0x201A, 0x201B, 0x2032}
SPACES = {0x00A0, 0x1680, 0x202F, 0x205F, 0x3000} | set(range(0x2000, 0x200B))
CODE_MAP = {  # typographic variants the grammar reads as one ASCII form
    0x2212: ("-", "R-MINUS", "U+2212 MINUS SIGN is the grammar's minus"),
    0x2010: ("-", "R-HYPHEN", "U+2010 HYPHEN is the grammar's minus"),
    0x2011: ("-", "R-HYPHEN", "U+2011 NON-BREAKING HYPHEN is the grammar's minus"),
    0x00D7: ("*", "R-TIMES", "U+00D7 MULTIPLICATION SIGN is the grammar's times"),
    0x00F7: ("/", "R-DIVIDE", "U+00F7 DIVISION SIGN is the grammar's divided by"),
    0x2264: ("<=", "R-LEQ", "U+2264 is the grammar's at most"),
    0x2265: (">=", "R-GEQ", "U+2265 is the grammar's at least"),
    0x2260: ("!=", "R-NEQ", "U+2260 is the grammar's is not"),
}
REFUSE_DASH = {0x2013, 0x2014, 0x2015}


def _hex(s):
    return s.encode("utf-8").hex()


class Canon:
    def __init__(self, raw):
        self.raw = raw
        self.events = []        # dicts: rule, cls, line, col, raw, canon, reason
        self.text = None

    def ev(self, cls, rule, line, col, raw, canon, reason):
        self.events.append({"cls": cls, "rule": rule, "line": line, "col": col,
                            "raw": _hex(raw), "canon": _hex(canon), "reason": reason})

    @property
    def refusals(self):
        return [e for e in self.events if e["cls"] == "REFUSE"]

    @property
    def repairs(self):
        return [e for e in self.events if e["cls"] == "REPAIR"]


def _context_marker(line):
    stripped = line.lstrip(" ")
    for m in ("Note:", "Title:"):
        if stripped.startswith(m):
            return len(line) - len(stripped) + len(m)
    return None


def canonicalize(raw):
    c = Canon(raw)
    data = raw
    if data.startswith(b"\xef\xbb\xbf"):
        c.ev("REPAIR", "R-BOM", 1, 1, "﻿", "", "a leading byte-order mark carries no text")
        data = data[3:]
    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as e:
        c.ev("REFUSE", "BYTES-NOT-UTF8", 0, e.start + 1, "", "",
             "byte %d is not UTF-8; an encoding is never guessed (executable-epistemics E-011, E-016)" % e.start)
        return c
    # line terminators
    lines, i, n, crlf, cr = [], 0, len(text), 0, 0
    cur = []
    while i < n:
        ch = text[i]
        if ch == "\r":
            if i + 1 < n and text[i + 1] == "\n":
                crlf += 1
                i += 1
            else:
                cr += 1
            lines.append("".join(cur))
            cur = []
        elif ch == "\n":
            lines.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
        i += 1
    if cur:
        lines.append("".join(cur))
    if crlf:
        c.ev("REPAIR", "R-CRLF", 0, 0, "\r\n", "\n", "%d CR LF line terminators read as LF" % crlf)
    if cr:
        c.ev("REPAIR", "R-CR", 0, 0, "\r", "\n", "%d lone CR line terminators read as LF" % cr)

    out_lines = []
    for ln, line in enumerate(lines, 1):
        out_lines.append(_scan_line(c, ln, line))
    # leading and trailing blank lines carry nothing
    lead = 0
    while lead < len(out_lines) and out_lines[lead] == "":
        lead += 1
    if lead:
        c.ev("REPAIR", "R-LEADING-BLANK", 1, 1, "\n" * lead, "", "%d leading blank lines" % lead)
    out_lines = out_lines[lead:]
    trail = 0
    while out_lines and out_lines[-1] == "":
        out_lines.pop()
        trail += 1
    if trail:
        c.ev("REPAIR", "R-TRAILING-BLANK", 0, 0, "\n" * trail, "", "%d trailing blank lines" % trail)
    body = "\n".join(out_lines) + "\n" if out_lines else ""
    if raw and not (text.endswith("\n") or text.endswith("\r")) and out_lines:
        c.ev("REPAIR", "R-FINAL-NEWLINE", len(out_lines), 0, "", "\n", "a final line terminator is added")
    c.text = None if c.refusals else body
    return c


def _segments(line):
    """Split a line into (kind, text, first column) by context, before any rewriting.
    kind: 'code', 'lit' (a literal's content, its delimiters belong to code), 'free'."""
    free_from = _context_marker(line)
    segs, buf, kind, start = [], [], "code", 1
    i, n = 0, len(line)

    def flush(next_kind, col):
        nonlocal buf, kind, start
        if buf:
            segs.append((kind, "".join(buf), start))
        buf, kind, start = [], next_kind, col

    opener = None
    while i < n:
        ch = line[i]
        if free_from is not None and i >= free_from and kind != "free":
            flush("free", i + 1)
        if kind == "free":
            buf.append(ch)
        elif kind == "code":
            if ch == '"' or ord(ch) in DQUOTES:
                buf.append(ch)
                opener = ch
                flush("lit", i + 2)
            else:
                buf.append(ch)
        else:  # literal content
            if ch == '"' and i + 1 < n and line[i + 1] == '"':
                buf.append('""')
                i += 2
                continue
            # A literal opened by a straight quote closes only at a straight quote: curly quotes inside it are its
            # text (red team E9: "Use “followed by” to join" had become code). One opened by a curly quote closes at
            # a curly closer or a straight quote.
            closes = ch == '"' or (opener != '"' and ord(ch) in CURLY_CLOSERS)
            if closes:
                flush("code", i + 1)
                buf.append(ch)
            else:
                buf.append(ch)
        i += 1
    unterminated = kind == "lit"
    flush(kind, n + 1)
    return segs, unterminated


def _scan_line(c, ln, line):
    """Rewrite one line by context: code, text literal, or free text (Note:/Title:)."""
    segs, unterminated = _segments(line)
    refused_before = len(c.refusals)
    res = []
    col = 0
    for kind, seg, start in segs:
        if kind == "free":
            # NFC only in free text. In code, NFC would turn U+212A KELVIN SIGN into K and U+037E GREEK QUESTION MARK
            # into ';' (a delimiter) before the ASCII rule could see them (red team E17): code refuses them instead.
            nfc = unicodedata.normalize("NFC", seg)
            if nfc != seg:
                c.ev("REPAIR", "R-NFC", ln, start, seg, nfc,
                     "Unicode canonical equivalence (UAX #15 NFC) in free text")
                seg = nfc
        elif kind == "lit" and unicodedata.normalize("NFC", seg) != seg:     # literals only (red team E26)
            c.ev("NOTE", "LITERAL-NOT-NFC", ln, start, seg, seg,
                 "a text literal is not in NFC; kept byte for byte, because it is output")
        for off, ch in enumerate(seg):
            col = start + off
            _scan_char(c, ln, col, ch, kind, res)
    if unterminated:
        c.ev("REFUSE", "UNTERMINATED-TEXT", ln, col + 1, "", "", "a text literal is not closed on its line")
    s = "".join(res)
    t = s.rstrip(" ")
    if t != s:
        c.ev("REPAIR", "R-TRAILING-SPACE", ln, len(t) + 1, s[len(t):], "", "trailing spaces carry nothing")
    # A repair may never move a literal's boundary. Re-segment the repaired line and compare the literals.
    # (Court finding L12: a curly-opened literal closed by U+201D, then a straight quote, became a doubled-quote
    # escape, so the delimiter turned into output text and a refused program into an accepted one.)
    # A line already refused is not compared: its refused characters are not in the repaired line, so the literals
    # would differ with no quote involved, and the event would say what did not happen (twin round 2, E19's line).
    if QUOTE_BOUNDARY_CHECK and not unterminated and len(c.refusals) == refused_before:
        before = [seg for kind, seg, _ in segs if kind == "lit"]
        after = [seg for kind, seg, _ in _segments(t)[0] if kind == "lit"]
        if before != after:
            c.ev("REFUSE", "QUOTE-BOUNDARY", ln, 1, line, t,
                 "repairing a typographic quote here would move a text literal's boundary "
                 "(%d literal(s) before the repair, %d after); write straight quotes" % (len(before), len(after)))
    return t


QUOTE_BOUNDARY_CHECK = True


def _scan_char(c, ln, col, ch, kind, res):
    cp = ord(ch)
    if cp in BIDI:
        c.ev("REFUSE", "BIDI-CONTROL", ln, col, ch, "",
             "%s can reorder what a reader sees (Trojan Source, CVE-2021-42574)" % _name(ch))
        return
    if (cp < 0x20 and ch != "\t") or cp == 0x7F or 0x80 <= cp <= 0x9F:
        c.ev("REFUSE", "CONTROL-CHAR", ln, col, ch, "", "control character U+%04X" % cp)
        return
    if kind == "free":
        cat = unicodedata.category(ch)
        if cat in ("Zl", "Zp"):
            c.ev("REFUSE", "CONTROL-CHAR", ln, col, ch, "", "%s would break a line" % _name(ch))
        elif cp in INVISIBLE or cp in HANGUL_FILLERS or (cat == "Cf" and cp not in JOINERS):
            c.ev("REFUSE", "INVISIBLE-CHAR", ln, col, ch, "", "%s is invisible" % _name(ch))
        elif cp in JOINERS:
            c.ev("NOTE", "JOINER-IN-FREE-TEXT", ln, col, ch, ch, "%s kept" % _name(ch))
            res.append(ch)
        elif cp in SPACES or ch == "\t":
            c.ev("REPAIR", "R-SPACE", ln, col, ch, " ", "%s in free text read as a space" % _name(ch))
            res.append(" ")
        else:
            res.append(ch)
        return
    if kind == "lit":      # a literal's content: output text, preserved byte for byte
        cat = unicodedata.category(ch)
        if ch == "\t":
            c.ev("REFUSE", "CONTROL-CHAR", ln, col, ch, "", "a tab inside a text literal would be output")
        elif cat in ("Zl", "Zp"):
            c.ev("REFUSE", "CONTROL-CHAR", ln, col, ch, "",
                 "%s would break a line inside a text literal (red team E19)" % _name(ch))
        elif cp in INVISIBLE or cp in HANGUL_FILLERS or (cat == "Cf" and cp not in JOINERS):
            c.ev("REFUSE", "INVISIBLE-CHAR", ln, col, ch, "",
                 "%s inside a text literal would be output unseen (format characters, tags and fillers: red team "
                 "E19)" % _name(ch))
        elif cp in JOINERS:
            c.ev("NOTE", "JOINER-IN-LITERAL", ln, col, ch, ch, "%s kept: it is output text" % _name(ch))
            res.append(ch)
        else:
            res.append(ch)
        return
    # code context (a literal's delimiters belong here)
    if ch == '"' or cp in DQUOTES:
        if ch != '"':
            c.ev("REPAIR", "R-QUOTE-DELIM", ln, col, ch, '"',
                 "%s delimits a text literal; the grammar reads it as \"" % _name(ch))
        res.append('"')
    elif cp in SQUOTES:
        c.ev("REPAIR", "R-APOSTROPHE", ln, col, ch, "'", "%s in code read as '" % _name(ch))
        res.append("'")
    elif cp in SPACES or ch == "\t":
        c.ev("REPAIR", "R-SPACE", ln, col, ch, " ", "%s in code read as a space" % _name(ch))
        res.append(" ")
    elif cp in CODE_MAP:
        rep, rule, why = CODE_MAP[cp]
        c.ev("REPAIR", rule, ln, col, ch, rep, why)
        res.append(rep)
    elif cp in REFUSE_DASH:
        c.ev("REFUSE", "DASH-AMBIGUOUS", ln, col, ch, "",
             "%s could mean minus, a range or punctuation; write - or words" % _name(ch))
    elif cp in INVISIBLE or cp in JOINERS:
        c.ev("REFUSE", "INVISIBLE-CHAR", ln, col, ch, "", "%s is invisible in code" % _name(ch))
    elif cp < 0x80 or ch == "§":
        res.append(ch)
    else:
        c.ev("REFUSE", "NON-ASCII-CODE", ln, col, ch, "",
             "%s in code: identifiers and keywords are ASCII (UTS #39 confusables are refused, not guessed)"
             % _name(ch))


def _name(ch):
    return "U+%04X %s" % (ord(ch), unicodedata.name(ch, "UNNAMED"))


def sha256_hex(b):
    return hashlib.sha256(b).hexdigest()
