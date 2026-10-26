// test_rt.rs: the conformance harness of orlog_rt.rs (RUNTIME-SPEC.md section 9).
//
// usage: test_rt VECTORS        (vectors/runtime-vectors.txt)
//
// 1. Every vector line runs through the runtime twice: through the pure function (`orl_*`, whose
//    `Err` is the refusal code) and through the `Rt` method a generated program calls, on a test
//    run whose `refuse` panics with the receipt's status line instead of exiting (the hook
//    `test_unwind`). A line passes only when both give the vector's result. Printing runs through
//    the `orl_fmt_*` function and through the text builder; SHA-256 one shot and byte by byte.
//    `f_lt` and `f_eq` are the native comparisons a generated program writes (`<`, `==`).
//    Prints every failing line, then `RUNTIME VECTORS <passed> / <total>`.
// 2. The event-chain check: law seal = SHA-256("law"); 'S' clause 1 "hello\n" (through s_lit and
//    say), 'A' clause 2 var 0 Int 42 (ev_assign_i), 'R' clause 3 "OVERFLOW" (refuse). Prints the
//    heads in the format of src/check_chain.py.
// 3. Checks of what no vector covers (lists, limits, claims, the builder's printing of lists),
//    each against a value written here by hand: `RUNTIME EXTRA <passed> / <total>`.
// Exit status 1 when anything failed.

include!("orlog_rt.rs");

const TR_C: u32 = 9;
const TR_ZERO_SEAL: &str = "0000000000000000000000000000000000000000000000000000000000000000";

/// Runs f; a refusal (or finish) of a test run comes back as Err(its status line).
fn tr_catch<T>(f: impl FnOnce() -> T) -> Result<T, String> {
    match std::panic::catch_unwind(std::panic::AssertUnwindSafe(f)) {
        Ok(v) => Ok(v),
        Err(p) => match p.downcast::<OrlEnded>() {
            Ok(e) => {
                let e = *e;
                Err(e.status)
            }
            Err(_) => Err("PANIC".to_string()),
        },
    }
}

fn tr_rt(law_hex: &str, claim_clause: &[u32]) -> Rt {
    Rt::with_sinks("rust", law_hex, TR_ZERO_SEAL, claim_clause, None, None, None, true)
}

// ---------------------------------------------------------------- the vectors' notation

fn vi(v: i64) -> String {
    format!("i:{}", v)
}
fn vx(v: i64) -> String {
    format!("x:{}", v)
}
fn vf(v: f64) -> String {
    format!("f:{:016X}", v.to_bits())
}
fn vb(v: bool) -> String {
    (if v { "b:1" } else { "b:0" }).to_string()
}
fn vs(bytes: &[u8]) -> String {
    format!("s:{}", String::from_utf8_lossy(bytes))
}

/// A pure function's result in the vectors' notation.
fn pure<T>(r: OrlR<T>, f: fn(T) -> String) -> String {
    match r {
        Ok(v) => f(v),
        Err(code) => format!("!{}", code),
    }
}

/// A method's result in the vectors' notation (a refusal must name the clause TR_C).
fn meth<T>(r: Result<T, String>, f: fn(T) -> String) -> String {
    match r {
        Ok(v) => f(v),
        Err(s) => {
            let tail = format!(" {}", TR_C);
            match s.strip_prefix("status REFUSED ").and_then(|t| t.strip_suffix(tail.as_str())) {
                Some(code) => format!("!{}", code),
                None => format!("?{}", s),
            }
        }
    }
}

/// The two paths must agree; their common answer is compared with the vector.
fn both(p: String, m: String) -> String {
    if p == m {
        p
    } else {
        format!("pure {} but method {}", p, m)
    }
}

fn pi(s: &str) -> Result<i64, String> {
    s.strip_prefix("i:").and_then(|t| t.parse::<i64>().ok()).ok_or_else(|| format!("bad argument {}", s))
}
fn px(s: &str) -> Result<i64, String> {
    s.strip_prefix("x:").and_then(|t| t.parse::<i64>().ok()).ok_or_else(|| format!("bad argument {}", s))
}
fn pf(s: &str) -> Result<f64, String> {
    s.strip_prefix("f:")
        .filter(|t| t.len() == 16)
        .and_then(|t| u64::from_str_radix(t, 16).ok())
        .map(f64::from_bits)
        .ok_or_else(|| format!("bad argument {}", s))
}
fn pb(s: &str) -> Result<bool, String> {
    match s {
        "b:0" => Ok(false),
        "b:1" => Ok(true),
        _ => Err(format!("bad argument {}", s)),
    }
}
fn phex(s: &str) -> Result<Vec<u8>, String> {
    let t = s.strip_prefix("hex:").ok_or_else(|| format!("bad argument {}", s))?;
    let b = t.as_bytes();
    if b.len() % 2 != 0 {
        return Err(format!("bad argument {}", s));
    }
    let mut out = Vec::with_capacity(b.len() / 2);
    for i in 0..b.len() / 2 {
        match (orl_hexval(b[2 * i]), orl_hexval(b[2 * i + 1])) {
            (Some(hi), Some(lo)) => out.push((hi << 4) | lo),
            _ => return Err(format!("bad argument {}", s)),
        }
    }
    Ok(out)
}

/// Runs one vector line; Err carries what the runtime gave.
fn tr_line(rt: &mut Rt, line: &str) -> Result<(), String> {
    let pos = line.find(" => ").ok_or_else(|| "no ' => ' in the line".to_string())?;
    let (lhs, want) = (&line[..pos], &line[pos + 4..]);
    let mut parts = lhs.split(' ');
    let op = parts.next().unwrap_or("");
    let a: Vec<&str> = parts.collect();
    let arg = |k: usize| -> Result<&str, String> { a.get(k).copied().ok_or_else(|| format!("argument {} missing", k + 1)) };
    let got: String = match op {
        // ---- Int
        "i_neg" => {
            let x = pi(arg(0)?)?;
            both(pure(orl_i_neg(x), vi), meth(tr_catch(|| rt.i_neg(x, TR_C)), vi))
        }
        "i_abs" => {
            let x = pi(arg(0)?)?;
            both(pure(orl_i_abs(x), vi), meth(tr_catch(|| rt.i_abs(x, TR_C)), vi))
        }
        "i_isqrt" => {
            let x = pi(arg(0)?)?;
            both(pure(orl_i_isqrt(x), vi), meth(tr_catch(|| rt.i_isqrt(x, TR_C)), vi))
        }
        "i_add" => {
            let (x, y) = (pi(arg(0)?)?, pi(arg(1)?)?);
            both(pure(orl_i_add(x, y), vi), meth(tr_catch(|| rt.i_add(x, y, TR_C)), vi))
        }
        "i_sub" => {
            let (x, y) = (pi(arg(0)?)?, pi(arg(1)?)?);
            both(pure(orl_i_sub(x, y), vi), meth(tr_catch(|| rt.i_sub(x, y, TR_C)), vi))
        }
        "i_mul" => {
            let (x, y) = (pi(arg(0)?)?, pi(arg(1)?)?);
            both(pure(orl_i_mul(x, y), vi), meth(tr_catch(|| rt.i_mul(x, y, TR_C)), vi))
        }
        "i_div" => {
            let (x, y) = (pi(arg(0)?)?, pi(arg(1)?)?);
            both(pure(orl_i_div(x, y), vi), meth(tr_catch(|| rt.i_div(x, y, TR_C)), vi))
        }
        "i_quot" => {
            let (x, y) = (pi(arg(0)?)?, pi(arg(1)?)?);
            both(pure(orl_i_quot(x, y), vi), meth(tr_catch(|| rt.i_quot(x, y, TR_C)), vi))
        }
        "i_rem" => {
            let (x, y) = (pi(arg(0)?)?, pi(arg(1)?)?);
            both(pure(orl_i_rem(x, y), vi), meth(tr_catch(|| rt.i_rem(x, y, TR_C)), vi))
        }
        "i_max" => vi(Rt::i_max(pi(arg(0)?)?, pi(arg(1)?)?)),
        "i_min" => vi(Rt::i_min(pi(arg(0)?)?, pi(arg(1)?)?)),
        // ---- Fix
        "x_from_i" => {
            let n = pi(arg(0)?)?;
            both(pure(orl_x_from_i(n), vx), meth(tr_catch(|| rt.x_from_i(n, TR_C)), vx))
        }
        "x_neg" => {
            let x = px(arg(0)?)?;
            both(pure(orl_x_neg(x), vx), meth(tr_catch(|| rt.x_neg(x, TR_C)), vx))
        }
        "x_abs" => {
            let x = px(arg(0)?)?;
            both(pure(orl_x_abs(x), vx), meth(tr_catch(|| rt.x_abs(x, TR_C)), vx))
        }
        "x_sqrt" => {
            let x = px(arg(0)?)?;
            both(pure(orl_x_sqrt(x), vx), meth(tr_catch(|| rt.x_sqrt(x, TR_C)), vx))
        }
        "x_trunc" => vi(Rt::x_trunc(px(arg(0)?)?)),
        "x_round" => vi(Rt::x_round(px(arg(0)?)?)),
        "x_to_f" => {
            let (x, r) = (px(arg(0)?)?, pb(arg(1)?)?);
            both(pure(orl_x_to_f(x, r), vf), meth(tr_catch(|| rt.x_to_f(x, r, TR_C)), vf))
        }
        "x_add" => {
            let (x, y) = (px(arg(0)?)?, px(arg(1)?)?);
            both(pure(orl_x_add(x, y), vx), meth(tr_catch(|| rt.x_add(x, y, TR_C)), vx))
        }
        "x_sub" => {
            let (x, y) = (px(arg(0)?)?, px(arg(1)?)?);
            both(pure(orl_x_sub(x, y), vx), meth(tr_catch(|| rt.x_sub(x, y, TR_C)), vx))
        }
        "x_mul" => {
            let (x, y) = (px(arg(0)?)?, px(arg(1)?)?);
            both(pure(orl_x_mul(x, y), vx), meth(tr_catch(|| rt.x_mul(x, y, TR_C)), vx))
        }
        "x_div" => {
            let (x, y) = (px(arg(0)?)?, px(arg(1)?)?);
            both(pure(orl_x_div(x, y), vx), meth(tr_catch(|| rt.x_div(x, y, TR_C)), vx))
        }
        "x_max" => vx(Rt::x_max(px(arg(0)?)?, px(arg(1)?)?)),
        "x_min" => vx(Rt::x_min(px(arg(0)?)?, px(arg(1)?)?)),
        // ---- Float
        "f_neg" => vf(Rt::f_neg(pf(arg(0)?)?)),
        "f_abs" => vf(Rt::f_abs(pf(arg(0)?)?)),
        "f_sqrt" => vf(Rt::f_sqrt(pf(arg(0)?)?)),
        "f_trunc" => {
            let x = pf(arg(0)?)?;
            both(pure(orl_f_trunc(x), vi), meth(tr_catch(|| rt.f_trunc(x, TR_C)), vi))
        }
        "f_round" => {
            let x = pf(arg(0)?)?;
            both(pure(orl_f_round(x), vi), meth(tr_catch(|| rt.f_round(x, TR_C)), vi))
        }
        "f_to_x" => {
            let (x, r) = (pf(arg(0)?)?, pb(arg(1)?)?);
            both(pure(orl_f_to_x(x, r), vx), meth(tr_catch(|| rt.f_to_x(x, r, TR_C)), vx))
        }
        "f_add" => vf(Rt::f_add(pf(arg(0)?)?, pf(arg(1)?)?)),
        "f_sub" => vf(Rt::f_sub(pf(arg(0)?)?, pf(arg(1)?)?)),
        "f_mul" => vf(Rt::f_mul(pf(arg(0)?)?, pf(arg(1)?)?)),
        "f_div" => vf(Rt::f_div(pf(arg(0)?)?, pf(arg(1)?)?)),
        "f_max" => vf(Rt::f_max(pf(arg(0)?)?, pf(arg(1)?)?)),
        "f_min" => vf(Rt::f_min(pf(arg(0)?)?, pf(arg(1)?)?)),
        "f_lt" => vb(pf(arg(0)?)? < pf(arg(1)?)?),
        "f_eq" => vb(pf(arg(0)?)? == pf(arg(1)?)?),
        "f_from_i" => {
            let (n, r) = (pi(arg(0)?)?, pb(arg(1)?)?);
            both(pure(orl_f_from_i(n, r), vf), meth(tr_catch(|| rt.f_from_i(n, r, TR_C)), vf))
        }
        // ---- printing: the format function, and the text builder
        "fmt_i" => {
            let n = pi(arg(0)?)?;
            let mut v = Vec::new();
            orl_fmt_i(n, &mut v);
            rt.s_reset(TR_C);
            rt.s_i(n);
            both(vs(&v), vs(&rt.s_take()))
        }
        "fmt_x" => {
            let x = px(arg(0)?)?;
            let mut v = Vec::new();
            orl_fmt_x(x, &mut v);
            rt.s_reset(TR_C);
            rt.s_x(x);
            both(vs(&v), vs(&rt.s_take()))
        }
        "fmt_f" => {
            let x = pf(arg(0)?)?;
            let mut v = Vec::new();
            orl_fmt_f(x, &mut v);
            rt.s_reset(TR_C);
            rt.s_f(x);
            both(vs(&v), vs(&rt.s_take()))
        }
        // ---- SHA-256: one shot, and byte by byte through the running hash
        "sha256" => {
            let msg = phex(arg(0)?)?;
            let mut h = OrlSha256::new();
            for b in &msg {
                h.update(std::slice::from_ref(b));
            }
            both(format!("hex:{}", orl_hex(&orl_sha256(&msg))), format!("hex:{}", orl_hex(&h.finish())))
        }
        _ => return Err(format!("unknown op {}", op)),
    };
    if got == want {
        Ok(())
    } else {
        Err(format!("got {}", got))
    }
}

// ---------------------------------------------------------------- the event-chain check

fn tr_chain() -> bool {
    let law = orl_sha256(b"law");
    let mut rt = tr_rt(&orl_hex(&law), &[]);
    println!("head0 {}", orl_hex(&rt.head));
    rt.s_reset(1);
    rt.s_lit(b"hello");
    rt.say(1);
    println!("head1 {}", orl_hex(&rt.head));
    rt.ev_assign_i(2, 0, 42);
    println!("head2 {}", orl_hex(&rt.head));
    let r: Result<(), String> = tr_catch(|| rt.refuse("OVERFLOW", 3));
    println!("head3 {}", orl_hex(&rt.head));
    let status = match r {
        Ok(()) => "no refusal".to_string(),
        Err(s) => s,
    };
    println!("CHAIN events {}, {}", rt.events, status);
    rt.events == 3 && status == "status REFUSED OVERFLOW 3"
}

// ---------------------------------------------------------------- what no vector covers

fn st<T: std::fmt::Debug>(r: Result<T, String>) -> String {
    match r {
        Ok(v) => format!("ok {:?}", v),
        Err(s) => s,
    }
}

struct TrCount {
    passed: u32,
    total: u32,
}

impl TrCount {
    fn check(&mut self, name: &str, got: String, want: &str) {
        self.total += 1;
        if got == want {
            self.passed += 1;
        } else {
            println!("FAIL extra {}: got {:?}, want {:?}", name, got, want);
        }
    }
}

fn tr_extra() -> TrCount {
    let mut k = TrCount { passed: 0, total: 0 };

    // the builder's printing of every kind, lists included
    let mut rt = tr_rt(TR_ZERO_SEAL, &[]);
    rt.s_reset(4);
    rt.s_list(b'I', &[1, -2, i64::MIN]);
    rt.s_lit(b" ");
    rt.s_list(b'X', &[ORL_ONE, 1, -(ORL_ONE / 2)]);
    rt.s_lit(b" ");
    let nan_payload = 0x7FF0_0000_0000_0001u64 as i64;
    rt.s_list(
        b'F',
        &[Rt::f_bits(0.5), Rt::f_bits(-0.0), nan_payload, Rt::f_bits(f64::INFINITY), Rt::f_bits(f64::NEG_INFINITY)],
    );
    rt.s_lit(b" ");
    rt.s_list(b'B', &[1, 0]);
    rt.s_lit(b" ");
    rt.s_list(b'I', &[]);
    rt.s_lit(b" ");
    rt.s_b(true);
    rt.s_lit(b" ");
    rt.s_b(false);
    rt.s_lit(b" ");
    rt.s_t("Ørlǫg".as_bytes());
    rt.s_lit(b" ");
    rt.s_x(-1);
    rt.s_lit(b" ");
    rt.s_i(0);
    rt.s_lit(b" ");
    rt.s_f(1.0);
    k.check(
        "builder",
        String::from_utf8_lossy(&rt.s_take()).into_owned(),
        "[1, -2, -9223372036854775808] [1.0, 0.00000000023283064365386962890625, -0.5] \
         [0.5, -0.0, NaN, Infinity, -Infinity] [true, false] [] true false Ørlǫg \
         -0.00000000023283064365386962890625 0 1.0",
    );
    let before = rt.s_take();
    rt.say(4);
    k.check("say leaves the builder", format!("{}", rt.s_take() == before), "true");

    // TEXT-TOO-LONG at the clause of the last reset, exactly above 2^24 bytes
    rt.s_reset(77);
    let big = vec![b'a'; ORL_TEXT_MAX - 1];
    k.check("text fill", st(tr_catch(|| rt.s_lit(&big))), "ok ()");
    k.check("text to the limit", st(tr_catch(|| rt.s_lit(b"b"))), "ok ()");
    k.check("text empty at the limit", st(tr_catch(|| rt.s_lit(b""))), "ok ()");
    k.check("text over", st(tr_catch(|| rt.s_lit(b"c"))), "status REFUSED TEXT-TOO-LONG 77");
    rt.s_reset(78);
    rt.s_lit(&big);
    k.check("list over", st(tr_catch(|| rt.s_list(b'I', &[]))), "status REFUSED TEXT-TOO-LONG 78");
    rt.s_reset(79);
    rt.s_lit(&big[1..]);
    k.check("int to the limit", st(tr_catch(|| rt.s_i(-5))), "ok ()");
    k.check("int over", st(tr_catch(|| rt.s_i(1))), "status REFUSED TEXT-TOO-LONG 79");
    drop(big);

    // OUTPUT-TOO-LONG: the output may reach 2^30 bytes, not pass it
    let mut rt = tr_rt(TR_ZERO_SEAL, &[]);
    rt.out_bytes = ORL_OUTPUT_MAX - 3;
    rt.s_reset(5);
    rt.s_lit(b"ab");
    k.check("say to the limit", st(tr_catch(|| rt.say(5))), "ok ()");
    k.check("output bytes", rt.out_bytes.to_string(), "1073741824");
    rt.s_reset(6);
    k.check("say over", st(tr_catch(|| rt.say(6))), "status REFUSED OUTPUT-TOO-LONG 6");
    k.check("say over writes nothing", format!("{} {}", rt.out_bytes, rt.events), "1073741824 2");

    // lists
    let mut rt = tr_rt(TR_ZERO_SEAL, &[]);
    k.check("l_new negative", st(tr_catch(|| rt.l_new(-1, 0, 31))), "status REFUSED NEGATIVE-LENGTH 31");
    k.check("l_new above 2^24", st(tr_catch(|| rt.l_new((1 << 24) + 1, 0, 32))), "status REFUSED LIST-TOO-LONG 32");
    let mut v = rt.l_new(1 << 24, 5, 33);
    k.check("l_new 2^24", v.len().to_string(), "16777216");
    k.check("l_push at 2^24", st(tr_catch(|| rt.l_push(&mut v, 1, 34))), "status REFUSED LIST-TOO-LONG 34");
    k.check("l_get 0", st(tr_catch(|| rt.l_get(&v, 0, 35))), "status REFUSED INDEX-OUT-OF-RANGE 35");
    k.check("l_get last", st(tr_catch(|| rt.l_get(&v, 1 << 24, 35))), "ok 5");
    k.check("l_get past", st(tr_catch(|| rt.l_get(&v, (1 << 24) + 1, 36))), "status REFUSED INDEX-OUT-OF-RANGE 36");
    k.check("l_set -1", st(tr_catch(|| rt.l_set(&mut v, -1, 1, 37))), "status REFUSED INDEX-OUT-OF-RANGE 37");
    k.check("l_get MIN", st(tr_catch(|| rt.l_get(&v, i64::MIN, 37))), "status REFUSED INDEX-OUT-OF-RANGE 37");
    drop(v);
    let mut w = rt.l_new(0, 0, 38);
    k.check("l_pop empty", st(tr_catch(|| rt.l_pop(&mut w, 39))), "status REFUSED EMPTY-LIST 39");
    rt.l_push(&mut w, 4, 40);
    rt.l_push(&mut w, 6, 40);
    rt.l_set(&mut w, 1, 9, 40);
    rt.l_pop(&mut w, 40);
    k.check("list ops", format!("{:?} {}", w, rt.l_get(&w, 1, 40)), "[9] 9");

    // claims, musts, finish
    let mut rt = tr_rt(TR_ZERO_SEAL, &[7, 8]);
    k.check("claim true", st(tr_catch(|| rt.claim(1, 50, true, 3, 60, 4))), "ok ()");
    k.check("claim false", st(tr_catch(|| rt.claim(1, 51, false, 5, 61, 6))), "status REFUSED CLAIM-REFUTED 51");
    k.check("must true", st(tr_catch(|| rt.must(0, 52, true))), "ok ()");
    k.check("must false", st(tr_catch(|| rt.must(0, 53, false))), "status REFUSED MUST-FAILED 53");
    let fin: Result<(), String> = tr_catch(|| rt.finish());
    k.check("finish", st(fin), "status COMPLETED");
    let receipt = rt.receipt_text("COMPLETED");
    let claim_lines: Vec<&str> = receipt.lines().filter(|l| l.starts_with("claim")).collect();
    k.check("receipt claims", claim_lines.join("|"), "claims 2|claim 0 7 0 0 0 0 0|claim 1 8 2 1 8 61 6");
    k.check("events", rt.events.to_string(), "6");
    k
}

fn main() {
    std::panic::set_hook(Box::new(|_| {}));
    let path = match std::env::args_os().nth(1) {
        Some(p) => p,
        None => {
            eprintln!("usage: test_rt VECTORS");
            std::process::exit(2);
        }
    };
    let data = match std::fs::read(&path) {
        Ok(d) => d,
        Err(e) => {
            eprintln!("test_rt: cannot read {}: {}", std::path::Path::new(&path).display(), e);
            std::process::exit(2);
        }
    };
    let text = String::from_utf8_lossy(&data);
    let mut rt = tr_rt(TR_ZERO_SEAL, &[]);
    let (mut passed, mut total) = (0u64, 0u64);
    for line in text.split('\n') {
        if line.is_empty() {
            continue;
        }
        total += 1;
        match tr_line(&mut rt, line) {
            Ok(()) => passed += 1,
            Err(why) => println!("FAIL {}   [{}]", line, why),
        }
    }
    println!("RUNTIME VECTORS {} / {}", passed, total);
    let chain_ok = tr_chain();
    let extra = tr_extra();
    println!("RUNTIME EXTRA {} / {}", extra.passed, extra.total);
    if passed != total || !chain_ok || extra.passed != extra.total {
        std::process::exit(1);
    }
}
