/*
 * test_rt.c -- the conformance harness of orlog_rt.h (RUNTIME-SPEC.md section 9).
 *
 *   test_rt VECTORS [CHAIN-DIR]
 *
 * 1. Runs every line of VECTORS. A refusable operation is run twice: its pure
 *    form (orl__NAME, refusal code through an out-parameter) and the contract's
 *    wrapper (orl_NAME), whose refusal is observed through ORL_TEST's hook and a
 *    longjmp; the line passes only when both give the expected value, or both
 *    refuse with the expected code (the wrapper with the clause it was given).
 *    A printing line is checked through the formatter and through the builder.
 *    A SHA-256 line is checked one-shot and fed byte by byte and in chunks.
 *    Prints every failing line, then RUNTIME VECTORS <passed> / <total>.
 * 2. The event-chain check: law seal SHA-256("law"); events 'S' clause 1
 *    payload "hello\n", 'A' clause 2 payload var 0 + Int 42, 'R' clause 3
 *    payload "OVERFLOW"; prints head0..head3 (compare with src/check_chain.py)
 *    and the receipt and trace the run wrote into CHAIN-DIR (default: the
 *    executable's own folder, so that a run never writes beside its caller).
 * 3. Extra checks of what the vectors do not reach: the builder's, the output's
 *    and the lists' limits and refusals, list printing, texts.
 *
 * Exit status 0 when everything passed, 1 otherwise.
 */
#define ORL_TEST 1
#include "orlog_rt.h"
#include <setjmp.h>

#define CLAUSE 77u

/* ---------------------------------------------------------------- the refusal hook */

static jmp_buf T_jb;
static int T_armed;
static const char *T_code;
static uint32_t T_clause;

static void T_hook(const char *code, uint32_t c) {
    T_code = code != NULL ? code : "(finish)";
    T_clause = c;
    if (T_armed) {
        T_armed = 0;
        longjmp(T_jb, 1);
    }
    fprintf(stderr, "UNEXPECTED REFUSAL %s %u outside a guarded call\n", T_code, (unsigned)c);
    exit(1);
}

/* dst = expr, with a refusal observed in T_code / T_clause (T_code NULL: none). */
#define WRAPPED(dst, expr)                          \
    do {                                            \
        T_code = NULL;                              \
        T_clause = 0;                               \
        T_armed = 1;                                \
        if (setjmp(T_jb) == 0) { (dst) = (expr); }  \
        T_armed = 0;                                \
    } while (0)

#define GUARDED(stmt)                               \
    do {                                            \
        T_code = NULL;                              \
        T_clause = 0;                               \
        T_armed = 1;                                \
        if (setjmp(T_jb) == 0) { stmt; }            \
        T_armed = 0;                                \
    } while (0)

/* ---------------------------------------------------------------- small text helpers */

static void app(char *dst, size_t cap, const char *s) {
    size_t n = strlen(dst), k = strlen(s);
    if (n + 1 >= cap) return;
    if (k > cap - 1 - n) k = cap - 1 - n;
    memcpy(dst + n, s, k);
    dst[n + k] = '\0';
}

static void app_n(char *dst, size_t cap, const char *s, size_t k) {
    size_t n = strlen(dst);
    if (n + 1 >= cap) return;
    if (k > cap - 1 - n) k = cap - 1 - n;
    memcpy(dst + n, s, k);
    dst[n + k] = '\0';
}

static void app_i64(char *dst, size_t cap, int64_t v) {
    char b[ORL_FMT_I_MAX];
    app_n(dst, cap, b, orl__fmt_i(b, v));
}

static void app_hex64(char *dst, size_t cap, uint64_t v) {
    char b[17];
    int i;
    for (i = 0; i < 16; ++i) b[i] = "0123456789ABCDEF"[(v >> (60 - 4 * i)) & 15u];
    b[16] = '\0';
    app(dst, cap, b);
}

static void hexify(const uint8_t *p, size_t n, char *out) {
    size_t i;
    for (i = 0; i < n; ++i) {
        out[2 * i] = orl__hexd[p[i] >> 4];
        out[2 * i + 1] = orl__hexd[p[i] & 15u];
    }
    out[2 * n] = '\0';
}

/* ---------------------------------------------------------------- vector values */

typedef struct {
    char kind;          /* 'i' 'x' 'f' 'b' 's' 'h' (hex:), '!' (a refusal) */
    int64_t iv;         /* i: x: b: */
    uint64_t fv;        /* f: the binary64 bits */
    const char *text;   /* s: the text; hex: the digits; !: the code */
    size_t tlen;
} val_t;

static int parse_i64(const char *s, int64_t *out) {
    const char *p = s, *e = NULL;
    int neg = 0;
    uint64_t m = 0;
    if (*p == '-') { neg = 1; p++; }
    if (*p == '\0') return 0;
    for (; *p != '\0'; ++p) {
        unsigned d;
        if (*p < '0' || *p > '9') return 0;
        d = (unsigned)(*p - '0');
        if (m > (UINT64_MAX - d) / 10u) return 0;
        m = m * 10u + d;
    }
    *out = orl__signed(neg, m, &e);
    return e == NULL;
}

static int parse_hex64(const char *s, uint64_t *out) {
    uint64_t v = 0;
    int i;
    for (i = 0; i < 16; ++i) {
        int d = orl__hexval((unsigned char)s[i]);
        if (d < 0) return 0;
        v = (v << 4) | (uint64_t)d;
    }
    if (s[16] != '\0') return 0;
    *out = v;
    return 1;
}

static int parse_val(const char *t, val_t *v, int result) {
    memset(v, 0, sizeof *v);
    if (result && t[0] == '!') { v->kind = '!'; v->text = t + 1; v->tlen = strlen(t + 1); return v->tlen > 0; }
    if (strncmp(t, "i:", 2) == 0) { v->kind = 'i'; return parse_i64(t + 2, &v->iv); }
    if (strncmp(t, "x:", 2) == 0) { v->kind = 'x'; return parse_i64(t + 2, &v->iv); }
    if (strncmp(t, "f:", 2) == 0) { v->kind = 'f'; return parse_hex64(t + 2, &v->fv); }
    if (strncmp(t, "b:", 2) == 0) {
        v->kind = 'b';
        if (strcmp(t + 2, "0") == 0) v->iv = 0;
        else if (strcmp(t + 2, "1") == 0) v->iv = 1;
        else return 0;
        return 1;
    }
    if (result && strncmp(t, "s:", 2) == 0) { v->kind = 's'; v->text = t + 2; v->tlen = strlen(t + 2); return 1; }
    if (strncmp(t, "hex:", 4) == 0) {
        size_t i;
        v->kind = 'h';
        v->text = t + 4;
        v->tlen = strlen(t + 4);
        if (v->tlen % 2 != 0) return 0;
        for (i = 0; i < v->tlen; ++i)
            if (orl__hexval((unsigned char)v->text[i]) < 0) return 0;
        return 1;
    }
    return 0;
}

/* ---------------------------------------------------------------- judging outcomes */

static void describe(char *dst, size_t cap, const char *code, char kind, int64_t iv, uint64_t fv) {
    char k[3];
    if (code != NULL) { app(dst, cap, "!"); app(dst, cap, code); return; }
    k[0] = kind; k[1] = ':'; k[2] = '\0';
    app(dst, cap, k);
    if (kind == 'f') app_hex64(dst, cap, fv);
    else app_i64(dst, cap, iv);
}

static int match(const val_t *x, const char *code, char kind, int64_t iv, uint64_t fv) {
    if (x->kind == '!') return code != NULL && strcmp(code, x->text) == 0;
    if (code != NULL || x->kind != kind) return 0;
    if (kind == 'f') return x->fv == fv;
    return x->iv == iv;
}

/* The pure outcome and the wrapped outcome against the expected value. */
static int judge(const val_t *x, char kind,
                 const char *pe, int64_t pv, uint64_t pf,
                 const char *we, uint32_t wc, int64_t wv, uint64_t wf,
                 char *why, size_t cap) {
    int okp = match(x, pe, kind, pv, pf);
    int okw = match(x, we, kind, wv, wf) && (we == NULL || wc == CLAUSE);
    if (okp && okw) return 1;
    app(why, cap, "pure ");
    describe(why, cap, pe, kind, pv, pf);
    app(why, cap, " | wrapped ");
    describe(why, cap, we, kind, wv, wf);
    if (we != NULL && wc != CLAUSE) app(why, cap, " (clause not passed)");
    return 0;
}

static int judge_plain(const val_t *x, char kind, int64_t v, uint64_t f, char *why, size_t cap) {
    if (match(x, NULL, kind, v, f)) return 1;
    app(why, cap, "got ");
    describe(why, cap, NULL, kind, v, f);
    return 0;
}

/* ---------------------------------------------------------------- operation families */

typedef int64_t (*pi1_t)(int64_t, const char **);
typedef int64_t (*wi1_t)(int64_t, uint32_t);
typedef int64_t (*pi2_t)(int64_t, int64_t, const char **);
typedef int64_t (*wi2_t)(int64_t, int64_t, uint32_t);
typedef int64_t (*ii2_t)(int64_t, int64_t);
typedef int64_t (*ii1_t)(int64_t);
typedef double (*ff1_t)(double);
typedef double (*ff2_t)(double, double);
typedef int64_t (*pfi_t)(double, const char **);
typedef int64_t (*wfi_t)(double, uint32_t);

static int t_i1(pi1_t p, wi1_t w, char rk, const val_t *a, const val_t *x, char *why, size_t cap) {
    const char *pe;
    int64_t pv = p(a[0].iv, &pe);
    volatile int64_t wv = 0;
    WRAPPED(wv, w(a[0].iv, CLAUSE));
    return judge(x, rk, pe, pv, 0, T_code, T_clause, wv, 0, why, cap);
}

static int t_i2(pi2_t p, wi2_t w, char rk, const val_t *a, const val_t *x, char *why, size_t cap) {
    const char *pe;
    int64_t pv = p(a[0].iv, a[1].iv, &pe);
    volatile int64_t wv = 0;
    WRAPPED(wv, w(a[0].iv, a[1].iv, CLAUSE));
    return judge(x, rk, pe, pv, 0, T_code, T_clause, wv, 0, why, cap);
}

static int t_fi(pfi_t p, wfi_t w, const val_t *a, const val_t *x, char *why, size_t cap) {
    double d = orl__bf(a[0].fv);
    const char *pe;
    int64_t pv = p(d, &pe);
    volatile int64_t wv = 0;
    WRAPPED(wv, w(d, CLAUSE));
    return judge(x, 'i', pe, pv, 0, T_code, T_clause, wv, 0, why, cap);
}

static int t_x_to_f(const val_t *a, const val_t *x, char *why, size_t cap) {
    const char *pe;
    double pd = orl__x_to_f(a[0].iv, (int)a[1].iv, &pe);
    volatile double wd = 0.0;
    double wcopy;
    WRAPPED(wd, orl_x_to_f(a[0].iv, (int)a[1].iv, CLAUSE));
    wcopy = wd;
    return judge(x, 'f', pe, 0, orl__fb(pd), T_code, T_clause, 0, orl__fb(wcopy), why, cap);
}

static int t_f_from_i(const val_t *a, const val_t *x, char *why, size_t cap) {
    const char *pe;
    double pd = orl__f_from_i(a[0].iv, (int)a[1].iv, &pe);
    volatile double wd = 0.0;
    double wcopy;
    WRAPPED(wd, orl_f_from_i(a[0].iv, (int)a[1].iv, CLAUSE));
    wcopy = wd;
    return judge(x, 'f', pe, 0, orl__fb(pd), T_code, T_clause, 0, orl__fb(wcopy), why, cap);
}

static int t_f_to_x(const val_t *a, const val_t *x, char *why, size_t cap) {
    double d = orl__bf(a[0].fv);
    const char *pe;
    int64_t pv = orl__f_to_x(d, (int)a[1].iv, &pe);
    volatile int64_t wv = 0;
    WRAPPED(wv, orl_f_to_x(d, (int)a[1].iv, CLAUSE));
    return judge(x, 'x', pe, pv, 0, T_code, T_clause, wv, 0, why, cap);
}

/* Text results: the formatter's bytes, and the builder's bytes and its copy. */
static int t_text(const char *got, size_t n, const val_t *x, char *why, size_t cap) {
    orl_text t;
    int ok;
    if (x->kind != 's') { app(why, cap, "expected a text"); return 0; }
    ok = n == x->tlen && memcmp(got, x->text, n) == 0;
    ok = ok && orl__sb_len == x->tlen && (x->tlen == 0 || memcmp(orl__sb, x->text, x->tlen) == 0);
    t = orl_s_take();
    ok = ok && orl_t_eq(t, orl_t_lit(x->text, (uint32_t)x->tlen));
    free((void *)t.p);
    if (ok) return 1;
    app(why, cap, "got s:");
    app_n(why, cap, got, n);
    app(why, cap, " | builder s:");
    app_n(why, cap, (const char *)orl__sb, orl__sb_len);
    return 0;
}

static int t_sha(const val_t *a, const val_t *x, char *why, size_t cap) {
    size_t n = a[0].tlen / 2, i, step;
    uint8_t *msg = (uint8_t *)orl__alloc(n), dg[32];
    char hex[65], hex2[65];
    int ok = 1;
    static const size_t steps[4] = {1, 7, 63, 64};
    if (x->kind != 'h' || x->tlen != 64) { free(msg); app(why, cap, "expected 32 bytes of hex"); return 0; }
    for (i = 0; i < n; ++i)
        msg[i] = (uint8_t)((orl__hexval((unsigned char)a[0].text[2 * i]) << 4) |
                           orl__hexval((unsigned char)a[0].text[2 * i + 1]));
    orl__sha256_once(msg, n, dg);
    hexify(dg, 32, hex);
    if (memcmp(hex, x->text, 64) != 0) ok = 0;
    for (step = 0; step < 4; ++step) {
        orl__sha256 h;
        orl__sha_init(&h);
        for (i = 0; i < n; i += steps[step])
            orl__sha_update(&h, msg + i, (n - i < steps[step]) ? n - i : steps[step]);
        orl__sha_final(&h, dg);
        hexify(dg, 32, hex2);
        if (memcmp(hex2, x->text, 64) != 0) ok = 0;
    }
    free(msg);
    if (ok) return 1;
    app(why, cap, "got hex:");
    app(why, cap, hex);
    app(why, cap, " (or a streamed digest differs)");
    return 0;
}

/* ---------------------------------------------------------------- one vector line */

static int run_line(char *line, char *why, size_t cap) {
    char *sep = strstr(line, " => "), *tok[8], *p;
    int nt = 0, i;
    val_t a[6], x;
    const char *op;
    if (sep == NULL) { app(why, cap, "no ' => '"); return 0; }
    *sep = '\0';
    if (!parse_val(sep + 4, &x, 1)) { app(why, cap, "bad result"); return 0; }
    for (p = line; *p != '\0' && nt < 8;) {
        tok[nt++] = p;
        while (*p != '\0' && *p != ' ') p++;
        if (*p == ' ') *p++ = '\0';
    }
    if (nt < 1 || nt > 7) { app(why, cap, "bad arity"); return 0; }
    op = tok[0];
    for (i = 1; i < nt; ++i)
        if (!parse_val(tok[i], &a[i - 1], 0)) { app(why, cap, "bad argument"); return 0; }

#define IS(name, n) (strcmp(op, name) == 0 && nt == (n) + 1)
    /* Int */
    if (IS("i_add", 2)) return t_i2(orl__i_add, orl_i_add, 'i', a, &x, why, cap);
    if (IS("i_sub", 2)) return t_i2(orl__i_sub, orl_i_sub, 'i', a, &x, why, cap);
    if (IS("i_mul", 2)) return t_i2(orl__i_mul, orl_i_mul, 'i', a, &x, why, cap);
    if (IS("i_div", 2)) return t_i2(orl__i_div, orl_i_div, 'i', a, &x, why, cap);
    if (IS("i_quot", 2)) return t_i2(orl__i_quot, orl_i_quot, 'i', a, &x, why, cap);
    if (IS("i_rem", 2)) return t_i2(orl__i_rem, orl_i_rem, 'i', a, &x, why, cap);
    if (IS("i_neg", 1)) return t_i1(orl__i_neg, orl_i_neg, 'i', a, &x, why, cap);
    if (IS("i_abs", 1)) return t_i1(orl__i_abs, orl_i_abs, 'i', a, &x, why, cap);
    if (IS("i_isqrt", 1)) return t_i1(orl__i_isqrt, orl_i_isqrt, 'i', a, &x, why, cap);
    if (IS("i_max", 2)) return judge_plain(&x, 'i', orl_i_max(a[0].iv, a[1].iv), 0, why, cap);
    if (IS("i_min", 2)) return judge_plain(&x, 'i', orl_i_min(a[0].iv, a[1].iv), 0, why, cap);
    /* Fix */
    if (IS("x_from_i", 1)) return t_i1(orl__x_from_i, orl_x_from_i, 'x', a, &x, why, cap);
    if (IS("x_add", 2)) return t_i2(orl__i_add, orl_x_add, 'x', a, &x, why, cap);
    if (IS("x_sub", 2)) return t_i2(orl__i_sub, orl_x_sub, 'x', a, &x, why, cap);
    if (IS("x_mul", 2)) return t_i2(orl__x_mul, orl_x_mul, 'x', a, &x, why, cap);
    if (IS("x_div", 2)) return t_i2(orl__x_div, orl_x_div, 'x', a, &x, why, cap);
    if (IS("x_neg", 1)) return t_i1(orl__i_neg, orl_x_neg, 'x', a, &x, why, cap);
    if (IS("x_abs", 1)) return t_i1(orl__i_abs, orl_x_abs, 'x', a, &x, why, cap);
    if (IS("x_sqrt", 1)) return t_i1(orl__x_sqrt, orl_x_sqrt, 'x', a, &x, why, cap);
    if (IS("x_trunc", 1)) return judge_plain(&x, 'i', orl_x_trunc(a[0].iv), 0, why, cap);
    if (IS("x_round", 1)) return judge_plain(&x, 'i', orl_x_round(a[0].iv), 0, why, cap);
    if (IS("x_max", 2)) return judge_plain(&x, 'x', orl_x_max(a[0].iv, a[1].iv), 0, why, cap);
    if (IS("x_min", 2)) return judge_plain(&x, 'x', orl_x_min(a[0].iv, a[1].iv), 0, why, cap);
    if (IS("x_to_f", 2)) return t_x_to_f(a, &x, why, cap);
    /* Float */
    if (IS("f_from_i", 2)) return t_f_from_i(a, &x, why, cap);
    if (IS("f_to_x", 2)) return t_f_to_x(a, &x, why, cap);
    if (IS("f_trunc", 1)) return t_fi(orl__f_trunc, orl_f_trunc, a, &x, why, cap);
    if (IS("f_round", 1)) return t_fi(orl__f_round, orl_f_round, a, &x, why, cap);
    if (IS("f_neg", 1)) return judge_plain(&x, 'f', 0, orl__fb(orl_f_neg(orl__bf(a[0].fv))), why, cap);
    if (IS("f_abs", 1)) return judge_plain(&x, 'f', 0, orl__fb(orl_f_abs(orl__bf(a[0].fv))), why, cap);
    if (IS("f_sqrt", 1)) return judge_plain(&x, 'f', 0, orl__fb(orl_f_sqrt(orl__bf(a[0].fv))), why, cap);
    if (strncmp(op, "f_", 2) == 0 && nt == 3) {
        double l = orl__bf(a[0].fv), r = orl__bf(a[1].fv);
        if (IS("f_add", 2)) return judge_plain(&x, 'f', 0, orl__fb(orl_f_add(l, r)), why, cap);
        if (IS("f_sub", 2)) return judge_plain(&x, 'f', 0, orl__fb(orl_f_sub(l, r)), why, cap);
        if (IS("f_mul", 2)) return judge_plain(&x, 'f', 0, orl__fb(orl_f_mul(l, r)), why, cap);
        if (IS("f_div", 2)) return judge_plain(&x, 'f', 0, orl__fb(orl_f_div(l, r)), why, cap);
        if (IS("f_max", 2)) return judge_plain(&x, 'f', 0, orl__fb(orl_f_max(l, r)), why, cap);
        if (IS("f_min", 2)) return judge_plain(&x, 'f', 0, orl__fb(orl_f_min(l, r)), why, cap);
        if (IS("f_lt", 2)) return judge_plain(&x, 'b', l < r, 0, why, cap);
        if (IS("f_eq", 2)) return judge_plain(&x, 'b', l == r, 0, why, cap);
    }
    /* printing: the formatter, and the builder after a reset */
    if (IS("fmt_i", 1)) {
        char b[ORL_FMT_I_MAX];
        size_t n = orl__fmt_i(b, a[0].iv);
        orl_s_reset(CLAUSE);
        orl_s_i(a[0].iv);
        return t_text(b, n, &x, why, cap);
    }
    if (IS("fmt_x", 1)) {
        char b[ORL_FMT_X_MAX];
        size_t n = orl__fmt_x(b, a[0].iv);
        orl_s_reset(CLAUSE);
        orl_s_x(a[0].iv);
        return t_text(b, n, &x, why, cap);
    }
    if (IS("fmt_f", 1)) {
        char b[ORL_FMT_F_MAX];
        size_t n = orl__fmt_f(b, orl__bf(a[0].fv));
        orl_s_reset(CLAUSE);
        orl_s_f(orl__bf(a[0].fv));
        return t_text(b, n, &x, why, cap);
    }
    if (IS("sha256", 1) && a[0].kind == 'h') return t_sha(a, &x, why, cap);
#undef IS
    app(why, cap, "unknown operation or arity");
    return 0;
}

/* ---------------------------------------------------------------- the vectors */

static int run_vectors(const char *path) {
    FILE *f = fopen(path, "rb");
    char *buf, *p, *end;
    long size;
    long passed = 0, total = 0;
    char why[4096];
    if (f == NULL) { fprintf(stderr, "cannot open %s\n", path); exit(2); }
    if (fseek(f, 0, SEEK_END) != 0 || (size = ftell(f)) < 0 || fseek(f, 0, SEEK_SET) != 0) {
        fprintf(stderr, "cannot size %s\n", path);
        exit(2);
    }
    buf = (char *)orl__alloc((size_t)size + 1);
    if (fread(buf, 1, (size_t)size, f) != (size_t)size) { fprintf(stderr, "cannot read %s\n", path); exit(2); }
    fclose(f);
    buf[size] = '\0';
    for (p = buf, end = buf + size; p < end;) {
        char *nl = memchr(p, '\n', (size_t)(end - p)), *copy;
        size_t len = nl != NULL ? (size_t)(nl - p) : (size_t)(end - p);
        if (len > 0 && p[len - 1] == '\r') len--;
        if (len > 0) {
            p[len] = '\0';
            copy = (char *)orl__alloc(len + 1);
            memcpy(copy, p, len + 1);
            why[0] = '\0';
            total++;
            if (run_line(p, why, sizeof why)) passed++;
            else printf("FAIL %s  ->  %s\n", copy, why);
            free(copy);
        }
        p = nl != NULL ? nl + 1 : end;
    }
    free(buf);
    printf("RUNTIME VECTORS %ld / %ld\n", passed, total);
    return passed == total && total > 0;
}

/* ---------------------------------------------------------------- the event chain */

static void print_head(const char *label) {
    char hex[65];
    hexify(orl__head, 32, hex);
    printf("%s %s\n", label, hex);
}

static char *slurp(const char *path, size_t *n) {
    FILE *f = fopen(path, "rb");
    char *b;
    long size;
    if (f == NULL) return NULL;
    if (fseek(f, 0, SEEK_END) != 0 || (size = ftell(f)) < 0 || fseek(f, 0, SEEK_SET) != 0) { fclose(f); return NULL; }
    b = (char *)orl__alloc((size_t)size + 1);
    if (fread(b, 1, (size_t)size, f) != (size_t)size) { fclose(f); free(b); return NULL; }
    fclose(f);
    b[size] = '\0';
    *n = (size_t)size;
    return b;
}

static void join(char *dst, size_t cap, const char *dir, const char *name) {
    dst[0] = '\0';
    app(dst, cap, dir);
    app(dst, cap, "/");
    app(dst, cap, name);
}

static int chain_check(const char *dir) {
    char out_p[1024], rc_p[1024], tr_p[1024], a0[] = "test_rt";
    char *av[5];
    uint8_t law[32], text[32], dg[32];
    char law_hex[65], text_hex[65], h[4][65], want[1024], hx[65];
    size_t n;
    char *rc, *tr;
    int ok = 1;
    join(out_p, sizeof out_p, dir, "chain-output.txt");
    join(rc_p, sizeof rc_p, dir, "chain-receipt.txt");
    join(tr_p, sizeof tr_p, dir, "chain-trace.txt");
    av[0] = a0; av[1] = out_p; av[2] = rc_p; av[3] = tr_p; av[4] = NULL;
    orl__sha256_once("law", 3, law);
    hexify(law, 32, law_hex);
    orl__sha256_once("text", 4, text);
    hexify(text, 32, text_hex);

    printf("EVENT CHAIN (law seal = SHA-256(\"law\"))\n");
    orl_init(4, av, "c99", law_hex, text_hex, 0, NULL);
    hexify(orl__head, 32, h[0]);
    print_head("head0");
    orl_s_reset(1);
    orl_s_lit("hello", 5);
    orl_say(1);
    hexify(orl__head, 32, h[1]);
    print_head("head1");
    orl_ev_assign_i(2, 0, 42);
    hexify(orl__head, 32, h[2]);
    print_head("head2");
    GUARDED(orl_refuse(ORL_OVERFLOW, 3));
    if (T_code == NULL || strcmp(T_code, ORL_OVERFLOW) != 0 || T_clause != 3) {
        printf("CHAIN: orl_refuse was not observed\n");
        ok = 0;
    }
    hexify(orl__head, 32, h[3]);
    print_head("head3");

    rc = slurp(rc_p, &n);
    if (rc == NULL) { printf("CHAIN: no receipt\n"); return 0; }
    printf("---- %s\n%s", "chain-receipt.txt", rc);
    tr = slurp(tr_p, &n);
    if (tr == NULL) { printf("CHAIN: no trace\n"); free(rc); return 0; }
    printf("---- %s\n%s----\n", "chain-trace.txt", tr);

    /* the files agree with the heads printed above */
    want[0] = '\0';
    app(want, sizeof want, "1 S 1 68656c6c6f0a "); app(want, sizeof want, h[1]); app(want, sizeof want, "\n");
    app(want, sizeof want, "2 A 2 0000000049000000000000002a "); app(want, sizeof want, h[2]); app(want, sizeof want, "\n");
    app(want, sizeof want, "3 R 3 4f564552464c4f57 "); app(want, sizeof want, h[3]); app(want, sizeof want, "\n");
    if (strcmp(tr, want) != 0) { printf("CHAIN: the trace is not the three events\n"); ok = 0; }
    orl__sha256_once("hello\n", 6, dg);
    hexify(dg, 32, hx);
    want[0] = '\0';
    app(want, sizeof want, "status REFUSED OVERFLOW 3\noutput-bytes 6\noutput-sha256 ");
    app(want, sizeof want, hx);
    app(want, sizeof want, "\nevents 3\ntrace-head ");
    app(want, sizeof want, h[3]);
    app(want, sizeof want, "\nops 0\nclaims 0\nend\n");
    if (strstr(rc, want) == NULL || strncmp(rc, "orlog-receipt 0\nbackend c99\nlaw-seal ", 37) != 0) {
        printf("CHAIN: the receipt does not describe the run\n");
        ok = 0;
    }
    free(rc);
    free(tr);
    printf("CHAIN FILES %s\n", ok ? "CONSISTENT WITH THE HEADS" : "INCONSISTENT");
    return ok;
}

/* ---------------------------------------------------------------- extra checks */

static int x_pass, x_total;

static void expect(int cond, const char *what) {
    x_total++;
    if (cond) x_pass++;
    else printf("EXTRA FAIL %s\n", what);
}

static int refused_with(const char *code, uint32_t c) {
    return T_code != NULL && strcmp(T_code, code) == 0 && T_clause == c;
}

static int builder_is(const char *s) {
    size_t n = strlen(s);
    return orl__sb_len == n && (n == 0 || memcmp(orl__sb, s, n) == 0);
}

static void extra_checks(void) {
    static const int64_t li[3] = {1, -2, INT64_MIN};
    int64_t lx[2], lf[4], lb[3] = {1, 0, 5};
    char *mib = (char *)orl__alloc((size_t)1 << 20);
    volatile int64_t v = 0;
    orl_list l, big, cp;
    orl_text t;
    int i;

    /* the builder: exactly 2^24 bytes is allowed; one more byte refuses */
    memset(mib, 'a', (size_t)1 << 20);
    orl_s_reset(9);
    GUARDED(for (i = 0; i < 16; ++i) orl_s_lit(mib, (uint32_t)1 << 20));
    expect(T_code == NULL && orl__sb_len == ORL_TEXT_MAX, "builder holds exactly 2^24 bytes");
    GUARDED(orl_s_lit("x", 1));
    expect(refused_with(ORL_TEXT_TOO_LONG, 9), "TEXT-TOO-LONG past 2^24, clause of the last reset");
    orl_s_reset(10);
    GUARDED(orl_s_lit(mib, (uint32_t)1 << 20));
    GUARDED(orl_s_i(-5));
    expect(T_code == NULL && orl__sb_len == ((uint32_t)1 << 20) + 2, "reset empties the builder");
    free(mib);

    /* the output: exactly 2^30 bytes is allowed; one more refuses */
    orl__out_bytes = ORL_OUTPUT_MAX - 3;
    orl_s_reset(5);
    orl_s_lit("ab", 2);
    GUARDED(orl_say(5));
    expect(T_code == NULL && orl__out_bytes == ORL_OUTPUT_MAX, "output reaches exactly 2^30 bytes");
    orl_s_reset(5);
    GUARDED(orl_say(6));
    expect(refused_with(ORL_OUTPUT_TOO_LONG, 6), "OUTPUT-TOO-LONG past 2^30, the say's clause");

    /* lists */
    GUARDED(l = orl_l_new(-1, 0, 4));
    expect(refused_with(ORL_NEGATIVE_LENGTH, 4), "l_new(-1) refuses NEGATIVE-LENGTH");
    GUARDED(l = orl_l_new((int64_t)ORL_LIST_MAX + 1, 0, 4));
    expect(refused_with(ORL_LIST_TOO_LONG, 4), "l_new(2^24 + 1) refuses LIST-TOO-LONG");
    l = orl_l_new(3, 7, 4);
    expect(orl_l_len(&l) == 3 && l.v[0] == 7 && l.v[2] == 7, "l_new(3, 7)");
    WRAPPED(v, orl_l_get(&l, 0, 4));
    expect(refused_with(ORL_INDEX_OUT_OF_RANGE, 4), "l_get(0) refuses");
    WRAPPED(v, orl_l_get(&l, 4, 4));
    expect(refused_with(ORL_INDEX_OUT_OF_RANGE, 4), "l_get(len + 1) refuses");
    WRAPPED(v, orl_l_get(&l, INT64_MIN, 4));
    expect(refused_with(ORL_INDEX_OUT_OF_RANGE, 4), "l_get(INT64_MIN) refuses");
    GUARDED(orl_l_set(&l, 2, -1, 4));
    WRAPPED(v, orl_l_get(&l, 2, 4));
    expect(T_code == NULL && v == -1, "l_set then l_get (1-based)");
    GUARDED(orl_l_set(&l, 4, 0, 4));
    expect(refused_with(ORL_INDEX_OUT_OF_RANGE, 4), "l_set(len + 1) refuses");
    cp = orl_l_copy(&l);
    GUARDED(orl_l_push(&l, 5, 4));
    expect(T_code == NULL && orl_l_len(&l) == 4 && l.v[3] == 5 && orl_l_len(&cp) == 3, "l_push; a copy is apart");
    GUARDED(for (i = 0; i < 4; ++i) orl_l_pop(&l, 4));
    expect(T_code == NULL && orl_l_len(&l) == 0, "l_pop to empty");
    GUARDED(orl_l_pop(&l, 8));
    expect(refused_with(ORL_EMPTY_LIST, 8), "l_pop of an empty list refuses EMPTY-LIST");
    orl_l_free(&l);
    orl_l_free(&cp);
    GUARDED(big = orl_l_new((int64_t)ORL_LIST_MAX, 1, 4));
    expect(T_code == NULL && big.len == ORL_LIST_MAX, "l_new(2^24) is allowed");
    GUARDED(orl_l_push(&big, 0, 11));
    expect(refused_with(ORL_LIST_TOO_LONG, 11), "l_push past 2^24 refuses LIST-TOO-LONG");
    orl_l_free(&big);
    l = orl_l_from(3, li);
    expect(orl_l_len(&l) == 3 && l.v[2] == INT64_MIN, "l_from");
    orl_l_free(&l);

    /* list and scalar printing through the builder */
    orl_s_reset(1);
    orl_s_list('I', li, 3);
    expect(builder_is("[1, -2, -9223372036854775808]"), "s_list I");
    lx[0] = (int64_t)1 << 32;
    lx[1] = -((int64_t)1 << 31);
    orl_s_reset(1);
    orl_s_list('X', lx, 2);
    expect(builder_is("[1.0, -0.5]"), "s_list X");
    lf[0] = orl_f_bits(0.5);
    lf[1] = orl_f_bits(-0.0);
    lf[2] = (int64_t)UINT64_C(0x7FF0000000000001);
    lf[3] = (int64_t)ORL__NEG_INF;
    orl_s_reset(1);
    orl_s_list('F', lf, 4);
    expect(builder_is("[0.5, -0.0, NaN, -Infinity]"), "s_list F (a signalling NaN prints NaN)");
    orl_s_reset(1);
    orl_s_list('B', lb, 3);
    expect(builder_is("[true, false, true]"), "s_list B");
    orl_s_reset(1);
    orl_s_list('I', NULL, 0);
    expect(builder_is("[]"), "s_list of no elements");
    orl_s_reset(1);
    orl_s_b(1);
    orl_s_lit(" ", 1);
    orl_s_b(0);
    orl_s_lit(" ", 1);
    orl_s_t(orl_t_lit("\xC3\x98" "rl" "\xC7\xAB" "g", 7));
    expect(builder_is("true false \xC3\x98" "rl" "\xC7\xAB" "g"), "s_b and s_t (raw UTF-8 bytes)");

    /* texts */
    t = orl_s_take();
    expect(orl_t_eq(t, orl_t_lit("true false \xC3\x98" "rl" "\xC7\xAB" "g", 18)), "s_take is the builder's bytes");
    expect(!orl_t_eq(t, orl_t_lit("true false", 10)), "t_eq: different lengths differ");
    expect(orl_t_eq(orl_t_lit("", 0), orl_t_lit(NULL, 0)), "t_eq: two empty texts are equal");
    free((void *)t.p);

    /* the longest Float text: -0. and 1074 digits (1077 bytes), the negative smallest subnormal */
    {
        char neg[ORL_FMT_F_MAX], pos[ORL_FMT_F_MAX];
        size_t nn = orl__fmt_f(neg, orl__bf(UINT64_C(0x8000000000000001)));
        size_t np = orl__fmt_f(pos, orl__bf(UINT64_C(0x0000000000000001)));
        expect(nn == 1077 && np == 1076 && neg[0] == '-' && memcmp(neg + 1, pos, np) == 0 &&
               memcmp(pos, "0.000000", 8) == 0 && pos[np - 1] == '5', "fmt_f of the smallest subnormals (1077 and 1076 bytes)");
    }

    /* a C truth value other than 1 is encoded as the byte 1: the same head as for 1 */
    {
        uint8_t start[32], h1[32], h2[32];
        memcpy(start, orl__head, 32);
        orl_ev_assign_b(3, 1, 1);
        memcpy(h1, orl__head, 32);
        memcpy(orl__head, start, 32);
        orl_ev_assign_b(3, 1, 2);
        memcpy(h2, orl__head, 32);
        expect(memcmp(h1, h2, 32) == 0 && memcmp(h1, start, 32) != 0, "ev_assign_b encodes any nonzero as 1");
    }

    /* NaN canonicalisation in the scalar operations a program can reach */
    expect(orl__fb(orl_f_canon(orl_bits_f((int64_t)UINT64_C(0xFFF8000000000001)))) == ORL__CANON_NAN, "f_canon");
    expect(orl__fb(orl_f_div(0.0, -0.0)) == ORL__CANON_NAN, "f_div 0/0 is the canonical NaN");
    expect(orl__fb(orl_f_div(-1.0, 0.0)) == ORL__NEG_INF, "f_div -1/+0 is -Infinity");
    expect(orl__fb(orl_f_div(1.0, -0.0)) == ORL__NEG_INF, "f_div 1/-0 is -Infinity");

    printf("EXTRA CHECKS %d / %d\n", x_pass, x_total);
}

/* The folder of the executable, from argv[0] (".", when argv[0] names no folder):
   the chain files land beside the harness, whatever the working directory. */
static void exe_dir(const char *argv0, char *out, size_t cap) {
    size_t n = argv0 != NULL ? strlen(argv0) : 0, cut = 0, i;
    int found = 0;
    for (i = 0; i < n; ++i)
        if (argv0[i] == '/' || argv0[i] == '\\') { cut = i; found = 1; }
    out[0] = '\0';
    if (!found || cut == 0) { app(out, cap, found ? "/" : "."); return; }
    app_n(out, cap, argv0, cut);
}

int main(int argc, char **argv) {
    int ok_v, ok_c;
    char dir[1024];
    if (argc < 2) {
        fprintf(stderr, "usage: test_rt VECTORS [CHAIN-DIR]\n");
        return 2;
    }
    orl_test_refuse_hook = T_hook;
    ok_v = run_vectors(argv[1]);
    exe_dir(argv[0], dir, sizeof dir);
    ok_c = chain_check(argc > 2 ? argv[2] : dir);
    extra_checks();
    return (ok_v && ok_c && x_pass == x_total) ? 0 : 1;
}
