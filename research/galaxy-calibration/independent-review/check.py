#!/usr/bin/env python3
"""Independent KMOS parsing and contrast checks, with no author imports.

The input remains outside the review output. Only aggregate derived values and
hashes are written. Pass the separately obtained TSV as the first argument.
"""
import csv
import hashlib
import json
import math
from pathlib import Path
from statistics import mean, median
import sys

HERE=Path(__file__).resolve().parent
AUTHOR=HERE.parent


def main():
    path=Path(sys.argv[1])
    manifest=json.loads((AUTHOR/'public-manifest.json').read_text())
    hashes={}
    for f in manifest['files']:
        actual=hashlib.sha256((AUTHOR/f['path']).read_bytes()).hexdigest()
        assert actual==f['sha256'],f['path']
        hashes[f['path']]=actual
    lines=[ln for ln in path.read_text().splitlines() if ln.strip() and not ln.startswith('#')]
    header=next(csv.reader([lines[0]],delimiter='\t'))
    rows=[dict(zip(header,map(float,cells))) for cells in csv.reader(lines[3:],delimiter='\t')]
    canonical=hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
    assert canonical=='afadb1ef14ab6b88ce492f3fbf53d7d81e30fe178dcab6642aafdd1744c918f3'
    groups=[[r for r in rows if a<r['z']<b] for a,b in [(0,1.2),(1.2,1.8),(1.8,3)]]
    assert [len(g) for g in groups]==[65,24,46]
    def x(r):return .5*math.log10(.315*(1+r['z'])**3+.685)
    # Additive unit factors cancel, so compute the contrast directly in catalogue units.
    def y(r):return 4*math.log10(r['Vcirc'])-r['logMb']
    lo,hi=groups[0],groups[2]
    dx=mean(map(x,hi))-mean(map(x,lo))
    dy=mean(map(y,hi))-mean(map(y,lo))
    gas=mean(r['logMb']-r['logM*'] for r in hi)-mean(r['logMb']-r['logM*'] for r in lo)
    stellar=mean(4*math.log10(r['Vcirc'])-r['logM*'] for r in hi)-mean(4*math.log10(r['Vcirc'])-r['logM*'] for r in lo)
    assert abs(dy-(stellar-gas))<1e-13
    saved=json.loads((AUTHOR/'results/kmos-diagnostic.json').read_text())
    assert abs(dx-saved['primary_low_to_high']['delta_x'])<1e-13
    assert abs(dy-saved['primary_low_to_high']['delta_y_dex'])<1e-13
    contrasts={}
    for q in [0,1]:
        residue=dy-q*dx
        vr=math.pow(10,residue/4)
        mr=math.pow(10,-residue)
        assert abs(4*math.log10(vr)-residue)<1e-13
        assert abs(-math.log10(mr)-residue)<1e-13
        contrasts[str(q)]={'residue_dex':residue,'velocity_factor':vr,'mass_factor':mr}
    bins=[]
    for lower,upper in [(100,200),(200,300),(300,500)]:
        ll=[r for r in lo if lower<=r['Vcirc']<upper]
        hh=[r for r in hi if lower<=r['Vcirc']<upper]
        bins.append({'counts':[len(ll),len(hh)],'delta_y_dex':mean(map(y,hh))-mean(map(y,ll))})
    # A rounding-only enclosure is not a statistical confidence interval.
    def y_bounds(r):
        return (4*math.log10(r['Vcirc']-.05)-(r['logMb']+.005),
                4*math.log10(r['Vcirc']+.05)-(r['logMb']-.005))
    lower=mean(y_bounds(r)[0] for r in hi)-mean(y_bounds(r)[1] for r in lo)
    upper=mean(y_bounds(r)[1] for r in hi)-mean(y_bounds(r)[0] for r in lo)
    assert upper<0
    bad=[]
    for r in rows:
        frac=4.4*(r['sigma0']/r['Vcirc'])**2
        assert frac<1
        if frac>=.5:
            frac_min=4.4*((r['sigma0']-.05)/(r['Vcirc']+.05))**2
            frac_max=4.4*((r['sigma0']+.05)/(r['Vcirc']-.05))**2
            bad.append({'Seq':int(r['Seq']),'fraction':frac,'rounding_bounds':[frac_min,frac_max]})
    assert len(bad)==1 and bad[0]['Seq']==6 and bad[0]['rounding_bounds'][0]>.5
    # Common-intercept residual RMS reproduced separately.
    rms={}
    for q in [0,1]:
        residuals=[y(r)-q*x(r) for r in rows]
        center=mean(residuals)
        rms[str(q)]=math.sqrt(mean((z-center)**2 for z in residuals))
        assert abs(rms[str(q)]-saved['q_scores']['all_135'][str(q)]['descriptive_rms_dex'])<1e-13
    result={'source_hashes':hashes,'numeric_input_sha256':canonical,
            'delta_x':dx,'delta_y_dex':dy,'median_delta_y_dex':median(map(y,hi))-median(map(y,lo)),
            'stellar_delta_y_dex':stellar,'gas_algebraic_contribution_dex':gas,
            'calibration_contrasts':contrasts,'speed_bins':bins,
            'descriptive_rms':rms,
            'rounding_only_delta_y_enclosure_dex':[lower,upper],
            'rotation_cut_approximation_failures':bad,
            'disposition':'Point diagnostics reproduced. No likelihood, measurement of a0, or inference on q is established.'}
    (HERE/'evidence.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='source_hashes'},indent=2))


if __name__=='__main__':main()
