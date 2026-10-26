"""A random generator of valid OL-0 programs, for differential testing (reference vs backends).

Programs use Int, Fix and Float (with promotions and conversions), Bool, Text and lists, rules with provisos and
notwithstanding, procedures, If/Otherwise chains (inline and block), Unless, While (bounded), For, claims (with
every oracle kind), musts, Append/Remove/Set item, and text concatenation. Every name is fresh, so there is no
shadowing; every rule is used only after its last Define; every procedure only after its definition.
"""
import os
import random

AVOID = os.environ.get("FUZZ_AVOID", "1") == "1"   # steer clear of the front-end crashes already found

INT_EDGE = ["9223372036854775807", "4611686018427387904", "2147483647", "2147483648", "4294967296",
            "3037000499", "3037000500", "9007199254740993", "9007199254740992", "1000000007"]
FIX_LIT = ["0.5", "1.25", "0.1", "3.14159", "2.5", "1.5", "0.75", "100.0", "0.0000000002", "0.00000000023283064365386962890625",
           "2147483647.5", "65536.0", "46340.95", "0.333", "7.0", "1.0", "0.0", "12.125", "1000.001"]
FLT_LIT = ["0.5", "0.1", "1.5", "2.5", "3.0", "0.2", "1.0", "0.0", "123456789.123", "1000000000000000000000.0",
           "0.000000000000000000000000000000001", "9007199254740993.0", "4503599627370496.5", "0.3",
           str(int(1.7976931348623157e308)) + ".0",
           "0." + "0" * 307 + "1", "0." + "0" * 320 + "5", "2.2250738585072014"]
WORDS = ["alpha", "beta", "gamma", "delta", "omega", "kappa", "sigma", "theta"]
NUM = ("int", "fix", "float")


class Gen:
    def __init__(self, seed, size=None):
        self.r = random.Random(seed)
        self.seed = seed
        self.mode = self.r.choice(["fixed", "floats"])
        self.D = "fix" if self.mode == "fixed" else "float"
        self.n = 0
        self.lines = []           # (label tuple, text)
        self.kinds = []           # (label, kind) for executed clause candidates (certificate targets)
        self.claim_labels = []
        self.scopes = [{}]        # name -> (type, readonly)
        self.rules = {}           # name -> type (usable)
        self.procs = []           # usable procedure names
        self.in_proc = False
        self.size = size or self.r.randint(6, 22)
        self.safe = self.r.random() < 0.75
        self.no_rules = False

    # ------------------------------------------------ names and scopes
    def fresh(self, prefix="v"):
        self.n += 1
        return "%s%d" % (prefix, self.n)

    def visible(self, pred=lambda t: True, writable=False):
        out = []
        for s in self.scopes:
            for name, (t, ro) in s.items():
                if pred(t) and not (writable and ro):
                    out.append((name, t))
        return out

    def declare(self, name, t, ro=False):
        self.scopes[-1][name] = (t, ro)

    # ------------------------------------------------ literals
    def lit(self, t):
        r = self.r
        if t == "int":
            x = r.random()
            if x < 0.75:
                return str(r.randint(0, 20))
            if x < 0.85 and not self.safe:
                return r.choice(INT_EDGE)
            return str(r.randint(0, 100000))
        if t == "fix":
            if self.mode == "fixed":
                return r.choice(FIX_LIT[:12] if self.safe else FIX_LIT)
            return "(%s as a fixed)" % self.lit("int")
        if t == "float":
            if self.mode == "floats":
                return r.choice(FLT_LIT[:8] if self.safe else FLT_LIT)
            return "(%s as a float)" % self.lit("int")
        if t == "bool":
            return r.choice(["true", "false"])
        if t == "text":
            return '"%s"' % r.choice(["a", "x y", "", "say \"\"hi\"\"", "æøå", "1.5", "Z"])
        raise ValueError(t)

    # ------------------------------------------------ expressions
    def expr(self, t, d):
        r = self.r
        if isinstance(t, tuple):
            return self.list_expr(t, d)
        cands = self.visible(lambda u: u == t)
        rules = [n for n, u in self.rules.items() if u == t] if not self.no_rules else []
        if d <= 0 or r.random() < 0.25:
            pick = r.random()
            if cands and pick < 0.55:
                return r.choice(cands)[0]
            if rules and pick < 0.7:
                return r.choice(rules)
            return self.lit(t)
        if t in NUM:
            return self.num_expr(t, d)
        if t == "bool":
            return self.bool_expr(d)
        if t == "text":
            return self.text_expr(d)
        raise ValueError(t)

    def operand(self, t, d):
        """An operand of a t-typed arithmetic op: t itself, or an Int to be promoted."""
        if t != "int" and self.r.random() < 0.3:
            return self.expr("int", d)
        return self.expr(t, d)

    def num_expr(self, t, d):
        r = self.r
        k = r.random()
        lists = self.visible(lambda u: u == ("list", t))
        if lists and k < 0.08:
            name = r.choice(lists)[0]
            idx = r.choice(["1", "(the length of %s)" % name, "(%s)" % self.expr("int", d - 1)])
            return "(item %s of %s)" % (idx, name)
        if k < 0.5:
            a, b = self.expr(t, d - 1), self.operand(t, d - 1)
            if r.random() < 0.5:
                a, b = b, a
            if t == "int" and self.safe and r.random() < 0.5:
                b = str(r.randint(1, 9))
            forms = ["(%s plus %s)", "(%s + %s)", "(%s minus %s)", "(%s - %s)", "(%s times %s)", "(%s * %s)",
                     "the sum of %s and %s", "the product of %s and %s", "the larger of %s and %s",
                     "the smaller of %s and %s"]
            if t != "int" or not self.safe or r.random() < 0.15:
                forms += ["(%s divided by %s)", "(%s / %s)"]
            if t == "int":
                forms += ["the quotient of %s by %s", "the remainder of %s by %s", "(%s modulo %s)"]
            return r.choice(forms) % (a, b)
        if k < 0.65:
            a = self.expr(t, d - 1)
            forms = ["(-%s)", "the negation of %s", "the absolute value of %s", "the square root of %s"]
            if self.safe and t == "int":
                forms = forms[:3] + ["the square root of (the absolute value of %s)"]
            return r.choice(forms) % (a if a.startswith("(") or a[0].isalnum() and " " not in a else "(%s)" % a)
        if k < 0.85:
            return self.conversion(t, d)
        if t == "int":
            lists = self.visible(lambda u: isinstance(u, tuple))
            if lists and r.random() < 0.5:
                return "(the length of %s)" % r.choice(lists)[0]
        return self.expr(t, d - 1)

    def conversion(self, t, d):
        r = self.r
        if t == "int":
            src = r.choice(["fix", "float"])
            a = self.expr(src, d - 1)
            forms = ["(%s rounded to an integer)", "the integer part of %s"]
            if not self.safe or r.random() < 0.2:
                forms.append("(%s as an integer)")
            return r.choice(forms) % self.paren(a)
        if t == "fix":
            src = r.choice(["int", "float"])
            a = self.expr(src, d - 1)
            forms = ["(%s rounded to a fixed)"]
            if src == "int" or not self.safe or r.random() < 0.3:
                forms.append("(%s as a fixed)")
            return r.choice(forms) % self.paren(a)
        src = r.choice(["int", "fix"])
        a = self.expr(src, d - 1)
        forms = ["(%s rounded to a float)"]
        if src == "int" or not self.safe or r.random() < 0.3:
            forms.append("(%s as a float)")
        return r.choice(forms) % self.paren(a)

    def atom(self, t):
        cands = self.visible(lambda u: u == t)
        rules = [n for n, u in self.rules.items() if u == t] if not self.no_rules else []
        k = self.r.random()
        if cands and k < 0.5:
            return self.r.choice(cands)[0]
        if rules and k < 0.6:
            return self.r.choice(rules)
        return self.lit(t)

    def paren(self, a):
        if a.startswith("(") and a.endswith(")"):
            return a
        return "(%s)" % a

    def bool_expr(self, d):
        r = self.r
        k = r.random()
        if k < 0.45:
            t = r.choice(NUM)
            a = self.expr(t, d - 1)
            b = self.operand(t, d - 1) if r.random() < 0.8 else self.expr(t, d - 1)
            if r.random() < 0.5:
                a, b = b, a
            if AVOID and r.random() < 0.5:
                a, b = self.atom(t), (self.atom(t) if r.random() < 0.7 else self.atom("int"))
                return r.choice(["(%s = %s)", "(%s != %s)", "(%s equals %s)", "(%s is equal to %s)", "(%s is not %s)",
                                 "(%s is %s)"]) % (a, b)
            forms = ["(%s < %s)", "(%s > %s)", "(%s <= %s)", "(%s >= %s)", "(%s is less than %s)", "(%s is not less than %s)", "(%s is greater than %s)",
                     "(%s is not greater than %s)", "(%s is at least %s)", "(%s is not at most %s)",
                     "(%s is at most %s)", "(%s is not at least %s)"]
            if not AVOID:
                forms += ["(%s is equal to %s)", "(%s is not %s)", "(%s = %s)", "(%s != %s)", "(%s equals %s)"]
            return r.choice(forms) % (a, b)
        if k < 0.6:
            t = r.choice(NUM)
            a = self.expr(t, d - 1)
            preds = ["zero", "positive", "negative", "not zero", "not negative"]
            if t == "int":
                preds += ["even", "odd", "not even"]
            return "(%s is %s)" % (self.paren(a), r.choice(preds))
        if k < 0.8:
            a, b = self.expr("bool", d - 1), self.expr("bool", d - 1)
            return r.choice(["(%s and %s)", "(%s or %s)"]) % (a, b)
        if k < 0.88:
            return r.choice(["(not %s)", "(it is not the case that %s)"]) % self.expr("bool", d - 1)
        if k < 0.94:
            t = r.choice(["bool", "text"])
            return r.choice(["(%s = %s)", "(%s != %s)"]) % (self.expr(t, d - 1), self.expr(t, d - 1))
        lists = self.visible(lambda u: u == ("list", "bool"))
        if lists:
            return "(item 1 of %s)" % r.choice(lists)[0]
        return self.lit("bool")

    def text_expr(self, d):
        r = self.r
        if r.random() < 0.1:
            return "this law's seal"
        parts = []
        for _ in range(r.randint(2, 4)):
            t = r.choice(["text", "int", "fix", "float", "bool", "text"])
            lists = self.visible(lambda u: isinstance(u, tuple))
            if lists and r.random() < 0.15:
                parts.append(r.choice(lists)[0])
            else:
                parts.append(self.paren(self.expr(t, d - 1)) if t != "text" else self.paren(self.expr(t, d - 1)))
        return "(" + " followed by ".join(parts) + ")"

    def list_expr(self, t, d):
        r = self.r
        e = t[1]
        cands = self.visible(lambda u: u == t)
        if cands and r.random() < 0.3:
            return r.choice(cands)[0]
        if r.random() < 0.6:
            n = r.randint(1, 4)
            items = [self.paren(self.expr(e, d - 1))]
            for _ in range(n - 1):
                items.append(self.paren(self.operand(e, d - 1)) if e != "bool" else self.paren(self.expr(e, d - 1)))
            r.shuffle(items)
            if n == 1:
                body = items[0]
            elif r.random() < 0.5:
                body = ", ".join(items[:-1]) + " and " + items[-1]
            else:
                body = ", ".join(items)
            return "(the list %s)" % body
        cnt = str(r.randint(0, 4)) if self.safe else self.paren(self.expr("int", d - 1))
        return "(a list of %s copies of %s)" % (cnt, self.paren(self.expr(e, d - 1)))

    # ------------------------------------------------ statements
    def stype(self):
        r = self.r
        return r.choice(["int", "int", "fix", "float", "bool", "text", ("list", "int"), ("list", self.D),
                         ("list", "bool"), ("list", r.choice(NUM))])

    def inline(self, d):
        """An inline statement (no declarations that outlive it are useful, but Let is legal)."""
        r = self.r
        k = r.random()
        w = self.visible(lambda u: True, writable=True)
        if k < 0.35 or not w:
            return "say %s" % self.expr(self.stype() if r.random() < 0.3 else r.choice(NUM + ("text",)), d)
        if k < 0.6:
            name, t = r.choice(w)
            return "set %s to %s" % (name, self.assign_expr(t, d))
        if k < 0.75:
            nums = [x for x in w if x[1] in NUM]
            if nums:
                name, t = r.choice(nums)
                return "%s %s by %s" % (r.choice(["increase", "decrease"]), name, self.operand(t, d))
        if k < 0.85 and self.procs:
            p = r.choice(self.procs)
            return ("perform %s" % p) if r.random() < 0.5 else p
        if k < 0.92:
            return "we claim that %s" % self.expr("bool", d)
        lists = [x for x in w if isinstance(x[1], tuple)]
        if lists:
            name, t = r.choice(lists)
            return "append %s to %s" % (self.paren(self.operand(t[1], d) if t[1] != "bool" else self.expr("bool", d)),
                                        name)
        return "say %s" % self.expr("int", d)

    def assign_expr(self, t, d):
        if t in ("fix", "float") and self.r.random() < 0.2:
            return self.expr("int", d)        # promoted on store
        return self.expr(t, d)

    def clause(self, label, text, kind="stmt"):
        self.lines.append((label, text))
        if kind == "stmt":
            self.kinds.append(label)
        return label

    def block(self, label, depth, count):
        self.scopes.append({})
        k = 0
        for _ in range(count):
            k = self.statement(label, k, depth)
        self.scopes.pop()
        return k

    def statement(self, parent, k, depth):
        """Writes one statement (maybe several sibling clauses) under parent; returns the last sibling number."""
        r = self.r
        top = parent == ()
        lab = lambda n: parent + (n,)
        x = r.random()
        dd = r.randint(1, 3)
        w = self.visible(lambda u: True, writable=True)
        if top and not self.in_proc and x < 0.07:
            return self.define(parent, k)
        if top and not self.in_proc and x < 0.12:
            return self.procedure(parent, k)
        if x < 0.3 or not w:
            t = self.stype()
            name = self.fresh()
            e = self.expr(t, dd)
            self.clause(lab(k + 1), "Let %s be %s." % (name, e))
            self.declare(name, t)
            return k + 1
        if x < 0.42:
            name, t = r.choice(w)
            if isinstance(t, tuple) and r.random() < 0.5:
                self.clause(lab(k + 1), "Set item %s of %s to %s." % (self.paren(self.expr("int", 1)) if not self.safe
                                                                  else "1", name, self.paren(self.assign_expr(t[1], dd))))
            else:
                self.clause(lab(k + 1), "Set %s to %s." % (name, self.assign_expr(t, dd)))
            return k + 1
        if x < 0.5:
            nums = [v for v in w if v[1] in NUM or (isinstance(v[1], tuple) and v[1][1] in NUM)]
            if nums:
                name, t = r.choice(nums)
                verb = r.choice(["Increase", "Decrease"])
                if isinstance(t, tuple):
                    self.clause(lab(k + 1), "%s item 1 of %s by %s." % (verb, name, self.operand(t[1], dd)))
                else:
                    self.clause(lab(k + 1), "%s %s by %s." % (verb, name, self.operand(t, dd)))
                return k + 1
        if x < 0.62:
            t = self.stype() if r.random() < 0.6 else "text"
            self.clause(lab(k + 1), "Say %s." % self.expr(t, dd))
            return k + 1
        if x < 0.7 and depth < 3:
            return self.if_chain(parent, k, depth)
        if x < 0.75:
            if r.random() < 0.5:
                self.clause(lab(k + 1), "If %s, %s; otherwise, %s." % (self.expr("bool", dd), self.inline(dd),
                                                                     self.inline(dd)))
            else:
                self.clause(lab(k + 1), "%s %s, %s." % (r.choice(["If", "Unless"]), self.expr("bool", dd),
                                                        self.inline(dd)))
            return k + 1
        if x < 0.8 and depth < 3:
            return self.for_loop(parent, k, depth)
        if x < 0.84 and depth < 3:
            return self.while_loop(parent, k, depth)
        if x < 0.88:
            lists = [v for v in w if isinstance(v[1], tuple)]
            if lists:
                name, t = r.choice(lists)
                if r.random() < 0.7:
                    self.clause(lab(k + 1), "Append %s to %s." % (self.paren(self.operand(t[1], dd) if t[1] != "bool"
                                                                             else self.expr("bool", dd)), name))
                else:
                    self.clause(lab(k + 1), "Remove the last item of %s." % name)
                return k + 1
        if x < 0.93:
            return self.claim(parent, k, dd)
        if x < 0.95:
            self.clause(lab(k + 1), "It must hold that %s." % self.expr("bool", dd))
            return k + 1
        if self.procs:
            p = r.choice(self.procs)
            self.clause(lab(k + 1), ("Perform %s." % p) if r.random() < 0.5 else "%s." % p.capitalize())
            return k + 1
        self.clause(lab(k + 1), "Say %s." % self.expr("int", dd))
        return k + 1

    def claim(self, parent, k, dd):
        r = self.r
        label = parent + (k + 1,)
        orc = r.random()
        tail = ""
        if orc < 0.3:
            tail = ""
        elif orc < 0.45:
            tail = ", by computation"
        elif orc < 0.55:
            tail = ", by the owner"
        elif orc < 0.65:
            tail = ', by the theorem "%s"' % r.choice(WORDS)
        elif orc < 0.9 and self.kinds:
            tgt = r.choice(self.kinds)
            tail = ", by the certificate of §%s" % ".".join(map(str, tgt))
            if r.random() < 0.5:
                tail += ' under the theorem "%s"' % r.choice(WORDS)
        if self.claim_labels and r.random() < 0.3:
            tail += ", given §%s" % ".".join(map(str, r.choice(self.claim_labels)))
        cond = self.expr("bool", dd)
        if r.random() < 0.5:
            cond = "(%s or true)" % cond          # mostly true, so runs go on
        self.clause(label, "We claim that %s%s." % (cond, tail), kind="claim")
        self.claim_labels.append(label)
        return k + 1

    def if_chain(self, parent, k, depth):
        r = self.r
        lab = parent + (k + 1,)
        self.clause(lab, "If %s, do the following." % self.expr("bool", 2))
        self.block(lab, depth + 1, r.randint(1, 3))
        k += 1
        for _ in range(r.randint(0, 2)):
            lab = parent + (k + 1,)
            if r.random() < 0.5:
                self.clause(lab, "Otherwise, if %s, do the following." % self.expr("bool", 2), kind="absorbed")
                self.block(lab, depth + 1, r.randint(1, 2))
            else:
                self.clause(lab, "Otherwise, if %s, %s." % (self.expr("bool", 2), self.inline(2)), kind="absorbed")
            k += 1
        if r.random() < 0.6:
            lab = parent + (k + 1,)
            if r.random() < 0.5:
                self.clause(lab, "Otherwise, do the following.", kind="absorbed")
                self.block(lab, depth + 1, r.randint(1, 2))
            else:
                self.clause(lab, "Otherwise, %s." % self.inline(2), kind="absorbed")
            k += 1
        return k

    def for_loop(self, parent, k, depth):
        r = self.r
        lab = parent + (k + 1,)
        name = self.fresh("i")
        lo = r.choice(["1", "0", "the larger of %s and -2" % self.paren(self.expr("int", 1)), "-2"])
        hi = r.choice(["3", "2", "1", "0", "the smaller of %s and 4" % self.paren(self.expr("int", 1))])
        if self.safe:
            lo, hi = r.choice([("1", "3"), ("0", "2"), ("1", "1"), ("2", "1"), ("-1", "1")])
        self.clause(lab, "For each %s from %s to %s, do the following." % (name, lo, hi))
        self.scopes.append({})
        self.declare(name, "int", ro=True)
        self.block(lab, depth + 1, r.randint(1, 3))
        self.scopes.pop()
        return k + 1

    def while_loop(self, parent, k, depth):
        r = self.r
        cnt = self.fresh("w")
        lab = parent + (k + 1,)
        self.clause(lab, "Let %s be 0." % cnt)
        self.declare(cnt, "int")
        k += 1
        lab = parent + (k + 1,)
        n = r.randint(1, 4)
        fuel = n + 1 if r.random() < 0.9 else n - 1 if n > 1 else 1
        self.clause(lab, "While %s is less than %d, at most %d times, do the following." % (cnt, n, fuel))
        self.scopes.append({})
        self.clause(lab + (1,), "Increase %s by 1." % cnt)
        self.scopes[-1]  # body scope
        kk = 1
        for _ in range(r.randint(0, 2)):
            kk = self.statement(lab, kk, depth + 1)
        self.scopes.pop()
        return k + 1

    def define(self, parent, k):
        r = self.r
        t = r.choice(["int", "fix", "float", "bool", "text", "int"])
        name = self.fresh("r")
        n = r.randint(1, 3)
        labels = []
        self.no_rules = AVOID
        for j in range(n):
            lab = parent + (k + 1,)
            e = self.expr(t, 2)
            prov = ""
            p = r.random()
            if p < 0.4:
                prov = ", provided that %s" % self.expr("bool", 1)
            elif p < 0.6:
                prov = ", unless %s" % self.expr("bool", 1)
            over = ""
            if labels and r.random() < 0.5:
                tg = r.sample(labels, r.randint(1, len(labels)))
                refs = ["§%s" % ".".join(map(str, x)) for x in tg]
                over = "Notwithstanding %s, " % (refs[0] if len(refs) == 1 else ", ".join(refs[:-1]) + " and " + refs[-1])
            self.clause(lab, "%sdefine %s as %s%s." % (over, name, e, prov) if over else
                        "Define %s as %s%s." % (name, e, prov), kind="define")
            labels.append(lab)
            k += 1
        self.no_rules = False
        self.rules[name] = t
        return k

    def procedure(self, parent, k):
        r = self.r
        lab = parent + (k + 1,)
        pname = "run job %s%d" % (r.choice(WORDS), self.n)
        self.n += 1
        self.clause(lab, "To %s, do the following." % pname, kind="proc")
        saved = self.scopes
        self.scopes = [dict(self.scopes[0])]
        self.in_proc = True
        self.no_rules = AVOID
        self.block(lab, 1, r.randint(1, 3))
        self.in_proc = False
        self.no_rules = False
        self.scopes = saved
        self.procs.append(pname)
        return k + 1

    def program(self):
        k = 0
        if self.mode == "floats" or self.r.random() < 0.3:
            self.clause((1,), "Decimals are %s." % ("floats" if self.mode == "floats" else "fixed"), kind="decimals")
            k = 1
        while k < self.size:
            k = self.statement((), k, 0)
        out = []
        for label, text in self.lines:
            out.append("§%s %s" % (".".join(map(str, label)), text))
        return ("\n".join(out) + "\n").encode("utf-8")


def generate(seed, size=None):
    return Gen(seed, size).program()


if __name__ == "__main__":
    import sys
    sys.stdout.buffer.write(generate(int(sys.argv[1])))
