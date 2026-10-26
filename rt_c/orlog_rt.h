/*
 * orlog_rt.h -- the C99 runtime of ORLOG OL-0.
 *
 * Contract: RUNTIME-SPEC.md (DECLARED 2026-10-25). Numeric meaning:
 * src/orlog/numeric_ref.py (exact rationals, one rounding at the end).
 * Held by: vectors/runtime-vectors.txt, run by test_rt.c.
 *
 * One header; every function is static (static inline, so that a program that
 * uses only part of the runtime compiles without -Wunused-function); ISO C99
 * only: no __int128, no builtins, no extensions, no pragma but
 * STDC FP_CONTRACT OFF. Signed overflow is never evaluated: every checked
 * operation tests before it computes, and INT64_MIN / -1 and INT64_MIN % -1
 * are never evaluated. 128-bit products and quotients are built from uint64_t
 * halves. A conversion to double never relies on the cast's rounding: the
 * integer is rounded by integer arithmetic to at most 53 bits, then ldexp
 * scales it exactly. Floats print exactly through a base-10^9 bignum. SHA-256
 * is implemented here.
 *
 * Include this header before any other header: on Windows it defines
 * _CRT_SECURE_NO_WARNINGS, which must precede the C library's first header or
 * fopen is reported as deprecated.
 *
 * Refusals. Every refusable operation has a pure form
 *     orl__NAME(args..., const char **e)
 * that returns its value and sets *e to NULL or to the refusal code, and the
 * contract's wrapper orl_NAME(args..., c) that calls orl_refuse(*e, c).
 * With ORL_TEST defined, orl_refuse and orl_finish call orl_test_refuse_hook
 * (when it is set) after the receipt is written and the files are closed and
 * before exit, so that a harness can observe a refusal (for example by
 * longjmp out of the hook). Without ORL_TEST there is no hook.
 */
#ifndef ORLOG_RT_H
#define ORLOG_RT_H

#if defined(_WIN32) && !defined(_CRT_SECURE_NO_WARNINGS)
#define _CRT_SECURE_NO_WARNINGS 1
#endif

#include <float.h>

#if FLT_EVAL_METHOD != 0
#error "orlog_rt.h: FLT_EVAL_METHOD must be 0 (every double operation evaluated in binary64)"
#endif
#pragma STDC FP_CONTRACT OFF

#include <limits.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#if FLT_RADIX != 2 || DBL_MANT_DIG != 53 || DBL_MAX_EXP != 1024 || DBL_MIN_EXP != -1021
#error "orlog_rt.h: double must be IEEE 754 binary64"
#endif
#if CHAR_BIT != 8
#error "orlog_rt.h: a byte must have 8 bits"
#endif

/* ================================================================ types and limits */

typedef struct { const uint8_t *p; uint32_t n; } orl_text;
typedef struct { int64_t *v; uint64_t len, cap; } orl_list;

#define ORL_LIST_MAX   ((uint64_t)1 << 24)
#define ORL_TEXT_MAX   ((uint32_t)1 << 24)
#define ORL_OUTPUT_MAX ((uint64_t)1 << 30)
#define ORL_FMT_I_MAX  24      /* "-9223372036854775808" is 20 bytes */
#define ORL_FMT_X_MAX  48      /* sign, 10 integer digits, '.', 32 fraction digits: 44 */
#define ORL_FMT_F_MAX  1100    /* the longest is "-0." and 1074 digits: 1077 bytes */

#define ORL_OVERFLOW           "OVERFLOW"
#define ORL_DIVISION_BY_ZERO   "DIVISION-BY-ZERO"
#define ORL_INEXACT_DIVISION   "INEXACT-DIVISION"
#define ORL_NEGATIVE_SQRT      "NEGATIVE-SQRT"
#define ORL_INEXACT_CONVERSION "INEXACT-CONVERSION"
#define ORL_NOT_FINITE         "NOT-FINITE"
#define ORL_INDEX_OUT_OF_RANGE "INDEX-OUT-OF-RANGE"
#define ORL_EMPTY_LIST         "EMPTY-LIST"
#define ORL_NEGATIVE_LENGTH    "NEGATIVE-LENGTH"
#define ORL_LIST_TOO_LONG      "LIST-TOO-LONG"
#define ORL_TEXT_TOO_LONG      "TEXT-TOO-LONG"
#define ORL_OUTPUT_TOO_LONG    "OUTPUT-TOO-LONG"
#define ORL_CLAIM_REFUTED      "CLAIM-REFUTED"
#define ORL_MUST_FAILED        "MUST-FAILED"

#define ORL__TWO63      ((uint64_t)1 << 63)
#define ORL__LOW32      UINT64_C(0xFFFFFFFF)
#define ORL__HALF32     UINT64_C(0x80000000)
#define ORL__EXP_MASK   UINT64_C(0x7FF0000000000000)
#define ORL__FRAC_MASK  UINT64_C(0x000FFFFFFFFFFFFF)
#define ORL__CANON_NAN  UINT64_C(0x7FF8000000000000)
#define ORL__POS_INF    UINT64_C(0x7FF0000000000000)
#define ORL__NEG_INF    UINT64_C(0xFFF0000000000000)

/* ================================================================ basics */

static const char orl__hexd[17] = "0123456789abcdef";

/* A misuse of the runtime by the generated code, or an allocation that fails:
   neither is a refusal of the contract. Message on stderr, exit status 3. */
static inline void orl__fatal(const char *what) {
    fputs("orlog: runtime error: ", stderr);
    fputs(what, stderr);
    fputc('\n', stderr);
    exit(3);
}

static inline void *orl__alloc(size_t n) {
    void *p = malloc(n ? n : 1);
    if (p == NULL) orl__fatal("out of memory");
    return p;
}

static inline void *orl__regrow(void *q, size_t n) {
    void *p = realloc(q, n ? n : 1);
    if (p == NULL) orl__fatal("out of memory");
    return p;
}

static inline void orl__be32(uint8_t *p, uint32_t v) {
    p[0] = (uint8_t)(v >> 24);
    p[1] = (uint8_t)(v >> 16);
    p[2] = (uint8_t)(v >> 8);
    p[3] = (uint8_t)v;
}

static inline void orl__be64(uint8_t *p, uint64_t v) {
    orl__be32(p, (uint32_t)(v >> 32));
    orl__be32(p + 4, (uint32_t)(v & ORL__LOW32));
}

/* Decimal digits of v; returns the length (at most 20). No terminator. */
static inline size_t orl__fmt_u64(char *buf, uint64_t v) {
    char t[20];
    size_t n = 0, i;
    do {
        t[n++] = (char)('0' + (int)(v % 10u));
        v /= 10u;
    } while (v != 0);
    for (i = 0; i < n; ++i) buf[i] = t[n - 1 - i];
    return n;
}

/* |a| as an unsigned value; 2^63 for INT64_MIN. Never negates a signed value. */
static inline uint64_t orl__mag(int64_t a) {
    return a < 0 ? (uint64_t)0 - (uint64_t)a : (uint64_t)a;
}

/* neg ? -m : m as int64_t, or OVERFLOW when it is outside [-2^63, 2^63 - 1]. */
static inline int64_t orl__signed(int neg, uint64_t m, const char **e) {
    if (neg) {
        if (m > ORL__TWO63) { *e = ORL_OVERFLOW; return 0; }
        if (m == ORL__TWO63) return INT64_MIN;
        return -(int64_t)m;
    }
    if (m > (uint64_t)INT64_MAX) { *e = ORL_OVERFLOW; return 0; }
    return (int64_t)m;
}

static inline uint64_t orl__fb(double x) { uint64_t u; memcpy(&u, &x, sizeof u); return u; }
static inline double orl__bf(uint64_t u) { double x; memcpy(&x, &u, sizeof x); return x; }

static inline int orl__isnan_bits(uint64_t u) {
    return (u & ORL__EXP_MASK) == ORL__EXP_MASK && (u & ORL__FRAC_MASK) != 0;
}

/* ================================================================ SHA-256 (FIPS 180-4) */

typedef struct { uint32_t s[8]; uint64_t n; uint8_t b[64]; size_t bl; } orl__sha256;

static const uint32_t orl__sha_k[64] = {
    0x428a2f98u, 0x71374491u, 0xb5c0fbcfu, 0xe9b5dba5u, 0x3956c25bu, 0x59f111f1u, 0x923f82a4u, 0xab1c5ed5u,
    0xd807aa98u, 0x12835b01u, 0x243185beu, 0x550c7dc3u, 0x72be5d74u, 0x80deb1feu, 0x9bdc06a7u, 0xc19bf174u,
    0xe49b69c1u, 0xefbe4786u, 0x0fc19dc6u, 0x240ca1ccu, 0x2de92c6fu, 0x4a7484aau, 0x5cb0a9dcu, 0x76f988dau,
    0x983e5152u, 0xa831c66du, 0xb00327c8u, 0xbf597fc7u, 0xc6e00bf3u, 0xd5a79147u, 0x06ca6351u, 0x14292967u,
    0x27b70a85u, 0x2e1b2138u, 0x4d2c6dfcu, 0x53380d13u, 0x650a7354u, 0x766a0abbu, 0x81c2c92eu, 0x92722c85u,
    0xa2bfe8a1u, 0xa81a664bu, 0xc24b8b70u, 0xc76c51a3u, 0xd192e819u, 0xd6990624u, 0xf40e3585u, 0x106aa070u,
    0x19a4c116u, 0x1e376c08u, 0x2748774cu, 0x34b0bcb5u, 0x391c0cb3u, 0x4ed8aa4au, 0x5b9cca4fu, 0x682e6ff3u,
    0x748f82eeu, 0x78a5636fu, 0x84c87814u, 0x8cc70208u, 0x90befffau, 0xa4506cebu, 0xbef9a3f7u, 0xc67178f2u
};

static inline uint32_t orl__ror(uint32_t x, int n) {
    return (uint32_t)((x >> n) | (x << (32 - n)));
}

static inline void orl__sha_block(uint32_t s[8], const uint8_t *p) {
    uint32_t w[64], a, b, c, d, e, f, g, h;
    int i;
    for (i = 0; i < 16; ++i)
        w[i] = ((uint32_t)p[4 * i] << 24) | ((uint32_t)p[4 * i + 1] << 16) |
               ((uint32_t)p[4 * i + 2] << 8) | (uint32_t)p[4 * i + 3];
    for (i = 16; i < 64; ++i) {
        uint32_t s0 = orl__ror(w[i - 15], 7) ^ orl__ror(w[i - 15], 18) ^ (w[i - 15] >> 3);
        uint32_t s1 = orl__ror(w[i - 2], 17) ^ orl__ror(w[i - 2], 19) ^ (w[i - 2] >> 10);
        w[i] = (uint32_t)(w[i - 16] + s0 + w[i - 7] + s1);
    }
    a = s[0]; b = s[1]; c = s[2]; d = s[3]; e = s[4]; f = s[5]; g = s[6]; h = s[7];
    for (i = 0; i < 64; ++i) {
        uint32_t S1 = orl__ror(e, 6) ^ orl__ror(e, 11) ^ orl__ror(e, 25);
        uint32_t ch = (e & f) ^ (~e & g);
        uint32_t t1 = (uint32_t)(h + S1 + ch + orl__sha_k[i] + w[i]);
        uint32_t S0 = orl__ror(a, 2) ^ orl__ror(a, 13) ^ orl__ror(a, 22);
        uint32_t mj = (a & b) ^ (a & c) ^ (b & c);
        uint32_t t2 = (uint32_t)(S0 + mj);
        h = g; g = f; f = e; e = (uint32_t)(d + t1);
        d = c; c = b; b = a; a = (uint32_t)(t1 + t2);
    }
    s[0] += a; s[1] += b; s[2] += c; s[3] += d; s[4] += e; s[5] += f; s[6] += g; s[7] += h;
}

static inline void orl__sha_init(orl__sha256 *h) {
    h->s[0] = 0x6a09e667u; h->s[1] = 0xbb67ae85u; h->s[2] = 0x3c6ef372u; h->s[3] = 0xa54ff53au;
    h->s[4] = 0x510e527fu; h->s[5] = 0x9b05688cu; h->s[6] = 0x1f83d9abu; h->s[7] = 0x5be0cd19u;
    h->n = 0;
    h->bl = 0;
}

static inline void orl__sha_update(orl__sha256 *h, const void *data, size_t n) {
    const uint8_t *p = (const uint8_t *)data;
    if (n == 0) return;
    h->n += (uint64_t)n;
    if (h->bl != 0) {
        size_t take = 64 - h->bl;
        if (take > n) take = n;
        memcpy(h->b + h->bl, p, take);
        h->bl += take;
        p += take;
        n -= take;
        if (h->bl < 64) return;
        orl__sha_block(h->s, h->b);
        h->bl = 0;
    }
    while (n >= 64) {
        orl__sha_block(h->s, p);
        p += 64;
        n -= 64;
    }
    if (n != 0) {
        memcpy(h->b, p, n);
        h->bl = n;
    }
}

/* Finishes h (which must not be used afterwards) and writes the digest. */
static inline void orl__sha_final(orl__sha256 *h, uint8_t out[32]) {
    uint8_t pad[72];
    uint64_t bits = h->n * 8u;
    size_t padlen = h->bl < 56 ? 56 - h->bl : 120 - h->bl;
    int i;
    memset(pad, 0, sizeof pad);
    pad[0] = 0x80;
    for (i = 0; i < 8; ++i) pad[padlen + (size_t)i] = (uint8_t)(bits >> (56 - 8 * i));
    orl__sha_update(h, pad, padlen + 8);
    for (i = 0; i < 8; ++i) orl__be32(out + 4 * i, h->s[i]);
}

static inline void orl__sha256_once(const void *p, size_t n, uint8_t out[32]) {
    orl__sha256 h;
    orl__sha_init(&h);
    orl__sha_update(&h, p, n);
    orl__sha_final(&h, out);
}

/* ================================================================ run state */

typedef struct { uint32_t clause, ref_clause; uint64_t evals, trues, cost, ref_cost; } orl__claim_rec;

/* The operation counter of the contract: only the generated code changes it. */
static uint64_t orl_ops;

static FILE *orl__out, *orl__rcpt, *orl__trc;
static const char *orl__backend = "";
static uint8_t orl__law[32];
static char orl__law_hex[65], orl__text_hex[65];
static orl__sha256 orl__out_hash;
static uint64_t orl__out_bytes;
static uint8_t orl__head[32];
static uint64_t orl__events;
static orl__claim_rec *orl__claims;
static uint32_t orl__n_claims;
static uint8_t *orl__sb;
static uint32_t orl__sb_len, orl__sb_cap, orl__sb_clause;

#ifdef ORL_TEST
/* Called by orl_refuse (code, clause) and orl_finish (NULL, 0) just before exit. */
static void (*orl_test_refuse_hook)(const char *code, uint32_t c);
#endif

/* ================================================================ the event hash chain */

static inline void orl__trace_hex(const uint8_t *p, size_t n) {
    char buf[1024];
    size_t k = 0, i;
    for (i = 0; i < n; ++i) {
        buf[k++] = orl__hexd[p[i] >> 4];
        buf[k++] = orl__hexd[p[i] & 15u];
        if (k == sizeof buf) {
            fwrite(buf, 1, k, orl__trc);
            k = 0;
        }
    }
    if (k != 0) fwrite(buf, 1, k, orl__trc);
}

typedef struct { orl__sha256 h; uint32_t len, put; } orl__ev;

/* head = SHA-256(head || kind || clause (u32 BE) || len (u32 BE) || payload) */
static inline void orl__ev_begin(orl__ev *x, int kind, uint32_t c, uint32_t len) {
    uint8_t hd[9];
    orl__sha_init(&x->h);
    orl__sha_update(&x->h, orl__head, 32);
    hd[0] = (uint8_t)kind;
    orl__be32(hd + 1, c);
    orl__be32(hd + 5, len);
    orl__sha_update(&x->h, hd, 9);
    x->len = len;
    x->put = 0;
    if (orl__trc != NULL) {
        char num[24];
        fwrite(num, 1, orl__fmt_u64(num, orl__events + 1), orl__trc);
        fputc(' ', orl__trc);
        fputc(kind, orl__trc);
        fputc(' ', orl__trc);
        fwrite(num, 1, orl__fmt_u64(num, c), orl__trc);
        fputc(' ', orl__trc);
        if (len == 0) fputc('-', orl__trc);
    }
}

static inline void orl__ev_put(orl__ev *x, const void *p, size_t n) {
    if (n == 0) return;
    if (n > (size_t)(x->len - x->put)) orl__fatal("event payload longer than its length");
    orl__sha_update(&x->h, p, n);
    x->put += (uint32_t)n;
    if (orl__trc != NULL) orl__trace_hex((const uint8_t *)p, n);
}

static inline void orl__ev_end(orl__ev *x) {
    if (x->put != x->len) orl__fatal("event payload shorter than its length");
    orl__sha_final(&x->h, orl__head);
    orl__events += 1;
    if (orl__trc != NULL) {
        fputc(' ', orl__trc);
        orl__trace_hex(orl__head, 32);
        fputc('\n', orl__trc);
    }
}

static inline void orl__event(int kind, uint32_t c, const void *p, size_t n) {
    orl__ev x;
    if (n > UINT32_MAX) orl__fatal("event payload too long");
    orl__ev_begin(&x, kind, c, (uint32_t)n);
    orl__ev_put(&x, p, n);
    orl__ev_end(&x);
}

/* ================================================================ receipt, refusal, finish */

static inline void orl__put_hex(FILE *f, const uint8_t *p, size_t n) {
    size_t i;
    for (i = 0; i < n; ++i) {
        fputc(orl__hexd[p[i] >> 4], f);
        fputc(orl__hexd[p[i] & 15u], f);
    }
}

static inline void orl__put_key_u64(FILE *f, const char *key, uint64_t v) {
    char num[24];
    fputs(key, f);
    fputc(' ', f);
    fwrite(num, 1, orl__fmt_u64(num, v), f);
    fputc('\n', f);
}

static inline void orl__receipt(const char *code, uint32_t c) {
    FILE *f = orl__rcpt;
    orl__sha256 t;
    uint8_t oh[32];
    char num[24];
    uint32_t i;
    if (f == NULL) return;
    t = orl__out_hash;
    orl__sha_final(&t, oh);
    fputs("orlog-receipt 0\n", f);
    fputs("backend ", f); fputs(orl__backend, f); fputc('\n', f);
    fputs("law-seal ", f); fputs(orl__law_hex, f); fputc('\n', f);
    fputs("text-seal ", f); fputs(orl__text_hex, f); fputc('\n', f);
    if (code != NULL) {
        fputs("status REFUSED ", f);
        fputs(code, f);
        fputc(' ', f);
        fwrite(num, 1, orl__fmt_u64(num, c), f);
        fputc('\n', f);
    } else {
        fputs("status COMPLETED\n", f);
    }
    orl__put_key_u64(f, "output-bytes", orl__out_bytes);
    fputs("output-sha256 ", f); orl__put_hex(f, oh, 32); fputc('\n', f);
    orl__put_key_u64(f, "events", orl__events);
    fputs("trace-head ", f); orl__put_hex(f, orl__head, 32); fputc('\n', f);
    orl__put_key_u64(f, "ops", orl_ops);
    orl__put_key_u64(f, "claims", orl__n_claims);
    for (i = 0; i < orl__n_claims; ++i) {
        const orl__claim_rec *r = &orl__claims[i];
        uint64_t v[7];
        int k;
        v[0] = i; v[1] = r->clause; v[2] = r->evals; v[3] = r->trues;
        v[4] = r->cost; v[5] = r->ref_clause; v[6] = r->ref_cost;
        fputs("claim", f);
        for (k = 0; k < 7; ++k) {
            fputc(' ', f);
            fwrite(num, 1, orl__fmt_u64(num, v[k]), f);
        }
        fputc('\n', f);
    }
    fputs("end\n", f);
}

/* Flushes and closes *pf; returns 1 when a write or the close failed. */
static inline int orl__close(FILE **pf) {
    int bad = 0;
    if (*pf != NULL) {
        if (fflush(*pf) != 0 || ferror(*pf)) bad = 1;
        if (fclose(*pf) != 0) bad = 1;
        *pf = NULL;
    }
    return bad;
}

/* Output and trace are closed first; the receipt is written only when they
   were written whole, so that a receipt never describes a file that failed. */
static inline void orl__end(const char *code, uint32_t c) {
    int bad = 0;
    bad |= orl__close(&orl__out);
    bad |= orl__close(&orl__trc);
    if (!bad) orl__receipt(code, c);
    bad |= orl__close(&orl__rcpt);
#ifdef ORL_TEST
    if (orl_test_refuse_hook != NULL) orl_test_refuse_hook(code, c);
#endif
    if (bad) {
        fputs("orlog: a file could not be written\n", stderr);
        exit(2);
    }
    exit(0);
}

/* Never returns: event 'R', the receipt with "status REFUSED <code> <c>", exit 0. */
static inline void orl_refuse(const char *code, uint32_t c) {
    orl__event('R', c, code, strlen(code));
    orl__end(code, c);
}

/* Never returns: the receipt with "status COMPLETED", exit 0. */
static inline void orl_finish(void) {
    orl__end(NULL, 0);
}

/* ================================================================ Int */

static inline int64_t orl__i_add(int64_t a, int64_t b, const char **e) {
    *e = NULL;
    if ((b > 0 && a > INT64_MAX - b) || (b < 0 && a < INT64_MIN - b)) { *e = ORL_OVERFLOW; return 0; }
    return a + b;
}

static inline int64_t orl__i_sub(int64_t a, int64_t b, const char **e) {
    *e = NULL;
    if ((b < 0 && a > INT64_MAX + b) || (b > 0 && a < INT64_MIN + b)) { *e = ORL_OVERFLOW; return 0; }
    return a - b;
}

/* The 128-bit product of two 64-bit unsigned values, from 32-bit halves. */
static inline void orl__mul64(uint64_t a, uint64_t b, uint64_t *hi, uint64_t *lo) {
    uint64_t a0 = a & ORL__LOW32, a1 = a >> 32, b0 = b & ORL__LOW32, b1 = b >> 32;
    uint64_t p00 = a0 * b0, p01 = a0 * b1, p10 = a1 * b0, p11 = a1 * b1;
    uint64_t mid = (p00 >> 32) + (p01 & ORL__LOW32) + (p10 & ORL__LOW32);
    *lo = (mid << 32) | (p00 & ORL__LOW32);
    *hi = p11 + (p01 >> 32) + (p10 >> 32) + (mid >> 32);
}

/* (nh:nl) = d * (qh:ql) + r with 0 <= r < d; d != 0. */
static inline void orl__divmod128(uint64_t nh, uint64_t nl, uint64_t d,
                                  uint64_t *qh, uint64_t *ql, uint64_t *r) {
    uint64_t rem, q = 0;
    int i;
    *qh = nh / d;
    rem = nh % d;
    for (i = 63; i >= 0; --i) {
        uint64_t top = rem >> 63;                 /* 2*rem + bit would not fit */
        rem = (rem << 1) | ((nl >> i) & 1u);
        if (top != 0 || rem >= d) {
            rem -= d;                             /* exact modulo 2^64: the true value is < d */
            q |= (uint64_t)1 << i;
        }
    }
    *ql = q;
    *r = rem;
}

/* floor(sqrt(hi:lo)), two bits at a time. Requires (hi:lo) < 2^120, so that the
   root is < 2^60 and the remainder (<= 2*root) shifted by two fits in 64 bits.
   Callers pass at most 2^95. */
static inline uint64_t orl__isqrt128(uint64_t hi, uint64_t lo) {
    uint64_t root = 0, rem = 0;
    int i;
    for (i = 63; i >= 0; --i) {
        uint64_t two = i >= 32 ? (hi >> (2 * (i - 32))) & 3u : (lo >> (2 * i)) & 3u;
        uint64_t trial;
        rem = (rem << 2) | two;
        trial = (root << 2) | 1u;
        root <<= 1;
        if (rem >= trial) {
            rem -= trial;
            root |= 1u;
        }
    }
    return root;
}

static inline int64_t orl__i_mul(int64_t a, int64_t b, const char **e) {
    uint64_t hi, lo;
    *e = NULL;
    orl__mul64(orl__mag(a), orl__mag(b), &hi, &lo);
    if (hi != 0) { *e = ORL_OVERFLOW; return 0; }
    return orl__signed((a < 0) != (b < 0), lo, e);
}

static inline int64_t orl__i_neg(int64_t a, const char **e) {
    *e = NULL;
    if (a == INT64_MIN) { *e = ORL_OVERFLOW; return 0; }
    return -a;
}

static inline int64_t orl__i_abs(int64_t a, const char **e) {
    *e = NULL;
    if (a == INT64_MIN) { *e = ORL_OVERFLOW; return 0; }
    return a < 0 ? -a : a;
}

/* The exact quotient: DIVISION-BY-ZERO, then INEXACT-DIVISION, then OVERFLOW. */
static inline int64_t orl__i_div(int64_t a, int64_t b, const char **e) {
    *e = NULL;
    if (b == 0) { *e = ORL_DIVISION_BY_ZERO; return 0; }
    if (b == -1) {                                /* never inexact; a % -1 is never evaluated */
        if (a == INT64_MIN) { *e = ORL_OVERFLOW; return 0; }
        return -a;
    }
    if (a % b != 0) { *e = ORL_INEXACT_DIVISION; return 0; }
    return a / b;
}

/* Euclidean: a = b*q + r with 0 <= r < |b|. Only (INT64_MIN, -1) overflows q. */
static inline int64_t orl__i_quot(int64_t a, int64_t b, const char **e) {
    int64_t q, r;
    *e = NULL;
    if (b == 0) { *e = ORL_DIVISION_BY_ZERO; return 0; }
    if (b == -1) {
        if (a == INT64_MIN) { *e = ORL_OVERFLOW; return 0; }
        return -a;
    }
    q = a / b;
    r = a % b;
    if (r < 0) q = b > 0 ? q - 1 : q + 1;
    return q;
}

static inline int64_t orl__i_rem(int64_t a, int64_t b, const char **e) {
    int64_t r;
    *e = NULL;
    if (b == 0) { *e = ORL_DIVISION_BY_ZERO; return 0; }
    if (b == -1) return 0;
    r = a % b;
    if (r < 0) r = b > 0 ? r + b : r - b;         /* r - b with b = INT64_MIN is r + 2^63 > 0 */
    return r;
}

static inline int64_t orl__i_isqrt(int64_t a, const char **e) {
    *e = NULL;
    if (a < 0) { *e = ORL_NEGATIVE_SQRT; return 0; }
    return (int64_t)orl__isqrt128(0, (uint64_t)a);
}

static inline int64_t orl_i_add(int64_t a, int64_t b, uint32_t c) {
    const char *e; int64_t r = orl__i_add(a, b, &e); if (e) orl_refuse(e, c); return r;
}
static inline int64_t orl_i_sub(int64_t a, int64_t b, uint32_t c) {
    const char *e; int64_t r = orl__i_sub(a, b, &e); if (e) orl_refuse(e, c); return r;
}
static inline int64_t orl_i_mul(int64_t a, int64_t b, uint32_t c) {
    const char *e; int64_t r = orl__i_mul(a, b, &e); if (e) orl_refuse(e, c); return r;
}
static inline int64_t orl_i_neg(int64_t a, uint32_t c) {
    const char *e; int64_t r = orl__i_neg(a, &e); if (e) orl_refuse(e, c); return r;
}
static inline int64_t orl_i_abs(int64_t a, uint32_t c) {
    const char *e; int64_t r = orl__i_abs(a, &e); if (e) orl_refuse(e, c); return r;
}
static inline int64_t orl_i_div(int64_t a, int64_t b, uint32_t c) {
    const char *e; int64_t r = orl__i_div(a, b, &e); if (e) orl_refuse(e, c); return r;
}
static inline int64_t orl_i_quot(int64_t a, int64_t b, uint32_t c) {
    const char *e; int64_t r = orl__i_quot(a, b, &e); if (e) orl_refuse(e, c); return r;
}
static inline int64_t orl_i_rem(int64_t a, int64_t b, uint32_t c) {
    const char *e; int64_t r = orl__i_rem(a, b, &e); if (e) orl_refuse(e, c); return r;
}
static inline int64_t orl_i_isqrt(int64_t a, uint32_t c) {
    const char *e; int64_t r = orl__i_isqrt(a, &e); if (e) orl_refuse(e, c); return r;
}
static inline int64_t orl_i_max(int64_t a, int64_t b) { return a > b ? a : b; }
static inline int64_t orl_i_min(int64_t a, int64_t b) { return a < b ? a : b; }

/* ================================================================ Fix (raw int64 = value * 2^32) */

static inline int64_t orl__x_from_i(int64_t n, const char **e) {
    *e = NULL;
    if (n < -((int64_t)1 << 31) || n > ((int64_t)1 << 31) - 1) { *e = ORL_OVERFLOW; return 0; }
    return n * ((int64_t)1 << 32);
}

/* round-half-even(a*b / 2^32) */
static inline int64_t orl__x_mul(int64_t a, int64_t b, const char **e) {
    uint64_t hi, lo, qh, ql, f;
    *e = NULL;
    orl__mul64(orl__mag(a), orl__mag(b), &hi, &lo);
    qh = hi >> 32;
    ql = (hi << 32) | (lo >> 32);
    f = lo & ORL__LOW32;
    if (f > ORL__HALF32 || (f == ORL__HALF32 && (ql & 1u) != 0)) {
        ql += 1;
        if (ql == 0) qh += 1;
    }
    if (qh != 0) { *e = ORL_OVERFLOW; return 0; }
    return orl__signed((a < 0) != (b < 0), ql, e);
}

/* round-half-even(a*2^32 / b); DIVISION-BY-ZERO first */
static inline int64_t orl__x_div(int64_t a, int64_t b, const char **e) {
    uint64_t ua, ub, qh, ql, r;
    *e = NULL;
    if (b == 0) { *e = ORL_DIVISION_BY_ZERO; return 0; }
    ua = orl__mag(a);
    ub = orl__mag(b);
    orl__divmod128(ua >> 32, ua << 32, ub, &qh, &ql, &r);
    if (r > ub - r || (r == ub - r && (ql & 1u) != 0)) {   /* 2r > b, or a tie and q odd */
        ql += 1;
        if (ql == 0) qh += 1;
    }
    if (qh != 0) { *e = ORL_OVERFLOW; return 0; }
    return orl__signed((a < 0) != (b < 0), ql, e);
}

/* isqrt(a * 2^32) */
static inline int64_t orl__x_sqrt(int64_t a, const char **e) {
    uint64_t u;
    *e = NULL;
    if (a < 0) { *e = ORL_NEGATIVE_SQRT; return 0; }
    u = (uint64_t)a;
    return (int64_t)orl__isqrt128(u >> 32, u << 32);
}

static inline int64_t orl_x_from_i(int64_t n, uint32_t c) {
    const char *e; int64_t r = orl__x_from_i(n, &e); if (e) orl_refuse(e, c); return r;
}
static inline int64_t orl_x_add(int64_t a, int64_t b, uint32_t c) {
    const char *e; int64_t r = orl__i_add(a, b, &e); if (e) orl_refuse(e, c); return r;
}
static inline int64_t orl_x_sub(int64_t a, int64_t b, uint32_t c) {
    const char *e; int64_t r = orl__i_sub(a, b, &e); if (e) orl_refuse(e, c); return r;
}
static inline int64_t orl_x_neg(int64_t a, uint32_t c) {
    const char *e; int64_t r = orl__i_neg(a, &e); if (e) orl_refuse(e, c); return r;
}
static inline int64_t orl_x_abs(int64_t a, uint32_t c) {
    const char *e; int64_t r = orl__i_abs(a, &e); if (e) orl_refuse(e, c); return r;
}
static inline int64_t orl_x_mul(int64_t a, int64_t b, uint32_t c) {
    const char *e; int64_t r = orl__x_mul(a, b, &e); if (e) orl_refuse(e, c); return r;
}
static inline int64_t orl_x_div(int64_t a, int64_t b, uint32_t c) {
    const char *e; int64_t r = orl__x_div(a, b, &e); if (e) orl_refuse(e, c); return r;
}
static inline int64_t orl_x_sqrt(int64_t a, uint32_t c) {
    const char *e; int64_t r = orl__x_sqrt(a, &e); if (e) orl_refuse(e, c); return r;
}

/* To Int toward zero. C99 division truncates toward zero; the divisor is 2^32. */
static inline int64_t orl_x_trunc(int64_t a) { return a / ((int64_t)1 << 32); }

/* To Int, half-even. |result| <= 2^31: no refusal. */
static inline int64_t orl_x_round(int64_t a) {
    uint64_t u = orl__mag(a), q = u >> 32, f = u & ORL__LOW32;
    if (f > ORL__HALF32 || (f == ORL__HALF32 && (q & 1u) != 0)) q += 1;
    return a < 0 ? -(int64_t)q : (int64_t)q;
}

static inline int64_t orl_x_max(int64_t a, int64_t b) { return a > b ? a : b; }
static inline int64_t orl_x_min(int64_t a, int64_t b) { return a < b ? a : b; }

/* ================================================================ Float */

static inline double orl_f_canon(double x) {
    return orl__isnan_bits(orl__fb(x)) ? orl__bf(ORL__CANON_NAN) : x;
}
static inline double orl_f_add(double a, double b) { return orl_f_canon(a + b); }
static inline double orl_f_sub(double a, double b) { return orl_f_canon(a - b); }
static inline double orl_f_mul(double a, double b) { return orl_f_canon(a * b); }

/* IEEE division; division by a signed zero is written out (as in numeric_ref)
   rather than left to the C division, whose zero divisor C99 leaves undefined
   outside Annex F. */
static inline double orl_f_div(double a, double b) {
    if (b == 0.0) {
        if (orl__isnan_bits(orl__fb(a)) || a == 0.0) return orl__bf(ORL__CANON_NAN);
        return ((orl__fb(a) ^ orl__fb(b)) >> 63) != 0 ? orl__bf(ORL__NEG_INF) : orl__bf(ORL__POS_INF);
    }
    return orl_f_canon(a / b);
}

static inline double orl_f_neg(double a) { return orl_f_canon(-a); }
static inline double orl_f_abs(double a) { return orl_f_canon(fabs(a)); }

/* Correctly rounded (IEEE 754); sqrt(-0.0) = -0.0; a NaN or a negative gives NaN. */
static inline double orl_f_sqrt(double a) {
    if (orl__isnan_bits(orl__fb(a)) || a < 0.0) return orl__bf(ORL__CANON_NAN);
    return sqrt(a);
}

/* By the comparison, not by fmax: a NaN operand may come back as it is. */
static inline double orl_f_max(double a, double b) { return a > b ? a : b; }
static inline double orl_f_min(double a, double b) { return a < b ? a : b; }

static inline int64_t orl_f_bits(double x) { int64_t i; memcpy(&i, &x, sizeof i); return i; }
static inline double orl_bits_f(int64_t i) { double x; memcpy(&x, &i, sizeof x); return x; }

/* n * 2^scale as a double, for |n * 2^scale| in the normal range or zero.
   Exact or INEXACT-CONVERSION; rounded: nearest, ties to even. The integer is
   rounded to at most 53 bits by integer arithmetic; the cast of that integer
   and ldexp by a power of two are then both exact. */
static inline double orl__i_to_f(int64_t n, int scale, int rounded, const char **e) {
    uint64_t u = orl__mag(n), m = u;
    int shift = 0;
    double r;
    *e = NULL;
    if (u >= ((uint64_t)1 << 53)) {
        uint64_t t = u >> 53, rem, half;
        while (t != 0) { shift++; t >>= 1; }       /* shift = bit length of u - 53, 1..11 */
        m = u >> shift;
        rem = u & (((uint64_t)1 << shift) - 1);
        if (rem != 0) {
            if (!rounded) { *e = ORL_INEXACT_CONVERSION; return 0.0; }
            half = (uint64_t)1 << (shift - 1);
            if (rem > half || (rem == half && (m & 1u) != 0)) {
                m += 1;
                if (m == ((uint64_t)1 << 53)) { m >>= 1; shift += 1; }
            }
        }
    }
    r = ldexp((double)(int64_t)m, shift + scale);
    return n < 0 ? -r : r;
}

#define ORL__EXACT 0
#define ORL__ROUND 1
#define ORL__TRUNC 2

/* x * 2^scale to Int: NOT-FINITE; then exact (INEXACT-CONVERSION), half-even
   or toward zero; then OVERFLOW. Works on the bits: |x| = m * 2^k. */
static inline int64_t orl__f_to_i(double x, int scale, int mode, const char **e) {
    uint64_t u = orl__fb(x), m, q, r;
    int neg = (int)(u >> 63), ex = (int)((u >> 52) & 0x7FFu), k, s;
    *e = NULL;
    if (ex == 0x7FF) { *e = ORL_NOT_FINITE; return 0; }
    m = u & ORL__FRAC_MASK;
    if (ex == 0) k = -1074;
    else { m |= (uint64_t)1 << 52; k = ex - 1075; }
    if (m == 0) return 0;
    k += scale;
    if (k >= 0) {                                  /* an integer: only OVERFLOW can refuse */
        uint64_t limit = neg ? ORL__TWO63 : ORL__TWO63 - 1;
        if (k > 63 || m > (limit >> k)) { *e = ORL_OVERFLOW; return 0; }
        return orl__signed(neg, m << k, e);
    }
    s = -k;
    if (s >= 64) { q = 0; r = m; }
    else { q = m >> s; r = m & (((uint64_t)1 << s) - 1); }
    if (r != 0) {
        if (mode == ORL__EXACT) { *e = ORL_INEXACT_CONVERSION; return 0; }
        if (mode == ORL__ROUND && s < 64) {        /* s >= 64: r < 2^53 < half, rounds down */
            uint64_t half = (uint64_t)1 << (s - 1);
            if (r > half || (r == half && (q & 1u) != 0)) q += 1;
        }
    }
    return orl__signed(neg, q, e);
}

static inline double orl__x_to_f(int64_t a, int rounded, const char **e) { return orl__i_to_f(a, -32, rounded, e); }
static inline double orl__f_from_i(int64_t n, int rounded, const char **e) { return orl__i_to_f(n, 0, rounded, e); }
static inline int64_t orl__f_to_x(double x, int rounded, const char **e) {
    return orl__f_to_i(x, 32, rounded ? ORL__ROUND : ORL__EXACT, e);
}
static inline int64_t orl__f_trunc(double x, const char **e) { return orl__f_to_i(x, 0, ORL__TRUNC, e); }
static inline int64_t orl__f_round(double x, const char **e) { return orl__f_to_i(x, 0, ORL__ROUND, e); }

static inline double orl_x_to_f(int64_t a, int rounded, uint32_t c) {
    const char *e; double r = orl__x_to_f(a, rounded, &e); if (e) orl_refuse(e, c); return r;
}
static inline int64_t orl_f_to_x(double x, int rounded, uint32_t c) {
    const char *e; int64_t r = orl__f_to_x(x, rounded, &e); if (e) orl_refuse(e, c); return r;
}
static inline double orl_f_from_i(int64_t n, int rounded, uint32_t c) {
    const char *e; double r = orl__f_from_i(n, rounded, &e); if (e) orl_refuse(e, c); return r;
}
static inline int64_t orl_f_trunc(double x, uint32_t c) {
    const char *e; int64_t r = orl__f_trunc(x, &e); if (e) orl_refuse(e, c); return r;
}
static inline int64_t orl_f_round(double x, uint32_t c) {
    const char *e; int64_t r = orl__f_round(x, &e); if (e) orl_refuse(e, c); return r;
}

/* ================================================================ printing (exact decimals) */

/* Int: decimal, '-' for negatives. Returns the length; no terminator. */
static inline size_t orl__fmt_i(char *buf, int64_t v) {
    if (v < 0) {
        buf[0] = '-';
        return 1 + orl__fmt_u64(buf + 1, orl__mag(v));
    }
    return orl__fmt_u64(buf, (uint64_t)v);
}

/* Fix: sign, integer part, '.', every fraction digit (or "0"). frac*10 < 10*2^32. */
static inline size_t orl__fmt_x(char *buf, int64_t a) {
    uint64_t u = orl__mag(a), frac = u & ORL__LOW32;
    size_t n = 0;
    if (a < 0) buf[n++] = '-';
    n += orl__fmt_u64(buf + n, u >> 32);
    buf[n++] = '.';
    if (frac == 0) buf[n++] = '0';
    while (frac != 0) {
        frac *= 10u;
        buf[n++] = (char)('0' + (int)(frac >> 32));
        frac &= ORL__LOW32;
    }
    return n;
}

/* A non-negative integer in base 10^9, little-endian limbs. 128 limbs hold
   1152 digits; the largest number printed has 767 (an odd 53-bit m times 5^1074). */
#define ORL__BN_LIMBS 128
typedef struct { uint32_t d[ORL__BN_LIMBS]; int n; } orl__bn;

static inline void orl__bn_set(orl__bn *b, uint64_t v) {
    b->n = 0;
    do {
        b->d[b->n++] = (uint32_t)(v % 1000000000u);
        v /= 1000000000u;
    } while (v != 0);
}

static inline void orl__bn_mul(orl__bn *b, uint32_t m) {
    uint64_t carry = 0;
    int i;
    for (i = 0; i < b->n; ++i) {
        uint64_t t = (uint64_t)b->d[i] * m + carry;   /* < 10^9 * 2^32 + 2^33 */
        b->d[i] = (uint32_t)(t % 1000000000u);
        carry = t / 1000000000u;
    }
    while (carry != 0) {
        if (b->n >= ORL__BN_LIMBS) orl__fatal("bignum overflow");
        b->d[b->n++] = (uint32_t)(carry % 1000000000u);
        carry /= 1000000000u;
    }
}

/* The decimal digits (no leading zeros; "0" for zero); returns the count. */
static inline size_t orl__bn_dec(const orl__bn *b, char *out) {
    size_t n = orl__fmt_u64(out, b->d[b->n - 1]);
    int i, k;
    for (i = b->n - 2; i >= 0; --i) {
        uint32_t v = b->d[i];
        for (k = 8; k >= 0; --k) {
            out[n + (size_t)k] = (char)('0' + (int)(v % 10u));
            v /= 10u;
        }
        n += 9;
    }
    return n;
}

/* Float: NaN, Infinity, -Infinity; otherwise the sign bit's '-', then the exact
   decimal of the binary64 (".0" when integral; every digit, no trailing zero).
   buf must hold ORL_FMT_F_MAX bytes. */
static inline size_t orl__fmt_f(char *buf, double x) {
    static const uint32_t pow5[13] = {
        1u, 5u, 25u, 125u, 625u, 3125u, 15625u, 78125u, 390625u, 1953125u,
        9765625u, 48828125u, 244140625u
    };
    uint64_t u = orl__fb(x), m = u & ORL__FRAC_MASK;
    int ex = (int)((u >> 52) & 0x7FFu), e;
    size_t n = 0;
    orl__bn b;
    char dig[ORL__BN_LIMBS * 9 + 9];
    size_t L;
    if (ex == 0x7FF) {
        if (m != 0) { memcpy(buf, "NaN", 3); return 3; }
        if (u >> 63) { memcpy(buf, "-Infinity", 9); return 9; }
        memcpy(buf, "Infinity", 8);
        return 8;
    }
    if (u >> 63) buf[n++] = '-';
    if (ex == 0) e = -1074;
    else { m |= (uint64_t)1 << 52; e = ex - 1075; }
    if (m == 0) { memcpy(buf + n, "0.0", 3); return n + 3; }
    while ((m & 1u) == 0) { m >>= 1; e += 1; }     /* m odd: |x| = m * 2^e */
    orl__bn_set(&b, m);
    if (e >= 0) {                                  /* an integer: m * 2^e, then ".0" */
        while (e >= 29) { orl__bn_mul(&b, (uint32_t)1 << 29); e -= 29; }
        if (e > 0) orl__bn_mul(&b, (uint32_t)1 << e);
        n += orl__bn_dec(&b, buf + n);
        buf[n++] = '.';
        buf[n++] = '0';
        return n;
    } else {                                       /* m * 5^s / 10^s: exactly s fraction digits */
        size_t s = (size_t)(-e), t = s, i;
        while (t >= 13) { orl__bn_mul(&b, 1220703125u); t -= 13; }
        if (t > 0) orl__bn_mul(&b, pow5[t]);
        L = orl__bn_dec(&b, dig);
        if (L <= s) {
            buf[n++] = '0';
            buf[n++] = '.';
            for (i = L; i < s; ++i) buf[n++] = '0';
            memcpy(buf + n, dig, L);
            n += L;
        } else {
            memcpy(buf + n, dig, L - s);
            n += L - s;
            buf[n++] = '.';
            memcpy(buf + n, dig + (L - s), s);
            n += s;
        }
        return n;
    }
}

/* ================================================================ text and the builder */

static inline orl_text orl_t_lit(const char *p, uint32_t n) {
    orl_text t;
    t.p = (const uint8_t *)p;
    t.n = n;
    return t;
}

static inline int orl_t_eq(orl_text a, orl_text b) {
    return a.n == b.n && (a.n == 0 || memcmp(a.p, b.p, a.n) == 0);
}

static inline void orl_s_reset(uint32_t c) {
    orl__sb_len = 0;
    orl__sb_clause = c;
}

/* Every append: TEXT-TOO-LONG (clause of the last orl_s_reset) when the builder
   would exceed 2^24 bytes; exactly 2^24 is allowed. */
static inline void orl__s_put(const void *p, size_t n) {
    if (n > (size_t)(ORL_TEXT_MAX - orl__sb_len)) {
        orl_refuse(ORL_TEXT_TOO_LONG, orl__sb_clause);
        return;
    }
    if (orl__sb_len + n > orl__sb_cap) {
        size_t cap = orl__sb_cap != 0 ? orl__sb_cap : 256;
        while (cap < orl__sb_len + n) cap *= 2;
        if (cap > ORL_TEXT_MAX) cap = ORL_TEXT_MAX;
        orl__sb = (uint8_t *)orl__regrow(orl__sb, cap);
        orl__sb_cap = (uint32_t)cap;
    }
    if (n != 0) memcpy(orl__sb + orl__sb_len, p, n);
    orl__sb_len += (uint32_t)n;
}

static inline void orl_s_lit(const char *p, uint32_t n) { orl__s_put(p, n); }
static inline void orl_s_t(orl_text t) { orl__s_put(t.p, t.n); }

static inline void orl_s_i(int64_t v) {
    char buf[ORL_FMT_I_MAX];
    orl__s_put(buf, orl__fmt_i(buf, v));
}

static inline void orl_s_x(int64_t raw) {
    char buf[ORL_FMT_X_MAX];
    orl__s_put(buf, orl__fmt_x(buf, raw));
}

static inline void orl_s_f(double x) {
    char buf[ORL_FMT_F_MAX];
    orl__s_put(buf, orl__fmt_f(buf, x));
}

static inline void orl_s_b(int v) {
    if (v) orl__s_put("true", 4);
    else orl__s_put("false", 5);
}

static inline void orl__s_elem(int tag, int64_t slot) {
    switch (tag) {
    case 'I': orl_s_i(slot); break;
    case 'X': orl_s_x(slot); break;
    case 'F': orl_s_f(orl__bf((uint64_t)slot)); break;
    case 'B': orl_s_b(slot != 0); break;
    default: orl__fatal("unknown list tag"); break;
    }
}

/* '[' elements printed by their type, separated by ", ", ']' (tag I X F B). */
static inline void orl_s_list(int tag, const int64_t *slots, uint64_t n) {
    uint64_t i;
    orl__s_put("[", 1);
    for (i = 0; i < n; ++i) {
        if (i != 0) orl__s_put(", ", 2);
        orl__s_elem(tag, slots[i]);
    }
    orl__s_put("]", 1);
}

/* A heap copy of the builder's bytes (never freed by the runtime). */
static inline orl_text orl_s_take(void) {
    orl_text t;
    uint8_t *p = (uint8_t *)orl__alloc(orl__sb_len);
    if (orl__sb_len != 0) memcpy(p, orl__sb, orl__sb_len);
    t.p = p;
    t.n = orl__sb_len;
    return t;
}

/* ================================================================ Say */

/* The line is the builder's bytes and one LF: OUTPUT-TOO-LONG when the output
   would exceed 2^30 bytes; else written, hashed, and event 'S'. The builder is
   left as it is (the generated code resets it). */
static inline void orl_say(uint32_t c) {
    uint64_t line = (uint64_t)orl__sb_len + 1;
    orl__ev x;
    if (line > ORL_OUTPUT_MAX - orl__out_bytes) {
        orl_refuse(ORL_OUTPUT_TOO_LONG, c);
        return;
    }
    if (orl__out != NULL) {
        if (orl__sb_len != 0) fwrite(orl__sb, 1, orl__sb_len, orl__out);
        fputc('\n', orl__out);
    }
    orl__sha_update(&orl__out_hash, orl__sb, orl__sb_len);
    orl__sha_update(&orl__out_hash, "\n", 1);
    orl__out_bytes += line;
    orl__ev_begin(&x, 'S', c, (uint32_t)line);
    orl__ev_put(&x, orl__sb, orl__sb_len);
    orl__ev_put(&x, "\n", 1);
    orl__ev_end(&x);
}

/* ================================================================ value encodings and events */

/* An element without its tag: 8 bytes big-endian for I X F (F: the canonical
   bits), 1 byte (0/1) for B. Returns the length. */
static inline size_t orl__enc_elem(uint8_t *p, int tag, int64_t slot) {
    switch (tag) {
    case 'I':
    case 'X':
        orl__be64(p, (uint64_t)slot);
        return 8;
    case 'F': {
        uint64_t u = (uint64_t)slot;
        orl__be64(p, orl__isnan_bits(u) ? ORL__CANON_NAN : u);
        return 8;
    }
    case 'B':
        p[0] = (uint8_t)(slot != 0);
        return 1;
    default:
        orl__fatal("unknown value tag");
        return 0;
    }
}

/* A scalar value encoding: the tag, then the element. */
static inline size_t orl__enc_slot(uint8_t *p, int tag, int64_t slot) {
    p[0] = (uint8_t)tag;
    return 1 + orl__enc_elem(p + 1, tag, slot);
}

static inline void orl__ev_scalar(int kind, uint32_t c, uint32_t var, int tag, int64_t slot) {
    uint8_t p[13];
    orl__be32(p, var);
    orl__event(kind, c, p, 4 + orl__enc_slot(p + 4, tag, slot));
}

static inline void orl_ev_assign_i(uint32_t c, uint32_t var, int64_t v) { orl__ev_scalar('A', c, var, 'I', v); }
static inline void orl_ev_assign_x(uint32_t c, uint32_t var, int64_t v) { orl__ev_scalar('A', c, var, 'X', v); }
static inline void orl_ev_assign_f(uint32_t c, uint32_t var, double v) { orl__ev_scalar('A', c, var, 'F', orl_f_bits(v)); }
/* Any nonzero v is true: orl__enc_elem writes the byte 1 (its one normalisation point). */
static inline void orl_ev_assign_b(uint32_t c, uint32_t var, int v) { orl__ev_scalar('A', c, var, 'B', v); }

static inline void orl_ev_assign_t(uint32_t c, uint32_t var, orl_text t) {
    uint8_t p[9];
    orl__ev x;
    if (t.n > UINT32_MAX - 9) orl__fatal("text too long for an event");
    orl__be32(p, var);
    p[4] = 'T';
    orl__be32(p + 5, t.n);
    orl__ev_begin(&x, 'A', c, 9 + t.n);
    orl__ev_put(&x, p, 9);
    orl__ev_put(&x, t.p, t.n);
    orl__ev_end(&x);
}

static inline void orl_ev_assign_l(uint32_t c, uint32_t var, int tag, const int64_t *slots, uint64_t n) {
    uint8_t hd[10], buf[1024];
    size_t k = 0;
    uint64_t i, w;
    orl__ev x;
    if (tag != 'I' && tag != 'X' && tag != 'F' && tag != 'B') orl__fatal("unknown list tag");
    if (n > ORL_LIST_MAX) orl__fatal("list too long for an event");
    w = tag == 'B' ? 1 : 8;
    orl__be32(hd, var);
    hd[4] = 'L';
    hd[5] = (uint8_t)tag;
    orl__be32(hd + 6, (uint32_t)n);
    orl__ev_begin(&x, 'A', c, (uint32_t)(10 + n * w));
    orl__ev_put(&x, hd, 10);
    for (i = 0; i < n; ++i) {
        k += orl__enc_elem(buf + k, tag, slots[i]);
        if (k > sizeof buf - 8) {
            orl__ev_put(&x, buf, k);
            k = 0;
        }
    }
    if (k != 0) orl__ev_put(&x, buf, k);
    orl__ev_end(&x);
}

static inline void orl_ev_item(uint32_t c, uint32_t var, uint64_t index, int tag, int64_t slot) {
    uint8_t p[21];
    orl__be32(p, var);
    orl__be64(p + 4, index);
    orl__event('E', c, p, 12 + orl__enc_slot(p + 12, tag, slot));
}

static inline void orl_ev_push(uint32_t c, uint32_t var, int tag, int64_t slot) {
    orl__ev_scalar('P', c, var, tag, slot);
}

static inline void orl_ev_pop(uint32_t c, uint32_t var, uint64_t newlen) {
    uint8_t p[12];
    orl__be32(p, var);
    orl__be64(p + 4, newlen);
    orl__event('Q', c, p, 12);
}

/* ================================================================ lists (1-based; slots int64_t) */

static inline orl_list orl_l_new(int64_t n, int64_t fill, uint32_t c) {
    orl_list l;
    uint64_t i;
    l.v = NULL;
    l.len = 0;
    l.cap = 0;
    if (n < 0) { orl_refuse(ORL_NEGATIVE_LENGTH, c); return l; }
    if ((uint64_t)n > ORL_LIST_MAX) { orl_refuse(ORL_LIST_TOO_LONG, c); return l; }
    l.cap = n != 0 ? (uint64_t)n : 4;
    l.v = (int64_t *)orl__alloc((size_t)l.cap * sizeof(int64_t));
    for (i = 0; i < (uint64_t)n; ++i) l.v[i] = fill;
    l.len = (uint64_t)n;
    return l;
}

static inline orl_list orl_l_from(uint64_t n, const int64_t *slots) {
    orl_list l;
    if (n > ORL_LIST_MAX) orl__fatal("list literal longer than 2^24");
    l.cap = n != 0 ? n : 4;
    l.v = (int64_t *)orl__alloc((size_t)l.cap * sizeof(int64_t));
    if (n != 0) memcpy(l.v, slots, (size_t)n * sizeof(int64_t));
    l.len = n;
    return l;
}

static inline orl_list orl_l_copy(const orl_list *s) {
    return orl_l_from(s->len, s->v);
}

static inline int64_t orl_l_get(const orl_list *l, int64_t k, uint32_t c) {
    if (k < 1 || (uint64_t)k > l->len) { orl_refuse(ORL_INDEX_OUT_OF_RANGE, c); return 0; }
    return l->v[k - 1];
}

static inline void orl_l_set(orl_list *l, int64_t k, int64_t v, uint32_t c) {
    if (k < 1 || (uint64_t)k > l->len) { orl_refuse(ORL_INDEX_OUT_OF_RANGE, c); return; }
    l->v[k - 1] = v;
}

static inline void orl_l_push(orl_list *l, int64_t v, uint32_t c) {
    if (l->len >= ORL_LIST_MAX) { orl_refuse(ORL_LIST_TOO_LONG, c); return; }
    if (l->len == l->cap) {
        uint64_t cap = l->cap != 0 ? l->cap * 2 : 4;
        if (cap > ORL_LIST_MAX) cap = ORL_LIST_MAX;
        l->v = (int64_t *)orl__regrow(l->v, (size_t)cap * sizeof(int64_t));
        l->cap = cap;
    }
    l->v[l->len++] = v;
}

static inline void orl_l_pop(orl_list *l, uint32_t c) {
    if (l->len == 0) { orl_refuse(ORL_EMPTY_LIST, c); return; }
    l->len -= 1;
}

static inline int64_t orl_l_len(const orl_list *l) { return (int64_t)l->len; }

/* Not in the contract: releases a list's slots (the runtime never frees one). */
static inline void orl_l_free(orl_list *l) {
    free(l->v);
    l->v = NULL;
    l->len = 0;
    l->cap = 0;
}

/* ================================================================ claims and musts */

static inline void orl_claim(uint32_t id, uint32_t c, int result, uint64_t cost,
                             uint32_t ref_clause, uint64_t ref_cost) {
    uint8_t p[5];
    int r = result != 0;
    orl__claim_rec *rec;
    if (id >= orl__n_claims) orl__fatal("claim id out of range");
    orl__be32(p, id);
    p[4] = (uint8_t)r;
    orl__event('C', c, p, 5);
    rec = &orl__claims[id];
    rec->evals += 1;
    rec->trues += (uint64_t)r;
    rec->cost += cost;
    rec->ref_clause = ref_clause;
    rec->ref_cost = ref_cost;
    if (!r) orl_refuse(ORL_CLAIM_REFUTED, c);
}

static inline void orl_must(uint32_t id, uint32_t c, int result) {
    uint8_t p[5];
    int r = result != 0;
    orl__be32(p, id);
    p[4] = (uint8_t)r;
    orl__event('M', c, p, 5);
    if (!r) orl_refuse(ORL_MUST_FAILED, c);
}

/* ================================================================ init */

static inline int orl__hexval(int ch) {
    if (ch >= '0' && ch <= '9') return ch - '0';
    if (ch >= 'a' && ch <= 'f') return ch - 'a' + 10;
    if (ch >= 'A' && ch <= 'F') return ch - 'A' + 10;
    return -1;
}

/* 64 hex digits (either case) to 32 bytes and their lowercase spelling. */
static inline void orl__seal(const char *hex, uint8_t out[32], char norm[65], const char *what) {
    int i;
    if (hex == NULL) orl__fatal(what);
    for (i = 0; i < 64; ++i) {
        int v = orl__hexval((unsigned char)hex[i]);
        if (v < 0) orl__fatal(what);
        norm[i] = orl__hexd[v];
        if ((i & 1) == 0) out[i / 2] = (uint8_t)(v << 4);
        else out[i / 2] = (uint8_t)(out[i / 2] | v);
    }
    if (hex[64] != '\0') orl__fatal(what);
    norm[64] = '\0';
}

static inline FILE *orl__open(const char *path) {
    FILE *f = fopen(path, "wb");
    if (f == NULL) {
        fputs("orlog: cannot open file: ", stderr);
        fputs(path, stderr);
        fputc('\n', stderr);
        exit(2);
    }
    return f;
}

/* argv[1] output path, argv[2] receipt path, optional argv[3] trace path.
   A missing path, or a file that cannot be opened: message on stderr, exit 2. */
static inline void orl_init(int argc, char **argv, const char *backend, const char *law_hex,
                            const char *text_hex, uint32_t n_claims, const uint32_t *claim_clause) {
    uint8_t text_bytes[32];
    orl__sha256 h;
    uint32_t i;
    if (argc < 3 || argv == NULL || argv[1] == NULL || argv[2] == NULL) {
        fputs("orlog: usage: PROGRAM OUTPUT RECEIPT [TRACE]\n", stderr);
        exit(2);
    }
    orl__seal(law_hex, orl__law, orl__law_hex, "law seal is not 64 hex digits");
    orl__seal(text_hex, text_bytes, orl__text_hex, "text seal is not 64 hex digits");
    orl__backend = backend != NULL ? backend : "";
    orl__out = orl__open(argv[1]);
    orl__rcpt = orl__open(argv[2]);
    orl__trc = (argc > 3 && argv[3] != NULL) ? orl__open(argv[3]) : NULL;
    orl__sha_init(&h);
    orl__sha_update(&h, "orlog-trace-0", 13);
    orl__sha_update(&h, orl__law, 32);
    orl__sha_final(&h, orl__head);
    orl__events = 0;
    orl__sha_init(&orl__out_hash);
    orl__out_bytes = 0;
    free(orl__claims);
    orl__claims = NULL;
    orl__n_claims = n_claims;
    if (n_claims != 0) {
        orl__claims = (orl__claim_rec *)orl__alloc((size_t)n_claims * sizeof(orl__claim_rec));
        for (i = 0; i < n_claims; ++i) {
            orl__claims[i].clause = claim_clause != NULL ? claim_clause[i] : 0;
            orl__claims[i].ref_clause = 0;
            orl__claims[i].evals = 0;
            orl__claims[i].trues = 0;
            orl__claims[i].cost = 0;
            orl__claims[i].ref_cost = 0;
        }
    }
    orl__sb_len = 0;
    orl__sb_clause = 0;
}

#endif /* ORLOG_RT_H */
