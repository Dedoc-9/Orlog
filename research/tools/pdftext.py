"""Crude standard-library PDF text extractor for searching (not faithful layout).

Usage: python -I pdftext.py FILE.pdf [N_CHARS]
Decompresses FlateDecode streams and joins literal strings found in TJ/Tj operators.
"""
import re
import sys
import zlib


def literal_strings(data):
    out = []
    i = 0
    n = len(data)
    while i < n:
        c = data[i]
        if c == 0x28:  # '('
            depth = 1
            i += 1
            buf = bytearray()
            while i < n and depth > 0:
                c = data[i]
                if c == 0x5C:  # backslash
                    i += 1
                    if i < n:
                        e = data[i]
                        if e in b"nrtbf":
                            buf.append({110: 10, 114: 13, 116: 9, 98: 8, 102: 12}[e])
                        elif 0x30 <= e <= 0x37:
                            j = i
                            v = 0
                            while j < n and j < i + 3 and 0x30 <= data[j] <= 0x37:
                                v = v * 8 + (data[j] - 0x30)
                                j += 1
                            buf.append(v & 0xFF)
                            i = j - 1
                        else:
                            buf.append(e)
                elif c == 0x28:
                    depth += 1
                    buf.append(c)
                elif c == 0x29:
                    depth -= 1
                    if depth > 0:
                        buf.append(c)
                else:
                    buf.append(c)
                i += 1
            out.append(bytes(buf))
        elif c == 0x54 and i + 1 < n and data[i + 1] in (0x2A,):  # T* newline
            out.append(b"\n")
            i += 1
        elif c == 0x45 and i + 1 < n and data[i + 1] == 0x54:  # ET end text
            out.append(b"\n")
            i += 2
        elif c == 0x5D:  # ']' end of TJ array: maybe a space
            i += 1
        else:
            # big negative kerning inside TJ often means a space
            m = re.match(rb"-(\d{3,})", data[i:i + 8])
            if m and int(m.group(1)) >= 200:
                out.append(b" ")
                i += len(m.group(0))
                continue
            i += 1
    return b"".join(out)


def main():
    path = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
    raw = open(path, "rb").read()
    texts = []
    for m in re.finditer(rb"stream\r?\n", raw):
        start = m.end()
        end = raw.find(b"endstream", start)
        if end < 0:
            continue
        chunk = raw[start:end]
        try:
            dec = zlib.decompress(chunk)
        except Exception:
            try:
                dec = zlib.decompressobj().decompress(chunk)
            except Exception:
                continue
        if b"TJ" in dec or b"Tj" in dec:
            texts.append(literal_strings(dec))
    text = b"\n".join(texts).decode("latin-1", errors="replace")
    sys.stdout.write(text[:limit])


if __name__ == "__main__":
    main()
