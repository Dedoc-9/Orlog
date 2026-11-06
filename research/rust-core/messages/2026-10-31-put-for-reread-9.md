# The message put to him before he authorized REREAD-9 (2026-10-31), word for word

It told him each condition he set for REREAD-9 read as met, and asked whether to begin. Kept by his D6 (his ruling on REREAD-9's disposition).

Taken from the session's own transcript by a script, never retyped. The text follows, unedited.

---

I've applied ZB3 and ZB5 to the runner's check. The runner itself is unchanged, and so are the checker, the reference and the laws. Nothing is committed.

**ZB3: the check now holds the whole environment record.**
- **The ENV line and the after-run line.** The check builds both lines itself and requires each run's lines to match exactly:
  - the implementation, version and platform a fresh interpreter reports when run the way the runner is run;
  - the default recursion limit, and `format_check` not imported;
  - exactly the `orlog` modules a fresh import loads, each by its file's hash: eight for a text, five for a law.

  Before, it only checked that each listed module's hash was right.
- **"Against the runner's own recorded environment"** I read as: compare what the runner's ENV line records with what a fresh interpreter reports, run the way the runner runs.
- **A bytecode cache in each folder, by name.** There are three new cases, one each for `src/orlog`, `research/rust-core` and `research/law-sufficiency`, and each fault must name its folder.
- **Result.** 46 of 46 against the real runner, twice. All 43 earlier rows read exactly as before.

**ZB3 is what catches reader 2's changes.** I ran their four runner changes against both versions of the check. The four are kept as plants, counted separately from the 16 so your count stays exact.

| change | check before ZB3 | check now |
|---|---|---|
| X1: modules listed as `orlog.interp` alone | passes, 43 of 43 | caught |
| X2: bytecode check covers one folder | passes, 43 of 43 | caught |
| X3: ENV line drops the platform | caught only by chance | caught |
| X4: ENV line drops implementation and version | passes, 43 of 43 | caught |

**ZB5.** The fifth REREAD-6 change, a run that keeps the text-seal line in both modes, is added and caught. The record reads 15 of 16, as you ruled; V11 is still the one no case reaches.

**The old records and hashes are preserved.**
- **New records go to new names.** The five draft 9 records are now written as `-9-zb` files. Amendment 11's `-9` files are untouched, with their hashes still in that amendment.
- **What differs.** Three of the new records differ from the old only in the header line that hashes the code (the checker's record also names the new draft sha). The other two are the runs above.
- **Superseded records, kept late.** My earlier reruns had overwritten the records Amendments 9 and 10 name. Both sets are now kept in `kept/`, each matching its amendment's hash: Amendment 10's from my backup, and Amendment 9's rebuilt exactly. So are the two run logs that had gone to scratch, under your ruling I. Amendment 8's records can't be rebuilt, because the checker changed in between; they survive only as hashes and logs.
- **The kept evidence** checks 48 of 48, and no kept file names your account, compressed contents included.

**Where the notes are.** Amendment 12 in SHEET.md records all of this. Amendment 7's account of the check carries two notes saying what it had missed. Draft 9 names the ruling, and RULINGS.md has it word for word.

**REREAD-9.** Every condition you set now reads as met:
- A–D are in the sheet's language.
- The checker implements C, and the independent verifier checked it.
- The six files are resolved.
- Every leftover item has a disposition. ZA7's extension is withheld rather than adopted; I read that as a disposition, but say if you see it differently.
- The 91-depth challenge is drafted.

Starting it would mean three readers working at once on draft 9 and the sheet. They wouldn't open `research/law-sufficiency/`, and one of them would try to write a line deeper than 91. Their reports would be saved word for word, then a proposed disposition would come to you. It takes a good number of tokens and some time.

Still open apart from that: ZA7's counters, R4's witness as a plant, and the Verðandi experiment's two decisions.
