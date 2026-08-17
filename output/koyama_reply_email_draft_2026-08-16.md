# Reply email draft

**Subject:** Joint manuscript revision and complete numerical/spectral packet

Dear Professor Koyama,

Thank you for sending the complete TeX source and for inviting me to lead the
numerical and computational integration. I have now completed a joint revision
and assembled a self-contained review packet. It includes the revised TeX and
PDF, the low-zero reconstruction figure, the full numerical data and scripts,
independent verification material, the limited Lean sources, a technical
change log, and checksums.

I implemented the four technical corrections we discussed:

1. the character selector now consistently uses
   `(1 - conjugate(chi(a)))`, so it selects the class `a` rather than `a^{-1}`;
2. the regularized statement is now a two-parameter analytic target with
   `T = T(x)` and explicit `T`-dependence retained in the coefficient;
3. the modulus-19 transient discussion now incorporates the certified odd
   character zero near `gamma = 0.018956399080226143`, and the former
   `exp(33.4)` settling estimate has been removed;
4. Table 3 has been rebuilt from the raw class counts, including the eight
   corrected cells at `1.3 x 10^13`, the sign correction for `N=19, a=10` at
   `1.3 x 10^11`, and the previously omitted class `a=20` modulo 23.

The numerical section now includes the ordinary-count data through
`3 x 10^14`, the exact 567/567 comparison with the independently checked
baseline through `1.3 x 10^13`, and the low-zero reconstruction. With 25
positive zeros per nonprincipal character, the top-decade correlations for the
`-1` trajectories are 0.826--0.971; for modulus 19, using 100 zeros raises the
correlation to 0.9925. The endpoint ranks and continuing rank reversals are
reported explicitly, so the computation motivates the regularization without
being used as evidence for eventual raw-count dominance.

I have not included the proposed finite-`x` mollified comparison plot. At
present the precise statistic, common normalization, logarithm branch, and
admissible `T(x)` regime are not fixed, and the summed off-diagonal estimate is
not yet proved. Plotting before those choices are settled would leave a
rescaling ambiguity. The manuscript therefore states the two-parameter limit
and the apex/nadir hierarchy as conjectures, while keeping the character
identity and the verified finite computations at their proved scope.

The packet also contains the contribution statement, the deliberately narrow
Lean-scope paragraph, and the computational/AI-assistance disclosure. Before
we update arXiv or submit to Inventiones, could you please review and confirm:

- the revised theorem/conjecture boundary and the open analytic obligations;
- the title, author order, affiliations, and contribution statement;
- the corrected Table 3 and numerical interpretation; and
- the public data/code archive we should cite with a permanent DOI.

I suggest that neither of us submit or replace the manuscript until we have
both approved the same final compiled PDF. Once you send your comments, I can
make the final coordinated TeX pass and prepare the archive-ready version.

Best regards,

Saar

**Suggested attachment:** `koyama_share_packet_2026-08-16.zip`
