# KMOS3D peak-speed diagnostic

The recovered KMOS3D table supports a descriptive comparison of galaxy mass and modeled peak speed. Its acceleration-like proxy falls with redshift, opposite to a template proportional to the Hubble expansion rate. This table alone cannot establish how the physical acceleration scale evolves.

These results are prepared for independent computational review. They are not a measurement of a0, a confidence interval on q, or a new empirical gas measurement.

The input is the [official VizieR catalogue J/ApJ/842/121/table3](https://doi.org/10.26093/cds/vizier.18420121), credited to Übler et al. (2017). The canonical numeric hash is checked by the existing input validator. The sample has 135 rows, grouped into 65 low, 24 middle and 46 high redshift galaxies. The full method was frozen in ANALYSIS-PLAN.md before these row-derived diagnostics.

This research used the VizieR catalogue access tool, CDS, Strasbourg, France, [DOI 10.26093/cds/vizier](https://doi.org/10.26093/cds/vizier).

## Calculation

Use the catalogue peak speed Vp and baryonic mass Mt to define

```text
x = log10 E(z),       E(z) = sqrt[0.315(1+z)^3 + 0.685]
y = log10[Vp^4/(G Mt)]          (SI units)
b4 = log10(Mt/Msun) - 4 log10[Vp/(242 km/s)]
```

A difference in y equals the negative difference in b4. The asymptotic relation Vflat^4=G Mtrue a0 would connect this expression to a0 only with the required velocity and mass mappings. We use the relation here as a conditional diagnostic. The plotted curves have a free normalization anchored to the low-redshift mean.

| Sample | Count | Redshift range | Mean x | Mean b4 |
|---|---:|---:|---:|---:|
| Low | 65 | 0.602 to 1.032 | 0.222658 | 10.693090 |
| Middle | 24 | 1.306 to 1.665 | 0.378982 | 10.787445 |
| High | 46 | 2.028 to 2.529 | 0.533182 | 10.860574 |

The high-minus-low difference is delta y=-0.167484 dex, with delta x=0.310524. A q=0 template predicts zero change. A q=1 template predicts +0.310524 dex. Their residual contrasts are therefore -0.167484 and -0.478008 dex, respectively.

## What changes the result

| Fixed diagnostic | High minus low y, dex |
|---|---:|
| Arithmetic means, primary | -0.167484 |
| Conventional medians | -0.155735 |
| Equal weight for three fixed speed bins | -0.199504 |
| Stellar mass substituted for baryonic mass | -0.003641 |
| Approximate rotation speed substituted for circular speed | -0.238354 |

The speed bins are [100,200), [200,300), [300,500) km/s. Their low/high counts are 20/10, 29/26 and 16/10. Their proxy shifts are -0.224264, -0.188033 and -0.186214 dex. The sign survives these descriptive checks. Weighting a few broad bins does not remove survey selection effects or match every galaxy property.

The catalogue gas contribution has an exact algebraic role. The mean of log10(Mt/Mstar) rises from 0.182462 to 0.346304 dex. Its difference, 0.163843 dex, supplies about 98% of the 0.167484 dex baryonic proxy decrease. Stellar-mass substitution nearly removes that decrease. This identifies dependence on the adopted gas estimates, without showing that those estimates are wrong.

Removing approximate pressure support changes the high-minus-low proxy by another -0.070870 dex. This operation changes the observable and is not a preferred physical correction. One row fails reconstruction of the published rotation-dominance cut from the approximate peak-radius formula. It remains included. REPRODUCTION-NOTES.md records that failure and the summary-median convention.

## Calibration required by each template

Let cv=log10(Vp/Vflat) and cm=log10(Mt/Mtrue). If the asymptotic relation applies,

```text
y = log10 A + q x + 4 cv - cm
delta y - q delta x = 4 delta cv - delta cm
```

Here delta means the high-minus-low difference of sample means. Ratios below are ratios of geometric mean calibration factors. They assume no extra population or selection offset.

| Template | Residual contrast, dex | Required (Vp/Vflat) high/low if masses exact | Required (Mt/Mtrue) high/low if velocity mapping exact |
|---|---:|---:|---:|
| q=0 | -0.167484 | 0.908090 | 1.470564 |
| q=1 | -0.478008 | 0.759448 | 3.006134 |

Thus q=1 requires a 24.1% drop in the peak-to-flat speed ratio, or a factor 3.01 increase in the catalogue-to-true mass ratio, if one nuisance mapping carries the entire discrepancy. These are conditional requirements. The table provides no calibrated prior probability for either adjustment, and combinations are possible.

Changing q by d and cv by -d x/4 leaves every predicted y unchanged. This exact degeneracy prevents identifying q when the velocity mapping may evolve freely. An external normalization at z=0 does not remove it because x(0)=0.

For completeness, descriptive residual RMS after a fitted common intercept is 0.362879 dex for q=0 and 0.414987 dex for q=1 across all 135 rows. The low/high subset gives 0.369637 and 0.431473 dex. These distances describe point estimates under the stated proxy. They are not likelihoods or model probabilities.

## Source definitions and sample limitations

The [published article](https://www.mpe.mpg.de/~saglia/journals_pdf/uebler2017.pdf) supplies these definitions. Stellar masses use population synthesis and a Chabrier IMF. Gas masses use a scaling relation depending on redshift and galaxy properties (page 3, Section 2.2). Vcirc is the modeled maximum, including pressure support, and the authors discuss the absence of flat outer curves (pages 3 to 4).

The 135 objects follow cuts from 240 modeled galaxies and 536 observations (pages 3 to 4). Only 56.25% of the modeled parent sample remains. Published comparisons demonstrate sensitivity to selection and pressure support (pages 8 and 12). The sample has different star-formation offsets across redshift (page 5). These facts prevent treating it as a random sample of all galaxies.

The paper uses Omega_m=0.3 and H0=70. This diagnostic uses the requested Omega_m=0.315 only in E(z), without rescaling catalogue masses or speeds. Individual distance and modeling inputs are absent. Page 11 discusses missing atomic gas and mass systematics. The catalogue also lacks per-object errors, joint covariance and resolved radii.

## Reproduce

Place these files next to the existing kmos_inventory.py and obtain the source TSV through the published input contract. The diagnostic itself uses Python's standard library. Matplotlib is needed only for the figure.

```sh
python3 kmos_diagnostic.py /path/to/kmos-table3.tsv --output results
python3 -m unittest discover -p 'test_kmos_diagnostic.py' -v
python3 -m pip install -r plot-requirements.txt
python3 kmos_diagnostic.py /path/to/kmos-table3.tsv --output results --plot
```

The script asserts the input hash, counts, compatible published summaries, positive approximate rotation speeds, complete speed-bin coverage and algebraic identities. Four unit tests check synthetic q laws, calibration signs and powers, the exact degeneracy, and bin boundaries.

The generated JSON contains full precision, checks and limitations. The PNG and PDF show derived diagnostics without redistributing the raw catalogue or article.

A physical inference next needs independent constraints on the velocity and gas mappings, individual correlated errors and a selection model. Resolved profiles could support a different radial-acceleration test. Until those inputs are present, the executable result is the proxy trend and the calibration change required by each template.
