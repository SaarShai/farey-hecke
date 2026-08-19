# Q7 MMS primary-source receipt

Date: 2026-08-19

**Status: SOURCE VERIFIED.**  This is a provenance and scope receipt, not a
new proof claim.  It banks the exact public source consumed by the q=7
operator-binding proof without adding third-party PDF bytes to the repository.

## Version and byte identity

Primary source: Dieter Mayer, Tobias Mühlenbruch, and Fredrik Strömberg,
*The transfer operator for the Hecke triangle groups*, arXiv:0912.2236v2,
15 March 2010; DCDS 32 (2012), 2453–2484.

- abstract/version page: <https://arxiv.org/abs/0912.2236>
- versioned PDF: <https://arxiv.org/pdf/0912.2236v2>

Fresh fetch and comparison with the locally inspected copy:

```text
$ curl -sSL https://arxiv.org/pdf/0912.2236v2 \
    -o /tmp/q7-mms-primary-0912.2236v2.pdf
$ shasum -a 256 /tmp/q7-mms-primary-0912.2236v2.pdf \
    tmp/pdfs/mms-0912.2236v2.pdf
a10020bd084534dc60fc3e887958f1583f2fc115d567961b461df1a59b32e072  /tmp/q7-mms-primary-0912.2236v2.pdf
a10020bd084534dc60fc3e887958f1583f2fc115d567961b461df1a59b32e072  tmp/pdfs/mms-0912.2236v2.pdf

$ pdfinfo /tmp/q7-mms-primary-0912.2236v2.pdf \
    | rg '^(Title|Author|Pages):'
Title:           The transfer operator for the Hecke triangle groups
Author:          D. Mayer, T. Mhlenbruch, F. Strmberg
Pages:           30
```

The PDF metadata drops the accents in two surnames; the paper title page is
the spelling authority used above.

## Theorem and formula locations

The locations were reproduced by

```text
$ pdftotext -layout /tmp/q7-mms-primary-0912.2236v2.pdf \
    /tmp/q7-mms-primary-0912.2236v2.txt
$ rg -n 'Theorem 4\.10|Lemma 5\.1|For q = 2h.*> 5|Theorem 6\.4|Remark 4' \
    /tmp/q7-mms-primary-0912.2236v2.txt
1216:Theorem 4.10. The operator Ls : B → B is nuclear of order zero ...
1337:Lemma 5.1. The operators P : B → B and Ls : B → B commute ...
1385:For q = 2hq + 3 > 5 we get
1872:Theorem 6.4. The Selberg zeta function ZS (s) ...
1914:Remark 4. Using the explicit form of the maps which fix rq ...
```

The source supports the following bounded uses:

| source location | use in the q=7 chain | source boundary |
|---|---|---|
| p. 20, Theorem 4.10 | the full Banach transfer operator is nuclear of order zero and has meromorphic continuation with pole lattice \(s=(1-k)/2\) | it does not identify the Python/Hilbert realization |
| p. 21, Lemma 5.1 | \(P\) commutes with the transfer operator; its \(\pm\) eigenspaces are invariant and complemented by \((I\pm P)/2\) | reduced-space conjugacy still has to be proved in the q=7 note |
| p. 21, equation (34) | the reduced odd-q operator for \(q=2h_q+3>5\) | specialization and all 19 code occurrences still have to be checked |
| p. 28, Theorem 6.4 | \(Z_S\) is the quotient of the full/reduced determinant product by the \(K_s\) determinant | a numerator zero needs a nonzero denominator and the correct reduced sector |
| p. 29, Remark 4 | source caveat concerning the broader eigenfunction/automorphic correspondence | no general q>3 automorphic or parity claim is inferred |

For q=7, the displayed odd-q heading applies literally:

```text
$ python3 - <<'PY'
q = 7
h = (q - 3) // 2
kappa = 2 * h + 1
print(f"q={q} h={h} kappa={kappa} odd_scope={q == 2*h + 3 and q > 5}")
PY
q=7 h=2 kappa=5 odd_scope=True
```

Substituting \(h_7=2\), \(\kappa_7=5\) in equation (34) gives the three row
forms used by `Q7_R5_OPERATOR_BINDING_SOL.md`; the separate 19-occurrence
source/receipt audit remains the binding authority for the implementation.

## Explicit non-claims

MMS does **not** by itself prove the q=7 Python-to-operator correspondence,
the Hardy/Banach common-continuation lemma, the finite contour certificate,
the `K_s` nonvanishing gate, a scattering interpretation, or the full LAW.
Those implications retain the statuses of their own proof and referee
artifacts.  This receipt closes only the prior documentary gap that the exact
MMS version and theorem numbering had not been durably banked.

**READY FOR ASSEMBLY REFEREE**
