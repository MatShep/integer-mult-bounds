# Independent audit of the p2 projector bridge

This independently reimplements and checks the projector/regular-module rank
argument in [Ali Romman's PR5618](https://github.com/CrocSwap/integer-mult-bounds/pull/5618),
exact head `4d112aaf8e8760d34015f934ab8a63d2b9ccda83`, sections 1-4.
No blocking error was found in that argument under its credited premises.
The two exact second moments are again **27/343**, giving the credited target
deficit **82266/343 > 239** and hence its existing 240-return conclusion.
This is independent AI corroboration, not a new theorem, physical supplier,
human review, formal-kernel acceptance or kappa improvement.

Read [AUDIT.md](AUDIT.md) for the rank/phase bridge and precise coverage boundary,
and [RESULT.json](RESULT.json) for exact finite coverage. The new verifier imports
no predecessor executable. It derives its own row and column bases and uses two
distinct balanced orthogonal projectors, rather than assuming their spaces are
equal. Four literal twisted-regular fixtures exercise all central phase residues
and a nonsymmetric idempotent. A distinct-gauge fixture with repeated pair ratios
gives **19/81**, rejecting the Sidon formula **5/27** in that domain.

## Reproduce

```sh
python3.12 -B scripts/research_package.py --package research/p2-oracle-projector-audit
```

Python 3.12 and its standard library suffice. Both registered commands are
warning-strict, isolated normal/optimized runs. The expected markers are
`PASS_INDEPENDENT_P2_PROJECTOR_AUDIT` and `PASS_REGISTERED_RESEARCH_PACKAGE`.
The verifier is read-only unless explicitly invoked with `--write` to regenerate
its receipt. Its only live scientific inputs are two pinned original data
files, with exact bytes retained in canonical main. No audited executable runs.

## Limits and credit

The source 224h+r deficit and 240-return upper construction, and the pointwise
Clifford faithfulness that applies for f>=72, remain credited premises. The
39-observation caller, all-size native theorem, complete source-history replay,
physical ordinary decoding, paid compiler, precision/tape and outer admission
were not independently verified. An invertible metric rescaling in this rank
proof is not a free division-by-11 implementation. No selected cold replay ran.

The sharp theorem, balanced-projection method, Sidon observation and second
moment belong to Ali Romman/PR5618. PR5587 supplies the history deficit and oracle
construction; PR5526 the faithfulness premise; PR5449 the history formulation.
Retain Dugongue/PR4948, Chris R/Clear1nsight/PR4978, josecarlosgonzalezroque-design/
PR5570, Cao Yifan, Cinna Davis, DLamdata, zxv and their native/controller/Clifford
lineage. Projection, trace and Sylvester rank inequalities are classical.
This separate audit and executable were prepared for MatShep with substantial
OpenAI Codex assistance; Apache-2.0. PR5618's unchanged original package is retained
in the publication ancestry to keep every audited proof byte accessible.

## Open next questions

Further exact leakage-rank computation cannot improve the already-sharp oracle
return count. A productive caller needs a changed paid input, observations,
ordinary alphabet, capacity or targets and a complete favorable invoice. Start
with one literal changed input and its observation boundary; that physical
construction and all its costs remain unknown. This audit reserves no such task.
