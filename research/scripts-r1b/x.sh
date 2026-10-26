#!/bin/sh
# usage: x.sh NAME SAVED_FILE
# copies a fetched PDF (SAVED_FILE, a path) into its own folder under research/dl-r1b/NAME, which git ignores, and
# extracts its text with pdftotext. (It first named a session scratch folder and a tool-results folder by absolute
# path; prosecutor F36 found both dead after the move into this repository.)
S=$(cd "$(dirname "$0")/.." && pwd)
D=$S/dl-r1b/$1
mkdir -p "$D"
cp "$2" "$D/$1.pdf"
pdftotext -enc UTF-8 "$D/$1.pdf" "$D/$1.txt"
echo "$1: $(wc -w < "$D/$1.txt") words -> $D/$1.txt"
