# Coverage of the projector and regular-module bridge

Audited target: Ali Romman's PR5618, head
`4d112aaf8e8760d34015f934ab8a63d2b9ccda83`, PROOF.md sections 1-4.
This is an independent AI audit with a separately written executable; no
predecessor executable is imported or run. It corroborates the existing result.
The preliminary calculation preceded discovery of PR5618; its final proof/code
were then read to bind this audit to the actual argument. No blind review,
human scientific acceptance, proof-kernel verification or novelty is claimed.

## Premises retained rather than re-proved

At each fixed f>=72, use the credited pointwise theorem to identify A with the
unitary twisted group algebra of the full projective monomial Clifford group H
on 17 axes. Set h=|H|. PR5587 gives the target deficit at least 224h+r, where r
is the complex rank of right multiplication by L=I-C3 C1 on A^112. It also
supplies the 240-return arbitrary-linear-oracle upper construction. Each new
same-capacity return contributes at most h dimensions even with feedback.
These source/history/capacity statements are **premises** of this audit.

## 1. The rank bridge, checked through a different factorization

The pinned literal scalar code C=F^T is an involution of trace 96 and size 112.
P=(I-C)/2 is an idempotent of rank 8. The verifier establishes these directly,
using exact rational multiplication and elimination. For the actual diagonal
unitary gauges D_s=diag(K_s), set P_s=D_s^-1 P D_s and C_s=I-2P_s.

The useful identity, including its sign, is

    L = 2(P3-P1) C1.

Since C1 is invertible, rank(L)=rank(P3-P1). Factor P_s=U_s V_s with full
column/row ranks 8h in the regular representation. Factoring the difference
through [U3 U1], diag(I,-I), and [V3;V1], Sylvester's inequality gives

    rank(L) >= 16h - delta_column - delta_row.

Here the deltas are the intersections of the two column spaces and of the two
row spaces. This does not assume that the idempotents are orthogonal.
For right multiplication on row vectors, componentwise x->x* is a conjugate
linear isomorphism to left multiplication by L*. In the unitary regular
representation L* is the Hilbert-space adjoint of L; their ranks agree.
Thus the left-operator calculation bounds the required right-module rank.

A separate literal S3 group-ring fixture constructs the left and right actions
from the group multiplication table. The 18x18 matrices differ, so this is a
noncommutative test. Componentwise group inversion intertwines the right action
with the transposed group-star action exactly; the latter is the Hilbert-space
adjoint of the left action. All three exact ranks are 8. No source regular-module
rank is inferred from this finite fixture.

The executable checks the full signed factorization and ranks on four literal
42x42 realifications of twisted C7 regular representations, using a deliberately
nonsymmetric scalar idempotent. The phase-zero case has real rank 24; the other
three have rank 28. These finite controls corroborate, rather than replace, the
written general rank argument.

## 2. Two independent metrics

An orthogonal projection is constructed from an independently selected basis
B as B(B^T B)^-1 B^T. For im(P), its integer numerator R has scale 28 and rank 8.
Every diagonal entry of R/28 is 1/14. Full symmetry, idempotence and inclusion
of every source column are checked.

For the row intersection, multiply all row vectors on the right by the same
invertible diagonal matrix B0. B0 has entry +1/11 at the eight selected ports
(C_ii=12), and 1 elsewhere. This preserves their intersection dimension and
commutes with the monomial gauges. Recompute the orthogonal projection onto
the rows of P B0 independently. It is distinct from the first projection, but
again has scale 28, rank 8 and constant diagonal 1/14. Its full identities and
every balanced source row are checked. Consequently both intersection losses
can be bounded by the same moment formula without asserting equality of their
underlying spaces. This positive scaling differs from the predecessor's -1/11
identification; both are legitimate rank metrics, with no physical cost credit.

For orthogonal projections E,F, EFE is positive semidefinite. The common space
is its eigenvalue-one space; all other eigenvalues lie in [0,1]. Therefore
dim(im(E) intersect im(F)) <= Tr((EF)^2). This holds in the finite unitary regular
representation, regardless of the tensor phase cocycle.

## 3. Why unsigned binary ratios suffice for all phases

Put J_i=K_(1,i) K_(3,i)^-1. The separately implemented binary matrix code embeds
all actual 9-axis normalizers into the two 17-axis blocks and uses ordinary
binary elimination for inverses. It finds 12433 binary ratio classes: the 112
diagonal pairs in the identity class, and 12432 singleton off-diagonal classes.

For either scalar orthogonal projector T, conjugating by D1 and expanding gives

    Tr((T1 T3)^2)/h
      = sum_(i,j,k,l) T_ij T_jk T_kl T_li
          tau(J_j J_k^-1 J_l J_i^-1).

Normalized regular trace tau vanishes on every nonidentity projective group
class. A surviving word must satisfy equality of the binary ratios for (j,k)
and (i,l). The certified partition leaves just two possibilities: j=k and i=l,
or (j,k)=(i,l). In each, the **literal signed word** cancels as a unitary followed
by its exact inverse, so the phase is exactly +1. No omitted binary collision
can contribute an unknown phase. This is why computing a separate signed phase
table is unnecessary for this particular audit, and why all f residues are covered
by the argument. It would fail without the complete ordered-ratio partition.

For rank 8, m=112 and constant diagonal d=1/14, either projection gives

    2 d^2 sum_(i,j) T_ij^2 - m d^4
      = 2*8*d^2 - 112*d^4 = 27/343.

The code also sums the full pair-group expression independently for both
projectors. Synthetic C7 gauges with X^7=i^a for a=0,1,2,3 give the expected 5/27
in all four literal twisted regular matrices. The C5 gauges 0,1,2 are distinct
but repeat pair ratios; their literal moment is 19/81, not 5/27. This is a control
against replacing the Sidon condition by mere distinctness.

## 4. Consequence and boundary

Both deltas are at most (27/343)h, hence

    r/h >= 16-54/343 = 5434/343,
    (224h+r)/h >= 82266/343 > 239.

The integer lower bound 240 and the inherited 240-return construction agree.
This confirms the audited implication under the stated premises. No exact
regular-module rank, new return theorem, native 240-call construction or new
kappa follows from this audit. It does not make the metric rescaling a free
ordinary operation. The original observation inventory, Clifford faithfulness,
history deficit and oracle construction were not replayed. Native realization,
owned state, storage, routes, precision/tape, compiler and complete outer bill
remain outside this independent check.

The verifier includes six semantic rejection controls, including a damaged
literal involution, collapsed gauges, singular binary map, misuse of a
nonsymmetric idempotent as an orthogonal projection, false 239 capacity and the
insufficient first-moment closure. All comparisons are exact and remain active
under optimized Python.

Credit Ali Romman's PR5618 for the result and projection/Sidon method and the
classical projection/Sylvester/trace inequalities. Retain the original source
and contributor lineage listed in README.md. New independent audit: MatShep
with substantial OpenAI Codex assistance; Apache-2.0.
