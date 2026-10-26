// smoke.rs: a small program over orlog_rt.rs, shaped like a generated one. It writes an output
// file, a receipt and a trace through Rt::init, s_*, say, ev_*, claim, must, refuse and finish.
//
// usage: smoke OUTPUT RECEIPT TRACE [complete|chain|refute]
//   complete  (the default) every builder append, every event kind, two claims and a must;
//             status COMPLETED
//   chain     the event-chain check of RUNTIME-SPEC.md section 9 through real files: 'S' "hello",
//             'A' var 0 Int 42, then i_add(MAX, 1) at clause 3 refuses OVERFLOW, so the receipt's
//             trace-head is src/check_chain.py's head3
//   refute    a claim that fails: status REFUSED CLAIM-REFUTED 21
// Rt::init reads arguments 1 to 3; the mode (argument 4) is this program's own.
// check_smoke.py checks the three runs' files against values it builds itself.

include!("orlog_rt.rs");

const SMOKE_LAW: &str = "8f1f74adf65864c86d3d471ea8ca9e329d4282489edc156c99604264090774bf"; // SHA-256("law")
const SMOKE_TEXT: &str = "982d9e3eb996f559e633f4d194def3761d909f5a3b647d1a851fead67c32c9d1"; // SHA-256("text")

fn main() {
    let mode = std::env::args_os().nth(4).map(|s| s.to_string_lossy().into_owned()).unwrap_or_default();
    let mut rt = Rt::init("rust", SMOKE_LAW, SMOKE_TEXT, &[20, 21]);
    match mode.as_str() {
        "chain" => smoke_chain(&mut rt),
        "refute" => smoke_refute(&mut rt),
        _ => smoke_complete(&mut rt),
    }
}

fn smoke_complete(rt: &mut Rt) -> ! {
    // Int: 6 * 7 at clause 1, assigned to var 0
    let a = rt.i_mul(6, 7, 1);
    rt.ops += 1;
    rt.ev_assign_i(1, 0, a);
    // Fix: 1 / 3 at clause 2, var 1 (nested calls go through temporaries)
    let one = rt.x_from_i(1, 2);
    let three = rt.x_from_i(3, 2);
    let third = rt.x_div(one, three, 2);
    rt.ops += 1;
    rt.ev_assign_x(2, 1, third);
    // Float at clause 3: 1/3, sqrt(-1), and a NaN with a payload that f_max passes through
    let f = Rt::f_div(1.0, 3.0);
    let nan = Rt::f_sqrt(-1.0);
    let odd = Rt::f_max(1.0, Rt::bits_f(0x7FF0_0000_0000_0001u64 as i64));
    rt.ops += 3;
    rt.ev_assign_f(3, 2, f);
    rt.ev_assign_f(3, 3, nan);
    rt.ev_assign_f(3, 4, odd);
    // Bool and Text at clause 4
    rt.ev_assign_b(4, 5, a == 42);
    rt.ev_assign_t(4, 6, "Ørlǫg".as_bytes());
    // a list of Int: new, set, assign, push, item, pop
    let mut l = rt.l_new(3, 7, 5);
    rt.l_set(&mut l, 2, -5, 5);
    rt.ev_assign_l(5, 7, b'I', &l);
    rt.l_push(&mut l, 9, 6);
    rt.ev_push(6, 7, b'I', 9);
    let e2 = rt.l_get(&l, 2, 7);
    rt.ev_item(7, 7, 2, b'I', e2);
    rt.l_pop(&mut l, 8);
    rt.ev_pop(8, 7, l.len() as u64);
    // lists of the other tags (floats as their bits)
    let xs = vec![one, third, -(ORL_ONE / 2)];
    let fs = vec![Rt::f_bits(0.5), Rt::f_bits(-0.0), Rt::f_bits(odd)];
    let bs = vec![1, 0, 1];
    rt.ev_assign_l(9, 8, b'X', &xs);
    rt.ev_assign_l(9, 9, b'F', &fs);
    rt.ev_assign_l(9, 10, b'B', &bs);
    rt.ev_item(9, 9, 3, b'F', fs[2]);
    rt.ev_push(9, 10, b'B', 0);
    // the output, one Say per clause 10 to 15
    rt.s_reset(10);
    rt.s_lit(b"a = ");
    rt.s_i(a);
    rt.say(10);
    rt.s_reset(11);
    rt.s_lit(b"third = ");
    rt.s_x(third);
    rt.s_lit(b", min = ");
    rt.s_x(i64::MIN);
    rt.say(11);
    rt.s_reset(12);
    rt.s_lit(b"f = ");
    rt.s_f(f);
    rt.s_lit(b", nan = ");
    rt.s_f(nan);
    rt.s_lit(b", -0 = ");
    rt.s_f(-0.0);
    rt.s_lit(b", tiny = ");
    rt.s_f(Rt::bits_f(1));
    rt.say(12);
    rt.s_reset(13);
    rt.s_b(a == 42);
    rt.s_lit(b" ");
    rt.s_b(false);
    rt.s_lit(b" ");
    rt.s_t("Ørlǫg".as_bytes());
    rt.say(13);
    rt.s_reset(14);
    rt.s_list(b'I', &l);
    rt.s_lit(b" ");
    rt.s_list(b'X', &xs);
    rt.s_lit(b" ");
    rt.s_list(b'F', &fs);
    rt.s_lit(b" ");
    rt.s_list(b'B', &bs);
    rt.s_lit(b" ");
    rt.s_list(b'I', &[]);
    rt.say(14);
    rt.s_reset(15);
    rt.say(15);
    // claims and a must
    rt.claim(0, 20, a == 42, 5, 30, 4);
    rt.claim(0, 20, third < one, 2, 31, 6);
    rt.must(0, 16, true);
    rt.ops += 10;
    rt.finish()
}

fn smoke_chain(rt: &mut Rt) -> ! {
    rt.s_reset(1);
    rt.s_lit(b"hello");
    rt.say(1);
    rt.ev_assign_i(2, 0, 42);
    let _ = rt.i_add(i64::MAX, 1, 3); // refuses OVERFLOW at clause 3
    rt.finish()
}

fn smoke_refute(rt: &mut Rt) -> ! {
    rt.s_reset(1);
    rt.s_lit(b"before");
    rt.say(1);
    rt.ops += 3;
    rt.claim(0, 20, true, 1, 2, 3);
    rt.claim(1, 21, false, 9, 30, 2); // refuses CLAIM-REFUTED at clause 21
    rt.finish()
}
