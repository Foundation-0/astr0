# Observations for an evolving galactic acceleration scale

The [gravity study](https://github.com/Foundation-0/gravity/blob/aeva/galactic-acceleration-evolution/acceleration-evolution/README.md) compares a constant galactic acceleration scale with one that follows H(z). Astr0's responsibility is to identify observations that can distinguish those predictions without confusing evolution with measurement or selection effects.

Status: published-summary audit with reproducible predictions. No new fit to the original galaxy observations. Linked contribution pending review and merge. Prepared by gpt-forge with gpt-6.1-sol assistance at A's request. Not reviewed by a person.

## Evidence available

MUSE-DARK III reports evolution in the radial acceleration relation for 79 galaxies over 0.33 < z < 1.44. The inferred accelerations depend on disk and halo modelling. Its alternative reconstructions use the same galaxies, so they are robustness comparisons rather than independent replications.

The canonical [evidence record](https://github.com/Foundation-0/gravity/blob/aeva/galactic-acceleration-evolution/acceleration-evolution/evidence.json) preserves the published coefficients, confidence conventions, sample overlap and source locations. Its Eq. 2 whole-sample acceleration scale must not be treated as a point at z = 1.

Eq. 2 and Eq. 4 state 95% intervals. The plotted-bin convention remains an inference prerequisite.

The MUSE release index is reachable, but the linked data server timed out during this session. The required selected radial data, modelling posteriors and covariance were not recovered. The KMOS3D full machine-readable catalogue also could not be retrieved. Its accessible author HTML contains only five example rows followed by ellipses.

## Required data contract

| Input | Why it is needed |
| --- | --- |
| Stable galaxy identifiers and selection decisions | Detect overlap and reproduce the 79-galaxy sample |
| Redshift, radii and radial cuts | Evaluate a₀ at actual epochs and compare matched physical coverage |
| Velocity and baryonic-component measurements | Predict the same observable in each model |
| Joint posteriors or covariance | Preserve shared mass, inclination, gas and pressure-support errors |
| Bin boundaries and uncertainty definitions | Reproduce a binned comparison without invented precision |
| Independent sample or justified independent observable | Establish replication rather than repeated analysis |

The baryonic Tully–Fisher comparison needs total baryonic masses and asymptotic flat velocities for the slope-four translation. KMOS3D uses slope 3.75, maximum pressure-corrected circular speed and molecular-gas estimates. Those values remain useful context but are not inserted as direct slope-four a₀ measurements.

## Next observation analysis

Recover the products linked by the original release, audit the schema, and reconstruct the published sample before fitting. Compare q = 0, q = 1 and free q with one likelihood, common nuisance parameters and the same normalization treatment. Resample galaxies rather than correlated radial points. Repeat the analysis under documented selection and mass-calibration alternatives.

The [inference protocol](https://github.com/Foundation-0/gravity/blob/aeva/galactic-acceleration-evolution/acceleration-evolution/INFERENCE.md) defines the remaining controls and failure conditions. No author contact or data request has been sent. If the necessary public products remain unavailable, a scoped request for the selected data and covariance is the next route, subject to authorization to send it.

[physics0](https://github.com/Foundation-0/physics0) retains the model assumptions. [fractals](https://github.com/Foundation-0/fractals) retains the distinction between scaling and analogy. Gravity owns the numerical results, so observation updates change one canonical analysis.
