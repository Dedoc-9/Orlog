# R3: number–letter codes, check digits, determinism, tilings, chaos, novelty

Fact-check for ØRLǪG, 2026-10-25. No design. **Tags:** **[C]** CHECKED, I read the source text (page, paper, standard or code); **[C~]** CHECKED from an abstract, search excerpt or secondary summary only; **[M]** MEMORY; **[D]** derived here by arithmetic or short algebra, every number recomputed by `r3-work/tools/derive_checks.py` beside this file.

## 0. Leading findings

1. **Not new:** per-line check symbols in source listings (1983); compiler-enforced checksums on literals (Solidity, EIP-55); chaos as an amplifier of cross-platform float differences (1997 on); self-derived expected values as a named test defect, recast as a provenance property in August 2026 (section F).
2. **Not found**, which is not proof of novelty: assurance verdicts under grounded or well-founded semantics with circular support reported as the least/greatest-fixed-point gap; runtime enforcement, by deterministic operation counting, that a check costs less than what it checks; program or claim hashes as pronounceable words inside source. Every ingredient is prior art.
3. **x∘y = a·x + y**, a ∉ {0,1}, is totally anti-symmetric [D]; iterated it is Horner's rule, which the ISO/IEC 7064 pure systems compute [C code].
4. **Unconfirmed:** Levesque & Verlet's full text (known via Rein & Tamayo and the Hoovers); Blum–Kannan's "little-oh" wording; Ecker & Poch's text; Anton's wording (pages refused); the Gustavus Adolphus chronogram's year (1627 or 1632, by spelling); why Cakravākam is melakarta 16 (the stated last-consonant rule gives 26 [D]); the 1947 Ulam–von Neumann note itself.

## A. Number–letter systems

**Kaṭapayādi** [C~ table; every decoding here reproduces it]: 1 ka ṭa pa ya · 2 kha ṭha pha ra · 3 ga ḍa ba la · 4 gha ḍha bha va · 5 ṅa ṇa ma śa · 6 ca ta ṣa · 7 cha tha sa · 8 ja da ha · 9 jha dha · 0 ña na or a standalone vowel. In a conjunct only the consonant bearing the vowel counts; a vowelless consonant is ignored. Digits read right to left, *aṅkānāṃ vāmato gatiḥ*: *jaya* → 18 [C]. Earliest cited use: Haridatta, 683 CE [C]. Uses [C; D]: melakarta rāga numbers from the first two syllables (*dhī-ra* → 29); Kerala astronomy (Mādhava's sine table); Kali-day chronograms (*āyurārogyasaukhyam* = 1,712,210, closing the Nārāyaṇīyam).

π verses:
- **Karaṇapaddhati** (Puthumana Somayāji): circumference 31415926536 for diameter 10¹⁰ [C]. **Date disputed:** 1375–1475, or 1732/33 from its closing chronogram [C~].
- **Sadratnamālā** IV.2 (Śaṅkara Varman, 1819), *bhadrāmbudhi…*: 314159265358979324 for diameter 10¹⁷, π correctly rounded to 17 decimals [C; D]. Wikipedia also says "31 decimal places", an internal error.
- **gopībhāgya…**: π/10 to 31 decimals; its printed 32nd digit is 2, the true one 5 [D]; read left to right, against the rule [C]. It comes from Tirtha's *Vedic Mathematics* (1965): the **ancient attribution is spurious** [C~].
- **Mādhava** (often conflated): 2827433388233 for diameter 9×10¹¹, in *bhūtasaṅkhyā* word-numerals, not Kaṭapayādi; 2 above the rounded truth [C; D].

**Āryabhaṭa** (Āryabhaṭīya, Gītikāpāda 2): varga consonants 1–25, avarga 30–100; vowels set the place, ×1, ×10², ×10⁴, … [C]. *khyughṛ* = 4,320,000, the Sun's revolutions per yuga [C~; D]. The value is a sum, so syllable order does not matter [D].

**Abjad (ḥisāb al-jummal)** [C]: ا1 ب2 ج3 د4 ه5 و6 ز7 ح8 ط9 ي10 ك20 ل30 م40 ن50 س60 ع70 ف80 ص90 ق100 ر200 ش300 ت400 ث500 خ600 ذ700 ض800 ظ900 غ1000, ordered *ʾabjad hawwaz ḥuṭṭī…*; the Maghrebi variant has ص60 ض90 س300 ظ800 غ900 ش1000. No zero.

**Greek** [C]: 24 letters plus digamma/stigma 6, koppa 90, sampi 900. Isopsephy (*isos* + *psēphos*, "equal pebble") sums them: in Suetonius, Νέρων = 1005 = "killed his own mother" [C; D]; a Pompeii graffito's "545"; Revelation 13:18.

**Stoicheia**: plural of *stoicheion*, from *stoichos* "row": a member of a series, then a letter, then an element; the title of Euclid's *Elements* [C~].

**Gematria**: 1–9, 10–90, 100–400; finals 500–900 in *mispar gadol*; חי = 18 [C].

**Chronogram**: the year is the sum of all Roman-numeral letters, in any order [C]. SICVLICIDIVM = 1764 (Madéfalva; initial S not counted) [C; D]. Earliest confirmed: mid-14th century [C].

**Polybius square** (Histories X.45–47): credited to Cleoxenus and Democleitus, improved by Polybius; Greek letters in five tablets of five (the last four), signalled by torches; Latin merges I/J or C/K [C].

**A1Z26**: A=1 … Z=26 [M].

**PGP word list** (Juola & Zimmermann, 1995): two 256-word lists, two-syllable words for even byte positions and three-syllable for odd, so a swapped, duplicated or omitted word shows [C].

**Proquint** (Wilkerson, 2009): 16 bits → consonant-vowel-consonant-vowel-consonant from 16 consonants and 4 vowels; 127.0.0.1 = lusab-babad; no checksum [C].

**BIP-39** (Palatinus, Rusnak, Voisine & Bowe, 2013): entropy plus the first ENT/32 bits of its SHA-256; 11 bits per word from 2048 words with unique four-letter prefixes; seed = PBKDF2-HMAC-SHA512, 2048 iterations, salt "mnemonic" + passphrase [C].

**Bubble Babble** (Huima; draft 2000, corrected 2011): 2 bytes → 5 characters (6 vowels, 17 consonants), framed x…x; a mod-36 checksum in the vowels catches some errors [C].

| System | Map | Order | Errors |
|---|---|---|---|
| Kaṭapayādi | many letters → one digit | positional | none |
| Āryabhaṭa | sum of syllables | order-free [D] | none |
| Abjad, isopsephy, gematria, chronogram | many-to-one sum | commutative | none |
| Polybius | one-to-one on 25 cells (merged pair two-to-one) | ordered pairs | none |
| A1Z26 | one-to-one per letter; unseparated digits ambiguous (12 = L or AB) [D] | ordered | none |
| PGP words | one-to-one per byte | ordered | swaps, duplicates, omissions; a wrong valid word passes [D] |
| Proquint | one-to-one | ordered | invalid letters only |
| BIP-39 | one-to-one, with checksum | ordered | random damage passes with probability 2^−CS (1/16 at 12 words, 1/256 at 24) [D] |
| Bubble Babble | one-to-one | ordered | partial, about 0.58 bit per vowel [C] |

## B. Check digits

- **Luhn** (IBM; US 2,950,048, 1960): every single-digit error and most adjacent transpositions; misses 09↔90 and the twins 22↔55, 33↔66, 44↔77 [C].
- **Verhoeff** (1969, Mathematical Centre Tract 29; any base, Gumm 1985): D5 with the permutation (1 5 8 9 4 2 7 0)(3 6); all single errors and adjacent transpositions [C].
- **Damm** (Marburg dissertation, 2004): a totally anti-symmetric (TA) quasigroup of order 10 — (c∗x)∗y = (c∗y)∗x ⇒ x = y and x∗y = y∗x ⇒ x = y — with zero diagonal; all single errors and adjacent transpositions [C]. TA quasigroups exist for every n ≠ 2, 6 (*Discrete Math.* 307(6):715–729, 2007), refuting Ecker & Poch's conjecture of none for n = 4k+2 [C]. No order-10 system of this kind catches all jump transpositions and jump twins [C~].
- **x∘y = a·x + y** [D]: both TA conditions reduce to (a−1)(x−y) = 0, and a ≠ 0 makes a quasigroup, so it is TA for every q ≥ 3 (brute force over GF(3)…GF(13) and GF(4) agrees). Iterated, it is Horner's rule with weights a^(n−i): the ISO/IEC 7064 pure family — MOD 11-2 is check = 2·check + d mod 11, MOD 37-2 likewise, MOD 97-10 is the integer mod 97, i.e. a = 10 [C code; D]. It catches jump transpositions only if a² ≠ 1; its diagonal (a+1)x is zero only for a = −1, which misses them [D]. No source found calls it *the* standard construction; Damm's constructions target orders 4k+2.

## C. Physics determinism

**Levesque & Verlet**, *J. Stat. Phys.* 72:519–537 (1993): an integer, time-symmetric MD algorithm, used to show that time-asymmetric evolution is typical under reversible dynamics [C~]. Update r_{n+1} = 2r_n − r_{n−1} + [h²F(r_n)/m], positions on an integer grid, [·] a rounding; reversed by swapping r_{n+1} and r_{n−1} [C, via Rein & Tamayo 2017; Hoover & Hoover 2017]. Conditions [C]: forces depend only on positions; every lossy step (float force, rounding) happens mid-step from r_n alone, so stepping back recomputes the same rounded value. In the leapfrog form (JANUS, Rein & Tamayo) velocities sit on a grid too; reversal by v → −v needs rounding symmetric about zero, as IEEE-754's is; a power-of-two step makes multiplication a shift; Liouville holds exactly (a bijection of the grid), but it is only "formally" symplectic [C]. Reversibility on one machine is not reproducibility across machines [D].

**Noether** (1918, *Nachr. Göttingen*, 235–257): every continuous symmetry of the action yields a conservation law [C~]. Discrete version for variational integrators: Marsden & West, *Acta Numerica* 10 (2001) [C~].

**Momentum** [D]: store integer momenta, round each pair's impulse once to J, apply +J and −J. Integer addition is exact and associative, so Σp is invariant bit for bit in any order, absent overflow. It breaks with per-particle rounding of F/mᵢ under unequal masses, with a non-odd rounding applied to each sign separately, and with float accumulation, which is not associative [C~]. GPU MD codes accumulate forces in fixed point for deterministic sums (Tinker-HP, crediting AMBER) [C~].

**Symplectic integrators** [C~]: by backward error analysis a symplectic method of order p exactly follows a shadow Hamiltonian H̃ = H + O(h^p). The series diverges, but optimal truncation leaves an exponentially small error, so the energy error stays in an O(h^p) band, without drift, for exponentially long times (Benettin & Giorgilli 1994; Hairer, Lubich & Wanner). Round-off adds a random walk on top [M].

## D. Tilings and sampling

- **Aztec diamond**: order n has 2^{n(n+1)/2} domino tilings; four proofs, Elkies, Kuperberg, Larsen & Propp, *J. Algebraic Combin.* 1 (1992) 111–132, 219–234 [C~].
- **Arctic circle** [C]: for large n, all but an ε fraction of tilings have their temperate zone within εn of the inscribed circle of radius n/√2, with frozen corners outside. Manuscript dated 1 March 1995; arXiv 1998; journal version in *Ann. Inst. Henri Poincaré D*, online 11 May 2026.
- **Domino shuffling** (introduced by EKLP): destroy bad 2×2 blocks, slide each domino, create blocks by a fair coin; a uniform order-n tiling becomes a uniform order-(n+1) tiling, and only creation is random [C].
- **Height functions** (Thurston, *Amer. Math. Monthly* 97(8):757–773, 1990): a tileability test for simply connected regions [C]. Heights form a distributive lattice under pointwise min and max, with flips as covering relations, and any two tilings are flip-connected (Saldanha et al., 1995) [C~]. Propp generalised it (1993 preprint; *Electron. J. Combin.* 2025) [C~]. Flip-connectivity fails in 3-D [C~].
- **Coupling from the past** (Propp & Wilson, *Random Structures & Algorithms* 9:223–252, 1996): coupled chains run from −T to 0, T doubling until they coalesce; a monotone chain needs only its top and bottom states; §4.3 samples domino and lozenge tilings through the lattice [C].

## E. Chaos as an amplifier

The map 4x(1−x) is conjugate to the tent map by x = sin²(πy/2) and to doubling by x = sin²(πθ), so x_n = sin²(2ⁿπθ₀); invariant density 1/(π√(x(1−x))); Lyapunov exponent ln 2 [C~]. Ulam and von Neumann proposed it as a random source (*Bull. AMS* 53:1120, 1947) [C~ citation].

**Prior art for detecting float non-reproducibility:** Rosinski & Williamson (*SIAM J. Sci. Comput.* 18:552–564, 1997) validated climate-model ports by the growth of rounding perturbations [C~]. Yabuki & Tsuchiya (arXiv:1305.3128, 2013) showed double-precision logistic orbits depend on the FPU's mode [C~]. Nepomuceno et al. (*Appl. Math. Comput.*, 2018) bound simulation error by the divergence of two algebraically equal forms, across Matlab, Scilab, Octave, Fortran and C [C~]. CESM's ensemble consistency tests replace bit-for-bit comparison, one variant after nine steps (Milroy et al. 2018) [C~]. FLiT bisects compiler-induced differences [C~].

## F. Novelty checks (adversarial)

**F1. Assurance argumentation.** Assurance 2.0 (Bloomfield & Rushby, arXiv:2004.10474) searches actively for defeaters; eliminative argumentation (Goodenough, Weinstock & Klein) uses rebutting, undermining and undercutting defeaters; GSN v3 is SCSC-141C (May 2021) [C~]. Prior art: grounded semantics is a least fixed point (Dung 1995) [M], tied by Dung to well-founded semantics [C~]; Kripke (1975) defined groundedness by the least fixed point, the truth-teller holding in some fixed points but not the least [C~]; evidential argumentation (Oren & Norman 2008) excludes circular support [C~]. On assurance: CLARISSA (arXiv:2408.11699) checks cases with s(CASP) stable models, defeaters as negation as failure, and no circularity property [C]; Bloomfield, Netkachova & Rushby (arXiv:2405.15800) propagate verdicts up a tree "with cross links" and leave cycles untreated [C]; some tools forbid circular arguments syntactically [C~]. **Not found:** grounded or well-founded verdicts, or the fixed-point gap, applied to assurance cases.

**F2. Oracle provenance.** Named smells: Self-Test, Ugly Mirror/Tautological test, Test Tautology, and the rule that an expected value should be a constant, not computed in the test (Garousi & Küçük 2018; Open Catalog of Test Smells; Rwemalika et al. 2022) [C, via Canedo]. Canedo (arXiv:2608.17214, 17 August 2026) treats "state-anchored" oracles as a provenance property, says the flow check is decidable on the import-and-call graph, and found no shipping linter implementing it [C]. OraclePolish passes self-referential oracles [C, via Canedo]; Jest's `--ci` refuses to write new snapshots and approval-test tools have strict modes [C~]; Randoop separates regression from error-revealing tests [M]. **Not found:** build-time refusal by provenance type.

**F3. Cost asymmetry.** Blum & Kannan (STOC 1989; *J. ACM* 1995): a checker must be "quantifiably different", its time excluding calls to the program below that of any correct program [C~]; the "little-oh" wording is [M]. Verifiable computing (Gennaro, Gentry & Parno 2010): verification far cheaper than computation [C~]. Deterministic metering: Wasmtime fuel, about one unit per instruction [C~]; Ethereum gas [M]. Overhead control: SMCO caps monitoring overhead by time (*STTT*, 2012) [C~]; Klemen et al. (ICLP 2018) bound check overhead statically [C~]; the verifier's dilemma (Luu et al., CCS 2015) [C~]. **Not found:** runtime counted enforcement that a check costs less than the computation.

**F4. Words and check symbols in source.** COMPUTE!'s Automatic Proofreader (October 1983) printed a checksum per line; its 1986 version used two letters and caught transpositions [C]. MLX (December 1983) added a checksum byte per line [C]. Solidity rejects address literals failing EIP-55 (about 15 check bits; 0.0247% of mistyped addresses pass) [C]; Dhall pins sha256 hashes of normalised imports [C~]. Hoon has pronounceable literal types, @p and @q [C~]; PGP words, Bubble Babble, proquints, BIP-39 and humanhash serve display. **Not found:** hashes written as words in source.

## Sources

A: en.wikipedia.org/wiki/Katapayadi_system · arxiv.org/abs/2405.11144 · list.indology.info/pipermail/indology/1995-October/003466.html · cse.iitk.ac.in/users/amit/books/krishna-1992-vedic-mathematics-sixteen.html · en.wikipedia.org/wiki/Karanapaddhati · en.wikipedia.org/wiki/Āryabhaṭa_numeration · en.wikipedia.org/wiki/Abjad_numerals · en.wikipedia.org/wiki/Isopsephy · bibliaparalela.com/greek/4747.htm · en.wikipedia.org/wiki/Gematria · en.wikipedia.org/wiki/Chronogram · en.wikipedia.org/wiki/Polybius_square · en.wikipedia.org/wiki/PGP_word_list · raw.githubusercontent.com/dsw/proquint/master/proquint-proposal.txt · github.com/bitcoin/bips/blob/master/bip-0039.mediawiki · mit.edu/~kenta/one/bubblebabble/spec/jrtrjwzi/draft-huima-01.txt
B: en.wikipedia.org/wiki/{Luhn_algorithm, Verhoeff_algorithm, Damm_algorithm} · portal.mardi4nfdi.de/wiki/Item:Q868332 · github.com/arthurdejong/python-stdnum (iso7064/mod_11_2.py, mod_37_2.py, mod_97_10.py)
C: link.springer.com/article/10.1007/BF01048022 · arxiv.org/abs/1704.07715 · arxiv.org/abs/1706.08678 · eudml.org/doc/59024 · lagrange.mechse.illinois.edu/pubs/MaWe2001/ · arxiv.org/abs/2011.01207 · open-std.org/JTC1/SC22/WG21/docs/papers/2025/p3375r2.html
D: arxiv.org/abs/math/9201305 · ar5iv.labs.arxiv.org/html/math/9801068 · ems.press/doi/10.4171/aihpd/233 · en.wikipedia.org/wiki/Domino_tiling · arxiv.org/abs/math/0209005 · stat.berkeley.edu/~aldous/206-RWG/RWGpapers/propp_wilson.pdf
E: arxiv.org/abs/1305.3128 · doi.org/10.1016/j.amc.2018.02.020 · epubs.siam.org/doi/10.1137/S1064827594275534 · gmd.copernicus.org/articles/11/697/2018/
F: arxiv.org/abs/2408.11699 · arxiv.org/abs/2405.15800 · arxiv.org/abs/2004.10474 · scsc.uk/scsc-141c · dbai.tuwien.ac.at/local/reports/dbai-tr-2014-87.pdf · arxiv.org/abs/2004.07275 · arxiv.org/abs/2608.17214 · github.com/facebook/jest/pull/3456 · pub.dev/packages/approval_tests · eprint.iacr.org/2009/547 · docs.wasmtime.dev/examples-interrupting-wasm.html · fsl.cs.stonybrook.edu/docs/smco-sttt/smco.pdf · arxiv.org/abs/1804.02380 · en.wikipedia.org/wiki/The_Automatic_Proofreader · en.wikipedia.org/wiki/MLX_(machine_language_entry_software) · docs.soliditylang.org/en/latest/types.html · eips.ethereum.org/EIPS/eip-55 · github.com/dhall-lang/dhall-lang/wiki/Safety-guarantees · hackage.haskell.org/package/urbit-hob · pypi.org/project/humanhash3
