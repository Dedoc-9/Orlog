import sys

# Insert a blank line between two consecutive non-empty prose lines, so each
# statement / bearing / tag line renders as its own paragraph. List items and
# headings are left as they are.
path = sys.argv[1]
with open(path, encoding="utf-8", newline="") as f:
    lines = f.read().split("\n")


def prose(s):
    t = s.strip()
    if not t or t.startswith("#") or t.startswith("- "):
        return False
    if len(t) > 2 and t[0].isdigit() and t[1] == ".":
        return False
    return True


out = []
for i, line in enumerate(lines):
    out.append(line)
    if i + 1 < len(lines) and prose(line) and prose(lines[i + 1]):
        out.append("")
with open(path, "w", encoding="utf-8", newline="") as f:
    f.write("\n".join(out))
print(len(lines), "->", len(out))
