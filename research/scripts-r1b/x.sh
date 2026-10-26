#!/bin/sh
# usage: x.sh NAME SAVED_FILE_BASENAME
# copies a WebFetch-saved PDF into its own folder under dl-r1b/NAME and extracts its text with pdftotext
S=/c/Users/DILLB_~1/AppData/Local/Temp/claude/C--Users-dillb-lzxy763-Desktop-Verdandi/c3c597f5-fd74-40a1-bfa3-a31b0538ea72/scratchpad/orlog/research
T=/c/Users/dillb_lzxy763/.claude/projects/C--Users-dillb-lzxy763-Desktop-Verdandi/c3c597f5-fd74-40a1-bfa3-a31b0538ea72/tool-results
D=$S/dl-r1b/$1
mkdir -p "$D"
cp "$T/$2" "$D/$1.pdf"
pdftotext -enc UTF-8 "$D/$1.pdf" "$D/$1.txt"
echo "$1: $(wc -w < "$D/$1.txt") words -> $D/$1.txt"
