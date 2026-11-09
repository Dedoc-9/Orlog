# Ørlǫg PR verification discipline

**Status: ADOPTED (2026-11-09).** The standing Ørlǫg PR verification discipline, governing all future Ørlǫg pull
requests, with verification proportional to the applicable `AGENTS.md §4` change-impact row (§4 is the authoritative
mapping and prevails). Installed at `docs/engineering/release/PR-VERIFICATION-DISCIPLINE.md`.

**Provenance.** Adopted source: the archive artifact `ORLOG-PR-VERIFICATION-DISCIPLINE-2026-11-09-rev4.md`, sha256
`26453c8dc336d6763bff79ffeb22b1f39bbbd1d92d16bc854a758ea17f906713` (archive chain, byte-preserved: v1
`cc2eae3465e606b7218bfe53bb15ea557249590e7c51c61dc5259706cbcb71d6` → rev2
`3e90c17a55b6afc30f2ff38fc51544979359947590d56bee3c1b14f0b92e9361` → rev3
`e63f00427374da57a749226d0107f3fb91a33ff02d41897b511d9a1ec5139bd8` → rev4). Adoption record (archive):
`ORLOG-PR-DISCIPLINE-ADOPTION-2026-11-09.md`. The substantive content below (§1–§6) is **byte-identical to the adopted
rev4**; only this status/provenance block differs from the source. Hashes are assistant-computed; verify against the
archived bytes. Note: §3's worked instance, §5's installation plan and §6's governance block below retain rev4's
archive-draft wording, preserved byte-for-byte under the adopted-substance rule.

## 1. Core invariants — MANDATORY (what adoption would bind)

1. **Tree identity** — the tree tested is the tree pushed.
2. **Historical provenance** — frozen artifacts remain byte-identical; append-only records may grow, but **prior content
   and its meaning are preserved**: an existing finding is never reversed, erased, or rewritten in substance; a
   correction is a dated note beside the original, which stays readable and unchanged in meaning. Recovering old bytes
   from git history does **not** license rewriting the live record — **a record that rewrites a finding and appends a
   note still violates the invariant.** A disclosed, meaning-preserving redaction (e.g. F42's home-path replacement,
   "nothing else changed, byte for byte") is permitted; a substantive change is not.
3. **Proportional verification** — verification follows the applicable `AGENTS.md §4` change-impact row, **not** a
   universal full-suite requirement. That section is the authoritative mapping and prevails in the event of any
   difference.
4. **Traceability** — every claim is classified **Measured / Historical / Proposed / Owner-ruled / Authorized**, and the
   tags never bleed: a green test (Measured) never promotes a court-record scope (Proposed) to Owner-ruled.
5. **Authorization** — consequential actions require explicit authorization identifying the **exact action and target**
   (CLAUDE.md §3 b6). Owner authorization is governed by `CLAUDE.md §3`; this discipline defines verification
   requirements, not a competing approval or authorization process.

## 2. Mechanisms — OPTIONAL

| invariant it serves | optional mechanism (today) |
|---|---|
| 1 Tree identity | `Gated-Tree:` trailer + post-push `git rev-parse HEAD^{tree}` equality check |
| 5 Base/patch identity | a particular hashing script (`Get-FileHash` / `git rev-parse <commit>:<path>`) |
| 2 Historical provenance | a specific archive layout; the git-blob-SAME listing format |
| 4 Honest test results | a particular test runner / `tests/selftest.py` invocation |
| 5 Authorization | a particular PR template or manifest layout |

**Substitution proviso (settled).** A mechanism may be **replaced operationally without re-adoption, provided the
replacement still satisfies the same mandatory invariant it served.** A change that would weaken, drop, or fail to meet
an invariant is **not** a mechanism swap — it is an amendment to the discipline and needs re-adoption.

## 3. The verification manifest (realizes the invariants)

**Template** — carried with every Ørlǫg PR:

| field | content | invariant |
|---|---|---|
| Base commit | exact source state (40-hex) | 5 |
| Patch commit | exact proposed change (40-hex) | 5 |
| Changed files | complete scope — every path | 4, 5 |
| SHA-256 | the patch, and each cited evidence artifact | 5 |
| Self-test | **the applicable §4 row**: expected and actual (count + backends + exit) | 3, 4 |
| Red-team rows | green + plants caught **only for findings the change could affect** (see §4) | 3 |
| Historical artifacts | (a) frozen reproducers byte-identical (blob-SAME list); (b) records append-only, **prior meaning preserved**, no finding rewritten | 2 |
| Exclusions | needle/`work`, release gate, plant harness, unrelated work — each untouched / not run | 4 |
| Policy provenance | adopted-policy **source hash** + installed-file hash (for a policy PR) | 2, 4 |

**Worked instance — this arc, stated as source identity, not whole-tree identity:**
- `HEAD` was **reported** as `e2b40eee277c837cbf1f74f3768ee722e0e6e03c`, with tree
  `0b949ac259c7134b3a696e00d061b8201db0381b`.
- `src/` and `tests/` were **reported** byte-identical to that commit.
- The working tree had additional modifications under `court/redteam-eng/` — so **the tested working tree was not
  identical to the committed tree.**
- Those modifications were **reported** not read by `tests/selftest.py`.
- The self-test result — `ORLOG SELFTEST 211/211 (backends: python,c99,rust)`, exit 0, the backend list quoted from the
  actual summary line — is **REPORTED**, pending owner verification.

(The rest of this arc's instance — E7–E26 green + E7 plant `arbiter-lenient-receipts` CAUGHT, reproducers blob-SAME,
records append-only, needle/gate excluded — is in the parent reports, cited by hash:
`COURT-ROUND-2-REVERIFICATION-RESULTS-2026-11-09.md` sha256 `d97cfbe0…`.)

## 4. The provenance-test checklist

**Pre-push, in the independent clone:**
1. **Build** the patch in the independent clone — never the live checkout.
2. **Verify** it applies against the exact intended base (manifest Base commit). *(inv. 5)*
3. **Run the applicable `AGENTS.md §4` self-test row** — not the full suite — and record expected vs actual. *(inv. 3)*
4. **Check** historical artifacts: frozen reproducers blob-identical; records append-only with prior meaning preserved
   (no finding rewritten); frozen/pinned files (COMPAT-0 versions, twin expectations, vectors, the seven adversary
   outputs) untouched. *(inv. 2)*
5. **Review** the diff for scope contamination — no needle/`work`, no release gate, no unrelated change. *(inv. 4)*
6. **Present** the exact commit, branch, remote and PR destination for authorization — action **and** target. *(inv. 5)*

**Red-team rows (proportional, settled).** In the reported verification E7–E26 were green and the E7 plant CAUGHT; a
future PR reruns regression rows and their plants **only for the findings a change could affect** (the §4 change-impact
scope) — a change that cannot reach the arbiter, door, front end or labels reruns none. The discipline never requires
every PR to rerun all E7–E26 plants.

**Post-push — the landing check:**
7. **Verify the remote independently:** pushed tree id = tested tree id; the PR's base/head are the authorized ones; the
   PR diff equals the reviewed diff. A successful local test is not evidence the pushed tree holds the tested bytes.
   *(inv. 1)*

## 5. Installation plan (each step separately authorized; none taken)

1. **Freeze** — preserve the proposed source at its reported hash as parent provenance (owner-verified before freeze).
2. **Revise** — a later dated version, *if and when authorized* (this rev4 is such a revision, archive-only).
3. **Adopt** — explicitly name the resulting document and its scope. *(owner's recommendation: all future PRs, with
   proportional §4 verification — no full release gate for trivial changes.)*
4. **Install** — add it additively at the chosen path (`docs/engineering/release/PR-VERIFICATION-DISCIPLINE.md`, a new
   directory convention, or beside the top-level docs), then the **separately authorized** one-line discoverability
   pointer (which edits a governing file → the owner's word).
5. **Prove** — the installation PR is its own first worked example, using the applicable §4 verification row; its
   manifest records **both** the adopted-policy source hash **and** the installed-file hash, so policy provenance is
   independently auditable.

## 6. Governance

- **Archive-only proposal.** Nothing adopted, installed, or written to the Ørlǫg repo. Stand-down in force; S1–S4
  untouched.
- **Two decisions remain the owner's:** adopt (name the document and scope), then install (authorize the path, then the
  pointer). The five invariants are what adoption binds; the mechanisms stay optional, swappable only while they still
  satisfy their invariant.
- Every hash herein is assistant-computed and reproducible — **verify against the archived bytes before any freeze.**
  This document grades itself: the manifest instance is REPORTED (pending owner verification); the discipline is a
  PROPOSAL.
