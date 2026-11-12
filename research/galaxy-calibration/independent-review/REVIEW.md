# Independent review of the KMOS3D point-table diagnostic

**Disposition: no blocking scientific or computational defect found.** The reported proxy contrast and required calibration shifts are reproducible for the selected 135-row catalogue. They do not establish a physical acceleration-scale trend, an estimate of \(q\), or a statistical preference between the two templates.

Reviewed 12 November 2026 by gpt-forge using gpt-6-astra. Every file hash in `public-manifest.json` was verified before review. [evidence.json](evidence.json) records the exact hashes and independent aggregate checks. The source catalogue remains outside the review artifacts.

## Independent numerical checks

[check.py](check.py) parses the input directly and imports neither the author's diagnostic nor the inventory code. It independently confirms the canonical numeric hash, the 65/24/46 group sizes, and the contrast computed in catalogue units so that the additive SI conversion cancels.

| Quantity | Independent value |
|---|---:|
| High-minus-low mean \(\log_{10}E\) | 0.310524417768 |
| High-minus-low mean proxy | -0.167483891033 dex |
| Conventional-median proxy contrast | -0.155734942472 dex |
| Stellar-only proxy contrast | -0.003641081668 dex |
| Gas mass-boost difference | 0.163842809365 dex |
| Required velocity-factor ratio for \(q=1\), masses exact | 0.759447790273 |
| Required mass-factor ratio for \(q=1\), velocities exact | 3.006133814591 |

The three speed-bin counts and contrasts also match. The common-intercept RMS values reproduce to floating-point precision. The identities \(\Delta y=\Delta y_\star-\Delta\log(M_b/M_\star)\) and \(\Delta y-q\Delta x=4\Delta c_v-\Delta c_m\) have the reported signs and powers.

The author's executable was replayed into a separate review directory. Its output agrees with the frozen JSON. This replay is separate from the independent parser and algebra checks.

## Source interpretation

The primary [Übler et al. article](https://arxiv.org/html/1703.04321v2), sections II.2–II.4, defines the catalogue velocity as the maximum modeled circular speed including pressure support. It also states the rotation cut as \(v_{\rm rot,max}/\sigma_0>\sqrt{4.4}\). The catalogue is selected from a larger observed and modeled parent sample.

The report correctly treats peak speed as a different input from an independently measured asymptotic circular speed. The paper discusses approximate comparisons between velocity measures, but those comparisons do not supply a per-galaxy asymptotic-speed calibration and joint error model for this diagnostic.

The gas contribution is based on a redshift-dependent scaling relation. The nearly complete algebraic accounting of the baryonic proxy contrast by that contribution is therefore informative about the construction of the catalogue. It is not evidence by itself that the gas estimates are biased or that the true gas evolution is absent.

The catalogue lacks the per-row uncertainty and covariance information needed to reproduce the published error-weighted regression. The report clearly separates its unweighted summaries from that regression and does not promote residual RMS into a likelihood. The different background cosmology is also disclosed.

## Rounding and unresolved selection reconstruction

An additional review check allows each tabulated velocity to vary by half its 0.1 km/s reporting unit and each log baryonic mass by half its 0.01 dex reporting unit. The high-minus-low mean proxy remains in \([-0.178237,-0.156731]\) dex throughout that rounding box.

This is only a bound on tabulation rounding. It is not a measurement-error interval and does not account for modeling, sample selection, mass calibration or correlated uncertainties.

The reported approximate rotation-cut failure for Seq 6 persists over the rounding box: \(4.4\sigma_0^2/V_{\rm circ}^2\) lies between 0.509128 and 0.510808, above 0.5. The author correctly keeps the row and labels the peak-radius reconstruction approximate. Inferring an exact survey-selection error from this calculation would be unwarranted.

The upper-middle order statistic is compatible with the published even-sized group summaries. The ordinary medians remain recorded. This is a plausible reproduction convention, not proof of which median implementation the original authors used.

## What can be published and what remains open

The publishable result is the bounded proxy contrast, its stated sensitivity checks, and the calibration change that each conditional template would require. An unconstrained redshift-dependent velocity mapping absorbs any change in \(q\), as the report shows. A local normalization alone does not remove that freedom.

The exact contrasts do not supply the missing likelihood or external calibration bounds. Further numerical fitting of \(q\) to these same point estimates would not answer the physical question. Useful next work requires independent velocity/gas calibration, correlated measurement information and a defensible selection model, or resolved profiles for a different radial-acceleration analysis.
