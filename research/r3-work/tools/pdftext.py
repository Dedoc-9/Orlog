"""Crude PDF text extraction with the standard library only.

Decompresses FlateDecode streams and pulls string operands of Tj/TJ/'/" text
operators. Good enough to search for phrases; not a faithful renderer.
Usage: python -I pdftext.py FILE.pdf [OUT.txt]
"""
import re
import sys
import zlib


def streams(data):
    for m in re.finditer(rb"stream\r?\n", data):
        start = m.end()
        end = data.find(b"endstream", start)
        if end < 0:
            continue
        raw = data[start:end]
        for cut in (raw, raw.rstrip(b"\r\n")):
            try:
                yield zlib.decompress(cut)
                break
            except Exception:
                try:
                    d = zlib.decompressobj()
                    out = d.decompress(cut)
                    if out:
                        yield out
                        break
                except Exception:
                    pass


def unescape(s):
    out = bytearray()
    i = 0
    while i < len(s):
        c = s[i]
        if c == 0x5C and i + 1 < len(s):  # backslash
            n = s[i + 1]
            mapping = {0x6E: 10, 0x72: 13, 0x74: 9, 0x62: 8, 0x66: 12,
                       0x28: 0x28, 0x29: 0x29, 0x5C: 0x5C}
            if n in mapping:
                out.append(mapping[n])
                i += 2
                continue
            if 0x30 <= n <= 0x37:
                j = i + 1
                k = j
                while k < len(s) and k < j + 3 and 0x30 <= s[k] <= 0x37:
                    k += 1
                out.append(int(s[j:k], 8) & 0xFF)
                i = k
                continue
            i += 2
            continue
        out.append(c)
        i += 1
    return bytes(out)


def text_of(content):
    parts = []
    # TJ arrays and Tj strings
    for m in re.finditer(rb"\[(.*?)\]\s*TJ|\((.*?)(?<!\\)\)\s*Tj|(T\*|Td|TD|Tm|ET)", content, re.S):
        if m.group(1) is not None:
            arr = m.group(1)
            chunk = []
            for sm in re.finditer(rb"\((.*?)(?<!\\)\)|(-?\d+\.?\d*)", arr, re.S):
                if sm.group(1) is not None:
                    chunk.append(unescape(sm.group(1)))
                else:
                    try:
                        if float(sm.group(2)) < -200:
                            chunk.append(b" ")
                    except ValueError:
                        pass
            parts.append(b"".join(chunk))
        elif m.group(2) is not None:
            parts.append(unescape(m.group(2)))
        else:
            parts.append(b"\n" if m.group(3) in (b"ET", b"T*", b"Td", b"TD", b"Tm") else b"")
    return b"".join(parts)


def main():
    path = sys.argv[1]
    with open(path, "rb") as f:
        data = f.read()
    texts = []
    for s in streams(data):
        if b"Tj" in s or b"TJ" in s:
            texts.append(text_of(s))
    out = b"\n".join(texts).decode("latin-1")
    if len(sys.argv) > 2:
        with open(sys.argv[2], "w", encoding="utf-8") as f:
            f.write(out)
    else:
        sys.stdout.write(out)


if __name__ == "__main__":
    main()
