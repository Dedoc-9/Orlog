// ØRLǪG OL-0 runtime for Rust: orlog_rt.rs
//
// The contract is RUNTIME-SPEC.md (DECLARED 2026-10-25). The numeric meaning of every function is
// src/orlog/numeric_ref.py (exact rationals, one rounding at the end); this file implements the same
// rules with integer and IEEE operations and is held to them by vectors/runtime-vectors.txt.
//
// This file is pasted at the top of a generated program whose `fn main` follows it in the same file
// (a harness may `include!` it instead). Therefore: standard library only, no `unsafe`, no `mod`, no
// `main`, no top-level `use` (the generated program may import the same names), every top-level
// name begins `Orl`, `orl_` or `ORL_` except `Rt`, and every item carries `#[allow(dead_code)]`
// because a program uses only part of the runtime.
//
// Shape: each refusable operation is a pure function `orl_*(...) -> OrlR<T>` whose `Err` holds the
// refusal code, plus a thin `Rt` method that refuses on `Err`. A method that can refuse (or that
// changes the run's state) takes `&mut self`; one that cannot is an associated function
// (`Rt::f_add(a, b)`).
//
// Nested refusable calls cannot be written `rt.x_div(rt.x_from_i(1, c), d, c)`: that borrows `rt`
// mutably twice. Generated code sequences them through temporaries, which also makes the
// evaluation order explicit.

/// The result of a refusable operation: the value, or the refusal code.
#[allow(dead_code)]
pub type OrlR<T> = Result<T, &'static str>;

#[allow(dead_code)]
pub const ORL_ONE: i64 = 1 << 32;
#[allow(dead_code)]
pub const ORL_CANON_NAN_BITS: u64 = 0x7FF8_0000_0000_0000;
#[allow(dead_code)]
pub const ORL_LIST_MAX: usize = 1 << 24;
#[allow(dead_code)]
pub const ORL_TEXT_MAX: usize = 1 << 24;
#[allow(dead_code)]
pub const ORL_OUTPUT_MAX: u64 = 1 << 30;

// ------------------------------------------------------------------ integer helpers

/// An exact integer into Int, or OVERFLOW.
#[allow(dead_code)]
fn orl_chk(v: i128) -> OrlR<i64> {
    if v < i64::MIN as i128 || v > i64::MAX as i128 {
        Err("OVERFLOW")
    } else {
        Ok(v as i64)
    }
}

/// (-1)^neg * mag into Int, or OVERFLOW.
#[allow(dead_code)]
fn orl_signed(neg: bool, mag: u128) -> OrlR<i64> {
    if mag > (1u128 << 64) {
        return Err("OVERFLOW");
    }
    let v = mag as i128;
    orl_chk(if neg { -v } else { v })
}

/// (round_half_even(m / 2^s), exact) for m < 2^64 and any s.
#[allow(dead_code)]
fn orl_rhe_shr(m: u64, s: u32) -> (u64, bool) {
    if s == 0 {
        return (m, true);
    }
    if s > 64 {
        // m < 2^64 <= 2^(s-1): the quotient is below one half
        return (0, m == 0);
    }
    let m = m as u128;
    let q = m >> s;
    let r = m & ((1u128 << s) - 1);
    let half = 1u128 << (s - 1);
    let up = r > half || (r == half && (q & 1) == 1);
    ((q + up as u128) as u64, r == 0)
}

/// floor(sqrt(n)), exactly (Newton's iteration from above).
#[allow(dead_code)]
fn orl_isqrt(n: u128) -> u128 {
    if n < 2 {
        return n;
    }
    let bits = 128 - n.leading_zeros();
    let mut x: u128 = 1u128 << ((bits + 1) / 2); // x >= sqrt(n), x <= 2^64
    loop {
        let y = (x + n / x) >> 1;
        if y >= x {
            return x;
        }
        x = y;
    }
}

// ------------------------------------------------------------------ binary64 helpers

/// True when the binary64 with these bits is finite.
#[allow(dead_code)]
fn orl_f_finite(bits: u64) -> bool {
    ((bits >> 52) & 0x7FF) != 0x7FF
}

/// True when the binary64 with these bits is a NaN.
#[allow(dead_code)]
fn orl_f_isnan(bits: u64) -> bool {
    ((bits >> 52) & 0x7FF) == 0x7FF && (bits & 0x000F_FFFF_FFFF_FFFF) != 0
}

/// The canonical bits: any NaN pattern becomes 0x7FF8000000000000, any other is kept.
///
/// Decided on the integer bits, which pass through `black_box` first. A float-level guard is
/// not safe at -O (MEASURED with rustc 1.96.1 on x86-64): `if a < 0.0 { NaN } else { a.sqrt() }`
/// and `let r = a.sqrt(); if r.is_nan() { NaN } else { r }` both compiled to a bare `sqrtsd`,
/// which returns x86's default NaN 0xFFF8000000000000. The IR optimizer rewrites
/// `is_nan(sqrt(a))` as `a < 0`, and the backend then drops the select of the NaN constant.
/// `black_box` hides where the bits came from, so the test cannot be tied back to the operation.
#[allow(dead_code)]
fn orl_canon_bits(bits: u64) -> u64 {
    let b = std::hint::black_box(bits);
    if orl_f_isnan(b) {
        ORL_CANON_NAN_BITS
    } else {
        b
    }
}

/// Finite binary64 bits -> (negative, m, e) with |value| = m * 2^e and m < 2^53.
#[allow(dead_code)]
fn orl_f_parts(bits: u64) -> (bool, u64, i32) {
    let neg = (bits >> 63) != 0;
    let be = ((bits >> 52) & 0x7FF) as i32;
    let frac = bits & 0x000F_FFFF_FFFF_FFFF;
    if be == 0 {
        (neg, frac, -1074)
    } else {
        (neg, frac | (1u64 << 52), be - 1075)
    }
}

/// The binary64 nearest (ties to even) to (-1)^neg * mag * 2^scale, built from integers:
/// (bits, exact). Zero gives +0.0. The callers keep the result normal and finite
/// (mag < 2^64, scale 0 or -32).
#[allow(dead_code)]
fn orl_to_f64_bits(mag: u64, neg: bool, scale: i32) -> (u64, bool) {
    if mag == 0 {
        return (0, true);
    }
    let len = 64 - mag.leading_zeros() as i32; // 1..=64
    let (mut q, exact, mut shift) = if len <= 53 {
        (mag << ((53 - len) as u32), true, len - 53)
    } else {
        let (q, ex) = orl_rhe_shr(mag, (len - 53) as u32);
        (q, ex, len - 53)
    };
    if q == (1u64 << 53) {
        q >>= 1;
        shift += 1;
    }
    // value = q * 2^(shift + scale), 2^52 <= q < 2^53
    let biased = (shift + scale + 52 + 1023) as u64;
    let sign = if neg { 1u64 << 63 } else { 0 };
    (sign | (biased << 52) | (q & 0x000F_FFFF_FFFF_FFFF), exact)
}

// ------------------------------------------------------------------ Int

#[allow(dead_code)]
pub fn orl_i_add(a: i64, b: i64) -> OrlR<i64> {
    a.checked_add(b).ok_or("OVERFLOW")
}

#[allow(dead_code)]
pub fn orl_i_sub(a: i64, b: i64) -> OrlR<i64> {
    a.checked_sub(b).ok_or("OVERFLOW")
}

#[allow(dead_code)]
pub fn orl_i_mul(a: i64, b: i64) -> OrlR<i64> {
    a.checked_mul(b).ok_or("OVERFLOW")
}

#[allow(dead_code)]
pub fn orl_i_neg(a: i64) -> OrlR<i64> {
    a.checked_neg().ok_or("OVERFLOW")
}

#[allow(dead_code)]
pub fn orl_i_abs(a: i64) -> OrlR<i64> {
    a.checked_abs().ok_or("OVERFLOW")
}

/// The exact quotient: DIVISION-BY-ZERO, then INEXACT-DIVISION, then OVERFLOW.
#[allow(dead_code)]
pub fn orl_i_div(a: i64, b: i64) -> OrlR<i64> {
    if b == 0 {
        return Err("DIVISION-BY-ZERO");
    }
    let (a, b) = (a as i128, b as i128); // no INT64_MIN % -1 trap
    if a % b != 0 {
        return Err("INEXACT-DIVISION");
    }
    orl_chk(a / b)
}

/// Euclidean quotient: a = b*q + r, 0 <= r < |b|.
#[allow(dead_code)]
pub fn orl_i_quot(a: i64, b: i64) -> OrlR<i64> {
    if b == 0 {
        return Err("DIVISION-BY-ZERO");
    }
    orl_chk((a as i128).div_euclid(b as i128))
}

/// Euclidean remainder: 0 <= r < |b|.
#[allow(dead_code)]
pub fn orl_i_rem(a: i64, b: i64) -> OrlR<i64> {
    if b == 0 {
        return Err("DIVISION-BY-ZERO");
    }
    Ok((a as i128).rem_euclid(b as i128) as i64)
}

#[allow(dead_code)]
pub fn orl_i_isqrt(a: i64) -> OrlR<i64> {
    if a < 0 {
        return Err("NEGATIVE-SQRT");
    }
    Ok(orl_isqrt(a as u128) as i64)
}

// ------------------------------------------------------------------ Fix (raw int64 = value * 2^32)

#[allow(dead_code)]
pub fn orl_x_from_i(n: i64) -> OrlR<i64> {
    orl_chk((n as i128) * (ORL_ONE as i128))
}

#[allow(dead_code)]
pub fn orl_x_add(a: i64, b: i64) -> OrlR<i64> {
    a.checked_add(b).ok_or("OVERFLOW")
}

#[allow(dead_code)]
pub fn orl_x_sub(a: i64, b: i64) -> OrlR<i64> {
    a.checked_sub(b).ok_or("OVERFLOW")
}

#[allow(dead_code)]
pub fn orl_x_neg(a: i64) -> OrlR<i64> {
    a.checked_neg().ok_or("OVERFLOW")
}

#[allow(dead_code)]
pub fn orl_x_abs(a: i64) -> OrlR<i64> {
    a.checked_abs().ok_or("OVERFLOW")
}

/// round_half_even(a*b / 2^32), checked.
#[allow(dead_code)]
pub fn orl_x_mul(a: i64, b: i64) -> OrlR<i64> {
    let p = (a as i128) * (b as i128); // |p| <= 2^126
    let q = p >> 32; // floor(p / 2^32)
    let r = p & 0xFFFF_FFFF; // p - q * 2^32, in [0, 2^32)
    let half: i128 = 1 << 31;
    let q = if r > half || (r == half && (q & 1) == 1) { q + 1 } else { q };
    orl_chk(q)
}

/// DIVISION-BY-ZERO; round_half_even(a * 2^32 / b), checked.
#[allow(dead_code)]
pub fn orl_x_div(a: i64, b: i64) -> OrlR<i64> {
    if b == 0 {
        return Err("DIVISION-BY-ZERO");
    }
    let mut n = (a as i128) * (ORL_ONE as i128); // |n| <= 2^95
    let mut d = b as i128;
    if d < 0 {
        n = -n;
        d = -d;
    }
    let q = n.div_euclid(d); // floor, since d > 0
    let r = n.rem_euclid(d); // n - q * d, in [0, d)
    let twice = 2 * r;
    let q = if twice > d || (twice == d && (q & 1) == 1) { q + 1 } else { q };
    orl_chk(q)
}

/// isqrt(a * 2^32); NEGATIVE-SQRT.
#[allow(dead_code)]
pub fn orl_x_sqrt(a: i64) -> OrlR<i64> {
    if a < 0 {
        return Err("NEGATIVE-SQRT");
    }
    Ok(orl_isqrt((a as u128) << 32) as i64)
}

/// To Int, toward zero.
#[allow(dead_code)]
pub fn orl_x_trunc(a: i64) -> i64 {
    let q = (a.unsigned_abs() >> 32) as i64; // <= 2^31
    if a < 0 {
        -q
    } else {
        q
    }
}

/// To Int, half-even.
#[allow(dead_code)]
pub fn orl_x_round(a: i64) -> i64 {
    let (q, _) = orl_rhe_shr(a.unsigned_abs(), 32);
    let q = q as i64; // <= 2^31
    if a < 0 {
        -q
    } else {
        q
    }
}

// ------------------------------------------------------------------ conversions

/// Fix -> Float: exact or INEXACT-CONVERSION; rounded = nearest-even.
#[allow(dead_code)]
pub fn orl_x_to_f(a: i64, rounded: bool) -> OrlR<f64> {
    let (bits, exact) = orl_to_f64_bits(a.unsigned_abs(), a < 0, -32);
    if !exact && !rounded {
        return Err("INEXACT-CONVERSION");
    }
    Ok(f64::from_bits(bits))
}

/// Int -> Float: exact or INEXACT-CONVERSION; rounded = nearest-even.
#[allow(dead_code)]
pub fn orl_f_from_i(n: i64, rounded: bool) -> OrlR<f64> {
    let (bits, exact) = orl_to_f64_bits(n.unsigned_abs(), n < 0, 0);
    if !exact && !rounded {
        return Err("INEXACT-CONVERSION");
    }
    Ok(f64::from_bits(bits))
}

/// Float -> Fix: NOT-FINITE; x * 2^32 exact or INEXACT-CONVERSION (rounded: half-even); OVERFLOW.
#[allow(dead_code)]
pub fn orl_f_to_x(x: f64, rounded: bool) -> OrlR<i64> {
    let bits = x.to_bits();
    if !orl_f_finite(bits) {
        return Err("NOT-FINITE");
    }
    let (neg, m, e) = orl_f_parts(bits);
    if m == 0 {
        return Ok(0);
    }
    let t = e + 32;
    let mag: u128 = if t >= 0 {
        if t > 74 {
            return Err("OVERFLOW");
        }
        (m as u128) << t
    } else {
        let (q, exact) = orl_rhe_shr(m, (-t) as u32);
        if !exact && !rounded {
            return Err("INEXACT-CONVERSION");
        }
        q as u128
    };
    orl_signed(neg, mag)
}

/// Float -> Int toward zero: NOT-FINITE, OVERFLOW.
#[allow(dead_code)]
pub fn orl_f_trunc(x: f64) -> OrlR<i64> {
    let bits = x.to_bits();
    if !orl_f_finite(bits) {
        return Err("NOT-FINITE");
    }
    let (neg, m, e) = orl_f_parts(bits);
    let mag: u128 = if e >= 0 {
        if e > 74 {
            return Err("OVERFLOW");
        }
        (m as u128) << e
    } else if e <= -64 {
        0
    } else {
        (m >> ((-e) as u32)) as u128
    };
    orl_signed(neg, mag)
}

/// Float -> Int half-even: NOT-FINITE, OVERFLOW.
#[allow(dead_code)]
pub fn orl_f_round(x: f64) -> OrlR<i64> {
    let bits = x.to_bits();
    if !orl_f_finite(bits) {
        return Err("NOT-FINITE");
    }
    let (neg, m, e) = orl_f_parts(bits);
    let mag: u128 = if e >= 0 {
        if e > 74 {
            return Err("OVERFLOW");
        }
        (m as u128) << e
    } else {
        orl_rhe_shr(m, (-e) as u32).0 as u128
    };
    orl_signed(neg, mag)
}

// ------------------------------------------------------------------ printing (exact decimals)

/// Decimal digits of an unsigned integer.
#[allow(dead_code)]
pub fn orl_fmt_u(v: u64, out: &mut Vec<u8>) {
    let mut buf = [0u8; 20];
    let mut i = buf.len();
    let mut v = v;
    loop {
        i -= 1;
        buf[i] = b'0' + (v % 10) as u8;
        v /= 10;
        if v == 0 {
            break;
        }
    }
    out.extend_from_slice(&buf[i..]);
}

#[allow(dead_code)]
pub fn orl_fmt_i(n: i64, out: &mut Vec<u8>) {
    if n < 0 {
        out.push(b'-');
    }
    orl_fmt_u(n.unsigned_abs(), out);
}

/// Sign, integer part of |raw| / 2^32, then every fraction digit, or `.0`.
#[allow(dead_code)]
pub fn orl_fmt_x(a: i64, out: &mut Vec<u8>) {
    if a < 0 {
        out.push(b'-');
    }
    let m = a.unsigned_abs();
    orl_fmt_u(m >> 32, out);
    out.push(b'.');
    let mut r = m & 0xFFFF_FFFF;
    if r == 0 {
        out.push(b'0');
        return;
    }
    while r != 0 {
        r *= 10; // < 2^36
        out.push(b'0' + (r >> 32) as u8);
        r &= 0xFFFF_FFFF;
    }
}

#[allow(dead_code)]
pub fn orl_fmt_b(v: bool, out: &mut Vec<u8>) {
    out.extend_from_slice(if v { &b"true"[..] } else { &b"false"[..] });
}

/// A small bignum: base 10^9 limbs, least significant first.
#[allow(dead_code)]
fn orl_big_mul_small(v: &mut Vec<u32>, k: u64) {
    // k <= 1220703125 and limb < 10^9: limb * k + carry < 2^63
    let mut carry: u64 = 0;
    for limb in v.iter_mut() {
        let t = (*limb as u64) * k + carry;
        *limb = (t % 1_000_000_000) as u32;
        carry = t / 1_000_000_000;
    }
    while carry != 0 {
        v.push((carry % 1_000_000_000) as u32);
        carry /= 1_000_000_000;
    }
}

#[allow(dead_code)]
fn orl_big_digits(v: &[u32], out: &mut Vec<u8>) {
    let mut i = v.len();
    while i > 1 && v[i - 1] == 0 {
        i -= 1;
    }
    if i == 0 {
        out.push(b'0');
        return;
    }
    orl_fmt_u(v[i - 1] as u64, out);
    while i > 1 {
        i -= 1;
        let mut x = v[i - 1];
        let mut buf = [b'0'; 9];
        for j in (0..9).rev() {
            buf[j] = b'0' + (x % 10) as u8;
            x /= 10;
        }
        out.extend_from_slice(&buf);
    }
}

/// NaN, Infinity, -Infinity; otherwise the sign bit, then the EXACT decimal value of the binary64.
#[allow(dead_code)]
pub fn orl_fmt_f(x: f64, out: &mut Vec<u8>) {
    let bits = x.to_bits();
    if !orl_f_finite(bits) {
        if orl_f_isnan(bits) {
            out.extend_from_slice(b"NaN");
        } else if (bits >> 63) != 0 {
            out.extend_from_slice(b"-Infinity");
        } else {
            out.extend_from_slice(b"Infinity");
        }
        return;
    }
    let (neg, mut m, mut e) = orl_f_parts(bits);
    if neg {
        out.push(b'-');
    }
    if m == 0 {
        out.extend_from_slice(b"0.0");
        return;
    }
    let tz = m.trailing_zeros();
    m >>= tz; // m odd from here
    e += tz as i32;
    let mut big: Vec<u32> = Vec::with_capacity(8);
    let mut t = m;
    loop {
        big.push((t % 1_000_000_000) as u32);
        t /= 1_000_000_000;
        if t == 0 {
            break;
        }
    }
    if e >= 0 {
        let mut k = e as u32;
        while k >= 30 {
            orl_big_mul_small(&mut big, 1u64 << 30);
            k -= 30;
        }
        if k > 0 {
            orl_big_mul_small(&mut big, 1u64 << k);
        }
        orl_big_digits(&big, out);
        out.extend_from_slice(b".0");
    } else {
        // m * 2^e = m * 5^k / 10^k; m odd, so the last of the k fraction digits is 5
        let k = (-e) as usize;
        let mut j = k;
        while j >= 13 {
            orl_big_mul_small(&mut big, 1_220_703_125); // 5^13
            j -= 13;
        }
        if j > 0 {
            orl_big_mul_small(&mut big, 5u64.pow(j as u32));
        }
        let mut d: Vec<u8> = Vec::with_capacity(k + 24);
        orl_big_digits(&big, &mut d);
        if d.len() > k {
            let split = d.len() - k;
            out.extend_from_slice(&d[..split]);
            out.push(b'.');
            out.extend_from_slice(&d[split..]);
        } else {
            out.extend_from_slice(b"0.");
            for _ in d.len()..k {
                out.push(b'0');
            }
            out.extend_from_slice(&d);
        }
    }
}

/// One list element, printed by its tag (I X F B; floats as their bits; bools 0/1).
#[allow(dead_code)]
pub fn orl_fmt_slot(tag: u8, v: i64, out: &mut Vec<u8>) {
    match tag {
        b'X' => orl_fmt_x(v, out),
        b'F' => orl_fmt_f(f64::from_bits(v as u64), out),
        b'B' => orl_fmt_b(v != 0, out),
        _ => orl_fmt_i(v, out),
    }
}

// ------------------------------------------------------------------ hex

#[allow(dead_code)]
pub fn orl_hex_into(bytes: &[u8], out: &mut Vec<u8>) {
    const D: &[u8; 16] = b"0123456789abcdef";
    for &b in bytes {
        out.push(D[(b >> 4) as usize]);
        out.push(D[(b & 15) as usize]);
    }
}

#[allow(dead_code)]
pub fn orl_hex(bytes: &[u8]) -> String {
    let mut v = Vec::with_capacity(bytes.len() * 2);
    orl_hex_into(bytes, &mut v);
    String::from_utf8(v).unwrap_or_default()
}

#[allow(dead_code)]
fn orl_hexval(c: u8) -> Option<u8> {
    match c {
        b'0'..=b'9' => Some(c - b'0'),
        b'a'..=b'f' => Some(c - b'a' + 10),
        b'A'..=b'F' => Some(c - b'A' + 10),
        _ => None,
    }
}

// ------------------------------------------------------------------ SHA-256 (FIPS 180-4)

#[allow(dead_code)]
const ORL_SHA256_K: [u32; 64] = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
];

#[allow(dead_code)]
fn orl_sha256_block(h: &mut [u32; 8], block: &[u8]) {
    let mut w = [0u32; 64];
    for t in 0..16 {
        w[t] = u32::from_be_bytes([block[4 * t], block[4 * t + 1], block[4 * t + 2], block[4 * t + 3]]);
    }
    for t in 16..64 {
        let s0 = w[t - 15].rotate_right(7) ^ w[t - 15].rotate_right(18) ^ (w[t - 15] >> 3);
        let s1 = w[t - 2].rotate_right(17) ^ w[t - 2].rotate_right(19) ^ (w[t - 2] >> 10);
        w[t] = w[t - 16].wrapping_add(s0).wrapping_add(w[t - 7]).wrapping_add(s1);
    }
    let mut a = h[0];
    let mut b = h[1];
    let mut c = h[2];
    let mut d = h[3];
    let mut e = h[4];
    let mut f = h[5];
    let mut g = h[6];
    let mut hh = h[7];
    for t in 0..64 {
        let s1 = e.rotate_right(6) ^ e.rotate_right(11) ^ e.rotate_right(25);
        let ch = (e & f) ^ (!e & g);
        let t1 = hh
            .wrapping_add(s1)
            .wrapping_add(ch)
            .wrapping_add(ORL_SHA256_K[t])
            .wrapping_add(w[t]);
        let s0 = a.rotate_right(2) ^ a.rotate_right(13) ^ a.rotate_right(22);
        let maj = (a & b) ^ (a & c) ^ (b & c);
        let t2 = s0.wrapping_add(maj);
        hh = g;
        g = f;
        f = e;
        e = d.wrapping_add(t1);
        d = c;
        c = b;
        b = a;
        a = t1.wrapping_add(t2);
    }
    h[0] = h[0].wrapping_add(a);
    h[1] = h[1].wrapping_add(b);
    h[2] = h[2].wrapping_add(c);
    h[3] = h[3].wrapping_add(d);
    h[4] = h[4].wrapping_add(e);
    h[5] = h[5].wrapping_add(f);
    h[6] = h[6].wrapping_add(g);
    h[7] = h[7].wrapping_add(hh);
}

/// A running SHA-256.
#[allow(dead_code)]
#[derive(Clone)]
pub struct OrlSha256 {
    h: [u32; 8],
    buf: [u8; 64],
    n: usize,
    len: u64,
}

#[allow(dead_code)]
impl OrlSha256 {
    pub fn new() -> OrlSha256 {
        OrlSha256 {
            h: [
                0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab,
                0x5be0cd19,
            ],
            buf: [0u8; 64],
            n: 0,
            len: 0,
        }
    }

    pub fn update(&mut self, data: &[u8]) {
        let mut data = data;
        self.len = self.len.wrapping_add(data.len() as u64);
        if self.n > 0 {
            let take = std::cmp::min(64 - self.n, data.len());
            self.buf[self.n..self.n + take].copy_from_slice(&data[..take]);
            self.n += take;
            data = &data[take..];
            if self.n == 64 {
                let block = self.buf;
                orl_sha256_block(&mut self.h, &block);
                self.n = 0;
            }
        }
        while data.len() >= 64 {
            orl_sha256_block(&mut self.h, &data[..64]);
            data = &data[64..];
        }
        if !data.is_empty() {
            self.buf[..data.len()].copy_from_slice(data);
            self.n = data.len();
        }
    }

    /// The digest of everything given so far (the running state is not changed).
    pub fn finish(&self) -> [u8; 32] {
        let mut s = self.clone();
        let bit_len = self.len.wrapping_mul(8);
        let mut pad = [0u8; 64];
        pad[0] = 0x80;
        let pad_len = if s.n < 56 { 56 - s.n } else { 120 - s.n }; // 1..=64
        s.update(&pad[..pad_len]);
        s.update(&bit_len.to_be_bytes());
        let mut out = [0u8; 32];
        for i in 0..8 {
            out[4 * i..4 * i + 4].copy_from_slice(&s.h[i].to_be_bytes());
        }
        out
    }
}

#[allow(dead_code)]
pub fn orl_sha256(data: &[u8]) -> [u8; 32] {
    let mut h = OrlSha256::new();
    h.update(data);
    h.finish()
}

// ------------------------------------------------------------------ event value encodings

/// The bytes of one slot under its tag, without the tag: 8 bytes big-endian for I and X, the
/// canonical bits for F (any NaN as 0x7FF8000000000000), 1 byte 0/1 for B. An unknown tag is
/// encoded as 8 bytes.
#[allow(dead_code)]
fn orl_enc_slot(tag: u8, v: i64, p: &mut Vec<u8>) {
    match tag {
        b'B' => p.push(if v != 0 { 1 } else { 0 }),
        b'F' => p.extend_from_slice(&orl_canon_bits(v as u64).to_be_bytes()),
        _ => p.extend_from_slice(&v.to_be_bytes()),
    }
}

/// The value encoding of a slot under its tag: the tag byte, then the slot's bytes.
#[allow(dead_code)]
fn orl_enc_value(tag: u8, v: i64, p: &mut Vec<u8>) {
    p.push(tag);
    orl_enc_slot(tag, v, p);
}

// ------------------------------------------------------------------ lists

/// The length for l_new: NEGATIVE-LENGTH, LIST-TOO-LONG above 2^24.
#[allow(dead_code)]
pub fn orl_l_len(n: i64) -> OrlR<usize> {
    if n < 0 {
        Err("NEGATIVE-LENGTH")
    } else if n > ORL_LIST_MAX as i64 {
        Err("LIST-TOO-LONG")
    } else {
        Ok(n as usize)
    }
}

/// The 0-based position of 1-based index k in a list of length len: INDEX-OUT-OF-RANGE.
#[allow(dead_code)]
pub fn orl_l_index(len: usize, k: i64) -> OrlR<usize> {
    if k < 1 || (k as u64) > (len as u64) {
        Err("INDEX-OUT-OF-RANGE")
    } else {
        Ok((k - 1) as usize)
    }
}

// ------------------------------------------------------------------ the run

/// Writes a message on stderr and exits with status 2 (a file that cannot be opened or written).
#[allow(dead_code)]
fn orl_fatal(msg: &str) -> ! {
    let mut e = std::io::stderr();
    let _ = std::io::Write::write_all(&mut e, msg.as_bytes());
    let _ = std::io::Write::write_all(&mut e, b"\n");
    let _ = std::io::Write::flush(&mut e);
    std::process::exit(2)
}

#[allow(dead_code)]
fn orl_create(path: &std::ffi::OsStr, what: &str) -> std::fs::File {
    match std::fs::File::create(path) {
        Ok(f) => f,
        Err(e) => orl_fatal(&format!(
            "orlog: cannot open the {} file {}: {}",
            what,
            std::path::Path::new(path).display(),
            e
        )),
    }
}

/// A seal given to init: exactly 64 hex digits, as 32 bytes.
#[allow(dead_code)]
fn orl_seal(hex: &str, what: &str) -> [u8; 32] {
    let b = hex.as_bytes();
    let mut raw = [0u8; 32];
    if b.len() != 64 {
        orl_fatal(&format!("orlog: the {} seal is not 64 hex digits", what));
    }
    for i in 0..32 {
        match (orl_hexval(b[2 * i]), orl_hexval(b[2 * i + 1])) {
            (Some(hi), Some(lo)) => raw[i] = (hi << 4) | lo,
            _ => orl_fatal(&format!("orlog: the {} seal is not 64 hex digits", what)),
        }
    }
    raw
}

/// What the receipt reports of one declared claim.
#[allow(dead_code)]
pub struct OrlClaimStat {
    clause: u32,
    evaluations: u64,
    trues: u64,
    cost: u64,
    ref_clause: u32,
    ref_cost: u64,
}

/// The panic payload of `refuse` and `finish` in a test run (never in a program: `Rt::init`
/// always exits).
#[allow(dead_code)]
pub struct OrlEnded {
    pub status: String,
}

/// The run: the event hash chain, the output file and its running SHA-256, the text builder,
/// the claims, the receipt.
#[allow(dead_code)]
pub struct Rt {
    /// The operation counter; only the generated code changes it.
    pub ops: u64,
    backend: String,
    law_hex: String,
    text_hex: String,
    head: [u8; 32],
    events: u64,
    out: Option<std::io::BufWriter<std::fs::File>>,
    receipt: Option<std::fs::File>,
    trace: Option<std::io::BufWriter<std::fs::File>>,
    out_bytes: u64,
    out_sha: OrlSha256,
    sb: Vec<u8>,
    sb_clause: u32,
    claims: Vec<OrlClaimStat>,
    test_unwind: bool,
}

#[allow(dead_code)]
impl Rt {
    // ---------------------------------------------------------- init

    /// argv[1] the output path, argv[2] the receipt path, optional argv[3] the trace path (further
    /// arguments are ignored). All three files are created at once; a missing argument, a file that
    /// cannot be opened or a seal that is not 64 hex digits ends the process with status 2 and a
    /// message on stderr, before anything is written.
    pub fn init(backend: &str, law_hex: &str, text_hex: &str, claim_clause: &[u32]) -> Rt {
        let args: Vec<std::ffi::OsString> = std::env::args_os().collect();
        if args.len() < 3 {
            orl_fatal("orlog: usage: PROGRAM OUTPUT RECEIPT [TRACE]");
        }
        let _ = orl_seal(law_hex, "law");
        let _ = orl_seal(text_hex, "text");
        let out = orl_create(&args[1], "output");
        let receipt = orl_create(&args[2], "receipt");
        let trace = if args.len() > 3 { Some(orl_create(&args[3], "trace")) } else { None };
        Rt::with_sinks(backend, law_hex, text_hex, claim_clause, Some(out), Some(receipt), trace, false)
    }

    /// The run over the given files (any may be absent). `test_unwind` makes `refuse` and
    /// `finish` panic with an `OrlEnded` instead of writing the receipt and exiting: a test hook,
    /// set only by the harness.
    fn with_sinks(
        backend: &str,
        law_hex: &str,
        text_hex: &str,
        claim_clause: &[u32],
        out: Option<std::fs::File>,
        receipt: Option<std::fs::File>,
        trace: Option<std::fs::File>,
        test_unwind: bool,
    ) -> Rt {
        let law_seal = orl_seal(law_hex, "law");
        let text_seal = orl_seal(text_hex, "text");
        let mut h = OrlSha256::new();
        h.update(b"orlog-trace-0");
        h.update(&law_seal);
        Rt {
            ops: 0,
            backend: backend.to_string(),
            law_hex: orl_hex(&law_seal),
            text_hex: orl_hex(&text_seal),
            head: h.finish(),
            events: 0,
            out: out.map(|f| std::io::BufWriter::with_capacity(1 << 16, f)),
            receipt,
            trace: trace.map(|f| std::io::BufWriter::with_capacity(1 << 16, f)),
            out_bytes: 0,
            out_sha: OrlSha256::new(),
            sb: Vec::new(),
            sb_clause: 0,
            claims: claim_clause
                .iter()
                .map(|&c| OrlClaimStat {
                    clause: c,
                    evaluations: 0,
                    trues: 0,
                    cost: 0,
                    ref_clause: 0,
                    ref_cost: 0,
                })
                .collect(),
            test_unwind,
        }
    }

    fn or_refuse<T>(&mut self, r: OrlR<T>, c: u32) -> T {
        match r {
            Ok(v) => v,
            Err(code) => self.refuse(code, c),
        }
    }

    // ---------------------------------------------------------- Int

    pub fn i_add(&mut self, a: i64, b: i64, c: u32) -> i64 {
        self.or_refuse(orl_i_add(a, b), c)
    }
    pub fn i_sub(&mut self, a: i64, b: i64, c: u32) -> i64 {
        self.or_refuse(orl_i_sub(a, b), c)
    }
    pub fn i_mul(&mut self, a: i64, b: i64, c: u32) -> i64 {
        self.or_refuse(orl_i_mul(a, b), c)
    }
    pub fn i_neg(&mut self, a: i64, c: u32) -> i64 {
        self.or_refuse(orl_i_neg(a), c)
    }
    pub fn i_abs(&mut self, a: i64, c: u32) -> i64 {
        self.or_refuse(orl_i_abs(a), c)
    }
    pub fn i_div(&mut self, a: i64, b: i64, c: u32) -> i64 {
        self.or_refuse(orl_i_div(a, b), c)
    }
    pub fn i_quot(&mut self, a: i64, b: i64, c: u32) -> i64 {
        self.or_refuse(orl_i_quot(a, b), c)
    }
    pub fn i_rem(&mut self, a: i64, b: i64, c: u32) -> i64 {
        self.or_refuse(orl_i_rem(a, b), c)
    }
    pub fn i_isqrt(&mut self, a: i64, c: u32) -> i64 {
        self.or_refuse(orl_i_isqrt(a), c)
    }
    pub fn i_max(a: i64, b: i64) -> i64 {
        if a > b {
            a
        } else {
            b
        }
    }
    pub fn i_min(a: i64, b: i64) -> i64 {
        if a < b {
            a
        } else {
            b
        }
    }

    // ---------------------------------------------------------- Fix

    pub fn x_from_i(&mut self, n: i64, c: u32) -> i64 {
        self.or_refuse(orl_x_from_i(n), c)
    }
    pub fn x_add(&mut self, a: i64, b: i64, c: u32) -> i64 {
        self.or_refuse(orl_x_add(a, b), c)
    }
    pub fn x_sub(&mut self, a: i64, b: i64, c: u32) -> i64 {
        self.or_refuse(orl_x_sub(a, b), c)
    }
    pub fn x_neg(&mut self, a: i64, c: u32) -> i64 {
        self.or_refuse(orl_x_neg(a), c)
    }
    pub fn x_abs(&mut self, a: i64, c: u32) -> i64 {
        self.or_refuse(orl_x_abs(a), c)
    }
    pub fn x_mul(&mut self, a: i64, b: i64, c: u32) -> i64 {
        self.or_refuse(orl_x_mul(a, b), c)
    }
    pub fn x_div(&mut self, a: i64, b: i64, c: u32) -> i64 {
        self.or_refuse(orl_x_div(a, b), c)
    }
    pub fn x_sqrt(&mut self, a: i64, c: u32) -> i64 {
        self.or_refuse(orl_x_sqrt(a), c)
    }
    pub fn x_trunc(a: i64) -> i64 {
        orl_x_trunc(a)
    }
    pub fn x_round(a: i64) -> i64 {
        orl_x_round(a)
    }
    pub fn x_max(a: i64, b: i64) -> i64 {
        if a > b {
            a
        } else {
            b
        }
    }
    pub fn x_min(a: i64, b: i64) -> i64 {
        if a < b {
            a
        } else {
            b
        }
    }
    pub fn x_to_f(&mut self, a: i64, rounded: bool, c: u32) -> f64 {
        self.or_refuse(orl_x_to_f(a, rounded), c)
    }
    pub fn f_to_x(&mut self, x: f64, rounded: bool, c: u32) -> i64 {
        self.or_refuse(orl_f_to_x(x, rounded), c)
    }

    // ---------------------------------------------------------- Float

    /// Any NaN -> the canonical quiet NaN 0x7FF8000000000000 (decided on the bits: see
    /// `orl_canon_bits`).
    pub fn f_canon(x: f64) -> f64 {
        f64::from_bits(orl_canon_bits(x.to_bits()))
    }
    pub fn f_add(a: f64, b: f64) -> f64 {
        Rt::f_canon(a + b)
    }
    pub fn f_sub(a: f64, b: f64) -> f64 {
        Rt::f_canon(a - b)
    }
    pub fn f_mul(a: f64, b: f64) -> f64 {
        Rt::f_canon(a * b)
    }
    /// IEEE division (by a signed zero: a signed infinity, or NaN for 0/0 and NaN/0), then canon.
    pub fn f_div(a: f64, b: f64) -> f64 {
        Rt::f_canon(a / b)
    }
    pub fn f_neg(a: f64) -> f64 {
        Rt::f_canon(-a)
    }
    pub fn f_abs(a: f64) -> f64 {
        Rt::f_canon(a.abs())
    }
    /// Correctly rounded square root, then canon: NaN or negative (not -0.0) gives the canonical
    /// NaN, sqrt(-0.0) = -0.0. No float-level guard before the root (see `orl_canon_bits`).
    pub fn f_sqrt(a: f64) -> f64 {
        Rt::f_canon(a.sqrt())
    }
    /// `a > b ? a : b`, by the comparison (not fmax); a NaN passes through as it is.
    pub fn f_max(a: f64, b: f64) -> f64 {
        if a > b {
            a
        } else {
            b
        }
    }
    /// `a < b ? a : b`, by the comparison (not fmin); a NaN passes through as it is.
    pub fn f_min(a: f64, b: f64) -> f64 {
        if a < b {
            a
        } else {
            b
        }
    }
    pub fn f_from_i(&mut self, n: i64, rounded: bool, c: u32) -> f64 {
        self.or_refuse(orl_f_from_i(n, rounded), c)
    }
    pub fn f_trunc(&mut self, x: f64, c: u32) -> i64 {
        self.or_refuse(orl_f_trunc(x), c)
    }
    pub fn f_round(&mut self, x: f64, c: u32) -> i64 {
        self.or_refuse(orl_f_round(x), c)
    }
    pub fn f_bits(x: f64) -> i64 {
        x.to_bits() as i64
    }
    pub fn bits_f(i: i64) -> f64 {
        f64::from_bits(i as u64)
    }

    // ---------------------------------------------------------- the text builder

    /// Empties the builder; `c` is the clause of any TEXT-TOO-LONG until the next reset.
    pub fn s_reset(&mut self, c: u32) {
        self.sb.clear();
        self.sb_clause = c;
    }
    fn s_room(&mut self, n: usize) {
        if n > ORL_TEXT_MAX - self.sb.len() {
            let c = self.sb_clause;
            self.refuse("TEXT-TOO-LONG", c);
        }
    }
    /// Raw UTF-8 bytes.
    pub fn s_lit(&mut self, p: &[u8]) {
        self.s_room(p.len());
        self.sb.extend_from_slice(p);
    }
    pub fn s_i(&mut self, v: i64) {
        let mut t = Vec::with_capacity(20);
        orl_fmt_i(v, &mut t);
        self.s_lit(&t);
    }
    pub fn s_x(&mut self, raw: i64) {
        let mut t = Vec::with_capacity(48);
        orl_fmt_x(raw, &mut t);
        self.s_lit(&t);
    }
    pub fn s_f(&mut self, x: f64) {
        let mut t = Vec::with_capacity(32);
        orl_fmt_f(x, &mut t);
        self.s_lit(&t);
    }
    pub fn s_b(&mut self, v: bool) {
        let mut t = Vec::with_capacity(5);
        orl_fmt_b(v, &mut t);
        self.s_lit(&t);
    }
    pub fn s_t(&mut self, t: &[u8]) {
        self.s_lit(t);
    }
    /// `[` elements printed by the tag (I X F B), separated by `, `, `]`. The limit is checked
    /// piece by piece, so a list never builds more than the limit in memory; the refusal (code
    /// and clause) is the same as for the whole append.
    pub fn s_list(&mut self, tag: u8, slots: &[i64]) {
        self.s_lit(b"[");
        let mut t: Vec<u8> = Vec::with_capacity(48);
        for (i, &v) in slots.iter().enumerate() {
            t.clear();
            if i > 0 {
                t.extend_from_slice(b", ");
            }
            orl_fmt_slot(tag, v, &mut t);
            self.s_lit(&t);
        }
        self.s_lit(b"]");
    }
    /// A heap copy of the builder's bytes (the builder is not changed).
    pub fn s_take(&self) -> Vec<u8> {
        self.sb.clone()
    }

    // ---------------------------------------------------------- Say

    /// The line is the builder's bytes plus one LF: OUTPUT-TOO-LONG if the output would exceed
    /// 2^30 bytes; else the line is written to the output, added to the output's SHA-256, and
    /// emitted as event 'S'. The builder is left as it was.
    pub fn say(&mut self, c: u32) {
        let n = self.sb.len() as u64 + 1;
        if n > ORL_OUTPUT_MAX - self.out_bytes {
            self.refuse("OUTPUT-TOO-LONG", c);
        }
        let mut line = std::mem::take(&mut self.sb);
        line.push(b'\n');
        if let Some(o) = self.out.as_mut() {
            if let Err(e) = std::io::Write::write_all(o, &line) {
                orl_fatal(&format!("orlog: cannot write the output file: {}", e));
            }
        }
        self.out_sha.update(&line);
        self.out_bytes += n;
        self.event(b'S', c, &line);
        line.pop();
        self.sb = line;
    }

    // ---------------------------------------------------------- the event hash chain

    /// head = SHA-256(head || kind || clause u32 BE || len u32 BE || payload); events += 1; and
    /// with a trace, the line `<events> <kind> <clause> <payload hex or -> <head hex>`.
    /// Payloads are below 2^32 bytes while lists and texts keep their 2^24 limits.
    fn event(&mut self, kind: u8, clause: u32, payload: &[u8]) {
        let mut h = OrlSha256::new();
        h.update(&self.head);
        h.update(&[kind]);
        h.update(&clause.to_be_bytes());
        h.update(&(payload.len() as u32).to_be_bytes());
        h.update(payload);
        self.head = h.finish();
        self.events = self.events.wrapping_add(1);
        if self.trace.is_some() {
            let mut line: Vec<u8> = Vec::with_capacity(100 + 2 * payload.len());
            orl_fmt_u(self.events, &mut line);
            line.push(b' ');
            line.push(kind);
            line.push(b' ');
            orl_fmt_u(clause as u64, &mut line);
            line.push(b' ');
            if payload.is_empty() {
                line.push(b'-');
            } else {
                orl_hex_into(payload, &mut line);
            }
            line.push(b' ');
            orl_hex_into(&self.head, &mut line);
            line.push(b'\n');
            if let Some(t) = self.trace.as_mut() {
                if let Err(e) = std::io::Write::write_all(t, &line) {
                    orl_fatal(&format!("orlog: cannot write the trace file: {}", e));
                }
            }
        }
    }

    fn var_payload(var: u32, extra: usize) -> Vec<u8> {
        let mut p = Vec::with_capacity(4 + extra);
        p.extend_from_slice(&var.to_be_bytes());
        p
    }

    pub fn ev_assign_i(&mut self, c: u32, var: u32, v: i64) {
        let mut p = Rt::var_payload(var, 9);
        orl_enc_value(b'I', v, &mut p);
        self.event(b'A', c, &p);
    }
    pub fn ev_assign_x(&mut self, c: u32, var: u32, v: i64) {
        let mut p = Rt::var_payload(var, 9);
        orl_enc_value(b'X', v, &mut p);
        self.event(b'A', c, &p);
    }
    pub fn ev_assign_f(&mut self, c: u32, var: u32, v: f64) {
        let mut p = Rt::var_payload(var, 9);
        orl_enc_value(b'F', v.to_bits() as i64, &mut p);
        self.event(b'A', c, &p);
    }
    pub fn ev_assign_b(&mut self, c: u32, var: u32, v: bool) {
        let mut p = Rt::var_payload(var, 2);
        orl_enc_value(b'B', v as i64, &mut p);
        self.event(b'A', c, &p);
    }
    pub fn ev_assign_t(&mut self, c: u32, var: u32, t: &[u8]) {
        let mut p = Rt::var_payload(var, 5 + t.len());
        p.push(b'T');
        p.extend_from_slice(&(t.len() as u32).to_be_bytes());
        p.extend_from_slice(t);
        self.event(b'A', c, &p);
    }
    pub fn ev_assign_l(&mut self, c: u32, var: u32, tag: u8, slots: &[i64]) {
        let mut p = Rt::var_payload(var, 6 + 8 * slots.len());
        p.push(b'L');
        p.push(tag);
        p.extend_from_slice(&(slots.len() as u32).to_be_bytes());
        for &v in slots {
            orl_enc_slot(tag, v, &mut p);
        }
        self.event(b'A', c, &p);
    }
    pub fn ev_item(&mut self, c: u32, var: u32, index: u64, tag: u8, slot: i64) {
        let mut p = Rt::var_payload(var, 17);
        p.extend_from_slice(&index.to_be_bytes());
        orl_enc_value(tag, slot, &mut p);
        self.event(b'E', c, &p);
    }
    pub fn ev_push(&mut self, c: u32, var: u32, tag: u8, slot: i64) {
        let mut p = Rt::var_payload(var, 9);
        orl_enc_value(tag, slot, &mut p);
        self.event(b'P', c, &p);
    }
    pub fn ev_pop(&mut self, c: u32, var: u32, newlen: u64) {
        let mut p = Rt::var_payload(var, 8);
        p.extend_from_slice(&newlen.to_be_bytes());
        self.event(b'Q', c, &p);
    }

    // ---------------------------------------------------------- claims, musts, the end

    /// Emits 'C'; for a declared id (0-based) evaluations += 1, trues += result, cost += cost
    /// (u64, wrapping) and the latest ref_clause and ref_cost are kept; a false result refuses
    /// CLAIM-REFUTED at `c`.
    pub fn claim(&mut self, id: u32, c: u32, result: bool, cost: u64, ref_clause: u32, ref_cost: u64) {
        let mut p = Rt::var_payload(id, 1);
        p.push(result as u8);
        self.event(b'C', c, &p);
        if let Some(s) = self.claims.get_mut(id as usize) {
            s.evaluations = s.evaluations.wrapping_add(1);
            s.trues = s.trues.wrapping_add(result as u64);
            s.cost = s.cost.wrapping_add(cost);
            s.ref_clause = ref_clause;
            s.ref_cost = ref_cost;
        }
        if !result {
            self.refuse("CLAIM-REFUTED", c);
        }
    }

    /// Emits 'M'; a false result refuses MUST-FAILED at `c`.
    pub fn must(&mut self, id: u32, c: u32, result: bool) {
        let mut p = Rt::var_payload(id, 1);
        p.push(result as u8);
        self.event(b'M', c, &p);
        if !result {
            self.refuse("MUST-FAILED", c);
        }
    }

    /// Emits 'R' with the code, writes the receipt `status REFUSED <code> <c>`, closes the files,
    /// exits 0.
    pub fn refuse(&mut self, code: &str, c: u32) -> ! {
        self.event(b'R', c, code.as_bytes());
        let status = format!("REFUSED {} {}", code, c);
        self.end(&status)
    }

    /// Writes the receipt `status COMPLETED`, closes the files, exits 0.
    pub fn finish(&mut self) -> ! {
        self.end("COMPLETED")
    }

    /// The receipt's text for the given status.
    fn receipt_text(&self, status: &str) -> String {
        let mut r = String::with_capacity(512 + 64 * self.claims.len());
        r.push_str("orlog-receipt 0\n");
        r.push_str(&format!("backend {}\n", self.backend));
        r.push_str(&format!("law-seal {}\n", self.law_hex));
        r.push_str(&format!("text-seal {}\n", self.text_hex));
        r.push_str(&format!("status {}\n", status));
        r.push_str(&format!("output-bytes {}\n", self.out_bytes));
        r.push_str(&format!("output-sha256 {}\n", orl_hex(&self.out_sha.finish())));
        r.push_str(&format!("events {}\n", self.events));
        r.push_str(&format!("trace-head {}\n", orl_hex(&self.head)));
        r.push_str(&format!("ops {}\n", self.ops));
        r.push_str(&format!("claims {}\n", self.claims.len()));
        for (id, s) in self.claims.iter().enumerate() {
            r.push_str(&format!(
                "claim {} {} {} {} {} {} {}\n",
                id, s.clause, s.evaluations, s.trues, s.cost, s.ref_clause, s.ref_cost
            ));
        }
        r.push_str("end\n");
        r
    }

    fn end(&mut self, status: &str) -> ! {
        if self.test_unwind {
            std::panic::panic_any(OrlEnded { status: format!("status {}", status) });
        }
        if let Some(mut o) = self.out.take() {
            if let Err(e) = std::io::Write::flush(&mut o) {
                orl_fatal(&format!("orlog: cannot write the output file: {}", e));
            }
        }
        if let Some(mut t) = self.trace.take() {
            if let Err(e) = std::io::Write::flush(&mut t) {
                orl_fatal(&format!("orlog: cannot write the trace file: {}", e));
            }
        }
        let text = self.receipt_text(status);
        if let Some(mut f) = self.receipt.take() {
            if let Err(e) = std::io::Write::write_all(&mut f, text.as_bytes()) {
                orl_fatal(&format!("orlog: cannot write the receipt file: {}", e));
            }
            if let Err(e) = std::io::Write::flush(&mut f) {
                orl_fatal(&format!("orlog: cannot write the receipt file: {}", e));
            }
        }
        std::process::exit(0)
    }

    // ---------------------------------------------------------- lists (Vec<i64>; floats as bits)

    /// NEGATIVE-LENGTH; LIST-TOO-LONG above 2^24.
    pub fn l_new(&mut self, n: i64, fill: i64, c: u32) -> Vec<i64> {
        let len = self.or_refuse(orl_l_len(n), c);
        vec![fill; len]
    }
    /// 1-based; INDEX-OUT-OF-RANGE.
    pub fn l_get(&mut self, v: &[i64], k: i64, c: u32) -> i64 {
        let i = self.or_refuse(orl_l_index(v.len(), k), c);
        v[i]
    }
    /// 1-based; INDEX-OUT-OF-RANGE.
    pub fn l_set(&mut self, v: &mut [i64], k: i64, x: i64, c: u32) {
        let i = self.or_refuse(orl_l_index(v.len(), k), c);
        v[i] = x;
    }
    /// LIST-TOO-LONG when the list would pass 2^24 elements.
    pub fn l_push(&mut self, v: &mut Vec<i64>, x: i64, c: u32) {
        if v.len() >= ORL_LIST_MAX {
            self.refuse("LIST-TOO-LONG", c);
        }
        v.push(x);
    }
    /// EMPTY-LIST.
    pub fn l_pop(&mut self, v: &mut Vec<i64>, c: u32) {
        if v.pop().is_none() {
            self.refuse("EMPTY-LIST", c);
        }
    }
}
