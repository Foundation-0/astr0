# Observations that separate competing explanations

Research note, 12 November 2026. This note connects the archive projects to the Foundation0 convergence study. It proposes checks using published examples. No new search has been run on this hub's candidates, and its project-level discovery claims have not been independently revalidated here.

## Observe where the alternatives disagree

In the published analysis of ASASSN-24fw, historical DASCH observations support a long period but leave a half-period alternative. ASAS covers the otherwise missing phase and shows normal brightness, excluding that alternative. The uneventful exposure supplies information because the alternatives predict different behavior there.

It does not settle the physical nature of the occulter. [Primary analysis, Section III.1 and Figures 5–6](https://arxiv.org/html/2507.05367v3).

The next observation should target the phase where remaining explanations disagree. A missing detection matters only with a limiting brightness, exposure coverage and probability of detecting the predicted event. An absent archive entry alone cannot exclude an eclipse or eruption.

## Shared errors can survive repeated measurements

An exact Gaussian probe in the convergence study reduces target posterior variance by a factor of 25.75 when a reference channel measures the disturbance shared with the target. The reference alone contains no target information under the model. Repeating the target measurement with the same disturbance barely helps. This is a constructed example, not a measured improvement to DASCH data.

[Schölkopf et al.'s half-sibling regression](https://proceedings.mlr.press/v37/scholkopf15.pdf) supplies the established method: use a reference to predict shared disturbance. A reference contaminated by the wanted signal can subtract that signal. Audit reference-star variability, blending, common calibration and time-dependent artifacts before treating extra agreement as independent evidence.

## Survival and visibility are different

HS Hya's binary persisted while its eclipses ceased as orbital inclination changed. Historical plates and modern photometry preserve the changing visibility. [Davenport et al.](https://arxiv.org/abs/2107.10954) report the history and the later absence of eclipses. A vanished eclipse does not by itself imply a vanished binary.

## Next tests

- Reproduce one published period ambiguity, including the observations with no dimming. Record phase coverage, limiting brightness, quality flags and event-detection completeness for each competing period.
- Test any common-error correction on known variable stars and injected events. Hold out epochs and reference stars, and compare with existing archive calibration before claiming improvement.
- For a candidate that no longer eclipses, compare inclination change, period error, source mismatch and changing obscuration. Preserve proper-motion and matching uncertainty across epochs.
- Release an interpretable pilot sample with its selection rule before estimating occurrence rates. Population inference requires the probability of entering the sample, as explained by [Mandel, Farr and Gair](https://arxiv.org/pdf/1809.02063).

## Evidence and credit

The [canonical research bundle](https://github.com/Foundation-0/gravity/tree/9b7f165021918e66c99f8bd291af5ac83ebef11d/research/convergences-20261112) contains the synthesis, route reports, primary-source ledgers and reproducible probes. Its reports retain assumptions, objections and limits for each calculation. The research used gpt-6-astra with ultra reasoning. Publication preparation used gpt-6.1-sol.

The canonical bundle records the full division of work.
