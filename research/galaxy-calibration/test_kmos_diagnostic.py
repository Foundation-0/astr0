"""Identity and input-boundary tests, not an uncertainty model."""
import math
from pathlib import Path
import tempfile
import unittest
import sys

import kmos_diagnostic as k


class DiagnosticIdentities(unittest.TestCase):
    def test_exact_synthetic_q_laws(self):
        for q in (0,1):
            low = [{'x':x,'y':-10+q*x} for x in (.20,.25,.30)]
            high = [{'x':x,'y':-10+q*x} for x in (.45,.50,.55)]
            d=k.contrast(low,high)['q_comparisons'][str(q)]
            self.assertAlmostEqual(d['observed_minus_predicted_dex'],0)
            self.assertAlmostEqual(d['required_Vpeak_over_Vflat_high_to_low_ratio_if_mass_exact'],1)
            self.assertAlmostEqual(d['required_Mtab_over_Mtrue_high_to_low_ratio_if_velocity_exact'],1)
            self.assertAlmostEqual(k.q_scores(low+high)[str(q)]['descriptive_rms_dex'],0)

    def test_calibration_drift_sign_and_fourth_power(self):
        # High Vpeak/Vflat is 0.8 times low; mass calibration is 1.2 times low.
        dx, q, vratio, mratio = .3, 1, .8, 1.2
        dy=q*dx+4*math.log10(vratio)-math.log10(mratio)
        d=k.contrast([{'x':0,'y':0}],[{'x':dx,'y':dy}])['q_comparisons']['1']
        self.assertAlmostEqual(d['required_Vpeak_over_Vflat_high_to_low_ratio_if_mass_exact'],vratio/mratio**.25)
        self.assertAlmostEqual(d['required_Mtab_over_Mtrue_high_to_low_ratio_if_velocity_exact'],mratio/vratio**4)

    def test_q_calibration_degeneracy(self):
        for x in (0,.2,.5):
            for dq in (-2,.731,1):
                q, cv, cm = .4,.03,.1
                original=q*x+4*cv-cm
                shifted=(q+dq)*x+4*(cv-dq*x/4)-cm
                self.assertAlmostEqual(original,shifted)

    def test_cosmology_and_bin_boundaries(self):
        self.assertEqual(k.evolution(0),1)
        self.assertEqual(k.group_name(1.199),'low')
        self.assertEqual(k.group_name(1.2),'mid')
        self.assertEqual(k.group_name(1.8),'high')


if __name__=='__main__': unittest.main()
