"""Arithmetic behind the DERIVED tags in R3 (standard library only)."""
from fractions import Fraction
import itertools

# 1. Katapayadi decodings: digits per syllable (left to right), then reversed.
def kp(digits):
    return int("".join(str(d) for d in reversed(digits)))

# bha dra mbu dhi si ddha ja nma ga ni ta shra ddha sma ya(d) bhu pa gih
sadratnamala = [4, 2, 3, 9, 7, 9, 8, 5, 3, 5, 6, 2, 9, 5, 1, 4, 1, 3]
print("sadratnamala", kp(sadratnamala))
# a yu ra ro gya sau khyam
print("narayaniyam", kp([0, 1, 2, 2, 1, 7, 1]))
print("dhira", kp([9, 2]), "jaya", kp([8, 1]))

PI = "31415926535897932384626433832795028841971"  # pi digits, no point
print("pi*1e17 rounded", round(Fraction(int(PI[:30]), 10 ** 29) * 10 ** 17))
print("pi*1e10 rounded", round(Fraction(int(PI[:30]), 10 ** 29) * 10 ** 10))
print("pi*9e11 rounded", round(Fraction(int(PI[:30]), 10 ** 29) * 9 * 10 ** 11))
printed = "31415926535897932384626433832792"   # gopi verse, pi/10 after the point
true = PI[:32]
first_diff = next((i for i in range(32) if printed[i] != true[i]), None)
print("gopi: first differing decimal of pi/10 =", None if first_diff is None else first_diff + 1,
      "printed", printed[first_diff], "true", true[first_diff])

# 2. Aryabhata khyughr: kh=2 (varga) with u, y=30 (avarga) with u, gh=4 with r.
print("khyughr", 2 * 10 ** 4 + 30 * 10 ** 4 + 4 * 10 ** 6)

# 3. Roman chronogram and Greek isopsephy.
ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
print("ICVLICIDIVM", sum(ROMAN.get(c, 0) for c in "ICVLICIDIVM"))
print("MDCIII", sum(ROMAN[c] for c in "MDCIII"))
print("Nero (nu epsilon rho omega nu)", 50 + 5 + 100 + 800 + 50)

# 4. x o y = a x + y over GF(p): total anti-symmetry, jump transpositions, diagonal.
def ta_report(p, a):
    op = lambda x, y: (a * x + y) % p
    els = range(p)
    quasi = all(len({op(x, y) for y in els}) == p for x in els) and \
        all(len({op(x, y) for x in els}) == p for y in els)
    comm = all(op(x, y) != op(y, x) for x in els for y in els if x != y)
    ta = all(op(op(c, x), y) != op(op(c, y), x)
             for c in els for x in els for y in els if x != y)
    # jump transposition b?c -> c?b over a middle symbol m, from any start s
    jump = all(op(op(op(s, x), m), y) != op(op(op(s, y), m), x)
               for s in els for m in els for x in els for y in els if x != y)
    zero_diag = all(op(x, x) == 0 for x in els)
    return quasi, comm, ta, jump, zero_diag

for p in (3, 5, 7, 11, 13):
    for a in range(p):
        q, cm, ta, jp, zd = ta_report(p, a)
        expect_ta = a not in (0, 1)
        expect_jump = expect_ta and (a * a) % p != 1
        assert (q and cm and ta) == expect_ta or a == 0, (p, a)
        if q:
            assert ta == expect_ta and jp == expect_jump, (p, a, ta, jp)
        assert zd == ((a + 1) % p == 0), (p, a)
print("GF(p) checks for p in 3,5,7,11,13: TA iff a not in {0,1}; jump iff a^2 != 1; zero diagonal iff a = -1")

# GF(4) = F2[t]/(t^2+t+1), elements 0..3 as bit pairs.
def gf4_mul(x, y):
    r = 0
    for i in range(2):
        if (y >> i) & 1:
            r ^= x << i
    if r & 4:
        r ^= 0b111
    return r
for a in range(4):
    op = lambda x, y: gf4_mul(a, x) ^ y
    ta = all(op(op(c, x), y) != op(op(c, y), x) for c in range(4) for x in range(4) for y in range(4) if x != y)
    cm = all(op(x, y) != op(y, x) for x in range(4) for y in range(4) if x != y)
    print("GF(4) a =", a, "TA" if (ta and cm and a != 0) else "not TA")

# 5. ISO 7064 MOD 11-2 recursion equals iterating x o y = 2x + y over Z_11.
def mod11_2(digits):
    c = 0
    for d in digits:
        c = (2 * c + d) % 11
    return c
def iterate(digits, a=2, p=11):
    c = 0
    for d in digits:
        c = (a * c + d) % p
    return c
for digits in itertools.product(range(10), repeat=4):
    assert mod11_2(digits) == iterate(digits)
print("MOD 11-2 == iterated 2x+y over Z_11 on all 4-digit strings")
# MOD 97-10 on a decimal string is int(s) % 97 == Horner with a = 10.
for n in range(0, 100000, 37):
    s = str(n)
    assert int(s) % 97 == iterate([int(ch) for ch in s], a=10, p=97)
print("int(s) % 97 == iterated 10x+y over Z_97")

# 6. BIP-39 sizes.
for ent in (128, 160, 192, 224, 256):
    cs = ent // 32
    print("BIP39 ENT", ent, "CS", cs, "words", (ent + cs) // 11, "random pass prob 1/%d" % (2 ** cs))
