// Experiment: which ways of canonicalizing a NaN survive -O.
const CANON: u64 = 0x7FF8_0000_0000_0000;

fn isnan_bits(b: u64) -> bool {
    ((b >> 52) & 0x7FF) == 0x7FF && (b & 0x000F_FFFF_FFFF_FFFF) != 0
}

// 1. a float-level guard selecting a NaN constant (the first runtime's f_sqrt)
#[inline(never)]
fn sqrt_guard(a: f64) -> f64 {
    if a.is_nan() || a < 0.0 {
        f64::from_bits(CANON)
    } else {
        a.sqrt()
    }
}

// 2. the native operation, then an integer-domain canonicalization
fn canon_int(x: f64) -> f64 {
    let b = x.to_bits();
    f64::from_bits(if isnan_bits(b) { CANON } else { b })
}
#[inline(never)]
fn sqrt_canon_int(a: f64) -> f64 {
    canon_int(a.sqrt())
}

// 3. as 2, with the bits passed through black_box
fn canon_bb(x: f64) -> f64 {
    let b = std::hint::black_box(x.to_bits());
    f64::from_bits(if isnan_bits(b) { CANON } else { b })
}
#[inline(never)]
fn sqrt_canon_bb(a: f64) -> f64 {
    canon_bb(a.sqrt())
}

// 4. a float-level canonicalization after the operation
fn canon_float(x: f64) -> f64 {
    if x.is_nan() {
        f64::from_bits(CANON)
    } else {
        x
    }
}
#[inline(never)]
fn sqrt_canon_float(a: f64) -> f64 {
    canon_float(a.sqrt())
}
#[inline(never)]
fn sub_canon_float(a: f64, b: f64) -> f64 {
    canon_float(a - b)
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let x: f64 = if args.len() > 1 { args[1].parse().unwrap_or(-2.0) } else { -2.0 };
    let inf = f64::INFINITY * (args.len() as f64);
    println!("1 guard        {:016X}", sqrt_guard(x).to_bits());
    println!("2 canon_int    {:016X}", sqrt_canon_int(x).to_bits());
    println!("3 canon_bb     {:016X}", sqrt_canon_bb(x).to_bits());
    println!("4 canon_float  {:016X}", sqrt_canon_float(x).to_bits());
    println!("5 inf-inf flt  {:016X}", sub_canon_float(inf, inf).to_bits());
}
