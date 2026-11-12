# Galaxy calibration inputs

This package records the inputs needed to recheck the reported change of galaxy acceleration with redshift. It gives researchers a data contract and a file inventory checker. No survey catalogue or new observational fit is included.

The current inventory is incomplete. The official [DARK release index](https://dark.univ-lyon1.fr/data-releases/) links to a server that timed out during retrieval. [MUSE-DARK I](https://doi.org/10.1051/0004-6361/202557396) describes best fit parameters and 95 percent intervals. Those intervals alone do not establish the correlations needed for joint inference.

## Inputs and checks

`data-contract.json` defines the scientific roles of four required products. Its field names are proposed normalized names. They are not verified original release columns. Record original names, units and conversion rules before using a downloaded table.

`retrieval-manifest.json` records the retrieval boundary. Its empty `artifacts` list is intentional. A future entry has `role`, `path`, `source_url`, `bytes`, `sha256`, and `schema` with `columns` and `units`. The paths are relative to a separately supplied data directory. Keep original data outside this repository until distribution terms are verified.

The checker verifies file bytes, declared source URLs and basic schema metadata. It rejects missing roles, changed bytes, repeated roles and paths outside the data directory. It does not inspect table contents or establish scientific readiness. Even a complete byte inventory reports `science_ready: false`.

```sh
python3 -m unittest discover -s research/galaxy-calibration -p 'test_*.py'
python3 research/galaxy-calibration/validate_manifest.py research/galaxy-calibration/retrieval-manifest.json --data-dir /path/to/local/data
```

The second command currently exits 1 because all four products are missing. The unit tests use synthetic text files. They test the inventory checker, not a galaxy analysis.

## Before inference

A researcher must verify original schemas and units, galaxy identifiers, the selected 79 objects, missing values and model labels. The 79-object requirement applies to replication of the MUSE-DARK III result. Other studies must declare their own selection.

Parent catalogues are not interchangeable with the selected sample. The release index describes 126 galaxies while Paper I describes 127. Reconcile that difference against actual release files before selecting rows.

Require joint draws, a justified covariance model, or original cubes with a validated reconstructed likelihood for shared radius, inclination, stellar mass and gas uncertainties. State the assumptions behind any substitute model. Distinguish measured inputs from accelerations reconstructed with a halo model. Recover a published baseline before testing redshift dependence. No such recovery has been performed here.

The next action is to acquire the original photometry and halo tables with their schema, then establish the selected membership and joint uncertainty product. The bounded retrieval attempts here do not show that data are absent from every public archive.

Prepared by gpt-forge using GPT-6.1 Sol. Human scientific review remains pending.

## An independent public sample is retrievable

The official CfA VizieR mirror delivered all 135 rows of [Ubler et al. (2017), Table 3](https://vizier.cfa.harvard.edu/viz-bin/VizieR-3?-source=J%2FApJ%2F842%2F121). The catalogue contains redshift, stellar and baryonic log masses, maximum modeled circular velocity and intrinsic velocity dispersion. `kmos-retrieval.json` records the actual response hash, units and ranges.

This sample can support a Tully-Fisher diagnostic, which compares galaxy mass with rotation speed. It lacks radial profiles and error columns in this table. It cannot supply the missing MUSE-DARK membership or establish a joint radial acceleration likelihood. No new fit is reported.

Download the original table separately, then inspect it:

```sh
curl --location --fail 'https://vizier.cfa.harvard.edu/viz-bin/asu-tsv?-source=J/ApJ/842/121/table3&-out.all&-out.max=unlimited' -o kmos-table3.tsv
python3 research/galaxy-calibration/kmos_inventory.py kmos-table3.tsv
```

The parser checks the catalogue name, columns, units, 135 unique sequence identifiers and finite physical values. Later responses include new request timestamps, so their byte hashes may differ. The recorded ranges and schema provide additional checks. Original catalogue bytes are not redistributed here.

This research has made use of the VizieR catalogue access tool, CDS, Strasbourg, France, [DOI 10.26093/cds/vizier](https://doi.org/10.26093/cds/vizier). The catalogue is credited to Ubler et al. (2017), ApJ 842, 121, catalogue DOI 10.26093/cds/vizier.18420121.
# KMOS diagnostic increment

The recovered 135-galaxy catalogue now has a [bounded mass–velocity diagnostic](RESULTS.md), with a frozen analysis plan, numerical results and a figure. Its peak-speed proxy decreases with redshift. The gas mass contribution accounts algebraically for nearly all of that decrease.

This is not an acceleration-scale measurement. The note quantifies the velocity or mass-calibration change required by constant and Hubble-tracking templates. A free redshift-dependent calibration prevents identifying the physical scaling.

A [separate Astra review](independent-review/REVIEW.md) reproduces the contrast and its calibration algebra with an independent parser. This is internal project review, not external peer review.

The author files remain at their reviewed hashes, including their original review-pending status. The review above supersedes that status. Run `python3 independent-review/check.py /path/to/kmos-table3.tsv` for the separate checks.
