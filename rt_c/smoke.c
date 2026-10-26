/*
 * smoke.c -- a hand-written stand-in for a generated program: it drives
 * orl_init, the builder, orl_say, every kind of event, orl_must, orl_claim and
 * orl_finish, so that the output, the trace and the receipt are exercised.
 *
 *   smoke OUTPUT RECEIPT [TRACE]
 *
 * Built with -DSMOKE_REFUSE it ends by refusing OVERFLOW at clause 14 instead
 * of completing. check_smoke.py rebuilds the expected output, events and
 * receipt independently (Python, from the spec's encodings and numeric_ref's
 * formatters) and compares them byte for byte.
 */
#include "orlog_rt.h"

static const char LAW_HEX[] = "8f6d5d392f1078b3fbc32cd7fce8a781b39a873e5bb4741a5918a88bca9dc6fe";  /* SHA-256("smoke law") */
static const char TEXT_HEX[] = "92c787c163c8a498e6710e71a99c268c9a7430202ca8ddca2ddb9d25c9957a5d"; /* SHA-256("smoke text") */

#define ORLOG_WORD "\xC3\x98" "rl" "\xC7\xAB" "g"   /* 7 bytes of UTF-8 */

int main(int argc, char **argv) {
    static const uint32_t claim_clause[2] = {11u, 12u};
    int64_t total = 0, i, third_x;
    int64_t fl[3], bl[3] = {1, 0, 1};
    double third_f, nan_f, inf_f;
    orl_list l;
    orl_text t;

    orl_init(argc, argv, "c99", LAW_HEX, TEXT_HEX, 2, claim_clause);

    /* Int: a loop with checked arithmetic, one assignment event per step */
    for (i = 1; i <= 10; ++i) {
        int64_t sq = orl_i_mul(i, i, 3);
        total = orl_i_add(total, sq, 3);
        orl_ops += 2;
        orl_ev_assign_i(3, 0, total);
    }
    orl_s_reset(4);
    orl_s_lit("sum of squares 1..10 = ", 23);
    orl_s_i(total);
    orl_say(4);

    /* Fix */
    third_x = orl_x_div(orl_x_from_i(1, 5), orl_x_from_i(3, 5), 5);
    orl_ops += 1;
    orl_ev_assign_x(5, 1, third_x);
    orl_s_reset(5);
    orl_s_lit("one third as Fix = ", 19);
    orl_s_x(third_x);
    orl_say(5);

    /* Float, NaNs (the event carries the canonical bits), -0.0, the smallest subnormal */
    third_f = orl_f_div(1.0, 3.0);
    orl_ops += 1;
    orl_ev_assign_f(6, 2, third_f);
    orl_s_reset(6);
    orl_s_lit("one third as Float = ", 21);
    orl_s_f(third_f);
    orl_say(6);
    inf_f = orl_f_div(1.0, 0.0);
    nan_f = orl_f_sub(inf_f, inf_f);
    orl_ev_assign_f(6, 3, nan_f);
    orl_ev_assign_f(6, 4, orl_bits_f((int64_t)UINT64_C(0xFFF8000000000001)));
    orl_s_reset(6);
    orl_s_f(nan_f);
    orl_s_lit(" ", 1);
    orl_s_f(inf_f);
    orl_s_lit(" ", 1);
    orl_s_f(orl_f_neg(0.0));
    orl_s_lit(" ", 1);
    orl_s_f(orl_bits_f(1));
    orl_say(6);

    /* Bool */
    orl_ev_assign_b(7, 5, 1);
    orl_s_reset(7);
    orl_s_lit("flag = ", 7);
    orl_s_b(1);
    orl_say(7);

    /* Text */
    orl_s_reset(8);
    orl_s_lit(ORLOG_WORD, 7);
    t = orl_s_take();
    orl_ev_assign_t(8, 6, t);
    orl_s_reset(8);
    orl_s_lit("text = ", 7);
    orl_s_t(t);
    orl_say(8);

    /* Lists: item, push, pop, whole assignments of I, F and B lists */
    l = orl_l_new(3, 0, 9);
    orl_l_set(&l, 2, 7, 9);
    orl_ev_item(9, 7, 2, 'I', 7);
    orl_l_push(&l, -5, 9);
    orl_ev_push(9, 7, 'I', -5);
    orl_l_pop(&l, 9);
    orl_ev_pop(9, 7, (uint64_t)orl_l_len(&l));
    orl_ev_assign_l(9, 7, 'I', l.v, l.len);
    orl_s_reset(9);
    orl_s_lit("list = ", 7);
    orl_s_list('I', l.v, l.len);
    orl_say(9);
    fl[0] = orl_f_bits(0.5);
    fl[1] = orl_f_bits(-0.0);
    fl[2] = (int64_t)UINT64_C(0x7FF4000000000000);   /* a signalling NaN: canonical in every event */
    orl_ev_assign_l(10, 8, 'F', fl, 3);
    orl_ev_item(10, 8, 3, 'F', fl[2]);
    orl_ev_push(10, 8, 'F', fl[2]);
    orl_ev_assign_l(10, 9, 'B', bl, 3);
    orl_s_reset(10);
    orl_s_list('F', fl, 3);
    orl_s_lit(" ", 1);
    orl_s_list('B', bl, 3);
    orl_say(10);

    /* a must, and claims (the second evaluated twice) */
    orl_must(0, 13, orl_l_len(&l) == 3);
    orl_claim(0, 11, total == 385, 20, 3, 20);
    orl_claim(1, 12, third_x == 1431655765, 7, 5, 7);
    orl_claim(1, 12, orl_t_eq(t, orl_t_lit(ORLOG_WORD, 7)), 8, 8, 9);

#ifdef SMOKE_REFUSE
    orl_s_reset(14);
    orl_s_lit("about to overflow", 17);
    orl_say(14);
    total = orl_i_mul(INT64_MAX, 2, 14);          /* refuses OVERFLOW at clause 14 */
    orl_s_reset(15);
    orl_s_lit("not reached", 11);
    orl_say(15);
#endif

    orl_l_free(&l);
    orl_finish();
    return 0;
}
