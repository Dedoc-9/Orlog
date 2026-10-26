# The doppler: the owner's question and the two texts he pasted (2026-10-26, verbatim)

On 2026-10-26, after R6 of the RUN-1 sheet was amended to the coarse rule (`research/run-1/RULINGS.md`, R6: in a run
whose law declares any port, no claim is GROUNDED; sound, not complete), the owner pasted two texts and asked two
questions of his own. The texts appear to be another model's replies; he did not say whose. They are kept here as he
pasted them, between his own words. The debate's reports and the judge's verdict sit beside this file. Nothing in it is
built or admitted.

---

## The first pasted text (a reply to the R6 amendment)

Both corrections accepted, and the second one was my error, not a wording quibble. I wrote "soundness guarantee: complete" in that table — that's incoherent. The coarse rule is sound and incomplete, and those are different properties: it never shows a false GROUNDED, and it withholds grounding from claims that don't touch a port. I also invented a "declared-port flag" that doesn't exist yet; it'll be the `(port …)` lines R5 introduces, which is a meaningful difference because it means the rule's input doesn't exist until 1a lands. Clock and entropy: accepted, no separate case.

**The one thing I'd change before moving on.** The evidence file measures the hazard; it does not test the fix. Everything it establishes is about v0 — indirect dependence is real, and it's invisible to declared-support analysis. The step from there to "under RUN-1 that claim would read GROUNDED over an unratified log" is a projection, and it's a good one, but by your own vocabulary it's DECLARED, not MEASURED. The measurement that would promote it is exactly the acceptance row you added to R12 — and that row can't run until a law can declare a port. So it's a *pending* row, not a passing one.

That distinction matters mechanically, not just pedantically: your headline number is "163/163 twice byte-identical." If a row that cannot execute gets folded into that count, the count stops meaning what it says. I'd keep pending rows in a separate tally — something like `163 pass / 164 rows, 1 pending (needs 1a)` — so the green figure never absorbs an untested claim. Verification cultures die by exactly this route, and you've built a language whose whole point is refusing it.

Related coverage gap worth recording: none of the 3,361 frozen texts declares a port, so COMPAT-0 exercises the new rule zero times. The rule is conservative by construction — it can't break v0 — but that also means it has no corpus behind it. Its only backing is the pending row.

**One footgun to document now, because it's permanent until fork 4.** Under the coarse rule, declaring a port you never read still costs every claim its grounding. A law with an unused port is indistinguishable, to the court, from one saturated in input. Users will hit this and read it as a bug. Either say it plainly in DOCTRINE — "declaring a port is a global grounding cost, not a local one" — or consider whether an unused port should be a door-level warning. The second option is cheaper than it sounds and doesn't weaken soundness.

Worth naming what the amendment actually is, too: it's about the moment a value crosses from text into log. In v0 the thrust value lives in the law, so the law's seal covers it and ratifying the claim ratifies the value. RUN-1 moves the value out of the text and into a log the seal doesn't cover. The amendment is the court noticing that crossing. That framing might belong in the dated note, since it explains why the narrow wording looked right.

**What next, in order:**

Finish the sheet. It's still awaiting your word, and you've now got eleven rulings and ten defaults I've only seen in fragments — R1, R2, R4, R7, R10 and the defaults in particular. R7's recommendation about holding the twin's paper round first is the one I'd most want to see in full, since the twin is currently carrying the front-end checking burden that four-way agreement can't. Then 1a, which is the smallest buildable slice and the one that makes the R12 row executable.

I'll take the adversary's seat on the rest if you paste them — one ruling at a time, arguing the option you didn't pick. That's the only way the sheet ends up containing a recorded dissent, and a ruling sheet with no dissent in it is indistinguishable from one nobody examined.

---

## The owner's question

"Also: what if we add something like a doppler that rules out non completeness as ruthlessly as sha256?"

---

## The second pasted text (a reply to that question)

A doppler is the right instrument for this, and the name is doing real work — but not the work you're hoping for. Worth separating what SHA-256 actually gives you from what it's usually said to give you.

SHA-256 doesn't rule out collisions. It makes finding one cost more than anyone can afford, under an assumption nobody has proven. Its ruthlessness is structural, not mathematical: the algorithm is public, verification is trivial, there's no secret, and the hardness assumption sits permanently exposed to anyone who wants to attack it. Collision resistance is an open conjecture that has survived twenty years of assault. That's the property to copy. Impossibility isn't on the menu.

Why the naive version can't work. Dependence is an existential: there exists an input log under which this claim's truth shifts. Independence is a universal: no log does. Existentials are witnessable; universals are not. Rice's theorem says any nontrivial semantic property of programs is undecidable, and noninterference — "this output is unaffected by that input" — is the canonical undecidable case (the Goguen–Meseguer formulation, building on Denning's lattice model of information flow). So a static doppler that decides port-independence cannot exist. Not "is hard to build." Cannot exist.

But R9 hands you the lever. You capped each tick at a budget. That makes every run finite-state, and the bounded question — "within N ticks and this value range, does any log flip this claim?" — is decidable, if expensive. That's the only honest place to stand: not completeness, but decidability at a stated bound.

So build it as a differential hunter, not a prover. The doppler metaphor is exactly right here: it measures shift by comparing two observations. Run the law twice with logs differing in one port, compare claim truth per tick, report the first divergent tick. That's your planted-defect arbiter's method aimed at the input log instead of the backends, and it fits Ragnarök's "a generator must not be its own sole verifier" — the witness is a pair of traces, checkable by a separate path.

Note what this buys and what it costs. A witness is a positive result: dependence proven, cheaply, permanently. Silence is not proof — it's "no dependence observed in domain D." And here's the limitation baked into the name: a doppler measures relative motion, not absolute position. A dependence that yields the same truth value across every log in D is invisible — not absent, just unshifted. Widen D and it may appear. That's why the domain must be published with the claim.

Make the domain the thing under attack. This is where you get SHA-256's structure. A claim reading PORT-FREE should carry the domain it was searched over, and anyone — including a hostile party — can re-run the search with a larger domain and refute it. Cheap refutation, permanently available, no secret. That's the ruthlessness you can actually have: not a guarantee that incompleteness is gone, but a standing bounty on it.

Then make the residue visible instead of silent. Don't leave GROUNDED/UNGROUNDED binary. The court already speaks in graded verdicts — CIRCULAR, UNREACHED, UNSUPPORTED, WELL-FOUNDED-but-UNGROUNDED. Add a third value on the grounding axis:
state	what it means	how it was reached
PORT-FREE	no dependence found, domain D published	doppler search + taint agreement
PORT-REACHABLE	dependence witnessed	first divergent tick named
UNKNOWN	neither	the coarse rule's default

Now incompleteness is a named state rather than a silent loss of grounding. The coarse rule stops being a blunt instrument and becomes the floor of a lattice — and it stays sound, because UNKNOWN never reads GROUNDED.

Two paths, per your own principle. The reference interpreter can propagate taint bits through the syntax tree — dynamic tracking sees actual data flow, which is precisely what L10 says the court can't see statically. Sound for the observed run, incomplete across paths. Pair it with the differential search and require agreement: taint says reachable, search finds no witness → investigate; search finds a witness, taint says clean → taint is broken. Neither is the other's sole verifier.

The weak link, which Ragnarök's adversary already named for Ragnarök itself. The search domain and the checker would be chosen by the same model family that wrote the law. A dependence outside the chosen domain is undetectable from inside. Publishing the domain mitigates this socially; nothing mitigates it technically.

Cost, honestly: the log space is exponential in ticks × ports × value range. R9 bounds each run, not the space of runs. Expect the doppler to be an admission-time tool on small domains, not a per-tick one — same economics as four-way checking.

The physics payoff is concrete, and it's the reason I'd build this before fork 4. A port-reachability map tells you exactly which state is externally driven and which is purely internal. That's what you need to decide what must be logged for replay — you log reachable ports and nothing else — and it's what makes a determinism audit tractable, since internal state can be checked without touching the log at all. The backward slice gives you the same map statically; the doppler gives it to you empirically first, and the two agreeing is a much stronger result than either alone.

---

## The owner's request

"Can you do better? websearch this with suybagen and debate"

---

## The third pasted text, added the same day with the owner's words "have it look into this too:"

Absolute position isn't a measurement problem, so a better instrument won't produce it. In physics the quantity doesn't exist — not because instruments are inadequate, but because position is only ever defined relative to a frame, and the frame is a choice. Galileo's point. So the real answer isn't a sharper doppler; it's **quotienting**. Declare what counts as the same, and whatever is well-defined on the quotient is absolute.

**The mechanism: orbit decomposition.** The log space is your coordinate system. Searching it for invariance is hopeless — exponential in ticks × ports × range. But suppose you can exhibit a group acting on the log space such that the claim is invariant under the action, and the action's orbits partition the reachable log space. Then invariance on one representative per orbit gives invariance everywhere. A universal collapses into finitely many checks. The group is tiny — translations, permutations, sign flips, scalings, a handful of generators — while the log space is astronomical. That asymmetry is the entire trick, and it's textbook: symmetry reduction for model checking is established work (Emerson & Sistla, *Symmetry and Model Checking*, CAV 1993; FMSD 1996), which quotients state spaces by permutation groups for exactly this reason.

**What makes it fit your court.** A symmetry σ is admissible as evidence only if it commutes with the tick function: σ(tick(s, l)) = tick(σ(s), σ(l)). That's a checkable equation — and because R9 caps each tick, it's checkable *exhaustively over the bounded state space*. So a symmetry witness is a **checked certificate**, not testimony. It rides the certificate channel, which is already groundable, and it never touches the untyped-terminals problem. That's what makes this architecture-native rather than bolted on. The certificate is a finite list of generators, each carrying a commutativity obligation discharged by exhaustive check. Generation and verification separate cleanly: one process proposes σ, another discharges the obligation, the twin discharges it independently. Your "a generator must not be its own sole verifier" is satisfied without new machinery.

**Keep the doppler — it becomes the refuter.** A claim reading PORT-FREE-BY-SYMMETRY is refutable by exhibiting a log pair outside the group's orbits that flips the claim. That's a doppler run on an adversarially chosen domain. The two aren't redundant: symmetry certifies, the doppler attacks the certificate. Require agreement, and disagreement is a refusal rather than a verdict.

**Name the residue honestly: accidental constancy.** A claim can be constant across the reachable log space without being invariant under any symmetry — the ball stays in the room for every thrust because the walls are thick. Symmetry methods are structurally blind to this, and so is the doppler, which simply observes no shift. This is the equivalent-mutant problem in different clothing: a property holding for reasons other than the one you believe. It deserves its own state, not silence.

| state | meaning | reached by |
|---|---|---|
| PORT-FREE-BY-SYMMETRY | invariant under a certified group, orbits cover the reachable space | discharged commutativity obligations |
| PORT-REACHABLE | dependence witnessed | first divergent tick named |
| ACCIDENTALLY-CONSTANT | no shift observed, no symmetry found | doppler silence — *not* a certificate |
| UNKNOWN | neither | the coarse rule's default |

**The part I'd actually build for: Noether.** A certified continuous symmetry *is* a conservation law. If the law's equivariance group is certified, conserved quantities come free, and conservation becomes an **oracle-free verification channel** — you don't need to know the correct trajectory to know energy must not drift. Every other check in your stack compares against something: the reference, the twin, a vector set, a certificate. This is the only one that needs no counterpart. And it catches what the doppler structurally cannot: a shared-front-end bug that corrupts the law and its reference identically still violates conservation. That's the front-end row of your independence table — currently checked by nothing but the twin and grounded claims — acquiring a third, genuinely independent instrument.

**Partial frames are fine.** The group may not act transitively enough, and then you get invariance along a subgroup — absolute position along some directions only. Still valuable: it tells you which directions in the log space are inert, which is precisely what you need for replay logging. Log only the directions that matter.

**Cost, and the honest novelty verdict.** Computing automorphism groups in general is hard. In practice laws declare their equivariances, or a small search finds them, and the commutativity obligation is cheap under R9's cap. So start with declared symmetries plus exhaustive verification of the obligation — buildable before fork 4 and before typed terminals. As for novelty: the mathematics is not new, and I'd resist claiming otherwise. What's arguably new is placing a symmetry witness inside a court that separates integrity from truth, as a ratified certificate on the existing channel, with the doppler retained as its designated refuter and accidental constancy as a named residue rather than a silent gap.

Sheet-wise: a pending R12 row — *claim reads PORT-FREE-BY-SYMMETRY with no discharged commutativity obligation → refusal*; ACCIDENTALLY-CONSTANT as a state distinct from PORT-FREE; and a note that symmetry witnesses inherit the certificate channel's typing, so they don't need fork 9 to arrive first.

---

## The fourth paste: the owner's question to the other model, and its answer

The owner then pasted, with nothing of his own outside it, the third text again (identical but for formatting), then
the question he had put to the other model, then its answer. His question, verbatim: "what is one feature we can
pioneer here now that  will streamline Computing automorphism groups later? be ambitious". The answer, verbatim:

Yes. One feature that pays forward for automorphisms while fitting Orlog's architecture: sealed equivariance.
The Feature

Add a declaration form that lives in the law text itself, ratified alongside every other claim:
(equivariant <generator-name> <parameters>)
  ; obliges: commutativity of σ with tick, discharged over R9-bounded state
  ; evidence: certificate <seal>, discharged by <checker-seal>

The generator names a transformation (translation, permutation, sign-flip, scaling). The obligation — σ(tick(s,l)) = tick(σ(s), σ(l)) — must be discharged before the law receives admission. The discharge is a finite exhaustive check over the bounded state space (R9 cap). The resulting certificate becomes part of the law seal and inherits the certificate channel, which is already groundable.
Why It's Pioneer-Worthy
Property	Sealed Equivariance	Typical Symmetry Work
Location	Inside the law text, sealed with every clause	External analysis, detached from code
Verification	Discharged at admission, certificate stored	Re-computed on demand, never ratified
Grounding	Uses existing certificate channel	External claim, ungrounded
Composition	Import-certified generators into new laws	Manual recomputation each time
Refutation	Doppler can still attack the certificate	No standing mechanism to attack

No language I'm aware of makes its own structural invariants first-class, ratifiable citizens of the program. You're making the program's algebraic properties part of the legal text, which is exactly the territory Orlog occupies — typed terms, declared support, graded grounding. This extends the court's vocabulary to include "this law is invariant under σ" as a certified proposition rather than an external assertion.
How It Streamlines Later Automorphism Work

    Cache invalidation, not recomputation. Certified generators become importable libraries. A physics law certified as translation-invariant on [0,100]^3 can cite that certificate rather than re-discharge the obligation on every new instance. The discharge obligation is "does this generator commute here?" — not "find all commuting generators."

    Generators, not groups. You don't need to compute the full automorphism group upfront. Declare generators of known subgroups; composition and closure follow algebraically. The certificate system handles the rest: two certified generators compose to a certified transformation, provided the composition obligation is discharged separately (or proved from the generators' certificates).

    Incremental discovery. A new program imports certified generators, adds local ones, discharges fewer obligations, and contributes its new certificates back into the shared registry. The registry grows organically rather than being computed ad hoc each time.

    Cross-language reuse. Because the discharge certificate is language-agnostic (a finite list of commutativity equations verified over a bounded domain), the same generator imported into Python, C, and Rust backends carries identical weight. Four-way agreement on the generator's validity becomes a bonus, not a requirement.

    The doppler's role clarified. A claim reading PORT-FREE-BY-SYMMETRY carries the sealed generators. A doppler attacker seeking refutation targets a generator's certificate directly: run a log outside the certified domain, show the claim shifts, invalidate the seal. The referee doesn't recompute the automorphism group; it re-verifies a single commutativity equation.

Concrete Implementation Path
Step	Deliverable	When
Syntax extension	(equivariant ...) line in the grammar, treated as a typed terminal	1b (when ports exist)
Obligation checker	Exhaustive commutativity checker over R9-bounded state, outputs certificate	1b, admission gate
Certificate format	Finite list: generator ID, parameters, discharged-over-domain, verifier seal	1b
Import mechanism	Laws can import certified generators, inheriting their commutativity obligations	After 1b
Doppler integration	Claims carrying PORT-FREE-BY-SYMMETRY tagged with their generator seals for attack surface	Fork 3 or 4
The Physics Payoff (Immediate)

Once you have sealed equivariance, a physics law can declare rotational invariance, translational invariance, or Galilean boost invariance as certified facts about the law itself. Conservation laws (energy, momentum) follow automatically from Noether's theorem applied to the certified generators. The physics benefit: you get conservation without needing to know the trajectory. Energy cannot drift if the certified symmetry holds, and the drift check becomes the independent refuter rather than the oracle.
Honest Novelty Assessment

The mathematics isn't new — symmetry-based model checking and equivariant program analysis are established (Emerson & Sistla 1996, Goguen & Meseguer 1982). What's new is placing equivariance inside a ratifiable legal framework where:

    The symmetry is part of the law seal, not an external claim
    Certification happens at admission time as a gate, not as an optional analysis
    Certificates inherit the existing grounding architecture (certificate channel, not testimony)
    Refutation uses a standing mechanism (the doppler) that exists independently

That's a different architecture than "compute symmetries when needed." It's a different ecology entirely — a library of certified transformations rather than a search problem.
Sheet Amendment

If this goes into the rulings, I'd add:
Row	Question	Option	Entails	Recommendation
R13	Can a law certify its own symmetries?	a. Yes, sealed equivariance	Generator declarations discharge commutativity at admission, certificate sealed	Yes
		b. No, deferred	Symmetry analysis external to the law	No — delays payoff, duplicates work
R13 Falsifier	a generator that passes its certificate but fails on an unbounded domain
