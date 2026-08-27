# Reply email draft — 2026-08-27

**Subject:** Agreed: Experimental Mathematics — final TeX, frontier replication complete, Zenodo ready

Dear Professor Koyama,

Thank you for both messages. I am glad the revision met your approval, and I
fully agree with the two-stage strategy: Experimental Mathematics is the right
home for this joint manuscript, and it keeps your Stage-2 analytic paper for
Inventiones cleanly separated. Let us proceed on that basis.

Since your last message I have completed the remaining technical items:

1. **Independent frontier replication.** The extension from `1.3 x 10^13` to
   `3 x 10^14` was previously a single run of our own sieve, and I did not
   want it in the paper without independent confirmation. I have now
   recomputed the entire frontier with a second, independent implementation
   (a primesieve-based iterator, run as three range-split cloud jobs). The
   two computations agree exactly in all 4896 shared class cells at all 72
   frontier grid points, and the range counts reproduce the published values
   of pi(10^14), pi(2 x 10^14), and pi(3 x 10^14). The manuscript's
   "one run" caveat is removed, and the replication code, outputs, and
   receipt are included in the archive package.

2. **Zenodo archive.** The complete computational package (data, zero tables,
   reconstruction and verification code, the new replication material, the
   Lean sources, and SHA-256 manifests) is assembled and ready to upload,
   with metadata listing both of us as creators and linking your preprint
   arXiv:2607.28931 as the companion theoretical reference. I will upload it,
   reserve the DOI, and insert it at the marked placeholder in the TeX before
   we finalize.

3. **Final TeX.** Attached. Beyond the DOI placeholder, the changes since the
   version you reviewed are: the abstract now leads with the verified
   computational results (the framing you proposed for Experimental
   Mathematics), your preprint is cited as the source of the regularized
   framework, and the replication sentences replace the single-run caveat.
   The compiled PDF is still eight pages with no warnings. One confirmation:
   the finite-x mollified comparison plot remains excluded, for the reasons
   we discussed — the statistic is not yet analytically fixed, so the plot
   belongs to Stage 2.

I have also drafted a short cover letter for the Experimental Mathematics
submission (attached); please edit freely. Two small points to settle at your
convenience: which of us acts as corresponding author for the submission, and
whether you would like any wording changes before I upload the Zenodo package
(its README and metadata are in the attached archive).

As agreed, neither of us submits or replaces anything until we have both
approved the same final compiled PDF.

Best regards,

Saar

**Attachments:**
- `koyama_final_packet_2026-08-27.zip` (manuscript TeX + PDF, changelog,
  verification report, numerics, Lean, checksums)
- `cover_letter_draft.md`
- (after DOI reservation) final TeX with the DOI inserted
