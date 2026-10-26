"""Depth probes after the NESTING-DEPTH repair: expression nesting, alone and inside the deepest allowed clause nest.

  python -B mkdeep2.py      (writes E24 and E25 reproducers into this folder)
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
S = "§"


def right_and(n):
    """true and (true and (... true)): each 'and' nests its right operand's code inside an if-block."""
    e = "true"
    for _ in range(n):
        e = "true and (%s)" % e
    return e


def deep_loops_with_expr(loops, ands):
    lines, label = [], []
    for d in range(loops):
        label.append("1")
        lines.append("%s%s For each i%d from 1 to 1, do the following." % (S, ".".join(label), d))
    label.append("1")
    lines.append("%s%s Say %s." % (S, ".".join(label), right_and(ands)))
    return "\n".join(lines) + "\n"


def write(name, text):
    with open(os.path.join(HERE, name), "wb") as fh:
        fh.write(text.encode("utf-8"))
    print("wrote", name)


if __name__ == "__main__":
    write("E24_python_depth_and_inside_loops.orl", deep_loops_with_expr(16, 70))
    write("E24b_and_inside_loops_ok.orl", deep_loops_with_expr(16, 50))
    write("E25_parser_recursion_parens.orl", "%s1 Say %s1%s.\n" % (S, "(" * 120, ")" * 120))
    write("E25b_parser_recursion_and.orl", "%s1 Say %s.\n" % (S, right_and(100)))
