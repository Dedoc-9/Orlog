"""Count words in a Markdown file: whitespace tokens holding at least one letter or digit.

Usage: python -I -X utf8 wordcount.py FILE.md
Prints the total, the total without the Sources section, and the plain whitespace count.
"""
import re
import sys

text = open(sys.argv[1], encoding="utf-8").read()
tokens = text.split()
words = [t for t in tokens if re.search(r"[0-9A-Za-zÀ-ɏ]", t)]
body = text.split("## Sources")[0]
body_words = [t for t in body.split() if re.search(r"[0-9A-Za-zÀ-ɏ]", t)]
print("words (alnum tokens):", len(words))
print("words without Sources:", len(body_words))
print("whitespace tokens:", len(tokens))
