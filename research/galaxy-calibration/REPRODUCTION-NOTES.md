# Reproduction notes and failed avenues

The scope in ANALYSIS-PLAN.md remains unchanged. The following checks were resolved before the primary statistic was printed.

| Check | Observed result | Treatment |
|---|---|---|
| Recover published band groups | Boundaries at z=1.2 and 1.8 yield 65, 24 and 46 rows. The actual redshift ranges are disjoint. | Use those groups. |
| Reproduce Table 1 with conventional medians | Some even-sized group summaries fail. Mid-group logMb is 10.935 versus published 10.97. High-group Vcirc is 257.1 versus published 260 km/s. | Record conventional medians separately. The upper central order statistic matches all twelve published central summaries at displayed precision. The paper does not specify the median algorithm, so this is a compatible convention, not proof of its implementation. |
| Reconstruct rotation-dominance selection | Seq 6 gives 4.4 sigma0^2/Vcirc^2=0.509967, corresponding to vrot/sigma0=2.05621, below sqrt(4.4)=2.09762. | Keep the row. Assert only a real positive approximate rotation speed. Report this failed cut reconstruction in JSON. Do not infer the exact modeled selection from the approximate formula. |
| Exact published Table 2 regression | Missing individual velocity errors and covariance prevent the published weighted inverse regression. | Compute unweighted residual means as a sanity check. They differ from the published low/high zero points by 0.009 to 0.014 dex. Do not call this exact regression reproduction. |
| Direct a0(z) inference | No measured asymptotic speeds, radii, profiles or row errors are present. | Do not fit q or report a q interval. Report the proxy and required calibration contrasts. |
| Survey selection correction | Rejected objects and individual acceptance probabilities are absent. | Quantify sample attrition and fixed velocity-bin sensitivity only. |
| Fetch official ReadMe through web tool | Request timed out during this analysis. | Reuse the parent's verified catalogue contract and original official table. Do not replace input. |
| PDF visual extraction through web tool | Screenshot request failed. | Download author-hosted published PDF, extract text locally and visually inspect rendered pages 4 and 5. The source cache is excluded from publication. |

The rotation cut contains a square root. Plain PDF text extraction loses that symbol. The rendering of published page 4 confirms vrot,max/sigma0 > sqrt(4.4). Quoting a threshold of 4.4 without the root would misstate the sample.

The pressure-removal statistic is a sensitivity demonstration. The peak-radius approximation r=2.2Rd does not provide each galaxy's exact model rotation speed. The failure at Seq 6 remains unresolved without model outputs. No additional cut, imputation or tolerance adjustment was applied to the scientific sample.
